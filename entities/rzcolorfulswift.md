---
title: RZColorfulSwift (rztime)
category: entities
tags:
  - swift
  - ios
  - attributed-string
  - rich-text
  - markdown
  - html
  - rztime
  - iOS-11
  - library
  - entity
sources:
  - https://github.com/rztime/RZColorfulSwift
  - https://github.com/rztime/RZColorful
  - https://github.com/rztime/RZRichTextView
source_url: https://github.com/rztime/RZColorfulSwift
created: 2026-09-03T05:20:00Z
updated: 2026-09-03T05:20:00Z
summary: rztime 的 iOS NSAttributedString 富文本工具库:链式 API + markdown→HTML + HTML↔NSAttributedString + UILabel/UITextView/UIButton 富文本。Swift 版本(iOS 11+) + 配套 ObjC RZColorful + RZRichTextView 富文本编辑器。
provenance:
  extracted: 0.88
  inferred: 0.08
  ambiguous: 0.04
base_confidence: 0.78
lifecycle: draft
lifecycle_changed: 2026-09-03
tier: supporting
---

# RZColorfulSwift (rztime)

## Source

- **GitHub**: <https://github.com/rztime/RZColorfulSwift>
- **作者**: rztime (QQ群 580839749, vip.qq.com)
- License: MIT
- Platform: **iOS 11+**(较低,但 iOS 11 早已 EOL)
- Repo: 19 Swift files / 2,723 LOC
- swift-tools-version: 6.0 (但支持 Swift 4.2 / 5.0 backward)

## 项目家族 (rztime 3 个相关 repo)

| Repo | Language | 用途 |
|---|---|---|
| **[RZColorful](https://github.com/rztime/RZColorful)** | ObjC | 原始版本, iOS 通用 |
| **RZColorfulSwift** (本文) | Swift | iOS Swift 适配,链式 API |
| **[RZRichTextView](https://github.com/rztime/RZRichTextView)** | Swift | 基于 UITextView 的富文本编辑器(README 提及) |

## Core Features (from README)

> iOS NSAttributedString 富文本方法(图文混排、多样式文本);文本超行,可自动添加"折叠"、"全部";markdown 转 html;UILabel、UITextView的富文本支持添加自定义 view、显示 gif、给文本添加背景图、文本支持点击等功能

**2.0.0 版本后**:
- 富文本添加的**点击功能**更友好
- 富文本的**布局计算**更高效

**支持能力**:
- NSAttributedString 多样化设置(字体、颜色、阴影、段落样式、url、下划线)
- 图文混排(`NSTextAttachment` 集成)
- 显示 GIF
- 添加 backgroundView
- 文本点击交互
- 文本**自动折叠**/展开(超行时)
- Markdown → HTML 转换
- HTML ↔ NSAttributedString 互换
- UILabel / UITextView / UITextField 的 attributedText 一行设置

## Public API

```swift
// Core class
public class ColorfulConferrerRZ {
    // 链式属性设置
}

// Paragraph styles
public class RZMutableParagraphStyle: NSMutableParagraphStyle
public class ParagraphStyleRZ<T: AnyObject>

// Attributes
public class TextAttributeRZ: AttributeKeyRZ
public class ImageAttributeRZ: AttributeKeyRZ
public protocol AttributePackageRZ

// Layout
public class TextLayoutRZ
public class RZColorfulView: UIView
public protocol RZColorfulViewProtocol

// UI extensions (chainable attributedText setter)
public extension RZColorfulSwiftBase where T: UILabel
public extension RZColorfulSwiftBase where T: UIButton
public extension NSAttributedString.Key

// Shadow + position
public struct ShadowStyleRZ<T: AnyObject>
public enum ConferInsertPositionRZ: Int
public enum ImageAttachmentHorizontalAlignRZ
public struct EmptyImagePlaceholderRZ
```

## Architecture

```
RZColorfulSwift/
├── Classes/
│   ├── AttributeCore/    — Core attribute types
│   │   ├── TextAttributeRZ.swift     — 文本属性(字体、颜色、阴影、下划线)
│   │   ├── ImageAttributeRZ.swift     — 图片 attachment
│   │   ├── ParagraphStyleRZ.swift     — 段落样式
│   │   ├── AttributeKeyRZ.swift       — Attribute key protocol
│   │   ├── ShadowStyleRZ.swift        — 阴影样式
│   │   └── ColorfulConferrerRZ.swift  — 主 API(链式)
│   ├── Core/                — 核心 Views + extension
│   │   ├── TextLayoutRZ.swift
│   │   ├── NSAttributedStringRZ.swift
│   │   ├── LabelRZ.swift / ButtonRZ.swift / TextFieldRZ.swift / TextViewRZ.swift
│   │   ├── RZColorfulView.swift       — 自定义富文本 View
│   │   ├── RZColorfulViewProtocol.swift
│   │   └── RZColorfulSwiftBase.swift  — 链式基类
│   └── Html/                — HTML/Markdown 互转
│       ├── NSAttributedStringRZHtml.swift
│       ├── MarkdownRZ.swift
│       └── HtmlTransformRZ.swift
```

### Pipeline

```
Chain attribute setters (ColorfulConferrerRZ)
    ↓
Build NSAttributedString (链式 API 内部)
    ↓
Set on UIView.attributedText (UILabel/UITextView/UIButton)
    ↓
Or use RZColorfulView (自定义 UIView, 性能优化)
```

## Use Cases

适用:
- 需要**链式 API 设置 NSAttributedString** 而非手动一个个 attribute
- 文本过长需要**自动折叠/展开**
- 需要 **HTML 互转** NSAttributedString
- 需要 **markdown → NSAttributedString** 转换
- iOS 11+ 部署(虽然 iOS 11 已 EOL,但代码仍可用)

不适用:
- 新项目 iOS 16+(应该考虑 MarkdownView / Textual 等现代方案)
- SwiftUI-only 项目(本 lib 主要为 UIKit)
- 需要 iOS 14+ 持续维护的项目(本 lib 节奏不明确)

## 与 vault 既有研究的关系

### [[synthesis/Research: SwiftUI 图文混排]]

本 lib 是 **iOS 富文本的"中国本土传统方案"**(rztime 是国内 iOS 资深开发者),提供了**链式 API**和**HTML/Markdown 互转**能力。

| 维度 | vault Research | RZColorfulSwift |
|---|---|---|
| 平台 | UIKit (UIViewRepresentable) | UIKit native |
| API 风格 | 手工设置属性 | **链式 API** |
| 编辑支持 | ✅(via UITextView) | ⚠️(部分) |
| HTML 互转 | ❌ | ✅ |

### [[entities/markdownview]] / [[entities/markdownui]] / [[entities/textual]]

这3 个是 **render 层**,RZColorfulSwift 是 **attributedString 工具层** — 不同抽象层,可以共存(RZColorfulSwift 构建 attributedString,然后 MarkdownView 渲染)。

## Related

- [[synthesis/Research: SwiftUI 图文混排]] — vault 既有研究综述
- [[concepts/swiftui-rich-text-rendering-comparison]] — 全方案对比
- https://github.com/rztime/RZColorful — ObjC 原版
- https://github.com/rztime/RZRichTextView — 同作者富文本编辑器

## Verification

- Cloned: `git clone --depth 1 https://github.com/rztime/RZColorfulSwift.git /tmp/rzcolorful-clone`
- 19 Swift files / 2,723 LOC verified by `find Classes -name "*.swift" -exec wc -l`
- iOS 11+ platform verified from `Package.swift` platforms array
- swiftLanguageVersions verified: [.v4_2, .v5](支持旧 Swift 编译器)
- Public API surface captured via grep `^public`
- Related repos verified via README 引用 (RZColorful ObjC + RZRichTextView)