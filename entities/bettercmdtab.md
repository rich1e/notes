---
title: BetterCmdTab — macOS 窗口切换器
category: entities
tags: [macos, tools, productivity]
summary: rokartur 出品的免费开源 Cmd+Tab 替代品，永久免费、零遥测；三种布局（列表/网格/缩略图）+ 模糊搜索 + 标签下钻 + Space 过滤，macOS 13+。
sources:
  - https://bettercmdtab.app/
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
---

# BetterCmdTab

## 定位

[rokartur](https://bettercmdtab.app/) 出品的 macOS Cmd+Tab 替代品，**永久免费、零遥测、无订阅**。安装通过 `brew install --cask bettercmdtab`。

## 核心特性

- **三种布局**：经典列表、app 图标网格、实时窗口缩略图
- **窗口标题**：在网格与缩略图模式下显示每个窗口的标题
- **搜索 & 启动**：按 `/` 进入模糊搜索，可启动任意已装 app
- **窗口循环**：`Cmd+\`` 在当前 app 的窗口间循环
- **多组快捷键**：每个快捷键可预过滤（所有窗口/当前 Space/可见 Space/当前 app/最小化）+ 自己的布局/排序/颜色
- **Tap or Hold**：轻按瞬切，按住则打开切换器
- **Stay open**：松开 Cmd 后切换器保持开启，Return 确认 / Esc 取消
- **标签下钻**：`\` 键挑出 Safari/Chrome/Arc/Finder/Terminal 的标签
- **标签作为行**：原生或浏览器标签各为一行（实验性 MRU 排序）
- **快速动作**：退出/关闭/最小化/最大化/隐藏；hover 出现快速按钮
- **Force quit**：`Cmd+Option+Q` 对挂起 app 发 SIGKILL
- **窗口管理**：`Ctrl+Cmd + 方向键` 平铺到半屏/角落/居中；1/2 → 2/3 → 1/3 循环
- **Spaces 即时切换**（无动画）
- **Dock 角标 + 音频指示器**在切换器中显示
- **Secure-input 存活**：`Cmd+Tab` 在密码框持有 Secure Event Input 时仍可用
- **三指触控板手势**（可选触觉反馈）
- **屏幕共享隐藏**：切换器不出现在录屏/共享屏幕中（macOS 14.6+）
- **Liquid Glass 材质**在 macOS 26 生效
- **配置导入导出**为版本化 `.cmdtab` 文件

## 系统要求

macOS 13.0+，Apple Silicon & Intel，v26.6.1。

## 安装

```bash
brew install --cask bettercmdtab
```

相关：[[concepts/macos-window-switcher]]、[[references/macos-window-switchers]]
