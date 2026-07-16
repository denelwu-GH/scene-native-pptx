# Changelog

All notable public changes to Scene Native PPTX and PPT Master are recorded here.

中文版本：[CHANGELOG.zh-CN.md](CHANGELOG.zh-CN.md)

## Unreleased

### Added

- Added bilingual PPT Master workflow diagrams showing both supported starting points, the strategy layer, the native reconstruction engine, approval, and final PowerPoint verification.

### Changed

- Reworked README copy around concrete user outcomes instead of internal implementation terminology.
- Put the full-deck `$ppt-master` prompt before the direct-reconstruction prompt.
- Expanded the Canva, Gamma, and Beautiful.ai section to explain the earlier strategy route as well as native final-mile delivery.
- Repositioned the README hero and section headlines with a higher-impact, outcome-first marketing voice while retaining public proof, methodology, and honest-limit sections.

## [0.2.0] - 2026-07-16

### Added

- Added the first-party `ppt-master` orchestration skill above the native reconstruction engine.
- Added four routes: reconstruction only, restyle existing, strategy to native, and narrative visual.
- Added structured deck briefs, storylines, claim registers, page contracts, visual bibles, and run manifests.
- Added user, project, and run-scoped presentation preferences with explicit precedence and privacy rules.
- Added deck-level design tokens, reusable component governance, and controlled slide overrides.
- Added inclusive presentation rules covering contrast, font size, titles, alt text, reading order, color use, and generated human representation.
- Added separate strategy and design approval gates.
- Added deterministic validation for preference precedence, feedback scope, claims, contrast, approvals, and delivery readiness.

### Changed

- Updated `scene-native-pptx` to accept approved upstream contracts from PPT Master without reinterpreting claims or protected content.
- Updated English and Chinese product positioning from a reconstruction utility to a two-layer presentation production system.
- Updated GitHub Actions to run both the native reconstruction regression and the PPT Master workflow regression.

### Validation

- Public-tree privacy and secret audit passed.
- PPT Master regression passed all seven workflow checks.
- Scene Native PPTX regression passed both public fixtures with zero skipped conversion groups.
- GitHub Actions passed for release commit `035ac1e`.

## [0.1.0] - 2026-07-13

### Added

- Published the native editable PowerPoint reconstruction engine.
- Added `native-first`, `hybrid-fidelity`, and `gorden-compat` routes.
- Added design-contract, scene, constrained SVG, DrawingML, package-integrity, text-preservation, and PowerPoint round-trip validation.
- Added two public synthetic regression fixtures, benchmark methodology, rendered galleries, and the first release demo.

[0.2.0]: https://github.com/denelwu-GH/scene-native-pptx/releases/tag/v0.2.0
[0.1.0]: https://github.com/denelwu-GH/scene-native-pptx/releases/tag/v0.1.0
