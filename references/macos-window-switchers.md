---
title: macOS 窗口切换器对比速查
category: references
tags: [macOS, tools, productivity]
summary: 主流 macOS 窗口切换器横向对比：AltTab / BetterCmdTab / Contexts / Witch 在许可证、macOS 兼容、布局、触发方式与独家特性上的差异。
sources:
  - https://bettercmdtab.app/
  - https://alt-tab.app/zh-cn/features
  - https://contexts.co/
  - https://manytricks.com/witch/
created: 2026-07-07
updated: 2026-07-07
tier: core
lifecycle: draft
lifecycle_changed: "2026-07-07"
base_confidence: 0.60
provenance:
  extracted: 0.88
  inferred: 0.10
  ambiguous: 0.02
relationships:
  - target: "[[concepts/macos-window-switcher]]"
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

# macOS 窗口切换器对比

> 维度取自四款工具官方页面，截至 2026-07。
> 概念背景见 [[concepts/macos-window-switcher]]。

## 概览

| 工具 | 价格 | 开源 | 最低 macOS | Apple Silicon | 触发方式 |
|------|------|------|------------|---------------|----------|
| [[entities/bettercmdtab]] | 永久免费 | ✓ | 13.0 | ✓ | 快捷键 + 三指触控板 |
| [[entities/alttab]] | 免费 + Pro 高级 | ✓ | 10.13 | ✓ | 快捷键 + 触控板手势 |
| [[entities/contexts]] | 付费（有试用） | — | Ventura (13) | ✓ | **边栏自动显示** + 边缘下滑 |
| [[entities/witch]] | 付费 | — | 经典全版本 | ✓ | 多组快捷键 + 菜单栏 |

## 核心能力

| 能力 | BetterCmdTab | AltTab | Contexts | Witch |
|------|--------------|--------|----------|-------|
| 窗口级切换 | ✓ | ✓ | ✓ | ✓ |
| 标签下钻 | ✓ (`\`) | ✓ | — | ✓ |
| 列表布局 | ✓ | ✓ | — | ✓ |
| 网格图标布局 | ✓ | ✓ | — | — |
| 实时窗口缩略图 | ✓ | ✓ | — | — |
| 模糊搜索 | ✓ (`/`) | — | — | ✓ |
| Space 过滤 | ✓ | ✓ | ✓ (按 Space 分组) | — |
| 多组独立快捷键 | ✓ | ✓ (Pro 9 组) | — | ✓ (核心卖点) |
| 例外规则 | ✓ | ✓ | — | ✓ |
| 多显示器独立列 | ✓ | ✓ | ✓ | — |
| 快速动作（关闭/最小化等） | ✓ | ✓ | — | ✓ (单键) |
| Force quit | ✓ | — | — | — |
| Secure-input 存活 | ✓ | — | — | — |
| 屏幕共享隐藏 | ✓ (14.6+) | — | — | — |
| 触控板手势 | ✓ (三指) | ✓ | ✓ (边缘下滑) | — |
| 菜单栏模式 | — | — | — | ✓ |
| Liquid Glass (macOS 26) | ✓ | — | — | — |
| 配置导入导出 | ✓ (.cmdtab) | — | — | — |
| 屏幕阅读器兼容 | — | ✓ | — | — |
| CLI 控制 | — | ✓ | — | — |

## 独家特性

- **BetterCmdTab**：Liquid Glass 材质、`Cmd+\`` 当前 app 窗口循环、Screen Sharing 隐藏、`.cmdtab` 配置迁移
- **AltTab**：悬停**最上层**原始大小预览、21 种语言、CLI (`--focus=window_id`)、Pro 9 组独立快捷键
- **Contexts**：**边栏常驻** + 触控板边缘下滑手势、与 macOS Ventura/Sonoma/Sequoia 原生融合
- **Witch**：**多切换器并存**（app/window/tab 三种粒度同时定义，互不干扰）、菜单栏模式、Spring-loaded 自动下钻

## 选择建议

| 偏好 | 推荐 |
|------|------|
| 永久免费 + 开源 + 简单 | BetterCmdTab |
| macOS 10.13–12 兼容 + 高度可配 | AltTab |
| 边栏常驻 + 触控板手势 | Contexts |
| Windows 转 Mac + 多组粒度切换 | Witch |
| 屏幕阅读器/中文等本地化 | AltTab |
| 多显示器 + 每显示器独立列 | Contexts / BetterCmdTab |
