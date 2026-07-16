#!/usr/bin/env python3
"""Run deterministic regression checks for PPT Master."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


def run(command: list[str], expect_success: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, text=True, capture_output=True)
    if expect_success and result.returncode != 0:
        raise RuntimeError(f"command failed: {' '.join(command)}\n{result.stdout}\n{result.stderr}")
    if not expect_success and result.returncode == 0:
        raise RuntimeError(f"command unexpectedly passed: {' '.join(command)}")
    return result


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    skill = args.skill_dir.resolve()
    output = args.output_dir.resolve()
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    scripts = skill / "scripts"
    assets = skill / "assets"
    checks: list[dict] = []

    initialized = output / "initialized-run"
    init_result = run([
        sys.executable,
        str(scripts / "init_run.py"),
        "--run-dir", str(initialized),
        "--deck-name", "Initialization Test",
        "--slide-count", "3",
        "--route", "restyle-existing",
    ])
    init_data = json.loads(init_result.stdout)
    page_count = len(list((initialized / "page-contracts").glob("*.json")))
    if init_data["slides"] != 3 or page_count != 3:
        raise RuntimeError("run initialization created the wrong page count")
    checks.append({"name": "run-initialization", "passed": True, "slides": page_count})

    resolved_path = output / "resolved-preferences.json"
    pref_dir = assets / "regression" / "preferences"
    run([
        sys.executable,
        str(scripts / "resolve_preferences.py"),
        "--user", str(pref_dir / "user.json"),
        "--project", str(pref_dir / "project.json"),
        "--run", str(pref_dir / "run.json"),
        "--output", str(resolved_path),
    ])
    preferences = json.loads(resolved_path.read_text(encoding="utf-8"))["preferences"]
    expected = {
        "language": "zh-CN",
        "informationDensity": "high",
        "palette": {"accent": "#1565D8"},
        "forbiddenStyles": ["purple gradients"],
        "delivery": {"nativeEditable": True},
        "typography": {"family": "PingFang SC"},
        "preserveLayout": True,
    }
    if preferences != expected:
        raise RuntimeError(f"preference precedence mismatch: {preferences}")
    checks.append({"name": "preference-precedence", "passed": True})

    feedback_cases = {
        "以后所有PPT都不要用紫色渐变": "user",
        "这套PPT统一使用品牌红": "project",
        "这一页不要改布局": "run",
        "我觉得卡片有点多": "review-required",
    }
    for text, expected_scope in feedback_cases.items():
        result = run([sys.executable, str(scripts / "classify_feedback.py"), "--text", text])
        actual = json.loads(result.stdout)
        if actual["suggestedScope"] != expected_scope or actual["mayPersistAutomatically"]:
            raise RuntimeError(f"feedback classification mismatch for {text}: {actual}")
    checks.append({"name": "feedback-classification", "passed": True, "cases": len(feedback_cases)})

    good = output / "good-run"
    shutil.copytree(assets / "regression" / "good-run", good)
    design_system = json.loads((assets / "templates" / "deck-design-system.json").read_text(encoding="utf-8"))
    design_system["components"] = [{"id": "page-title", "role": "title"}]
    write_json(good / "deck-design-system.json", design_system)
    shutil.copy2(assets / "templates" / "visual-bible.json", good / "visual-bible.json")
    good_result = run([
        sys.executable,
        str(scripts / "validate_master_run.py"),
        str(good),
        "--stage", "delivery",
        "--report", str(output / "good-run-report.json"),
    ])
    if not json.loads(good_result.stdout)["passed"]:
        raise RuntimeError("good run did not pass delivery validation")
    checks.append({"name": "delivery-gate-good-run", "passed": True})

    low_contrast = output / "bad-low-contrast"
    shutil.copytree(good, low_contrast)
    low_system = json.loads((low_contrast / "deck-design-system.json").read_text(encoding="utf-8"))
    low_system["accessibility"]["contrastPairs"][0]["foreground"] = "#AAAAAA"
    write_json(low_contrast / "deck-design-system.json", low_system)
    low_result = run([
        sys.executable,
        str(scripts / "validate_master_run.py"),
        str(low_contrast),
        "--stage", "delivery",
    ], expect_success=False)
    if "contrast failure" not in low_result.stdout:
        raise RuntimeError("low contrast failure was not reported")
    checks.append({"name": "accessibility-low-contrast-block", "passed": True})

    open_claim = output / "bad-open-verified-claim"
    shutil.copytree(good, open_claim)
    claims = json.loads((open_claim / "claim-register.json").read_text(encoding="utf-8"))
    claims["claims"][0]["evidence"] = {"status": "open", "sources": []}
    write_json(open_claim / "claim-register.json", claims)
    claim_result = run([
        sys.executable,
        str(scripts / "validate_master_run.py"),
        str(open_claim),
        "--stage", "delivery",
    ], expect_success=False)
    if "verified claim has open evidence" not in claim_result.stdout:
        raise RuntimeError("open verified claim was not blocked")
    checks.append({"name": "verified-claim-evidence-block", "passed": True})

    no_approval = output / "bad-missing-approval"
    shutil.copytree(good, no_approval)
    manifest = json.loads((no_approval / "run-manifest.json").read_text(encoding="utf-8"))
    manifest["approvals"]["strategy"]["status"] = "pending"
    write_json(no_approval / "run-manifest.json", manifest)
    approval_result = run([
        sys.executable,
        str(scripts / "validate_master_run.py"),
        str(no_approval),
        "--stage", "design",
    ], expect_success=False)
    if "strategy approval is required" not in approval_result.stdout:
        raise RuntimeError("missing strategy approval was not blocked")
    checks.append({"name": "approval-gate", "passed": True})

    report = {"passed": True, "checks": checks}
    write_json(output / "regression-report.json", report)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
