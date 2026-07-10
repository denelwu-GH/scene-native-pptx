#!/usr/bin/env python3
"""Fail when a public release tree contains common secrets or private paths."""

from __future__ import annotations

import argparse
import re
import zipfile
from pathlib import Path


TEXT_SUFFIXES = {
    ".css", ".html", ".js", ".json", ".md", ".mjs", ".py", ".sh",
    ".svg", ".txt", ".yaml", ".yml", ".xml",
}
EXCLUDED = {
    "PUBLICATION_AUDIT.md",
    "tools/audit_public_tree.py",
}
PATTERNS = {
    "private path": re.compile(r"(?:/Users/|/home/|/var/folders/|file://)", re.I),
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "OpenAI-style key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "Slack token": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b"),
    "assigned credential": re.compile(
        r"(?i)\b(?:api[_-]?key|access[_-]?token|secret|password)\b\s*[:=]\s*['\"][^'\"\s]{8,}['\"]"
    ),
}


def scan_text(label: str, text: str) -> list[str]:
    findings = []
    for name, pattern in PATTERNS.items():
        for match in pattern.finditer(text):
            line = text.count("\n", 0, match.start()) + 1
            findings.append(f"{label}:{line}: {name}")
    return findings


def scan_pptx(path: Path, relative: str) -> list[str]:
    findings = []
    with zipfile.ZipFile(path) as archive:
        bad = archive.testzip()
        if bad:
            findings.append(f"{relative}: corrupt ZIP entry {bad}")
        for name in archive.namelist():
            if name.endswith((".xml", ".rels", ".txt", ".json")):
                payload = archive.read(name).decode("utf-8", errors="replace")
                findings.extend(scan_text(f"{relative}!{name}", payload))
    return findings


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args()
    root = args.root.resolve()
    findings: list[str] = []

    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            findings.append(f"{path.relative_to(root)}: symbolic links are not allowed")
            continue
        if not path.is_file():
            continue
        relative = path.relative_to(root).as_posix()
        if relative in EXCLUDED or relative.startswith((".git/", "regression-output/", "regression-output-2/")):
            continue
        if path.suffix.lower() == ".pptx":
            findings.extend(scan_pptx(path, relative))
        elif path.suffix.lower() in TEXT_SUFFIXES:
            findings.extend(scan_text(relative, path.read_text(encoding="utf-8", errors="replace")))

    if findings:
        print("Public-tree audit failed:")
        print("\n".join(f"- {item}" for item in findings))
        raise SystemExit(1)
    print(f"Public-tree audit passed: {root}")


if __name__ == "__main__":
    main()
