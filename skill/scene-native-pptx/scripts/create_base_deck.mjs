import fs from "node:fs/promises";
import path from "node:path";
import { createRequire } from "node:module";
import { pathToFileURL } from "node:url";

const requireFromCwd = createRequire(path.join(process.cwd(), "package.json"));
const artifactEntry = requireFromCwd.resolve("@oai/artifact-tool");
const { Presentation, PresentationFile } = await import(pathToFileURL(artifactEntry).href);

const [outputPath, inspectPath, widthArg = "1600", heightArg = "900", countArg = "1"] = process.argv.slice(2);
if (!outputPath) {
  throw new Error("Usage: node create_base_deck.mjs <output.pptx> [inspect.ndjson] [width] [height] [slide-count]");
}

const width = Number(widthArg);
const height = Number(heightArg);
const slideCount = Number(countArg);
if (![width, height, slideCount].every(Number.isFinite) || width <= 0 || height <= 0 || slideCount < 1) {
  throw new Error(`Invalid slide dimensions or count: ${width}x${height}, count=${slideCount}`);
}

const presentation = Presentation.create({ slideSize: { width, height } });
for (let index = 0; index < slideCount; index += 1) {
  const slide = presentation.slides.add();
  slide.background.fill = "#FFFFFF";
}

const inspect = await presentation.inspect({ kind: "slide,layout", maxChars: 12000 });
if (inspectPath) await fs.writeFile(inspectPath, inspect.ndjson, "utf8");

const pptx = await PresentationFile.exportPptx(presentation);
await pptx.save(outputPath);
console.log(JSON.stringify({ outputPath, width, height, slideCount }));
