---
title: Apple Developer Documentation — NSTextAttachment / NSTextAttachmentLayout / NSTextAttachmentViewProvider
category: references
tags:
  - apple
  - swift
  - ios
  - uikit
  - nstextattachment
  - textkit
sources:
  - https://developer.apple.com/documentation/uikit/nstextattachment
  - https://developer.apple.com/documentation/uikit/nstextattachmentlayout
  - https://developer.apple.com/documentation/uikit/nstextattachmentviewprovider
source_url: https://developer.apple.com/documentation/uikit/nstextattachment
created: 2026-09-03T03:30:00Z
updated: 2026-09-03T03:30:00Z
summary: Apple 官方文档:NSTextAttachment 类 + iOS 15+ NSTextAttachmentLayout 协议 + view provider 容器。bounds/attachmentBounds/image 三件套。
provenance:
  extracted: 0.92
  inferred: 0.06
  ambiguous: 0.02
base_confidence: 0.85
lifecycle: draft
lifecycle_changed: 2026-09-03
tier: supporting
---

# Apple NSTextAttachment 三件套文档

## 来源

- `https://developer.apple.com/documentation/uikit/nstextattachment` — 类文档
- `https://developer.apple.com/documentation/uikit/nstextattachmentlayout` — iOS 15+ layout 协议
- `https://developer.apple.com/documentation/uikit/nstextattachmentviewprovider` — view provider 容器

## 覆盖范围

### NSTextAttachment (类)

继承自 `NSObject`,实现 `NSTextAttachmentContainer` (iOS 7+) + `NSTextAttachmentLayout` (iOS 15+)。提供三种 attachment 渲染入口:

1. `image: UIImage?` — 直接设置图片(渲染到 imageBounds)
2. `fileType: String?` + `data: Data?` — 从二进制构造(自动推断类型)
3. `imageForBounds:textContainer:characterIndex:` — 单 override 入口,返回要绘制的 image(可选);未设置 image 时,layout 时回调此方法,默认值是 `attachmentBounds`

imageBounds 默认等于 attachmentBounds(无任何 offset)。

### NSTextAttachmentLayout (iOS 15+ 协议)

三个 required 方法:
1. `attachmentBounds(for:location:textContainer:proposedLineFragment:position:)` → CGRect
2. `image(for:attributes:location:textContainer:)` → UIImage?
3. `viewProvider(for:location:textContainer:)` → NSTextAttachmentViewProvider?

### NSTextAttachmentViewProvider (iOS 15+)

容器类,关联 attachment + view。关键属性:
- `textAttachment`
- `textLayoutManager`
- `tracksTextAttachmentViewBounds` (Bool) — 控制 view bounds 是否跟 attachment bounds
- `view` / `loadView()`

## 关键发现

- **iOS 15 行为变更**:直接设置 `attachment.bounds` 在 iOS 15+ 变得**不可靠**。Apple 推动使用 `containerSize` + `baselineOffset` 或 override `textAttachmentBounds(...)`。
- **bounds / attachmentBounds 区别**: `bounds` 是 CGRect 的 setter;`attachmentBounds(for:...)` 是动态计算方法,layout engine 优先调用后者。

## 对 vault 中相关页的影响

- `[[projects/dayfold/skills/nstextattachment-bounds-overflow]]` — 在 iOS 15+ 设备上,即使 `bounds.width = textContainer.size.width - padding` 也可能不生效,需要切换到 `containerSize` 或 override `attachmentBounds(for:...)`
- `[[references/uikit-nstextattachment-vs-appkit]]` — iOS 15+ 的 `NSTextAttachmentLayout` 与 AppKit 的 `imageBounds(for:ContentModeType:containerSize:imageSize:)` **不是同一接口**,虽然意图相似

## Related

- [[projects/dayfold/skills/nstextattachment-bounds-overflow]]
- [[projects/dayfold/skills/uitextview-intrinsic-width-overflow]]
- [[references/uikit-nstextattachment-vs-appkit]]
- [[synthesis/Research: SwiftUI 图文混排]]