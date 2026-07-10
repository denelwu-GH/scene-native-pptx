import fs from "node:fs/promises";

const [inputPath, contractPath, outputPath] = process.argv.slice(2);
if (!inputPath) throw new Error("Usage: node validate_scene.mjs <scene.json> [contract.json|-] [report.txt]");

const scene = JSON.parse(await fs.readFile(inputPath, "utf8"));
const allowed = new Set([
  "defs", "linearGradient", "radialGradient", "stop", "filter", "feGaussianBlur",
  "feOffset", "feFlood", "feComposite", "feMerge", "feMergeNode", "marker",
  "g", "rect", "circle", "ellipse", "line", "path", "polyline", "polygon",
  "text", "tspan", "image", "#text",
]);
const forbidden = new Set(["foreignObject", "mask", "textPath", "animate", "animateTransform", "script", "style", "use"]);
const counts = {};
const errors = [];
const warnings = [];
const ids = new Set();
const textParts = [];
const imageHrefs = [];
const width = Number(scene.canvas?.width);
const height = Number(scene.canvas?.height);
const mode = scene.mode ?? scene.metadata?.editablePolicy?.mode ?? (scene.metadata?.editablePolicy?.images === "none" ? "native-first" : "hybrid-fidelity");

function visit(node, pointer) {
  counts[node.type] = (counts[node.type] ?? 0) + 1;
  if (!allowed.has(node.type)) errors.push(`${pointer}: unsupported type ${node.type}`);
  if (forbidden.has(node.type)) errors.push(`${pointer}: forbidden type ${node.type}`);
  const id = node.attrs?.id;
  if (id) {
    if (ids.has(id)) errors.push(`${pointer}: duplicate id ${id}`);
    ids.add(id);
  }
  const transform = node.attrs?.transform ?? "";
  if (/matrix|skew/i.test(transform)) errors.push(`${pointer}: unsupported transform ${transform}`);
  if (node.type === "#text") textParts.push(node.value ?? "");
  if (node.type === "image") {
    const href = node.attrs?.href ?? node.attrs?.["xlink:href"] ?? "";
    imageHrefs.push(href);
    if (!href || /^(https?:|data:|file:|\/)/i.test(href)) errors.push(`${pointer}: image must use a local relative path`);
    if (href && !/\.(png|jpe?g|webp)$/i.test(href)) errors.push(`${pointer}: unsupported hybrid image format ${href}`);
  }
  for (const [index, child] of (node.children ?? []).entries()) visit(child, `${pointer}.children[${index}]`);
}

if (!Number.isFinite(width) || !Number.isFinite(height) || width <= 0 || height <= 0) {
  errors.push("scene canvas must have positive width and height");
}
if (Number(scene.svg?.attrs?.width) !== width || Number(scene.svg?.attrs?.height) !== height) {
  errors.push("scene canvas and svg width/height must match");
}

const layerIds = new Set();
for (const [index, layer] of (scene.svg?.layers ?? []).entries()) {
  const id = layer.attrs?.id;
  if (!id) errors.push(`svg.layers[${index}] is missing id`);
  if (layerIds.has(id)) errors.push(`duplicate layer id: ${id}`);
  layerIds.add(id);
  visit(layer, `svg.layers[${index}]`);
}
if (scene.svg?.defs) visit(scene.svg.defs, "svg.defs");
if (!(scene.svg?.layers ?? []).length) errors.push("scene must contain at least one semantic layer");
if (mode === "native-first" && imageHrefs.length) errors.push("native-first scene cannot contain image nodes");

if (contractPath && contractPath !== "-") {
  const contract = JSON.parse(await fs.readFile(contractPath, "utf8"));
  if (contract.mode && contract.mode !== mode) errors.push(`mode mismatch: scene=${mode}, contract=${contract.mode}`);
  const normalize = (value) => String(value).replace(/\s+/g, "").normalize("NFKC");
  const sceneText = normalize(textParts.join(""));
  for (const text of (contract.texts ?? [])) {
    if (!sceneText.includes(normalize(text.text))) errors.push(`contract text missing from scene: ${text.id}`);
  }
}

if (!scene.components?.length) warnings.push("scene.components is missing; author new scenes with semantic components");

const report = [
  `scene=${inputPath}`,
  `mode=${mode}`,
  `canvas=${width}x${height}`,
  `layers=${scene.svg?.layers?.length ?? 0}`,
  `layer_ids=${[...layerIds].join(",")}`,
  `node_counts=${JSON.stringify(counts)}`,
  `image_count=${imageHrefs.length}`,
  `errors=${errors.length}`,
  `warnings=${warnings.length}`,
  ...errors.map((item) => `ERROR ${item}`),
  ...warnings.map((item) => `WARN ${item}`),
].join("\n") + "\n";

const actualOutput = outputPath || (!contractPath || contractPath === "-" ? undefined : undefined);
if (actualOutput) await fs.writeFile(actualOutput, report, "utf8");
process.stdout.write(report);
if (errors.length) process.exitCode = 1;
