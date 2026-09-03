---
title: RZColorfulSwift Package — 链式 AttributedString 工具库
category: references
tags:
  - swift
  - ios
  - attributed-string
  - rich-text
  - rztime
  - swift-package
  - iOS-11
sources:
  - "[[entities/rzcolorfulswift]]"
created: 2026-09-03T05:20:00Z
updated: 2026-09-03T05:20:00Z
summary: rztime/RZColorfulSwift 仓库参考:MIT,iOS 11+,Swift 6.0 tools,19 Swift files / 2723 LOC,3 模块(属性核心 / 核心 View / HTML 互转),含 markdown→NSAttributedString + 链式 API。
provenance:
  extracted: 0.88
  inferred: 0.08
  ambiguous: 0.04
base_confidence: 0.78
lifecycle: draft
lifecycle_changed: 2026-09-03
tier: peripheral
---

# RZColorfulSwift Package — 链式 AttributedString 工具库

## Source

- **GitHub**: <https://github.com/rztime/RZColorfulSwift>
- **作者**: rztime (QQ群 580839749)
- License: MIT
- swift-tools-version: 6.0(但 swiftLanguageVersions 支持 4.2 / 5.0)

## Repo Stats (shallow clone)

- 19 Swift files (在 RZColorfulSwift/Classes/)
- 2,723 LOC

## Architecture

### Source Layout

```
RZColorfulSwift/
└── Classes/
    ├── AttributeCore/    — Core attribute types
    │   ├── TextAttributeRZ.swift         — 文本属性(字体、颜色、阴影、下划线)
    │   ├── ImageAttributeRZ.swift         — 图片 attachment
    │   ├── ParagraphStyleRZ.swift         — 段落样式
    │   ├── AttributeKeyRZ.swift           — Attribute key protocol
    │   ├── ShadowStyleRZ.swift            — 阴影样式
    │   └── ColorfulConferrerRZ.swift      — 主 API(链式)
    ├── Core/                — 核心 Views + extensions
    │   ├── TextLayoutRZ.swift             — 文本布局
    │   ├── NSAttributedStringRZ.swift
    │   ├── LabelRZ.swift / ButtonRZ.swift / TextFieldRZ.swift / TextViewRZ.swift
    │   ├── RZColorfulView.swift           — 自定义富文本 View
    │   ├── RZColorfulViewProtocol.swift
    │   └── RZColorfulSwiftBase.swift      — 链式基类
    └── Html/                — HTML/Markdown 互转
        ├── NSAttributedStringRZHtml.swift
        ├── MarkdownRZ.swift
        └── HtmlTransformRZ.swift
```

### Public API Surface

```swift
// Core class (链式 API 入口)
public class ColorfulConferrerRZ

// Paragraph styles
public class RZMutableParagraphStyle: NSMutableParagraphStyle
public class ParagraphStyleRZ<T: AnyObject>
public protocol AttributePackageRZ

// Attribute keys
public class TextAttributeRZ: AttributeKeyRZ
public class ImageAttributeRZ: AttributeKeyRZ
public class AttributeKeyRZ

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

## Platform Matrix

| 平台 | 最低 |
|---|---|
| iOS | **11.0** |

⚠️ 平台要求**很低**(iOS 11),但 iOS 11 已 EOL,实际部署应 ≥ iOS 14。

## 功能能力

| 能力 | 说明 |
|---|---|
| 链式 API | `colorfulConferrer().text(...).font(...).add(...)` |
| 图文混排 | NSTextAttachment 集成 |
| 自定义 view | 嵌入任意 UIView 到富文本 |
| GIF 显示 | NSTextAttachment + animatedImage |
| 背景图 | 文本区域背景图 |
| 文本点击 | 自定义点击回调 |
| 自动折叠 | 文本超行 → "全部"按钮 |
| Markdown → HTML | 文本转 HTML |
| HTML ↔ NSAttributedString | 双向转换 |
| UILabel/UITextView/UIButton | 一行 attributedText 设置 |

## Dependencies

无外部依赖(纯本地 Swift + UIKit)。

## Use in Vault

- [[entities/rzcolorfulswift]] — 实体视角
- [[synthesis/Research: SwiftUI 图文混排]] — vault 既有研究综述
- [[concepts/swiftui-rich-text-rendering-comparison]] — 全方案对比
- [[entities/markdownview]] / [[entities/markdownui]] / [[entities/textual]] — render 层

## Verification

- Cloned: `git clone --depth 1 https://github.com/rztime/RZColorfulSwift.git /tmp/rzcolorful-clone`
- 19 Swift files / 2,723 LOC verified by `find Classes -name "*.swift" -exec wc -l`
- swift-tools-version 6.0 verified from `Package.swift` first line
- iOS 11+ platform verified from `Package.swift` platforms array
- 3-module architecture (AttributeCore / Core / Html) verified by `ls RZColorfulSwift/Classes/`
- Public API surface captured via grep `^public`