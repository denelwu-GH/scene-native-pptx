#!/usr/bin/env python3
"""Import an already-constrained SVG into the scene container for fixtures.

This is not the main image-to-scene authoring route; it exists for controlled
SVG imports and regression fixture preparation.
"""

from __future__ import annotations

import argparse
import json
import xml.etree.ElementTree as ET
from pathlib import Path


def local(tag: str) -> str:
    return tag.split("}", 1)[-1]


def attribute_name(name: str) -> str:
    if name.startswith("{http://www.w3.org/XML/1998/namespace}"):
        return f"xml:{local(name)}"
    if name.startswith("{http://www.w3.org/1999/xlink}"):
        return "href" if local(name) == "href" else local(name)
    return local(name)


def convert(element: ET.Element) -> dict:
    node = {
        "type": local(element.tag),
        "attrs": {attribute_name(key): value for key, value in element.attrib.items()},
    }
    children = []
    if element.text and element.text.strip():
        children.append({"type": "#text", "value": element.text})
    for child in element:
        children.append(convert(child))
        if child.tail and child.tail.strip():
            children.append({"type": "#text", "value": child.tail})
    if children:
        node["children"] = children
    return node


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--name", required=True)
    parser.add_argument("--source-reference", required=True)
    parser.add_argument("--mode", choices=["native-first", "hybrid-fidelity", "gorden-compat"], required=True)
    args = parser.parse_args()

    root = ET.parse(args.input).getroot()
    width = float(root.attrib.get("width", "0"))
    height = float(root.attrib.get("height", "0"))
    converted = [convert(child) for child in root]
    defs = next((item for item in converted if item["type"] == "defs"), None)
    layers = []
    for index, item in enumerate(converted):
        if item["type"] == "defs":
            continue
        if item["type"] == "g":
            item.setdefault("attrs", {}).setdefault("id", f"layer-{index + 1}")
            layers.append(item)
            continue
        layers.append({
            "type": "g",
            "attrs": {"id": f"root-{item['type']}-{index + 1}", "data-role": "imported-root"},
            "children": [item],
        })
    components = [
        {
            "id": layer.get("attrs", {}).get("id", f"layer-{index + 1}"),
            "type": "layer",
            "role": layer.get("attrs", {}).get("data-role", "imported-layer"),
            "zIndex": index,
            "editPolicy": "native" if args.mode == "native-first" else "hybrid",
        }
        for index, layer in enumerate(layers)
    ]
    scene = {
        "schemaVersion": "2.0.0",
        "mode": args.mode,
        "metadata": {
            "name": args.name,
            "sourceReference": args.source_reference,
            "sourceSvg": str(args.input.resolve()),
            "authoringRoute": "design contract -> scene.json -> constrained SVG -> native DrawingML PPTX",
            "editablePolicy": {"mode": args.mode},
        },
        "canvas": {
            "width": int(width) if width.is_integer() else width,
            "height": int(height) if height.is_integer() else height,
            "viewBox": root.attrib.get("viewBox", f"0 0 {width:g} {height:g}"),
            "units": "px",
        },
        "components": components,
        "svg": {
            "attrs": {local(key): value for key, value in root.attrib.items()} | {"xmlns": "http://www.w3.org/2000/svg"},
            "defs": defs,
            "layers": layers,
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(scene, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
