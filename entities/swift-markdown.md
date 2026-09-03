---
title: Swift Markdown
category: entities
tags:
  - apple
  - swift
  - markdown
  - parser
  - library
  - cmark
  - entity
sources:
  - https://github.com/swiftlang/swift-markdown
  - https://swiftlang.github.io/swift-markdown/documentation/markdown/
source_url: https://github.com/swiftlang/swift-markdown
created: 2026-09-03T04:30:00Z
updated: 2026-09-03T04:30:00Z
summary: Apple/Swift.org 官方开源 Markdown 解析库:Swift package,基于 GitHub cmark-gfm,提供不可变/persistent copy-on-write markup tree + visitor pattern。被 MarkdownView / RichText / DocC 等项目采用。
provenance:
  extracted: 0.90
  inferred: 0.08
  ambiguous: 0.02
base_confidence: 0.92
lifecycle: draft
lifecycle_changed: 2026-09-03
tier: supporting
relationships:
  - target: "[[references/fatbobman-swiftui-rich-text-layout]]"
    type: related_to
  - target: "[[synthesis/Research: SwiftUI 图文混排]]"
    type: related_to
---

# Swift Markdown

## Source

- GitHub: <https://github.com/swiftlang/swift-markdown>
- 文档: <https://swiftlang.github.io/swift-markdown/documentation/markdown/>
- Owner: Apple Inc. + Swift project authors
- License: Apache 2.0
- License Years: 2021-2023
- swift-tools-version: 6.2
- 总 Swift 代码: ~9000 行 (70 swift 文件)

## What It Is

Swift `Markdown` 是 **Apple 官方**的 Swift package,用于**解析、构建、编辑、分析** Markdown 文档。

- 解析器由 **GitHub-flavored Markdown's [cmark-gfm](https://github.com/github/cmark-gfm)** 驱动(因此严格遵循 spec)
- 提供 **immutable/persistent、thread-safe、copy-on-write** value type markup tree
- 设计哲学类似 [SwiftSyntax](https://github.com/swiftlang/swift-syntax)

## Core API

### Public Types (摘录)

```swift
// Base protocol
public protocol Markup {
    var children: MarkupChildren { get }
    func accept<V: MarkupVisitor>(_ visitor: V) -> V.Result
}

// Document
public struct Document: Markup, BasicBlockContainer {
    public init(parsing source: String, options: ParseOptions = .default)
    public init(parsing url: URL, options: ParseOptions = .default)
}

// Collections
public struct MarkupChildren: Sequence { ... }
public struct TypedChildIndexPath: RandomAccessCollection, ... { ... }

// Visitor
public protocol MarkupVisitor { ... }

// Directives
public struct DirectiveArgument: Equatable, Sendable
public protocol BlockDirective: BlockMarkup { ... }
```

### Basic Usage

```swift
import Markdown

let source = "This is a markup *document*."
let document = Document(parsing: source)
print(document.debugDescription())
// Document
// └─ Paragraph
//    ├─ Text "This is a markup "
//    ├─ Emphasis
//    │  └─ Text "document"
//    └─ Text "."
```

## Architecture

### 目录结构

```
Sources/Markdown/
├── Base/                       — 核心 protocol + Document
├── Block Nodes/                — Heading, Paragraph, List, CodeBlock
├── Inline Nodes/               — Text, Emphasis, Strong, Link, Code
├── Interpretive Nodes/          — Aside, AsideAutoTitle 等
├── Parser/                     — cmark-gfm 集成
├── Visitor/                    — MarkupVisitor protocol
├── Rewriter/                   — MarkupRewriter(改写树)
├── Structural Restrictions/     — protocol 约束(协议层 DSL)
└── Infrastructure/             — SourceLocation, Replacement
```

### 关键设计决策

1. **Copy-on-write value types**: `_MarkupData` 私有 struct 提供持久化数据,public `Markup` protocol 暴露接口。
2. **Protocol-Oriented Programming**: Structural Restrictions 大量使用 protocol 表达节点类型约束(`BasicBlockContainer`、`InlineContainer` 等),非 class hierarchy。
3. **Visitor Pattern**: 替代 tree walking,适合序列化、修改、重写场景。
4. **cmark-gfm 集成**: 解析器委托给 C 库(SwiftPM 包装),保持 spec 一致性。

## Adoption

- **MarkdownView** (LiYanan): 用 swift-markdown 解析 markdown,FlowLayout 拼装 — 见 [[references/fatbobman-swiftui-rich-text-layout]]
- **RichText** (LiYanan): 与 MarkdownView 同生态
- **DocC** (Apple 官方): 文档生成使用 swift-markdown 解析
- **X / Grok** (xAI): MarkdownView 被采用
- **Hugging Face Chat**: MarkdownView 被采用

## 与 vault 既有研究的关系

- [[synthesis/Research: SwiftUI 图文混排]] — 讨论 SwiftUI 富文本时引用 swift-markdown 是 MarkdownView 的解析后端
- [[references/fatbobman-swiftui-rich-text-layout]] — 详细描述 LiYanan 的 MarkdownView 1.0 如何使用 swift-markdown
- [[concepts/swiftui-rich-text-rendering-comparison]] — 与 MarkdownUI / Down 等 markdown 库对比时,Apple `AttributedString(markdown:)` 是最弱选项

## Use Cases for This Wiki

- 📌 **GitHub URL ingest 源** — Apple 官方库的权威参考资料
- 📌 **dayfold 应用** — dayfold 笔记 app 可选 swift-markdown 作为日记格式支持
- 📌 **所有 SwiftUI markdown 渲染方案的解析后端** — `AttributedString(markdown:)` (iOS 15+)、`Down`、`MarkdownUI`、`MarkdownView` 都依赖类似 parser

## Related

- [[references/fatbobman-swiftui-rich-text-layout]] — MarkdownView 实战
- [[synthesis/Research: SwiftUI 图文混排]] — vault 既有研究
- [[concepts/swiftui-rich-text-rendering-comparison]] — 全 markdown 渲染方案对比
- [[references/apple-developer-nstextattachment-docs]] — Apple 另一个核心文本 API
- https://swiftlang.github.io/swift-markdown/documentation/markdown/ — 官方文档

## Verification

- Repo cloned at /tmp/swift-markdown-clone (depth=1, 78 swift files, 9004 LOC)
- Public API verified by grep `^public` in Source files
- Repository: github.com/swiftlang/swift-markdown (Apple/Swift.org)
- License: Apache 2.0
- README quoted verbatim