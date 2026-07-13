# 首发文案：中文

## 标题

PPT手搓时代结束了：比 Canva、Gamma 更懂 PowerPoint 交付的铂金级 Skill

## 正文

Canva、Gamma、Beautiful.ai 很擅长视觉创作和 AI 生成初稿。但当页面已经定稿，收件人还要在 Microsoft PowerPoint 中继续改字、换色、移动模块时，真正难的是最后一公里。

很多图片转 PPT 的方案，最后都会落到两种妥协之一：要么保留设计感，但整页只剩一张图片；要么全部重画，但还原度和效率都不理想。

Scene Native PPTX 想解决的是这件事：把设计稿中真正需要继续修改的部分，重建为原生 PowerPoint 对象。

它会把文字、卡片、连接线、路径、渐变和语义分组做成可选择、可移动、可改色、可改文案的 DrawingML 对象；只有摄影、生成式插画等不适合原生表达的部分，才会作为独立、可替换的本地素材保留。

整个流程是：

```text
设计契约 -> scene.json -> 受约束 SVG -> 原生 DrawingML -> PPTX
```

目前公开样例已完成验证：

- 全原生页面：85 个原生形状、31 个可编辑文字对象、0 张图片；
- 混合高保真页面：53 个原生形状、22 个可编辑文字对象、1 个可替换视觉素材；
- 已通过 PowerPoint for Mac 打开、保存、关闭、重新打开验证，无修复提示；
- 每次提交都会运行公开树审计和双样本回归。

它不替代 Canva、Gamma 或 Beautiful.ai，而是补齐它们到原生可编辑 PowerPoint 交付之间的空白。可以把它理解为：Canva、Gamma、Beautiful.ai 负责把页面做漂亮，Scene Native PPTX 负责把页面交付成真正能改的 PowerPoint。

项目采用 MIT License，已经封装成可安装的 Codex Skill。

GitHub：https://github.com/denelwu-GH/scene-native-pptx

保留设计感，保留可编辑性，交付一份经得住 PowerPoint 的 PowerPoint。

## 短版

我开源了一个图生 PPT 工作流：Scene Native PPTX。它不把设计稿简单压成图片，而是通过 `scene.json`、受约束 SVG 和 DrawingML，把文字、卡片、连线、图形重建为原生可编辑 PPTX。MIT License：https://github.com/denelwu-GH/scene-native-pptx
