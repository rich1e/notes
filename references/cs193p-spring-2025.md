---
title: Stanford CS193P Spring 2025 — iOS App Development
category: references
tags: [ios, swift, swiftui, education, stanford]
sources:
  - "https://www.youtube.com/watch?v=kCjDulwChRQ"
created: 2026-07-10T14:30:00Z
updated: 2026-07-10T14:30:00Z
summary: Stanford CS193P Spring 2025 课程参考：Paul Hegarty 主讲，6周叙事式 App 开发 + 5次作业 + 3周自选项目，SwiftUI 协议导向编程核心课程。
base_confidence: 0.83
lifecycle: reviewed
lifecycle_changed: "2026-08-12"
lifecycle_reason: "auto-promoted by wiki-lint --consolidate: age>30d, confidence>0.7"
tier: core
provenance:
  extracted: 0.80
  inferred: 0.15
  ambiguous: 0.05
relationships:
  - target: "[[concepts/swiftui-framework]]"
    type: related_to
  - target: "[[concepts/swift-fundamentals]]"
    type: related_to
  - target: "[[skills/xcode-ide-guide]]"
    type: related_to
---

# Stanford CS193P Spring 2025 — iOS App Development

CS193P 是 Stanford 大学由 **Paul Hegarty** 主讲的 iOS 开发课程，Spring 2025 版基于 **SwiftUI + Swift** 开发 iPhone/iPad/macOS App。

课程公开在 YouTube，是学习 SwiftUI 最权威的免费资源之一。

## 课程定位

- **目标平台**：iPhone / iPad / macOS（Apple silicon）
- **语言**：Swift（函数式 + 协议导向，非 OOP）
- **框架**：SwiftUI（全面采用，不教 UIKit）
- **前置要求**：有较多编程经验（能写有一定规模的代码）、熟悉多种语言；**不要求** Swift 或 iOS 背景

> "Swift 不是面向对象语言——是函数式 + 协议导向。如果你来自 Java/Python，需要转变思维模型。" — Paul Hegarty, Lecture 1 ^[extracted]

## 课程结构

### 学习方式：双轨并行

| 轨道 | 形式 | 目的 |
|---|---|---|
| **Narrative（叙事）轨** | 6周内一起搭建一个完整 App | 理解各部分如何协同工作 |
| **Vignette（小品）轨** | 独立主题深度讲解 | 掌握特定技术细节 |

Paul Hegarty 认为两者结合才能最有效地学习新框架：先跟着叙事理解全局，再通过 vignette 深挖细节。^[extracted]

### 时间线

| 阶段 | 时长 | 内容 |
|---|---|---|
| Narrative App 开发 | 第 1–6 周 | 跟着课程搭建同一个 App，逐步扩展功能 |
| 个人自选项目 | 最后 3 周 | 学生自选主题，可组队（≤ 2 人，有条件） |

### 作业

5 次编程作业（Programming Assignments），**顺序依赖**：每次作业建立在上一次基础上，必须按时完成否则难以跟上进度。

## Lecture 1 核心要点

### Swift 与 SwiftUI 的关系

```
struct ContentView: View {    // struct 实现 View 协议
    var body: some View {     // some View = 不透明类型，编译器推断
        Text("Hello")
    }
}
```

- **`View` 是协议**，不是基类。遵从它意味着"我有一个 `body` 属性"
- 遵从 `View` 后，编译器自动提供数百个内置函数（modifier、layout 方法等）
- **`some View`**：不透明返回类型，调用者只知道返回某种 View，具体类型由编译器决定

### ViewBuilder

SwiftUI 的多视图组合机制：

- `body` 闭包被 `@ViewBuilder` 标注，可包含多个视图表达式
- 多个 View 被打包成 `TupleView`（"bag of Lego"）
- 最多 10 个直接子 View；超出需用 `Group`

### 尾随闭包

SwiftUI 布局 API 的语法糖，使嵌套视图看起来像声明式标记：

```swift
VStack {        // 最后一个参数是 @ViewBuilder 闭包，可写在括号外
    Text("A")
    Text("B")
}
```

## 学习建议（来自 Lecture 1）

1. **不要死记语法**——理解概念，语法查文档
2. **边看边在 Xcode 里动手**——Preview Canvas 给即时反馈
3. **用 vignette 深挖感兴趣的主题**——不要跳过，它们补充叙事中没时间展开的细节
4. **作业要按时做**——顺序依赖，拖延会导致雪球效应

## 相关资源

- YouTube 播放列表：CS193P Spring 2025（搜索 "CS193P Paul Hegarty 2025"）
- 官方课程页：`cs193p.sites.stanford.edu`
- [[synthesis/ios17-app-development-book × cs193p-spring-2025]] — Stanford 课程与入门书的互补覆盖结构

## 关联页面

- [[concepts/swiftui-framework]] — ViewBuilder / `some View` / 状态管理完整参考
- [[concepts/swift-fundamentals]] — Swift 语言基础（POP / struct / 闭包）
- [[skills/xcode-ide-guide]] — Preview Canvas 最佳实践
- [[entities/ios17-app-development-book]] — 配套书籍参考
- [[concepts/ios-app-architecture]] — MVC/MVVM 在 iOS 中的实践
