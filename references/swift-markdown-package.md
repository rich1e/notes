---
title: Swift Markdown Package — 源码与文档
category: references
tags:
  - apple
  - swift
  - markdown
  - package
  - cmark-gfm
  - source-repo
sources:
  - https://github.com/swiftlang/swift-markdown
  - https://swiftlang.github.io/swift-markdown/documentation/markdown/
  - "[[entities/swift-markdown]]"
source_url: https://github.com/swiftlang/swift-markdown
created: 2026-09-03T04:30:00Z
updated: 2026-09-03T04:30:00Z
summary: Apple/Swift.org swift-markdown 仓库的参考:Apache 2.0 license, Swift 6.2 tools,基于 cmark-gfm,70 Swift 文件,9004 LOC,持久化 CoW markup tree。
provenance:
  extracted: 0.92
  inferred: 0.06
  ambiguous: 0.02
base_confidence: 0.90
lifecycle: draft
lifecycle_changed: 2026-09-03
tier: peripheral
---

# Swift Markdown Package — 源码与文档

## Source

- **GitHub**: <https://github.com/swiftlang/swift-markdown>
- **文档**: <https://swiftlang.github.io/swift-markdown/documentation/markdown/>
- **Owner**: Apple Inc. + Swift project authors
- **License**: Apache 2.0 (Copyright 2021-2023)
- **swift-tools-version**: 6.2

## Repo Stats (shallow clone)

- 70 Swift files
- 9,004 LOC

## Architecture

### Source Layout

```
Sources/Markdown/
├── Base/                       — Core protocol + Document
│   ├── Markup.swift              — `protocol Markup`
│   ├── Document.swift            — `struct Document`
│   ├── _MarkupData.swift         — Private CoW backing
│   ├── MarkupChildren.swift      — Sequence collection
│   ├── ChildIndexPath.swift      — Indexing primitives
│   ├── DirectiveArgument.swift
│   └── LiteralMarkup.swift       — Text/SoftBreak protocols
├── Block Nodes/                  — Heading, Paragraph, List, CodeBlock
├── Inline Nodes/                 — Text, Emphasis, Strong, Link, Code
├── Interpretive Nodes/           — AsideAutoTitle
├── Parser/                       — CommonMarkConverter + cmark-gfm integration
│   ├── CommonMarkConverter.swift
│   ├── BlockDirectiveParser.swift
│   ├── ParseOptions.swift
│   ├── RangeAdjuster.swift
│   └── RangerTracker.swift
├── Visitor/                      — MarkupVisitor protocol
├── Rewriter/                     — MarkupRewriter
├── Structural Restrictions/       — Protocol constraints (DSL)
└── Infrastructure/               — SourceLocation, Replacement
```

### Public API Surface (from `^public` grep)

```swift
// Core protocol
public protocol Markup
public struct Document: Markup, BasicBlockContainer
public struct _MarkupData  // private backing

// Containers
public struct MarkupChildren: Sequence
public struct ReversedMarkupChildren: Sequence
public struct TypedChildIndexPath: RandomAccessCollection, ExpressibleByArrayLiteral, Sendable

// Restrictions (protocol constraints)
public protocol BlockMarkup
public protocol InlineMarkup
public protocol BlockContainer: BlockMarkup
public protocol BasicBlockContainer: BlockContainer
public protocol ListItemContainer: BlockContainer
public protocol InlineContainer: InlineMarkup
public protocol BasicInlineContainer: InlineContainer
public protocol LiteralMarkup: Markup
public protocol BlockDirective: BlockMarkup

// Directives
public struct DirectiveArgument: Equatable, Sendable
public struct DirectiveArgumentText: Equatable, Sendable

// Visitor
public protocol MarkupVisitor

// Rewriter
public protocol MarkupRewriter
public struct MarkupRewriterImpl  // implementation
```

### Package.swift (highlights)

```swift
let package = Package(
    name: "swift-markdown",
    products: [
        .library(name: "Markdown", targets: ["Markdown"]),
    ],
    targets: [
        .target(
            name: "Markdown",
            dependencies: [
                "CAtomic",
                .product(name: "cmark-gfm", package: cmarkPackageName),
                .product(name: "cmark-gfm-extensions", package: cmarkPackageName),
                ...
            ]
        ),
    ]
)
```

**核心依赖**: `swift-cmark`(GitHub-flavored Markdown C 实现)+ `cmark-gfm-extensions`(tables / strikethrough / task list 等 GFM 扩展)。

## Why This Is a Key Reference

Swift Markdown 的设计模式(持久化 CoW markup tree + protocol-oriented + visitor)是 **Apple 文本处理库的"标准模式"**。同一模式也用在:

- **[SwiftSyntax](https://github.com/swiftlang/swift-syntax)** — Swift 编译器解析
- **[swift-syntax](https://github.com/swiftlang/swift-format)** — Swift formatter
- **MarkdownView / RichText** — LiYanan 实现的第三方 Markdown 渲染

## Use in Vault

- [[entities/swift-markdown]] — Entity 视角
- [[concepts/persistent-copy-on-write-markup-tree]] — 数据结构模式
- [[references/fatbobman-swiftui-rich-text-layout]] — MarkdownView 实战使用
- [[synthesis/Research: SwiftUI 图文混排]] — vault 既有研究

## Verification

- Cloned: `git clone --depth 1 https://github.com/swiftlang/swift-markdown.git /tmp/swift-markdown-clone`
- 70 swift files, 9004 LOC verified by `find Sources -name "*.swift" -exec wc -l`
- License verified from `LICENSE.txt` (Apache 2.0)
- swift-tools-version from `Package.swift` first line (`// swift-tools-version:6.2`)
- Architecture map verified by reading `ls Sources/Markdown/` and grep `^public`

## Related

- [[entities/markdownview]] — MarkdownView (LiYanan) 是 swift-markdown 在 SwiftUI 渲染层的 production 用户
