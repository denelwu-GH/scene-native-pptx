---
name: ppt-master
description: Plan, design, rebuild, and deliver professional PowerPoint decks from source documents, old PPTX files, screenshots, design images, or a written brief. Use when Codex must create or restructure a complete presentation, improve its storyline and claims, preserve user-approved content or layout, learn explicit presentation preferences, enforce brand and inclusive-design rules, generate coherent visual references, or orchestrate high-fidelity native editable PPTX production through scene-native-pptx.
---

# PPT Master

Orchestrate the full presentation lifecycle. Treat `scene-native-pptx` as the native rendering engine; keep strategy, evidence, preferences, deck-level design, and approval gates here.

## Non-Negotiable Rules

1. Preserve source files. Work in a new run directory unless the user explicitly requests in-place editing.
2. Apply instructions in this order: current explicit request, run brief, project profile, user profile, skill defaults.
3. Preserve exact text and layout whenever the user forbids rewriting or rearrangement.
4. Do not present PoC, target experience, or vision content as a verified deployed capability.
5. Do not persist inferred preferences. Persist only explicit, stable preferences with user awareness; never store client secrets or deck content in a user profile.
6. Build accessibility and inclusive representation into the design contract, not as a final cosmetic pass.
7. Require strategy and design approval before expensive native reconstruction unless the user explicitly requests a direct reconstruction.
8. Do not claim delivery until PowerPoint opens, saves, closes, and reopens without repair when PowerPoint is available.

## Choose A Route

- `reconstruction-only`: a finished design image exists. Skip strategy rewriting and use `$scene-native-pptx` directly after recording immutable constraints.
- `restyle-existing`: preserve specified text and layout while unifying the visual system.
- `strategy-to-native` (default for full decks): audit sources, build the story and evidence model, design, then reconstruct natively.
- `narrative-visual`: build user stories or scene-based pages with text-free generated artwork and deterministic native text.

Never silently switch routes. Record the route in `run-manifest.json`.

## Start A Run

1. Load the presentation workspace dependencies.
2. Inspect all named source files and define the exact page and edit boundary.
3. Initialize an isolated run:

```bash
python3 scripts/init_run.py \
  --run-dir <absolute-run-dir> \
  --deck-name "<deck-name>" \
  --slide-count <n> \
  --route strategy-to-native
```

4. Resolve optional preference files:

```bash
python3 scripts/resolve_preferences.py \
  --user ~/.codex/ppt-master/user-profile.json \
  --project <project>/.ppt-master/project-profile.json \
  --run <run>/deck-brief.json \
  --output <run>/resolved-preferences.json
```

Read `references/user-preferences.md` before recording or applying persistent preferences.

## Phase 1: Brief And Source Audit

Complete `deck-brief.json` before redesigning content. Record:

- audience, presentation objective, decision sought, and language;
- source-of-truth hierarchy and required source pages;
- immutable text, layout, logo, and brand constraints;
- rewrite permission and excluded scope;
- delivery format, editability, and accessibility expectations.

Use `references/strategy-and-evidence.md` for source auditing and evidence boundaries.

## Phase 2: Storyline And Claims

Complete `storyline.json`, `claim-register.json`, and every file under `page-contracts/`.

Each slide must have one role, one takeaway, one transition, and explicit evidence classification. Each page contract must define required elements, forbidden changes, exact-text policy, visual pattern, and accessibility metadata.

Run the structural gate:

```bash
python3 scripts/validate_master_run.py <run-dir> --stage draft
```

Do not proceed with unresolved factual claims unless they are visibly labeled as PoC, target experience, or vision.

## Phase 3: Deck Design System

Create one `deck-design-system.json` for the entire deck before designing individual pages. Define reusable tokens and components for typography, colors, spacing, grids, cards, icons, charts, logos, footnotes, and source labels.

Read:

- `references/deck-design-system.md` for component and override policy;
- `references/inclusive-presentation-design.md` for accessibility and representation rules.

Per-slide contracts may override the deck system only when the exception is documented.

## Phase 4: Visual Direction

Select one visual route per page:

- native infographic or architecture page;
- data and evidence page;
- photo or product-led page;
- text-free narrative scene with native text overlay.

For narrative pages, read `references/narrative-visuals.md` and create `visual-bible.json` before generating scenes. Keep generated Chinese text, fake logos, fake interface labels, and invented data out of artwork.

Inspect every reference at original resolution. Correct local defects with image editing; regenerate from scratch only when composition is fundamentally wrong.

## Phase 5: Approval Gate

Record approvals in `run-manifest.json`:

- `strategy`: storyline, claims, page roles, and exact text approved;
- `design`: reference images, deck system, and page composition approved.

Run:

```bash
python3 scripts/validate_master_run.py <run-dir> --stage design
```

Do not treat silence as approval.

## Phase 6: Native Production

Invoke `$scene-native-pptx` for approved pages. Pass it:

- exact page contract and text;
- deck design tokens and permitted overrides;
- reference image and local assets;
- required mode (`native-first` or `hybrid-fidelity`);
- accessibility metadata and semantic reading order.

Keep all exact text, cards, connectors, and simple icons native. Use raster assets only for genuine photos, product renders, protected brand artwork, or complex illustrations.

## Phase 7: Delivery QA And Learning

Run both page-level and deck-level QA:

- source text and page count;
- storyline continuity and terminology consistency;
- claim maturity and visible labeling;
- deck design-system consistency;
- contrast, font size, slide titles, alt text, and reading order;
- native object inventory, overflow, visual similarity, and package integrity;
- PowerPoint repair-free round trip.

Then run:

```bash
python3 scripts/validate_master_run.py <run-dir> --stage delivery
```

When the user gives feedback, classify it before storing it:

```bash
python3 scripts/classify_feedback.py --text "<feedback>"
```

Treat `review-required` as a request-local signal until the user confirms broader scope.

## Deliverables

```text
<run>/
├── deck-brief.json
├── resolved-preferences.json
├── storyline.json
├── claim-register.json
├── deck-design-system.json
├── visual-bible.json
├── page-contracts/
├── design/
├── native/
├── qa/
└── run-manifest.json
```

## Multi-Agent Roles

Delegate only when the user authorizes subagents. Keep roles disjoint:

- presentation strategist;
- evidence and claims auditor;
- brand and inclusive-design reviewer;
- visual storyteller or art director;
- native PPT implementer;
- independent delivery QA.

Give independent QA raw artifacts and acceptance criteria, not the expected verdict.

## Regression

After modifying this skill, run:

```bash
python3 scripts/run_regression.py --skill-dir . --output-dir /tmp/ppt-master-regression
```

The regression checks run initialization, preference precedence, feedback classification, claims, deck design-system structure, accessibility contrast, approvals, and delivery readiness.
