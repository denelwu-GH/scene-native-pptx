#!/usr/bin/env python3
"""Inject constrained SVG slides into an Artifact Tool PPTX as DrawingML.

The script never imports python-pptx. It supports multiple slides and controlled
local media returned by the bundled standalone SVG converter.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import re
import sys
import types
import zipfile
from pathlib import Path


IMAGE_CONTENT_TYPES = {
    "png": "image/png",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "gif": "image/gif",
    "bmp": "image/bmp",
    "tif": "image/tiff",
    "tiff": "image/tiff",
    "webp": "image/webp",
    "svg": "image/svg+xml",
}


def load_converter(repo: Path):
    scripts = repo / "skills" / "ppt-master" / "scripts"
    package_dir = scripts / "svg_to_pptx"
    sys.path.insert(0, str(scripts))

    package = types.ModuleType("svg_to_pptx")
    package.__path__ = [str(package_dir)]
    package.__package__ = "svg_to_pptx"
    sys.modules["svg_to_pptx"] = package

    module = importlib.import_module("svg_to_pptx.drawingml.converter")
    return module.convert_svg_to_slide_shapes


def add_default(content_types: str, extension: str, content_type: str) -> str:
    if re.search(rf'<Default\s+Extension="{re.escape(extension)}"\b', content_types):
        return content_types
    node = f'<Default Extension="{extension}" ContentType="{content_type}"/>'
    return content_types.replace("</Types>", f"  {node}\n</Types>")


def add_override(content_types: str, part_name: str, content_type: str) -> str:
    normalized = part_name if part_name.startswith("/") else f"/{part_name}"
    if f'PartName="{normalized}"' in content_types:
        return content_types
    node = f'<Override PartName="{normalized}" ContentType="{content_type}"/>'
    return content_types.replace("</Types>", f"  {node}\n</Types>")


def relationships_xml(entries: list[dict[str, str]]) -> bytes:
    extra = "".join(
        f'\n  <Relationship Id="{item["id"]}" Type="{item["type"]}" Target="{item["target"]}"/>'
        for item in entries
    )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n'
        '  <Relationship Id="rId1" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" '
        f'Target="../slideLayouts/slideLayout1.xml"/>{extra}\n'
        '</Relationships>'
    ).encode("utf-8")


def main() -> None:
    skill_dir = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=skill_dir / "assets" / "ppt-master")
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--svg", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--trace", type=Path, required=True)
    parser.add_argument("--native-objects", action="store_true")
    args = parser.parse_args()

    convert = load_converter(args.repo)
    replacements: dict[str, bytes] = {}
    additions: dict[str, bytes] = {}
    defaults: dict[str, str] = {}
    overrides: dict[str, str] = {}
    slides_trace: list[dict] = []

    with zipfile.ZipFile(args.base, "r") as source:
        names = set(source.namelist())
        for index in range(1, len(args.svg) + 1):
            required = f"ppt/slides/slide{index}.xml"
            if required not in names:
                raise RuntimeError(
                    f"Base deck has fewer slides than requested: missing {required}. "
                    "Create the base with create_base_deck.mjs and the same slide count."
                )

    for slide_num, svg_path in enumerate(args.svg, start=1):
        trace: list[dict] = []
        slide_xml, media, rels, anim_targets, package_files, content_overrides = convert(
            svg_path,
            slide_num=slide_num,
            verbose=True,
            merge_paragraphs=False,
            image_optimize=False,
            native_objects=args.native_objects,
            trace_out=trace,
        )

        media_name_map: dict[str, str] = {}
        for media_name, media_data in media.items():
            extension = media_name.rsplit(".", 1)[-1].lower()
            digest = hashlib.sha256(media_data).hexdigest()[:16]
            final_name = f"s{slide_num}_{digest}.{extension}"
            media_name_map[media_name] = final_name
            additions[f"ppt/media/{final_name}"] = media_data
            defaults[extension] = IMAGE_CONTENT_TYPES.get(extension, f"image/{extension}")

        rewritten_rels = []
        for relationship in rels:
            item = dict(relationship)
            target = item.get("target", "")
            if target.startswith("../media/"):
                old_name = target.split("../media/", 1)[1]
                if old_name not in media_name_map:
                    raise RuntimeError(f"Missing converter media payload: {old_name}")
                item["target"] = f"../media/{media_name_map[old_name]}"
            rewritten_rels.append(item)

        replacements[f"ppt/slides/slide{slide_num}.xml"] = slide_xml.encode("utf-8")
        replacements[f"ppt/slides/_rels/slide{slide_num}.xml.rels"] = relationships_xml(rewritten_rels)

        for part_name, part_data in package_files.items():
            payload = part_data.encode("utf-8") if isinstance(part_data, str) else part_data
            existing = additions.get(part_name)
            if existing is not None and existing != payload:
                raise RuntimeError(f"Conflicting generated package part: {part_name}")
            additions[part_name] = payload
            extension = Path(part_name).suffix.lstrip(".").lower()
            if extension == "xlsx":
                defaults[extension] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

        overrides.update(content_overrides)
        slides_trace.append(
            {
                "slide_num": slide_num,
                "source_svg": str(svg_path.resolve()),
                "animation_targets": anim_targets,
                "media_files": sorted(media_name_map.values()),
                "trace": trace,
            }
        )

    with zipfile.ZipFile(args.base, "r") as source:
        content_types = source.read("[Content_Types].xml").decode("utf-8")
        for extension, content_type in sorted(defaults.items()):
            content_types = add_default(content_types, extension, content_type)
        for part_name, content_type in sorted(overrides.items()):
            content_types = add_override(content_types, part_name, content_type)
        replacements["[Content_Types].xml"] = content_types.encode("utf-8")

        args.output.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(args.output, "w", compression=zipfile.ZIP_DEFLATED) as target:
            written = set()
            for item in source.infolist():
                name = item.filename
                payload = replacements.get(name, source.read(name))
                target.writestr(item, payload)
                written.add(name)
            for name, payload in {**replacements, **additions}.items():
                if name not in written:
                    info = zipfile.ZipInfo(name, date_time=(2020, 1, 1, 0, 0, 0))
                    info.compress_type = zipfile.ZIP_DEFLATED
                    info.external_attr = 0o644 << 16
                    target.writestr(info, payload)

    args.trace.parent.mkdir(parents=True, exist_ok=True)
    args.trace.write_text(
        json.dumps(
            {
                "base_pptx": str(args.base.resolve()),
                "output_pptx": str(args.output.resolve()),
                "python_pptx_loaded": "pptx" in sys.modules,
                "slide_count": len(args.svg),
                "slides": slides_trace,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(args.output)


if __name__ == "__main__":
    main()
