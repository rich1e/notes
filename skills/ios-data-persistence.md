---
title: iOS 数据持久化
category: skills
tags: [ios, core-data, swiftdata, persistence]
relationships:
  - target: "[[projects/dayfold/dayfold]]"
    type: uses
sources: ["buckets/books/iOS 17 App Development for Beginners.epub"]
created: 2026-07-01T00:00:00Z
updated: 2026-07-01T00:00:00Z
summary: iOS 五大持久化方案：UserDefaults（偏好设置）、Property List、SQLite（轻量关系型）、Core Data（ORM）、SwiftData（Swift 原生 ORM）及 CRUD 模式。
base_confidence: 0.87
lifecycle: draft
lifecycle_changed: "2026-07-01"
tier: supporting
provenance:
  extracted: 0.88
  inferred: 0.12
  ambiguous: 0.00
---

# iOS 数据持久化

## 方案选型

| 方案 | 适用场景 | 数据量 |
|---|---|---|
| UserDefaults | 用户偏好、简单配置 | 极小（几KB） |
| Property List (.plist) | 静态配置、本地化字符串 | 小 |
| SQLite | 自定义 SQL 查询、轻量 DB | 中 |
| Core Data | 复杂对象图、CloudKit 同步 | 大 |
| SwiftData | Swift 原生 ORM（iOS 17+） | 大 |

## UserDefaults

键值对持久化，适合存储偏好设置：

```swift
let defaults = UserDefaults.standard

// 写入
defaults.set("Alice", forKey: "username")
defaults.set(true, forKey: "darkMode")
defaults.set(42, forKey: "lastScore")

// 读取（key 不存在时返回类型零值）
let name  = defaults.string(forKey: "username") ?? "Guest"
let dark  = defaults.bool(forKey: "darkMode")
let score = defaults.integer(forKey: "lastScore")

// 删除
defaults.removeObject(forKey: "username")
```

⚠️ 不要存储敏感信息（密码/token），应使用 **Keychain**。

## Property List（.plist）

XML 格式键值存储，根类型为 Array 或 Dictionary：

```swift
// 读取 Bundle 内的 plist
func loadPlist<T>(named name: String) -> T? {
    guard let path = Bundle.main.path(forResource: name, ofType: "plist"),
          let data = FileManager.default.contents(atPath: path)
    else { return nil }
    return try? PropertyListSerialization.propertyList(
        from: data, options: .mutableContainersAndLeaves, format: nil) as? T
}

let states: [String]? = loadPlist(named: "States")
```

支持类型：Dictionary、Array、Boolean、Data、Date、String、Number。

## SQLite

轻量级嵌入式关系型数据库，无需服务器：

```swift
import SQLite3

var db: OpaquePointer?
let dbPath = FileManager.default
    .urls(for: .documentDirectory, in: .userDomainMask)[0]
    .appendingPathComponent("app.db").path

// 打开/创建数据库
sqlite3_open(dbPath, &db)

// 建表
let createSQL = "CREATE TABLE IF NOT EXISTS Users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER);"
sqlite3_exec(db, createSQL, nil, nil, nil)

// 插入
let insertSQL = "INSERT INTO Users (name, age) VALUES (?, ?);"
var stmt: OpaquePointer?
sqlite3_prepare_v2(db, insertSQL, -1, &stmt, nil)
sqlite3_bind_text(stmt, 1, "Alice", -1, nil)
sqlite3_bind_int(stmt, 2, 30)
sqlite3_step(stmt)
sqlite3_finalize(stmt)

sqlite3_close(db)
```

## Core Data

Apple 的 ORM 框架，基于对象图管理：

### 基本概念

- **NSManagedObjectContext**：工作区，所有增删改查都在 context 内完成
- **NSManagedObject**：实体实例（自动生成子类）
- **NSFetchRequest**：查询请求
- **NSPersistentContainer**：封装 Core Data 栈

### CRUD

```swift
// Create
let context = CoreDataStack.shared.context
let entry = Entry(context: context)
entry.title = "My Entry"
entry.createdAt = Date()
try? context.save()

// Read（FetchRequest）
let request: NSFetchRequest<Entry> = Entry.fetchRequest()
request.predicate = NSPredicate(format: "deletedAt == nil")
request.sortDescriptors = [NSSortDescriptor(key: "createdAt", ascending: false)]
let entries = try? context.fetch(request)

// Update
entry.title = "Updated Title"
try? context.save()

// Delete
context.delete(entry)
try? context.save()
```

### SwiftUI 中的 Core Data

```swift
// @FetchRequest 自动监听变化
@FetchRequest(
    sortDescriptors: [SortDescriptor(\.createdAt, order: .reverse)],
    predicate: NSPredicate(format: "deletedAt == nil")
) var entries: FetchedResults<Entry>
```

⚠️ **sheet/cover 不继承 managedObjectContext**，必须显式注入：

```swift
.sheet(isPresented: $showEditor) {
    EditorView().environment(\.managedObjectContext, context)
}
```

参见 [[projects/dayfold/concepts/swiftui-context-propagation]]。

### CloudKit 同步

在 `NSPersistentContainer` 替换为 `NSPersistentCloudKitContainer` 即可启用 iCloud 同步。无 iCloud 时优雅降级：监听 `NSCocoaErrorDomain 134400` 错误，清空 `cloudKitContainerOptions` 后重新加载。参见 [[projects/dayfold/concepts/core-data-cloudkit-fallback]]。

## SwiftData（iOS 17+）

Swift 原生 ORM，宏驱动，与 SwiftUI 深度集成：

```swift
import SwiftData

@Model
class Item {
    var name: String
    var createdAt: Date
    var isCompleted: Bool = false

    init(name: String) {
        self.name = name
        self.createdAt = Date()
    }
}

// App 入口配置
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .modelContainer(for: Item.self)
    }
}

// 视图中使用
struct ContentView: View {
    @Query(sort: \.createdAt, order: .reverse) var items: [Item]
    @Environment(\.modelContext) private var context

    var body: some View {
        List(items) { item in Text(item.name) }
    }
}
```

**SwiftData vs Core Data**：SwiftData 代码量少 80%，但仅限 iOS 17+；Core Data 兼容 iOS 8+，功能更丰富（尤其 CloudKit 集成）。

## 关联页面

- [[projects/dayfold/skills/soft-delete-with-trash]] — `deletedAt` 时间戳软删除实现
- [[projects/dayfold/concepts/core-data-cloudkit-fallback]] — CloudKit 降级本地存储
- [[projects/dayfold/skills/entry-editor-image-dirty-tracking]] — MediaAsset 脏标记
- [[concepts/swift-fundamentals]] — Swift 基础
- [[entities/ios17-app-development-book]] — 来源书籍

## 相关

- [[projects/dayfold/dayfold]] — >-
