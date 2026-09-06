---
title: "SwiftUI ToolbarItemPlacement —— 语义 vs 位置 placement 全解"
category: concepts
tags:
  - swiftui
  - toolbar
  - placement
  - ios-26
  - ux
  - toolbarcontentbuilder
sources:
  - "https://developer.apple.com/documentation/swiftui/toolbaritemplacement"
  - "https://developer.apple.com/documentation/swiftui/toolbarcontentbuilder"
  - "https://developer.apple.com/documentation/swiftui/toolbars"
created: "2026-09-06T16:00:00Z"
updated: "2026-09-06T16:00:00Z"
summary: "Apple ToolbarItemPlacement 枚举的语义 vs 位置双层体系：semantic（让系统决定位置）与 positional（明确指定位置），iOS 26 语义 placement 由系统结合平台约定动态决定。"
base_confidence: 0.78
lifecycle: draft
lifecycle_changed: "2026-09-06"
tier: supporting
provenance:
  extracted: 0.75
  inferred: 0.20
  ambiguous: 0.05
---

# SwiftUI ToolbarItemPlacement

## Context

iOS 26 工具栏 API 包含两组 placement：
1. **Semantic** — 系统根据上下文自动决定位置（推荐）
2. **Positional** — 显式指定锚点（兼容/特殊场景）

## Finding

### Semantic placements（系统决定）

| Placement | 用途 | 视觉位置 |
|-----------|------|----------|
| `.automatic` | 默认（系统选最佳位置）| 上下文相关 |
| `.principal` | 主标题区中央 | NavigationBar 中央 |
| `.status` | 状态指示 | 状态栏附近 |
| `.primaryAction` | 主要操作（如 Compose）| 显眼位置 |
| `.secondaryAction` | 次要操作 | 折叠/次要区 |
| `.confirmationAction` | 确认操作（Save / Done）| 显眼 + `glassProminent` style |
| `.cancellationAction` | 取消操作（Cancel）| 显眼 + standard glass |
| `.destructiveAction` | 破坏性操作（Delete）| 红色警示 |
| `.navigation` | 导航操作（back/forward）| leading 区域 |

### Positional placements（明确位置）

| Placement | 位置 |
|-----------|------|
| `.topBarLeading` / `.topBarTrailing` | NavigationBar 左右 |
| `.bottomBar` | 屏幕底栏（iPhone navigation bar 等价） |
| `.bottomOrnament` | Vision Pro 装饰栏 |
| `.keyboard` | 键盘上方 |
| `.largeTitle` / `.title` / `.largeSubtitle` / `.subtitle` | Navigation title 区 |

## iOS 26 关键变化

- **`.bottomBar` + `.glassEffect`** 是 Liquid Glass 设计语言的核心入口（参考 [[references/swiftui-ios26-toolbar-transitions-morphing]]）
- **`ToolbarSpacer`**（`fixed` / `flexible`）—— iOS 26 新增，隔离相同 placement 内的按钮
- **`DefaultToolbarItem(kind: .search, placement: .bottomBar)`** —— 让搜索框成为工具栏成员而非顶部独立元素
- **`toolbar(id:)`** —— 给工具栏项分配稳定 ID，跨屏 morph 时不"跳"

## 何时用 semantic vs positional

- **首选 semantic**：让系统在 NavigationStack/TabView/sheet 不同上下文里自动适配
- **必要时 positional**：toolbar 必须严格放底部（`.bottomBar`），或者需要与其他 placement 视觉对齐
- **`keyboard` placement** 是 iOS 17+ keyboard toolbar 的关键（参考 [[concepts/swiftui-keyboard-toolbar-safeareainset-pattern]] 中相关讨论）

## Open Questions

1. iOS 26 是否新增了 placement 值（如 `.bottomBarOverlay`、liquid-glass specific）？Apple 文档需核对。^[ambiguous]
2. `.bottomOrnament` 在 iPhone 是否有效（visionOS 专属）？^[ambiguous]

## 相关页面

- [[references/swiftui-ios26-toolbar-transitions-morphing]] — iOS 26 toolbar 4 大新 API
- [[references/kavsoft-swiftui-custom-keyboard-toolbar]] — `.bottomBar` + Liquid Glass 实战
- [[references/daniill12321-customtoolbar-ios26-package]] — `.safeAreaBar` 与 `.bottomBar` 关系
- [[concepts/swiftui-keyboard-toolbar-safeareainset-pattern]] — `.keyboard` placement 主题