# QA Gates

## P0 Blocking Gates

- Design contract validator reports zero errors.
- Scene validator reports zero errors.
- Converter reports zero skipped top-level elements.
- `python_pptx_loaded` is false in conversion trace.
- ZIP integrity test passes.
- `scripts/validate_pptx_package.py` reports no malformed XML, duplicate ZIP entry, missing relationship target, or duplicate slide shape ID.
- Exact contract text is present and not rewritten.
- No missing major region, connector, or declared asset.
- Native-first output contains zero picture shapes.
- Hybrid output contains no undeclared picture shape and no raster text.
- Overflow test passes.
- Microsoft PowerPoint opens, saves, closes, and reopens the file without repair.

## Visual Gates

- Render source design, constrained SVG, and PPTX to the same pixel dimensions.
- Run `scripts/render_compare.mjs <reference> <svg> <ppt-render> <qa-dir>` from the configured presentation workspace.
- Require PPTX-vs-SVG MAE at or below 18 by default; investigate values above 18 and block above 22 unless documented.
- Use overlays and side-by-side inspection in addition to numeric metrics.
- Require major region position and size to remain visually aligned.
- Reject text/icon overlap, connector-through-text, cropped icons, duplicated assets, and accidental layer changes.

## Structural Inventory

Record:

- shape count;
- group count;
- editable text-run count;
- picture/media count;
- gradients, shadows, and conversion skips;
- final file size and SHA-256.

## Compatibility Matrix

Validate with Artifact Tool and LibreOffice. Use Microsoft PowerPoint as the final compatibility authority when available. PowerPoint normalization may change ZIP bytes without changing editable objects; record both pre-save and post-save hashes when reproducibility matters.

Run `scripts/inspect_pptx.mjs <deck.pptx> <qa-dir>` from the configured Artifact Tool workspace before delivery.
