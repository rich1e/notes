---
title: MarkdownView Package — LiYanan 的 SwiftUI Markdown 渲染实现
category: references
tags:
  - swiftui
  - markdown
  - rendering
  - liyanan
  - swift-markdown
  - rich-text
  - swift-package
  - iOS-16
sources:
  - "[[entities/markdownview]]"
  - "[[entities/swift-markdown]]"
created: 2026-09-03T05:10:00Z
updated: 2026-09-03T05:10:00Z
summary: LiYanan2004/MarkdownView 仓库参考:11124 Swift LOC,Swift 6.2 tools,基于 Apple swift-markdown,集成 Highlightr + SwiftMath + RichText 4 个依赖。iOS 16+ / macOS 13+ / visionOS 1+。
provenance:
  extracted:0.90
  inferred:0.08
  ambiguous:0.02
base_confidence:0.88
lifecycle:draft
lifecycle_changed:2026-09-03
tier:peripheral
---

# MarkdownView Package — LiYanan 的 SwiftUI Markdown 渲染实现

## Source

- **GitHub**: <https://github.com/LiYanan2004/MarkdownView>
- **Swift Package Index**: <https://swiftpackageindex.com/LiYanan2004/MarkdownView>
- **作者**: LiYanan (高一生,GitHub @LiYanan2004,X/Twitter @LiYanan2004)
- License: 同 Swift Package 标准(参见 LICENSE)
- swift-tools-version: 6.2

## Repo Stats (shallow clone)

- 11,124 Swift LOC

## Architecture

### Source Layout

```
Sources/MarkdownView/
├── MarkdownView.swift              — Main static view
├── MarkdownText.swift               — Inline markdown text view
├── MarkdownReader.swift            — Container with custom renderers
├── StreamingMarkdownReader.swift   — Incremental streaming view
├── MarkdownTableOfContentReader.swift — TOC view
├── Configuration/                  — MarkdownComponent + parsing options
│   ├── MarkdownTintableComponent.swift
│   └── MarkdownComponent.swift
├── Parser/                         — MarkdownDocumentParsingOptions + ParseResult
├── Math/                           — LaTeX math context
└── Styles/                         — Style protocols + concrete impls
    ├── Tables/                     — Github/Default/Grid MarkdownTableStyle
    ├── Lists/                      — Ordered/Unordered marker protocols
    └── Code Blocks/                — Highlightr integration
```

### Public API Surface

```swift
// Main Views
public struct MarkdownView: View
public struct MarkdownText: View
public struct MarkdownReader<Content: View>: View
public struct StreamingMarkdownReader<Content: View>: View
public struct MarkdownTableOfContentReader<Content: View>: View

// Configuration
public enum MarkdownComponent: Hashable, Sendable, CaseIterable
public enum MarkdownTintableComponent: Hashable, Sendable
public struct MarkdownDocumentParsingOptions: OptionSet, Sendable, Hashable
public struct MarkdownParseResult: Sendable

// Math
public struct MarkdownMathContext: Sendable, Hashable

// Style Protocols + Implementations
public protocol MarkdownTableStyle
public struct GithubMarkdownTableStyle: MarkdownTableStyle
public struct DefaultMarkdownTableStyle: MarkdownTableStyle
public struct GridMarkdownTableStyle: MarkdownTableStyle
public protocol MarkdownOrderedListMarkerProtocol
public protocol MarkdownUnorderedListMarkerProtocol
public struct CodeHighlighterTheme: Hashable, Sendable
```

### Dependencies (Package.swift)

```swift
.package(url: "https://github.com/swiftlang/swift-markdown.git", from: "0.8.0"),
.package(url: "https://github.com/raspu/Highlightr.git", from: "2.3.0"),
.package(url: "https://github.com/mgriebling/SwiftMath.git", from: "1.7.3"),
.package(url: "https://github.com/LiYanan2004/RichText.git", from: "1.0.0"),
```

| 依赖 | 作者 | 用途 |
|---|---|---|
| **swift-markdown** | Apple | CommonMark / GFM 解析 |
| **Highlightr** | raspu | 代码语法高亮 |
| **SwiftMath** | mgriebling | LaTeX 数学公式 |
| **RichText** | **LiYanan 自己** | iOS 文本选择支持 |

**关键洞察**:**RichText 是 LiYanan 自己写的独立 SwiftUI text editor lib**,从 MarkdownView 抽出。MarkdownView 通过 RichText 解决"iOS 上 SwiftUI 文本选择"问题 — 这是 vault [[synthesis/Research: SwiftUI 图文混排]] Open Question 的关键答案。

### Pipeline

```
Markdown String
    ↓ MarkdownParser (uses swift-markdown CommonMark)
Node Tree
    ↓ Style Protocols + Component configuration
SwiftUI View Tree (Native views via Layout protocol)
```

## Platform Matrix

| 平台 | 最低 |
|---|---|
| macOS | 13.0 |
| iOS | 16.0 |
| tvOS | 16.0 |
| watchOS | 9.0 |
| visionOS | 1.0 |

**比较**:
- MarkdownUI: iOS 15+ / macOS 12+(更低)
- MarkdownView: iOS 16+ / macOS 13+(本文)
- Textual: iOS 18+ / macOS 15+(最高)

MarkdownView 在中等门槛,iOS 16+ 项目可用。

## Use Cases (Adoption)

**X/Grok (xAI)** + **Hugging Face Chat** = 知名 production users。
这是 SwiftUI markdown 渲染生态中**实战 production 验证最强**的方案(超过 MarkdownUI)。

## Use in Vault

- [[entities/markdownview]] — 实体视角
- [[references/fatbobman-swiftui-rich-text-layout]] — LiYanan 实战深度解析
- [[entities/swift-markdown]] — Apple 解析后端
- [[entities/markdownui]] — 同类 read-only markdown 库(对比)
- [[entities/textual]] — iOS 18+ 更前沿方案
- [[synthesis/Research: SwiftUI 图文混排]] — vault 既有研究综述

## Verification

- Cloned: `git clone --depth 1 https://github.com/LiYanan2004/MarkdownView.git /tmp/markdownview-clone`
- 11,124 Swift LOC verified by `find Sources -name "*.swift" -exec wc -l`
- swift-tools-version 6.2 verified from `Package.swift` first line
- Platform matrix verified from `Package.swift` platforms array
- Dependency list verified: `swift-markdown` + `Highlightr` + `SwiftMath` + `RichText` (4 dependencies, all confirmed)
- Adopted by X/Grok + Hugging Face Chat (confirmed via Fatbobman article)
- Public API: 5 Views + Configuration + Style protocols confirmed via grep