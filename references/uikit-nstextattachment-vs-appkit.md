---
title: UIKit 与 AppKit 的 NSTextAttachment API 差异
category: reference
tags:
  - uikit
  - appkit
  - nstextattachment
  - ios
  - macos
sources: [dayfold session (2026-09-02)]
summary: >-
  AppKit 的 NSTextAttachment 提供参数化 override imageBounds(for:
  ContentModeType: containerSize: imageSize:)，可在 attachment 渲染时根据
  container 尺寸重算 image 绘制框；iOS UIKit 的 NSTextAttachment 没有该入口，
  渲染走 imageForBounds:textContainer:characterIndex:，imageBounds 默认 =
  attachmentBounds。iOS 15+ 提供 NSTextAttachmentLayout 协议族作为现代替代。
provenance:
  extracted: 0.90
  inferred: 0.08
  ambiguous: 0.02
base_confidence: 0.92
lifecycle: draft
lifecycle_changed: 2026-09-02
created: 2026-09-02
updated: 2026-09-02
tier: supporting
---

# UIKit 与 AppKit 的 NSTextAttachment API 差异

## Context

调试跨平台富文本渲染代码（macOS AppKit + iOS UIKit 共用一套 `NSTextAttachment` 子类）时容易踩一个坑：把 macOS 上跑通的 `imageBounds(for: ContentModeType: containerSize: imageSize:)` override 搬到 iOS 项目，编译报错。换言之**该 API 仅存在于 AppKit**，UIKit 没有等价入口。

## 关键事实

iOS UIKit 的 `NSTextAttachment` **没有** `imageBounds(for: ContentModeType: containerSize: imageSize:)` 这个参数化 override。**该 API 仅存在于 AppKit**。

证据来源：`Xcode.app/Contents/Developer/Platforms/iPhoneSimulator.platform/Developer/SDKs/iPhoneSimulator.sdk/System/Library/Frameworks/UIKit.framework/Headers/NSTextAttachment.h`：

```objc
- (nullable UIImage *)imageForBounds:(CGRect)imageBounds
                       textContainer:(nullable NSTextContainer *)textContainer
                       characterIndex:(NSUInteger)charIndex
    API_AVAILABLE(macos(10.11), ios(7.0), tvos(9.0), visionos(1.0))
    API_UNAVAILABLE(watchos);
```

UIKit 只有这一个 attachment 渲染入口。image 被绘制到 `imageBounds`，`imageBounds` 默认 = `attachmentBounds`。

## 实测错误尝试

尝试加 `override func imageBounds(for contentMode: NSTextAttachment.ContentModeType, ...)` 时编译报错：

```
error: 'ContentModeType' is not a member type of class 'UIKit.NSTextAttachment'
error: method does not override any method from its superclass
```

`NSTextAttachment.ContentModeType` 是 AppKit 的类型，UIKit 没有等价的 enum。

## iOS 现代替代 API（iOS 15+）

Apple 文档推荐用 `NSTextAttachmentLayout` 协议族做自定义 attachment layout：

- `attachmentBounds(for:location:textContainer:proposedLineFragment:position:)` — 自定义 attachment 占位框
- `image(for:attributes:location:textContainer:)` — 自定义渲染图片
- `viewProvider(for:location:textContainer:)` — 用 UIView 替代图片渲染（支持交互）

通过 `NSTextAttachment.textAttachmentView` 或实现协议接入。这套 API **iOS 15+ 才可用**，且行为模型与 AppKit `imageBounds(for:...)` 并不一一对应。

## 工程含义

如果遇到 attachment 渲染尺寸与预期不符（拉伸 / 错位 / 撑爆），**唯一可控的杠杆是 `attachmentBounds`**——返回什么尺寸，UIKit 就把 image 绘制到那个尺寸。

不要去搜 `imageBounds(for: ContentModeType: ...)` 这个 override，那不存在于 iOS。在 iOS 上做尺寸控制只能：
1. 精确计算 attachment 的目标尺寸（正确扣除 `textContainerInset` 与 `lineFragmentPadding`），见 [[projects/dayfold/skills/nstextattachment-bounds-overflow]]
2. 或升级到 iOS 15+ 并实现 `NSTextAttachmentLayout` 协议

## Verification

- 在 UIKit 项目中尝试 override `imageBounds(for: ContentModeType:)` → 编译报错，确认 API 不存在
- 在 AppKit 项目中 override `imageBounds(for: ContentModeType: containerSize: imageSize:)` → 编译通过且运行时按容器尺寸渲染

## Related

- [[projects/dayfold/skills/nstextattachment-bounds-overflow]] — 同 session 触发的 bounds 计算修复
- [[projects/dayfold/skills/uitextview-intrinsic-width-overflow]] — 同一根因的「下游尺寸汇报」修复
- [[projects/dayfold/skills/swiftui-editor-scrollview-vs-attachment]] — 同一 session 的外层滚动反行为