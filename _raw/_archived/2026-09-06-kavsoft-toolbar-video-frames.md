---
title: "_raw — Kavsoft iOS 26 Keyboard Toolbar 视频元数据 + 抽帧笔记"
category: raw
tags:
  - youtube
  - raw
  - kavsoft
  - swiftui
sources:
  - "https://www.youtube.com/watch?v=W30FV6QBTok"
created: "2026-09-06T14:35:00Z"
updated: "2026-09-06T14:35:00Z"
summary: "Kavsoft 视频原始资料：metadata + 5 帧代码转录快照，供 references/kavsoft-swiftui-custom-keyboard-toolbar.md 蒸馏溯源。"
---

# _raw — Kavsoft iOS 26 Keyboard Toolbar

## 视频元数据

- **标题**：iOS 26 Custom Animated Keyboard ToolBar Using SwiftUI | Expandable Toolbar | Custom Keyboard Toolbar
- **频道**：Kavsoft (5.59 万订阅)
- **时长**：440.541 sec (7:20)
- **发布日期**：4 个月前 (2026-05 区间)
- **观看次数**：3522
- **点赞**：101
- **评论**：8
- **Tags (YouTube)**：swiftui, kavsoft, Xcode, iOS 26, apple, ui, ux, ui design, apple animations, apple Design, apple notes app toolbar, swiftui custom toolbar, swiftui custom bottom bar, swiftui expandable bottom bar
- **Categories**：Education
- **系列**：SwiftUI 7.0 Tutorials | WWDC 2025 (102 个视频 playlist)
- **字幕**：无 VTT 字幕轨（fabric/yt-dlp 均失败）；视频内嵌英语字幕气泡

## 演示项目

- **项目名**：CustomTFT
- **Source code**：Patreon 付费（https://www.patreon.com/posts/ios-26-custom-156302807）

## 抽帧时间线

| Timestamp | 帧文件 | 内容 |
|-----------|--------|------|
| 0:00 | `assets/kavsoft-toolbar-thumb.png` | 缩略图：标题卡 + iPhone Notes 风格演示 |
| 1:00 | `assets/kavsoft-toolbar-1min.png` | 标准 `.toolbar` 写法起点（NavigationStack + ToolbarItem） |
| 2:00 | `assets/kavsoft-toolbar-2min.png` | 问题陈述（字幕气泡）+ ContentView.swift 起始 |
| 4:10 | `assets/kavsoft-toolbar-4min10s.png` | `ExpandableGlassMenu<Content, Label>: View, Animatable` 组件实现 |
| 6:00 | `assets/kavsoft-toolbar-6min.png` | 最终 ContentView：safeAreaInset + BaseActions + 触发器 Button |

## 蒸馏产物**

`references/kavsoft-swiftui-custom-keyboard-toolbar.md`

## 蒸馏备注

- **字幕提取方式**：chrome 浏览器 `video.currentTime = N` 跳帧 + screenshot 抓取文字气泡
- **代码片段可信度**：高—— Kavsoft 教程代码完整且与视频同步打字演示，未出现截断
- **代码风格**：标准 SwiftUI 6 / iOS 26，使用 `.buttonStyle(.glass)`、`.buttonBorderShape(.circle)`、`.toolbarTitleDisplayMode(.inlineLarge)` 等 iOS 26 新 API
- **未蒸馏部分**：Background Action 段（行 80-93）的细节实现（BaseActions 函数体内）— 因视频帧未覆盖，不强行补全