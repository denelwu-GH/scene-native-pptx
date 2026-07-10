import fs from "node:fs/promises";

const [inputPath, outputPath] = process.argv.slice(2);
if (!inputPath || !outputPath) {
  throw new Error("Usage: node scene_to_svg.mjs <scene.json> <output.svg>");
}

const scene = JSON.parse(await fs.readFile(inputPath, "utf8"));

function escapeAttribute(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll('"', "&quot;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

function escapeText(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

function renderNode(node, depth = 1) {
  if (node.type === "#text") return escapeText(node.value);

  const indent = "  ".repeat(depth);
  const attributes = Object.entries(node.attrs ?? {})
    .map(([key, value]) => ` ${key}="${escapeAttribute(value)}"`)
    .join("");
  const children = node.children ?? [];

  if (!children.length) return `${indent}<${node.type}${attributes}/>`;

  const inlineTextOnly = children.every((child) => child.type === "#text" || child.type === "tspan");
  if (inlineTextOnly) {
    const inner = children.map((child) => {
      if (child.type === "#text") return escapeText(child.value);
      return renderNode(child, 0).trim();
    }).join("");
    return `${indent}<${node.type}${attributes}>${inner}</${node.type}>`;
  }

  const inner = children.map((child) => renderNode(child, depth + 1)).join("\n");
  return `${indent}<${node.type}${attributes}>\n${inner}\n${indent}</${node.type}>`;
}

const rootAttrs = Object.entries(scene.svg.attrs)
  .map(([key, value]) => ` ${key}="${escapeAttribute(value)}"`)
  .join("");
const body = [scene.svg.defs, ...scene.svg.layers]
  .filter(Boolean)
  .map((node) => renderNode(node, 1))
  .join("\n\n");
const output = `<?xml version="1.0" encoding="UTF-8"?>\n<svg${rootAttrs}>\n${body}\n</svg>\n`;

await fs.writeFile(outputPath, output, "utf8");
console.log(outputPath);

