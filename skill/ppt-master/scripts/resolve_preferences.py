#!/usr/bin/env python3
"""Resolve user, project, and run preferences with explicit precedence."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def read_preferences(path: Path | None) -> tuple[dict, str | None]:
    if path is None:
        return {}, None
    expanded = path.expanduser().resolve()
    if not expanded.exists():
        return {}, None
    data = json.loads(expanded.read_text(encoding="utf-8"))
    preferences = data.get("preferences", {})
    if not isinstance(preferences, dict):
        raise ValueError(f"preferences must be an object: {expanded}")
    return preferences, str(expanded)


def deep_merge(base: dict, override: dict) -> dict:
    result = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--user", type=Path)
    parser.add_argument("--project", type=Path)
    parser.add_argument("--run", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    resolved: dict = {}
    sources: list[dict] = []
    for scope, path in (("user", args.user), ("project", args.project), ("run", args.run)):
        preferences, actual_path = read_preferences(path)
        if actual_path:
            resolved = deep_merge(resolved, preferences)
            sources.append({"scope": scope, "path": actual_path})

    output = {
        "schemaVersion": "1.0.0",
        "resolvedAt": datetime.now(timezone.utc).isoformat(),
        "precedence": ["skill-defaults", "user", "project", "run", "current-explicit-instruction"],
        "sources": sources,
        "preferences": resolved,
    }
    target = args.output.expanduser().resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
