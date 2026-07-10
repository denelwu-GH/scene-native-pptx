#!/usr/bin/env python3
"""Run deterministic static regression fixtures for the skill."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


NS = {
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
}


def run(command: list[str], cwd: Path | None = None) -> None:
    subprocess.run(command, cwd=cwd, check=True)


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
    node = shutil.which("node")
    if not node:
        raise RuntimeError("node is required")

    results = []
    combined_svgs = []
    combined_texts = []
    for fixture in sorted((skill / "assets" / "regression").glob("sample-*")):
        case_out = output / fixture.name
        case_out.mkdir()
        fixture_assets = fixture / "assets"
        if fixture_assets.is_dir():
            shutil.copytree(fixture_assets, case_out / "assets")
        scene = fixture / "scene.json"
        contract = fixture / "design-contract.json"
        expected_svg = fixture / "expected.svg"
        generated_svg = case_out / "generated.svg"
        validation = case_out / "scene-validation.txt"
        trace = case_out / "conversion-trace.json"
        pptx = case_out / "output.pptx"

        run([node, str(skill / "scripts" / "validate_design_contract.mjs"), str(contract), str(case_out / "contract-validation.txt")])
        run([node, str(skill / "scripts" / "validate_scene.mjs"), str(scene), str(contract), str(validation)])
        run([node, str(skill / "scripts" / "scene_to_svg.mjs"), str(scene), str(generated_svg)])
        if generated_svg.read_bytes() != expected_svg.read_bytes():
            raise RuntimeError(f"{fixture.name}: scene_to_svg output is not deterministic")

        run([
            sys.executable,
            str(skill / "scripts" / "build_native_pptx.py"),
            "--base", str(skill / "assets" / "base-artifact-tool-1600x900.pptx"),
            "--svg", str(generated_svg),
            "--output", str(pptx),
            "--trace", str(trace),
        ])
        run([
            sys.executable,
            str(skill / "scripts" / "verify_pptx_text.py"),
            str(pptx),
            str(contract),
            "--report", str(case_out / "text-report.json"),
        ])
        run([
            sys.executable,
            str(skill / "scripts" / "validate_pptx_package.py"),
            str(pptx),
            "--report", str(case_out / "package-report.json"),
        ])

        with zipfile.ZipFile(pptx) as archive:
            bad = archive.testzip()
            if bad:
                raise RuntimeError(f"{fixture.name}: corrupt ZIP entry {bad}")
            root = ET.fromstring(archive.read("ppt/slides/slide1.xml"))
            counts = {
                "shapes": len(root.findall(".//p:sp", NS)),
                "groups": len(root.findall(".//p:grpSp", NS)),
                "pictures": len(root.findall(".//p:pic", NS)),
                "text_runs": len(root.findall(".//a:t", NS)),
            }

        trace_data = json.loads(trace.read_text(encoding="utf-8"))
        skipped = sum(
            event.get("summary", {}).get("skipped", 0)
            for slide in trace_data["slides"]
            for event in slide["trace"]
        )
        if trace_data.get("python_pptx_loaded") or skipped:
            raise RuntimeError(f"{fixture.name}: invalid conversion trace")

        results.append({
            "fixture": fixture.name,
            "scene_sha256": hashlib.sha256(scene.read_bytes()).hexdigest(),
            "svg_sha256": hashlib.sha256(generated_svg.read_bytes()).hexdigest(),
            "pptx_sha256": hashlib.sha256(pptx.read_bytes()).hexdigest(),
            "pptx_size": pptx.stat().st_size,
            "skipped": skipped,
            "contract_texts": len(json.loads(contract.read_text(encoding="utf-8")).get("texts", [])),
            **counts,
        })

        combined_svgs.append(generated_svg)
        combined_texts.extend(json.loads(contract.read_text(encoding="utf-8")).get("texts", []))

    combined_result = None
    if len(combined_svgs) > 1:
        combined_pptx = output / "combined-2slides.pptx"
        combined_trace = output / "combined-conversion-trace.json"
        combined_contract = output / "combined-contract.json"
        combined_contract.write_text(
            json.dumps({"texts": combined_texts}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        command = [
            sys.executable,
            str(skill / "scripts" / "build_native_pptx.py"),
            "--base", str(skill / "assets" / "base-artifact-tool-2slides.pptx"),
        ]
        for svg in combined_svgs:
            command.extend(["--svg", str(svg)])
        command.extend(["--output", str(combined_pptx), "--trace", str(combined_trace)])
        run(command)
        run([
            sys.executable,
            str(skill / "scripts" / "verify_pptx_text.py"),
            str(combined_pptx),
            str(combined_contract),
            "--report", str(output / "combined-text-report.json"),
        ])
        run([
            sys.executable,
            str(skill / "scripts" / "validate_pptx_package.py"),
            str(combined_pptx),
            "--report", str(output / "combined-package-report.json"),
        ])
        with zipfile.ZipFile(combined_pptx) as archive:
            if archive.testzip():
                raise RuntimeError("combined deck ZIP integrity failed")
            slide_count = len([
                name for name in archive.namelist()
                if name.startswith("ppt/slides/slide") and name.endswith(".xml")
            ])
        if slide_count != len(combined_svgs):
            raise RuntimeError(f"combined deck slide count mismatch: {slide_count}")
        combined_result = {
            "slides": slide_count,
            "pptx_size": combined_pptx.stat().st_size,
            "pptx_sha256": hashlib.sha256(combined_pptx.read_bytes()).hexdigest(),
            "contract_texts": len(combined_texts),
        }

    report = {"passed": True, "fixtures": results, "combined": combined_result}
    (output / "regression-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
