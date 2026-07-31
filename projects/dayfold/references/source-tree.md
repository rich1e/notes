---

title: Dayfold 源码目录布局
category: project
tags:
  - ios
  - swift
  - swiftui
  - codebase-structure
relationships:
  - target: "[[projects/dayfold/dayfold]]"
    type: related_to
sources: [projects/dayfold]
summary: >-
  dayfold/dayfold/ 下的模块划分：Models / Services / ViewModels / Views
  (Entry / Timeline / Map / Tags / Common) / Extensions，App 入口 dayfoldApp.swift。
provenance:
  extracted: 0.90
  inferred: 0.08
  ambiguous: 0.02
base_confidence: 0.85
lifecycle: draft
lifecycle_changed: 2026-06-29
tier: peripheral
created: 2026-06-29T00:00:00Z
updated: 2026-06-29T00:00:00Z
---

# [[projects/dayfold/dayfold|Dayfold]] 源码目录布局

```
dayfold/
├── AppIcons/                   # 应用图标资源
├── dayfold/                    # 实际 Xcode 工程根目录
│   ├── dayfoldApp.swift        # @main，注入 viewContext，集成 SecurityManager
│   ├── Info.plist
│   ├── dayfold.xcdatamodeld/   # Core Data schema（Entry / MediaAsset / Location / Tag / Notebook）
│   ├── Models/                 # NSManagedObject 扩展 + 工厂方法
│   │   ├── Entry.swift
│   │   ├── Location.swift
│   │   ├── MediaAsset.swift
│   │   └── Tag.swift
│   ├── Services/
│   │   ├── CoreDataStack.swift           # 单例；CloudKit 134400 降级
│   │   ├── MediaService.swift            # 图片读写 + 缩略图 + 路径验证
│   │   ├── LocationService.swift         # @MainActor CLLocationManager
│   │   ├── WeatherService.swift          # WeatherKit 封装
│   │   ├── SecurityManager.swift         # LAContext 锁屏
│   │   └── CardExporter.swift            # 单条日记导出图片
│   ├── ViewModels/             # 全部 @MainActor ObservableObject
│   │   ├── EntryListViewModel.swift
│   │   ├── EntryEditorViewModel.swift
│   │   ├── TimelineViewModel.swift
│   │   ├── MapViewModel.swift
│   │   └── TagManagerViewModel.swift
│   ├── Views/
│   │   ├── MainTabView.swift             # 根容器：抽屉 + 内容区
│   │   ├── SidebarView.swift             # DrawerView + SidebarTab 枚举
│   │   ├── HomeView.swift                # 笔记本封面墙
│   │   ├── NotebookDetailView.swift      # 笔记本时间轴（含 SwipeToDeleteRow）
│   │   ├── LockScreenView.swift          # 生物识别锁屏 UI
│   │   ├── Entry/
│   │   │   ├── EntryListView.swift
│   │   │   ├── EntryDetailView.swift
│   │   │   ├── EntryEditorView.swift     # 沉浸式黑色编辑器
│   │   │   ├── EntryCardPreviewSheet.swift
│   │   │   ├── TrashView.swift           # 回收箱
│   │   │   └── Components/               # EntryCard / MediaPicker / TagPicker / MarkdownEditor / FormattingToolbar
│   │   ├── Timeline/                     # TimelineView / TimelineListView / CalendarView / MonthGridView / EntryBottomSheet / PhotoWallView
│   │   ├── Map/                          # MapView / MapKitView / MapSearchBar / MapEntryCard / EntryAnnotation
│   │   ├── Tags/                         # TagsView / TagEditorView
│   │   └── Common/                       # EntryHeader / MediaGrid / WarmCardView
│   └── Extensions/             # Color+Warm / Font+Warm / Transitions+Warm / View+Extensions
├── docs/                       # 设计文档 / 实施进度 / Core Data 设置 / 已知日志
│   ├── IMPLEMENTATION_PROGRESS.md
│   ├── XCODE_COREDATA_SETUP.md
│   ├── XCODE_KNOWN_LOGS.md
│   └── superpowers/{plans,specs}/
├── scripts/
├── README.md
├── CLAUDE.md
├── CURRENT_PROGRESS.md
└── NEXT_STEPS.md
```

## 模块职责

| 目录 | 职责 |
| --- | --- |
| `Models/` | `NSManagedObject` 子类扩展 + 工厂方法（`create` / `moveToTrash` / `restore`），不持有 UI 状态 |
| `Services/` | 全局单例 / 跨 View 共享能力（Core Data / 媒体 / 位置 / 天气 / 锁屏） |
| `ViewModels/` | 表单状态、列表过滤、auto-save、地图 / 日历数据；只通过 `@Published` 与 View 通信 |
| `Views/Entry/` | 日记核心 CRUD 与回收箱；`Components/` 是被多个 Entry 视图复用的子组件 |
| `Views/Timeline/` | 时间轴 4 种浏览：时间轴列表 / 月历 / 照片墙 / 底部抽屉 |
| `Views/Map/` | MapKit 全局地图，搜索 + 聚合 + 底部选择卡 |
| `Views/Tags/` | 标签管理（CRUD） |
| `Views/Common/` | 跨 Entry / Timeline 复用的 UI 组件（EntryHeader / MediaGrid） |
| `Extensions/` | 全局设计 token 与视图修饰符 |

## 数据流入口

- `dayfoldApp.swift` 注入 `\.managedObjectContext` + `SecurityManager` 环境对象。
- `MainTabView` 是普通用户能看到的第一个完整 UI（解锁后），包含所有主要导航。
- `LockScreenView` 只在 `SecurityManager.isLocked == true` 时显示。

## 文档位置

- `CLAUDE.md`：项目记忆（commit 规范、构建命令、架构概览、关键设计约定、已知可忽略日志）。
- `docs/XCODE_KNOWN_LOGS.md`：SourceKit 误报、CloudKit 134400、键盘辅助栏约束冲突等可忽略日志。
- `docs/superpowers/specs/`：设计规格。
- `docs/superpowers/plans/`：实施计划。
