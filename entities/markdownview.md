---
title: MarkdownView (LiYanan2004/MarkdownView)
category: entities
tags:
  - swiftui
  - markdown
  - rendering
  - commonmark
  - liyanan
  - streaming
  - latex
  - svg
  - iOS-16
  - library
  - entity
sources:
  - https://github.com/LiYanan2004/MarkdownView
  - https://github.com/LiYanan2004/RichText
  - https://swiftpackageindex.com/LiYanan2004/MarkdownView
source_url: https://github.com/LiYanan2004/MarkdownView
created: 2026-09-03T05:10:00Z
updated: 2026-09-03T05:10:00Z
summary: LiYanan 的 SwiftUI markdown 渲染库(2022-07 起),基于 Apple swift-markdown + CommonMark 完整支持,内置 SVG / LaTeX / streaming / 文本选择。被 X/Grok + Hugging Face Chat 采用。iOS 16+ / macOS 13+ / visionOS 1+。
provenance:
  extracted: 0.90
  inferred: 0.08
  ambiguous: 0.02
base_confidence: 0.88
lifecycle: draft
lifecycle_changed: 2026-09-03
tier: supporting
---

# MarkdownView (LiYanan2004/MarkdownView)

## Source

- **GitHub**: <https://github.com/LiYanan2004/MarkdownView>
- **Swift Package Index**: <https://swiftpackageindex.com/LiYanan2004/MarkdownView>
- **作者**: LiYanan (同一作者 [RichText](https://github.com/LiYanan2004/RichText))
- **首次发布**: 2022-07
- **采用方**: X / Grok (xAI) + Hugging Face Chat
- License: 同 Swift Package 协议(参见 LICENSE)
- swift-tools-version: 6.2
- Repo: 11,124 Swift LOC

## Platforms

- macOS 13.0+
- iOS 16.0+
- tvOS 16.0+
- watchOS 9.0+
- visionOS 1.0+

⚠️ 比 MarkdownUI (iOS 15+) 平台要求更高,比 Textual (iOS 18+) 低。

## Highlighted Features

- ✅ Full CommonMark compliance(基于 swift-markdown)
- ✅ Built-in SVG image support
- ✅ LaTeX math rendering(SwiftMath 集成)
- ✅ **Continuous text selection** on iOS and macOS
- ✅ Extensible rendering with block directives
- ✅ Customizable block styling
- ✅ **Streaming** rendering(`StreamingMarkdownReader` for incremental parsing)

## Dependencies (Package.swift)

```swift
.package(url: "https://github.com/swiftlang/swift-markdown.git", from: "0.8.0"),
.package(url: "https://github.com/raspu/Highlightr.git", from: "2.3.0"),
.package(url: "https://github.com/mgriebling/SwiftMath.git", from: "1.7.3"),
.package(url: "https://github.com/LiYanan2004/RichText.git", from: "1.0.0"),
```

| 依赖 | 用途 |
|---|---|
| **swift-markdown** (Apple) | CommonMark 解析 |
| **Highlightr** | 代码语法高亮 |
| **SwiftMath** | LaTeX 数学公式 |
| **RichText** (作者自己) | 内部富文本支持 / iOS 文本选择 |

⚠️ **关键依赖**: **`RichText` 是 LiYanan 自己写的独立 SwiftUI text editor lib**。MarkdownView 用 RichText 来实现"iOS 连续文本选择"能力。

## Public API

### 3 个核心 View

```swift
public struct MarkdownView: View        // 静态 markdown
public struct MarkdownText: View        // 行内 markdown (类似 SwiftUI Text)
public struct MarkdownReader<Content: View>: View   // Container with custom rendering
public struct StreamingMarkdownReader<Content: View>: View  // 流式
public struct MarkdownTableOfContentReader<Content: View>: View  // TOC
```

### Configuration

```swift
public enum MarkdownComponent: Hashable, Sendable, CaseIterable
public enum MarkdownTintableComponent: Hashable, Sendable
public struct MarkdownDocumentParsingOptions: OptionSet, Sendable, Hashable
```

### Style Protocols

```swift
public protocol MarkdownTableStyle
public struct GithubMarkdownTableStyle: MarkdownTableStyle
public struct DefaultMarkdownTableStyle: MarkdownTableStyle
public struct GridMarkdownTableStyle: MarkdownTableStyle
public protocol MarkdownOrderedListMarkerProtocol
public protocol MarkdownUnorderedListMarkerProtocol
public struct CodeHighlighterTheme: Hashable, Sendable
```

### Math

```swift
public struct MarkdownMathContext: Sendable, Hashable
```

## Architecture

### Source Layout

```
Sources/MarkdownView/
├── MarkdownView.swift              — Main static view
├── MarkdownText.swift               — Inline text view
├── MarkdownReader.swift            — Container with custom renderers
├── StreamingMarkdownReader.swift   — Streaming/incremental view
├── MarkdownTableOfContentReader.swift — TOC reader
├── Configuration/                  — MarkdownComponent, options
├── Parser/                         — MarkdownDocumentParsingOptions, ParseResult
├── Math/                           — LaTeX math context
├── Styles/                         — Table/List/CodeBlock style protocols + impls
│   ├── Tables/                     — Github/Default/Grid
│   ├── Lists/                      — Ordered/Unordered list markers
│   └── Code Blocks/                — Highlightr integration
└── Internals (presumably)
```

### Pipeline

```
Markdown String
    ↓ MarkdownParser (uses swift-markdown CommonMark)
Node Tree
    ↓ Style Protocols (custom)
SwiftUI View Tree (Native views, not AttributedString)
```

## Usage

### Static Markdown

```swift
let string = """
# MarkdownView

This is [MarkdownView](https://github.com/liyanan2004/MarkdownView).

MarkdownView renders Markdown with SwiftUI views.
"""

MarkdownView(string)
```

### Streaming

`StreamingMarkdownReader` 优化流式 markdown:
- scheduled document processing
- incremental parsing as new content arrives
- background document parsing

## 与 vault 既有研究的关系

### [[references/fatbobman-swiftui-rich-text-layout]]

LiYanan 在 fatbobman 文章详细描述了 MarkdownView 1.0 的实现细节(Layout 协议 + 相邻 Text 合并 + SVG + LaTeX)。本文的 MarkdownView 已进入更成熟版本(stable API + RichText 集成)。

### [[entities/swift-markdown]]

- swift-markdown (Apple):**解析器**层
- MarkdownView (LiYanan):**渲染层**(SwiftUI-native views over the AST)

### [[entities/markdownui]]

| 维度 | MarkdownUI | **MarkdownView** |
|---|---| | | |
| Author | gonzalezreal | **LiYanan** |
| Status | ⚠️ maintenance | ✅ active |
| CommonMark | ❌(GFM only via extensions) | ✅ |
| SVG | ❌ | ✅ built-in |
| LaTeX | ❌ | ✅ (SwiftMath) |
| Streaming | ❌ | ✅ `StreamingMarkdownReader` |
| Text selection | ❌(iOS TextRenderer fails) | ✅ (via RichText) |
| Production | ❌(limited) | ✅ X/Grok + Hugging Face Chat |

### [[entities/richtext]] (not yet in vault, future)

**RichText 是 LiYanan 的另一独立 lib**(从 MarkdownView 2.x 抽出):
- 通用 SwiftUI text editor
- 解决 TextRenderer vs textSelection 互斥
- MarkdownView 用 RichText 来支持 iOS 文本选择

### [[synthesis/Research: SwiftUI 图文混排]]

LiYanan 是 SwiftUI 富文本领域最重要的实战作者。MarkdownView + RichText 是其知识的两大产出。

## Adoption & Use Cases

适用:
- iOS 16+ SwiftUI app 渲染 markdown 文档
- 需要 streaming(聊天 / 实时 AI 输出)
- 需要 SVG / LaTeX 支持
- 需要 iOS 连续文本选择

不适用:
- 仅 macOS 12 或 iOS 15(平台不支持)
- 需要 edit 功能(→ RichText)
- 想要 MarkdownUI 同等 Theme 系统(更简洁)

## Related

- [[synthesis/entities-markdownview × entities-textual]] — 同一作者 gonzalezreal 的代际演进对比（MarkdownView iOS 16+ / Textual iOS 18+））

- [[references/fatbobman-swiftui-rich-text-layout]] — LiYanan 实战深度解析
- [[entities/swift-markdown]] — Apple 解析后端
- [[entities/markdownui]] — 同类 read-only markdown 库(对比)
- [[entities/textual]] — iOS 18+ 的更前沿方案
- [[synthesis/Research: SwiftUI 图文混排]] — vault 既有研究综述
- <https://github.com/LiYanan2004/RichText> — 同作者独立 lib

## Verification

- Cloned: `git clone --depth 1 https://github.com/LiYanan2004/MarkdownView.git /tmp/markdownview-clone`
- 11,124 Swift LOC verified by `find Sources -name "*.swift" -exec wc -l`
- swift-tools-version 6.2 verified from `Package.swift` first line
- Platform matrix verified from `Package.swift` platforms array (macOS 13+ / iOS 16+)
- Dependency list verified: `swift-markdown` + `Highlightr` + `SwiftMath` + `RichText` (all 4 dependencies confirmed)
- Adopted by X/Grok + Hugging Face Chat confirmed via Fatbobman article + LiYanan announcement
- Public API surface: 5 main Views (MarkdownView / MarkdownText / MarkdownReader / StreamingMarkdownReader / MarkdownTableOfContentReader) confirmed via grep