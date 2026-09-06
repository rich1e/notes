---
title: "Apple Developer Documentation: AnimatableModifier"
category: references
tags:
  - swiftui
  - animation
  - animatable
  - animatablemodifier
  - apple-developer
  - documentation
sources:
  - "https://developer.apple.com/documentation/swiftui/animatablemodifier"
source_url: "https://developer.apple.com/documentation/swiftui/animatablemodifier"
created: "2026-09-06T16:00:00Z"
updated: "2026-09-06T16:00:00Z"
summary: "Apple 官方 AnimatableModifier 协议文档：定义、adoption path、animatableData 要求、与 Animatable 区别。"
affinity:
  ios: 1.0
  swiftui: 1.0
promotion_status: project
provenance:
  extracted: 0.85
  inferred: 0.10
  ambiguous: 0.05
base_confidence: 0.92
lifecycle: draft
lifecycle_changed: "2026-09-06"
tier: supporting
---

# Apple Developer Documentation: AnimatableModifier

来源：[developer.apple.com/documentation/swiftui/animatablemodifier](https://developer.apple.com/documentation/swiftui/animatablemodifier)（Apple 官方）
本地蒸馏：[[concepts/swiftui-animatablemodifier-pattern]] 提炼该文档核心 + 与 vault 既有实现的对照。

## 文档要点（直接摘自 Apple）

`AnimatableModifier`：Animate between different versions of a modifier by using AnimatableModifier to set up animations for when the modifier's...

- 定义：协议是 `ViewModifier` 与 `Animatable` 的复合
- `animatableData` 要求：必须把内部可动画状态暴露
- 典型用法：弹跳按钮、路径动画、进度条

## 关键引用（Apple 原文）

> Animate between different versions of a modifier by using AnimatableModifier to set up animations for when the modifier's data changes.

## 与 vault 既有实现的对照

| Apple 文档示例 | vault 实战 |
|--------------|-----------|
| 通用 AnimatableModifier 模板 | `ExpandableGlassMenu` ([[references/kavsoft-swiftui-custom-keyboard-toolbar]]):用 `progress: CGFloat` 0→1 插值 |
| | `ScaleModifier` ([[references/daniill12321-customtoolbar-ios26-package]]):用 `bounce: CGFloat` 三角波循环 |

vault 既有 cluster 是该协议的"实战教科书"，vault 用户在读 Apple 文档时应优先参考这两个仓库的具体实现。

## 限制与文档盲区

- Apple 文档未详细说明 **`animatableData` 是否支持多字段 struct**（如 `struct { scale, rotation, opacity }`）^[ambiguous]
- iOS 26 新增 `Phase Animator` 与 `AnimatableModifier` 的关系文档未细说 ^[ambiguous]
- 性能文档未量化 `animatableData` 字段数 vs frame 耗时关系 ^[ambiguous]

## 相关页面

- [[concepts/swiftui-animatablemodifier-pattern]] — vault 抽象概念页
- [[references/kavsoft-swiftui-custom-keyboard-toolbar]] — 实战案例 1
- [[references/daniill12321-customtoolbar-ios26-package]] — 实战案例 2
- [[references/swiftui-ios26-toolbar-transitions-morphing]] — iOS 26 工具栏上下文