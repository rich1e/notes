---
title: iOS 多线程
category: skills
tags: [ios, actor, swift]
sources: ["buckets/books/iOS 17 App Development for Beginners.epub"]
created: 2026-07-01T00:00:00Z
updated: 2026-07-01T00:00:00Z
summary: GCD（Grand Central Dispatch）三种队列类型（主/全局/自定义）、QoS 优先级、DispatchGroup 等待多任务、NSOperation/BlockOperation 高级控制。
base_confidence: 0.87
lifecycle: draft
lifecycle_changed: "2026-07-01"
tier: supporting
provenance:
  extracted: 0.90
  inferred: 0.10
  ambiguous: 0.00
relationships:
  - target: "[[concepts/swiftui-framework]]"
    type: related_to
  - target: "[[concepts/arc-memory-management]]"
    type: related_to
  - target: "[[concepts/swift-fundamentals]]"
    type: related_to

---

# iOS 多线程

iOS 并发编程有两套 API：底层的 **GCD（Grand Central Dispatch）** 和高层的 **NSOperation**。Swift 5.5+ 还引入了结构化并发（参见 [[concepts/swift-concurrency]]）。

## GCD 概念

GCD 以**队列（Dispatch Queue）**为核心，分为：

- **串行队列（Serial）**：一次只执行一个任务，按添加顺序执行
- **并发队列（Concurrent）**：同时执行多个任务，顺序不固定

### 主队列（Main Queue）

主线程队列，**必须在此更新 UI**：

```swift
DispatchQueue.main.async {
    self.label.text = "Updated"
    self.activityIndicator.stopAnimating()
}
```

⚠️ 永远不要在主队列上执行耗时操作（网络请求、文件 IO），否则 App 卡死。

### 全局队列（Global Queue）

系统提供的共享并发队列，按 QoS 分级：

```swift
DispatchQueue.global(qos: .userInitiated).async {
    let image = downloadImage(url: url)   // 后台执行
    DispatchQueue.main.async {
        imageView.image = image           // 回主线程更新 UI
    }
}
```

### 自定义队列（Custom Queue）

```swift
// 串行队列
let serialQueue = DispatchQueue(label: "com.app.serial")

// 并发队列
let concurrentQueue = DispatchQueue(label: "com.app.concurrent",
                                    attributes: .concurrent)

serialQueue.async { print("Task 1") }
serialQueue.async { print("Task 2") }   // 等 Task 1 完成后执行
```

## Quality of Service（QoS）

| 级别 | 用途 | 优先级 |
|---|---|---|
| `.userInteractive` | 动画、手势响应 | 最高 |
| `.userInitiated` | 用户触发的操作（加载新页面） | 高 |
| `.default` | 通用 | 中 |
| `.utility` | 数据备份、图片处理 | 中低 |
| `.background` | 统计上报、清理缓存 | 最低 |

```swift
let queue = DispatchQueue(label: "com.app.background", qos: .background)
queue.async { analyticsService.flush() }
```

## DispatchGroup（等待多任务完成）

```swift
let group = DispatchGroup()

group.enter()
fetchUserProfile { profile in
    self.userProfile = profile
    group.leave()
}

group.enter()
fetchUserPosts { posts in
    self.posts = posts
    group.leave()
}

group.notify(queue: .main) {
    // 所有任务完成后在主线程执行
    self.tableView.reloadData()
}
```

## DispatchSemaphore（限制并发数）

```swift
let semaphore = DispatchSemaphore(value: 3)   // 最多 3 个并发

for item in items {
    DispatchQueue.global().async {
        semaphore.wait()              // 获取许可
        process(item)
        semaphore.signal()            // 释放许可
    }
}
```

## DispatchBarrier（读写分离）

在并发队列中实现线程安全的读写：

```swift
let queue = DispatchQueue(label: "com.app.data", attributes: .concurrent)
var data: [String] = []

// 并发读取
func read() -> [String] {
    queue.sync { data }
}

// 独占写入（barrier 执行时，其他任务暂停）
func write(_ item: String) {
    queue.async(flags: .barrier) { data.append(item) }
}
```

## NSOperation / NSOperationQueue

比 GCD 更高层的 API，支持**依赖关系**和**取消**：

```swift
// BlockOperation 封装闭包
let op1 = BlockOperation { print("Download image") }
let op2 = BlockOperation { print("Process image") }
op2.addDependency(op1)   // op2 等 op1 完成后执行

let queue = OperationQueue()
queue.maxConcurrentOperationCount = 2
queue.addOperations([op1, op2], waitUntilFinished: false)

// 取消所有操作
queue.cancelAllOperations()
```

## GCD vs Swift Concurrency vs NSOperation

| 特性 | GCD | Swift Concurrency | NSOperation |
|---|---|---|---|
| 语法简洁度 | 中 | 高 | 中 |
| 依赖管理 | 手动 | `async let` | 原生 |
| 取消支持 | 无原生 | Task.cancel() | 原生 |
| iOS 最低版本 | iOS 8+ | iOS 15+ | iOS 8+ |
| 数据安全 | 手动（Barrier/Semaphore） | Actor | 手动 |

**推荐选择**：新项目优先 Swift Concurrency；兼容 iOS 14 及以下用 GCD；需要复杂任务依赖图用 NSOperation。

## 关联页面

- [[concepts/swift-concurrency]] — async/await、Actor（现代并发推荐方式）
- [[skills/ios-networking]] — 网络请求的线程管理
- [[entities/ios17-app-development-book]] — 来源书籍
- [[concepts/swift-fundamentals]] — Swift 语言基础
- [[concepts/arc-memory-management]] — ARC 与内存安全
- [[concepts/swiftui-framework]] — SwiftUI 框架
