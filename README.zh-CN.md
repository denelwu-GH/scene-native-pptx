<div align="center">

# PPT Master + Scene Native PPTX

### PPT 手搓时代结束了：比 Canva、Gamma 更懂 PowerPoint 交付的铂金级 Skill

**扔进一句需求、旧 PPT、Word/PDF、截图或完整设计稿，出来一套能汇报、能修改、能交付的原生 PowerPoint。**

这不是又一个只会帮你排版的 AI。它把**故事线、证据、整套设计、用户偏好、原生可编辑生产和 PowerPoint 实机验收**装进同一条流水线。装一次，把反复熬夜手搓 PPT 变成可以复用的专业生产系统。

<p>
  <a href="https://github.com/denelwu-GH/scene-native-pptx/actions/workflows/ci.yml"><img alt="回归测试" src="https://github.com/denelwu-GH/scene-native-pptx/actions/workflows/ci.yml/badge.svg"></a>
  <a href="https://github.com/denelwu-GH/scene-native-pptx/releases/tag/v0.2.0"><img alt="v0.2.0 版本" src="https://img.shields.io/badge/%E7%89%88%E6%9C%AC-v0.2.0-7C3AED.svg"></a>
  <a href="LICENSE"><img alt="MIT License" src="https://img.shields.io/badge/license-MIT-16A34A.svg"></a>
  <img alt="原生可编辑 PowerPoint" src="https://img.shields.io/badge/PowerPoint-%E5%8E%9F%E7%94%9F%E5%8F%AF%E7%BC%96%E8%BE%91-0F766E.svg">
  <img alt="实测评分 9.4 分" src="https://img.shields.io/badge/%E5%AE%9E%E6%B5%8B%E8%AF%84%E5%88%86-9.4%2F10-2563EB.svg">
</p>

<p><a href="README.md">English</a> | <strong>简体中文</strong> · <a href="CHANGELOG.zh-CN.md">更新记录</a></p>

</div>

<p align="center">
  <img src="benchmarks/gallery/agentic-operating-system-showcase.png" alt="由 Scene Native PPTX 生成的高品质原生可编辑 PowerPoint" width="100%">
</p>

<p align="center"><strong>不是把图片塞进 PPT，而是把设计稿真正变成 PPT。</strong></p>

<p align="center">
  <img src="benchmarks/gallery/scene-native-pptx-demo.gif" alt="Scene Native PPTX 从设计目标到原生可编辑 PowerPoint 的演示" width="100%">
</p>

<p align="center"><sub>设计目标 → 语义分层 → 原生对象 → 可编辑 PowerPoint</sub></p>

## 你可能再也不想手搓 PPT 了

市面上很多工具能生成“看起来像 PPT 的东西”，但真正交付时，代价通常还是由你承担：

- 保留完整设计稿，但整页只剩一张无法编辑的图片；
- 用 OCR 恢复文字，但接受错字、漏字和排版漂移；
- 把图标和框架切成脆弱的图片图层；
- 全部手工重画，但失去原设计的精致感。

**PPT Master 先把内容变成一套能讲清楚、能说服人的演示；Scene Native PPTX 再把设计稿重建为真正的 PowerPoint 内容。** 在 `native-first` 模式下，文字、卡片、连接线、图标、渐变和语义分组都会成为可选择、可移动、可改色、可改文案的原生 DrawingML 对象。

## 一个 Skill 栈，接管 PPT 全流程

从“我只有一堆资料”到“这份 PPT 可以发给老板了”，两层 Skill 各自负责最擅长的部分：

| Skill | 负责什么 |
| --- | --- |
| **`ppt-master`** | 受众与原稿审计、故事线、主张与证据、用户和项目偏好、整套设计系统、包容性设计、审批关卡和整套 QA |
| **`scene-native-pptx`** | 高保真视觉重建、受约束 SVG、原生 DrawingML 转换、文件校验和 PowerPoint 实机往返 |

<p align="center">
  <img src="benchmarks/gallery/ppt-master-workflow.zh-CN.svg" alt="PPT Master 从原始资料到原生可编辑 PowerPoint 的完整流程" width="100%">
</p>

<p align="center"><sub>手里有什么就从什么开始；先确认逻辑与设计，再交付真正可编辑的 PowerPoint。</sub></p>

| 你手上有什么 | 使用什么 | 最终得到什么 |
| --- | --- | --- |
| 一句话需求、原始资料或旧 PPT | `$ppt-master` | 故事线、证据、整套设计系统、视觉方向和原生交付 |
| 截图或已经确认的设计稿 | `$scene-native-pptx` | 高保真原生可编辑重建 |

已经有完整设计稿时，可以直接使用底层引擎；还需要先把事情讲清楚时，就从 PPT Master 开始。

## 真正进入 PowerPoint 的效果

<table>
  <tr>
    <td width="50%" align="center">
      <img src="benchmarks/gallery/native-output.png" alt="全原生可编辑 PowerPoint 输出"><br>
      <strong>全原生输出</strong><br>
      85 个原生形状 · 31 个可编辑文字对象 · 0 张图片
    </td>
    <td width="50%" align="center">
      <img src="benchmarks/gallery/hybrid-output.png" alt="混合高保真可编辑 PowerPoint 输出"><br>
      <strong>混合高保真输出</strong><br>
      53 个原生形状 · 22 个可编辑文字对象 · 1 个可替换素材
    </td>
  </tr>
</table>

以上均为公开合成回归页面，并且是在 Microsoft PowerPoint 实机保存、关闭和重新打开后渲染得到的真实结果。

## 为什么 PPT 重度用户会需要它

| 你的真实需求 | 双 Skill 系统的交付结果 |
| --- | --- |
| 手里只有零散资料，不知道怎么组织 | PPT Master 把资料转成故事线、主张台账和逐页生产合同 |
| 不想每次重复解释自己的偏好 | 明确偏好可以按用户、项目或本次任务保存，同时不把客户 PPT 内容写入长期档案 |
| 页面还要有设计感 | 先生成或读取视觉设计稿，并始终把它作为还原目标 |
| 文案不能被 AI 改写或 OCR 识别错 | 文字来自设计契约，不靠 OCR 猜测 |
| 后续还要改字、改色、移动模块 | 文字、卡片、路径、连接线和分组都是原生对象 |
| 文件必须正常打开 | 校验 ZIP、XML、关系、ID、越界，并完成 PowerPoint 实机往返 |
| 团队需要稳定复用 | `scene.json` 是 SVG 和 PPTX 的确定性统一数据源 |
| 有复杂插画又不想整页压图 | 只把难以原生表达的局部素材保留为可替换图片 |

## Canva、Gamma 做到初稿，我们继续做到交付

Canva、Gamma 和 Beautiful.ai 很适合视觉创作、AI 生成初稿和浏览器内演示。但对必须交付 `.pptx`、继续改字改色、适配企业模板、经得住领导逐页修改的重度用户来说，**生成出来只是上半场，PowerPoint 里还能不能继续工作才是下半场。**

- PPT Master 可以更早从原始资料、旧 PPT、汇报对象和审批约束开始工作；
- 以已经通过视觉确认的设计稿为目标，也可以从其他工具导出的页面图片开始；
- 把关键文字、几何图形、卡片、路径和连接线重建为原生 PowerPoint 内容；
- 交付一份收件人仍可在 Microsoft PowerPoint 中继续修改、无需重画的 `.pptx`。

**还需要梳理逻辑时使用 PPT Master；设计已经确认时使用 Scene Native PPTX 完成原生交付。** 我们不和浏览器生成工具争“谁更快出第一稿”，我们解决的是它们经常没有继续完成的最后一公里：**原生、可编辑、可复用、能通过 PowerPoint 实机验收。** 这是交付链路定位，不代表与上述品牌存在关联，也不是无条件的产品排名。

## 从设计稿到可编辑对象

```text
内容 -> 设计契约 -> 视觉参考稿 -> scene.json
     -> 受约束 SVG -> 原生 DrawingML -> PPTX
```

- **视觉参考稿**负责控制设计意图。
- **设计契约**负责锁定精确文字、语义区域、层级和可编辑策略。
- **`scene.json`**确定性生成受约束 SVG 和原生 PowerPoint。
- **PowerPoint 实机往返**是最终兼容性门禁。

<p align="center">
  <img src="benchmarks/gallery/semantic-layer-exploded-view.png" alt="Scene Native PPTX 将设计稿按语义拆解为可编辑图层" width="100%">
</p>

这不是按像素切片。每页会按 **背景**、**连接线**、**原生几何**、**图标与素材**、**可编辑文字** 五类语义层重建，最后汇成一个真正的 `.pptx`。团队真正需要改的内容仍然可以被选中、移动、改色和重写。

## 选择适合的模式

| 模式 | 最适合的页面 | 输出策略 |
| --- | --- | --- |
| `native-first` | 架构图、流程图、卡片页、仪表盘、信息图 | 全部使用原生 DrawingML，图片数量必须为 0 |
| `hybrid-fidelity` | 包含摄影、AI 插画、复杂光效或品牌素材的页面 | 文字和版式原生，仅保留少量可替换 PNG/JPEG/WebP |
| `gorden-compat` | 只有位图、没有结构化源稿的历史页面 | 使用背景、框架、图标和文字四层逆向作为兜底 |

## 30 秒，把 PPT 生产线装进 Codex

```bash
git clone https://github.com/denelwu-GH/scene-native-pptx.git
cp -R scene-native-pptx/skill/scene-native-pptx ~/.codex/skills/scene-native-pptx
cp -R scene-native-pptx/skill/ppt-master ~/.codex/skills/ppt-master
```

直接重建设计稿时调用 `$scene-native-pptx`，制作整套 PPT 时调用 `$ppt-master`。

## 一句话，让它接管下一套 PPT

```text
使用 $ppt-master，把这些资料制作成一套逻辑完整、视觉统一、具备包容性、
原生可编辑的 PowerPoint。先审计原稿，建立故事线和主张台账，再确定整套设计系统
和视觉方向；审批后调用 $scene-native-pptx 完成原生制作和交付验收。
```

已经有确认后的设计稿，可以直接使用底层引擎：

```text
使用 $scene-native-pptx，把这张幻灯片截图重建为高保真、原生、可编辑的
PowerPoint。严格保留原文和布局，默认使用 native-first；只有局部复杂插画
无法原生表达时才使用 hybrid-fidelity，并在交付前完成 PowerPoint 实机往返验收。
```

## 不是自封“最强”，是把五条路线真的跑了一遍

![可编辑 PowerPoint 重建方案评分](benchmarks/benchmark-comparison.svg)

| 实测路线 | 加权评分 | 主要限制 |
| --- | ---: | --- |
| 分层图片 + 可编辑文字 | 6.4 / 10 | 框架仍是位图，切片和去底质量不稳定 |
| 组件化形状 + 图片图标 | 7.4 / 10 | 曲线、渐变和阴影被明显简化 |
| HTML/DOM 转 PPTX | 6.8 / 10 | 复杂标题、径向图形和富文本容易漂移 |
| 受约束 SVG 验证原型 | 8.8 / 10 | 尚未形成完整语义契约和回归门禁 |
| **Scene JSON + 受约束 SVG + DrawingML** | **9.4 / 10** | 需要严格的场景建模和 PowerPoint 实机验收 |

这不是通用产品排名，而是针对同类复杂信息图页面的工程实测。评分综合了视觉还原度、可编辑性、PowerPoint 稳定性、可重复性和文件效率。完整规则见[评分方法](benchmarks/methodology.md)和[原始评分数据](benchmarks/benchmark-scores.json)。

## 敢写“铂金级”，就敢把证据放出来

- 实测原生样本包含 **185 个原生形状、10 个组合、63 个文字对象和 0 张图片**。
- PowerPoint for Mac 16.107 完成**打开、保存、关闭和重新打开，全程没有修复提示**。
- 公开双样本回归保留 **53 条精确契约文字，转换跳过数为 0**。
- 24.5 KB 的原生结果比组件化版本**小 84.0%**，比分层图片版本**小 98.3%**。
- 每次公开推送都会在 [GitHub Actions](https://github.com/denelwu-GH/scene-native-pptx/actions) 中执行泄露扫描和双样本回归。

## 自己运行回归测试

```bash
python3 ~/.codex/skills/scene-native-pptx/scripts/run_regression.py \
  --skill-dir ~/.codex/skills/scene-native-pptx \
  --output-dir /tmp/scene-native-pptx-regression

python3 ~/.codex/skills/ppt-master/scripts/run_regression.py \
  --skill-dir ~/.codex/skills/ppt-master \
  --output-dir /tmp/ppt-master-regression
```

底层引擎测试包含一张全原生智能编排页，以及一张插画可独立替换的混合模式页面。PPT Master 测试覆盖偏好优先级、反馈范围、主张证据、对比度、审批关卡和交付状态。

## 仓库结构

```text
skill/ppt-master/          整套 PPT 策略与生产总控
skill/scene-native-pptx/   原生可编辑 PowerPoint 底层引擎
benchmarks/                实测证据、评分方法、图表和效果图库
tools/                     公开样本、图表、元数据和审计工具
CHANGELOG.zh-CN.md         中文版本更新记录
PUBLICATION_AUDIT.md       发布前隐私与敏感信息审计
THIRD_PARTY_NOTICES.md     第三方依赖和许可声明
```

## 版本与更新记录

- [PPT Master v0.2.0](https://github.com/denelwu-GH/scene-native-pptx/releases/tag/v0.2.0)：新增整套 PPT 总控、分级偏好、设计系统、包容性设计、主张证据和审批关卡。
- [Scene Native PPTX v0.1.0](https://github.com/denelwu-GH/scene-native-pptx/releases/tag/v0.1.0)：首个公开版原生可编辑重建引擎。
- 查看完整[更新记录](CHANGELOG.zh-CN.md)。

## 坦诚说明当前限制

- 无法从所有任意截图中魔法般恢复百分之百准确的语义结构。
- 复杂模糊、噪点、遮罩、摄影素材和生成式插画应保留为独立图片素材。
- 不能只看像素指标，还必须检查文字换行、对象结构和 PowerPoint 修复行为。
- LibreOffice 和浏览器渲染只能作为辅助，不能替代 Microsoft PowerPoint 实机测试。

## 安全、隐私与许可

公开回归样本均为本仓库专门制作的合成示例，不包含客户演示文稿、企业 Logo、本机用户名或绝对源文件路径。准备公开自己的示例或分支前，请先阅读 [PUBLICATION_AUDIT.md](PUBLICATION_AUDIT.md)。

本仓库采用 [MIT License](LICENSE)。`skill/scene-native-pptx/assets/ppt-master` 中的转换器子集保留原始 MIT 许可，详情见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

---

<div align="center">

### 别再手搓下一套 PPT。把资料交给 PPT Master，把可编辑成品带走。

**[立即安装](#30-秒把-ppt-生产线装进-codex) · [查看实测](#不是自封最强是把五条路线真的跑了一遍) · [Read in English](README.md)**

</div>
