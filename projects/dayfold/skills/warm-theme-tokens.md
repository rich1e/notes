---
title: 暖色主题色与字体
category: project
tags: [ios, swiftui, ux]
relationships:
  - target: "[[concepts/swiftui-framework]]"
    type: uses
sources: [projects/dayfold]
summary: >-
  Color.warmPaper/Cream/Light/Brown/Accent/Gray/Dark 与 Font.warmTitle/Headline/Body/Caption/Footnote
  组成项目的视觉 token 体系；.warmCard() modifier 统一卡片样式。
provenance:
  extracted: 0.85
  inferred: 0.10
  ambiguous: 0.05
base_confidence: 0.85
lifecycle: draft
lifecycle_changed: 2026-06-29
tier: supporting
created: 2026-06-29T00:00:00Z
updated: 2026-06-29T00:00:00Z
---

# 暖色主题色与字体

## 调色板

文件：`dayfold/dayfold/Extensions/Color+Warm.swift`

```swift
extension Color {
    static let warmPaper  = Color(red: 0.97, green: 0.95, blue: 0.92)  // 主背景米色
    static let warmCream  = Color(red: 0.99, green: 0.97, blue: 0.94)  // 卡片底
    static let warmLight  = Color(red: 0.96, green: 0.93, blue: 0.88)
    static let warmBrown  = Color(red: 0.45, green: 0.38, blue: 0.30)  // 主文字棕
    static let warmAccent = Color(red: 0.85, green: 0.50, blue: 0.30)  // 强调橙
    static let warmGray   = Color(red: 0.65, green: 0.62, blue: 0.58)
    static let warmDark   = Color(red: 0.30, green: 0.27, blue: 0.23)
}
```

## 字体阶梯

文件：`dayfold/dayfold/Extensions/Font+Warm.swift`

| Token | 用途 |
| --- | --- |
| `warmTitle` | 大标题（日记本名） |
| `warmHeadline` | 节标题（月份名） |
| `warmBody` | 正文 |
| `warmCaption` | 元信息（时间 / 位置 / 天气） |
| `warmFootnote` | 脚注 / 副标题 |

## 卡片样式

文件：`dayfold/dayfold/Extensions/View+Extensions.swift`

```swift
extension View {
    func warmCard() -> some View {
        self
            .background(Color.warmCream)
            .cornerRadius(12)
            .shadow(color: Color.black.opacity(0.04), radius: 6, x: 0, y: 2)
    }
}
```

## 副标题组合的"分隔符颜色"

`NotebookDetailView.subtitleView` 用 `Text(" · ")` 拼接「HH:mm · 坐标 · 天气」，
分隔符单独用 `Color(hex: "5A5A68")`（更暗的灰），与字段本身的 `8A8A98` 区分开。

## 编辑器与列表的"双主题" ^[inferred]

- 列表 / 详情 / 日历视图：暖色（`warmPaper` 米色背景 + 棕色文字）。
- 笔记本详情 / 编辑器：暗黑（`Color(hex: "2A2A30")` 背景 + 白色文字）。
- 这种"主页面暖色 + 创作面暗黑"的设计对应"日常浏览 vs. 沉浸写作"的两种心境，
  是项目视觉语言的一部分。改主题时务必分别测试。

## 相关

- [[concepts/swiftui-framework]] — SwiftUI 声明式 UI 框架核心：View 协议、ViewBuilder tuple 组合、`some View` 不透明类型、布局容器、状态管理、修饰符
