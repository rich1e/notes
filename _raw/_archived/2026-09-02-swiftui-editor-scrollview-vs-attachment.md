---
title: 图文混排下外层 ScrollViewReader scrollTo 的反行为
created: 2026-09-02
updated: 2026-09-02
tags: [swiftui, textkit, nstextattachment, dayfold]
summary: 图文混排下每插图触发 textHeight 增大，scrollTo editorAnchor 底部会把标题/历史图片/历史文本全部推出屏幕顶部；改为内层 UITextView 自管理 caret 可见性即可。
base_confidence: 0.75
provenance:
  extracted: 0.8
  inferred: 0.2
lifecycle: draft
lifecycle_changed: 2026-09-02
sources:
  - dayfold session (2026-09-02)
---

## 现象

`EntryEditorView` 用 `ScrollViewReader { ScrollView { VStack { title + SelectableTextEditor + tags + Spacer } } }`，并且 `.onChange(of: textHeight) { if newValue > oldValue { proxy.scrollTo("editorAnchor", anchor: .bottom) } }`。

意图是"正文长高（新增行/插图）时滚到正文底保证光标可见"——这是纯文本编辑场景的合理优化。

**图文混排下产生反行为**：用户在已有图片的笔记里再插入一张图 → textHeight 增大 → `scrollTo("editorAnchor", anchor: .bottom)` 被触发 → `editorAnchor` 是 ScrollView 内 VStack 的高度锚点 → "滚到底" = 把 VStack 内**所有**元素（标题 TextField、第一张图片、之前的文本）一并推过 ScrollView 顶部 → 用户视觉上看到第二张图 + 大段空白，标题/历史图/历史文本全部不可见。

## 修复

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
- caret 可见性由 UITextView 自身（`isScrollEnabled=false` 时 contentSize 仍正确）+ `keyboardAdaptive()` 键盘上推共同保障
- 如果后续发现 caret 被键盘挡住，需要补一个基于 caret 位置的滚动（不再基于 textHeight）

## 适用条件

任何 SwiftUI 编辑器内部是 UITextView + 外层 ScrollView 包 VStack 的结构，且 UITextView 用 `isScrollEnabled=false + frame(height:)` 模式——图文混排下都不应该在外层用 `onChange(textHeight) → scrollTo` 这种"全局回滚"逻辑。

## 验证

- 构建 `xcodebuild ... ** BUILD SUCCEEDED **`
- 用户在模拟器手动复测通过
- commit `1f07c0e fix(editor): 移除图后外层滚动，整段不再被推出屏幕顶部`

## Related

- [[nstextattachment-bounds-overflow]] — 同一 session 的姊妹 bug：图片被撑爆
