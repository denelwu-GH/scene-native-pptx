# Scene Native PPTX

[English](README.md) | [**简体中文**](README.zh-CN.md)

从视觉设计目标生成高保真、原生、可编辑的 PowerPoint，而不是把整页压成一张截图。

![方案评分对比](benchmarks/benchmark-comparison.svg)

核心工作流：

```text
内容 -> 设计契约 -> 视觉参考稿 -> scene.json
     -> 受约束 SVG -> 原生 DrawingML -> PPTX
```

视觉参考稿负责控制设计意图，设计契约负责锁定精确文字、语义区域、可编辑策略和安全约束；`scene.json` 则作为确定性生成 SVG 与 PowerPoint 的统一数据源。

## 为什么需要这套方案

传统图片转 PPT 工作流通常只能优化问题的一侧：

- 整页图片能够保留外观，但几乎无法编辑；
- OCR 加图片切片容易造成文字漂移、图标缺损和脆弱分层；
- HTML/CSS 导出虽然能生成可编辑文本框，却容易让复杂图表和连接关系变形；
- 不受约束的 SVG 转换可能生成 PowerPoint 不支持或需要修复的 OOXML。

Scene Native PPTX 使用受限制的场景模型和 SVG 规范，让文字、卡片、路径、连接线、渐变和语义分组保持为 PowerPoint 原生对象。只有确实不适合重画的局部插画或复杂视觉素材才保留为图片。

## 核心能力

- 以设计契约中的原文为准，不依赖 OCR 猜测文字。
- 支持图片对象为 0 的 `native-first` 原生模式。
- 支持仅保留局部 PNG/JPEG/WebP 素材的 `hybrid-fidelity` 混合模式。
- 提供稳定的语义分组和确定性的 scene-to-SVG 渲染。
- 不依赖 `python-pptx`，直接生成 DrawingML。
- 包含 ZIP、XML、关系目标、重复 ID、文字完整性、越界和视觉对比检查。
- 以 Microsoft PowerPoint 实机保存并重新打开作为最终兼容性门禁。
- 内置不含客户或品牌素材的双样本合成回归测试。

## 三种模式

- `native-first`：文字、卡片、连接线、图标、图表和装饰全部使用原生 DrawingML，图片对象必须为 0。
- `hybrid-fidelity`：版式和文字保持原生，仅将难以安全重建的局部插画保留为本地 PNG/JPEG/WebP。
- `gorden-compat`：仅在处理已有位图页面时，使用传统的背景、框架、图标和文字四层逆向流程作为兜底。

## 安装

将 Skill 目录复制或链接到 Codex Skills 目录：

```bash
cp -R skill/scene-native-pptx ~/.codex/skills/scene-native-pptx
```

之后可以在 Codex 中通过 `$scene-native-pptx` 调用。

## 快速验证

```bash
python3 ~/.codex/skills/scene-native-pptx/scripts/run_regression.py \
  --skill-dir ~/.codex/skills/scene-native-pptx \
  --output-dir /tmp/scene-native-pptx-regression
```

回归测试包含两个公开安全的合成样本：

- 高密度、全原生的智能编排架构页；
- 版式原生、插画独立可替换的混合模式页面。

## 实测评分

加权评分用于比较同类复杂信息图页面的工程实现效果，并不是普适的产品排名。评分综合了视觉还原度、可编辑性、PowerPoint 稳定性、可重复性和文件效率。完整规则见[评分方法](benchmarks/methodology.md)和[原始评分数据](benchmarks/benchmark-scores.json)。

| 实测路线 | 加权评分 | 主要限制 |
| --- | ---: | --- |
| 分层图片 + 可编辑文字 | 6.4 / 10 | 框架仍是位图，切片和去底质量不稳定 |
| 组件化形状 + 图片图标 | 7.4 / 10 | 曲线、渐变和阴影被明显简化 |
| HTML/DOM 转 PPTX | 6.8 / 10 | 复杂标题、径向图形和富文本容易漂移 |
| 受约束 SVG 验证原型 | 8.8 / 10 | 尚未形成完整语义契约和回归门禁 |
| **Scene JSON + 受约束 SVG + DrawingML** | **9.4 / 10** | 需要严格的场景建模和 PowerPoint 实机验收 |

当前原生样本包含 185 个原生形状、10 个组合、63 个文字对象和 0 张图片；在 PowerPoint for Mac 16.107 中完成打开、保存、关闭和重新打开，未出现修复提示。24.5 KB 的结果比 153.6 KB 组件化版本小 84.0%，比 1.44 MB 分层图片版本小 98.3%。

## 仓库结构

```text
skill/scene-native-pptx/   可直接安装的 Codex Skill
benchmarks/                评分方法、原始证据和图表
tools/                     公开样本与图表生成工具
PUBLICATION_AUDIT.md       发布前隐私与敏感信息审计
THIRD_PARTY_NOTICES.md     第三方依赖和许可声明
```

## 当前限制

- 不能自动从所有任意截图中恢复准确的语义结构。
- 复杂模糊、噪点、遮罩、摄影素材和生成式插画应保留为独立图片素材。
- 不能只依赖像素指标，还必须检查文字换行、对象结构和 PowerPoint 修复行为。
- LibreOffice 和浏览器渲染只能作为辅助检查，不能替代 Microsoft PowerPoint 实机往返测试。

## 安全与隐私

公开回归样本全部由程序生成，不包含客户演示文稿、企业 Logo、本机用户名或绝对源文件路径。准备公开自己的示例或分支前，请先阅读 [PUBLICATION_AUDIT.md](PUBLICATION_AUDIT.md)。

## 开源许可

本仓库采用 [MIT License](LICENSE)。`skill/scene-native-pptx/assets/ppt-master` 中包含的转换器子集保留原始 MIT 许可，详情见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
