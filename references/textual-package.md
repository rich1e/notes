---
title: Textual Package — MarkdownUI 继任者
category: references
tags:
  - swiftui
  - text-rendering
  - gonzalezreal
  - markdownui
  - textual
  - swift-package
  - iOS-18
sources:
  - "[[entities/textual]]"
  - "[[entities/markdownui]]"
created: 2026-09-03T05:00:00Z
updated: 2026-09-03T05:00:00Z
summary: gonzalezreal/textual 仓库参考:MIT 风格 license,Swift 6.0 tools,13188 Swift LOC,基于 Foundation AttributedString parser + SwiftUI.Text 渲染 pipeline。iOS 18+ / macOS 15+ / visionOS 2+。MarkdownUI 继任者。
provenance:
  extracted: 0.90
  inferred: 0.08
  ambiguous: 0.02
base_confidence: 0.85
lifecycle: draft
lifecycle_changed: 2026-09-03
tier: peripheral
---

# Textual Package — MarkdownUI 继任者

## Source

- **GitHub**: <https://github.com/gonzalezreal/textual>
- **作者**: Guille Gonzalez (@gonzalezreal) — 同 MarkdownUI 作者
- 公告: <https://github.com/gonzalezreal/swift-markdown-ui/discussions/437>
- License: 同 MarkdownUI
- swift-tools-version: 6.0

## Repo Stats (shallow clone)

- 13,188 Swift LOC(几乎是 MarkdownUI 的 2 倍)

## Architecture

### Source Layout

```
Sources/Textual/
├── TextualNamespace.swift           — Public namespace
├── View+Textual.swift                — SwiftUI extensions
├── MarkupParser.swift               — `MarkupParser` protocol (default: Foundation)
├── FontScaled.swift                 — Font-relative layout
├── ColorEnvironmentValues.swift     — Color customization
├── TextEnvironmentValues.swift        — Text customization
├── DynamicColor.swift                — Dynamic color support
├── EmojiProperties.swift             — Emoji rendering
└MathProperties.swift                — Math properties
```

### Pipeline

```
Markdown String
    ↓ MarkupParser (default: Foundation AttributedString)
Attributed String
    ↓ Inline resolution (images, math, etc.)
SwiftUI.Text rendering pipeline
    ↓ SwiftUI Layout
Final View Tree
```

### Dependencies (Package.swift)

```swift
.package(url: "https://github.com/pointfreeco/swift-concurrency-extras", from: "1.3.1"),
.package(url: "https://github.com/pointfreeco/swift-snapshot-testing", from: "1.18.7"),
.package(url: "https://github.com/gonzalezreal/swiftui-math", from: "0.1.0"),
```

**关键依赖**:
- `swiftui-math` (gonzalezreal 自己的另一库)— 数学公式渲染
- `swift-concurrency-extras` (pointfreeco)
- `swift-snapshot-testing`(仅测试)

**注意**:不再依赖 `swift-cmark`!Textual 用 Foundation `AttributedString` built-in parser。

### Public API Surface

```swift
// 2 个核心 View
public struct InlineText: View
public struct StructuredText: View

// Inline styling
public struct InlineStyle
public protocol InlineStyleTrait

// Parser abstraction
public protocol MarkupParser

// Environment values
publicextension EnvironmentValues {
    var textual: TextualEnvironmentValues
}
```

## Platform Matrix

| 平台 | 最低 |
|---|---|
| macOS | 15.0 |
| iOS | 18.0 |
| tvOS | 18.0 |
| watchOS | 11.0 |
| visionOS | 2.0 |

⚠️ **平台要求明显高于 MarkdownUI**(iOS 18+ vs iOS 15+)— iOS 17 项目**不能**用 Textual。

## 与 MarkdownUI 的对比

| 维度 | MarkdownUI | Textual |
|---|---|---|
| Platform floor | iOS 15+ | **iOS 18+** |
| Parser | swift-cmark (C) | Foundation AttributedString |
| LOC | 7,669 | 13,188 (+72%) |
| Status | ⚠️ maintenance | ✅ active dev |
| 设计哲学 | Markdown 渲染 | SwiftUI text 引擎 |
| 2 个 View | 单 `Markdown` | `InlineText` + `StructuredText` |
| 数学公式 | ❌(社区库) | ✅ 一流支持(SwiftUIMath) |
| 动画图 | ❌ | ✅(GIF/APNG/WebP) |

## Design Evolution

来自 README 描述的设计转变:
- **MarkdownUI**: "SwiftUI view that renders Markdown"
- **Textual**: "SwiftUI text rendering engine that happens to support Markdown"

**含义**:Textual 是**通用文本引擎**,Markdown 只是其中一种 markup。

## Use in Vault

- [[entities/textual]] — 实体视角
- [[entities/markdownui]] — 精神前身(同作者)
- [[synthesis/Research: SwiftUI 图文混排]] — vault 既有研究综述
- [[concepts/swiftui-rich-text-rendering-comparison]] — 全方案对比

## Verification

- Cloned: `git clone --depth 1 https://github.com/gonzalezreal/textual.git /tmp/textual-clone`
- 13,188 Swift LOC verified by `find Sources -name "*.swift" -exec wc -l`
- swift-tools-version 6.0 verified from `Package.swift` first line
- Platform matrix verified from `Package.swift` platforms array
- Dependency list verified: `swiftui-math` + `swift-concurrency-extras` + `swift-snapshot-testing`
- 2-view architecture (`InlineText` + `StructuredText`) confirmed from README usage docs
- Spirit-successor relationship confirmed via cross-link to MarkdownUI discussion #437