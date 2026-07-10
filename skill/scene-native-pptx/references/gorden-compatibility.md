# Gorden Compatibility

## Reuse

Reuse these ideas from `GordenSuperPPTSkill` and `GordenImagePPTGen`:

- structured `outline.json`;
- one self-contained imagegen prompt per slide;
- image generation manifest with prompt and source paths;
- reference-layout selection;
- per-slide retries instead of regenerating the whole deck;
- content-density and brand-consistency checks.

## Replace In The Main Route

Do not use these as the default reconstruction mechanism:

- generated green-screen background/frame/icon layers;
- chroma-key extraction;
- automatic icon slicing;
- visual OCR as final text authority;
- full-page background images;
- `python-pptx` composition of mostly raster layers.

Replace them with design contracts, semantic scene JSON, constrained SVG, and native DrawingML.

## Legacy Route

Use `gorden-compat` only when the user explicitly requests the legacy four-layer workflow or accepts partial editability. Label the output as layered-raster rather than fully native. Do not present it as equivalent to `native-first`.
