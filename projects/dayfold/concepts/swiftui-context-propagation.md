---
title: SwiftUI 上下文注入与 FetchRequest 响应
category: project
tags: [ios, swiftui, core-data, debugging]
relationships:
  - target: "[[concepts/swiftui-framework]]"
    type: uses
sources: [projects/dayfold]
summary: >-
  sheet / fullScreenCover 不会自动继承父视图的 managedObjectContext，
  必须显式 .environment(\.managedObjectContext, context) 否则子视图写入不刷新 @FetchRequest。
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

# SwiftUI 上下文注入与 FetchRequest 响应

## 坑点

SwiftUI 的 `sheet(item:)` / `fullScreenCover(item:)` 默认**不会**继承父视图的
`\.managedObjectContext`，子视图若用 `@Environment(\.managedObjectContext)` 拿到的会是
SwiftUI 的占位空 context。

表现：在 sheet / cover 内的 `EntryEditorView` 保存成功（`CoreDataStack.shared.save()`
返回 OK），但关闭 sheet 后**外层** `@FetchRequest` 列表不刷新。

## 修复模式

每次弹 sheet / cover 时都显式注入：

```swift
.sheet(item: $newEntryDate) { item in
    EntryEditorView(entry: nil, context: viewContext, prefillDate: item.date)
        .environment(\.managedObjectContext, viewContext)  // ← 必须
}

.fullScreenCover(isPresented: $showingNotebook) { notebook in
    NotebookDetailView(
        notebook: notebook,
        onNewEntry: { ... },
        isPresented: $showingNotebook
    )
    .environment(\.managedObjectContext, viewContext)  // ← 必须
}
```

## 历史 bug

- `54c75ce fix: fullScreenCover 和 sheet 缺少 managedObjectContext 注入，导致新增日记后列表不更新`
- `73ca97e fix: NotebookDetailView 改用 @Environment context，修复 @FetchRequest 不响应新增日记的问题`

第二个 fix 把 `NotebookDetailView` 内原来通过 `CoreDataStack.shared.viewContext` 硬取
context 的方式改为 `@Environment(\.managedObjectContext) private var context` —— 这样
一旦父视图正确注入环境，子视图就能共享同一实例。

## 验证方法

打开 sheet → 创建/编辑日记 → 关闭 sheet → 外层列表应自动出现新条目。如果不出现：
1. 检查 sheet 修饰符链上有没有 `.environment(\.managedObjectContext, ...)`。
2. 检查 sheet 内容是否在内部又用 `CoreDataStack.shared.viewContext` 重新创建了一个独立
   context（应统一从环境拿）。
3. 用 `print(context === CoreDataStack.shared.viewContext)` 在子视图内确认是同一对象。

## 关联

- `CalendarView` 内 `newEntryDate` 用 `.sheet(item:)` 而非 `.sheet(isPresented:)` +
  独立 `@State` 日期，避免 SwiftUI 同帧捕获旧 `date` 值导致 `prefillDate` 失效。
- `EntryDetailView` 早期有"双 sheet 冲突"问题，commit `280a4f7` 通过统一 `sheetMode`
  枚举解决（见 [[projects/dayfold/concepts/architecture-overview]]）。

## 相关

- [[concepts/swiftui-framework]] — SwiftUI 声明式 UI 框架核心：View 协议、ViewBuilder tuple 组合、`some View` 不透明类型、布局容器、状态管理、修饰符
