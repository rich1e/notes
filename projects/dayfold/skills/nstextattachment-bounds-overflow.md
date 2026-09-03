---
title: NSTextAttachment 在 UITextView 中被纵向拉伸的根因与修复
category: project
tags:
  - swiftui
  - uikit
  - nstextattachment
  - textkit
  - dayfold
relationships:
  - target: "[[projects/dayfold/skills/uitextview-intrinsic-width-overflow]]"
    type: related_to
  - target: "[[projects/dayfold/skills/auto-expanding-texteditor-scroll]]"
    type: related_to
  - target: "[[projects/dayfold/skills/swiftui-editor-scrollview-vs-attachment]]"
    type: related_to
  - target: "[[references/uikit-nstextattachment-vs-appkit]]"
    type: uses
  - target: "[[projects/dayfold/concepts/architecture-overview]]"
    type: uses
sources: [dayfold session (2026-09-02)]
summary: >-
  UITextView 嵌入 NSTextAttachment 显示横图时被纵向拉伸：attachment.bounds.width
  超过 textContainer.lineFragmentWidth 触发回行放大机制，layoutManager
  用被撑大的 textContainer 重算布局，渲染尺寸随之放大。修复须以
  textContainer.size.width 而非 bounds.width 算 attachment 目标尺寸。
provenance:
  extracted: 0.70
  inferred: 0.25
  ambiguous: 0.05
base_confidence: 0.78
lifecycle: draft
lifecycle_changed: 2026-09-02
created: 2026-09-02
updated: 2026-09-02
tier: supporting
---

# NSTextAttachment 在 UITextView 中被纵向拉伸的根因与修复

## Context

`UITextView` 内嵌 `NSTextAttachment` 显示横图（如 4032×3024）时，图片被渲染成 ≈393×710pt 的纵向拉伸版本，撑满 editorArea 全部可见空间，标题 TextField 被挤出屏幕。肉眼看到的是"图片被异常放大"，但根因出在**文本容器宽度计算**环节，不是图片本身。

这一根因与 [[projects/dayfold/skills/uitextview-intrinsic-width-overflow]] 描述的"同一 bug 另一种面孔"互补：那里修的是下游「尺寸汇报」环节，本页修的是上游「图片尺寸计算」环节。

## Finding

`NSTextAttachment.attachmentBounds(for:proposedLineFragment:...)` 接收的 `proposedLineFragment.width` 是 textContainer 的行宽。**当 `attachment.bounds.width > textContainer.lineFragmentWidth` 时**触发以下链式放大：

1. UIKit 把 attachment 拆到下一行，新行宽度自动扩到 `attachment.bounds.width`
2. textContainer 宽度被 attachment 撑大
3. layoutManager 用被撑大的 textContainer 重新计算整页布局
4. attachment 实际渲染高度被放大

实测预渲染 393×294 的图，渲染出 393×710——可见 layoutManager 用被撑大的行宽重算了 attachment 的显示高度。

### 触发阈值

原代码传 `containerWidth = bounds.width`（393pt）。`bounds.width` 含 `textContainerInset` 横向（16+16=32pt）。textContainer 实际可用宽度 = `bounds.width - inset - lineFragmentPadding*2` ≈ 361pt。**393 > 361 → 触发回行放大机制**。

## Fix

`SelectableTextEditor.rebuildAttributedTextIfNeeded` 把 attachment 的 `containerWidth` 从 `bounds.width` 改为 `textContainer.size.width`，首次 layout 前可能为 0，兜底用 `bounds.width - insetH - padding`：

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

然后传给 `RichTextMarkdownParser.attributedString(containerWidth:)`，attachment init 用 `effectiveWidth` 算 `displaySize`。**保证 `attachment.bounds.width ≤ textContainer.lineFragmentWidth` 即可避免回行放大**。

## 关键事实

iOS UIKit 的 `NSTextAttachment` **没有** `imageBounds(for: ContentModeType: containerSize: imageSize:)` 这个 override（那是 AppKit 的 API，详见 [[references/uikit-nstextattachment-vs-appkit]]）。UIKit 渲染 attachment 走 `imageForBounds:textContainer:characterIndex:`，image 绘制到 `imageBounds`，`imageBounds` 默认 = `attachmentBounds`。

**结论：无法通过 override 阻止拉伸，唯一可控杠杆是 `attachmentBounds` → 即正确计算 attachment 的目标尺寸 → 即把 containerWidth 修正到 textContainer 可用宽度**。^[inferred]

## 适用条件

任何 SwiftUI 编辑器内部是 UITextView + 内联 `NSTextAttachment` 的图文混排场景，喂给 attachment 的"可用宽度"必须用 `textContainer.size.width`（或 `bounds.width - inset - lineFragmentPadding*2`）而**不是** `bounds.width` 原始值。

## Verification

- 构建 `xcodebuild ... ** BUILD SUCCEEDED **`
- 用户在模拟器手动复测通过（feedback "通过验证，commit"）
- commit `2843f9c fix(editor): 用 textContainer 可用宽度算 attachment，避免图片撑爆`

## Related

- [[projects/dayfold/skills/uitextview-intrinsic-width-overflow]] — 同一根因的「下游尺寸汇报」修复
- [[projects/dayfold/skills/swiftui-editor-scrollview-vs-attachment]] — 同一 session 的姊妹 bug（外层滚动反行为）
- [[references/uikit-nstextattachment-vs-appkit]] — UIKit 与 AppKit 的 NSTextAttachment API 差异
- [[projects/dayfold/skills/auto-expanding-texteditor-scroll]] — 编辑器外层 ScrollView 复合滚动的整体架构