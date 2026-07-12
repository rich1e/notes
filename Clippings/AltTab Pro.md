---
title: AltTab Pro
source: https://alt-tab.app/zh-cn/features
author:
  - "[[lwouis]]"
published:
created: 2026-07-07
description: 详尽探索 AltTab 的全部功能——深色模式、窗口预览、键盘快捷键、触控板手势、辅助功能等等。
tags:
  - clippings
  - tools
  - macos
---
## 功能

### 深色模式

![[assets/Clippings/AltTab Pro/IMG-20260707134012245.webp|深色模式]]

AltTab 会自动跟随 macOS 的外观设置。无论浅色还是深色，切换器始终保持原生而精致的观感。

### 在最上层预览所选窗口

将指针悬停在缩略图上，即可在一切内容之上以原始大小查看该窗口。无需任何猜测。

### 即松即切或保持打开

选择 AltTab 的行为方式：松开快捷键即可瞬间切换，或保持面板打开以按自己的节奏浏览窗口。不同快捷键可以有不同的行为。

### 状态徽章与红绿灯图标

一眼看清哪些窗口已最小化、已隐藏，或位于另一个 Space 上。熟悉的红绿灯图标让你直接从切换器关闭、最小化窗口或将其全屏。

### 用任意按键自定义快捷键

几乎可用任意按键组合配置快捷键——修饰键、功能键等等。每个快捷键都能按应用、Space 或屏幕筛选窗口。

借助 Pro，最多可设置 9 组相互独立的快捷键，每组都有自己的触发键和筛选规则。

### 触控板手势

用触控板手势触发 AltTab，享受无需键盘的体验。通过滑动浏览各个窗口，让窗口切换如同切换 Space 一般流畅。

### 用例外规则隐藏特定窗口

正在运行虚拟机、远程桌面，或带有大量子窗口的应用？添加例外规则，将特定应用或窗口类型从切换器中隐藏。让你的窗口列表保持整洁，专注于真正重要的内容。

### 辅助功能

AltTab 完全兼容 VoiceOver、粘滞键以及降低透明度设置。每个元素都为屏幕阅读器做了恰当标注，让人人都能无障碍地切换窗口。

### 兼容性

无论你用的是十年前的 MacBook 还是最新的 Mac，AltTab 都能正常运行。我们支持从 10.13 High Sierra 到最新版本的每一个 macOS 版本，并在 Intel 与 Apple Silicon 上原生运行。

### 隐私

AltTab 尊重你的隐私。没有遥测、没有追踪、不收集数据。应用完全在你的设备上运行。网络访问仅用于检查更新和可选的崩溃报告。

[阅读完整隐私政策 →](https://alt-tab.app/zh-cn/privacy)

### 命令行使用

从命令行控制 AltTab。对.app 程序包内的可执行文件运行以下命令：

```
AltTab --list                              # 以 JSON 列出窗口（ID + 标题）
AltTab --detailed-list                     # 以 JSON 列出窗口（详细信息）
AltTab --show=shortcut_index               # 为某个快捷键显示 AltTab 界面
AltTab --focus=window_id                   # 按 ID 聚焦指定窗口
AltTab --focusUsingLastFocusOrder=order    # 按上次聚焦顺序聚焦
```

AltTab.app 必须处于运行状态，才能跟踪窗口状态并执行命令。

### 本地化

AltTab 提供 21 种语言：

Bahasa Indonesia, Deutsch, English, Español, Français, Italiano, Nederlands, Polski, Português (Brasil), Svenska, Tiếng Việt, Türkçe, Русский, עִבְרִית, العربية, ภาษาไทย, 日本語, 简体中文, 繁體中文, 繁體中文 (香港), 한국어