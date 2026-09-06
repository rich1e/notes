---
title: 非滚动 UITextView 的 intrinsic 宽度反向撑宽 SwiftUI 层级
category: project
tags: [mobile, swiftui, Bugfix, xcode, app-architecture]
relationships:
  - target: "[[projects/dayfold/skills/auto-expanding-texteditor-scroll]]"
    type: extends
  - target: "[[projects/dayfold/skills/entry-editor-image-dirty-tracking]]"
    type: related_to
  - target: "[[projects/dayfold/concepts/architecture-overview]]"
    type: uses
sources: [projects/dayfold]
summary: >-
  isScrollEnabled=false 的 UITextView 会把被超宽 NSTextAttachment 撑大的
  contentSize.width 报成 intrinsicContentSize.width，SwiftUI 父容器采纳后
  整个界面横向溢出；修复须 override intrinsicContentSize 锁死横向。
provenance:
  extracted: 0.82
  inferred: 0.16
  ambiguous: 0.02
base_confidence: 0.9
lifecycle: reviewed
lifecycle_changed: 2026-09-02
created: 2026-09-02T14:30:00Z
updated: 2026-09-02T14:30:00Z
---

# 非滚动 UITextView 的 intrinsic 宽度反向撑宽 SwiftUI 层级

## Context

图文混排编辑器把图片作为 `NSTextAttachment` 内联进 `UITextView`（`isScrollEnabled = false`，靠 `sizeThatFits` 回报高度给外层 SwiftUI `ScrollView`）。重开带图日记进入编辑时，顶部日期、标题、右上「完毕」按钮被推出屏幕两侧——表面看像"内容显示不完整"，实为**整个视图层级被横向撑宽**。

同一根因在插图场景下表现为另一副面孔：图片撑爆整屏、且每次 layout 逐次变大。二者是同一 bug 的两种外观。^[inferred]

## Finding

**非滚动 UITextView 会把被超宽内容撑大的 `contentSize.width` 当作 `intrinsicContentSize.width` 汇报给 SwiftUI**，父 `VStack` 采纳该 intrinsic 宽度后整个层级横向溢出。

运行时实测（iPhone 16 Pro，正确宽度应为 402pt）：

```
第1次 layoutSubviews: bounds=402.0  container=370.0  intrinsic=32.0   ← 图片未加载
第2次 layoutSubviews: bounds=454.7  container=422.7  intrinsic=454.7  ← 被撑宽 52.7pt
```

`intrinsic` 从 32 跃升至 454.7 且与 `contentSize` 完全同步，即为撑宽的传导路径。

### 修复

override `intrinsicContentSize`，横向返回 `noIntrinsicMetric`，只让高度参与自适应：

```swift
final class EditorTextView: UITextView {
    override var intrinsicContentSize: CGSize {
        let sup = super.intrinsicContentSize
        return CGSize(width: UIView.noIntrinsicMetric, height: sup.height)
    }
}
```

## Reasoning

关键在于**撑宽发生在下游的「尺寸汇报」环节，而非上游的「图片尺寸计算」环节**。

该 bug 前后返工 5 轮，前 4 轮全部在改「喂给 attachment 的宽度」（改高度上限、改 `image(forBounds:)` 现绘、改宽度来源），方向都在上游，因此全部无效。只有拦住 UITextView 向 SwiftUI 汇报宽度这一步才真正止住。^[inferred]

### 三条连带约束

1. **绝不回读 `textContainer.size.width` 来算 attachment 宽度。** 非滚动 UITextView 的 textContainer 会被超宽 attachment 反向撑宽，回读到的是「已被上一次超宽图污染」的值，拿去渲染下一张图 → 宽度每次 layout 递增。只能用 `bounds.width` 减去**自己设定的** `textContainerInset` 与 `lineFragmentPadding`。

2. **宽度未就绪时不要用 `UIScreen.main.bounds.width` 兜底。** `updateUIView` 早于 `layoutSubviews`，此时 `bounds.width == 0`；用假宽度会按错误尺寸预渲染图片，并把宽度缓存判据写成假值，导致真实宽度到位时反被判定为「无需重建」。正确做法是直接跳过，`layoutSubviews` 必然带真实宽度回来触发。

3. **竖图高度上限不能用容器宽度。** 原实现 `if height > safeWidth { height = safeWidth }` 拿宽度当高度上限，实测把 1668×2500 的竖图压成 282×422 严重变形。应改为宽度的 1.6 倍等合理倍数。

## Implications

- 任何 `UIViewRepresentable` 包裹的自适应高度 UIKit 视图，只要内容可能超宽（内联附件、长英文单词、宽表格），都应显式锁死横向 intrinsic。^[inferred]
- `NSTextAttachment` 的正确渲染路径是**构造期预渲染到 `self.image`**：UIKit 优先用 `self.image`（带解码缓存），`image(forBounds:)` 仅在其为 nil 时作为 fallback 调用，且在其中现绘 4032×3024 原图会产生约 30MB 中间位图触发内存压力而静默失败。
- 已确认不引入第三方富文本库：`swift-markdown-ui` / `MarkdownView` 仅只读渲染；`RichTextKit` 底层同为 NSTextAttachment 且有 Backspace 删图已知 bug、作者考虑停止维护。

## Related

- [[synthesis/Research: SwiftUI 图文混排]] — synthesis
- [[projects/dayfold/skills/auto-expanding-texteditor-scroll]] — 本页所修正的复合滚动架构（阶段 H 后 `imageFlow` 与 ScrollViewReader 均已移除）
- [[projects/dayfold/skills/entry-editor-image-dirty-tracking]] — 编辑器图片脏标记与持久化
- [[projects/dayfold/skills/dayone-photo-library-picker]] — 图片来源的多选选图器
- [[projects/dayfold/concepts/architecture-overview]] — Dayfold 架构概览
- [[projects/dayfold/skills/simulator-runtime-log-capture]] — 定位本 bug 所用的运行时日志抓取方法
