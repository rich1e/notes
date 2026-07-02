---
title: Dayfold
category: project
tags: [ios, swiftui, core-data, cloudkit, weatherkit, personal, architecture]
sources: [projects/dayfold]
summary: >-
  暖色风格的 iOS 个人日记 App，MVVM + SwiftUI + Core Data/CloudKit；抽屉式导航，自定义
  暖色主题与多视图浏览（时间轴/相册/地图/日历/照片墙）。
provenance:
  extracted: 0.55
  inferred: 0.40
  ambiguous: 0.05
base_confidence: 0.78
lifecycle: draft
lifecycle_changed: 2026-06-29
tier: core
created: 2026-06-29T00:00:00Z
updated: 2026-06-29T00:00:00Z
---

# Dayfold

iOS 18.1+ 个人日记应用，专注"温暖文艺"的写作与回顾体验。SwiftUI 全栈，Core Data +
CloudKit 同步，无 iCloud 账号自动降级为纯本地存储。Bundle ID `com.Yuqi.dayfold`，iCloud
Container `iCloud.com.Yuqi.dayfold`。

## 关键概念

- [[projects/dayfold/concepts/architecture-overview]] — 抽屉式导航 + MVVM 分层 + 共享
  `CoreDataStack` 单例的数据流。
- [[projects/dayfold/concepts/core-data-cloudkit-fallback]] — `NSPersistentCloudKitContainer`
  134400 降级本地的实现细节。
- [[projects/dayfold/concepts/swiftui-context-propagation]] — sheet / fullScreenCover 内
  `.environment(\.managedObjectContext, context)` 必须显式注入。
- [[projects/dayfold/concepts/fetchrequest-vs-observedobject]] — 列表与行内属性变化的不同刷
  新机制。
- [[projects/dayfold/concepts/drawer-architecture]] — `MainTabView` 用 85% 屏宽抽屉而非
  TabBar，`ZStack` 偏移 + `spring(0.38, 0.82)`。

## 模式与技巧

- [[projects/dayfold/skills/entry-editor-image-dirty-tracking]] — `imagesChanged` 脏标记
  控制 MediaAsset 全量重建，避免无操作误删。
- [[projects/dayfold/skills/soft-delete-with-trash]] — 软删除字段 `deletedAt` + FetchRequest
  predicate 隔离回收箱数据。
- [[projects/dayfold/skills/warm-theme-tokens]] — 暖色主题色与字体的统一抽象
  （`Color.warmPaper` / `Font.warmHeadline` / `.warmCard()`）。
- [[projects/dayfold/skills/swipe-to-delete-row]] — 自定义手势 + 速度阈值 + 角落圆角并入
  的左滑删除容器。

## 引用

- [[projects/dayfold/references/source-tree]] — 当前源码目录布局与各模块职责。
