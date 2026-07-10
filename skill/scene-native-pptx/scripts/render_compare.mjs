import fs from "node:fs/promises";
import path from "node:path";
import { createRequire } from "node:module";
import { pathToFileURL } from "node:url";

const requireFromCwd = createRequire(path.join(process.cwd(), "package.json"));
const sharpEntry = requireFromCwd.resolve("sharp");
const { default: sharp } = await import(pathToFileURL(sharpEntry).href);

const [referencePath, svgPath, pptRenderPath, outputDir] = process.argv.slice(2);
if (!referencePath || !svgPath || !pptRenderPath || !outputDir) {
  throw new Error("Usage: node render_compare.mjs <reference.png> <scene.svg> <ppt-render.png> <output-dir>");
}

await fs.mkdir(outputDir, { recursive: true });
const metadata = await sharp(referencePath).metadata();
const width = metadata.width;
const height = metadata.height;
if (!width || !height) throw new Error("Unable to determine reference image dimensions");

const referencePng = await sharp(referencePath).resize(width, height).png().toBuffer();
const reference = await sharp(referencePng).removeAlpha().raw().toBuffer();
const svgPngPath = path.join(outputDir, "scene-render.png");
await sharp(svgPath, { density: 96 }).resize(width, height).png().toFile(svgPngPath);
const svgBuffer = await sharp(svgPngPath).removeAlpha().raw().toBuffer();
const pptPng = await sharp(pptRenderPath).resize(width, height).png().toBuffer();
const pptBuffer = await sharp(pptPng).removeAlpha().raw().toBuffer();

function metrics(a, b) {
  let absolute = 0;
  let squared = 0;
  for (let index = 0; index < a.length; index += 1) {
    const delta = a[index] - b[index];
    absolute += Math.abs(delta);
    squared += delta * delta;
  }
  const mae = absolute / a.length;
  const mse = squared / a.length;
  const psnr = 10 * Math.log10((255 * 255) / Math.max(mse, 1e-12));
  return { mae, mse, psnr };
}

const result = {
  width,
  height,
  svgVsReference: metrics(svgBuffer, reference),
  pptVsReference: metrics(pptBuffer, reference),
  pptVsSvg: metrics(pptBuffer, svgBuffer),
};

await sharp({ create: { width, height: height * 3, channels: 3, background: "white" } })
  .composite([
    { input: referencePng, top: 0, left: 0 },
    { input: svgPngPath, top: height, left: 0 },
    { input: pptPng, top: height * 2, left: 0 },
  ])
  .png()
  .toFile(path.join(outputDir, "reference-scene-ppt-stacked.png"));

await fs.writeFile(path.join(outputDir, "metrics.json"), `${JSON.stringify(result, null, 2)}\n`, "utf8");
console.log(JSON.stringify(result));
