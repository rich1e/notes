---
title: Persistent Copy-on-Write Markup Tree
category: concepts
tags:
  - data-structure
  - value-type
  - persistent
  - copy-on-write
  - swift
  - markdown
  - ast
  - design-pattern
sources:
  - "[[entities/swift-markdown]]"
created: 2026-09-03T04:30:00Z
updated: 2026-09-03T04:30:00Z
summary: Apple swift-markdown 的核心数据结构模式:不可变 + persistent(copy-on-write value type)markup tree,只 copy 子结构中被修改的分支。Protocol-Oriented 表达节点类型约束,Visitor pattern 替代 tree walking。
provenance:
  extracted: 0.78
  inferred: 0.18
  ambiguous: 0.04
base_confidence: 0.85
lifecycle: draft
lifecycle_changed: 2026-09-03
tier: supporting
---

# Persistent Copy-on-Write Markup Tree

## Context

解析 Markdown / HTML / SwiftSyntax 后,会得到一个 **AST(抽象语法树)**。问题是:**怎么在 value-type 的 Swift 里高效地表示 + 修改 + 遍历一棵 AST**?

swift-markdown 选择:**Persistent Copy-on-Write Markup Tree**。这是和 SwiftSyntax 共享的设计哲学。

## Core Properties

### 1. Immutable + Persistent

- **Immutable**: 每个 node 创建后不能修改
- **Persistent**: 修改节点会**共享未修改的子树**,只 copy 被改动分支 → 像 Git / persistent data structure
- 好处:天然**线程安全**(无 race condition)、**structural sharing**(内存高效)

### 2. Copy-on-Write

- 内部 struct `_MarkupData` 持有实际数据,使用 Swift 标准库的 CoW 优化(Array/Dictionary 都已 CoW)
- 节点公开协议 `Markup`,但底层是 `Copy`-able value type

```swift
public protocol Markup {
    var children: MarkupChildren { get }
    func accept<V: MarkupVisitor>(_ visitor: V) -> V.Result
}
```

### 3. Protocol-Oriented 节点约束

不用 `enum Markup { case heading, paragraph, ... }`,而是 protocol:

```swift
public protocol BlockMarkup: Markup { }
public protocol InlineMarkup: Markup { }
public protocol BlockContainer: BlockMarkup { }
public protocol BasicBlockContainer: BlockContainer { }
public protocol ListItemContainer: BlockContainer { }
public protocol InlineContainer: InlineMarkup { }
public protocol BasicInlineContainer: InlineContainer { }
public protocol LiteralMarkup: Markup { }
public protocol BlockDirective: BlockMarkup { }
```

**每个 protocol 表达一个语义约束**,节点通过 conformance 表明自己"是/包含/字面量"。

优势:
- 静态检查节点是否可作为容器
- 文档化节点类型关系(替代 class hierarchy)
- 易扩展(新节点只需 conform 合适 protocols)

### 4. Visitor Pattern 替代 Tree Walking

不递归访问 children,而是 accept visitor:

```swift
public protocol MarkupVisitor {
    associatedtype Result
    func visitDocument(_ document: Document) -> Result
    func visitHeading(_ heading: Heading) -> Result
    func visitParagraph(_ paragraph: Paragraph) -> Result
    // ... 每个节点类型一个 visit 方法
}
```

优势:
- 分离"遍历逻辑"(visitor)和"数据结构"(tree)
- 序列化/分析/改写 各自独立 visitor
- 与 Swift 的 existential 类型结合 → 类型安全 dispatch

## 与替代方案对比

### Class-based AST(如 Java DOM)

- ❌ 共享可变状态 → 线程不安全
- ❌ 多版本管理需要 deep copy
- ✅ 简单直观

### Enum-based AST(如 Rust serde_json)

- ✅ Value type
- ❌ 节点类型 extension 难(每加一个 case 改所有 visitor)
- ✅ Pattern matching 友好

### Persistent CoW + Protocol(Apple 选择)

- ✅ 线程安全
- ✅ 多版本共存(常见编辑场景)
- ✅ Protocol extension 易扩展
- ⚠️ Swift 的 existential 类型限制(每次只能装一种类型)
- ⚠️ Visitor 需要为每个节点类型写 visit 方法(模板代码)

## 在 swift-markdown 中的具体实现

```swift
// Private backing struct with CoW semantics
public struct _MarkupData {
    var kind: Kind
    var parent: Markup?
    var range: SourceRange?
    var childData: ChildData
}

// Public protocol exposes only what's needed
public protocol Markup {
    var _data: _MarkupData { get }
    var children: MarkupChildren { get }
    func accept<V: MarkupVisitor>(_ visitor: V) -> V.Result
}

// Concrete node
public struct Document: Markup, BasicBlockContainer {
    public var _data: _MarkupData
    public init(parsing: String, options: ParseOptions = .default) { ... }
}
```

## 适用场景

适合:
- AST 经常需要"修改 → 比较 → 回滚"的(语法高亮、linter、formatter)
- 多线程共享同一份树(LSP server、多窗口编辑器)
- 节点类型相对稳定(不频繁加新节点)

不适合:
- 需要深度 pattern matching(用 enum-based AST 更合适)
- 节点类型经常扩展(visitor 模板代码爆炸)
- 极小树(overhead 大于收益)

## 启发

- **SwiftSyntax** (Apple 官方): 同样的模式 — 不可变 + CoW + protocol + visitor
- **swift-cmark / cmark-gfm**: C 库实现,但 Swift binding 暴露 immutable API
- **MarkdownView / RichText**: 都基于 swift-markdown,继承这套设计哲学

## Related

- [[entities/swift-markdown]] — Apple 官方实现
- [[references/fatbobman-swiftui-rich-text-layout]] — LiYanan 用 swift-markdown + 此模式
- [[synthesis/Research: SwiftUI 图文混排]] — 富文本编辑器的数据结构选择
- https://swiftlang.github.io/swift-markdown/documentation/markdown/ — API
- [SwiftSyntax](https://github.com/swiftlang/swift-syntax) — 同同设计哲学的姐妹项目

## Verification

- Source: Apple swift-markdown repo (cloned at /tmp/swift-markdown-clone)
- Architecture confirmed by `ls Sources/Markdown/` and grep `^public` in source files
- Pattern visible: private `_MarkupData` struct (CoW), public `Markup` protocol, structured restrictions as protocols
- Visitor pattern confirmed: `MarkupVisitor` protocol with one `visit*` method per node type