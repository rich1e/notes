---
title: Research: SwiftUI 图文混排
category: synthesis
tags:
  - swiftui
  - uikit
  - nstextattachment
  - uitextview
  - rich-text
  - research
sources:
  - "[[references/apple-developer-nstextattachment-docs]]"
  - "[[skills/uiviewrepresentable-uitextview-rich-text]]"
  - "[[concepts/swiftui-rich-text-rendering-comparison]]"
  - "[[projects/dayfold/skills/nstextattachment-bounds-overflow]]"
  - "[[projects/dayfold/skills/uitextview-intrinsic-width-overflow]]"
  - "[[projects/dayfold/skills/auto-expanding-texteditor-scroll]]"
  - "[[projects/dayfold/skills/swiftui-editor-scrollview-vs-attachment]]"
  - "[[references/uikit-nstextattachment-vs-appkit]]"
  - "[[projects/dayfold/skills/dayone-photo-library-picker]]"
  - "[[projects/dayfold/skills/entry-editor-image-dirty-tracking]]"
created: 2026-09-03T03:30:00Z
updated: 2026-09-03T03:30:00Z
summary: 3-round research on SwiftUI inline image+text rendering:唯一可编辑方案是 UIViewRepresentable + UITextView,iOS 15+ bounds 行为变更,NSTextAttachment 内存陷阱(4032×3024 PNG = 48MB),read-only 与 editable 的鸿沟。
provenance:
  extracted: 0.55
  inferred: 0.35
  ambiguous: 0.10
base_confidence: 0.78
lifecycle: draft
lifecycle_changed: 2026-09-03
tier: supporting
---

# Research: SwiftUI 图文混排

## Overview

SwiftUI 中实现"图文混排"(rich text with inline images)有 4 类主流方案,但**唯一同时支持可编辑 + attachment 的方案是 `UIViewRepresentable` 包装 `UITextView`**。Apple 在 iOS 15 改变了 `NSTextAttachment` 的 layout 行为(直接设 `bounds` 变得不可靠),iOS 16+ 提供 SwiftUI native `AttributedString` 但 attachment 能力受限。read-only 渲染有多个第三方选项(MarkdownUI / Down / Markdownosaur)。

## Key Findings

### 1. 编辑器必须用 UIKit (2024-2026 共识)

- SwiftUI `TextEditor` 不支持 attachment(`Apple's `TextEditor` still doesn't support `NSTextAttachment` as of iOS 18`)
- SwiftUI `Text(AttributedString)` 支持 inline attachment,但 size 控制弱,无选区/拷贝能力
- 唯一可行:`UIViewRepresentable + UITextView`,Coordinator 处理 delegate(`UITextViewDelegate`)

> 关键架构细节见 [[skills/uiviewrepresentable-uitextview-rich-text]]

### 2. iOS 15+ NSTextAttachment 行为变更

- 直接设 `attachment.bounds` 在 iOS 15+ **变得不可靠**(Stack Overflow Q 69625941, Q 70368520, Apple Developer Forum Thread 691990)
- Apple 推动使用 `containerSize` + `baselineOffset` 或 override `textAttachmentBounds(for:...)`
- 同时引入 `NSTextAttachmentLayout` 协议族(view provider / dynamic bounds)

**对 dayfold 当前 fix 的影响**:`[[projects/dayfold/skills/nstextattachment-bounds-overflow]]` 用 `attachment.bounds.width = textContainer.size.width - padding*2`,这个方案在 iOS 14- 上有效,**iOS 15+ 上需额外 override 或换 `containerSize`**。这是一个已知 gap,应在 iOS 15+ 设备上重新验证。

### 3. NSTextAttachment 内存陷阱

- `UIImage` 自动解码并缓存全 bitmap(4 字节/像素)
- **4032×3024 PNG 解码后 = 48MB**
- NSTextAttachment 同步渲染,大图导致内存尖刺

**强制约束**:下 attachment 之前必须**降采样**到显示尺寸 — 使用 `CGImageSource` + `kCGImageSourceThumbnailMaxPixelSize` 或 iOS 15+ `preparingForDisplay()`。

参考 [[projects/dayfold/skills/dayone-photo-library-picker]] 已有 ≤2048px 降采样策略。

### 4. read-only vs editable 的鸿沟

SwiftUI native 方案**全部是只读**:
- `MarkdownUI` (gonzalezreal) — 自定义 CommonMark 解析 + SwiftUI native views,但无 edit
- `Down` (cmark) — 127ms 渲染 War and Peace,但 UIKit 输出非 SwiftUI
- `Markdownosaur` (基于 Apple swift-markdown) — GFM 扩展支持,但仍 UIKit

Apple `AttributedString(markdown:)` (iOS 15+) 只覆盖粗体/斜体/链接,**不支持 inline image / 代码块 / 表格**。

### 5. 决策矩阵

```
可编辑? → 是 → UIViewRepresentable + UITextView (唯一)
         └ 否 → SwiftUI native 优先
                ├  完整 Markdown + 代码高亮? → MarkdownUI + Splash
                ├  简单 inline 图 + Dynamic Type? → AttributedString (iOS 16+) + NSTextAttachment
                └  长文性能? → Down + 只读 UITextView
```

## Core Concepts

- [[concepts/swiftui-rich-text-rendering-comparison]] — 全方案矩阵 + 决策树
- [[references/uikit-nstextattachment-vs-appkit]] — iOS vs AppKit 的 imageBounds API 差异
- [[projects/dayfold/skills/nstextattachment-bounds-overflow]] — Pre-iOS 15 的 bounds 修复 + iOS 15+ gap
- [[projects/dayfold/skills/uitextview-intrinsic-width-overflow]] — intrinsicContentSize 撑宽根因
- [[projects/dayfold/skills/auto-expanding-texteditor-scroll]] — isScrollEnabled=false + 外层 ScrollView 范式
- [[projects/dayfold/skills/swiftui-editor-scrollview-vs-attachment]] — ScrollViewReader 反行为

## Entities & Tools

- [[references/apple-developer-nstextattachment-docs]] — NSTextAttachment 类 + iOS 15+ Layout 协议官方文档
- [[projects/dayfold/skills/dayone-photo-library-picker]] — Day One 风格选图 + ≤2048px 降采样
- [[projects/dayfold/skills/entry-editor-image-dirty-tracking]] — 编辑器图片脏标记与持久化
- [[references/ios-design-patterns]] — GoF 23种模式 + iOS 反模式
- [[references/cs193p-spring-2025]] — Stanford SwiftUI 核心课

## Contradictions & Open Questions

### Contradiction 1: iOS 15+ bounds 行为变更

- **Round 1 中的一篇资料**说"`bounds` 设置在 iOS 15+ 被忽略,推荐 `containerSize`"
- **Round 3 中 dayfold 实际 fix**仍用 `bounds.width = textContainer.size.width`
- **结论**:dayfold 当前 fix 在 iOS 15+ 设备上**可能失效**,需要后续验证 + 升级到 `containerSize` 或 override 路径

### Contradiction 2: SwiftUI AttributedString 的 attachment 能力

- **Round 1 文档**: "Text(AttributedString) supports inline NSTextAttachment, image renders inline at baseline"
- **Round 3 另一文档**: "SwiftUI TextEditor still doesn't support NSTextAttachment as of iOS 18"
- **可能的解释**: 两者**不冲突** — `Text(AttributedString)` 是只读渲染,支持 attachment;`TextEditor` 是编辑器,不支持 attachment。这是 read-only vs editable 的另一体现。

### Open Questions

1. **iOS 15+ dayfold fix 兼容性**: 现有 dayfold skill 在 iOS 15+ 上还能用吗?需要测或重写。
2. **AttributedString 的图片 size**: 能否通过 `AttributedString` 的 `.attachment` API 精确控制图片 size,还是只能渲染 baseline 尺寸?
3. **TextKit 2 (NSTextLayoutManager)**: 是否带来新的 inline image 能力?(Round 2 搜索无果,可能是 Apple 文档不全)
4. **MarkdownUI 是否放弃维护**: 据 Round 2 结果,"recent maintenance has shifted toward Textual (a broader text rendering engine), suggesting the original gonzalezreal/MarkdownUI is in mature/stable mode"。需要确认 fork 状态。

## Sources Consulted

### Web Sources

1. [Apple Developer — NSTextAttachment](https://developer.apple.com/documentation/uikit/nstextattachment)
2. [Apple Developer — NSTextAttachmentLayout](https://developer.apple.com/documentation/uikit/nstextattachmentlayout)
3. [Apple Developer — NSTextAttachmentViewProvider](https://developer.apple.com/documentation/uikit/nstextattachmentviewprovider)
4. [Apple Developer Forum Thread 691990 — iOS15 NSTextAttachment](https://developer.apple.com/forums/thread/691990)
5. [Apple Developer Forum Thread 696744 — iOS 15 image attachment behavior](https://developer.apple.com/forums/thread/696744)
6. [Stack Overflow Q 69625941 — NSTextAttachment bounds iOS 15](https://stackoverflow.com/questions/69625941/setting-nstextattachment-bounds-doesnt-work-on-ios-15)
7. [Stack Overflow Q 70368520 — NSTextAttachment.bounds does not work on iOS 15](https://stackoverflow.com/questions/70368520/nstextattachment-bounds-does-not-work-on-ios-15)
8. [Stack Overflow Q 72677713 — Restrict size of NSTextAttachment image](https://stackoverflow.com/questions/72677713/restrict-size-of-nstextattachment-image)
9. [Volcengine — iOS 15 NSTextAttachment.bounds 无效](https://www.volcengine.com/article/192454)
10. [Cocoanetics — Asynchronous NSTextAttachments](https://www.cocoanetics.com/2016/09/asynchronous-nstextattachments-22/)
11. [NSScreencast — Text Attachments](https://nsscreencast.com/episodes/217-text-attachments)
12. [Pete Hare — Rendering NSTextAttachment inline in a UITextView](https://petehare.com/inline-nstextattachment-rendering-in-uitextview)
13. [Markiv MarkdownUI DeepWiki](https://deepwiki.com/markiv/MarkdownUI)
14. [GitHub — MarkdownToAttributedString](https://www.github.com/madebywindmill/MarkdownToAttributedString)
15. [SwiftUI AttributedString vs NSAttributedString](https://swiftwithmajid.com/2024/12/01/swiftui-attributedstring-vs-nsattributedstring/)

### Vault Sources (cross-references)

- [[projects/dayfold/skills/nstextattachment-bounds-overflow]]
- [[projects/dayfold/skills/uitextview-intrinsic-width-overflow]]
- [[projects/dayfold/skills/auto-expanding-texteditor-scroll]]
- [[projects/dayfold/skills/swiftui-editor-scrollview-vs-attachment]]
- [[projects/dayfold/skills/dayone-photo-library-picker]]
- [[projects/dayfold/skills/entry-editor-image-dirty-tracking]]
- [[references/uikit-nstextattachment-vs-appkit]]
- [[references/cs193p-spring-2025]]
- [[references/ios-design-patterns]]

## Related

- [[entities/rzcolorfulswift]] — rztime 的中国本土 iOS 富文本工具库(链式 attributedString + markdown 互转 + 自动折叠);UIKit era 成熟方案,与本 vault 的现代 markdown render 方案互补
- [[entities/markdownui]] — MarkdownUI 已宣布 maintenance mode (2024-2025 公告,讨论 #437),新开发在 Textual;原 Open Question #4 现已确认
- [[entities/swift-markdown]] — Apple 官方 Swift Markdown (cmark-gfm 集成),被 MarkdownView/RichText/DocC/X-Grok/Hugging Face Chat 采用
- [[references/textual-package]] — gonzalezreal/Textual 仓库参考(Swift 6.0,13188 LOC,iOS 18+)
- [[references/rzcolorfulswift-package]] — rztime/RZColorfulSwift 仓库参考(Swift 6.0,2723 LOC)
- [[references/markdownview-package]] — LiYanan2004/MarkdownView 仓库参考(Swift 6.2,11124 LOC,被 X/Grok + Hugging Face Chat 采用)
- [[references/nstextattachment-tap-detection]] — NSTextAttachment 点击检测参考(URL scheme 模式)
- [[references/uikit-nstextattachment-vs-appkit]] — UIKit NSTextAttachment 与 AppKit 差异(API gap)
