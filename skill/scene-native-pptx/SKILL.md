---
name: scene-native-pptx
description: Generate high-fidelity slide design images and rebuild them as stable, native, editable PowerPoint files through design-contract.json, scene.json, constrained SVG, and DrawingML. Use when Codex must create a polished PPT from content, convert a slide image or screenshot to editable PPTX, preserve exact text and layout, avoid image slicing/OCR drift, or repair an image-to-PPT workflow that produces oversized or PowerPoint-repaired files.
---

# Scene Native PPTX

Build visually strong slides with an image-generation design pass, then reconstruct them through a deterministic native-object pipeline:

`content -> design contract -> imagegen reference -> scene.json -> constrained SVG -> DrawingML PPTX`

Treat the design image as the visual target. Treat the content/design contract as the source of truth for text and semantics.

## Start

1. Call `codex_app__load_workspace_dependencies` and follow `references/runtime-setup.md`. Use the bundled Node, Python, Artifact Tool, LibreOffice, and presentation utilities it returns; do not fall back to system runtimes when a bundled runtime exists.
2. Read `references/image-constraints.md` and `references/image-generation-prompts.md` before generating a new design image.
3. Read `references/scene-schema.md` and `references/svg-constraints.md` before authoring `scene.json`.
4. Read `references/qa-gates.md` before conversion and delivery.
5. Create an isolated run directory. Never reuse fixed temporary filenames across runs.

## Choose A Mode

- `native-first` (default): build text, cards, lines, icons, diagrams, and decoration as native DrawingML. Require zero picture shapes.
- `hybrid-fidelity`: keep only genuinely complex illustrations or brand artwork as local image assets; keep all text, layout, cards, and connectors native.
- `gorden-compat`: use only when the user explicitly prefers the legacy background/frame/icon slicing workflow. Read `references/gorden-compatibility.md` first.

Do not silently downgrade `native-first` to raster layers.

## Accept PPT Master Inputs

When `$ppt-master` invokes this skill, treat its approved artifacts as upstream authority:

- `deck-brief.json` defines immutable scope and rewrite permission;
- `resolved-preferences.json` and `deck-design-system.json` define deck-level defaults;
- `page-contracts/slide-XX.json` defines exact text, required elements, forbidden changes, claim labels, and acceptance criteria;
- `run-manifest.json` proves strategy and design approval.

Do not reinterpret approved claims or silently replace deck tokens. Record any required slide-level override in the design contract. Carry the page contract's accessible title, alt-text policy, and semantic reading order into native production and final QA.

## Phase 1: Lock Content

Create `content.json` before design work. Preserve user text verbatim unless the user explicitly requests rewriting.

Record stable IDs for every title, paragraph, label, metric, footer, logo, and semantic icon. Use source PPT/XML or user-provided text as authority when available. Do not use OCR as the authority when exact source text exists.

## Phase 2: Build The Design Contract

Create one `design-contract.json` per slide using the schema in `references/scene-schema.md`.

Define:

- canvas and mode;
- exact text objects and hierarchy;
- semantic regions with stable IDs and bounding boxes;
- icons/illustrations with native or hybrid policies;
- connector intent and z-order;
- brand palette, fonts, spacing, and safety rules;
- optional deck-token references, accessible title, alt-text policy, and semantic reading order when supplied upstream.

Run:

```bash
node scripts/validate_design_contract.mjs design-contract.json qa/design-contract.txt
```

Resolve every error before image generation.

## Phase 3: Generate The Design Image

When no design image is supplied, invoke the `imagegen` skill for each slide. Do not create the reference image with SVG, HTML, Canvas, Pillow, PowerPoint shapes, or screenshots.

Use the prompt templates in `references/image-generation-prompts.md`. Include the full design contract, exact text, palette, aspect ratio, and convertibility constraints. Save the prompt and source image path in `imagegen-manifest.json`.

Generate a correction edit instead of a fresh layout when only overlap, missing content, or icon integrity is wrong.

If the user supplies a design image, preserve it as `design/reference.png` and skip generation.

## Phase 4: Run Design QA

Inspect the image at original resolution. Reject it when any P0 condition occurs:

- missing or invented module;
- text, icon, connector, or illustration overlap not declared in the contract;
- connector crossing text;
- cropped icon or card;
- pseudo-text or missing exact headline;
- raster effect that cannot be represented in the selected mode.

Use `hybrid-fidelity` only for isolated complex artwork, never to hide layout reconstruction failure.

## Phase 5: Author Scene JSON

Use the design image and contract together. Generate `scene.json` directly; do not infer text with OCR.

Group the page semantically. Use stable layer IDs such as `background`, `header`, `connectors`, `cards`, `icons`, and `takeaway`. Express icons as paths or primitive geometry in `native-first` mode.

Run:

```bash
node scripts/validate_scene.mjs scene.json design-contract.json qa/scene-validation.txt
```

Fix unsupported elements, out-of-bounds geometry, duplicate IDs, contract mismatches, and undeclared raster assets.

## Phase 6: Render Constrained SVG

Render deterministically:

```bash
node scripts/scene_to_svg.mjs scene.json slide.svg
```

Apply the whitelist in `references/svg-constraints.md`. Never insert `foreignObject`, masks, text paths, animation, remote assets, or arbitrary CSS.

## Phase 7: Build Native PPTX

Create the base deck with Artifact Tool:

```bash
node scripts/create_base_deck.mjs base.pptx qa/base.inspect.ndjson 1600 900
```

Convert the SVG to DrawingML without importing `python-pptx`:

```bash
python3 scripts/build_native_pptx.py \
  --base base.pptx \
  --svg slide.svg \
  --output slide-native.pptx \
  --trace qa/conversion-trace.json
```

The script uses the bundled minimal `assets/ppt-master` converter and supports controlled local media in `hybrid-fidelity` mode.

## Phase 8: Validate

Execute every P0 gate in `references/qa-gates.md`:

- scene and SVG validation;
- conversion trace with zero skipped top-level elements;
- ZIP integrity;
- XML, relationship-target, and duplicate-shape-ID integrity with `scripts/validate_pptx_package.py`;
- native object inventory;
- slide rendering and overflow testing;
- Artifact Tool import/inspect/render;
- LibreOffice open/export;
- visual comparison against SVG and source design;
- Microsoft PowerPoint open, save, close, and reopen with no repair prompt.

Do not call a file complete before the real PowerPoint round trip passes when PowerPoint is available.

## Phase 9: Deliver

Package only durable artifacts:

```text
<run>/
├── content.json
├── design-contract.json
├── prompts/
├── imagegen-manifest.json
├── design/reference.png
├── scene/slide-XX.scene.json
├── svg/slide-XX.svg
├── out/<name>-native-editable.pptx
└── qa/
```

Run `scripts/package_delivery.py <run-dir> <output.zip>` to exclude lock files, caches, and temporary renders.

## Multi-Agent Execution

Delegate only when the user explicitly authorizes subagents. Assign disjoint slide ranges or disjoint responsibilities:

- content/design-contract owner;
- scene/SVG owner;
- independent QA owner.

Give every worker the raw artifact and exact output directory. Do not leak expected QA conclusions to the independent QA worker. Keep each slide in an isolated directory and integrate only after local validation.

## Regression

Run both bundled public-safe synthetic fixtures after changing scripts or constraints:

```bash
python3 scripts/run_regression.py --skill-dir . --output-dir /tmp/scene-native-pptx-regression
```

Sample 1 covers a dense all-native orchestration page. Sample 2 covers a hybrid service journey with native layout and isolated local artwork.
