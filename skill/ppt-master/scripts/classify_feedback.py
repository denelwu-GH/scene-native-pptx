#!/usr/bin/env python3
"""Suggest whether presentation feedback is run, project, or user scoped."""

from __future__ import annotations

import argparse
import json
import re


PATTERNS = {
    "run": [
        r"这次", r"这一页", r"本页", r"当前页", r"当前这版", r"只改", r"不要动其他页",
        r"\bthis time\b", r"\bthis slide\b", r"\bcurrent deck\b", r"\bonly for this\b",
    ],
    "project": [
        r"这套(?:PPT|ppt|演示)", r"这个项目", r"本项目", r"品牌稿", r"品牌规范", r"项目内",
        r"\bthis project\b", r"\bthis brand\b", r"\bproject-wide\b", r"\bbrand guideline",
    ],
    "user": [
        r"以后", r"默认", r"每次", r"一直", r"总是", r"再也不要", r"所有(?:PPT|ppt)", r"记住我",
        r"\bfrom now on\b", r"\balways\b", r"\bnever again\b", r"\bmy default\b", r"\bremember my\b",
    ],
}


def classify(text: str) -> dict:
    matches: dict[str, list[str]] = {}
    for scope, patterns in PATTERNS.items():
        found = [pattern for pattern in patterns if re.search(pattern, text, flags=re.IGNORECASE)]
        if found:
            matches[scope] = found

    if not matches:
        scope = "review-required"
        confidence = 0.0
        reason = "No explicit scope marker was found. Keep this feedback local until clarified."
    elif len(matches) == 1:
        scope = next(iter(matches))
        confidence = min(0.95, 0.7 + 0.1 * len(matches[scope]))
        reason = f"Explicit {scope}-scope language was found. Persistence still requires user awareness."
    else:
        scope = "review-required"
        confidence = 0.4
        reason = "Conflicting scope markers were found. Do not persist without clarification."

    return {
        "text": text,
        "suggestedScope": scope,
        "confidence": confidence,
        "matchedScopes": sorted(matches),
        "reason": reason,
        "mayPersistAutomatically": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True)
    args = parser.parse_args()
    print(json.dumps(classify(args.text), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
