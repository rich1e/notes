---
title: FetchRequest 与行内属性刷新
category: project
tags: [ios, swiftui, core-data, state-management]
sources: [projects/dayfold]
summary: >-
  @FetchRequest 只感知对象集合增删；同一对象上的属性/关系变化需把 NSManagedObject
  声明为 @ObservedObject 才能让行 UI 重新计算。
provenance:
  extracted: 0.70
  inferred: 0.25
  ambiguous: 0.05
base_confidence: 0.80
lifecycle: draft
lifecycle_changed: 2026-06-29
tier: supporting
created: 2026-06-29T00:00:00Z
updated: 2026-06-29T00:00:00Z
---

# FetchRequest 与行内属性刷新

## 核心规则

| 变化类型 | 触发 UI 刷新的方式 |
| --- | --- |
| 集合增删（新增/删除一条 Entry） | `@FetchRequest` 自动响应 |
| 同一 Entry 的属性变化（标题、内容、收藏等） | 必须 `@ObservedObject var entry: Entry` |
| 关系变化（添加 Tag、Location、MediaAsset） | `@ObservedObject` + 关系对象的 `@ObservedObject` |

`@FetchRequest` 只在集合层（FetchedResults）发生结构变化时通知 SwiftUI；对象属性
被 mutate 不会冒泡到行内。

## 已在项目中 `@ObservedObject` 化的组件

- `EntryCard` —— 显示单条 Entry 卡片
- `EntryHeader` —— 详情头部
- `TagRow` —— 标签行
- `EntryDetailView` —— 整个详情视图持有 `@ObservedObject var entry`
- `NotebookDetailView` 内的 `TimelineEntryRow`
- `TrashView` 内的 `TrashEntryRow`

## 反例（坑）

```swift
// 错误：编辑收藏后行不刷新
struct EntryRow: View {
    let entry: Entry  // 普通 let，不观察
    var body: some View {
        HStack {
            Text(entry.wrappedTitle)
            Image(systemName: entry.isFavorite ? "star.fill" : "star")
            // ↑ 收藏 toggle 后图标不变
        }
    }
}

// 正确
struct EntryRow: View {
    @ObservedObject var entry: Entry
    // ...
}
```

## 与 NSManagedObject 配合的注意点

- `Entry.wrappedTitle` 等 Swift 扩展 computed property 不会"被观察"——是
  `@ObservedObject` 让 SwiftUI 在 `objectWillChange` 发出时重算 body。
- 大量 `@ObservedObject` 持有同一对象不会重复订阅；`@FetchRequest` 已经是按对象 ID
  去重，SwiftUI 在 iOS 14+ 内部对 `ObservedObject` 也有同一对象的复用机制。
- 对 `Location`、`Tag`、`MediaAsset` 同理：行内展示关系字段时也要
  `@ObservedObject var location: Location`。

## 性能侧记 ^[inferred]

- 列表的"行内只读 1–2 个字段 + 缩略图"场景，`@ObservedObject` 触发的 body 重新计算成本
  可忽略；不要为了"省一次重算"改成把字段值提前拷到 `@State`——会失去自动同步且引入
  数据不一致 bug。
- 缩略图加载用 `.task(id: thumbnailSourceID)`（绑定 filename 拼接串）而非一次性
  `.task`，保证 `MediaAsset` 集合变化（用户增删图片）时自动重载。
