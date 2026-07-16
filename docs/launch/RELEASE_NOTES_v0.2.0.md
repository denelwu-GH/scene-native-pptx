# PPT Master v0.2.0

Scene Native PPTX is no longer only a high-fidelity reconstruction engine. This release adds PPT Master, an orchestration layer that can begin with source material, an old deck, or an incomplete brief and carry the work through strategy, evidence, design, native production, and delivery QA.

## Highlights

- Two installable skills with clear responsibilities.
- Storyline, claims, evidence maturity, page contracts, and approval gates before production.
- User, project, and run-scoped preferences without silently storing private deck content.
- Deck-level design systems instead of unrelated per-slide styling.
- Inclusive presentation checks for readability, object order, alternative text, and generated imagery.
- Deterministic workflow regression in GitHub Actions.

## Install

```bash
git clone https://github.com/denelwu-GH/scene-native-pptx.git
cp -R scene-native-pptx/skill/scene-native-pptx ~/.codex/skills/scene-native-pptx
cp -R scene-native-pptx/skill/ppt-master ~/.codex/skills/ppt-master
```

Use `$scene-native-pptx` when a finished design already exists. Use `$ppt-master` when the presentation still needs strategy, structure, or a coherent deck system.
