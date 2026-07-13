# Scene Native PPTX v0.1.0

Beautiful in. Editable out.

This first public release turns polished slide designs, screenshots, and image-based decks into stable, native, editable PowerPoint files.

## What ships

- `native-first` for pages rebuilt entirely as editable DrawingML objects.
- `hybrid-fidelity` for pages that need a small number of isolated, replaceable visual assets.
- A deterministic pipeline: design contract -> `scene.json` -> constrained SVG -> DrawingML -> PPTX.
- Two public regression fixtures, package validation, text checks, and public-tree privacy scanning.

## Verified in this release

- All-native sample: 85 native shapes, 31 editable text runs, 0 pictures.
- Hybrid sample: 53 native shapes, 22 editable text runs, 1 replaceable artwork asset.
- Microsoft PowerPoint for Mac 16.107: open, save, close, and reopen without a repair prompt.
- GitHub Actions runs the public two-sample regression on every push.

## Install

```bash
git clone https://github.com/denelwu-GH/scene-native-pptx.git
cp -R scene-native-pptx/skill/scene-native-pptx ~/.codex/skills/scene-native-pptx
```

Then call `$scene-native-pptx` in Codex.

## Scope

Text, cards, paths, connectors, groups, and simple icons are rebuilt as native objects. Photography, generative illustrations, and effects that cannot be expressed safely in DrawingML remain isolated local assets in hybrid mode.
