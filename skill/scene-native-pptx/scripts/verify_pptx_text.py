#!/usr/bin/env python3
"""Verify that every design-contract text string appears in a PPTX package."""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


NS = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}


def normalize(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value)
    normalized = re.sub(r"[•·▪◦]", "", normalized)
    return re.sub(r"\s+", "", normalized)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pptx", type=Path)
    parser.add_argument("contract", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    contract = json.loads(args.contract.read_text(encoding="utf-8"))
    with zipfile.ZipFile(args.pptx) as archive:
        slide_names = sorted(
            name for name in archive.namelist()
            if re.fullmatch(r"ppt/slides/slide\d+\.xml", name)
        )
        runs = []
        for name in slide_names:
            root = ET.fromstring(archive.read(name))
            runs.extend(node.text or "" for node in root.findall(".//a:t", NS))

    ppt_text = normalize("".join(runs))
    missing = [item["id"] for item in contract.get("texts", []) if normalize(item.get("text", "")) not in ppt_text]
    report = {
        "pptx": str(args.pptx),
        "contract": str(args.contract),
        "slide_count": len(slide_names),
        "contract_text_count": len(contract.get("texts", [])),
        "missing": missing,
        "passed": not missing,
    }
    payload = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(payload, encoding="utf-8")
    print(payload, end="")
    if missing:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
