#!/usr/bin/env python3
"""Generate bilingual PPT Master workflow diagrams as deterministic SVG assets."""

from __future__ import annotations

import html
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "benchmarks" / "gallery"


COPY = {
    "en": {
        "title": "FROM SOURCE TO NATIVE POWERPOINT",
        "subtitle": "PPT Master thinks. Scene Native PPTX builds. PowerPoint verifies.",
        "badge": "TWO-SKILL SYSTEM",
        "start": "START ANYWHERE",
        "inputs": ["ONE-LINE BRIEF", "OLD DECK", "SOURCE DOCS", "DESIGN TARGET"],
        "master": "PPT MASTER",
        "modules": [
            ("STORYLINE", "Page roles and takeaways"),
            ("CLAIMS & EVIDENCE", "Verified, PoC, target, vision"),
            ("DESIGN SYSTEM", "Tokens, patterns, components"),
            ("USER PREFERENCES", "User, project, current run"),
        ],
        "core": "ORCHESTRATE",
        "gate": "APPROVAL GATE",
        "engine": "SCENE NATIVE ENGINE",
        "layers": ["DESIGN CONTRACT", "SCENE.JSON", "CONSTRAINED SVG", "DRAWINGML"],
        "output": "NATIVE PPTX",
        "editable": "EDITABLE",
        "qa": "REPAIR-FREE QA",
        "steps": ["UNDERSTAND", "STRUCTURE", "DESIGN", "APPROVE", "REBUILD", "VERIFY"],
    },
    "zh": {
        "title": "从原始资料到原生可编辑 POWERPOINT",
        "subtitle": "PPT Master 负责思考，Scene Native PPTX 负责构建，PowerPoint 负责最终验证。",
        "badge": "双 SKILL 系统",
        "start": "任何起点",
        "inputs": ["一句话需求", "旧版 PPT", "原始资料", "确认后的设计稿"],
        "master": "PPT MASTER",
        "modules": [
            ("故事线", "页面角色与一句话结论"),
            ("主张与证据", "已验证、PoC、目标、愿景"),
            ("整套设计系统", "Token、版式与组件"),
            ("用户偏好", "用户、项目、本次任务"),
        ],
        "core": "统一编排",
        "gate": "审批关卡",
        "engine": "SCENE NATIVE 引擎",
        "layers": ["设计合同", "SCENE.JSON", "受约束 SVG", "DRAWINGML"],
        "output": "原生 PPTX",
        "editable": "真正可编辑",
        "qa": "无修复提示验收",
        "steps": ["理解", "组织", "设计", "审批", "重建", "验证"],
    },
}


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def text(x: int, y: int, value: str, size: int, fill: str = "#F7FBFF", weight: int = 600,
         anchor: str = "start", spacing: int = 0, family: str = "Inter, Arial, sans-serif") -> str:
    return (
        f'<text x="{x}" y="{y}" fill="{fill}" font-family="{family}" font-size="{size}" '
        f'font-weight="{weight}" text-anchor="{anchor}" letter-spacing="{spacing}">{esc(value)}</text>'
    )


def card(x: int, y: int, w: int, h: int, title: str, subtitle: str | None = None,
         accent: str = "#22D3EE", family: str = "Inter, Arial, sans-serif") -> str:
    parts = [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="url(#panel)" stroke="#274866" stroke-width="2"/>',
        f'<rect x="{x}" y="{y}" width="5" height="{h}" rx="2.5" fill="{accent}"/>',
        f'<circle cx="{x + 28}" cy="{y + 30}" r="10" fill="#07111D" stroke="{accent}" stroke-width="2"/>',
        f'<circle cx="{x + 28}" cy="{y + 30}" r="3.5" fill="{accent}"/>',
        text(x + 49, y + 36, title, 20, "#F7FBFF", 700, family=family),
    ]
    if subtitle:
        parts.append(text(x + 20, y + 72, subtitle, 14, "#91A7BD", 500, family=family))
    return "\n".join(parts)


def build(locale: str) -> str:
    c = COPY[locale]
    family = "PingFang SC, Microsoft YaHei, Arial, sans-serif" if locale == "zh" else "Inter, Arial, sans-serif"
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="900" viewBox="0 0 1800 900">',
        '<defs>',
        '<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#03070D"/><stop offset="0.55" stop-color="#07111C"/><stop offset="1" stop-color="#04080E"/></linearGradient>',
        '<linearGradient id="panel" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#111D2A"/><stop offset="1" stop-color="#08121D"/></linearGradient>',
        '<radialGradient id="core"><stop offset="0" stop-color="#0EA5E9" stop-opacity="0.92"/><stop offset="0.52" stop-color="#075985" stop-opacity="0.78"/><stop offset="1" stop-color="#07111D"/></radialGradient>',
        '<pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="#163149" stroke-width="1" opacity="0.34"/></pattern>',
        '<filter id="glow" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>',
        '<marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="#38BDF8"/></marker>',
        '</defs>',
        '<rect width="1800" height="900" fill="url(#bg)"/>',
        '<rect width="1800" height="900" fill="url(#grid)"/>',
        '<path d="M0 122H1800" stroke="#17334A"/>',
        text(54, 64, c["title"], 38, "#F8FBFF", 800, family=family),
        text(56, 98, c["subtitle"], 18, "#91A7BD", 500, family=family),
        '<rect x="1496" y="42" width="250" height="48" rx="24" fill="#0A1C2B" stroke="#22D3EE" stroke-width="1.5"/>',
        '<circle cx="1523" cy="66" r="6" fill="#34D399"/>',
        text(1627, 73, c["badge"], 16, "#C9F7FF", 700, "middle", family=family),
        text(52, 165, c["start"], 17, "#67E8F9", 700, spacing=1, family=family),
    ]

    input_y = [198, 315, 432, 549]
    input_accents = ["#38BDF8", "#A78BFA", "#34D399", "#FBBF24"]
    for idx, (label, y, accent) in enumerate(zip(c["inputs"], input_y, input_accents), 1):
        parts.extend([
            f'<rect x="52" y="{y}" width="250" height="90" rx="10" fill="url(#panel)" stroke="#274866" stroke-width="2"/>',
            f'<rect x="52" y="{y}" width="5" height="90" rx="2.5" fill="{accent}"/>',
            f'<circle cx="84" cy="{y + 45}" r="19" fill="#07111D" stroke="{accent}" stroke-width="2"/>',
            text(84, y + 51, f"0{idx}", 13, accent, 800, "middle", family=family),
            text(116, y + 52, label, 18, "#F7FBFF", 700, family=family),
        ])
    parts.append('<path d="M302 395H342" stroke="#38BDF8" stroke-width="3" marker-end="url(#arrow)" filter="url(#glow)"/>')

    parts.extend([
        '<rect x="350" y="150" width="610" height="550" rx="14" fill="#07111D" fill-opacity="0.88" stroke="#1C6385" stroke-width="2"/>',
        text(380, 186, c["master"], 20, "#67E8F9", 800, spacing=1, family=family),
        '<rect x="808" y="165" width="120" height="30" rx="15" fill="#0B2C3D" stroke="#22D3EE"/>',
        text(868, 186, "STRATEGY", 12, "#A5F3FC", 800, "middle", spacing=1, family=family),
    ])
    module_positions = [(385, 220), (700, 220), (385, 515), (700, 515)]
    module_accents = ["#38BDF8", "#FBBF24", "#A78BFA", "#34D399"]
    for (module_title, subtitle), (x, y), accent in zip(c["modules"], module_positions, module_accents):
        parts.append(card(x, y, 225, 110, module_title, subtitle, accent, family))

    center_x, center_y = 655, 420
    for x, y in ((610, 330), (700, 330), (610, 515), (700, 515)):
        parts.append(f'<path d="M{x} {y}L{center_x} {center_y}" stroke="#2E6D91" stroke-width="2"/>')
    parts.extend([
        f'<circle cx="{center_x}" cy="{center_y}" r="91" fill="none" stroke="#155E75" stroke-width="2" stroke-dasharray="7 8"/>',
        f'<circle cx="{center_x}" cy="{center_y}" r="70" fill="url(#core)" stroke="#67E8F9" stroke-width="3" filter="url(#glow)"/>',
        f'<path d="M625 395L655 377L685 395L655 413Z M625 420L655 438L685 420 M625 444L655 462L685 444" fill="none" stroke="#E0F7FF" stroke-width="4" stroke-linejoin="round"/>',
        text(center_x, 492, c["core"], 15, "#DDFBFF", 800, "middle", spacing=1, family=family),
    ])

    parts.extend([
        '<path d="M960 420H1010" stroke="#38BDF8" stroke-width="3" marker-end="url(#arrow)" filter="url(#glow)"/>',
        '<line x1="995" y1="190" x2="995" y2="650" stroke="#FBBF24" stroke-width="2" stroke-dasharray="6 8" opacity="0.8"/>',
        f'<g transform="translate(1015 420) rotate(-90)">{text(0, 0, c["gate"], 14, "#FCD34D", 800, "middle", spacing=1, family=family)}</g>',
        '<rect x="1040" y="150" width="420" height="550" rx="14" fill="#07111D" fill-opacity="0.88" stroke="#245176" stroke-width="2"/>',
        text(1070, 186, c["engine"], 20, "#7DD3FC", 800, spacing=1, family=family),
        '<rect x="1315" y="165" width="112" height="30" rx="15" fill="#0A2A22" stroke="#34D399"/>',
        text(1371, 186, "NATIVE", 12, "#A7F3D0", 800, "middle", spacing=1, family=family),
    ])

    layer_y = [235, 330, 425, 520]
    layer_colors = ["#38BDF8", "#22D3EE", "#A78BFA", "#34D399"]
    layer_x = [1080, 1105, 1130, 1155]
    for idx, (label, y, accent, x) in enumerate(zip(c["layers"], layer_y, layer_colors, layer_x), 1):
        parts.extend([
            f'<rect x="{x}" y="{y}" width="250" height="72" rx="8" fill="url(#panel)" stroke="{accent}" stroke-width="2"/>',
            f'<circle cx="{x + 30}" cy="{y + 36}" r="16" fill="#07111D" stroke="{accent}" stroke-width="2"/>',
            text(x + 30, y + 42, str(idx), 13, accent, 800, "middle", family=family),
            text(x + 58, y + 43, label, 17, "#F7FBFF", 700, family=family),
        ])
        if idx < 4:
            parts.append(f'<path d="M{x + 125} {y + 72}V{y + 91}" stroke="#38BDF8" stroke-width="2" marker-end="url(#arrow)"/>')

    parts.extend([
        '<path d="M1460 420H1500" stroke="#38BDF8" stroke-width="3" marker-end="url(#arrow)" filter="url(#glow)"/>',
        '<rect x="1510" y="150" width="238" height="550" rx="14" fill="#07111D" fill-opacity="0.9" stroke="#2E6D91" stroke-width="2"/>',
        text(1629, 186, c["output"], 20, "#F8FBFF", 800, "middle", spacing=1, family=family),
        '<path d="M1560 235H1670L1700 265V480H1560Z" fill="url(#panel)" stroke="#D9E6F2" stroke-width="3"/>',
        '<path d="M1670 235V265H1700" fill="none" stroke="#D9E6F2" stroke-width="3"/>',
        '<rect x="1588" y="292" width="82" height="92" rx="10" fill="#D34B2A" stroke="#FFB199" stroke-width="2"/>',
        text(1629, 358, "P", 64, "#FFFFFF", 800, "middle", family="Arial, sans-serif"),
        '<circle cx="1630" cy="521" r="38" fill="#08271F" stroke="#34D399" stroke-width="3" filter="url(#glow)"/>',
        '<path d="M1608 521L1624 537L1653 505" fill="none" stroke="#6EE7B7" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>',
        text(1629, 594, c["editable"], 18, "#A7F3D0", 800, "middle", family=family),
        text(1629, 625, c["qa"], 14, "#91A7BD", 600, "middle", family=family),
    ])

    parts.extend([
        '<rect x="52" y="755" width="1696" height="92" rx="12" fill="#07111D" stroke="#245176" stroke-width="2"/>',
        '<line x1="155" y1="801" x2="1645" y2="801" stroke="#234A67" stroke-width="3"/>',
    ])
    step_x = [170, 455, 740, 1025, 1310, 1595]
    for idx, (label, x) in enumerate(zip(c["steps"], step_x), 1):
        accent = "#34D399" if idx == 6 else "#38BDF8"
        parts.extend([
            f'<circle cx="{x}" cy="801" r="18" fill="#081621" stroke="{accent}" stroke-width="3" filter="url(#glow)"/>',
            f'<circle cx="{x}" cy="801" r="5" fill="{accent}"/>',
            text(x, 833, f"0{idx}  {label}", 14, "#D8E7F3", 700, "middle", spacing=1, family=family),
        ])

    parts.append('</svg>')
    return "\n".join(parts) + "\n"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for locale, filename in (("en", "ppt-master-workflow.svg"), ("zh", "ppt-master-workflow.zh-CN.svg")):
        target = OUT / filename
        target.write_text(build(locale), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()
