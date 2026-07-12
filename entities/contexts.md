---
title: Contexts — macOS 窗口切换器
category: entities
tags: [macos, tools, productivity]
summary: 边栏式 macOS 窗口切换器，自动隐藏边栏按 Space 分组列窗口；触控板边缘滑动 + 多显示器独立边栏；付费，免费试用；macOS Ventura+。
sources:
  - https://contexts.co/
created: 2026-07-07
updated: 2026-07-07
tier: peripheral
lifecycle: draft
lifecycle_changed: "2026-07-07"
base_confidence: 0.48
provenance:
  extracted: 0.90
  inferred: 0.08
  ambiguous: 0.02
relationships:
  - target: "[[concepts/macos-window-switcher]]"
    type: related_to
  - target: "[[references/macos-window-switchers]]"
    type: related_to
---

# Contexts

## 定位

[Contexts](https://contexts.co/) 是一款**边栏式**窗口切换器，区别于经典 Cmd+Tab 风格的弹出面板：

- 一个**自动隐藏的边栏**（类似 Dock）出现在屏幕侧边，按 **Space** 分组列出所有窗口
- 鼠标移到对应项即切换
- 边栏可隐藏直到指针移向屏幕边缘，也可通过"右滑手势"临时调出

## 核心特性

### 边栏模式（与 AltTab/Witch/BetterCmdTab 最大差异）
- 按 Space 分组列窗口
- 角标显示窗口数（和 Dock 一样）
- 临时隐藏 / 永驻模式可切换
- **两指从触控板顶部边缘下滑** 即可唤出边栏，手指上下移动即选择窗口，松开手指 = 切换

### 多显示器
- 中央窗口**默认在所有显示器同时显示**
- 每个显示器可有独立边栏，可设置成只列该显示器上的窗口
- 不再"扭头找切换器"

### 视觉
- 像系统原生组件
- Vibrant Dark 主题与系统深色菜单栏/Dock 协调
- 高对比度配色让窗口列表在浅色内容背景上更易识别

## 系统要求

macOS Ventura、Sonoma、Sequoia（v3.9）。

## 商业

付费软件，提供免费试用。

相关：[[concepts/macos-window-switcher]]、[[references/macos-window-switchers]]
