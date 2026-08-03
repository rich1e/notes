---
title: 软删除 + 回收箱
category: project
tags: [ios, swiftui, core-data, persistence, ux]
relationships:
  - target: "[[concepts/swiftui-framework]]"
    type: uses
sources: [projects/dayfold]
summary: >-
  Entry 用 deletedAt 时间戳实现软删除，@FetchRequest 用 NSPredicate 隔离
  "deletedAt == nil" 业务列表与 "deletedAt != nil" 回收箱列表；永久删除
  才级联删 MediaAsset / Location 与磁盘文件。
provenance:
  extracted: 0.75
  inferred: 0.20
  ambiguous: 0.05
base_confidence: 0.82
lifecycle: reviewed
lifecycle_changed: 2026-08-03
lifecycle_reason: "auto-promoted by wiki-lint --consolidate: age>30d, confidence>0.7"
tier: supporting
created: 2026-06-29T00:00:00Z
updated: 2026-08-03T05:47:33Z
---

# 软删除 + 回收箱

## 数据模型

`Entry.deletedAt: Date?` —— nil 表示正常，日期表示被"扔进回收箱"的时间。

`Entry.moveToTrash()` / `Entry.restore()` 工厂方法在 Models 扩展里，只翻转 `deletedAt`
字段。

## 列表 predicate 隔离

```swift
// 业务列表（全部日记 / 笔记本详情）
@FetchRequest(
    sortDescriptors: [NSSortDescriptor(keyPath: \Entry.createdAt, ascending: false)],
    predicate: NSPredicate(format: "deletedAt == nil"),
    animation: .default
)
private var entries: FetchedResults<Entry>

// 回收箱
@FetchRequest(
    sortDescriptors: [SortDescriptor(\.deletedAt, order: .reverse)],
    predicate: NSPredicate(format: "deletedAt != nil"),
    animation: .default
)
private var trashedEntries: FetchedResults<Entry>
```

两个 FetchRequest 不会互相看到对方数据；左滑删除 / 恢复都只改 `deletedAt`，列表会
自动增删。

## 永久删除的级联

仅在 `TrashView.permanentlyDelete` 与 `clearAll` 中执行：

```swift
for asset in entry.mediaAssetsArray {
    if let filename = asset.filename {
        Task { await MediaService.shared.deleteImage(filename: filename) }
    }
    viewContext.delete(asset)
}
if let location = entry.location { viewContext.delete(location) }
viewContext.delete(entry)
try? viewContext.save()
```

注意 `Entry` ↔ `MediaAsset` / `Location` 在 Core Data 模型里如果配了 cascade delete rule，
可以省掉手动 `viewContext.delete(asset)`；当前实现选择显式删除，可读性更好。

## 回收箱 UI

- 顶部"全部删除"按钮（红色胶囊） + 中间标题"回收箱" + 右上"×" 关闭按钮。
- 列表按"删除日"分组，**不是**创建日分组：`groupedEntries` 用 `entry.deletedAt` 排。
- 单条 `TrashEntryRow` 支持左滑恢复（青色 tint）/ 右滑彻底删除（destructive）。
- 关闭 sheet 后 `MainTabView.onDismiss` 强制把 `selectedTab` 从 `.trash` 复位为 `.list`，
  避免侧栏高亮残留。

## 为什么用 `deletedAt` 时间戳而不是 Bool ^[inferred]

- 时间戳可直接用于"按删除日分组"和"按删除日排序"（默认倒序，最近删的在前）。
- Bool 也能实现分组，但需要额外维护 `deletedAt` 字段做 UI 展示，不如直接用。
- 未来想做"30 天后自动清除"也只需在 `clearAll` 之外加一个 `purgeOlderThan(_:)` 任务。

## 与 CloudKit 同步的兼容性

软删除操作是普通的 `managedObject.setValue(_:forKey:)`，CloudKit 会把这条 mutation
同步到其他设备。其他设备上对应的 `Entry` 也会被 FetchRequest predicate 过滤掉——回收箱
**不会跨设备同步**。这是有意的设计：每个设备的"回收箱"代表本地用户操作历史。

## 相关

- [[concepts/swiftui-framework]] — SwiftUI 声明式 UI 框架核心：View 协议、ViewBuilder tuple 组合、`some View` 不透明类型、布局容器、状态管理、修饰符
