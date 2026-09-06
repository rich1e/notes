---
title: "DaniilL12321/customToolbar_iOS26 仓库参考"
category: references
tags:
  - swiftui
  - ios-26
  - github
  - repository
  - safeareabar
  - glass-effect
  - tutorial
sources:
  - "https://github.com/DaniilL12321/customToolbar_iOS26"
source_url: "https://github.com/DaniilL12321/customToolbar_iOS26"
created: "2026-09-06T15:25:00Z"
updated: "2026-09-06T15:25:00Z"
summary: "Daniil Lobanov 的 iOS 26 自定义动画底部栏 demo 仓库；189 LOC ContentView.swift 演示 5 个 iOS 26 新 API（safeAreaBar / glassEffect / AnyLayout / Animatable modifier / symbolEffect）。"
affinity:
  ios: 1.0
  swiftui: 1.0
promotion_status: project
provenance:
  extracted: 0.90
  inferred: 0.05
  ambiguous: 0.05
base_confidence: 0.82
lifecycle: draft
lifecycle_changed: "2026-09-06"
tier: supporting
---

# DaniilL12321/customToolbar_iOS26 仓库参考

> **作者**：Daniil Lobanov（俄罗斯开发者，2025-09-19 commit）
> **仓库**：https://github.com/DaniilL12321/customToolbar_iOS26
> **协议**：MIT
> **规模**：极小（7 files / 8.9KB / 2.2k tokens）
> **commit**：81d5b36fad58e263ca1b78fbd06572833bfe172e
> **本地缓存**：`_raw/github-DaniilL12321-customToolbar_iOS26.txt`

## 仓库定位

一个 **极简但密集**的 iOS 26 SwiftUI demo 仓库：

- **目的**：演示 iOS 26 的 `safeAreaBar` + Liquid Glass + 自定义动画组合
- **要求**：Xcode 26.0+ / iOS 26.0+（旧版本能跑但视觉是旧 iOS 风格）
- **场景**：编辑器型 App 的底部工具栏 + 搜索栏 + 主操作按钮三件套

## 仓库结构

```
customToolbar_iOS26/
├── README.md              # 俄语说明 + 演示视频链接
├── LICENSE                # MIT
└── testApp/
    ├── ContentView.swift  # 189 LOC 全部核心代码
    ├── testAppApp.swift   # @main App 入口（5 行）
    └── Assets.xcassets/   # 标准 App icon + AccentColor
```

**核心代码全在 1 个文件**：189 LOC ContentView.swift = 整个 demo。

## 5 个 iOS 26 新 API 一次性演示

### 1. `.safeAreaBar(edge: .bottom, spacing: 0)` (行 103)

iOS 26 新 modifier，专门用于"非滚动内容 + 底部固定栏 + 键盘跟随"。

```swift
.safeAreaBar(edge: .bottom, spacing: 0) {
    CustomBottomBar(...)
}
```

**与 `.safeAreaInset` 区别**：见 [[concepts/swiftui-safeareabar-vs-safeareainset-pattern]] 姊妹概念。

### 2. `.glassEffect(.regular.interactive(), in: .capsule / .circle)` (行 187, 198)

Liquid Glass API，比 `.buttonStyle(.glass)` 更细粒度——可应用于**任何 View**（不只是 Button）。

```swift
.glassEffect(.regular.interactive(), in: .capsule)  // 胶囊形玻璃
.glassEffect(.regular.interactive(), in: .circle)    // 圆形玻璃
```

`.regular.interactive()` 表示"用户可交互时变亮"——点击有视觉反馈。

### 3. `AnyLayout(HStackLayout vs ZStackLayout)` + `ForEach(subviews:)` (行 155-163)

iOS 17+ Layout protocol 的实战应用。折叠态和展开态用**不同布局策略**：

```swift
let layout = isExpanded ? AnyLayout(HStackLayout(spacing: 10)) : AnyLayout(ZStackLayout())

layout {
    ForEach(subviews: leadingContent(isExpanded)) { subview in
        subview.frame(width: 50, height: 50)
    }
}
```

- 折叠（`!isExpanded`）：ZStack 把按钮堆叠在重叠位置（节省横向空间）
- 展开（`isExpanded`）：HStack 水平排列按钮

`ForEach(subviews:)` (iOS 16+) 直接遍历 `@ViewBuilder` 产生的不透明视图集合，是处理"动态子视图组"的关键。

### 4. `ScaleModifier: ViewModifier, Animatable` (行 224-244)

自定义 modifier 实现**循环弹跳**动画——与 [[references/kavsoft-swiftui-custom-keyboard-toolbar]] 的 `ExpandableGlassMenu: View, Animatable` 是**同架构**：

```swift
struct ScaleModifier: ViewModifier, Animatable {
    var bounce: CGFloat
    var animatableData: CGFloat {
        get { bounce }
        set { bounce = newValue }
    }

    func body(content: Content) -> some View {
        content
            .compositingGroup()
            .blur(radius: loopProgress * 5)
            .glassEffect(.regular.interactive(), in: .capsule)
            .scaleEffect(1 + (loopProgress * 0.38), anchor: .center)
    }

    var loopProgress: CGFloat {
        let moddedBounce = bounce.truncatingRemainder(dividingBy: 1)
        let value = moddedBounce > 0.5 ? 1 - moddedBounce : moddedBounce
        return value * 2
    }
}
```

**关键技巧**：`bounce.truncatingRemainder(dividingBy: 1)` + `moddedBounce > 0.5 ? 1 - moddedBounce : moddedBounce` 形成**三角波**0→1→0→1，让 `scaleEffect` 在 [1.0, 1.38] 之间循环，触发 SwiftUI 动画管线持续插值。

### 5. `.contentTransition(.symbolEffect)` (行 126)

SF Symbol 动画过渡——非激活态是 `square.and.pencil`（笔），激活态是 `xmark`（关闭），用 `.symbolEffect` 让图标切换有视觉过渡：

```swift
Image(systemName: isKeyboardActive ? "xmark" : "square.and.pencil")
    .font(.title2)
    .contentTransition(.symbolEffect)
```

## 关键依赖图

无外部依赖（无 Swift Package Manager 依赖），纯 SwiftUI + iOS 26 标准 API。

## 关键技术观察

1. **依赖 `\.safeAreaBar`** 是 iOS 26 新增 modifier（Apple 在 WWDC 2025 SwiftUI 更新中提及）
2. **`isKeyboardActive` 用 `@FocusState`**——驱动键盘跟随的标准 SwiftUI 路径
3. **`@ViewBuilder var leadingContent: (_ isExpanded: Bool) -> LeadingContent`**——泛型 ViewBuilder 接受参数化子视图，与 Kavsoft ExpandableGlassMenu 同思路
4. **`.transition(.blurReplace)`** —— iOS 17+ View 替换时用 blur 过渡
5. **`interactiveSpring` 在 demo 中未使用** —— 用的是 `.smooth(duration: 0.3, extraBounce: 0)`（iOS 17+ 新 animation API，比 spring 简单）

## Vault 价值

- **5 个 iOS 26 API 集中在 189 行** —— 是 vault 现有 Kavsoft/hasanalidev/volcengine 集群的**完美补充**（各自 1-2 个 API，这个集中演示 5 个）
- **MIT 协议** —— 可直接借鉴代码片段到 dayfold 项目
- **`safeAreaBar` 概念** —— vault 缺失的关键 piece（既有 safeAreaInset 是 ScrollView 版本，本 demo 演示非滚动容器版本）

## Open Questions

1. `safeAreaBar` 在 iOS 26 公开 API 中是 stable 还是 beta？是否需要回退？^[ambiguous]
2. `.glassEffect(.regular.interactive(), in:)` 第三个参数 shape（`.capsule` / `.circle`）还支持哪些？^[ambiguous]
3. `ForEach(subviews:)` 与 `ForEach(0..<n)` 在 `@ViewBuilder` 上下文中的性能差异？^[ambiguous]

## 相关页面

- [[concepts/swiftui-safeareabar-vs-safeareainset-pattern]] — **核心概念提炼**：safeAreaBar 与 safeAreaInset 的对比、List vs ScrollView 选择
- [[concepts/swiftui-keyboard-toolbar-safeareainset-pattern]] — 姊妹概念（滚动容器版本）
- [[references/kavsoft-swiftui-custom-keyboard-toolbar]] — 同架构 Animatable 组件（ExpandableGlassMenu）
- [[references/swiftui-ios26-toolbar-transitions-morphing]] — iOS 26 同代 API 主题：变形而非固定+跟随
- [[references/volcengine-swiftui-keyboard-toolbar-zstack-offset]] — ZStack 反模式对照
- [[concepts/swiftui-animatablemodifier-pattern]] — `ScaleModifier: ViewModifier, Animatable` 的协议抽象提炼（vault 总结）
- [[synthesis/Research: SwiftUI Custom Animation Toolbar in iOS 26]] — 3 轮研究综合 master synthesis