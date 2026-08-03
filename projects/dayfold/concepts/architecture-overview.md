---

title: Dayfold 架构概览
category: project
tags:
  - ios
  - swiftui
  - core-data
  - app-architecture
relationships:
  - target: "[[projects/dayfold/dayfold]]"
    type: related_to
sources: [projects/dayfold]
summary: >-
  抽屉式根容器 + MVVM + 共享 CoreDataStack 单例：App 注入 viewContext，
  View 全部通过 @Environment 取 context，ViewModel 用 @StateObject 持有并保存。
provenance:
  extracted: 0.70
  inferred: 0.25
  ambiguous: 0.05
base_confidence: 0.80
lifecycle: reviewed
lifecycle_changed: 2026-08-03
lifecycle_reason: "auto-promoted by wiki-lint --consolidate: age>30d, confidence>0.7"
tier: core
created: 2026-06-29T00:00:00Z
updated: 2026-08-03T05:47:33Z
---

# [[projects/dayfold/dayfold|Dayfold]] 架构概览

## 三层结构

```
App (dayfoldApp)
  └─ WindowGroup
     ├─ SecurityManager.isLocked ? LockScreenView : MainTabView
     └─ .environment(\.managedObjectContext, CoreDataStack.shared.viewContext)
        .onAppear { coreDataStack.createPresetTags() }

MainTabView (根容器)
  ├─ DrawerView (SidebarTab 枚举, 85% 屏宽抽屉)
  └─ ZStack 内容区 (selectedTab 切换)
     ├─ HomeView         (.list)   笔记本封面墙
     ├─ EntryListView    (.photos) 全部日记
     ├─ MapView          (.map)    MapKit 全局地图
     ├─ PlaceholderView  (.stats / .settings) 占位
     └─ TrashView        (sheet 弹出，onDismiss 回退 .list)
```

- 抽屉分组：顶部「日记」(list/photos/map) + 底部「更多」(trash/stats/settings)。
- 选中 `trash` 不会留在主内容区，而是触发 `showingTrash = true` 用 sheet 弹出 `TrashView`，
  关闭后强制把 `selectedTab` 复位为 `.list`，避免侧栏高亮残留。

## 数据流

1. `dayfoldApp` 用 `@StateObject private var coreDataStack = CoreDataStack.shared` 拿到单例，
   把 `viewContext` 注入 SwiftUI 环境。
2. 所有 View **不**在 init 里取 context 参数，**全部**用 `@Environment(\.managedObjectContext)`。
3. 列表型 View 走 `@FetchRequest`（自动响应增删）。
4. 编辑/操作型 View 持有 `@StateObject EntryEditorViewModel(context:)`，VM 改完用
   `CoreDataStack.shared.save()` 触发 `NSManagedObjectContextDidSave`，FetchRequest 自动刷新。

## MVVM 边界

- 全部 ViewModel 都是 `@MainActor ObservableObject`，发布 `@Published` 字段给 View。
- View 不直接写 Core Data，写操作经 ViewModel → `CoreDataStack.shared.save()`。
- `EntryEditorViewModel` 同时承担：表单状态、auto-save 定时器（2s）、位置/天气拉取、
  图片脏标记。
- `TimelineViewModel` 负责月历圆点 Map、月份导航、选中日期条目查询。

## 服务层（`Services/`）

| 服务 | 职责 | 线程 |
| --- | --- | --- |
| `CoreDataStack` | 单例；lazy `persistentContainer`；CloudKit 134400 降级本地 | Main |
| `MediaService` | 读写 `Documents/Media/` 图片；路径验证防穿越；缩略图生成 | 私有 `fileQueue` |
| `LocationService` | `@MainActor` 包装 `CLLocationManager`，反向地理编码 `placeName` | Main |
| `WeatherService` | WeatherKit 封装，按可用性返回 `WeatherData?` | async |
| `SecurityManager` | `LAContext` 锁屏，认证失败保持 `isLocked` | Main + async |
| `CardExporter` | 单条日记渲染为分享卡图片 | Main |

## 已知设计权衡 ^[inferred]

- **不用 TabBar 用抽屉**：项目刻意"温暖文艺"，避免 iOS 通用 TabBar 的工具感。代价是
  内容区被 85% 屏宽抽屉遮挡（`MainTabView.swift:20` 显式注释"整体向右滑动"），需要靠
  `drawerOpen` toggle 控制可见性。
- **CoreDataStack 双层历史跟踪**：开启 `NSPersistentHistoryTrackingKey` +
  `NSPersistentStoreRemoteChangeNotificationPostOptionKey`，监听 `.NSPersistentStoreRemoteChange`
  是为了 CloudKit 镜像同步后的视图刷新；本地模式同样会触发但开销可忽略。
- **ViewModel 不持有 `viewContext` 为单例**：`EntryEditorView.init` 接收外部 context 构造 VM，
  编辑时再次 `.environment(\.managedObjectContext, context)` 注入 sheet 内容。Bug 历史上
  多次出现 sheet/cover 内写入不刷新列表（见 commit `54c75ce`）。
