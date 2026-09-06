---
title: "SwiftUI safeAreaBar vs safeAreaInset 模式 — iOS 26 自定义底部栏的正解"
category: concepts
tags:
  - swiftui
  - layout
  - safeareabar
  - safeareainset
  - ios-26
  - ux
  - mobile
sources:
  - "https://github.com/DaniilL12321/customToolbar_iOS26"
source_url: "https://github.com/DaniilL12321/customToolbar_iOS26"
created: "2026-09-06T15:25:00Z"
updated: "2026-09-06T15:25:00Z"
summary: "iOS 26 新增 .safeAreaBar(edge: .bottom) modifier，专门用于「容器内不滚动 + 需要底部固定栏 + 键盘跟随」场景；与既有 safeAreaInset 互补但语义更清晰。"
base_confidence: 0.78
lifecycle: draft
lifecycle_changed: "2026-09-06"
tier: supporting
provenance:
  extracted: 0.70
  inferred: 0.25
  ambiguous: 0.05
relationships:
  - target: "[[concepts/swiftui-keyboard-toolbar-safeareainset-pattern]]"
    type: related_to
  - target: "[[references/kavsoft-swiftui-custom-keyboard-toolbar]]"
    type: related_to
  - target: "[[references/swiftui-ios26-toolbar-transitions-morphing]]"
    type: related_to
  - target: "[[references/volcengine-swiftui-keyboard-toolbar-zstack-offset]]"
    type: contradicts
---

# SwiftUI safeAreaBar vs safeAreaInset 模式

## Context

iOS 26 新增 **`safeAreaBar(edge: .bottom, spacing: 0) { ... }`** modifier，专门处理"容器内有 List 等非滚动内容 + 需要底部固定工具栏 + 工具栏要跟随键盘"的场景。这与 iOS 15+ 的 `safeAreaInset(edge: .bottom)` 在 Surface 上类似，但语义更清晰、行为更可预测。

| 维度 | safeAreaInset (iOS 15+) | safeAreaBar (iOS 26) |
|------|-------------------------|------------------------|
| 容器内容 | 通常是 ScrollView（需要让内容避让） | 通常是 List / 固定内容（不需要避让）|
| 滚动行为 | 容器可滚动区域会收缩 | 内容不滚动，栏只是"插入"在底部 |
| 键盘跟随 | ✅ 自动 | ✅ 自动（API 一致性）|
| 视觉用途 | 滚动内容区的浮动工具栏 | 固定 List / 内容区的固定工具栏 |
| 反模式 ZStack 替代 | ❌ ScrollView 浮层 (vault 既已识别) | ❌ List + ZStack 浮层 (本页反对) |

## Finding

**正确的 `.safeAreaBar` 用法**：

```swift
NavigationStack(path: $path) {
    List {
        ForEach(1...50, id: \.self) { index in
            NavigationLink(value: "link") {
                Text("link \(index)")
            }
        }
    }
    .navigationTitle("title")
    .safeAreaPadding(.bottom, 50)   // 为栏预留 50pt 高度
    .navigationDestination(for: String.self) { value in
        Text("full view").navigationTitle(value)
    }
}
.safeAreaBar(edge: .bottom, spacing: 0) {  // ⚠️ 挂在内层 NavigationStack 之外的容器上
    CustomBottomBar(...)
}
```

**两个关键点**：
1. `.safeAreaBar` 挂在 NavigationStack 之外（不是内层 root view），让栏成为导航容器的边界元素
2. 内层 List 需要 `.safeAreaPadding(.bottom, 50)` 为栏预留视觉空间，否则 List 内容会延伸到栏底部

## Anti-Pattern: List + ZStack 浮层

ZStack + offset 路径同样不适用 List 容器：

```swift
// ❌ 反模式（与 keyboard toolbar 主题同根问题）
ZStack(alignment: .bottom) {
    NavigationStack { List { ... } }
    CustomBottomBar.offset(y: isKeyboardActive ? -keyboardHeight : 0)
}
```

后果：List 滚动到最底部时，最后一行会被工具栏遮挡；选中态展开时高度变化会让工具栏漂浮。

## 与现有 vault 知识的关系

- **与 [[concepts/swiftui-keyboard-toolbar-safeareainset-pattern]] 是姊妹概念**：两者都是"键盘跟随 + 不漂浮"模式的正解，区别在于容器是否滚动
- **与 [[references/kavsoft-swiftui-custom-keyboard-toolbar]] 主题相邻**：Kavsoft 关注可展开工具栏，本概念关注底部固定栏
- **与 [[references/volcengine-swiftui-keyboard-toolbar-zstack-offset]] 反模式对照**：火山引擎推 ZStack 路径在 List 容器同样失败
- **与 [[references/swiftui-ios26-toolbar-transitions-morphing]] 互补**：iOS 26 同代 API 主题，一个是变形（本页是固定+跟随）

## 何时选 safeAreaBar vs safeAreaInset

| 场景 | 选哪个 |
|------|--------|
| 内容区是 List / 静态 View | ✅ `safeAreaBar` (iOS 26) |
| 内容区是 ScrollView (滚动列表) | ✅ `safeAreaInset` (iOS 15+) |
| 内容区是 Form | ✅ `safeAreaBar` (iOS 26) |
| 内容区是 Grid（不滚动）| ✅ `safeAreaBar` (iOS 26) |
| 旧 iOS 版本兼容（< iOS 26）| ⚠️  只能用 `safeAreaInset` |

## Open Questions

1. `safeAreaBar` 是 iOS 26 正式 API 还是 beta 命名？Apple 文档是否完整？^[ambiguous]
2. `safeAreaPadding(.bottom, 50)` 的 50 是否应该用 GeometryReader 动态测量栏高度？^[ambiguous]
3. `safeAreaBar` 与 NavigationStack 内置的 toolbar 在同一 bottom 区域是否会冲突？^[ambiguous]

## 参考实现

`https://github.com/DaniilL12321/customToolbar_iOS26`（Daniil Lobanov，2025-09-19 commit，MIT 协议）

完整 demo 含：
- `ContentView.swift`（189 LOC，2025-09-19 更新）
- `CustomBottomBar<LeadingContent, MainAction>` 泛型组件
- `ScaleModifier: ViewModifier, Animatable` 弹跳动画 modifier（与 Kavsoft `ExpandableGlassMenu` 同架构）
- 5 个 iOS 26 新 API 在 1 个文件全部演示：

| API | 行号 | 用途 |
|-----|------|------|
| `.safeAreaBar(edge: .bottom, spacing: 0)` | 103 | 底部固定栏容器（iOS 26 新增）|
| `.glassEffect(.regular.interactive(), in: .capsule)` | 187, 198 | Liquid Glass 玻璃质感 |
| `AnyLayout(HStackLayout vs ZStackLayout)` + `ForEach(subviews:)` | 155-163 | 折叠/展开时切换布局策略 |
| `ScaleModifier: ViewModifier, Animatable` | 224-244 | 自定义弹跳动画 modifier |
| `.contentTransition(.symbolEffect)` | 126 | SF Symbol 动画过渡 |

## 相关页面

- [[concepts/swiftui-keyboard-toolbar-safeareainset-pattern]] — 滚动容器版本（ScrollView 内容避让）
- [[references/kavsoft-swiftui-custom-keyboard-toolbar]] — Animatable 组件同架构（Kavsoft ExpandableGlassMenu）
- [[references/swiftui-ios26-toolbar-transitions-morphing]] — iOS 26 同代 API：DefaultToolbarItem / ToolbarSpacer / toolbar(id:)，主题是变形而非固定+跟随
- [[references/volcengine-swiftui-keyboard-toolbar-zstack-offset]] — ZStack 反模式对照
- [[references/daniill12321-customtoolbar-ios26-package]] — DaniilL12321 仓库参考页（具体实现）