---
title: 自适应撑高 UITextEditor 与外层 ScrollView 复合滚动
category: project
tags: [mobile, swiftui, uikit, scrollview, texteditor, app-architecture]
relationships:
  - target: "[[projects/dayfold/skills/dayone-photo-library-picker]]"
    type: related_to
  - target: "[[projects/dayfold/concepts/architecture-overview]]"
    type: uses
  - target: "[[projects/dayfold/skills/uitextview-intrinsic-width-overflow]]"
    type: derived_from
sources: [projects/dayfold]
summary: >-
  长文本输入 + 大图共存于同一滚动容器：UITextView 关闭自身滚动按
  sizeThatFits 回报实高，外层 ScrollView 统一滚动，配合键盘自适应与
  交互式收键盘。阶段 H 后图片改为内联附件，ScrollViewReader 已移除。
provenance:
  extracted: 0.85
  inferred: 0.13
  ambiguous: 0.02
base_confidence: 0.88
lifecycle: reviewed
lifecycle_changed: 2026-09-02
---

# 自适应撑高 UITextEditor 与外层 ScrollView 复合滚动

> [!warning] 阶段 H 已修正三处
> 本页原记录的是阶段 G 架构。阶段 H 图文混排改造后：
> 1. **独立 `imageFlow` 大图流已移除** — 图片改为内联 `NSTextAttachment`，文字可在图片前后自由穿插（见 [[projects/dayfold/skills/uitextview-intrinsic-width-overflow]]）
> 2. **`ScrollViewReader` + `scrollTo("editorAnchor")` 已移除** — 图文混排下每插一张图都触发 textHeight 增大，滚到底会把标题与已插入的历史图片推出屏幕顶部
> 3. **最小高度 320 → 120** — 320pt 会在短正文下留出大片空白
>
> 下方「架构与实现」第 2、3 节与「关键代码」段落保留作为演进记录，**不代表当前实现**。

## Context
日记编辑器需要同时容纳：多行标题、长正文（UITextView 封装，支持选区格式化）、标签 chip 行、以及纵向全宽大图流。若 UITextView 保持自身滚动（`isScrollEnabled = true`），图片流只能放在滚动容器之外，超过 1–2 张大图必然溢出屏幕且无法滚动查看；若简单把 UITextView 塞进外层 ScrollView，两套滚动手势互相冲突、光标容易被键盘遮挡。

## Architecture & Implementation

### 1. 关闭内层滚动，高度回报驱动外层布局
- `SelectableTextEditor`（UIViewRepresentable 封装的 UITextView）增加 `isScrollEnabled: Bool = true` 开关与 `onHeightChange: ((CGFloat) -> Void)?` 回调。
- 编辑场景传 `isScrollEnabled: false`，在 `textViewDidChange` 与 `updateUIView` 后用 `sizeThatFits(CGSize(width: 实宽, height: .greatestFiniteMagnitude))` 计算内容实高并回报。
- View 层持有 `@State textHeight`，以外层 `.frame(height: max(320, textHeight))` 约束编辑器——320pt 是最小可视高度，内容增长时 UITextView 随外层 VStack 一起被撑高。

### 2. 外层 ScrollView 统一承载
- 结构：`ScrollView { VStack(spacing: 0) { 标题 TextField; SelectableTextEditor; 标签行; imageFlow 大图流; 底部占位 } }`。
- 图片流 `imageFlow` 为 `VStack(spacing: 16)`，每张 `Image.resizable().aspectRatio(原图宽高比, .fit).frame(maxWidth: .infinity)`，随正文一起滚动，无独立滚动区。
- `.scrollDismissesKeyboard(.interactively)` 保证下滑手势可收键盘。

### 3. 光标可见性保护
- 编辑器容器挂 `.id("editorAnchor")`，用 `ScrollViewReader` 包裹。
- 监听 `textHeight` 的 `onChange`：**仅当新值大于旧值**（正文长高、新增行）时 `proxy.scrollTo("editorAnchor", anchor: .bottom)`，把编辑器底部（即行尾光标处）滚入视口；变矮（删行）不滚动，避免视图跳动。

### 4. 键盘联动
- 自定义 `.keyboardAdaptive()` modifier：监听 `keyboardWillChangeFrameNotification` / `keyboardWillHideNotification`，以 `max(0, 屏高 - frame.minY)` 计算底部 padding 并 0.25s easeOut 动画，浮动工具栏随键盘移动。
- 工具栏用 `ZStack(alignment: .bottom)` 叠加在内容之上并 `.ignoresSafeArea(.keyboard, edges: .bottom)`，与键盘 padding 配合避免双重偏移。

### 5. 逃生舱预案（方案 B）
若光标/键盘联动出现无法快速修复的回归，可整体回退为：外层结构不动，`imageFlow` 放进固定高度（≤ 屏高 45%）的内滚子区。该预案在阶段 G 未触发，但作为可整体 revert 的降级路径保留在设计记录中。

## Key Code Reference

```swift
// EntryEditorView.swift - 编辑区
ScrollViewReader { proxy in
    ScrollView(showsIndicators: false) {
        VStack(alignment: .leading, spacing: 0) {
            TextField("标题", text: $viewModel.title, axis: .vertical) // ...
            SelectableTextEditor(
                text: $viewModel.content,
                onSelectionChange: { len in selectionLength = len },
                isScrollEnabled: false,
                onHeightChange: { textHeight = $0 }
            )
            .frame(height: max(320, textHeight))
            .id("editorAnchor")
            // 标签行 + imageFlow + 底部占位 ...
        }
    }
    .scrollDismissesKeyboard(.interactively)
    .onChange(of: textHeight) { oldValue, newValue in
        if newValue > oldValue {
            withAnimation { proxy.scrollTo("editorAnchor", anchor: .bottom) }
        }
    }
}
```

## Related
- [[synthesis/Research: SwiftUI 图文混排]] — synthesis
- [[projects/dayfold/skills/uitextview-intrinsic-width-overflow]] — 阶段 H 图文混排改造与本页三处修正的来源
- [[projects/dayfold/skills/dayone-photo-library-picker]] — 配套的照片多选与大图流来源
- [[projects/dayfold/skills/entry-editor-image-dirty-tracking]] — 编辑器图片脏标记保存机制
- [[projects/dayfold/concepts/architecture-overview]] — Dayfold 架构概览
