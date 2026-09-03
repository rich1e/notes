---
title: SwiftUI Markdown 渲染层 — MarkdownUI vs Textual 维护状态转移
category: references
tags:
  - swiftui
  - markdown
  - rendering
  - gonzalezreal
  - markdownui
  - textual
  - maintenance-mode
  - swift-package
sources:
  - "[[entities/markdownui]]"
  - "[[entities/swift-markdown]]"
created: 2026-09-03T04:50:00Z
updated: 2026-09-03T04:50:00Z
summary: gonzalezreal/swift-markdown-ui 仓库参考:MIT license,Swift 5.6 tools,7669 Swift LOC,基于 swift-cmark + NetworkImage + snapshot-testing。iOS 15+ / macOS 12+。maintenance mode 公告(讨论 #437)。
provenance:
  extracted: 0.92
  inferred: 0.06
  ambiguous: 0.02
base_confidence: 0.88
lifecycle: draft
lifecycle_changed: 2026-09-03
tier: peripheral
---

# SwiftUI Markdown 渲染层 — MarkdownUI vs Textual 维护状态转移

## Source

- **GitHub**: <https://github.com/gonzalezreal/swift-markdown-ui>
- **Documentation**: <https://github.com/gonzalezreal/swift-markdown-ui/discussions/437>(maintenance mode 公告)
- **继任项目**: <https://github.com/gonzalezreal/textual>
- 作者:Guille Gonzalez (@gonzalezreal)
- License: MIT
- swift-tools-version: 5.6

## Repo Stats (shallow clone)

- 7669 Swift LOC

## Architecture

### Source Layout

```
Sources/MarkdownUI/
├── Views/                — `Markdown` SwiftUI View + blocks (Heading/Paragraph/CodeBlock/Table)
├── Parser/               — Markdown → Node tree (BlockNode + InlineNode + HTMLTag)
├── Renderer/             — Node → SwiftUI View (AttributedStringInlineRenderer + TextInlineRenderer)
├── Theme/                — Theme system (TextStyle protocol + BlockStyle)
└── Extensibility/        — Plugin points (ImageProvider, CodeSyntaxHighlighter)
```

### Public API Surface

```swift
// Main view
public struct Markdown: View

// Theme system
public struct Theme: Sendable
public protocol TextStyle
public struct FontStyle: TextStyle
public struct FontWeight: TextStyle
public struct FontFamily: TextStyle
public struct BackgroundColor: TextStyle
// ... 13+ TextStyle implementations

// Block style
public struct BlockConfiguration
public struct TableBorderStyle
public struct TaskListMarkerConfiguration

// Extensibility
public protocol InlineImageProvider
public struct AssetInlineImageProvider: InlineImageProvider
public struct DefaultInlineImageProvider
public protocol CodeSyntaxHighlighter
```

### Pipeline

```
Markdown String
    ↓ MarkdownParser (uses swift-cmark gfm)
Node Tree (BlockNode + InlineNode)
    ↓ Renderer (AttributedString / Text)
SwiftUI View Tree (Text + Layout)
```

### Dependencies (Package.swift)

- `swift-cmark` (Apple official — cmark-gfm C lib + extensions)
- `NetworkImage` (gonzalezreal 自己的另一库)
- `swift-snapshot-testing` (仅测试)

## Maintenance Status (关键)

**MarkdownUI 已进入 maintenance mode**(README 顶部 `[!NOTE]` 公告):

> "MarkdownUI is in maintenance mode. New Development is happening in [Textual](https://github.com/gonzalezreal/textual), a SwiftUI-native text rendering engine that evolved from the ideas and lessons learned in MarkdownUI."

**含义**:
- ✅ 现有 API 稳定 — 现有用户不受影响
- ❌ 不接受新特性(feature requests 不再合并)
- ❌ 不推荐新项目长期采用
- ➡️ 新项目/新需求 → 考虑 Textual(同一作者,继承思想 + lessons learned)

## 对 vault 既有研究的影响

### [[synthesis/Research: SwiftUI 图文混排]]

之前列为 Open Question #4:"MarkdownUI 是否放弃维护?" — 本次 ingest 直接**确认**已宣布 maintenance mode。

### [[concepts/swiftui-rich-text-rendering-comparison]]

更新维护状态:MarkdownUI 仍可用,但**不是新项目的首选**;Textual 是首选(如果接受新 lib 的话)。

## Platform Matrix (from Package.swift)

| 平台 | 最低 |
|---|---|
| macOS | 12.0 |
| iOS | 15.0 |
| tvOS | 15.0 |
| macCatalyst | 15.0 |
| watchOS | 8.0 |
| **高级特性(tables, multi-image)** | macOS 13 / iOS 16 / tvOS 16 / watchOS 9 |

## Use in Vault

- [[entities/markdownui]] — 实体视角
- [[synthesis/Research: SwiftUI 图文混排]] — vault 既有研究综述
- [[concepts/swiftui-rich-text-rendering-comparison]] — 全方案对比
- [[entities/swift-markdown]] — Apple 官方解析后端

## Verification

- Cloned: `git clone --depth 1 https://github.com/gonzalezreal/swift-markdown-ui.git /tmp/markdownui-clone`
- 7669 Swift LOC verified by `find Sources -name "*.swift" -exec wc -l`
- swift-tools-version 5.6 verified from `Package.swift` first line
- Maintenance mode confirmed by README `[!NOTE]` blockquote at top
- Author confirmed as `@gonzalezreal` (Guille Gonzalez)
- Platform matrix verified from `Package.swift` platforms array
- Dependency list verified: `swift-cmark` + `NetworkImage` + `swift-snapshot-testing`