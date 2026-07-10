# Image Generation Prompts

## Design Prompt

```text
You are a senior presentation designer creating a high-fidelity PowerPoint design reference.

Create one 16:9 slide at high resolution using a 1600 x 900 composition grid.
Treat the supplied design contract and exact text as immutable. Do not add, delete, merge, summarize, or rewrite content.

Design goals:
- polished technology-business visual quality;
- dense but clearly scannable information hierarchy;
- independent zones for text, icons, illustrations, and connectors;
- no text overlapping icons, artwork, gradients, or connectors;
- geometry that can be rebuilt with native PowerPoint shapes;
- consistent 8 px grid, 32 px outer safe area, and 16-24 px module spacing;
- clean vector-like icons with complete boundaries;
- at most three gradient stops and one restrained shadow per object;
- no photographs, complex 3D, glass refraction, noise, bokeh, pseudo-text, or full-page blur in native-first mode.

Canvas and brand:
<canvas, palette, fonts, logo rules>

Regions and layout:
<paste every region ID, role, bounding box, and relative relationship>

Exact slide text:
<paste every text ID and verbatim text>

Asset semantics:
<paste every icon/illustration ID, meaning, bounding box, and native/hybrid policy>

Render the complete slide, not a template or wireframe. Preserve all IDs conceptually through clear visual grouping.
```

## Correction Prompt

```text
Edit the current slide image. Do not redesign the layout.

Keep every unlisted module, position, size, color, text, and connector unchanged.
Fix only these defects:
<list missing content, overlap, cropped icons, connector crossings, or text errors>

Do not add new modules. Do not move unaffected objects. Maintain the original 16:9 canvas and design style.
```

## Scene Authoring Prompt

```text
You are a native PowerPoint reconstruction engine.

Input: one slide design image plus its design-contract.json.
Output: JSON only, following the scene schema.

Rules:
- use the contract, not OCR, for all text;
- preserve canvas, region bounds, z-order, colors, spacing, and visual relationships;
- create stable IDs for every layer and object;
- use only allowed SVG primitives and inline attributes;
- rebuild icons as primitive or custom path geometry in native-first mode;
- emit local image nodes only for contract assets explicitly marked hybrid-raster;
- never emit foreignObject, mask, textPath, animation, remote URLs, or arbitrary CSS;
- separate text from icons and connectors;
- keep all geometry within the canvas;
- return no explanation outside the JSON object.
```

## Independent QA Prompt

```text
Compare the source design image, generated SVG render, and final PPTX render at identical dimensions.

Report findings in P0/P1/P2 order. Check content completeness, exact text, major region geometry, connector routing, icon integrity, layering, gradients, shadows, and unintended overlap. Treat a PowerPoint repair prompt, missing module, skipped converter element, wrong text, or undeclared full-slide bitmap as P0. Do not suggest aesthetic redesign unless it fixes a demonstrated mismatch.
```
