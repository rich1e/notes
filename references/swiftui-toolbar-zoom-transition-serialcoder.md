---
title: "Morphing Sheets Out of Buttons in SwiftUI (SerialCoder.dev)"
category: references
tags:
  - swiftui
  - navigation
  - sheet
  - matchedTransitionSource
  - zoom-transition
  - serialcoder
  - tutorial
sources:
  - "https://serialcoder.dev/?p=18226"
  - "https://serialcoder.dev/swiftui/morphing-sheets-out-of-buttons-in-swiftui"
source_url: "https://serialcoder.dev/?p=18226"
created: "2026-09-06T16:00:00Z"
updated: "2026-09-06T16:00:00Z"
summary: "SerialCoder.dev 教程：用 matchedTransitionSource + navigationTransition(.zoom) 实现 toolbar 按钮 → sheet 的放大过渡动画（iOS 18+，iOS 26 改进）。"
affinity:
  ios: 1.0
  swiftui: 1.0
promotion_status: project
provenance:
  extracted: 0.90
  inferred: 0.05
  ambiguous: 0.05
base_confidence: 0.85
lifecycle: draft
lifecycle_changed: "2026-09-06"
tier: supporting
---

# Morphing Sheets Out of Buttons in SwiftUI

来源：[serialcoder.dev/swiftui/morphing-sheets-out-of-buttons-in-swiftui](https://serialcoder.dev/?p=18226)
作者：SerialCoder.dev（独立 iOS 开发者博客，专注 SwiftUI 高级技术）

## 核心 API

iOS 18+ 引入 `matchedTransitionSource`（iOS 26 强化）：

```swift
@Namespace private var namespace
@State private var showSheet = false

// 源：toolbar 按钮
ToolbarItem(placement: .topBarTrailing) {
    Button {
        showSheet = true
    } label: {
        Image(systemName: "gear")
    }
    .matchedTransitionSource(id: "settingsSheet", in: namespace)
}

// 目标：sheet
.sheet(isPresented: $showSheet) {
    SettingsView()
        .navigationTransition(.zoom(sourceID: "settingsSheet", in: namespace))
}
```

**`id` 和 `namespace` 必须在源和目标间精确匹配**，否则 fallback 到普通 sheet 过渡。

## 关键技巧

1. **id 必须唯一**——同一视图多个 matchedTransitionSource 用不同 id
2. **`@Namespace` 用 `@State`** 或局部 `@Namespace` 修饰符
3. **目标 sheet 推荐自己包 `NavigationStack`** —— 让 `.navigationTransition` 在 sheet root 生效
4. **iOS 26 改进**：`matchedTransitionSource` 可直接挂在 `ToolbarContent` 上，无需包 view
5. **可与 `toolbar(id:)` 配合** —— morphing 工具栏按钮本身就是 toolbar item

## 何时用 vs 不用

| 场景 | 推荐 |
|------|------|
| toolbar 按钮触发 sheet，且 sheet 内容与按钮上下文相关 | ✅ matchedTransitionSource + zoom |
| sheet 是模态大表单（与触发器无关）| 普通 `.sheet` |
| toolbar 按钮触发 NavigationLink push | 用 NavigationStack 内置 push transition |
| 触发器是非 toolbar 元素（如 List row tap）| 同样适用，机制与 toolbar 无关 |

## iOS 26 vs iOS 18 差异

| 维度 | iOS 18 | iOS 26 |
|------|--------|--------|
| `matchedTransitionSource` 在 ToolbarContent 上 | ❌ | ✅ |
| 与 `toolbar(id:)` morphing 配合 | ❌ | ✅ |
| 与 Liquid Glass 视觉连贯 | ❌ | ✅ |
| `navigationTransition(.zoom)` 自动反向（dismiss 也 zoom） | 部分 | ✅ 完整 |

## Open Questions

1. iOS 26 是否对 `navigationTransition` 提供更细粒度动画曲线控制？^[ambiguous]
2. 多 sheet 同时 triggered 的 race condition？^[ambiguous]

## 相关页面

- [[references/swiftui-ios26-toolbar-transitions-morphing]] — iOS 26 toolbar 4 API 主题
- [[concepts/swiftui-toolbaritem-placement-semantic-vs-positional]] — placement 语义
- [[concepts/swiftui-animatablemodifier-pattern]] — 自定义动画 modifier