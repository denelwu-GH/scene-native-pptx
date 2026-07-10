# Scene Native PPTX

这是一个把高精度设计稿重建为稳定、原生、可编辑 PowerPoint 的 Codex Skill。

![方案评分对比](benchmarks/benchmark-comparison.svg)

核心工作流：

```text
内容 -> 设计契约 -> 视觉参考稿 -> scene.json
     -> 受约束 SVG -> 原生 DrawingML -> PPTX
```

它不把整页设计稿直接压成一张图片，也不依赖 OCR 猜测原文。设计契约负责锁定精确文字、语义区域、层级和可编辑策略；`scene.json` 负责把同一套结构稳定地输出为 SVG 和 PowerPoint。

## 适用场景

- 从内容和视觉参考生成高保真可编辑 PPT。
- 把截图或图片型页面重建为原生 PowerPoint 对象。
- 保持原文与布局，避免 OCR 漂移、图标切片错误和文字压图。
- 修复体积过大、对象关系异常、PowerPoint 提示修复的图片转 PPT 流程。

## 三种模式

- `native-first`：文字、卡片、连线、图标和图形全部使用原生 DrawingML，要求图片对象为 0。
- `hybrid-fidelity`：版式和文字保持原生，仅保留少量难以重画的透明 PNG/JPEG/WebP。
- `gorden-compat`：兼容传统的背景、框架、图标、文字四层逆向流程，仅用于已有位图页面的兜底。

## 安装

```bash
cp -R skill/scene-native-pptx ~/.codex/skills/scene-native-pptx
```

之后可在 Codex 中通过 `$scene-native-pptx` 调用。

## 实测结论

当前方案的加权评分为 **9.4/10**。相较最好的独立旧路线“组件化形状 + 图片图标”提升约 **2.0 分**；相较 HTML/DOM 路线提升约 **2.6 分**；相较同一技术线的受约束 SVG 验证原型提升 **0.6 分**。评分基于同类复杂科技信息图的实测，不代表所有页面类型。

当前原生样本包含 185 个原生形状、10 个组合、63 个文字对象和 0 张图片；在 PowerPoint for Mac 16.107 中完成打开、保存、关闭和重新打开，未出现修复提示。24.5 KB 的结果比 153.6 KB 组件化版本小 84.0%，比 1.44 MB 分层图片版本小 98.3%。

评分方法、原始数据和局限见 [benchmarks/methodology.md](benchmarks/methodology.md)。公开前的敏感信息检查见 [PUBLICATION_AUDIT.md](PUBLICATION_AUDIT.md)。
