---
title: Swift 语言基础
category: concepts
tags: [swift, ios, programming, type-system, concurrency]
sources: ["buckets/books/iOS 17 App Development for Beginners.epub"]
created: 2026-07-01T00:00:00Z
updated: 2026-07-01T00:00:00Z
summary: Swift 5.9 核心特性：类型系统、变量声明、集合类型、控制流、闭包、可选值与协议导向编程。
base_confidence: 0.88
lifecycle: draft
lifecycle_changed: "2026-07-01"
tier: core
provenance:
  extracted: 0.90
  inferred: 0.10
  ambiguous: 0.00
relationships:
  - target: "[[skills/ios-networking]]"
    type: related_to
  - target: "[[skills/ios-multithreading]]"
    type: related_to

---

# Swift 语言基础

Swift 是 Apple 设计的现代化、类型安全的编程语言，用于 iOS/macOS/watchOS/tvOS 开发。Swift 5.9 是 iOS 17 开发的当前版本。

## 类型系统

Swift 是**强类型**语言，支持**类型推断**（Type Inference）：

```swift
let name = "Alice"          // 推断为 String
var age = 30                // 推断为 Int
let pi: Double = 3.14159    // 显式类型注解
```

基本类型：

| 类型 | 说明 | 示例 |
|---|---|---|
| `Int` | 整数 | `42` |
| `Float` | 32位浮点 | `3.14` |
| `Double` | 64位浮点（推荐） | `3.14159` |
| `Bool` | 布尔值 | `true / false` |
| `String` | 字符串 | `"Hello"` |
| `Character` | 单字符 | `"A"` |
| `Tuple` | 元组（复合值） | `(200, "OK")` |

`let` 声明常量（不可变），`var` 声明变量（可变）。**优先使用 `let`**。

## 可选值（Optionals）

Swift 通过可选值显式处理空值，消除 null 引用错误：

```swift
var username: String? = nil    // 可为 nil 的 String
username = "rich1e"

// 安全解包方式
if let name = username {
    print("Hello, \(name)")
}

// 空合运算符
let display = username ?? "Guest"

// 可选链
let count = username?.count    // 返回 Int?
```

强制解包（`!`）在值确定非 nil 时使用，否则触发运行时崩溃。

## 集合类型

### Array（有序，可重复）

```swift
var fruits: [String] = ["Apple", "Banana"]
fruits.append("Cherry")
fruits.remove(at: 0)
```

### Set（无序，不重复）

```swift
var tags: Set<String> = ["swift", "ios"]
tags.insert("swiftui")
let hasSwift = tags.contains("swift")
```

### Dictionary（键值对）

```swift
var scores: [String: Int] = ["Alice": 95, "Bob": 87]
scores["Charlie"] = 100
let aliceScore = scores["Alice"] ?? 0
```

## 控制流

```swift
// for-in 循环
for fruit in fruits { print(fruit) }
for i in 1...5 { print(i) }        // 闭区间
for i in 0..<5 { print(i) }        // 半开区间

// switch（不需要 break，支持模式匹配）
switch score {
case 90...100: print("A")
case 70..<90:  print("B")
default:       print("C")
}

// guard 提前退出
func greet(name: String?) {
    guard let name = name else { return }
    print("Hello, \(name)")
}
```

## 闭包（Closures）

闭包是自包含的函数代码块，可捕获外部变量：

```swift
// 完整语法
let multiply = { (a: Int, b: Int) -> Int in
    return a * b
}

// 简化：尾随闭包 + 类型推断 + $0/$1 参数简写
let doubled = [1, 2, 3].map { $0 * 2 }         // [2, 4, 6]
let evens   = [1, 2, 3, 4].filter { $0 % 2 == 0 } // [2, 4]
let sum     = [1, 2, 3].reduce(0, +)            // 6
```

`@escaping` 修饰逃逸闭包（在函数返回后被调用，如异步回调）。

## 函数与参数标签

```swift
// 外部标签 / 内部名
func greet(person name: String, from city: String) -> String {
    return "Hello \(name) from \(city)"
}
greet(person: "Alice", from: "Beijing")

// 可变参数
func sum(_ numbers: Int...) -> Int { numbers.reduce(0, +) }

// inout 参数（修改外部变量）
func increment(_ value: inout Int) { value += 1 }
```

## 错误处理

```swift
enum NetworkError: Error {
    case invalidURL
    case noData
}

func fetchData(from url: String) throws -> Data {
    guard url.hasPrefix("https") else { throw NetworkError.invalidURL }
    // ...
}

do {
    let data = try fetchData(from: "https://api.example.com")
} catch NetworkError.invalidURL {
    print("Invalid URL")
} catch {
    print("Error: \(error)")
}
```

## 协议导向编程（POP）

Swift 鼓励用**协议（Protocol）**替代继承：

```swift
protocol Drawable {
    func draw()
    var color: String { get }
}

// 协议扩展提供默认实现
extension Drawable {
    func draw() { print("Drawing in \(color)") }
}

struct Circle: Drawable {
    var color = "red"
}
```

## 关联页面

- [[concepts/swiftui-framework]] — SwiftUI 声明式 UI 框架
- [[concepts/arc-memory-management]] — ARC 内存管理
- [[concepts/swift-concurrency]] — async/await 并发
- [[concepts/ios-app-architecture]] — MVC/MVVM 架构模式
- [[entities/ios17-app-development-book]] — 来源书籍
- [[skills/ios-multithreading]] — iOS 多线程
- [[skills/ios-networking]] — iOS 网络编程
