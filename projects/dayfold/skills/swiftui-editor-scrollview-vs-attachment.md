---
title: 图文混排下外层 ScrollViewReader.scrollTo 的反行为
category: project
tags:
  - swiftui
  - textkit
  - nstextattachment
  - dayfold
relationships:
  - target: "[[projects/dayfold/skills/auto-expanding-texteditor-scroll]]"
    type: extends
  - target: "[[projects/dayfold/skills/uitextview-intrinsic-width-overflow]]"
    type: related_to
  - target: "[[projects/dayfold/skills/nstextattachment-bounds-overflow]]"
    type: related_to
  - target: "[[projects/dayfold/concepts/architecture-overview]]"
    type: uses
sources: [dayfold session (2026-09-02)]
summary: >-
  图文混排下每次插入图片都触发 textHeight 增大，onChange + scrollTo("editorAnchor",
  anchor: .bottom) 把 ScrollView 内 VStack 的所有元素（标题 TextField、历史图片、
  历史文本）一并推出屏幕顶部。改为由内层 UITextView 自管 caret 可见性即可。
provenance:
  extracted: 0.80
  inferred: 0.18
  ambiguous: 0.02
base_confidence: 0.75
lifecycle: draft
lifecycle_changed: 2026-09-02
created: 2026-09-02
updated: 2026-09-02
tier: supporting
---

# 图文混排下外层 ScrollViewReader.scrollTo 的反行为

## Context

`EntryEditorView` 用如下结构：

```swift
ScrollViewReader { proxy in
    ScrollView {
        VStack {
            TextField("标题", ...)
            SelectableTextEditor
                .frame(height: max(120, textHeight))
                .id("editorAnchor")
            tags
            Spacer
        }
    }
    .onChange(of: textHeight) { _, new in
        if new > oldValue {
            withAnimation { proxy.scrollTo("editorAnchor", anchor: .bottom) }
        }
    }
}
```

意图是「正文长高（新增行/插图）时滚到正文底保证光标可见」——这是**纯文本编辑场景的合理优化**。

## 反行为

**图文混排下产生反行为**：用户在已有图片的笔记里再插入一张图 → textHeight 增大 → `scrollTo("editorAnchor", anchor: .bottom)` 被触发 → `editorAnchor` 是 ScrollView 内 VStack 的高度锚点 → 「滚到底」= 把 VStack 内**所有**元素（标题 TextField、第一张图片、之前的文本）一并推过 ScrollView 顶部 → 用户视觉上看到第二张图 + 大段空白，标题/历史图/历史文本全部不可见。

根因：`scrollTo(anchor: .bottom)` 把目标 view 的**底部对齐到 ScrollView 可见区域底部**，但「VStack 内的 view」被滚到底 = VStack 顶部以上所有内容被推出视口。在纯文本场景里 `editorAnchor` 之上只有标题，所以影响小；图文混排下 `editorAnchor` 之上还堆了历史图片，每插一张图都让滚动距离变大。^[inferred]

## Fix

`EntryEditorView.swift` 移除 ScrollViewReader + `.id("editorAnchor")` + onChange 三段：

```swift
// 移除前
ScrollViewReader { proxy in
    ScrollView {
        VStack { ... SelectableTextEditor.frame(height: max(120, textHeight)).id("editorAnchor") ... }
    }
    .onChange(of: textHeight) { _, new in
        if new > oldValue {
            withAnimation { proxy.scrollTo("editorAnchor", anchor: .bottom) }
        }
    }
}

// 移除后
ScrollView {
    VStack { ... SelectableTextEditor.frame(height: max(120, textHeight)) ... }
}
```

## 替代行为

- 正文增长时 VStack 内容自然扩展，ScrollView 自动处理溢出滚动
- caret 可见性由 UITextView 自身（`isScrollEnabled=false` 时 `contentSize` 仍正确）+ `keyboardAdaptive()` 键盘上推共同保障
- 如果后续发现 caret 被键盘挡住，需要补一个**基于 caret 位置**的滚动（不再基于 textHeight）

> 本修正与 [[projects/dayfold/skills/auto-expanding-texteditor-scroll]]「阶段 H 已修正三处」中的第 2 条对应（该 skill 已记录结论），本页保留根因与适用条件。

## 适用条件

任何 SwiftUI 编辑器内部是 UITextView + 外层 ScrollView 包 VStack 的结构，且 UITextView 用 `isScrollEnabled=false + frame(height:)` 模式——**图文混排下都不应该在外层用 `onChange(textHeight) → scrollTo(anchor: .bottom)` 这种「全局回滚」逻辑**。

纯文本场景可保留 `scrollTo(anchor: .bottom)`，因为 VStack 顶部元素固定不会因插入动作而上移。

## Verification

- 构建 `xcodebuild ... ** BUILD SUCCEEDED **`
- 用户在模拟器手动复测通过
- commit `1f07c0e fix(editor): 移除图后外层滚动，整段不再被推出屏幕顶部`

## Related

- [[synthesis/Research: SwiftUI 图文混排]] — synthesis
- [[projects/dayfold/skills/auto-expanding-texteditor-scroll]] — 整体复合滚动架构与阶段 H 演进
- [[projects/dayfold/skills/uitextview-intrinsic-width-overflow]] — 同一阶段 H 的姊妹 bug（intrinsic 宽度撑宽）
- [[projects/dayfold/skills/nstextattachment-bounds-overflow]] — 同一 session 的图片尺寸 bug
- [[projects/dayfold/concepts/architecture-overview]] — Dayfold 架构概览