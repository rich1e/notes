---
title: Textual (gonzalezreal/textual)
category: entities
tags:
  - swiftui
  - text-rendering
  - markdown
  - gonzalezreal
  - swiftui-text
  - rendering-engine
  - iOS-18
  - library
  - entity
sources:
  - https://github.com/gonzalezreal/textual
  - https://github.com/gonzalezreal/swift-markdown-ui/discussions/437
source_url: https://github.com/gonzalezreal/textual
created: 2026-09-03T05:00:00Z
updated: 2026-09-03T05:00:00Z
summary: gonzalezreal MarkdownUI 继任者:SwiftUI text rendering engine 而非纯 Markdown lib。基于 SwiftUI Text 原生 pipeline + Foundation AttributedString parser,**iOS 18+ / macOS 15+**,平台门槛高于 MarkdownUI。两个新 View:InlineText(行内) + StructuredText(块)。
provenance:
  extracted: 0.88
  inferred: 0.10
  ambiguous: 0.02
base_confidence: 0.85
lifecycle: draft
lifecycle_changed: 2026-09-03
tier: supporting
---

# Textual (gonzalezreal/textual)

## Source

- **GitHub**: <https://github.com/gonzalezreal/textual>
- 作者: Guille Gonzalez (@gonzalezreal) — 同 MarkdownUI 作者
- **设计哲学**: MarkdownUI 继任者(参见 <https://github.com/gonzalezreal/swift-markdown-ui/discussions/437>)
- **平台**: macOS 15+ / iOS 18+ / tvOS 18+ / watchOS 11+ / visionOS 2+
- swift-tools-version: 6.0
- License: 同 MarkdownUI(MIT)

## 关键定位转变

> **"Textual is the spiritual successor to MarkdownUI, reimagined from the ground up"**
>
> **"MarkdownUI focuses on Markdown rendering; Textual is designed as a SwiftUI text rendering engine that happens to support Markdown."**

设计哲学差异:

| 维度 | MarkdownUI | Textual |
|---|---|---|
| **目标** | Markdown 渲染 | SwiftUI text 渲染 |
| **平台** | iOS 15+ / macOS 12+ | **iOS 18+ / macOS 15+**(更高门槛) |
| **parser** | swift-cmark (C) | **Foundation `AttributedString` built-in**(Swift 原生) |
| **2 个 View** | 单 `Markdown` | `InlineText`(行内) + `StructuredText`(块) |
| **渲染 pipeline** | 自定义 | **复用 SwiftUI.Text 渲染 pipeline** |

## 核心 API

### `InlineText`(行内富文本)

```swift
InlineText(
  markdown: """
    This is a *lighthearted* but **perfectly serious** paragraph where `inline code` lives \
    happily alongside ~~a terrible idea~~ a better one, a [useful link](https://example.com), \
    and a bit of _extra emphasis_ just for style.
    """
)
```

是 SwiftUI `Text` 的 drop-in replacement,支持 attachment + 综合样式。

### `StructuredText`(块文档)

```swift
StructuredText(
  markdown: """
    # Heading 1
    ## Heading 2
    Paragraph with [link](url) and ![image](src).
    - list item
    """
)
```

### Inline Styling System

```swift
InlineText(markdown: "Use `git status` to check _uncommitted changes_")
    .font(.custom("Avenir Next", size: 18))
    .textual.inlineStyle(
        InlineStyle()
            .code(.monospaced, .fontScale(0.85), .backgroundColor(.purple))
            .emphasis(.italic, .underlineStyle(.single))
    )
```

## Key Features

来自 README:
- ✅ Specialized views: `InlineText` + `StructuredText`
- ✅ **Native text selection** with proper copy-paste
- ✅ Markdown via Foundation `AttributedString` built-in parser
- ✅ **Custom markup parser** via `MarkupParser` protocol(可扩展)
- ✅ Inline attachments:images / custom emoji
- ✅ Math expressions:inline + block(用 SwiftUIMath)
- ✅ **Animated image** support: GIF / APNG / WebP
- ✅ Syntax highlighting with customizable themes
- ✅ Font-relative layout(随 Dynamic Type 缩放)

## Dependencies (Package.swift)

```swift
.package(url: "https://github.com/pointfreeco/swift-concurrency-extras", from: "1.3.1"),
.package(url: "https://github.com/pointfreeco/swift-snapshot-testing", from: "1.18.7"),
.package(url: "https://github.com/gonzalezreal/swiftui-math", from: "0.1.0"),
```

- **swiftui-math** (gonzalezreal 自己的另一 lib): 数学公式渲染
- **swift-concurrency-extras** (pointfreeco): async utilities
- **swift-snapshot-testing** (pointfreeco): 仅测试

## 与 vault 既有研究的关系

### [[entities/markdownui]]

- Textual 是 MarkdownUI 的**精神继任者**(同一作者)
- **不是** 1:1 替换 — 平台门槛 iOS 18+ vs MarkdownUI iOS 15+
- 新项目 **iOS 18+** → 优先选 Textual
- 维护 iOS 15-17 项目 → 继续用 MarkdownUI
- 两者**不冲突,可并存**

### [[synthesis/Research: SwiftUI 图文混排]]

之前 Research 列:
- "TextRenderer 在 iOS 18+ 是方向"(WWDC 2024)
- "MarkdownUI gonzalezreal"为对比方案之一

Textual 直接验证了"iOS 18+ SwiftUI-native"路线 — 比 MarkdownUI 更向前一步,完全在 SwiftUI 渲染 pipeline 上做文章。

### [[concepts/swiftui-rich-text-rendering-comparison]]

更新 read-only markdown 渲染方案的"现状"行:
| 方案 | SwiftUI native | Edit | Performance | Status |
|---|---|---|---|---|
| **Textual** | ✅✅ | ❌ | 复用 SwiftUI.Text | ✅ **active dev** |
| MarkdownUI | ✅ | ❌ | 快 | ⚠️ maintenance |

## Use in Vault

- 文本渲染层(只读)— SwiftUI `Text` 的真正替代品
- 支持 inline image + 数学公式 + 语法高亮
- 编辑需求 → 仍需 [[skills/uiviewrepresentable-uitextview-rich-text]] 路径

## Related

- [[entities/markdownui]] — 精神前身
- [[synthesis/Research: SwiftUI 图文混排]] — vault 既有研究综述
- [[concepts/swiftui-rich-text-rendering-comparison]] — 全方案对比
- [[references/swift-markdown-ui-package]] — MarkdownUI 仓库参考
- [[references/swift-markdown-package]] — Apple 官方解析后端
- <https://github.com/gonzalezreal/textual> — GitHub 仓库

## Verification

- Cloned: `git clone --depth 1 https://github.com/gonzalezreal/textual.git /tmp/textual-clone`
- 13,188 Swift LOC verified by `find Sources -name "*.swift" -exec wc -l`
- swift-tools-version 6.0 verified from `Package.swift` first line
- Platform matrix verified from `Package.swift` platforms array
- Dependency list verified: `swiftui-math` (math) + `swift-concurrency-extras` + `swift-snapshot-testing`
- Spirit-successor relationship confirmed via cross-link to MarkdownUI discussion #437