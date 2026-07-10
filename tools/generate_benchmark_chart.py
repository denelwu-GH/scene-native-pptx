#!/usr/bin/env python3
"""Generate the public benchmark chart from benchmark-scores.json."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "benchmarks" / "benchmark-scores.json"
SVG_PATH = ROOT / "benchmarks" / "benchmark-comparison.svg"


def escape(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def main() -> None:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    routes = data["routes"]
    width, height = 1200, 620
    chart_x, chart_y, chart_w = 390, 146, 710
    row_h, bar_h = 78, 30
    palette = ["#94A3B8", "#38BDF8", "#64748B", "#2563EB", "#0F766E"]

    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="1200" height="620" rx="8" fill="#F8FAFC"/>',
        '<text x="54" y="62" font-family="Arial, sans-serif" font-size="30" font-weight="700" fill="#0F172A">Editable PPT reconstruction benchmark</text>',
        '<text x="54" y="94" font-family="Arial, sans-serif" font-size="15" fill="#475569">Weighted score: fidelity 30%, editability 25%, PowerPoint safety 20%, repeatability 15%, file efficiency 10%</text>',
    ]

    for tick in range(0, 11, 2):
        x = chart_x + chart_w * tick / 10
        parts.append(f'<line x1="{x:.1f}" y1="122" x2="{x:.1f}" y2="552" stroke="#E2E8F0" stroke-width="1"/>')
        parts.append(f'<text x="{x:.1f}" y="578" text-anchor="middle" font-family="Arial, sans-serif" font-size="13" fill="#64748B">{tick}</text>')

    for index, route in enumerate(routes):
        y = chart_y + index * row_h
        score = float(route["weightedScore"])
        fill = palette[index]
        bar_w = chart_w * score / 10
        weight = "700" if route["id"] == "scene-native" else "500"
        label = "Scene-native pipeline" if route["id"] == "scene-native" else route["label"]
        parts.append(
            f'<text x="54" y="{y + 21}" font-family="Arial, sans-serif" font-size="17" font-weight="{weight}" fill="#0F172A">{escape(label)}</text>'
        )
        parts.append(f'<rect x="{chart_x}" y="{y}" width="{chart_w}" height="{bar_h}" rx="6" fill="#E2E8F0"/>')
        parts.append(f'<rect x="{chart_x}" y="{y}" width="{bar_w:.1f}" height="{bar_h}" rx="6" fill="{fill}"/>')
        parts.append(f'<text x="{chart_x + bar_w - 10:.1f}" y="{y + 21}" text-anchor="end" font-family="Arial, sans-serif" font-size="15" font-weight="700" fill="#FFFFFF">{score:.1f}</text>')

    parts.extend([
        '<text x="54" y="598" font-family="Arial, sans-serif" font-size="12" fill="#64748B">Engineering benchmark, 2026-07-10. Scores combine measured artifacts with documented review criteria.</text>',
        '</svg>',
        '',
    ])
    SVG_PATH.write_text("\n".join(parts), encoding="utf-8")
    print(SVG_PATH)


if __name__ == "__main__":
    main()
