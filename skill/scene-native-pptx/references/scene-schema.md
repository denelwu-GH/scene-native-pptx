# Scene And Design Contract Schema

## Design Contract

Use one contract per slide:

```json
{
  "schemaVersion": "1.0.0",
  "metadata": {"name": "Slide title", "sourceReference": "/abs/design.png"},
  "mode": "native-first",
  "canvas": {"width": 1600, "height": 900, "units": "px"},
  "regions": [
    {"id": "header", "role": "title-area", "bbox": [48, 36, 1180, 140], "z": 10}
  ],
  "texts": [
    {
      "id": "title",
      "text": "Exact title",
      "role": "title",
      "bbox": [48, 66, 1100, 58],
      "font": {"family": "PingFang SC", "size": 42, "weight": 700, "color": "#111111"}
    }
  ],
  "assets": [
    {"id": "travel-icon", "kind": "icon", "semantic": "travel", "bbox": [1200, 80, 56, 56], "policy": "native-path"}
  ],
  "connectors": [
    {"id": "flow-1", "from": "input", "to": "hub", "routing": "orthogonal"}
  ]
}
```

Allowed modes: `native-first`, `hybrid-fidelity`, `gorden-compat`.

Bounding boxes use `[x, y, width, height]` in canvas pixels. IDs must be unique across regions, texts, assets, and connectors.

## Scene JSON

```json
{
  "schemaVersion": "1.0.0",
  "metadata": {
    "name": "Slide title",
    "sourceReference": "/abs/design.png",
    "authoringRoute": "scene.json -> constrained SVG -> native DrawingML PPTX",
    "editablePolicy": {"mode": "native-first"}
  },
  "canvas": {"width": 1600, "height": 900, "viewBox": "0 0 1600 900", "units": "px"},
  "svg": {
    "attrs": {"xmlns": "http://www.w3.org/2000/svg", "width": "1600", "height": "900", "viewBox": "0 0 1600 900"},
    "defs": {"type": "defs", "attrs": {}, "children": []},
    "layers": [
      {
        "type": "g",
        "attrs": {"id": "header", "data-role": "title-area"},
        "children": []
      }
    ]
  }
}
```

Represent text as `<text>` nodes with `data-text-id` matching the contract where practical. Store local hybrid assets under the slide directory and use relative paths only.
