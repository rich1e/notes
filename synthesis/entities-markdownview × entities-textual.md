---
title: "MarkdownView × Textual — gonzalezreal 渲染引擎的代际演进"
category: synthesis
tags:
  - swiftui
  - markdown
  - markdownview
  - textual
  - gonzalezreal
  - rendering-engine
sources:
  - "[[entities/markdownview]]"
  - "[[entities/textual]]"
  - "[[entities/markdownui]]"
  - "[[references/markdownview-package]]"
  - "[[references/textual-package]]"
  - "[[references/swift-markdown-package]]"
  - "[[concepts/swiftui-rich-text-rendering-comparison]]"
created: "2026-09-06T15:45:00Z"
updated: "2026-09-06T15:45:00Z"
summary: "MarkdownView（iOS 16+，生产验证：X/Grok + Hugging Face Chat）与 Textual（iOS 18+，同作者精神继任）的代际对比；2024-2025 同一作者的 SwiftUI markdown 渲染范式迁移。"
provenance:
  extracted: 0.45
  inferred: 0.45
  ambiguous: 0.10
base_confidence: 0.78
lifecycle: draft
lifecycle_changed: "2026-09-06"
tier: supporting
---

# MarkdownView × Textual — gonzalezreal 渲染引擎的代际演进

## The Connection

同作者（gonzalezreal）在 2022-2025 期间连续推出两个 SwiftUI markdown 渲染库，跨度覆盖 iOS 16 到 iOS 18+ 的范式迁移：

- **MarkdownView (2022-07 起)** — 基于 `Layout` 协议 + `FlowLayout` + 相邻 Text 合并的"工程技巧"派
- **Textual (2025)** — 基于 Foundation `AttributedString` built-in parser + 复用 `SwiftUI.Text` 渲染 pipeline 的"系统原生"派

这不是简单的"新版替代旧版"——**两个库并存**反映 Apple SwiftUI 自身在这 3 年里提供了更好的 markdown 渲染原语，让"自己写 markdown parser"的必要性逐步下降。

## Where They Co-occur

5 个 vault 页面同时引用两个 entity：

1. `[[concepts/swiftui-rich-text-rendering-comparison]]` — 渲染方案对比矩阵
2. `[[entities/markdownview]]` ↔ `[[entities/textual]]`（互相引用）
3. `[[references/markdownview-package]]` + `[[references/textual-package]]` — 仓库参考页
4. `[[entities/rzcolorfulswift]]` — 中国本土同类方案
5. `[[references/swift-markdown-package]]` — Apple 官方底层 cmark-gf

## Cross-cutting Insight

**MarkdownView 适合"中等门槛 + 生产验证"，Textual 适合"前沿 SwiftUI 平台"。**

| 维度 | MarkdownView | Textual |
|------|--------------|---------|
| Platform floor | iOS 16+ / macOS 13+ / visionOS 1+ | iOS 18+ / macOS 15+ / visionOS 2+ |
| 核心渲染机制 | 自写 `Layout` 协议 + 文本节点合并 | 复用 SwiftUI.Text 渲染 pipeline |
| Parser 后端 | swift-markdown (cmark-gfm) | Foundation `AttributedString` built-in |
| 富文本能力 | `AttributedString` 自定义样式 | `SwiftUI.Text` 内建支持 |
| 图像支持 | 通过 `Highlightr` 集成 | 通过 `SwiftMath` 集成 |
| 选择/编辑 | 通过同作者 `RichText` 库 | 内建 + `AttributedString.selection` |
| 生产部署 | X/Grok + Hugging Face Chat 已知采用 | 较新，生产案例少 |
| 维护状态 | 活跃 | 活跃（gonzalezreal 当前焦点）|

**关键启示**：当 Apple 提供原生支持（`AttributedString` 内建 markdown parser），自写 parser 的代码会自然萎缩——不是被废弃，而是失去增量价值。MarkdownView 的生产案例（X/Grok、Hugging Face）反映"iOS 16 是 2024 现实地板"，而 Textual 是"iOS 18+ 新项目首选"。

## Tensions and Trade-offs

1. **依赖外部 4 个库** vs**零依赖** — MarkdownView 依赖 `swift-markdown` + `Highlightr` + `SwiftMath` + `RichText`，Textual 全部内建或仅依赖 SwiftUI 系统 framework
2. **Layout 协议自定义 vs 系统渲染** — MarkdownView 在 iOS 16 自定义 `FlowLayout` 是工程亮点，但在 iOS 18+ SwiftUI.Text 已能正确处理 inline token，重写优势消失
3. **生产验证 vs 前沿技术** — MarkdownView 有真实高并发部署案例（X、Grok、Hugging Face 每天处理百万级 markdown），Textual 是新秀但设计更新

## Strongest Objection

> **测试**：MarkdownView 的"生产验证优势"是否会随 iOS 18+ 用户占比上升而消解？若 Apple 内部也用 Textual 范式（v0.9.0+），X/Grok 是否会在 2026-2027 年迁回 Textual？

这是一个可验证的市场问题——通过 GitHub commit history + App Store 版本时间线可以追踪。但目前没有公开数据点（X/Grok/Hugging Face 都没公开 markdown render 升级公告）。

## Open Questions

1. MarkdownView vs Textual 的"维护 mode"分界点是否会有官方声明？类似 MarkdownUI 那种[NOTE] 公告？
2. 是否存在"渐进迁移"路径——iOS 18+ 用 Textual，iOS 16-17 降级到 MarkdownView？
3. 同作者的 `RichText`（编辑器）能否与 Textual 配合，让"编辑 + 渲染"都用同一套 markdown 范式？

## Related

- [[entities/markdownview]]
- [[entities/textual]]
- [[entities/markdownui]] — gonzalezreal 的第一代（已 maintenance mode）
- [[entities/rzcolorfulswift]] — 中国本土同类方案（UIKit era）
- [[references/swift-markdown-package]] — Apple 官方 markdown 解析后端
- [[concepts/swiftui-rich-text-rendering-comparison]] — 4 代渲染方案对比矩阵
- [[references/fatbobman-swiftui-rich-text-layout]] — LiYanan（MarkdownView 作者）实战深度解析