---
title: UIKit NSTextAttachment 没有 AppKit 风格的 imageBounds override
created: 2026-09-02
updated: 2026-09-02
tags: [uikit, appkit, nstextattachment, ios]
summary: AppKit 的 NSTextAttachment 有 imageBounds(for: ContentModeType: containerSize: imageSize:) 参数化 override；iOS UIKit 的 NSTextAttachment 没有该入口，渲染走 imageForBounds:textContainer:characterIndex:，imageBounds 默认 = attachmentBounds。
base_confidence: 0.9
provenance:
  extracted: 0.9
  inferred: 0.1
lifecycle: draft
lifecycle_changed: 2026-09-02
sources:
  - dayfold session (2026-09-02)
---

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

UIKit 只有这一个 attachment 渲染入口。image 被绘制到 imageBounds，imageBounds 默认 = attachmentBounds。

## 实测错误尝试

尝试加 `override func imageBounds(for contentMode: NSTextAttachment.ContentModeType, ...)` 时编译报错：

```
error: 'ContentModeType' is not a member type of class 'UIKit.NSTextAttachment'
error: method does not override any method from its superclass
```

`NSTextAttachment.ContentModeType` 是 AppKit 的类型，UIKit 没有等价的 enum。

## iOS 现代替代 API（iOS 15+）

Apple 文档推荐用 `NSTextAttachmentLayout` 协议族（`attachmentBounds(for:location:textContainer:proposedLineFragment:position:)` + `image(for:attributes:location:textContainer:)` + `viewProvider(for:location:textContainer:)`）做自定义 attachment layout。**iOS 15+ 才可用**。

## 工程含义

如果遇到 attachment 渲染尺寸与预期不符（拉伸 / 错位 / 撑爆），**唯一可控的杠杆是 `attachmentBounds`**——返回什么尺寸，UIKit 就把 image 绘制到那个尺寸。**不要去搜 `imageBounds(for: ContentModeType: ...)` 这个 override，那不存在于 iOS**。

## Related

- [[nstextattachment-bounds-overflow]] — 同一个 session 触发：bounds overflow 导致 attachment 被纵向拉伸的修复路径
