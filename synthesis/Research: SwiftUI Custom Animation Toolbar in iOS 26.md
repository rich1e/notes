---
title: "Research: SwiftUI Custom Animation Toolbar in iOS 26"
category: synthesis
tags:
  - swiftui
  - ios-26
  - toolbar
  - animation
  - animatable
  - research
sources:
  - "[[references/kavsoft-swiftui-custom-keyboard-toolbar]]"
  - "[[references/daniill12321-customtoolbar-ios26-package]]"
  - "[[references/swiftui-ios26-toolbar-transitions-morphing]]"
  - "[[references/volcengine-swiftui-keyboard-toolbar-zstack-offset]]"
  - "[[references/apple-developer-animatablmodifier-docs]]"
  - "[[references/swiftui-toolbar-zoom-transition-serialcoder]]"
  - "[[references/fatbobman-swiftui-rich-text-layout]]"
created: "2026-09-06T16:00:00Z"
updated: "2026-09-06T16:00:00Z"
summary: "3 轮研究综合：iOS 26 SwiftUI 自定义动画工具栏，5 个核心子主题（AnimatableModifier / ToolbarItemPlacement / matchedTransitionSource / Liquid Glass 动画 / 性能 Profile）。"
provenance:
  extracted: 0.70
  inferred: 0.22
  ambiguous: 0.08
base_confidence: 0.80
lifecycle: draft
lifecycle_changed: "2026-09-06"
tier: core
---

# Research: SwiftUI Custom Animation Toolbar in iOS 26

## Overview

3 轮研究覆盖 iOS 26 SwiftUI 工具栏自定义动画的 5 个核心子主题：(1) AnimatableModifier 协议用于 modifier 内部状态插值；(2) ToolbarItemPlacement 的 semantic vs positional 双层；(3) matchedTransitionSource + navigationTransition(.zoom) 实现 toolbar 按钮 → sheet 的放大过渡；(4) Liquid Glass 工具栏视觉与 glassEffect API；(5) 120Hz ProMotion 性能 Profile。

**核心命题** —— iOS 26 工具栏动画已形成 **3 层架构**：(a) 协议层 `Animatable`/`AnimatableModifier`；(b) 系统层 `ToolbarItemPlacement` / `toolbar(id:)` / `DefaultToolbarItem`；(c) 视觉层 `Liquid Glass` + `matchedTransitionSource`。vault 既有 cluster (Kavsoft / hasanalidev / DaniilL12321) 是 (a)(c) 两层已落地的实战案例。

## Key Findings

- **`AnimatableModifier` 是 toolbar 弹跳/进度类动画的基石** —— vault 既有 `ExpandableGlassMenu`（Kavsoft）与 `ScaleModifier`（DaniilL12321）独立设计但同架构，证明该模式是 iOS 16+ 通用方案；iOS 26 通过 `Phase Animator` 进一步降低 `animatableData` 手写成本 ([Apple Docs](https://developer.apple.com/documentation/swiftui/animatablemodifier))
- **ToolbarItemPlacement 双层体系**：semantic 让系统决定位置（推荐），positional 显式指定。iOS 26 新增 `keyboard` 工具栏 placement 与 `ToolbarSpacer`/`DefaultToolbarItem` ([Apple ToolbarItemPlacement](https://developer.apple.com/documentation/swiftui/toolbaritemplacement))
- **`matchedTransitionSource` + `navigationTransition(.zoom)`** —— toolbar 按钮触发 sheet 时可实现放大过渡（从按钮位置展开 sheet），iOS 26 改进：可直接挂 `ToolbarContent`，无需包 view ([Series[SerialCoder.dev](https://serialcoder.dev/?p=18226))
- **Liquid Glass 视觉一致性** —— `.glassEffect(.regular.interactive(), in: .capsule | .circle)` 让任何 View 都能应用 glass 质感，不限于 Button。`ToolbarSpacer(.fixed | .flexible)` 防止 Liquid Glass 按钮"粘连" ([Vault: hasanalidev])
- **120Hz ProMotion 动画 frame budget 严苛** —— 8.33ms/frame，是 60Hz 的一半。"如果动画请求 120fps 但不能维持，可能渲染很差"（Apple ProMotion docs）—— 必须用 `CAFrameRateRange` 提示 + Xcode 26 SwiftUI Instrument 检测 hitches ([johal.in](https://johal.in/optimizing-ios-app-animations-with-core-animation))
- **GPU-friendly 动画属性** —— `opacity`, `scale`, `rotation`, `color` 走 Render Server；`frame`, `padding`, layout-affecting 改动走 layout pass（每帧重算）

## Core Concepts

- [[concepts/swiftui-animatablemodifier-pattern]] — `ViewModifier, Animatable` 协议抽象（vault 提炼自 Apple 官方 + Kavsoft + DaniilL12321 三源）
- [[concepts/swiftui-toolbaritem-placement-semantic-vs-positional]] — Apple ToolbarItemPlacement 双层体系（vault 提炼自 Apple 文档）
- [[concepts/swiftui-keyboard-toolbar-safeareainset-pattern]] — `safeAreaInset` 滚动容器跟随键盘模式
- [[concepts/swiftui-safeareabar-vs-safeareainset-pattern]] — iOS 26 `.safeAreaBar` 非滚动容器模式

## Entities & Tools

- **Kavsoft** —— iOS 26 SwiftUI 动画教学频道（YouTube），其 tutorial 是 vault `ExpandableGlassMenu` 实现的源头
- **Daniil Lobanov (DaniilL12321)** —— iOS 26 SwiftUI demo 仓库作者（189 LOC，5 个 iOS 26 API）
- **Hasan Ali Siseci (hasanalidev)** —— iOS 26 native Toolbar Transitions 文章作者
- **SerialCoder.dev** —— iOS 18+ zoom transition 教程作者
- **Hacking with Swift / Sarunw / SwiftLee** —— AnimatableModifier  教程资源（已纳入 references）

## Contradictions & Open Questions

1. **Animatable vs AnimatableModifier 选型** —— Apple 文档未明示何时选 `View, Animatable`（自绘 view）vs `ViewModifier, Animatable`（复用 modifier）。vault 既有两案例（Kavsoft 是后者，DaniilL12321 也是后者），社区共识倾向于 modifier-only。Apple 是否暗示 `View, Animatable` 正在 deprecate？^[ambiguous]
2. **iOS 26 Liquid Glass 性能** —— 多个 liquid glass 叠加是否影响 120Hz frame budget？Apple 文档未量化 ^[ambiguous]
3. **`matchedTransitionSource` 在 toolbar(id:) morphing 中的稳定性** —— toolbar item ID 变更是否会让 matchedTransitionSource 失效？^[ambiguous]
4. **`.glassEffect` 与 `.buttonStyle(.glass)` 关系** —— vault 既有 Kavsoft 用 `.buttonStyle(.glass)`，DaniilL12321 用 `.glassEffect`。两 API 是平级还是递进？Apple 文档需深查 ^[ambiguous]

## Sources Consulted

| Source | Type | Tier |
|--------|------|------|
| [Apple AnimatableModifier](https://developer.apple.com/documentation/swiftui/animatablemodifier) | Apple docs | core |
| [Apple ToolbarItemPlacement](https://developer.apple.com/documentation/swiftui/toolbaritemplacement) | Apple docs | core |
| [Apple ToolbarContentBuilder](https://developer.apple.com/documentation/swiftui/toolbarcontentbuilder) | Apple docs | supporting |
| [Apple Toolbars](https://developer.apple.com/documentation/swiftui/toolbars) | Apple docs | supporting |
| [SerialCoder Morphing Sheets](https://serialcoder.dev/?p=18226) | Tutorial | supporting |
| [WWDC25 Build SwiftUI views for Liquid Glass](https://developer.apple.com/videos/play/wwdc2025/284/) | Apple WWDC | core |
| [Apple ProMotion Optimization](https://developer.apple.com/documentation/quartzcore/optimizing-iphone-and-ipad-apps-to-support-promotion-displays) | Apple docs | core |
| [Apple Rendering Efficiency](https://msc-kobol-public-prod.apple.com/documentation/xcode/improving-your-app-s-rendering-efficiency) | Apple docs | core |
| [[references/kavsoft-swiftui-custom-keyboard-toolbar]] | Vault | core |
| [[references/daniill12321-customtoolbar-ios26-package]] | Vault | core |
| [[references/swiftui-ios26-toolbar-transitions-morphing]] | Vault | core |
| [[references/volcengine-swiftui-keyboard-toolbar-zstack-offset]] | Vault | supporting (反模式) |
| [[references/apple-developer-animatablmodifier-docs]] | Vault (本轮新增) | supporting |
| [[references/swiftui-toolbar-zoom-transition-serialcoder]] | Vault (本轮新增) | supporting |

## Vault Cluster 矩阵（更新）

| 主题 | 文档 |
|------|------|
| 1. AnimatableModifier 协议 | [[concepts/swiftui-animatablemodifier-pattern]]（本轮新增）|
| 2. ToolbarItemPlacement 双层 | [[concepts/swiftui-toolbaritem-placement-semantic-vs-positional]]（本轮新增）|
| 3. matchedTransitionSource zoom | [[references/swiftui-toolbar-zoom-transition-serialcoder]]（本轮新增）|
| 4. AnimatableModifier Apple 文档 | [[references/apple-developer-animatablmodifier-docs]]（本轮新增）|
| 5. 屏幕间 morph(DefaultToolbarItem) | [[references/swiftui-ios26-toolbar-transitions-morphing]] |
| 6. 可展开工具栏 (ExpandableGlassMenu) | [[references/kavsoft-swiftui-custom-keyboard-toolbar]] |
| 7. 5 API 集中 demo (ScaleModifier + glassEffect) | [[references/daniill12321-customtoolbar-ios26-package]] |
| 8. ZStack 反模式对照 | [[references/volcengine-swiftui-keyboard-toolbar-zstack-offset]] |
| 9. safeAreaBar vs safeAreaInset | [[concepts/swiftui-safeareabar-vs-safeareainset-pattern]] |
| 10. Keyboard safeAreaInset | [[concepts/swiftui-keyboard-toolbar-safeareainset-pattern]] |

**vault iOS 26 toolbar 集群** 现 10 个互链页面 + 1 个 master synthesis，3 层架构（协议/系统/视觉）覆盖完整。

## Strongest Objection

> **测试**：iOS 26 的 Liquid Glass + toolbar morphing + AnimatableModifier 三层组合在大规模 toolbar（10+ items）时，是否仍能维持 60Hz？vault 现有 demo 都是 3-5 items，规模化场景未验证。
>
> 测试方法：构建一个 12-item bottom toolbar 配合 matchedTransitionSource，在 iPhone 16 Pro (ProMotion) + Xcode 26 SwiftUI Instrument 下录制 trace，观察 Long View Body Updates 是否有红色 hitch。

这是 Apple 文档未给答案的可验证问题，vault 既有 cluster 是 good starting point 但不是 ground truth。

## Open Questions

1. `Animatable` (deprecated in favor of `AnimatableModifier`?)—— Apple 文档已分两个 protocol 但未明示 deprecation 路径 ^[ambiguous]
2. iOS 26 Liquid Glass 的渲染成本 —— 多个叠加是否影响 120Hz ^[ambiguous]
3. `toolbar(id:)` 与 `matchedTransitionSource` 配合时是否需要 namespace 共享 ^[ambiguous]
4. `.glassEffect(.regular.interactive(), in:)` 与 `.buttonStyle(.glass)` 的性能差异 ^[ambiguous]

## Related

- [[concepts/swiftui-animatablemodifier-pattern]]
- [[concepts/swiftui-toolbaritem-placement-semantic-vs-positional]]
- [[references/apple-developer-animatablmodifier-docs]]
- [[references/swiftui-toolbar-zoom-transition-serialcoder]]
- [[references/kavsoft-swiftui-custom-keyboard-toolbar]]
- [[references/daniill12321-customtoolbar-ios26-package]]
- [[references/swiftui-ios26-toolbar-transitions-morphing]]
- [[references/volcengine-swiftui-keyboard-toolbar-zstack-offset]]
- [[concepts/swiftui-keyboard-toolbar-safeareainset-pattern]]
- [[concepts/swiftui-safeareabar-vs-safeareainset-pattern]]