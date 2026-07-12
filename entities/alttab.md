---
title: AltTab — macOS 窗口切换器
category: entities
tags: [macos, tools, productivity]
summary: 开源 macOS 窗口切换器（lwouis 出品），免费版已覆盖核心需求，Pro 解锁多组快捷键与高级功能；兼容 macOS 10.13+，支持 21 种语言。
sources:
  - https://alt-tab.app/zh-cn/features
created: 2026-07-07
updated: 2026-07-07
tier: peripheral
lifecycle: draft
lifecycle_changed: "2026-07-07"
base_confidence: 0.55
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

# AltTab

## 定位

[lwouis](https://github.com/lwouis) 出品的开源 macOS 窗口切换器。理念：把 Windows 的 `Alt+Tab` 体验带到 macOS，覆盖到所有窗口、标签、菜单栏 app 的窗口。

## 核心特性

- **悬停原始大小预览**：鼠标停在缩略图上，**最上层**以原始大小展示所选窗口，无需猜测
- **即松即切 / 保持打开**：松开快捷键即切换 vs 保持面板可继续浏览，不同快捷键可分别设置
- **状态徽章**：最小化/隐藏/其他 Space 用红绿灯图标标识，可直接在切换器内关闭/最小化/全屏
- **多组快捷键**：Pro 最多 9 组独立快捷键，每组可按 app、Space、屏幕分别过滤
- **触控板手势**：滑动浏览窗口
- **例外规则**：隐藏虚拟机/远程桌面/特定子窗口
- **辅助功能**：VoiceOver、粘滞键、降低透明度全支持
- **隐私**：无遥测、无追踪；网络访问仅用于更新检查与可选崩溃报告
- **21 种语言本地化**（含简繁中文、日韩、阿拉伯、希伯来、泰语等）

## 命令行

```
AltTab --list                              # JSON 列出窗口（ID + 标题）
AltTab --detailed-list                     # JSON 列出窗口（详细信息）
AltTab --show=shortcut_index               # 触发第 N 组快捷键
AltTab --focus=window_id                   # 按 ID 聚焦窗口
AltTab --focusUsingLastFocusOrder=order    # 按上次聚焦顺序聚焦
```

`.app` 包内执行；AltTab 必须在运行中以维护窗口状态。

## 兼容性

macOS 10.13 High Sierra → 最新，Intel 与 Apple Silicon 原生。

## 商业

免费版已覆盖核心需求；Pro 解锁 9 组独立快捷键等高级功能。

相关：[[concepts/macos-window-switcher]]、[[references/macos-window-switchers]]
