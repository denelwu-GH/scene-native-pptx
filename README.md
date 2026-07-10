# Scene Native PPTX

Build high-fidelity, editable PowerPoint slides from a visual design target without flattening the whole page into a screenshot.

![Benchmark comparison](benchmarks/benchmark-comparison.svg)

The core pipeline is:

```text
content -> design contract -> design reference -> scene.json
        -> constrained SVG -> native DrawingML -> PPTX
```

The design reference controls visual intent. The design contract controls exact text, semantic regions, editability, and safety constraints. `scene.json` then becomes the single source for deterministic SVG and PowerPoint generation.

## Why This Exists

Image-to-PPT workflows usually optimize one side of the problem:

- a full-slide image preserves appearance but is barely editable;
- OCR plus image slicing creates fragile layers and text drift;
- HTML/CSS export gives editable boxes but often distorts complex diagrams;
- unconstrained SVG conversion can create unsupported or repair-prone OOXML.

Scene Native PPTX uses a deliberately restricted scene model and SVG profile so text, cards, paths, connectors, gradients, and semantic groups remain native PowerPoint objects. Only isolated artwork that is genuinely expensive to reconstruct stays rasterized.

## Capabilities

- Exact text preservation from a design contract, without OCR as the authority.
- `native-first` mode with zero image shapes.
- `hybrid-fidelity` mode for isolated local PNG/JPEG/WebP artwork.
- Stable semantic grouping and deterministic scene-to-SVG rendering.
- Direct DrawingML generation without `python-pptx`.
- ZIP, XML, relationship, duplicate-ID, text, overflow, and visual QA gates.
- Real Microsoft PowerPoint save/reopen validation as the final compatibility gate.
- Synthetic two-slide regression suite with no customer or brand assets.

## Install

Copy or symlink the skill directory into your Codex skills folder:

```bash
cp -R skill/scene-native-pptx ~/.codex/skills/scene-native-pptx
```

Then invoke it as `$scene-native-pptx` in Codex.

## Quick Validation

```bash
python3 ~/.codex/skills/scene-native-pptx/scripts/run_regression.py \
  --skill-dir ~/.codex/skills/scene-native-pptx \
  --output-dir /tmp/scene-native-pptx-regression
```

The regression suite checks two synthetic fixtures:

- a dense all-native orchestration diagram;
- a hybrid page with native layout and separately editable raster artwork.

## Benchmark Summary

The weighted score is an engineering benchmark for the same complex-slide use case, not a universal product ranking. It combines visual fidelity, editability, PowerPoint safety, repeatability, and file efficiency. See [the methodology](benchmarks/methodology.md) and [raw scores](benchmarks/benchmark-scores.json).

| Route tested | Weighted score | Main limitation |
| --- | ---: | --- |
| Layered raster + editable text | 6.4 / 10 | Framework remains a bitmap; slicing and matte quality vary |
| Componentized shapes + raster icons | 7.4 / 10 | Curves, gradients, and shadows are visibly simplified |
| HTML/DOM to PPTX | 6.8 / 10 | Complex headings, radial graphics, and rich text drift |
| Constrained SVG proof of concept | 8.8 / 10 | Good conversion, but no formal semantic contract or full regression harness |
| **Scene JSON + constrained SVG + DrawingML** | **9.4 / 10** | Requires disciplined scene authoring and final PowerPoint QA |

In the measured native sample, the final PowerPoint contained 185 native shapes, 10 groups, 63 text runs, and zero pictures. It opened, saved, closed, and reopened in PowerPoint for Mac 16.107 without a repair prompt. The 24.5 KB result was 84.0% smaller than the 153.6 KB componentized version and 98.3% smaller than the 1.44 MB layered-image version.

## Repository Layout

```text
skill/scene-native-pptx/   installable Codex skill
benchmarks/                scoring method, evidence, and charts
tools/                     public fixture and chart generators
PUBLICATION_AUDIT.md       release-time privacy and secret review
THIRD_PARTY_NOTICES.md     bundled dependency attribution
```

## Limits

- It does not automatically recover semantic structure from every arbitrary screenshot.
- Complex blur, noise, masks, photography, and generative illustrations should remain isolated image assets.
- Pixel metrics alone are insufficient; text flow, object structure, and PowerPoint repair behavior must also be inspected.
- LibreOffice and browser rendering are useful secondary checks, but they do not replace the Microsoft PowerPoint round trip.

## Security And Privacy

The public fixtures are generated from code and contain no customer decks, logos, local usernames, or absolute source paths. See [PUBLICATION_AUDIT.md](PUBLICATION_AUDIT.md) before publishing a fork with your own examples.

## License

The repository is released under the [MIT License](LICENSE). The bundled converter subset under `skill/scene-native-pptx/assets/ppt-master` retains its original MIT notice; see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
