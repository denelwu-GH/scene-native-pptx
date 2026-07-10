#!/usr/bin/env python3
"""Create a clean deterministic ZIP from a scene-native-pptx run directory."""

from __future__ import annotations

import argparse
import zipfile
from pathlib import Path


EXCLUDED_PARTS = {".DS_Store", "__pycache__", "node_modules", ".git"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    root = args.run_dir.resolve()
    files = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if any(part in EXCLUDED_PARTS for part in relative.parts):
            continue
        if path.name.startswith("~$") or path.suffix in {".tmp", ".lock"}:
            continue
        files.append((relative, path))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(args.output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for relative, path in sorted(files):
            info = zipfile.ZipInfo(str(relative), date_time=(2020, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, path.read_bytes())
    print(args.output)


if __name__ == "__main__":
    main()
