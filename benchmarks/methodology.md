# Benchmark Methodology

## Purpose

This benchmark compares five routes tested against the same target class: a dense 16:9 technology infographic with Chinese or mixed-language text, cards, curved connectors, a central radial graphic, gradients, shadows, and semantic icons.

It is an engineering decision aid, not a scientific or universal ranking. The routes were iterated at different times and not every visual metric was produced from an identical raster reference. Scores therefore combine measured evidence with documented review criteria.

## Weights

| Dimension | Weight | Definition |
| --- | ---: | --- |
| Visual fidelity | 30% | Layout, hierarchy, shape, typography, connector, gradient, and shadow similarity |
| Editability | 25% | Share of meaningful content represented as native text, geometry, groups, or isolated assets |
| PowerPoint safety | 20% | ZIP/XML integrity and Microsoft PowerPoint open/save/reopen behavior without repair |
| Repeatability | 15% | Determinism, semantic source model, validation coverage, and independence from OCR/cutout variance |
| File efficiency | 10% | Package size relative to editable object count and retained fidelity |

Each dimension is scored from 0 to 10. The total is:

```text
score = fidelity*0.30 + editability*0.25 + safety*0.20
      + repeatability*0.15 + efficiency*0.10
```

Published totals are rounded to one decimal. Raw values are in `benchmark-scores.json`.

## Measured Evidence

| Route | PPTX size | Object evidence | Visual / stability evidence |
| --- | ---: | --- | --- |
| Layered raster | 1,436,413 B | 27 images, 22 editable text boxes | Render and overflow tests passed; icon matte and semantic editability remained limited |
| Componentized | 153,557 B | 54 native shapes, 26 images, 22 text boxes | LibreOffice and package safety checks passed; connector and effect styling simplified |
| HTML/DOM | 861,732 B | 71 shapes, 61 text runs, 31 pictures | MAE 17.20; no repair; visible title overlap and radial-layout deformation |
| Constrained SVG proof | 23,986 B | 174 shapes, 63 text runs, 10 groups, 0 pictures | MAE 14.76; PowerPoint save/reopen passed |
| Scene Native | 24,512 B | 185 shapes, 63 text runs, 10 groups, 0 pictures | PPT-vs-SVG MAE 14.01; full PowerPoint round trip passed without repair |

## Interpretation

The current route scores 9.4/10, 2.0 points above the strongest earlier componentized route and 2.6 points above the HTML/DOM route. This does not mean every slide is 27% or 38% visually better. The gain is mainly the combination of fidelity, native editability, deterministic validation, and PowerPoint stability.

The file-size comparison is exact for the recorded test artifacts:

- 84.0% smaller than the 153,557-byte componentized deck;
- 97.2% smaller than the 861,732-byte HTML/DOM deck;
- 98.3% smaller than the 1,436,413-byte layered-image deck.

## Reproduction

Run the public synthetic regression suite:

```bash
python3 skill/scene-native-pptx/scripts/run_regression.py \
  --skill-dir skill/scene-native-pptx \
  --output-dir regression-output
```

The public fixtures verify pipeline behavior and do not reproduce the private benchmark artwork. Real Microsoft PowerPoint round-trip testing remains a release gate that requires a local PowerPoint installation.
