---
title: SwiftUI 富文本 markdown 渲染方案对比
category: concepts
tags:
  - swiftui
  - markdown
  - nstextattachment
  - rich-text
  - cross-platform
sources:
  - "[[skills/uiviewrepresentable-uitextview-rich-text]]"
  - "[[references/apple-developer-nstextattachment-docs]]"
created: 2026-09-03T03:30:00Z
updated: 2026-09-03T03:30:00Z
summary: read-only 与 editable 富文本方案分两套栈:SwiftUI native (MarkdownUI / AttributedString) vs UIKit (UITextView + Down / MarkdownUI)。SwiftUI native 适合 read-only 显示,UIKit 适合编辑 + attachment。
provenance:
  extracted: 0.65
  inferred: 0.30
  ambiguous: 0.05
base_confidence: 0.75
lifecycle: draft
lifecycle_changed: 2026-09-03
tier: supporting
---

# SwiftUI 富文本 markdown 渲染方案对比

## Context

SwiftUI 富文本/图文混排选型有**两个轴**:read-only 显示 vs 可编辑,SwiftUI-native vs UIKit-bridged。下面是主流选项的对比。

## 矩阵对比

| 方案 | 渲染层 | 可编辑 | Attachment | 性能 | 体积 |
|---|---|---|---|---|---|
| SwiftUI `TextEditor` | SwiftUI Text | ✅ | ❌ | 快 | 0 依赖 |
| SwiftUI `Text(AttributedString)` | SwiftUI Text | ✅ | ⚠️ inline 但弱 | 快 | 0 依赖 |
| `MarkdownUI` (gonzalezreal) | SwiftUI 原生 views | ❌ | ⚠️ lazy image | 中(3-5× 快于 WebView) | + 依赖 |
| `AttributedString(markdown:)` (iOS 15+) | Foundation → SwiftUI | ❌ | ❌(仅粗体/斜体) | 快 | 0 依赖 |
| `Down` (cmark) → `NSAttributedString` | UIKit TextKit | ❌(可扩展) | ⚠️ hook 协议 | 快(War and Peace 127ms) | + 依赖 |
| `Markdownosaur` (基于 swift-markdown) | UIKit TextKit | ❌ | ⚠️ | 中(0.04s older devices) | + 依赖 |
| `UIViewRepresentable + UITextView` | UIKit TextKit | ✅ | ✅ 完整 | 快(基础 TextKit) | 0 依赖 |

## 决策树

```
需要编辑能力?
├─ 是 → UIViewRepresentable + UITextView ✅ 唯一方案
│         └─ 复杂表/代码块 → 自定义 NSTextAttachmentLayout (iOS 15+)
└─ 否 → SwiftUI native 优先
         ├─ Markdown 格式? → MarkdownUI
         │                  └─ 代码高亮 → MarkdownUI + Splash
         ├─ 简单 inline 图? → AttributedString(markdown:) + NSTextAttachment (iOS 16+)
         └─ 长文本性能优先? → Down + UITextView(只读)
```

## Read-only 与 Editable 的鸿沟

**关键洞察**:SwiftUI native 方案全部是**只读渲染** — `TextEditor` 不支持 attachment,`MarkdownUI` 没有 edit 模式,`AttributedString(markdown:)` 只覆盖粗体/斜体/链接。

唯一同时支持 edit + attachment 的方案是 **UIViewRepresentable + UITextView**(2024-2026 业界共识)。

## NSTextAttachment 内存陷阱

参考 [[skills/uiviewrepresentable-uitextview-rich-text]] 的架构,但有个**易忽视的成本**:

**4032×3024 PNG 解码后是 48MB**。NSTextAttachment 用 UIImage 内部存储,iOS 解码后缓存全 bitmap(4 字节/像素)。

**解决**:必须在下 attachment 之前**降采样**到显示尺寸(`CGImageSource` + `kCGImageSourceThumbnailMaxPixelSize`)。

## Read-only 性能数字

- **Down** (`cmark`): War and Peace 在 127ms 渲染完毕
- **MarkdownUI**: 解析速度比 WebView 方案快 3-5×, 内存占用低 60-70%
- **Apple `AttributedString(markdown:)`**: 极快但只覆盖基础格式

## 跨平台注意

- Apple `AttributedString` 与 `NSAttributedString` 不完全互通(SwiftUI 是值类型 + Sendable,UIKit 是引用类型)
- 转换:`AttributedString(NSAttributedString)` 和 `NSAttributedString(AttributedString)`
- 但 image attachment 在双向转换时会**丢失细节**(ImageRenderer vs UIImage)

## Related

- [[entities/rzcolorfulswift]] — rztime 的链式 API 工具库(iOS 11+,UIKit era);可在 UILabel/UITextView 一行设置 attributedText
- [[entities/markdownview]] — LiYanan 的 MarkdownView (iOS 16+),被 X/Grok + Hugging Face Chat 采用;MarkdownUI(iOS 15+) vs MarkdownView(iOS 16+) vs Textual(iOS 18+) 三方比较
- [[entities/textual]] — gonzalezreal 的 MarkdownUI 继任(2024+),SwiftUI text rendering engine, iOS 18+ / macOS 15+;MarkdownUI iOS 15+ Textual iOS 18+ 共存覆盖
- [[entities/markdownui]] — MarkdownUI (gonzalezreal) 仍可用但已 maintenance mode;新项目考虑 [Textual](https://github.com/gonzalezreal/textual) 继任
- [[entities/swift-markdown]] — Apple 官方 markdown parser (cmark-gfm backend),vault 内所有 SwiftUI markdown 渲染方案的解析后端
- [[skills/uiviewrepresentable-uitextview-rich-text]]
- [[references/apple-developer-nstextattachment-docs]]
- [[projects/dayfold/skills/auto-expanding-texteditor-scroll]]
- [[projects/dayfold/skills/entry-editor-image-dirty-tracking]]
- [[references/cs193p-spring-2025]]
- [[synthesis/Research: SwiftUI 图文混排]]