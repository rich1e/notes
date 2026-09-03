---
title: NSTextAttachment 在 UITextView 中被纵向拉伸的根因与修复
created: 2026-09-02
updated: 2026-09-02
tags: [swiftui, uikit, nstextattachment, textkit, dayfold]
summary: attachment.bounds.width 超过 textContainer.lineFragmentWidth 时 textContainer 被撑宽，渲染尺寸随之放大；用 textContainer.size.width 而非 bounds.width 算 attachment 即可避免。
base_confidence: 0.75
provenance:
  extracted: 0.7
  inferred: 0.3
lifecycle: draft
lifecycle_changed: 2026-09-02
sources:
  - dayfold session (2026-09-02)
---

## 现象

`UITextView` 内嵌 `NSTextAttachment` 显示横图（4032×3024），图片被渲染成 ≈393×710pt 的纵向拉伸版本，撑满 editorArea 全部可见空间，标题 TextField 被挤出屏幕。

## 根因

`NSTextAttachment.attachmentBounds(for:proposedLineFragment:...)` 接收的 `proposedLineFragment.width` 是 textContainer 的行宽。**当 attachment.bounds.width > textContainer.lineFragmentWidth 时**：

1. UIKit 把 attachment 拆到下一行，新行宽度自动扩到 attachment.bounds.width
2. textContainer 宽度被 attachment 撑大
3. layoutManager 用被撑大的 textContainer 重新计算整页布局
4. attachment 实际渲染高度被放大（实测 393×294 预渲染的图，渲染出 393×710）

我之前传给 attachment 的 `containerWidth = bounds.width`（393pt）。`bounds.width` 含 `textContainerInset` 横向（16+16=32pt）。textContainer 实际可用宽度 = bounds.width - inset - lineFragmentPadding*2 ≈ 361pt。**393 > 361 → 触发上述回行放大机制**。

## 修复

`SelectableTextEditor.rebuildAttributedTextIfNeeded` 把 attachment 的 `containerWidth` 从 `bounds.width` 改为 `textContainer.size.width`（首次 layout 前可能为 0，兜底用 `bounds.width - insetH - padding`）：

```swift
let insetH = textView.textContainerInset.left + textView.textContainerInset.right
let padding = textView.textContainer.lineFragmentPadding * 2
let containerAvailable = textView.textContainer.size.width
let effectiveWidth: CGFloat
if containerAvailable > 1 {
    effectiveWidth = containerAvailable
} else if width > insetH + padding {
    effectiveWidth = width - insetH - padding
} else {
    effectiveWidth = max(1, width - insetH - padding)
}
```

然后传给 `RichTextMarkdownParser.attributedString(containerWidth:)`，attachment init 用 effectiveWidth 算 displaySize。**attachment.bounds.width ≤ textContainer.lineFragmentWidth → 不触发回行放大**。

## 关键事实

iOS UIKit 的 `NSTextAttachment` **没有** `imageBounds(for: ContentModeType: containerSize: imageSize:)` 这个 override（那是 AppKit 的 API）。UIKit 渲染 attachment 走 `imageForBounds:textContainer:characterIndex:`，image 绘制到 imageBounds，imageBounds 默认 = attachmentBounds。

**结论：无法通过 override 阻止拉伸，唯一可控杠杆是 attachmentBounds → 即正确计算 attachment 的目标尺寸 → 即把 containerWidth 修正到 textContainer 可用宽度**。

## 验证

- 构建 `xcodebuild ... ** BUILD SUCCEEDED **`
- 用户在模拟器手动复测通过（feedback "通过验证，commit"）
- commit `2843f9c fix(editor): 用 textContainer 可用宽度算 attachment，避免图片撑爆`

## Related

- [[swiftui-editor-scrollview-vs-attachment]] — 同一 session 的姊妹 bug
- [[uikit-nstextattachment-imagebounds-api-gap]] — UIKit 与 AppKit 的 API 差异
