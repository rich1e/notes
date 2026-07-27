---

title: Swift 并发
category: concepts
tags:
  - ios
  - swift
  - concurrency
relationships:
  - target: "[[projects/dayfold/dayfold]]"
    type: uses
  - target: "[[synthesis/arc-memory-management × swift-concurrency]]"
    type: related_to
sources: ["buckets/books/iOS 17 App Development for Beginners.epub"]
created: 2026-07-01T00:00:00Z
updated: 2026-07-01T00:00:00Z
summary: Swift 5.5+ 结构化并发：async/await、Task/TaskGroup、Actor 数据隔离、MainActor UI 更新、与 GCD 的对比。
base_confidence: 0.88
lifecycle: draft
lifecycle_changed: "2026-07-01"
tier: supporting
provenance:
  extracted: 0.88
  inferred: 0.12
  ambiguous: 0.00
---

# Swift 并发

Swift 5.5（iOS 15+）引入**结构化并发**模型，取代回调地狱和手动 GCD 调度。

## async/await

`async` 标记异步函数，`await` 暂停当前函数等待异步结果（不阻塞线程）：

```swift
func fetchUser(id: Int) async throws -> User {
    let url = URL(string: "https://api.example.com/users/\(id)")!
    let (data, _) = try await URLSession.shared.data(from: url)
    return try JSONDecoder().decode(User.self, from: data)
}

// 调用方
Task {
    do {
        let user = try await fetchUser(id: 42)
        print(user.name)
    } catch {
        print("Error: \(error)")
    }
}
```

## Task

`Task` 是并发工作的基本单元：

```swift
// 创建非结构化任务
let task = Task {
    return await expensiveComputation()
}
let result = await task.value   // 等待结果

// 取消任务
task.cancel()

// Task.sleep（非阻塞）
try await Task.sleep(nanoseconds: 1_000_000_000)  // 1秒
```

**Task 优先级**：`.high / .medium / .low / .background / .utility / .userInitiated`

## TaskGroup（并发执行多个任务）

```swift
func fetchAllUsers(ids: [Int]) async throws -> [User] {
    try await withThrowingTaskGroup(of: User.self) { group in
        for id in ids {
            group.addTask { try await fetchUser(id: id) }
        }
        var users: [User] = []
        for try await user in group {
            users.append(user)
        }
        return users
    }
}
```

`withTaskGroup`（不抛错）/ `withThrowingTaskGroup`（可抛错）。

## async let（并发绑定）

同时启动多个异步操作，然后等待所有结果：

```swift
async let profile = fetchProfile(userId: 1)
async let posts   = fetchPosts(userId: 1)
async let friends = fetchFriends(userId: 1)

// 等待所有三个并发任务完成
let (p, po, f) = try await (profile, posts, friends)
```

## Actor（数据隔离）

`actor` 是引用类型，内置**互斥访问保护**，消除数据竞争：

```swift
actor BankAccount {
    private var balance: Double = 0

    func deposit(_ amount: Double) {
        balance += amount
    }

    func getBalance() -> Double {
        return balance
    }
}

let account = BankAccount()
await account.deposit(100)         // 跨 actor 调用必须 await
let bal = await account.getBalance()
```

### @MainActor

`@MainActor` 保证代码在主线程执行，常用于 UI 更新：

```swift
@MainActor
class ViewModel: ObservableObject {
    @Published var items: [Item] = []

    func loadData() async {
        let fetched = await fetchItems()
        items = fetched          // 自动在主线程更新
    }
}

// 从任意上下文切换到主线程
await MainActor.run {
    self.label.text = "Done"
}
```

## 与 GCD 对比

| 特性 | GCD (DispatchQueue) | Swift Concurrency |
|---|---|---|
| 语法 | 回调嵌套 | async/await 线性 |
| 错误处理 | 复杂 | `throws` / `try await` |
| 取消 | 无原生支持 | `Task.cancel()` + `Task.checkCancellation()` |
| 数据安全 | 手动 (`DispatchBarrier`) | `actor` 内置保证 |
| 最低支持 | iOS 8+ | iOS 15+ |

GCD 仍有用武之地（如与 C 库集成、iOS 14 及以下兼容），参见 [[skills/ios-multithreading]]。

## 与 Combine 的关系

Swift Concurrency 可与 Combine 互操作：

```swift
// Publisher 转 async 序列
for await value in publisher.values {
    print(value)
}
```

## 关联页面

- [[concepts/swift-fundamentals]] — Swift 基础
- [[skills/ios-multithreading]] — GCD 多线程技巧
- [[skills/ios-networking]] — URLSession async/await 网络请求
- [[projects/dayfold/dayfold]] — dayfold 使用 async/await 加载数据
- [[entities/ios17-app-development-book]] — 来源书籍
