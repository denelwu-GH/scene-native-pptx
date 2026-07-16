# 更新记录

这里记录 Scene Native PPTX 和 PPT Master 的重要公开变更。

English: [CHANGELOG.md](CHANGELOG.md)

## 尚未发布

### 新增

- 新增中英文 PPT Master 全流程图，展示两种起点、策略层、原生重建引擎、审批关卡和 PowerPoint 最终验证。

### 调整

- README 文案进一步以用户结果为中心，减少用户不容易理解的内部实现术语。
- 将整套 `$ppt-master` 使用提示词放在直接还原提示词之前。
- 扩展 Canva、Gamma 和 Beautiful.ai 对比说明，同时讲清前期策略能力和原生交付能力。
- 将 README 首屏和核心章节升级为更高冲击、更结果导向的营销表达，同时保留公开证据、评分方法和坦诚限制。

## [0.2.0] - 2026-07-16

### 新增

- 新增位于原生重建引擎之上的第一方 `ppt-master` 总控 Skill。
- 新增直接还原、原稿美化、整套策划和场景叙事四种路线。
- 新增整套简报、故事线、主张台账、页面合同、视觉角色设定和运行清单。
- 新增用户、项目、本次任务三级 PPT 偏好，以及明确的优先级和隐私规则。
- 新增整套设计 Token、可复用组件和受控的单页例外机制。
- 新增对比度、字号、页面标题、替代文本、阅读顺序、颜色表达和人物生成的包容性规则。
- 新增故事线审批和视觉设计审批两道独立关卡。
- 新增偏好覆盖、反馈范围、主张证据、对比度、审批和交付状态的自动验证。

### 调整

- `scene-native-pptx` 现在能够接收 PPT Master 已审批的上游合同，不再自行改写主张或受保护内容。
- 中英文产品介绍从“图片转可编辑 PPT 工具”升级为“双层 PPT 生产系统”。
- GitHub Actions 现在同时执行原生重建回归和 PPT Master 流程回归。

### 验证

- 公开目录隐私与敏感信息扫描通过。
- PPT Master 七项流程回归全部通过。
- Scene Native PPTX 两个公开样本全部通过，转换跳过数为 0。
- 发布提交 `035ac1e` 的 GitHub Actions 已通过。

## [0.1.0] - 2026-07-13

### 新增

- 发布原生可编辑 PowerPoint 重建引擎。
- 新增 `native-first`、`hybrid-fidelity` 和 `gorden-compat` 三种路线。
- 新增设计合同、场景、受约束 SVG、DrawingML、文件完整性、文字保留和 PowerPoint 实机往返校验。
- 新增两个公开合成回归样本、评分方法、效果图库和首个 Release 演示。

[0.2.0]: https://github.com/denelwu-GH/scene-native-pptx/releases/tag/v0.2.0
[0.1.0]: https://github.com/denelwu-GH/scene-native-pptx/releases/tag/v0.1.0
