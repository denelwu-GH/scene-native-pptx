#!/usr/bin/env python3
"""Generate deterministic, public-safe regression fixtures for the skill."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skill" / "scene-native-pptx"
REGRESSION = SKILL / "assets" / "regression"
W, H = 1600, 900


def node(kind: str, attrs: dict | None = None, children: list | None = None) -> dict:
    return {"type": kind, "attrs": attrs or {}, "children": children or []}


def raw_text(value: str) -> dict:
    return {"type": "#text", "value": value}


def text_node(
    text_id: str,
    x: float,
    y: float,
    value: str,
    size: int,
    color: str = "#0F172A",
    weight: int = 500,
    anchor: str = "start",
) -> dict:
    return node(
        "text",
        {
            "id": f"shape-{text_id}",
            "data-text-id": text_id,
            "x": x,
            "y": y,
            "font-family": "Arial",
            "font-size": size,
            "font-weight": weight,
            "fill": color,
            "text-anchor": anchor,
            "letter-spacing": 0,
        },
        [raw_text(value)],
    )


def rect(x: float, y: float, w: float, h: float, **attrs) -> dict:
    base = {"x": x, "y": y, "width": w, "height": h}
    base.update(attrs)
    return node("rect", base)


def circle(cx: float, cy: float, r: float, **attrs) -> dict:
    base = {"cx": cx, "cy": cy, "r": r}
    base.update(attrs)
    return node("circle", base)


def line(x1: float, y1: float, x2: float, y2: float, **attrs) -> dict:
    base = {"x1": x1, "y1": y1, "x2": x2, "y2": y2}
    base.update(attrs)
    return node("line", base)


def contract_text(text_id: str, value: str, bbox: list[int], size: int, weight: int = 500, color: str = "#0F172A") -> dict:
    return {
        "id": text_id,
        "text": value,
        "role": "label",
        "bbox": bbox,
        "font": {"family": "Arial", "size": size, "weight": weight, "color": color},
    }


def base_defs() -> dict:
    return node("defs", {}, [
        node("linearGradient", {"id": "bg", "x1": "0", "y1": "0", "x2": "1", "y2": "1"}, [
            node("stop", {"offset": "0", "stop-color": "#FFFFFF"}),
            node("stop", {"offset": "0.58", "stop-color": "#F8FAFC"}),
            node("stop", {"offset": "1", "stop-color": "#EEF6FF"}),
        ]),
        node("linearGradient", {"id": "accent", "x1": "0", "y1": "0", "x2": "1", "y2": "1"}, [
            node("stop", {"offset": "0", "stop-color": "#22D3EE"}),
            node("stop", {"offset": "0.55", "stop-color": "#2563EB"}),
            node("stop", {"offset": "1", "stop-color": "#1E3A8A"}),
        ]),
        node("radialGradient", {"id": "hub-gradient", "cx": "35%", "cy": "28%", "r": "75%"}, [
            node("stop", {"offset": "0", "stop-color": "#67E8F9"}),
            node("stop", {"offset": "0.48", "stop-color": "#2563EB"}),
            node("stop", {"offset": "1", "stop-color": "#172554"}),
        ]),
        node("filter", {"id": "shadow", "x": "-20%", "y": "-20%", "width": "140%", "height": "150%"}, [
            node("feGaussianBlur", {"in": "SourceAlpha", "stdDeviation": "7"}),
            node("feOffset", {"dx": "0", "dy": "5", "result": "off"}),
            node("feFlood", {"flood-color": "#0F3F78", "flood-opacity": "0.15"}),
            node("feComposite", {"in2": "off", "operator": "in"}),
            node("feMerge", {}, [node("feMergeNode"), node("feMergeNode", {"in": "SourceGraphic"})]),
        ]),
    ])


def write_fixture(name: str, scene: dict, contract: dict) -> None:
    target = REGRESSION / name
    target.mkdir(parents=True, exist_ok=True)
    (target / "scene.json").write_text(json.dumps(scene, indent=2) + "\n", encoding="utf-8")
    (target / "design-contract.json").write_text(json.dumps(contract, indent=2) + "\n", encoding="utf-8")


def build_native_fixture() -> None:
    texts: list[dict] = []
    layers: list[dict] = []
    layers.append(node("g", {"id": "background", "data-role": "background"}, [
        rect(0, 0, W, H, fill="url(#bg)"),
        circle(790, 445, 270, fill="none", stroke="#BFDBFE", **{"stroke-width": 1, "stroke-dasharray": "8 10"}),
        circle(790, 445, 210, fill="none", stroke="#DBEAFE", **{"stroke-width": 1}),
    ]))

    header = [
        text_node("title", 62, 66, "Orchestration Control Plane", 38, "#0F172A", 700),
        text_node("subtitle", 62, 101, "From trusted signals to coordinated service actions", 18, "#475569", 500),
        rect(1372, 46, 166, 38, rx=19, fill="#E0F2FE", stroke="#7DD3FC", **{"stroke-width": 1}),
        text_node("status", 1455, 71, "NATIVE FIRST", 13, "#0369A1", 700, "middle"),
    ]
    layers.append(node("g", {"id": "header", "data-role": "title-area"}, header))
    texts.extend([
        contract_text("title", "Orchestration Control Plane", [62, 30, 760, 50], 38, 700),
        contract_text("subtitle", "From trusted signals to coordinated service actions", [62, 76, 720, 30], 18, 500, "#475569"),
        contract_text("status", "NATIVE FIRST", [1382, 48, 146, 34], 13, 700, "#0369A1"),
    ])

    input_specs = [
        ("01", "Live telemetry", "Health, capacity, context"),
        ("02", "User request", "Intent, priority, constraints"),
        ("03", "Policy signals", "Consent, risk, availability"),
    ]
    input_children = []
    for index, (number, title, desc) in enumerate(input_specs):
        y = 176 + index * 176
        input_children.extend([
            rect(62, y, 330, 132, rx=14, fill="#FFFFFF", stroke="#BFDBFE", **{"stroke-width": 1.4, "filter": "url(#shadow)"}),
            circle(112, y + 48, 27, fill="#EFF6FF", stroke="#60A5FA", **{"stroke-width": 1.5}),
            text_node(f"input-number-{index}", 112, y + 54, number, 15, "#2563EB", 700, "middle"),
            text_node(f"input-title-{index}", 157, y + 48, title, 20, "#0F172A", 700),
            text_node(f"input-desc-{index}", 157, y + 78, desc, 14, "#64748B", 500),
            line(392, y + 66, 566, 445, stroke="#60A5FA", **{"stroke-width": 3, "stroke-linecap": "round"}),
        ])
        texts.extend([
            contract_text(f"input-number-{index}", number, [87, y + 28, 50, 35], 15, 700, "#2563EB"),
            contract_text(f"input-title-{index}", title, [157, y + 24, 210, 32], 20, 700),
            contract_text(f"input-desc-{index}", desc, [157, y + 58, 210, 26], 14, 500, "#64748B"),
        ])
    layers.append(node("g", {"id": "inputs", "data-role": "input-cards"}, input_children))

    hub_children = [
        circle(790, 445, 152, fill="#EFF6FF", stroke="#BFDBFE", **{"stroke-width": 2}),
        circle(790, 445, 127, fill="none", stroke="#60A5FA", **{"stroke-width": 4, "stroke-dasharray": "14 9"}),
        circle(790, 445, 102, fill="url(#hub-gradient)", stroke="#22D3EE", **{"stroke-width": 5, "filter": "url(#shadow)"}),
        rect(748, 395, 84, 72, rx=14, fill="none", stroke="#FFFFFF", **{"stroke-width": 5}),
        line(764, 415, 816, 415, stroke="#FFFFFF", **{"stroke-width": 5, "stroke-linecap": "round"}),
        line(764, 433, 803, 433, stroke="#FFFFFF", **{"stroke-width": 5, "stroke-linecap": "round"}),
        text_node("hub-title", 790, 515, "POLICY ENGINE", 16, "#FFFFFF", 700, "middle"),
        text_node("hub-desc", 790, 541, "Plan  |  route  |  verify", 13, "#DBEAFE", 500, "middle"),
    ]
    texts.extend([
        contract_text("hub-title", "POLICY ENGINE", [690, 492, 200, 28], 16, 700, "#FFFFFF"),
        contract_text("hub-desc", "Plan  |  route  |  verify", [670, 520, 240, 24], 13, 500, "#DBEAFE"),
    ])
    layers.append(node("g", {"id": "hub", "data-role": "decision-hub"}, hub_children))

    output_specs = [
        ("Route work", "Match the best available capability"),
        ("Guard action", "Apply policy before execution"),
        ("Report state", "Return outcome and confidence"),
    ]
    output_children = []
    for index, (title, desc) in enumerate(output_specs):
        y = 176 + index * 176
        output_children.extend([
            line(1014, 445, 1168, y + 66, stroke="#22D3EE", **{"stroke-width": 4, "stroke-linecap": "round"}),
            circle(1168, y + 66, 7, fill="#22D3EE"),
            rect(1176, y, 362, 132, rx=14, fill="#FFFFFF", stroke="#A5F3FC", **{"stroke-width": 1.4, "filter": "url(#shadow)"}),
            circle(1226, y + 48, 27, fill="#ECFEFF", stroke="#2DD4BF", **{"stroke-width": 1.5}),
            node("path", {"d": f"M1213 {y + 48} L1222 {y + 57} L1240 {y + 38}", "fill": "none", "stroke": "#0F766E", "stroke-width": 4, "stroke-linecap": "round", "stroke-linejoin": "round"}),
            text_node(f"output-title-{index}", 1270, y + 48, title, 20, "#0F172A", 700),
            text_node(f"output-desc-{index}", 1270, y + 78, desc, 14, "#64748B", 500),
        ])
        texts.extend([
            contract_text(f"output-title-{index}", title, [1270, y + 24, 245, 32], 20, 700),
            contract_text(f"output-desc-{index}", desc, [1270, y + 58, 245, 26], 14, 500, "#64748B"),
        ])
    layers.append(node("g", {"id": "outputs", "data-role": "output-cards"}, output_children))

    metrics = [("12 ms", "Decision latency"), ("99.9%", "Trace coverage"), ("4", "Policy gates"), ("0", "Raster layers")]
    metric_children = []
    for index, (value, label) in enumerate(metrics):
        x = 62 + index * 378
        metric_children.extend([
            rect(x, 738, 344, 112, rx=12, fill="#FFFFFF", stroke="#CBD5E1", **{"stroke-width": 1.2}),
            rect(x, 738, 8, 112, rx=4, fill="#2563EB" if index < 3 else "#0F766E"),
            text_node(f"metric-value-{index}", x + 28, 785, value, 28, "#0F172A", 700),
            text_node(f"metric-label-{index}", x + 28, 817, label, 14, "#64748B", 500),
        ])
        texts.extend([
            contract_text(f"metric-value-{index}", value, [x + 28, 752, 180, 38], 28, 700),
            contract_text(f"metric-label-{index}", label, [x + 28, 795, 240, 26], 14, 500, "#64748B"),
        ])
    layers.append(node("g", {"id": "metrics", "data-role": "metric-strip"}, metric_children))

    scene = {
        "schemaVersion": "1.0.0",
        "mode": "native-first",
        "metadata": {"name": "Synthetic orchestration control plane", "sourceReference": "reference.png", "editablePolicy": {"mode": "native-first", "images": "none"}},
        "canvas": {"width": W, "height": H, "viewBox": f"0 0 {W} {H}", "units": "px"},
        "components": [{"id": "inputs"}, {"id": "hub"}, {"id": "outputs"}, {"id": "metrics"}],
        "svg": {"attrs": {"xmlns": "http://www.w3.org/2000/svg", "width": W, "height": H, "viewBox": f"0 0 {W} {H}"}, "defs": base_defs(), "layers": layers},
    }
    contract = {
        "schemaVersion": "1.0.0",
        "metadata": {"name": "Synthetic orchestration control plane", "sourceReference": "reference.png"},
        "mode": "native-first",
        "canvas": {"width": W, "height": H, "units": "px"},
        "regions": [
            {"id": "region-header", "role": "title-area", "bbox": [50, 24, 1500, 90], "z": 10},
            {"id": "region-inputs", "role": "input-cards", "bbox": [50, 160, 360, 520], "z": 20},
            {"id": "region-hub", "role": "decision-hub", "bbox": [560, 210, 460, 470], "z": 30},
            {"id": "region-outputs", "role": "output-cards", "bbox": [1150, 160, 400, 520], "z": 20},
            {"id": "region-metrics", "role": "metric-strip", "bbox": [50, 720, 1500, 145], "z": 20},
        ],
        "texts": texts,
        "assets": [],
        "connectors": [
            {"id": "connector-input-flow", "from": "region-inputs", "to": "region-hub", "routing": "fan-in"},
            {"id": "connector-output-flow", "from": "region-hub", "to": "region-outputs", "routing": "fan-out"},
        ],
    }
    write_fixture("sample-01", scene, contract)


def draw_icon(path: Path, kind: str, color: tuple[int, int, int, int]) -> None:
    image = Image.new("RGBA", (180, 180), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((12, 12, 168, 168), radius=38, fill=(245, 250, 255, 255), outline=(191, 219, 254, 255), width=4)
    c = color
    if kind == "map":
        draw.polygon([(50, 55), (88, 38), (128, 56), (128, 126), (90, 142), (50, 124)], outline=c, width=9)
        draw.line([(88, 40), (88, 140)], fill=c, width=7)
        draw.line([(52, 58), (126, 126)], fill=c, width=7)
    elif kind == "media":
        draw.rounded_rectangle((45, 50, 135, 130), radius=12, outline=c, width=9)
        draw.polygon([(80, 73), (80, 108), (112, 90)], fill=c)
    elif kind == "shield":
        draw.polygon([(90, 35), (137, 55), (130, 112), (90, 145), (50, 112), (43, 55)], outline=c, fill=(255, 255, 255, 0))
        draw.line([(68, 90), (84, 106), (116, 70)], fill=c, width=9)
    elif kind == "chart":
        draw.line([(48, 132), (48, 52)], fill=c, width=8)
        draw.line([(48, 132), (136, 132)], fill=c, width=8)
        draw.rectangle((65, 91, 80, 128), fill=c)
        draw.rectangle((91, 70, 106, 128), fill=c)
        draw.rectangle((117, 49, 132, 128), fill=c)
    else:
        draw.ellipse((52, 38, 128, 114), outline=c, width=9)
        draw.line([(90, 114), (90, 143)], fill=c, width=9)
        draw.line([(68, 143), (112, 143)], fill=c, width=9)
    image.save(path)


def build_hybrid_fixture() -> None:
    target = REGRESSION / "sample-02"
    assets_dir = target / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    icon_specs = [
        ("map.png", "map", (37, 99, 235, 255)),
        ("media.png", "media", (8, 145, 178, 255)),
        ("shield.png", "shield", (15, 118, 110, 255)),
        ("chart.png", "chart", (79, 70, 229, 255)),
    ]
    for filename, kind, color in icon_specs:
        draw_icon(assets_dir / filename, kind, color)

    texts: list[dict] = []
    layers: list[dict] = [
        node("g", {"id": "background", "data-role": "background"}, [rect(0, 0, W, H, fill="url(#bg)")]),
        node("g", {"id": "header", "data-role": "title-area"}, [
            text_node("title", 62, 66, "Media-Rich Service Journey", 38, "#0F172A", 700),
            text_node("subtitle", 62, 101, "Native layout with isolated, replaceable artwork", 18, "#475569", 500),
            rect(1360, 46, 178, 38, rx=19, fill="#CCFBF1", stroke="#5EEAD4", **{"stroke-width": 1}),
            text_node("status", 1449, 71, "HYBRID MODE", 13, "#0F766E", 700, "middle"),
        ]),
    ]
    texts.extend([
        contract_text("title", "Media-Rich Service Journey", [62, 30, 760, 50], 38, 700),
        contract_text("subtitle", "Native layout with isolated, replaceable artwork", [62, 76, 720, 30], 18, 500, "#475569"),
        contract_text("status", "HYBRID MODE", [1370, 48, 158, 34], 13, 700, "#0F766E"),
    ])

    stages = [
        ("Discover", "Understand the request", "assets/map.png"),
        ("Compose", "Assemble the response", "assets/media.png"),
        ("Protect", "Apply policy checks", "assets/shield.png"),
        ("Measure", "Capture the outcome", "assets/chart.png"),
    ]
    stage_children = []
    for index, (title, desc, href) in enumerate(stages):
        x = 62 + index * 378
        stage_children.extend([
            rect(x, 170, 344, 258, rx=16, fill="#FFFFFF", stroke="#CBD5E1", **{"stroke-width": 1.2, "filter": "url(#shadow)"}),
            node("image", {"id": f"art-{index}", "href": href, "x": x + 90, "y": 194, "width": 164, "height": 164}),
            text_node(f"stage-title-{index}", x + 172, 380, title, 22, "#0F172A", 700, "middle"),
            text_node(f"stage-desc-{index}", x + 172, 406, desc, 14, "#64748B", 500, "middle"),
        ])
        if index < len(stages) - 1:
            stage_children.extend([
                line(x + 344, 298, x + 378, 298, stroke="#38BDF8", **{"stroke-width": 5, "stroke-linecap": "round"}),
                node("polygon", {"points": f"{x + 370},288 {x + 382},298 {x + 370},308", "fill": "#38BDF8"}),
            ])
        texts.extend([
            contract_text(f"stage-title-{index}", title, [x + 72, 354, 200, 32], 22, 700),
            contract_text(f"stage-desc-{index}", desc, [x + 48, 386, 248, 26], 14, 500, "#64748B"),
        ])
    layers.append(node("g", {"id": "journey", "data-role": "service-stages"}, stage_children))

    panel_children = [
        rect(62, 476, 1476, 252, rx=16, fill="#FFFFFF", stroke="#BFDBFE", **{"stroke-width": 1.4, "filter": "url(#shadow)"}),
        rect(62, 476, 12, 252, rx=6, fill="url(#accent)"),
        text_node("panel-title", 104, 523, "The semantic layout stays editable", 26, "#0F172A", 700),
        text_node("panel-body", 104, 558, "Artwork is isolated into four local image objects; titles, cards, arrows, metrics, and callouts remain native PowerPoint content.", 16, "#475569", 500),
    ]
    metrics = [("4", "replaceable assets"), ("100%", "editable text"), ("0", "remote URLs")]
    for index, (value, label) in enumerate(metrics):
        x = 104 + index * 420
        panel_children.extend([
            rect(x, 606, 372, 88, rx=10, fill="#F8FAFC", stroke="#E2E8F0", **{"stroke-width": 1}),
            text_node(f"metric-value-{index}", x + 24, 646, value, 26, "#0F766E" if index == 2 else "#2563EB", 700),
            text_node(f"metric-label-{index}", x + 124, 646, label, 15, "#475569", 500),
        ])
        texts.extend([
            contract_text(f"metric-value-{index}", value, [x + 24, 617, 60, 38], 26, 700),
            contract_text(f"metric-label-{index}", label, [x + 124, 624, 210, 28], 15, 500, "#475569"),
        ])
    texts.extend([
        contract_text("panel-title", "The semantic layout stays editable", [104, 493, 760, 40], 26, 700),
        contract_text("panel-body", "Artwork is isolated into four local image objects; titles, cards, arrows, metrics, and callouts remain native PowerPoint content.", [104, 536, 1320, 32], 16, 500, "#475569"),
    ])
    layers.append(node("g", {"id": "explanation", "data-role": "hybrid-policy"}, panel_children))

    footer = [
        rect(62, 770, 1476, 80, rx=12, fill="#0F172A"),
        text_node("footer-title", 104, 807, "Hybrid fidelity rule", 18, "#FFFFFF", 700),
        text_node("footer-body", 310, 807, "Rasterize only the artwork that cannot be represented safely in DrawingML.", 16, "#CBD5E1", 500),
    ]
    texts.extend([
        contract_text("footer-title", "Hybrid fidelity rule", [104, 786, 180, 30], 18, 700, "#FFFFFF"),
        contract_text("footer-body", "Rasterize only the artwork that cannot be represented safely in DrawingML.", [310, 786, 980, 30], 16, 500, "#CBD5E1"),
    ])
    layers.append(node("g", {"id": "footer", "data-role": "takeaway"}, footer))

    scene = {
        "schemaVersion": "1.0.0",
        "mode": "hybrid-fidelity",
        "metadata": {"name": "Synthetic hybrid service journey", "sourceReference": "reference.png", "editablePolicy": {"mode": "hybrid-fidelity", "images": "isolated-local"}},
        "canvas": {"width": W, "height": H, "viewBox": f"0 0 {W} {H}", "units": "px"},
        "components": [{"id": "journey"}, {"id": "explanation"}, {"id": "footer"}],
        "svg": {"attrs": {"xmlns": "http://www.w3.org/2000/svg", "width": W, "height": H, "viewBox": f"0 0 {W} {H}"}, "defs": base_defs(), "layers": layers},
    }
    contract = {
        "schemaVersion": "1.0.0",
        "metadata": {"name": "Synthetic hybrid service journey", "sourceReference": "reference.png"},
        "mode": "hybrid-fidelity",
        "canvas": {"width": W, "height": H, "units": "px"},
        "regions": [
            {"id": "region-header", "role": "title-area", "bbox": [50, 24, 1500, 90], "z": 10},
            {"id": "region-journey", "role": "service-stages", "bbox": [50, 150, 1500, 300], "z": 20},
            {"id": "region-policy", "role": "hybrid-policy", "bbox": [50, 460, 1500, 290], "z": 20},
            {"id": "region-footer", "role": "takeaway", "bbox": [50, 755, 1500, 110], "z": 20},
        ],
        "texts": texts,
        "assets": [
            {"id": f"asset-{index}", "kind": "illustration", "semantic": title.lower(), "bbox": [62 + index * 378 + 90, 194, 164, 164], "policy": "local-raster-png"}
            for index, (title, _desc, _href) in enumerate(stages)
        ],
        "connectors": [
            {"id": "connector-stage-flow", "from": "region-journey", "to": "region-policy", "routing": "left-to-right"}
        ],
    }
    write_fixture("sample-02", scene, contract)


def showcase_defs() -> dict:
    return node("defs", {}, [
        node("linearGradient", {"id": "bg", "x1": "0", "y1": "0", "x2": "1", "y2": "1"}, [
            node("stop", {"offset": "0", "stop-color": "#030712"}),
            node("stop", {"offset": "0.55", "stop-color": "#071A37"}),
            node("stop", {"offset": "1", "stop-color": "#020617"}),
        ]),
        node("linearGradient", {"id": "panel", "x1": "0", "y1": "0", "x2": "1", "y2": "1"}, [
            node("stop", {"offset": "0", "stop-color": "#14284B"}),
            node("stop", {"offset": "1", "stop-color": "#091426"}),
        ]),
        node("linearGradient", {"id": "electric", "x1": "0", "y1": "0", "x2": "1", "y2": "0"}, [
            node("stop", {"offset": "0", "stop-color": "#20D9FF"}),
            node("stop", {"offset": "0.58", "stop-color": "#3B82F6"}),
            node("stop", {"offset": "1", "stop-color": "#7C3AED"}),
        ]),
        node("radialGradient", {"id": "core-gradient", "cx": "35%", "cy": "28%", "r": "78%"}, [
            node("stop", {"offset": "0", "stop-color": "#7DEBFF"}),
            node("stop", {"offset": "0.45", "stop-color": "#147BFF"}),
            node("stop", {"offset": "1", "stop-color": "#0A1C55"}),
        ]),
        node("filter", {"id": "shadow", "x": "-25%", "y": "-25%", "width": "150%", "height": "160%"}, [
            node("feGaussianBlur", {"in": "SourceAlpha", "stdDeviation": "8"}),
            node("feOffset", {"dx": "0", "dy": "6", "result": "off"}),
            node("feFlood", {"flood-color": "#01040D", "flood-opacity": "0.65"}),
            node("feComposite", {"in2": "off", "operator": "in"}),
            node("feMerge", {}, [node("feMergeNode"), node("feMergeNode", {"in": "SourceGraphic"})]),
        ]),
    ])


def add_showcase_text(
    children: list[dict],
    texts: list[dict],
    text_id: str,
    x: float,
    y: float,
    value: str,
    size: int,
    color: str,
    weight: int = 500,
    anchor: str = "start",
    bbox: list[int] | None = None,
) -> None:
    children.append(text_node(text_id, x, y, value, size, color, weight, anchor))
    if bbox is None:
        bbox = [int(x), int(y - size), max(100, int(len(value) * size * 0.72)), int(size * 1.45)]
    texts.append(contract_text(text_id, value, bbox, size, weight, color))


def build_native_showcase_fixture() -> None:
    texts: list[dict] = []
    layers: list[dict] = [
        node("g", {"id": "background", "data-role": "background"}, [
            rect(0, 0, W, H, fill="url(#bg)"),
            circle(804, 440, 300, fill="none", stroke="#1C4E86", **{"stroke-width": 1, "stroke-dasharray": "6 16", "opacity": "0.72"}),
            circle(804, 440, 242, fill="none", stroke="#164273", **{"stroke-width": 1, "opacity": "0.85"}),
            line(64, 686, 1536, 686, stroke="#16365E", **{"stroke-width": 1}),
        ]),
    ]

    header: list[dict] = []
    add_showcase_text(header, texts, "title", 64, 78, "Autonomous Decision Fabric", 42, "#F7FBFF", 700, bbox=[64, 34, 760, 56])
    add_showcase_text(header, texts, "subtitle", 64, 112, "Signals enter. Decisions coordinate. Outcomes verify.", 18, "#94A9C8", 500, bbox=[64, 92, 680, 30])
    header.extend([
        rect(1326, 46, 210, 42, rx=21, fill="#0A2547", stroke="#249BFF", **{"stroke-width": 1}),
        circle(1350, 67, 6, fill="#34D399"),
    ])
    add_showcase_text(header, texts, "status", 1425, 73, "ALL NATIVE", 14, "#CDEEFF", 700, "middle", [1342, 51, 178, 28])
    layers.append(node("g", {"id": "header", "data-role": "title-area"}, header))

    connector_children: list[dict] = []
    for y in (260, 402, 544):
        connector_children.extend([
            node("path", {"d": f"M418 {y} H548 C590 {y} 602 440 642 440", "fill": "none", "stroke": "#2374DC", "stroke-width": 3, "stroke-linecap": "round"}),
            node("path", {"d": f"M966 440 C1006 440 1018 {y} 1060 {y} H1138", "fill": "none", "stroke": "#28C7F7", "stroke-width": 3, "stroke-linecap": "round"}),
            circle(548, y, 5, fill="#249BFF"),
            circle(1060, y, 5, fill="#32D7F4"),
        ])
    layers.append(node("g", {"id": "connectors", "data-role": "connector-layer"}, connector_children))

    signal_specs = [
        ("01", "LIVE SIGNALS", "Context, capacity, events", "#25D6FF"),
        ("02", "INTENT MODEL", "Priority, constraints, goals", "#7AA2FF"),
        ("03", "POLICY", "Consent, risk, control", "#7CDBB5"),
    ]
    signal_children: list[dict] = []
    for index, (number, title, desc, color) in enumerate(signal_specs):
        y = 214 + index * 142
        signal_children.extend([
            rect(64, y, 354, 92, rx=14, fill="url(#panel)", stroke="#285585", **{"stroke-width": 1.2, "filter": "url(#shadow)"}),
            circle(106, y + 46, 22, fill="#0A274A", stroke=color, **{"stroke-width": 1.5}),
            line(98, y + 46, 114, y + 46, stroke=color, **{"stroke-width": 3, "stroke-linecap": "round"}),
            line(106, y + 38, 106, y + 54, stroke=color, **{"stroke-width": 3, "stroke-linecap": "round"}),
        ])
        add_showcase_text(signal_children, texts, f"signal-number-{index}", 146, y + 34, number, 13, color, 700, bbox=[146, y + 18, 36, 22])
        add_showcase_text(signal_children, texts, f"signal-title-{index}", 146, y + 58, title, 19, "#F7FBFF", 700, bbox=[146, y + 40, 214, 26])
        add_showcase_text(signal_children, texts, f"signal-desc-{index}", 146, y + 80, desc, 14, "#91A8C8", 500, bbox=[146, y + 65, 220, 20])
    layers.append(node("g", {"id": "signals", "data-role": "signal-inputs"}, signal_children))

    core_children: list[dict] = [
        circle(804, 440, 168, fill="#071A37", stroke="#214F84", **{"stroke-width": 2}),
        circle(804, 440, 145, fill="none", stroke="#2F83DE", **{"stroke-width": 6, "stroke-dasharray": "18 12"}),
        circle(804, 440, 118, fill="url(#core-gradient)", stroke="#4EE7FF", **{"stroke-width": 3, "filter": "url(#shadow)"}),
        node("polygon", {"points": "804,334 875,382 804,430 733,382", "fill": "none", "stroke": "#E4F7FF", "stroke-width": 4, "stroke-linejoin": "round"}),
        node("polygon", {"points": "804,366 875,414 804,462 733,414", "fill": "none", "stroke": "#8FCEFF", "stroke-width": 4, "stroke-linejoin": "round"}),
        node("polygon", {"points": "804,398 875,446 804,494 733,446", "fill": "none", "stroke": "#54DCFF", "stroke-width": 4, "stroke-linejoin": "round"}),
    ]
    add_showcase_text(core_children, texts, "core-label", 804, 530, "DECISION CORE", 15, "#EAF7FF", 700, "middle", [672, 512, 264, 26])
    add_showcase_text(core_children, texts, "core-desc", 804, 554, "interpret  ·  coordinate  ·  verify", 13, "#A6C2E4", 500, "middle", [642, 538, 324, 24])
    layers.append(node("g", {"id": "core", "data-role": "decision-core"}, core_children))

    outcome_specs = [
        ("01", "ROUTE THE WORK", "Best-fit capability selected", "#28C7F7"),
        ("02", "Govern", "Policy applied before execution", "#7AA2FF"),
        ("03", "VERIFY", "Outcome and trace delivered", "#7CDBB5"),
    ]
    outcome_children: list[dict] = []
    for index, (number, title, desc, color) in enumerate(outcome_specs):
        y = 214 + index * 142
        outcome_children.extend([
            rect(1138, y, 398, 92, rx=14, fill="url(#panel)", stroke="#285585", **{"stroke-width": 1.2, "filter": "url(#shadow)"}),
            rect(1160, y + 23, 44, 44, rx=10, fill="#0A274A", stroke=color, **{"stroke-width": 1.3}),
            node("path", {"d": f"M1172 {y + 46} L1182 {y + 56} L1195 {y + 36}", "fill": "none", "stroke": color, "stroke-width": 4, "stroke-linecap": "round", "stroke-linejoin": "round"}),
        ])
        add_showcase_text(outcome_children, texts, f"outcome-number-{index}", 1225, y + 34, number, 13, color, 700, bbox=[1225, y + 18, 36, 22])
        add_showcase_text(outcome_children, texts, f"outcome-title-{index}", 1225, y + 58, title, 18, "#F7FBFF", 700, bbox=[1225, y + 40, 280, 26])
        add_showcase_text(outcome_children, texts, f"outcome-desc-{index}", 1225, y + 80, desc, 14, "#91A8C8", 500, bbox=[1225, y + 65, 282, 20])
    layers.append(node("g", {"id": "outcomes", "data-role": "verified-outcomes"}, outcome_children))

    footer: list[dict] = [
        rect(64, 736, 1472, 104, rx=14, fill="#071426", stroke="#234C7B", **{"stroke-width": 1.2}),
        rect(64, 736, 6, 104, rx=3, fill="url(#electric)"),
    ]
    metric_specs = [("12 ms", "decision latency"), ("99.9%", "trace coverage"), ("0", "raster layers")]
    for index, (value, label) in enumerate(metric_specs):
        x = 116 + index * 294
        footer.extend([circle(x, 788, 20, fill="#0C3159", stroke="#2ED9FF", **{"stroke-width": 1.2}), circle(x, 788, 6, fill="#2ED9FF")])
        add_showcase_text(footer, texts, f"metric-value-{index}", x + 34, 782, value, 24, "#F7FBFF", 700, bbox=[x + 34, 758, 120, 32])
        add_showcase_text(footer, texts, f"metric-label-{index}", x + 34, 810, label, 14, "#8EA6C8", 500, bbox=[x + 34, 794, 150, 22])
    footer.extend([line(1032, 756, 1032, 820, stroke="#234C7B", **{"stroke-width": 1})])
    add_showcase_text(footer, texts, "footer-label", 1070, 777, "EDIT THE LOGIC,", 16, "#7EB7FF", 700, bbox=[1070, 758, 190, 24])
    add_showcase_text(footer, texts, "footer-emphasis", 1070, 808, "NOT THE PIXELS.", 23, "#F7FBFF", 700, bbox=[1070, 786, 310, 34])
    layers.append(node("g", {"id": "metrics", "data-role": "metric-strip"}, footer))

    scene = {
        "schemaVersion": "1.0.0",
        "mode": "native-first",
        "metadata": {"name": "Autonomous decision fabric", "sourceReference": "reference.png", "editablePolicy": {"mode": "native-first", "images": "none"}},
        "canvas": {"width": W, "height": H, "viewBox": f"0 0 {W} {H}", "units": "px"},
        "components": [{"id": "signals"}, {"id": "core"}, {"id": "outcomes"}, {"id": "metrics"}],
        "svg": {"attrs": {"xmlns": "http://www.w3.org/2000/svg", "width": W, "height": H, "viewBox": f"0 0 {W} {H}"}, "defs": showcase_defs(), "layers": layers},
    }
    contract = {
        "schemaVersion": "1.0.0",
        "metadata": {"name": "Autonomous decision fabric", "sourceReference": "reference.png"},
        "mode": "native-first",
        "canvas": {"width": W, "height": H, "units": "px"},
        "regions": [
            {"id": "header", "role": "title-area", "bbox": [64, 36, 1472, 90], "z": 10},
            {"id": "signals", "role": "signal-inputs", "bbox": [64, 214, 354, 376], "z": 20},
            {"id": "core", "role": "decision-core", "bbox": [636, 272, 336, 300], "z": 30},
            {"id": "outcomes", "role": "verified-outcomes", "bbox": [1138, 214, 398, 376], "z": 20},
            {"id": "metrics", "role": "metric-strip", "bbox": [64, 736, 1472, 104], "z": 20},
        ],
        "texts": texts,
        "assets": [],
        "connectors": [
            {"id": "signal-flow", "from": "signals", "to": "core", "routing": "orthogonal"},
            {"id": "outcome-flow", "from": "core", "to": "outcomes", "routing": "orthogonal"},
        ],
    }
    write_fixture("sample-01", scene, contract)


def build_hybrid_showcase_fixture() -> None:
    texts: list[dict] = []
    layers: list[dict] = [
        node("g", {"id": "background", "data-role": "background"}, [
            rect(0, 0, W, H, fill="url(#bg)"),
            circle(292, 414, 350, fill="none", stroke="#163C69", **{"stroke-width": 1, "stroke-dasharray": "6 16", "opacity": "0.7"}),
            line(64, 686, 1536, 686, stroke="#16365E", **{"stroke-width": 1}),
        ]),
    ]
    header: list[dict] = []
    add_showcase_text(header, texts, "title", 64, 78, "Hybrid Intelligence Studio", 42, "#F7FBFF", 700, bbox=[64, 34, 700, 56])
    add_showcase_text(header, texts, "subtitle", 64, 112, "Native structure with one isolated, replaceable visual asset.", 18, "#94A9C8", 500, bbox=[64, 92, 780, 30])
    header.extend([rect(1290, 46, 246, 42, rx=21, fill="#13243F", stroke="#8B5CF6", **{"stroke-width": 1}), circle(1314, 67, 6, fill="#C084FC")])
    add_showcase_text(header, texts, "status", 1412, 73, "HYBRID FIDELITY", 14, "#EEE3FF", 700, "middle", [1327, 51, 170, 28])
    layers.append(node("g", {"id": "header", "data-role": "title-area"}, header))

    media: list[dict] = [
        rect(64, 184, 706, 420, rx=22, fill="#051226", stroke="#2A5B91", **{"stroke-width": 1.4, "filter": "url(#shadow)"}),
        rect(82, 202, 670, 340, rx=16, fill="#020814", stroke="#245B9B", **{"stroke-width": 1}),
        node("image", {"id": "orchestration-artwork", "href": "assets/orchestration-artwork.png", "x": 82, "y": 202, "width": 670, "height": 340}),
        rect(104, 558, 164, 28, rx=14, fill="#102F57", stroke="#2ED9FF", **{"stroke-width": 1}),
        circle(122, 572, 5, fill="#34D399"),
    ]
    add_showcase_text(media, texts, "asset-label", 190, 577, "ISOLATED ARTWORK", 12, "#D7F4FF", 700, "middle", [130, 561, 125, 20])
    add_showcase_text(media, texts, "asset-note", 738, 577, "1 local PNG · swap without touching layout", 13, "#91A8C8", 500, "end", [405, 560, 330, 22])
    layers.append(node("g", {"id": "artwork", "data-role": "isolated-artwork"}, media))

    flow: list[dict] = [node("path", {"d": "M846 252 H890 V536 H846", "fill": "none", "stroke": "#347CC4", "stroke-width": 2, "stroke-linecap": "round"})]
    stage_specs = [
        ("01", "Frame", "Cards, connectors, text", "#2ED9FF"),
        ("02", "Isolate", "Artwork is local and replaceable", "#A78BFA"),
        ("03", "Deliver", "Open, edit, present", "#7CDBB5"),
    ]
    for index, (number, title, desc, color) in enumerate(stage_specs):
        y = 198 + index * 132
        flow.extend([
            rect(914, y, 622, 108, rx=16, fill="url(#panel)", stroke="#2A5586", **{"stroke-width": 1.2, "filter": "url(#shadow)"}),
            rect(938, y + 24, 56, 56, rx=14, fill="#0B274A", stroke=color, **{"stroke-width": 1.4}),
            circle(966, y + 52, 12, fill="none", stroke=color, **{"stroke-width": 3}),
            line(954, y + 52, 978, y + 52, stroke=color, **{"stroke-width": 2.5, "stroke-linecap": "round"}),
        ])
        add_showcase_text(flow, texts, f"stage-number-{index}", 1024, y + 39, number, 13, color, 700, bbox=[1024, y + 22, 36, 22])
        add_showcase_text(flow, texts, f"stage-title-{index}", 1024, y + 64, title, 16, "#F7FBFF", 700, bbox=[1024, y + 44, 220, 24])
        add_showcase_text(flow, texts, f"stage-desc-{index}", 1164, y + 66, desc, 15, "#A2B7D5", 500, bbox=[1164, y + 48, 320, 24])
    layers.append(node("g", {"id": "flow", "data-role": "hybrid-flow"}, flow))

    footer: list[dict] = [
        rect(64, 736, 1472, 104, rx=14, fill="#071426", stroke="#234C7B", **{"stroke-width": 1.2}),
        rect(64, 736, 6, 104, rx=3, fill="#8B5CF6"),
    ]
    metric_specs = [("1", "replaceable artwork"), ("100%", "editable text"), ("0", "full-slide bitmaps")]
    for index, (value, label) in enumerate(metric_specs):
        x = 116 + index * 315
        footer.extend([circle(x, 788, 20, fill="#19254B", stroke="#A78BFA" if index == 0 else "#2ED9FF", **{"stroke-width": 1.2}), circle(x, 788, 6, fill="#C4B5FD" if index == 0 else "#2ED9FF")])
        add_showcase_text(footer, texts, f"metric-value-{index}", x + 34, 782, value, 24, "#F7FBFF", 700, bbox=[x + 34, 758, 100, 32])
        add_showcase_text(footer, texts, f"metric-label-{index}", x + 34, 810, label, 14, "#8EA6C8", 500, bbox=[x + 34, 794, 176, 22])
    footer.extend([line(1074, 756, 1074, 820, stroke="#234C7B", **{"stroke-width": 1})])
    add_showcase_text(footer, texts, "footer-label", 1112, 777, "KEEP THE ART.", 16, "#C4B5FD", 700, bbox=[1112, 758, 200, 24])
    add_showcase_text(footer, texts, "footer-emphasis", 1112, 808, "EDIT EVERYTHING ELSE.", 21, "#F7FBFF", 700, bbox=[1112, 786, 340, 32])
    layers.append(node("g", {"id": "metrics", "data-role": "hybrid-metrics"}, footer))

    scene = {
        "schemaVersion": "1.0.0",
        "mode": "hybrid-fidelity",
        "metadata": {"name": "Hybrid intelligence studio", "sourceReference": "reference.png", "editablePolicy": {"mode": "hybrid-fidelity", "images": "isolated-local"}},
        "canvas": {"width": W, "height": H, "viewBox": f"0 0 {W} {H}", "units": "px"},
        "components": [{"id": "artwork"}, {"id": "flow"}, {"id": "metrics"}],
        "svg": {"attrs": {"xmlns": "http://www.w3.org/2000/svg", "width": W, "height": H, "viewBox": f"0 0 {W} {H}"}, "defs": showcase_defs(), "layers": layers},
    }
    contract = {
        "schemaVersion": "1.0.0",
        "metadata": {"name": "Hybrid intelligence studio", "sourceReference": "reference.png"},
        "mode": "hybrid-fidelity",
        "canvas": {"width": W, "height": H, "units": "px"},
        "regions": [
            {"id": "header", "role": "title-area", "bbox": [64, 36, 1472, 90], "z": 10},
            {"id": "artwork", "role": "isolated-artwork", "bbox": [64, 184, 706, 420], "z": 20},
            {"id": "flow", "role": "hybrid-flow", "bbox": [846, 198, 690, 374], "z": 20},
            {"id": "metrics", "role": "hybrid-metrics", "bbox": [64, 736, 1472, 104], "z": 20},
        ],
        "texts": texts,
        "assets": [
            {"id": "orchestration-artwork", "kind": "illustration", "semantic": "orchestration-core", "bbox": [82, 202, 670, 340], "policy": "local-raster-png"},
        ],
        "connectors": [{"id": "hybrid-flow", "from": "artwork", "to": "flow", "routing": "left-to-right"}],
    }
    write_fixture("sample-02", scene, contract)


def main() -> None:
    REGRESSION.mkdir(parents=True, exist_ok=True)
    build_native_showcase_fixture()
    build_hybrid_showcase_fixture()
    print(REGRESSION)


if __name__ == "__main__":
    main()
