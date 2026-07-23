---
title: ARC 与内存安全
category: concepts
tags: [swift, arc, ios]
sources: ["buckets/books/iOS 17 App Development for Beginners.epub"]
created: 2026-07-01T00:00:00Z
updated: 2026-07-01T00:00:00Z
summary: Swift ARC（自动引用计数）工作原理、强/弱/无主引用解决循环引用、内存冲突检测（独占访问规则）。
base_confidence: 0.88
lifecycle: draft
lifecycle_changed: "2026-07-01"
tier: supporting
provenance:
  extracted: 0.92
  inferred: 0.08
  ambiguous: 0.00
relationships:
  - target: "[[skills/ios-networking]]"
    type: related_to
  - target: "[[skills/ios-multithreading]]"
    type: related_to
  - target: "[[synthesis/arc-memory-management × swift-concurrency]]"
    type: synthesized_in

---

# ARC 与内存安全

## ARC 工作原理

**Automatic Reference Counting（ARC）** 是 Swift 的内存管理机制。它不是垃圾回收（GC），而是在**编译期**插入 retain/release 调用。

- 每个 class 实例有一个引用计数（reference count）
- 创建强引用时计数 +1，引用释放时 -1
- 计数归零时，实例被销毁（调用 `deinit`）
- **仅适用于引用类型（class）**；struct/enum 是值类型，由栈管理

```swift
class Student {
    let name: String
    init(name: String) { self.name = name; print("\(name) initialized") }
    deinit { print("\(name) deinitialized") }
}

var ref1: Student? = Student(name: "Alice")  // count = 1
var ref2 = ref1                              // count = 2
ref1 = nil                                   // count = 1（未释放）
ref2 = nil                                   // count = 0 → deinit
```

## 循环引用（Strong Reference Cycle）

两个对象互相持有强引用，导致计数永远无法归零，产生**内存泄漏**。

```swift
class Student {
    var scholarship: Scholarship?
    deinit { print("Student deinitialized") }
}
class Scholarship {
    var awardedTo: Student?       // ⚠️ 双向强引用 = 循环
    deinit { print("Scholarship deinitialized") }
}
```

### 解法一：weak 引用

`weak` 引用不增加引用计数，当对象被释放时自动置为 `nil`。

- **适用**：被引用对象生命周期比持有者短（或相等）
- **必须声明为 `var Optional`**

```swift
class CreditCard {
    weak var customer: Customer?   // 弱引用，不阻止 Customer 释放
}
```

### 解法二：unowned 引用

`unowned` 引用也不增加引用计数，但假设对象**始终非 nil**（不安全解包）。

- **适用**：被引用对象生命周期与持有者相同或更长
- 访问已释放对象会触发运行时崩溃

```swift
class Country {
    let capital: City!
}
class City {
    unowned let country: Country   // 城市不会比国家存活更久
}
```

### 解法三：闭包中的 [weak self] / [unowned self]

闭包捕获 `self` 会产生循环引用，用捕获列表打破：

```swift
class ViewController {
    var completionHandler: (() -> Void)?

    func setup() {
        completionHandler = { [weak self] in     // 打破循环
            guard let self = self else { return }
            self.updateUI()
        }
    }
}
```

## 内存冲突（Memory Safety）

Swift 在编译期和运行期检测**内存独占访问（exclusive access）**冲突。

### in-out 参数冲突

```swift
var total = 0
func increment(_ value: inout Int, by amount: Int) {
    value += amount
}
// ⚠️ 错误：同一变量作为 inout 传入同时读取
// increment(&total, by: total)  // 访问冲突
```

### 多线程属性访问冲突

在多线程环境下同时读写同一存储属性，必须使用 `Actor` 或同步机制保护。参见 [[concepts/swift-concurrency]]。

## 值类型 vs 引用类型

| 特性 | struct（值类型） | class（引用类型） |
|---|---|---|
| 内存位置 | 栈（通常）| 堆 |
| 赋值行为 | 复制 | 共享引用 |
| ARC 管理 | 不需要 | 需要 |
| 继承 | 不支持 | 支持 |
| `deinit` | 无 | 有 |

SwiftUI 推荐**值类型优先**：View、Model 用 struct；ViewModel/Service 用 class。

## 关联页面

- [[concepts/swift-fundamentals]] — Swift 语言基础
- [[concepts/swift-concurrency]] — Actor 解决多线程内存冲突
- [[projects/dayfold/concepts/core-data-cloudkit-fallback]] — CoreData 对象是引用类型
- [[entities/ios17-app-development-book]] — 来源书籍
- [[skills/ios-multithreading]] — iOS 多线程
- [[skills/ios-networking]] — iOS 网络编程
