#!/usr/bin/env python3
"""Normalize PPTX package metadata before committing a public template."""

from __future__ import annotations

import argparse
import re
import tempfile
import zipfile
from pathlib import Path


FIXED_TIME = (2020, 1, 1, 0, 0, 0)


def replace_tag(xml: str, tag: str, value: str) -> str:
    pattern = rf"(<{re.escape(tag)}(?:\s[^>]*)?>).*?(</{re.escape(tag)}>)"
    return re.sub(pattern, lambda match: f"{match.group(1)}{value}{match.group(2)}", xml, flags=re.DOTALL)


def sanitize(path: Path) -> None:
    with zipfile.ZipFile(path, "r") as source:
        entries = [(item.filename, source.read(item.filename)) for item in source.infolist()]

    normalized = []
    for name, payload in entries:
        if name == "docProps/core.xml":
            xml = payload.decode("utf-8")
            xml = replace_tag(xml, "dc:creator", "scene-native-pptx")
            xml = replace_tag(xml, "cp:lastModifiedBy", "scene-native-pptx")
            xml = replace_tag(xml, "lastModifiedBy", "scene-native-pptx")
            xml = replace_tag(xml, "cp:revision", "1")
            xml = replace_tag(xml, "revision", "1")
            xml = replace_tag(xml, "dcterms:created", "2025-01-01T00:00:00Z")
            xml = replace_tag(xml, "dcterms:modified", "2025-01-01T00:00:00Z")
            payload = xml.encode("utf-8")
        elif name == "docProps/app.xml":
            xml = payload.decode("utf-8")
            xml = replace_tag(xml, "ap:Application", "scene-native-pptx")
            xml = replace_tag(xml, "ap:PresentationFormat", "Widescreen")
            payload = xml.encode("utf-8")
        normalized.append((name, payload))

    with tempfile.NamedTemporaryFile(dir=path.parent, suffix=".pptx", delete=False) as handle:
        temporary = Path(handle.name)
    try:
        with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED) as target:
            for name, payload in normalized:
                info = zipfile.ZipInfo(name, date_time=FIXED_TIME)
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o644 << 16
                target.writestr(info, payload)
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pptx", nargs="+", type=Path)
    args = parser.parse_args()
    for path in args.pptx:
        sanitize(path)
        print(path)


if __name__ == "__main__":
    main()
