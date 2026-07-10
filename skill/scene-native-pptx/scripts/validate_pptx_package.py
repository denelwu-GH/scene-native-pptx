#!/usr/bin/env python3
"""Validate PPTX package integrity and common PowerPoint repair triggers."""

from __future__ import annotations

import argparse
import json
import posixpath
import re
import zipfile
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET


REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
P_NS = "http://schemas.openxmlformats.org/presentationml/2006/main"


def source_part_for_rels(name: str) -> str:
    if name == "_rels/.rels":
        return ""
    match = re.fullmatch(r"(.+)/_rels/([^/]+)\.rels", name)
    if not match:
        return ""
    return f"{match.group(1)}/{match.group(2)}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pptx", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    errors = []
    warnings = []
    slide_shape_counts = {}
    with zipfile.ZipFile(args.pptx) as archive:
        names = archive.namelist()
        name_set = set(names)
        duplicates = [name for name, count in Counter(names).items() if count > 1]
        if duplicates:
            errors.extend(f"duplicate ZIP entry: {name}" for name in duplicates)
        bad = archive.testzip()
        if bad:
            errors.append(f"corrupt ZIP entry: {bad}")

        for name in names:
            if not (name.endswith(".xml") or name.endswith(".rels")):
                continue
            try:
                root = ET.fromstring(archive.read(name))
            except ET.ParseError as exc:
                errors.append(f"invalid XML {name}: {exc}")
                continue

            if re.fullmatch(r"ppt/slides/slide\d+\.xml", name):
                ids = [node.get("id") for node in root.findall(f".//{{{P_NS}}}cNvPr")]
                duplicate_ids = [item for item, count in Counter(ids).items() if count > 1]
                if duplicate_ids:
                    errors.append(f"duplicate shape IDs in {name}: {duplicate_ids}")
                slide_shape_counts[name] = len(ids)

            if name.endswith(".rels"):
                source_part = source_part_for_rels(name)
                source_dir = posixpath.dirname(source_part)
                for relationship in root.findall(f"{{{REL_NS}}}Relationship"):
                    if relationship.get("TargetMode") == "External":
                        continue
                    target = relationship.get("Target", "")
                    resolved = target.lstrip("/") if target.startswith("/") else posixpath.normpath(posixpath.join(source_dir, target))
                    if resolved not in name_set:
                        errors.append(f"missing relationship target: {name} -> {target} ({resolved})")

        if "[Content_Types].xml" not in name_set:
            errors.append("missing [Content_Types].xml")
        if "ppt/presentation.xml" not in name_set:
            errors.append("missing ppt/presentation.xml")

    report = {
        "pptx": str(args.pptx),
        "size": args.pptx.stat().st_size,
        "slides": slide_shape_counts,
        "errors": errors,
        "warnings": warnings,
        "passed": not errors,
    }
    payload = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(payload, encoding="utf-8")
    print(payload, end="")
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
