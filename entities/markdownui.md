---
title: MarkdownUI (gonzalezreal/swift-markdown-ui)
category: entities
tags:
  - swiftui
  - markdown
  - rendering
  - theme
  - gonzalezreal
  - maintenance-mode
  - iOS-15
  - library
  - entity
sources:
  - https://github.com/gonzalezreal/swift-markdown-ui
  - https://github.com/gonzalezreal/textual
  - https://github.com/gonzalezreal/swift-markdown-ui/discussions/437
source_url: https://github.com/gonzalezreal/swift-markdown-ui
created: 2026-09-03T04:50:00Z
updated: 2026-09-03T04:50:00Z
summary: gonzalezreal (Guille Gonzalez)开源 SwiftUI native Markdown 渲染库,基于 cmark-gfm,支持 GFM spec、Theme 系统、ImageProvider 扩展。iOS 15+ / macOS 12+。**已宣布 maintenance mode,新开发转向 Textual**。
provenance:
  extracted: 0.90
  inferred: 0.08
  ambiguous: 0.02
base_confidence: 0.88
lifecycle: draft
lifecycle_changed: 2026-09-03
tier: supporting
---

# MarkdownUI (gonzalezreal/swift-markdown-ui)

## Source

- **GitHub**: <https://github.com/gonzalezreal/swift-markdown-ui>
- 作者: Guille Gonzalez (@gonzalezreal)
- License: MIT
- Repo: 7,669 Swift LOC,Swift tools 5.6
- 平台:macOS 12+ / iOS 15+ / tvOS 15+ / macCatalyst 15+ / watchOS 8+
- 高级特性: macOS 13+ / iOS 16+ / tvOS 16+ / watchOS 9+(tables + multi-image paragraphs)

## ⚠️ Maintenance Mode

README 顶部明确公告 **MarkdownUI is in maintenance mode**:
- 新开发转移到 [Textual](https://github.com/gonzalezreal/textual)— 同一作者的 SwiftUI-native text rendering engine
- Textual 继承 MarkdownUI 的思想和经验
- 公告讨论: <https://github.com/gonzalezreal/swift-markdown-ui/discussions/437>

**对 vault 的影响**:此 lib 仍是 iOS 15+ 上 SwiftUI markdown 渲染的最成熟方案,但**不要**选它做长期新项目。

## Core API

### Public `Markdown` View

```swift
import MarkdownUI

let markdownString = """
  ## Try MarkdownUI

  **MarkdownUI** is a native Markdown renderer for SwiftUI
  compatible with the [GitHub Flavored Markdown Spec](https://github.github.com/gfm/).
  """

var body: some View {
  Markdown(markdownString)
}
```

### Theme System

```swift
Markdown(markdownString)
    .markdownTheme(.gitHub)
    .markdownTheme(.docC)
    .markdownTextStyle(\.code) {  // custom TextStyle
        FontFamily(.monospaced)
        BackgroundColor(.gray.opacity(0.1))
    }
```

**Theme 抽象**:
- `protocol TextStyle` — font/color/background 的可组合单元
- `struct Theme: Sendable` — 完整主题(bundled: `.basic` / `.gitHub` / `.docC`)
- 用户可 override specific styles 或 create entire theme

### ImageProvider 扩展点

`protocol InlineImageProvider` 让你**自定义** image 加载:
- `AssetInlineImageProvider` — SwiftUI Asset catalog
- `DefaultInlineImageProvider` — URL + NetworkImage
- 用户可实现自定义(e.g. 从 Core Data / 数据库加载)

## Architecture

### 目录结构

```
Sources/MarkdownUI/
├── Views/                — `Markdown` SwiftUI View + 块渲染
│   ├── Markdown.swift
│   └── Blocks/           — Heading/Paragraph/CodeBlock/Table 等
├── Parser/               — Markdown → Node tree
│   ├── MarkdownParser.swift
│   ├── BlockNode.swift / InlineNode.swift
│   └── HTMLTag.swift
├── Renderer/             — Node → SwiftUI View
│   ├── AttributedStringInlineRenderer.swift
│   └── TextInlineRenderer.swift
├── Theme/                — Theme system
│   ├── Theme.swift       — Built-in themes
│   ├── TextStyle/        — Text style protocol + 13 个内置 styles
│   └── BlockStyle/       — Table border, task list marker 等
├── DSL/                  — 内部 DSL(MarkdownContent protocol)
│   └── Blocks/
└── Extensibility/        — Plugin points
    ├── ImageProvider.swift / AssetImageProvider.swift
    ├── InlineImageProvider.swift
    └── CodeSyntaxHighlighter.swift
```

### Pipeline

```
Markdown String
    ↓ MarkdownParser
Node Tree (BlockNode + InlineNode)
    ↓ Renderer
SwiftUI View Tree (Text + Layout)
```

### Dependencies

- `swift-cmark` (Apple official, GitHub-flavored Markdown C 解析)
- `NetworkImage` (作者自己的 [gonzalezreal/NetworkImage](https://github.com/gonzalezreal/NetworkImage) — 类似 AsyncImage)
- `swift-snapshot-testing` (仅测试)

## 与 vault 既有研究的关系

### [[synthesis/Research: SwiftUI 图文混排]]

之前 vault Research 文档说:
- "MarkdownUI (gonzalezreal) — 自定义 CommonMark 解析 + SwiftUI native views,但无 edit"
- "MarkdownUI 是否放弃维护"作为 Open Question

**本次 ingest 解决 Open Question**:MarkdownUI **已正式宣布 maintenance mode** — 新开发转向 Textual。

### [[concepts/swiftui-rich-text-rendering-comparison]]

MarkdownUI 在 read-only markdown 渲染方案中位置:
| 方案 | SwiftUI native | Edit | Performance | Status |
|---|---|---|---|---|
| **MarkdownUI** | ✅ | ❌ | 快 | ⚠️ **maintenance** |
| Textual (继任) | ✅ | ❌ | 快 | ✅ active dev |
| Down (cmark) | ❌ UIKit | ❌ | 极快 | active |
| Markdownosaur | ❌ UIKit | ❌ | 快 | active |
| AttributedString(markdown:) (Apple) | ✅ | ❌ | 快 | 弱(无图/代码块) |

### [[entities/swift-markdown]]

- Apple 官方 `swiftlang/swift-markdown`:**解析器**(给上游 AST)
- MarkdownUI:`swift-markdown` 之上的 SwiftUI 渲染层

两者互补:MarkdownUI **使用** swift-cmark (Apple swift-markdown 也用 cmark-gfm),但产品形态不同(解析 vs 渲染)。

## Adoption & Use Cases

适用:
- iOS 15+ SwiftUI app 渲染文档 / README / 帮助页
- 需要成熟 Theme 系统
- 不需要 edit(只读)

不适用:
- 需要 edit 功能(→ UIViewRepresentable + UITextTextView,见 [[skills/uiviewrepresentable-uitextview-rich-text]])
- 新项目长期支持(→ 考虑 Textual 继任)
- 仅 macOS 11 或 iOS 14 部署(平台不支持)

## Related

- [[entities/textual]] — 精神继任者(同作者 gonzalezreal),iOS 18+ 项目推荐
- [[synthesis/Research: SwiftUI 图文混排]] — vault 既有研究综述
- [[concepts/swiftui-rich-text-rendering-comparison]] — 全方案对比(更新维护状态)
- [[references/fatbobman-swiftui-rich-text-layout]] — MarkdownView 实战(同类问题域)
- [[entities/swift-markdown]] — Apple 官方解析后端
- <https://github.com/gonzalezreal/textual> — MarkdownUI 继任者

## Verification

- Cloned: `git clone --depth 1 https://github.com/gonzalezreal/swift-markdown-ui.git /tmp/markdownui-clone`
- 7,669 Swift LOC verified by `find Sources -name "*.swift" -exec wc -l`
- swift-tools-version 5.6 verified from `Package.swift` first line
- Maintenance mode confirmed by README `[!NOTE]` blockquote at top
- Author confirmed as `@gonzalezreal` (Guille Gonzalez)
- Platform matrix verified from `Package.swift` platforms array
- Dependency list verified: `swift-cmark` + `NetworkImage` + `swift-snapshot-testing`