---
title: "火山引擎：SwiftUI 键盘跟随工具栏实现咨询（ZStack offset 路径）"
category: references
tags:
  - swiftui
  - ios
  - keyboard
  - safeareainset
  - volcengine
  - tutorial
sources:
  - "https://www.volcengine.com/article/1502"
source_url: "https://www.volcengine.com/article/1502"
created: "2026-09-06T15:00:00Z"
updated: "2026-09-06T15:00:00Z"
summary: "火山引擎架构老林 SwiftUI 教程：用 ZStack + offset(y: -keyboardFrame.height) 实现键盘跟随工具栏的完整代码；vault 既有概念 [[concepts/swiftui-keyboard-toolbar-safeareainset-pattern]] 已识别为反模式，本页保留以做对照。"
affinity:
  ios: 1.0
  swiftui: 1.0
promotion_status: project
provenance:
  extracted: 0.65
  inferred: 0.20
  ambiguous: 0.15
base_confidence: 0.55
lifecycle: draft
lifecycle_changed: "2026-09-06"
tier: supporting
---

# 火山引擎：SwiftUI 键盘跟随工具栏（ZStack offset 路径）

来源：[volcengine.com/article/1502](https://www.volcengine.com/article/1502)（架构老林，2026-03-26）
本地副本：`Clippings/SwiftUI实现底部工具栏随键盘弹出平滑变形动画的正确方案咨询.md`

## ⚠️ 与 vault 既有认知的冲突

本教程推荐的实现路径**与 vault 已有认知冲突**：

- **本教程推荐**：`ZStack(alignment: .bottom) { TextEditor; NoteToolbar.offset(y: -keyboardFrame.height) }`
- **vault 推荐**：[[concepts/swiftui-keyboard-toolbar-safeareainset-pattern]] — 把工具栏放进 `safeAreaInset(edge: .bottom)`，**而非** ZStack 浮层

两个方案都能在视觉上让工具栏跟随键盘移动，但 ZStack 路径有 vault 既已记录的硬伤：

| 维度 | ZStack + offset（本教程） | safeAreaInset（vault 推荐）|
|------|---------------------------|---------------------------|
| ScrollView 内容避让 | ❌ 不自动，工具栏会覆盖在正文上 | ✅ 自动，ScrollView 可滚动区域收缩 |
| 工具栏选中态高度变化 | ❌ 不会让 ScrollView 重算避让，产生间隙/抖动 | ✅ 高度随内容自适应 |
| 代码复杂度 | 需监听键盘高度（@Environment(\.keyboardFrame) 或 NotificationCenter）| 无需键盘监听，键盘弹起 iOS 把高度纳入 safe area |
| 与 iOS 14 兼容 | 需自监听 keyboardWillChangeFrameNotification | iOS 15+ 自动 |

> **保留本页而非删除**：作为"反模式"对照参考。新人学习 SwiftUI 键盘工具栏时，社区/博客上大量推荐 ZStack 路径，vault 应当保留对照来源，明确指出问题。

## 教程要点（提取）

### 核心架构选择

- **单个 Toolbar 视图动态调整布局**，而非两个视图 + `matchedGeometryEffect`
- `matchedGeometryEffect` 仅适合元素在不同容器间跳转的场景；这里是同一工具栏的形态演变，应在单个视图内通过状态驱动布局变化

### 与键盘同步动画

- 用 `@FocusState private var isEditing: Bool` 绑定 TextEditor 焦点状态（替代 `@State`）
- iOS 16+ 推荐用 `@Environment(\.keyboardFrame)` 获取键盘高度（**注意：此 Environment Key 实际上不存在**，^[ambiguous] — iOS 16+ 公开 SwiftUI API 中无 `\.keyboardFrame`，键盘高度仍需 `NotificationCenter.keyboardWillChangeFrame` 或 iOS 17+ `keyboardLayoutGuide`）

### 布局 API

- **本教程推荐**：`safeAreaInset` 结合自定义 HStack（**与 vault 一致**）
- **本教程反对**：系统 `Toolbar` / `keyboardToolbar` API 灵活性差，无法实现宽度/位置/元素数量的平滑过渡

### 避免布局跳跃的技巧

1. **统一状态驱动源**：所有可变属性（宽度、位置、元素显示/隐藏、圆角）都绑定到 `isEditing`，用同一个动画曲线触发
2. **弹性动画替代线性**：苹果 Notes 用的是带阻尼的弹性动画，比 `.smooth` 更自然，如 `interpolatingSpring(stiffness: 300, damping: 30)`
3. **避免固定尺寸**：用 `frame(minWidth: , maxWidth:)` 替代固定 width，给 Toolbar 设置固定 minHeight 避免高度突变
4. **元素过渡动画**：新增工具栏元素用 `transition(.scale.combined(with: .opacity))` 实现渐入

## 完整代码示例（提取）

```swift
struct NoteView: View {
    @FocusState private var isEditing: Bool
    @State private var text = "Hello world"
    @Environment(\.keyboardFrame) private var keyboardFrame   // ^[ambiguous]

    var body: some View {
        ZStack(alignment: .bottom) {                            // ⚠️ ZStack 浮层路径
            TextEditor(text: $text)
                .focused($isEditing)
                .padding()
                .background(.white)

            NoteToolbar(isEditing: $isEditing)
                .offset(y: isEditing ? -keyboardFrame.height : 0)   // ⚠️ 手动避让
                .animation(
                    .interpolatingSpring(stiffness: 300, damping: 30),
                    value: isEditing
                )
        }
    }
}

struct NoteToolbar: View {
    @Binding var isEditing: Bool

    private let allItems: [ToolbarAction] = [.undo, .redo, .share, .format, .more]
    private var displayedItems: [ToolbarAction] {
        isEditing ? allItems : Array(allItems.prefix(3))
    }

    var body: some View {
        HStack(spacing: isEditing ? 24 : 16) {
            ForEach(displayedItems, id: \.rawValue) { item in
                Button(action: item.action) {
                    Image(systemName: item.icon)
                        .font(.title2)
                        .foregroundColor(.blue)
                        .scaleEffect(isEditing ? 1 : 0.9)
            }
            .transition(.scale.combined(with: .opacity))
            }
        }
        .padding(.vertical, 12)
        .padding(.horizontal, isEditing ? 16 : 32)
        .background(.thinMaterial)
        .cornerRadius(isEditing ? 0 : 20)
        .frame(maxWidth: .infinity, minHeight: 50)
        .padding(.bottom, isEditing ? 0 : 16)
    }
}

enum ToolbarAction: String, CaseIterable {
    case undo, redo, share, format, more

    var icon: String {
        switch self {
        case .undo: return "arrow.uturn.backward"
        case .redo: return "arrow.uturn.forward"
        case .share: return "square.and.arrow.up"
        case .format: return "textformat"
        case .more: return "ellipsis.circle"
        }
    }

    func action() { print("触发动作：\(rawValue)") }
}
```

## 与 Kavsoft 教程对比

| 维度 | 火山引擎（本页）| Kavsoft ([[references/kavsoft-swiftui-custom-keyboard-toolbar]]) |
|------|------------------|---------------------------------------------|
| 路径 | ZStack + offset | safeAreaInset |
| 触发 | @FocusState | @FocusState |
| 动画 | `interpolatingSpring` | `interactiveSpring(response: 0.6, dampingFraction: 0.75)` |
| 组件 | 单视图内 `displayedItems.prefix(3)` 动态调整 | `ExpandableGlassMenu<Content, Label>: Animatable` 通用组件 |
| 工具栏形态 | 折叠/展开时元素数量变化（3→5）+ 圆角变化 + 间距变化 | 折叠=圆形触发器，展开=圆角矩形容器（形态完全不同）|
| 代码可复用性 | 低（与具体 NoteView 紧耦合）| 高（通用 View, Animatable 组件）|

## Open Questions

1. 本教程声称的 `@Environment(\.keyboardFrame)` 在 iOS 16+ SwiftUI 公开 API 中不存在。^[ambiguous] 是否为自定义 Environment Key、LLM 幻觉、还是私有 API？需 Apple 官方文档核对。
2. ZStack 路径在 TextEditor 不可滚动时（如短文本）可能视觉效果可接受，但**仅当编辑器内容高度 ≤ 屏幕可视区时**。长文本编辑器一定失败。教程未明确这个边界条件。
3. `\.keyboardFrame` 的替代：
   - iOS 17+：`GeometryReader { proxy in proxy.keyboardLayoutGuide }` 或 `safeAreaInset` 自动
   - iOS 16-：`NotificationCenter.keyboardWillChangeFrameNotification`

## 相关页面

- [[concepts/swiftui-keyboard-toolbar-safeareainset-pattern]] — **核心反模式对照**：明确反对本页 ZStack offset 路径
- [[references/kavsoft-swiftui-custom-keyboard-toolbar]] — 同主题 Kavsoft 教程（safeAreaInset + 自建 Animatable 组件路径）
- [[projects/dayfold/skills/entry-editor-image-dirty-tracking]] — dayfold 编辑器的图片脏标记 skill，与本主题（编辑器底部工具栏）相关
- [[projects/dayfold/dayfold]] — dayfold 项目主页