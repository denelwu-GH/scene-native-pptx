# Image Constraints

## Profiles

### Native-first

- Use a 16:9 canvas, normally 1600 x 900 design coordinates.
- Keep all text, icons, connectors, containers, and diagrams translatable to native geometry.
- Use rectangles, rounded rectangles, circles, ellipses, straight or orthogonal connectors, and simple closed paths.
- Use flat or two-tone icons with complete visible boundaries.
- Use at most three gradient stops and one controlled shadow per object.
- Use no photographs, complex 3D objects, glass refraction, noise textures, bokeh, or full-page blur.

### Hybrid-fidelity

- Apply all native-first rules to layout and text.
- Permit only isolated illustrations, product renders, photographs, or protected brand artwork as raster assets.
- Give every raster asset its own contract ID, bounding box, local path, and reason.
- Never use a full-slide bitmap or a bitmap containing editable text.

## Geometry

- Use an 8 px layout grid.
- Keep important content at least 32 px from the canvas edge.
- Keep 16 px minimum separation between text and icons; use 24 px between major modules.
- Keep connectors out of text boxes and illustrations.
- Keep card radii consistent and normally at or below 12 px.
- Define stable card, board, and icon dimensions; do not let dynamic text resize layout.

## Typography

- Keep page titles at least 38 px, section titles at least 22 px, and body text at least 16 px at 1600 x 900.
- Use supported fonts such as PingFang SC, Microsoft YaHei, Aptos, Arial, or a user-supplied installed font.
- Keep letter spacing at zero.
- Do not use text on paths, perspective text, or text embedded inside illustrations.
- Keep exact text in `content.json` and `design-contract.json`; imagegen text is not authoritative.

## Convertibility Failures

Reject or regenerate designs with:

- text/icon overlap;
- clipped icons;
- large blurred halos;
- nested translucent glass panels;
- more than one complex filter on an object;
- connectors hidden behind text;
- tiny pseudo-text;
- gradients used as the only boundary between modules;
- complex visual content that spans multiple semantic modules.
