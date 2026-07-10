import fs from "node:fs/promises";
import path from "node:path";
import { createRequire } from "node:module";
import { pathToFileURL } from "node:url";

const requireFromCwd = createRequire(path.join(process.cwd(), "package.json"));
const artifactEntry = requireFromCwd.resolve("@oai/artifact-tool");
const { FileBlob, PresentationFile } = await import(pathToFileURL(artifactEntry).href);

const [inputPath, outputDir] = process.argv.slice(2);
if (!inputPath || !outputDir) throw new Error("Usage: node inspect_pptx.mjs <deck.pptx> <output-dir>");

await fs.mkdir(outputDir, { recursive: true });
const presentation = await PresentationFile.importPptx(await FileBlob.load(inputPath));
const inspect = await presentation.inspect({ kind: "slide,textbox,shape,image,layout", maxChars: 120000 });
await fs.writeFile(path.join(outputDir, "inspect.ndjson"), inspect.ndjson, "utf8");

for (const [index, slide] of presentation.slides.items.entries()) {
  const number = String(index + 1).padStart(2, "0");
  const preview = await presentation.export({ slide, format: "png", scale: 1 });
  await fs.writeFile(path.join(outputDir, `slide-${number}.png`), new Uint8Array(await preview.arrayBuffer()));
  const layout = await slide.export({ format: "layout" });
  await fs.writeFile(path.join(outputDir, `slide-${number}.layout.json`), await layout.text(), "utf8");
}

console.log(JSON.stringify({ slides: presentation.slides.items.length, outputDir }));
