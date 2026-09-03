---
title: Dayfold
category: project
tags:
  - ios
  - swiftui
  - core-data
  - cloudkit
  - weatherkit
sources: [projects/dayfold]
summary: >-
  暖色风格的 iOS 个人日记 App，MVVM + SwiftUI + Core Data/CloudKit；抽屉式导航，自定义
  暖色主题与多视图浏览（时间轴/相册/地图/日历/照片墙）。
provenance:
  extracted: 0.55
  inferred: 0.40
  ambiguous: 0.05
base_confidence: 0.78
lifecycle: reviewed
lifecycle_changed: 2026-08-03
lifecycle_reason: "auto-promoted by wiki-lint --consolidate: age>30d, confidence>0.7"
tier: core
created: 2026-06-29T00:00:00Z
updated: 2026-08-03T05:47:33Z
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
- [[projects/dayfold/skills/uitextview-intrinsic-width-overflow]] — 图文混排编辑器：非滚动
  UITextView 把被超宽 attachment 撑大的 contentSize 报成 intrinsic 宽度，撑宽整个 SwiftUI 层级；
  须 override `intrinsicContentSize` 锁死横向。
- [[projects/dayfold/skills/nstextattachment-bounds-overflow]] — 同根因的上游修复：
  attachment.bounds.width 超过 textContainer.lineFragmentWidth 触发回行放大，
  须用 `textContainer.size.width` 而非 `bounds.width` 算 attachment 目标尺寸。
- [[projects/dayfold/skills/swiftui-editor-scrollview-vs-attachment]] — 图文混排下
  `ScrollViewReader.scrollTo(anchor: .bottom)` 把标题与历史图片推出屏幕顶部的反行为；
  改由内层 UITextView 自管 caret 可见性即可。
- [[projects/dayfold/skills/dayone-photo-library-picker]] — 自研 Photos 框架深色多选选择器：
  PHCachingImageManager 组级视口预热 + ≤2048px 选择器内降采样。
- [[projects/dayfold/skills/simulator-runtime-log-capture]] — 模拟器运行时日志抓取
  （`simctl launch --console-pty`）与"代码是否真在跑"的验证纪律。

## 设计系统（Stitch）

- [[projects/dayfold/references/stitch-design-system]] — Google Stitch 设计系统资产索引（Project ID、Asset ID、已生成屏幕目录、本地文件布局）。

Stitch Design System Asset ID：`assets/4b1bee32e3894e98a837dda03816a473`

已生成屏幕：
- **Home Screen**（`ce330a7e2e21401aaf0a59d56b99575d`）— 3D 笔记本封面定调页面
- **Timeline Home**（`a388af4f3bcb409c96322277639b94d2`）— 主首页，Journal Card + FAB + Tab Bar ★

生成新屏幕时带 `designSystem: "assets/4b1bee32e3894e98a837dda03816a473"` 参数，配色/字体/圆角自动统一。

## 引用

- [[projects/dayfold/references/source-tree]] — 当前源码目录布局与各模块职责。
