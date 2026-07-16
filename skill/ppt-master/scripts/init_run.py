#!/usr/bin/env python3
"""Initialize an isolated PPT Master run from bundled templates."""

from __future__ import annotations

import argparse
import json
import shutil
import uuid
from datetime import datetime, timezone
from pathlib import Path


ROUTES = {"reconstruction-only", "restyle-existing", "strategy-to-native", "narrative-visual"}


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def replace_tokens(value, tokens: dict[str, str]):
    if isinstance(value, dict):
        return {key: replace_tokens(item, tokens) for key, item in value.items()}
    if isinstance(value, list):
        return [replace_tokens(item, tokens) for item in value]
    if isinstance(value, str):
        for token, replacement in tokens.items():
            value = value.replace(token, replacement)
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--deck-name", required=True)
    parser.add_argument("--slide-count", type=int, required=True)
    parser.add_argument("--route", choices=sorted(ROUTES), default="strategy-to-native")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    if args.slide_count < 1:
        raise SystemExit("--slide-count must be at least 1")

    skill_dir = Path(__file__).resolve().parent.parent
    templates = skill_dir / "assets" / "templates"
    run_dir = args.run_dir.expanduser().resolve()
    if run_dir.exists() and any(run_dir.iterdir()):
        if not args.force:
            raise SystemExit(f"run directory is not empty: {run_dir}; pass --force to replace it")
        shutil.rmtree(run_dir)

    for directory in ("page-contracts", "design", "native", "qa"):
        (run_dir / directory).mkdir(parents=True, exist_ok=True)

    now = datetime.now(timezone.utc).isoformat()
    tokens = {
        "__DECK_NAME__": args.deck_name,
        "__ROUTE__": args.route,
        "__RUN_ID__": str(uuid.uuid4()),
        "__CREATED_AT__": now,
    }

    for name in (
        "deck-brief.json",
        "storyline.json",
        "claim-register.json",
        "deck-design-system.json",
        "visual-bible.json",
        "run-manifest.json",
    ):
        data = replace_tokens(read_json(templates / name), tokens)
        write_json(run_dir / name, data)

    page_template = read_json(templates / "page-contract.json")
    for index in range(1, args.slide_count + 1):
        slide_id = f"slide-{index:02d}"
        data = replace_tokens(page_template, {"__SLIDE_ID__": slide_id})
        write_json(run_dir / "page-contracts" / f"{slide_id}.json", data)

    print(json.dumps({
        "runDir": str(run_dir),
        "route": args.route,
        "slides": args.slide_count,
        "runId": tokens["__RUN_ID__"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
