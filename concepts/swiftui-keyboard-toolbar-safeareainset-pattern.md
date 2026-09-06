---
title: SwiftUI 键盘跟随工具栏 safeAreaInset 模式
category: concepts
tags:
  - swiftui
  - layout
  - keyboard
  - safeareainset
  - ux
  - mobile
sources: []
created: 2026-09-06T17:00:00Z
updated: 2026-09-06T15:20:00Z
summary: "编辑器下方工具栏跟随键盘上移的正确做法是把工具栏放进 ScrollView/容器的 safeAreaInset(edge: .bottom)；ZStack 浮层 + padding(.bottom, keyboardHeight) 只能平移工具栏，不能同步让 ScrollView 内容收缩，会出现『工具栏漂浮在中间 + 内容覆盖』。"
base_confidence: 0.82
lifecycle: draft
lifecycle_changed: 2026-09-06
tier: supporting
provenance:
  extracted: 0.00
  inferred: 0.95
  ambiguous: 0.05
relationships:
  - target: "[[concepts/swiftui-rich-text-rendering-comparison]]"
    type: related_to
  - target: "[[references/kavsoft-swiftui-custom-keyboard-toolbar]]"
    type: extends
  - target: "[[references/volcengine-swiftui-keyboard-toolbar-zstack-offset]]"
    type: contradicts
  - target: "[[references/swiftui-ios26-toolbar-transitions-morphing]]"
    type: related_to
---

# SwiftUI 键盘跟随工具栏 safeAreaInset 模式

## Context

在 iOS 编辑器/输入框场景中,经常需要在文本框下方放一个"工具栏"(收起键盘 / 插入图片 / 切换输入法 / 选中态格式化等),并且希望:

- 键盘弹起时,工具栏紧贴键盘顶部,不被键盘覆盖;
- 工具栏上方的正文/ScrollView 内容不与工具栏重叠,正文最后一行始终可见;
- 键盘未弹时,工具栏坐在屏幕底安全区上方。

## Finding

把工具栏作为容器(常用 `ScrollView` 或 `VStack` 里 ScrollView)的 `.safeAreaInset(edge: .bottom, spacing: 0) { ... }` 的内容,可以同时解决"工具栏位置"和"内容避让"两个问题,无需手写键盘高度监听。

```swift
ScrollView { /* 标题 / 正文 / 标签 */ }
    .safeAreaInset(edge: .bottom, spacing: 0) {
        keyboardToolbar
    }
```

- `safeAreaInset` 会把 inset 内容插入到容器布局的边缘,**同时让容器可滚动区域收缩**,所以 ScrollView 的内容自然停在工具栏正上方。
- 键盘弹起时,iOS 的 safe area 把键盘高度纳入下边距,`safeAreaInset` 内容随之下移(贴在键盘顶部),无需自监听 `keyboardWillChangeFrameNotification`。
- 选中态展开/折叠(如 `FormattingToolbar(compact: true)` 显隐)时,inset 高度自动跟随实际内容,无空隙/重叠。

## Anti-Pattern: ZStack 浮层 + padding(keyboardHeight)

另一种常见反模式:

```swift
ZStack(alignment: .bottom) {
    VStack { topBar; editorArea }
    keyboardToolbar.padding(.bottom, keyboardHeight)
}
```

这条路径**只平移工具栏**,ScrollView 的高度仍按"未弹键盘"渲染,后果:

- 工具栏被推到屏幕中段而非键盘顶部,视觉上"漂浮在中间";
- 工具栏覆盖在正文上方,选中文本时光标被工具栏挡住;
- 选中态展开 FormattingToolbar 时,工具栏实际高度变化不会让 ScrollView 重算避让,产生间隙或压字。

**唯一仍需自监听键盘的边界情况**:`safeAreaInset` 在 iOS 14 旧版不自动跟键盘安全区(15+ 起基本一致),若要兼容 iOS 14 需保留 `KeyboardAdaptiveModifier` 但挂在 `safeAreaInset` 的内容上,而非外层 ZStack。

## 双倍占位的第二根钉

即便用了 ZStack 浮层,如果 ScrollView 内部还人为放一个 `Spacer().frame(height: 56)` 之类的"键盘占位",会和工具栏真实高度叠加,出现"工具栏在屏幕底 + ScrollView 内还有 56pt 死区"的双重补偿。占位高度**永远对不上**选中态展开后的实际工具栏高度,间隙/抖动不可避免。

**根除做法**:ScrollView 内部不写死占位,避让由 `safeAreaInset` 全权负责。

## When to Use

- 任何"内容区 + 底部固定/浮动工具栏"组合,只要工具栏要在键盘弹起时上移,首选 `safeAreaInset`。
- 工具栏高度会随选中态变化(如长按文本展开 Markdown 格式条)时,`safeAreaInset` 是唯一不会产生间隙的方案。

## When NOT to Use

- 工具栏位置由业务状态决定(如 `step` 进度条在键盘上方/下方切换)而非键盘:仍可用 `safeAreaInset` 配合 `if`,但视觉语义不同时用 VStack 子元素更清晰。
- 工具栏需要"浮在 ScrollView 之上但不挤开内容"(如悬浮操作条),可改用 `.overlay(alignment: .bottom)`;但要注意 overlay 不会让内容避让,需要自管占位。

## Related

- [[concepts/swiftui-framework]]
- [[concepts/swiftui-rich-text-rendering-comparison]]
- [[references/kavsoft-swiftui-custom-keyboard-toolbar]] — 同主题 Kavsoft 教程（safeAreaInset + Animatable 组件，可复用性高）
- [[references/volcengine-swiftui-keyboard-toolbar-zstack-offset]] — **反模式对照**：火山引擎/字节跳动旗下教程推荐的 ZStack + offset 路径，与本页 safeAreaInset 主张直接冲突；保留以备社区对比
- [[references/swiftui-ios26-toolbar-transitions-morphing]] — **主题区分**：iOS 26 屏幕间工具栏变形（navigation-driven morph）vs 键盘工具栏（keyboard-driven follow），是不同问题但同代 API
- [[concepts/swiftui-safeareabar-vs-safeareainset-pattern]] — **姊妹概念**：iOS 26 `.safeAreaBar(edge: .bottom)` 是本页 safeAreaInset 的非滚动容器版本；List / 固定内容用 safeAreaBar，ScrollView 用 safeAreaInset
