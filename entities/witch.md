---
title: Witch — macOS 窗口切换器
category: entities
tags: [macos, tools, productivity]
summary: Many Tricks 出品的付费窗口切换器，可同时存在多个切换器（app/window/tab 三种粒度独立）；支持横向/纵向/菜单栏三种布局与搜索式切换；适合 Windows 转 Mac 用户。
sources:
  - https://manytricks.com/witch/
created: 2026-07-07
updated: 2026-07-07
tier: peripheral
lifecycle: draft
lifecycle_changed: "2026-07-07"
base_confidence: 0.50
provenance:
  extracted: 0.92
  inferred: 0.06
  ambiguous: 0.02
relationships:
  - target: "[[concepts/macos-window-switcher]]"
    type: related_to
  - target: "[[references/macos-window-switchers]]"
    type: related_to
  - target: "[[synthesis/macos-window-switcher × macos-window-switchers]]"
    type: related_to
---

# Witch

## 定位

[Many Tricks](https://manytricks.com/) 出品的付费 macOS 窗口切换器（与同公司 Moom 窗口管理器搭配）。**核心卖点：多切换器并存**——可以同时定义 app / window / tab 三种粒度的切换器，各自定义排序、朝向、标签处理，互不干扰。

> "Perfect for Windows switchers to Mac." —— 官方描述

## 核心特性

### 多切换器（区别于竞品）
- 不必三选一，可同时存在多组切换器
- 每个切换器的动作（排序、朝向、标签处理）可独立定制

### 三种布局
- 横向（模拟内置 app 切换器）
- 纵向
- **菜单栏模式** —— 切换器常驻/可选显示在菜单栏

### 搜索式切换
- 启动搜索字段后输入字符，**实时过滤** app/window/tab
- 不再依赖"看到 → 选中"

### 高级功能
- **Spring-loaded**：选中某 app 后，延迟 N 毫秒自动下钻到该 app 的窗口/标签
- **Accessory app 支持**：菜单栏 app（如 Moom 偏好窗口在菜单栏模式下）也能在切换器中显示（内置切换器看不到）
- **作用域控制**：在特定 app 内禁用热键；排除某些 app；隐藏某些窗口（如图像工具的浮动工具面板）
- **快速动作**：H 隐藏、M 最小化等单键动作
- **外观定制**：面板颜色、字体、位置

## 商业

付费软件，Many Tricks 长期维护；提供试用。

相关：[[concepts/macos-window-switcher]]、[[references/macos-window-switchers]]

## 相关

- [[synthesis/macos-window-switcher × macos-window-switchers]] — 概念页和参考表都存在，但真正的综合洞见是：4 个独立开发者在同一时间段、用不同设计取舍解决同一问题——这暗示 macOS 内置 Cmd+Tab 的局限是**结构
