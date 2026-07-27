---
title: macOS 窗口切换器（Window Switcher）
category: concepts
tags: [macos, tools, productivity]
summary: 替代 macOS 内置 Cmd+Tab 的应用/窗口/标签切换工具，核心价值是把"app 粒度"扩展为"window 粒度"，并加入标签下钻、Space 过滤、快速动作等增强。
sources:
  - https://bettercmdtab.app/
  - https://alt-tab.app/zh-cn/features
  - https://contexts.co/
  - https://manytricks.com/witch/
created: 2026-07-07
updated: 2026-07-07
tier: supporting
lifecycle: draft
lifecycle_changed: "2026-07-07"
base_confidence: 0.62
provenance:
  extracted: 0.85
  inferred: 0.13
  ambiguous: 0.02
relationships:
  - target: "[[references/macos-window-switchers]]"
    type: related_to
  - target: "[[entities/alttab]]"
    type: related_to
  - target: "[[entities/bettercmdtab]]"
    type: related_to
  - target: "[[entities/contexts]]"
    type: related_to
  - target: "[[entities/witch]]"
    type: related_to
  - target: "[[synthesis/macos-window-switcher × macos-window-switchers]]"
    type: related_to
---

# macOS 窗口切换器

## 内置 Cmd+Tab 的局限

macOS 自带的 `Cmd+Tab` 是 **app 粒度** 切换器——它只切换应用，不切换同一应用的多个窗口，也看不见标签页。对于多窗口/多标签的工作流（开发、写作、客服、设计），这意味着：

- 同一个 Safari/Chrome 打开 10 个标签 → Cmd+Tab 只能选到浏览器，要切到具体标签还得 ⌘\` 或 ⌘1-9
- 同一应用开了 5 个 Finder 窗口 → 只能从 Dock 选窗口图标
- 最小化/隐藏的窗口从切换器中"消失"，找不到
- 菜单栏 app（系统设置、Hidden Bar 等）的偏好窗口默认不可见

第三方窗口切换器的核心价值：**把 app 粒度扩展为 window 粒度**，并补齐 Space/标签/快速动作等。

## 共同功能集

四款主流工具（AltTab、BetterCmdTab、Contexts、Witch）几乎都提供：

| 功能 | 说明 |
|------|------|
| 窗口级切换 | 不只是 app，每个窗口独立条目 |
| 标签下钻 | Safari/Chrome/Arc/Terminal 的标签可作为独立行 |
| 布局 | 列表（横向/纵向）、网格图标、实时窗口缩略图 |
| 模糊搜索 | 输名字过滤 |
| Space 过滤 | 当前 Space / 所有 Space / 可见 Space / 某显示器 |
| 快速动作 | 关闭/最小化/隐藏/退出/强制退出（部分支持多组快捷键） |
| 例外规则 | 排除某 app 或某类窗口（避免虚拟机/远程桌面刷屏） |
| 多组快捷键 | 不同快捷键打开不同过滤/布局 |
| 无遥测 | 主流工具均不收集数据 |

## 设计差异轴

四款工具在以下维度上各有取舍：

- **价格 / 开源**：AltTab（免费开源，Pro 付费高级版）、BetterCmdTab（永久免费开源）、Contexts（付费，免费试用）、Witch（付费，Many Tricks 出品）
- **触发方式**：默认快捷键 vs 触控板手势 vs 边栏自动弹出（Contexts 独有边栏模式）
- **多显示器**：是否每显示器独立列、缩略图出现在哪
- **macOS 兼容范围**：BetterCmdTab 需 macOS 13+，Contexts 仅 Ventura+，AltTab 兼容 10.13+，Witch 全版本
- **键盘鼠标取舍**：Witch/AltTab 鼠标可用，Contexts 几乎纯鼠标/触控板

## 选择建议

- **想要纯免费 + 简单 + 开源** → BetterCmdTab
- **想要最广 macOS 兼容 + 大量配置项** → AltTab
- **想要边栏常驻 + 触控板流** → Contexts
- **习惯 Windows Alt+Tab 体验** → Witch（按 app/window/tab 多切换器共存，菜单栏模式）

具体对比见 [[references/macos-window-switchers]]。
