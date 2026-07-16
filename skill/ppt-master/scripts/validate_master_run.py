#!/usr/bin/env python3
"""Validate PPT Master strategy, design, accessibility, and approval gates."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


MATURITY = {"public-verified", "internal-verified", "poc", "target-experience", "vision"}
CONTENT_POLICIES = {"exact", "rewritable", "visual-only"}
APPROVED = {"approved", "complete"}


def load_json(path: Path, errors: list[str]) -> dict:
    if not path.exists():
        errors.append(f"missing file: {path.name}")
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"invalid JSON {path.name}: {exc}")
        return {}
    if not isinstance(data, dict):
        errors.append(f"top-level JSON must be an object: {path.name}")
        return {}
    return data


def require_text(value, label: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"missing text: {label}")


def parse_hex(color: str) -> tuple[float, float, float] | None:
    if not isinstance(color, str) or not re.fullmatch(r"#[0-9A-Fa-f]{6}", color):
        return None
    values = tuple(int(color[index:index + 2], 16) / 255 for index in (1, 3, 5))
    return values


def luminance(color: tuple[float, float, float]) -> float:
    def linear(channel: float) -> float:
        return channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4
    red, green, blue = (linear(channel) for channel in color)
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue


def contrast_ratio(foreground: str, background: str) -> float | None:
    fg = parse_hex(foreground)
    bg = parse_hex(background)
    if fg is None or bg is None:
        return None
    light, dark = sorted((luminance(fg), luminance(bg)), reverse=True)
    return (light + 0.05) / (dark + 0.05)


def validate_brief(brief: dict, stage: str, errors: list[str]) -> None:
    deck = brief.get("deck", {})
    require_text(deck.get("name"), "deck-brief.deck.name", errors)
    require_text(deck.get("language"), "deck-brief.deck.language", errors)
    require_text(brief.get("route"), "deck-brief.route", errors)
    if stage in {"design", "delivery"}:
        for key in ("audience", "objective", "decision"):
            require_text(deck.get(key), f"deck-brief.deck.{key}", errors)
    constraints = brief.get("constraints")
    if not isinstance(constraints, dict):
        errors.append("deck-brief.constraints must be an object")
    elif stage in {"design", "delivery"}:
        for key in ("preserveSourceFiles", "preserveText", "preserveLayout", "allowedRewrite"):
            if not isinstance(constraints.get(key), bool):
                errors.append(f"deck-brief.constraints.{key} must be boolean")


def validate_storyline(storyline: dict, errors: list[str]) -> tuple[list[dict], set[str]]:
    slides = storyline.get("slides")
    if not isinstance(slides, list) or not slides:
        errors.append("storyline.slides must contain at least one slide")
        return [], set()
    ids: set[str] = set()
    titles: set[str] = set()
    for index, slide in enumerate(slides):
        label = f"storyline.slides[{index}]"
        if not isinstance(slide, dict):
            errors.append(f"{label} must be an object")
            continue
        slide_id = slide.get("id")
        require_text(slide_id, f"{label}.id", errors)
        if slide_id in ids:
            errors.append(f"duplicate storyline slide id: {slide_id}")
        ids.add(slide_id)
        for key in ("title", "role", "takeaway", "transition"):
            require_text(slide.get(key), f"{label}.{key}", errors)
        title = str(slide.get("title", "")).strip().casefold()
        if title and title in titles:
            errors.append(f"duplicate slide title: {slide.get('title')}")
        titles.add(title)
        if slide.get("evidenceClass") not in MATURITY:
            errors.append(f"invalid evidenceClass at {label}: {slide.get('evidenceClass')}")
    return slides, ids


def validate_claims(register: dict, slide_ids: set[str], errors: list[str], warnings: list[str]) -> set[str]:
    claims = register.get("claims")
    if not isinstance(claims, list):
        errors.append("claim-register.claims must be an array")
        return set()
    ids: set[str] = set()
    for index, claim in enumerate(claims):
        label = f"claim-register.claims[{index}]"
        if not isinstance(claim, dict):
            errors.append(f"{label} must be an object")
            continue
        claim_id = claim.get("id")
        require_text(claim_id, f"{label}.id", errors)
        if claim_id in ids:
            errors.append(f"duplicate claim id: {claim_id}")
        ids.add(claim_id)
        if claim.get("slideId") not in slide_ids:
            errors.append(f"claim references unknown slide: {claim.get('slideId')}")
        require_text(claim.get("statement"), f"{label}.statement", errors)
        require_text(claim.get("allowedWording"), f"{label}.allowedWording", errors)
        maturity = claim.get("maturity")
        if maturity not in MATURITY:
            errors.append(f"invalid claim maturity at {label}: {maturity}")
        evidence = claim.get("evidence", {})
        status = evidence.get("status")
        if status not in {"open", "closed"}:
            errors.append(f"{label}.evidence.status must be open or closed")
        if maturity in {"public-verified", "internal-verified"} and status != "closed":
            errors.append(f"verified claim has open evidence: {claim_id}")
        if status == "closed" and not evidence.get("sources"):
            errors.append(f"closed evidence has no sources: {claim_id}")
        if maturity in {"poc", "target-experience", "vision"} and not claim.get("visibleLabel"):
            errors.append(f"non-verified claim needs visibleLabel: {claim_id}")
        if maturity in {"target-experience", "vision"} and status == "closed":
            warnings.append(f"target or vision claim has closed evidence; verify the maturity label: {claim_id}")
    return ids


def validate_page_contracts(run_dir: Path, slide_ids: set[str], claim_ids: set[str], errors: list[str]) -> None:
    contract_dir = run_dir / "page-contracts"
    files = sorted(contract_dir.glob("*.json")) if contract_dir.exists() else []
    contracts: dict[str, dict] = {}
    for path in files:
        contract = load_json(path, errors)
        slide_id = contract.get("slideId")
        if slide_id in contracts:
            errors.append(f"duplicate page contract for {slide_id}")
        contracts[slide_id] = contract
    if set(contracts) != slide_ids:
        missing = sorted(slide_ids - set(contracts))
        extra = sorted(set(contracts) - slide_ids)
        if missing:
            errors.append(f"missing page contracts: {', '.join(missing)}")
        if extra:
            errors.append(f"page contracts without storyline slides: {', '.join(extra)}")

    for slide_id, contract in contracts.items():
        label = f"page-contracts/{slide_id}.json"
        for key in ("purpose", "takeaway", "storyRole", "visualPattern", "firstFocalPoint"):
            require_text(contract.get(key), f"{label}.{key}", errors)
        if contract.get("evidenceClass") not in MATURITY:
            errors.append(f"invalid evidenceClass in {label}")
        if contract.get("contentPolicy") not in CONTENT_POLICIES:
            errors.append(f"invalid contentPolicy in {label}")
        for claim_id in contract.get("claimIds", []):
            if claim_id not in claim_ids:
                errors.append(f"unknown claim id {claim_id} in {label}")
        accessibility = contract.get("accessibility", {})
        require_text(accessibility.get("title"), f"{label}.accessibility.title", errors)
        if not isinstance(accessibility.get("readingOrder"), list) or not accessibility.get("readingOrder"):
            errors.append(f"{label}.accessibility.readingOrder must not be empty")
        if not isinstance(accessibility.get("altText"), list):
            errors.append(f"{label}.accessibility.altText must be an array")
        if not contract.get("acceptanceCriteria"):
            errors.append(f"{label}.acceptanceCriteria must not be empty")


def validate_design_system(system: dict, errors: list[str], warnings: list[str]) -> None:
    tokens = system.get("tokens", {})
    for key in ("canvas", "grid", "colors", "typography", "spacing", "shape", "iconography", "chart"):
        if key not in tokens:
            errors.append(f"deck-design-system.tokens.{key} is required")
    accessibility = system.get("accessibility", {})
    min_body = accessibility.get("minBodyFontPt")
    if not isinstance(min_body, (int, float)) or min_body < 18:
        errors.append("deck-design-system.accessibility.minBodyFontPt must be at least 18")
    body_pt = tokens.get("typography", {}).get("bodyPt")
    if not isinstance(body_pt, (int, float)) or body_pt < min_body:
        errors.append("deck-design-system typography.bodyPt is below minBodyFontPt")
    pairs = accessibility.get("contrastPairs")
    if not isinstance(pairs, list) or not pairs:
        errors.append("deck-design-system.accessibility.contrastPairs must not be empty")
        return
    for index, pair in enumerate(pairs):
        foreground = pair.get("foreground")
        background = pair.get("background")
        minimum = pair.get("minimum", 4.5)
        ratio = contrast_ratio(foreground, background)
        if ratio is None:
            errors.append(f"invalid contrast color at contrastPairs[{index}]")
        elif ratio + 1e-9 < minimum:
            errors.append(
                f"contrast failure at contrastPairs[{index}]: {ratio:.2f}:1 < {minimum}:1"
            )
    if not system.get("components"):
        warnings.append("deck design system defines no reusable components")


def validate_manifest(manifest: dict, brief: dict, stage: str, errors: list[str]) -> None:
    if manifest.get("route") != brief.get("route"):
        errors.append("run-manifest.route does not match deck-brief.route")
    approvals = manifest.get("approvals", {})
    if stage in {"design", "delivery"} and approvals.get("strategy", {}).get("status") not in APPROVED:
        errors.append("strategy approval is required")
    if stage == "delivery" and approvals.get("design", {}).get("status") not in APPROVED:
        errors.append("design approval is required")
    if stage == "delivery":
        phases = manifest.get("phases", {})
        for phase in ("nativeProduction", "deliveryQa"):
            if phases.get(phase) not in APPROVED:
                errors.append(f"run-manifest.phases.{phase} must be complete for delivery")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--stage", choices=("draft", "design", "delivery"), default="draft")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    run_dir = args.run_dir.expanduser().resolve()
    errors: list[str] = []
    warnings: list[str] = []
    brief = load_json(run_dir / "deck-brief.json", errors)
    storyline = load_json(run_dir / "storyline.json", errors)
    claims = load_json(run_dir / "claim-register.json", errors)
    design_system = load_json(run_dir / "deck-design-system.json", errors)
    manifest = load_json(run_dir / "run-manifest.json", errors)

    validate_brief(brief, args.stage, errors)
    _, slide_ids = validate_storyline(storyline, errors)
    claim_ids = validate_claims(claims, slide_ids, errors, warnings)
    validate_page_contracts(run_dir, slide_ids, claim_ids, errors)
    validate_design_system(design_system, errors, warnings)
    validate_manifest(manifest, brief, args.stage, errors)

    result = {
        "runDir": str(run_dir),
        "stage": args.stage,
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
        "counts": {
            "slides": len(slide_ids),
            "claims": len(claim_ids),
        },
    }
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.report:
        target = args.report.expanduser().resolve()
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
