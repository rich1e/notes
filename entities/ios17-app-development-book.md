---
title: iOS 17 App Development for Beginners（书籍）
category: entities
tags: [mobile, swift, swiftui, book, develop]
sources: ["buckets/books/iOS 17 App Development for Beginners.epub"]
created: 2026-07-01T00:00:00Z
updated: 2026-08-03T05:47:33Z
summary: Arpit Kulsreshtha 著，Packt 出版，覆盖 Swift 5.9、SwiftUI、Xcode 15 的 iOS 17 入门开发书，共19章。
base_confidence: 0.83
lifecycle: reviewed
lifecycle_changed: 2026-08-03
lifecycle_reason: "auto-promoted by wiki-lint --consolidate: age>30d, confidence>0.7"
tier: core
provenance:
  extracted: 0.95
  inferred: 0.05
  ambiguous: 0.00
relationships:
  - target: "[[concepts/arc-memory-management]]"
    type: extends
  - target: "[[concepts/swift-concurrency]]"
    type: related_to
  - target: "[[skills/ios-networking]]"
    type: related_to
  - target: "[[skills/ios-multithreading]]"
    type: related_to
  - target: "[[skills/ios-app-store-publishing]]"
    type: extends
  - target: "[[skills/xcode-ide-guide]]"
    type: extends

  - target: "[[references/cs193p-spring-2025]]"
    type: related_to
  - target: "[[synthesis/arc-memory-management × swift-concurrency]]"
    type: related_to
---

# iOS 17 App Development for Beginners

- **作者**：Arpit Kulsreshtha
- **技术栈**：Swift 5.9、SwiftUI、Xcode 15
- **系统要求**：macOS 13 Ventura 或更高；Apple ID；iOS 设备可选

## 章节结构

| 章节 | 主题 |
|---|---|
| Ch1 | [[skills/xcode-ide-guide|Xcode IDE 入门]] |
| Ch2 | [[concepts/swift-fundamentals|Swift 语言基础]] |
| Ch3 | 类、结构体、枚举 |
| Ch4 | 协议、扩展、错误处理 |
| Ch5 | [[concepts/arc-memory-management|ARC 与内存安全]] |
| Ch6 | iOS 17 架构实现 |
| Ch7 | UIKit 用户界面设计 |
| Ch8 | [[concepts/swiftui-framework|SwiftUI 用户界面设计]] |
| Ch9 | [[concepts/swift-concurrency|Swift 并发]] |
| Ch10 | [[skills/ios-data-persistence|SQLite 与 Core Data]] |
| Ch11 | 文件管理（iCloud 同步） |
| Ch12 | Core Location 与 MapKit |
| Ch13 | 相机与照片库 |
| Ch14 | [[skills/ios-multithreading|iOS 多线程]] |
| Ch15 | [[skills/ios-networking|iOS 网络编程]] |
| Ch16 | [[references/ios-design-patterns|架构模式与反模式]] |
| Ch17 | [[skills/ios-app-store-publishing|发布到 App Store]] |
| Ch18 | Xcode Cloud CI/CD |
| Ch19 | 新框架（RealityKit/VisionKit/ActivityKit） |

## 关联页面

- [[concepts/swift-fundamentals]] — Swift 语言核心
- [[concepts/swiftui-framework]] — SwiftUI 框架
- [[concepts/ios-app-architecture]] — iOS 架构模式
- [[projects/dayfold/dayfold]] — 本地 SwiftUI 项目

## 相关

- [[references/cs193p-spring-2025]] — Stanford CS193P Spring 2025 课程参考：Paul Hegarty 主讲，6周叙事式 App 开发 + 5次作业 + 3周自选项目，Sw
- [[synthesis/arc-memory-management × swift-concurrency]] — ARC 解决引用类型的生命周期问题（堆上何时释放），Actor 解决引用类型的并发访问问题（多线程何时安全读写）——两套机制作用在同一类型上但维度正交。
- [[synthesis/ios17-app-development-book × cs193p-spring-2025]] — 书（地图）vs 课（罗盘）：两条 iOS 学习路径
