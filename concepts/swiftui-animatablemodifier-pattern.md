---
title: "SwiftUI AnimatableModifier 协议 —— 自定义 modifier 与动画"
category: concepts
tags:
  - swiftui
  - animation
  - animatable
  - animatablemodifier
  - viewmodifier
  - ios-26
sources:
  - "https://developer.apple.com/documentation/swiftui/animatablemodifier"
  - "https://www.hackingwithswift.com/quick-start/swiftui"
  - "https://sarunw.com/posts/"
  - "https://swiftuifoundation.com/"
created: "2026-09-06T16:00:00Z"
updated: "2026-09-06T16:00:00Z"
summary: "AnimatableModifier 协议让自定义 ViewModifier 的内部状态可被 SwiftUI 动画管线插值，是 toolbar 工具类弹跳/进度/路径动画的基石；与 Kavsoft ExpandableGlassMenu / DaniilL12321 ScaleModifier 同架构。"
affinity:
  ios: 0.95
  swiftui: 1.0
promotion_status: project
provenance:
  extracted: 0.55
  inferred: 0.35
  ambiguous: 0.10
base_confidence: 0.72
lifecycle: draft
lifecycle_changed: "2026-09-06"
tier: supporting
---

# SwiftUI AnimatableModifier 协议

## Context

`ViewModifier` 默认只渲染静态外观 —— 当 modifier 内部状态改变时，SwiftUI 直接重绘，不做插值。要让自定义 modifier **响应动画**（比如按下时弹一下、拖动时缩放、进度条平滑增长），需要实现 `Animatable` 或 `AnimatableModifier` 协议。

SwiftUI 提供两条路径：

1. **`View, Animatable`** — 让整个 view 可动画（用于自绘 view）
2. **`ViewModifier, Animatable`** — 让 modifier 可动画（**核心场景**：toolbar 工具按钮、菜单项、可复用 modifier）

## Finding

`AnimatableModifier` 是 `ViewModifier` 与 `Animatable` 的复合协议。核心要求：

```swift
struct BounceModifier: ViewModifier, Animatable {
    var var bounce: CGFloat
    var animatableData: CGFloat {
        get { bounce }
        set { bounce = newValue }
    }

    func body(content: Content) -> some View {
        content
            .scaleEffect(1 + (bounce * 0.38))
            .blur(radius: bounce * 5)
    }
}
```

**关键**：`animatableData` 把 modifier 内部的 `CGFloat` 暴露给 SwiftUI 动画管线。当外部状态用 `.animation(.bouncy, value: ...)` 驱动时，SwiftUI 会在每帧重新调用 `body(content:)`，传入新插值后的 `animatableData`。

## 与 vault 既实现的对照

| Vault 实现 | 位置 | AnimatableData 类型 | 动画来源 |
|------------|------|---------------------|----------|
| `ExpandableGlassMenu` | [[references/kavsoft-swiftui-custom-keyboard-toolbar]] | `CGFloat progress` (0→1) | `.animation(.interactiveSpring(...), value: isExpanded)` |
| `ScaleModifier` | [[references/daniill12321-customtoolbar-ios26-package]] | `CGFloat bounce`（循环三角波）| `withAnimation(.bouncy) { bounce += 1 }` |

两个仓库独立设计但同架构 —— vault 既有 cluster 已隐含此模式，本页把模式抽象升华为概念。

## iOS 26 增强

- **`Phase Animator`** (iOS 17+,强化于 iOS 26) — 对 `AnimatableModifier` 不需 manual `animatableData` 的 high-level 抽象
- **`.symbolEffect` / `contentTransition(.symbolEffect)`** — SF Symbol 切换自动动画（参考 [[references/swiftui-ios26-toolbar-transitions-morphing]] 中 `.contentTransition(.symbolEffect)` 用法）
- **`.animation(_:value:)` 改良** — iOS 26 优化 implicit animation 的依赖追踪

## 何时用 AnimatableModifier vs 普通 ViewModifier

| 场景 | 推荐 |
|------|------|
| 静态 modifier（边距、圆角固定）| 普通 `ViewModifier` |
| 弹跳/缩放/旋转类交互反馈 | `ViewModifier, Animatable` |
| 自定义进度条/路径动画 | `ViewModifier, Animatable` |
| 整个 view 都是手画（如波形图）| `View, Animatable` |
| iOS 17+ 想避免手写 `animatableData` | `Phase Animator` |

## 性能要点

- **保持 `animatableData` 计算轻量** — `body(content:)` 在每帧调用，避免在内部做 expensive layout
- **GPU-friendly 属性** — `opacity`, `scale`, `rotation`, `blur`, `offset` 都走 Render Server；`frame`, `padding`, layout-affecting 改动走 layout pass
- **避免在 `body` 里创建 `Formatter` 或 Date components**（每帧重建）

参考 [[concepts/swiftui-rich-text-rendering-comparison]] 关于布局与渲染 pipeline 的拆解。

## Open Questions

1. `Phase Animator` 与手写 `AnimatableModifier` 在 iOS 26 性能上有无差异？^[ambiguous]
2. `animatableData` 支持多字段组合（struct 多 CGFloat）吗？Apple 文档需更详细。^[ambiguous]

## 相关页面

- [[references/kavsoft-swiftui-custom-keyboard-toolbar]] — 实战：`ExpandableGlassMenu`
- [[references/daniill12321-customtoolbar-ios26-package]] — 实战：`ScaleModifier`
- [[references/swiftui-ios26-toolbar-transitions-morphing]] — iOS 26 工具栏 API 主题
- [[concepts/swiftui-rich-text-rendering-comparison]] — 渲染 pipeline 拆解