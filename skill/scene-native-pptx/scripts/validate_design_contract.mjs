import fs from "node:fs/promises";

const [inputPath, outputPath] = process.argv.slice(2);
if (!inputPath) throw new Error("Usage: node validate_design_contract.mjs <contract.json> [report.txt]");

const contract = JSON.parse(await fs.readFile(inputPath, "utf8"));
const errors = [];
const warnings = [];
const allowedModes = new Set(["native-first", "hybrid-fidelity", "gorden-compat"]);
const width = Number(contract.canvas?.width);
const height = Number(contract.canvas?.height);
const mode = contract.mode;
const ids = new Set();

if (!contract.schemaVersion) errors.push("schemaVersion is required");
if (!allowedModes.has(mode)) errors.push(`unsupported mode: ${mode}`);
if (!Number.isFinite(width) || !Number.isFinite(height) || width <= 0 || height <= 0) {
  errors.push("canvas.width and canvas.height must be positive numbers");
}

function checkId(item, pointer) {
  if (!item?.id) {
    errors.push(`${pointer}.id is required`);
    return;
  }
  if (ids.has(item.id)) errors.push(`duplicate id: ${item.id}`);
  ids.add(item.id);
}

function checkBbox(item, pointer) {
  const bbox = item?.bbox;
  if (!Array.isArray(bbox) || bbox.length !== 4 || !bbox.every(Number.isFinite)) {
    errors.push(`${pointer}.bbox must be [x,y,width,height]`);
    return;
  }
  const [x, y, w, h] = bbox;
  if (w <= 0 || h <= 0) errors.push(`${pointer}.bbox must have positive width and height`);
  if (x < 0 || y < 0 || x + w > width || y + h > height) {
    errors.push(`${pointer}.bbox is outside the canvas`);
  }
}

for (const [index, region] of (contract.regions ?? []).entries()) {
  checkId(region, `regions[${index}]`);
  checkBbox(region, `regions[${index}]`);
}

for (const [index, text] of (contract.texts ?? []).entries()) {
  checkId(text, `texts[${index}]`);
  checkBbox(text, `texts[${index}]`);
  if (typeof text.text !== "string" || !text.text.length) errors.push(`texts[${index}].text is required`);
  if (!Number.isFinite(Number(text.font?.size)) || Number(text.font?.size) <= 0) {
    errors.push(`texts[${index}].font.size must be positive`);
  }
}

for (const [index, asset] of (contract.assets ?? []).entries()) {
  checkId(asset, `assets[${index}]`);
  checkBbox(asset, `assets[${index}]`);
  if (!asset.policy) errors.push(`assets[${index}].policy is required`);
  if (mode === "native-first" && /raster|image|bitmap/i.test(asset.policy ?? "")) {
    errors.push(`native-first asset cannot be raster: ${asset.id}`);
  }
}

for (const [index, connector] of (contract.connectors ?? []).entries()) {
  checkId(connector, `connectors[${index}]`);
  if (!connector.from || !connector.to) errors.push(`connectors[${index}] requires from and to`);
}

if (!(contract.texts ?? []).length) warnings.push("contract contains no text objects");
if (!(contract.regions ?? []).length) warnings.push("contract contains no semantic regions");

const report = [
  `contract=${inputPath}`,
  `mode=${mode}`,
  `canvas=${width}x${height}`,
  `ids=${ids.size}`,
  `errors=${errors.length}`,
  `warnings=${warnings.length}`,
  ...errors.map((item) => `ERROR ${item}`),
  ...warnings.map((item) => `WARN ${item}`),
].join("\n") + "\n";

if (outputPath) await fs.writeFile(outputPath, report, "utf8");
process.stdout.write(report);
if (errors.length) process.exitCode = 1;
