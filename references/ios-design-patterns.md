---
title: iOS 设计模式速查
category: references
tags: [ios, design-patterns, swift, architecture, anti-patterns]
sources: ["buckets/books/iOS 17 App Development for Beginners.epub"]
created: 2026-07-01T00:00:00Z
updated: 2026-07-01T00:00:00Z
summary: iOS/Swift 设计模式速查：创建型（5种）、结构型（7种）、行为型（11种）GoF 23种模式 + iOS 常见反模式清单。
base_confidence: 0.85
lifecycle: draft
lifecycle_changed: "2026-07-01"
tier: supporting
provenance:
  extracted: 0.78
  inferred: 0.22
  ambiguous: 0.00
---

# iOS 设计模式速查

## 创建型模式（Creational）— 如何创建对象

### Singleton（单例）

确保类只有一个实例，提供全局访问点：

```swift
class CoreDataStack {
    static let shared = CoreDataStack()
    private init() {}
}
// 使用：CoreDataStack.shared.context
```

iOS 中大量使用：`URLSession.shared`、`UserDefaults.standard`、`NotificationCenter.default`。

### Factory Method（工厂方法）

定义创建对象的接口，子类决定实例化哪个类：

```swift
protocol ViewControllerFactory {
    func makeDetailViewController(for item: Item) -> UIViewController
}
```

### Abstract Factory（抽象工厂）

创建一系列相关对象，无需指定具体类。常用于主题/样式切换。

### Builder（构建者）

分步构建复杂对象：

```swift
struct AlertBuilder {
    private var title: String = ""
    private var message: String = ""
    private var actions: [UIAlertAction] = []

    func title(_ t: String) -> AlertBuilder { var b = self; b.title = t; return b }
    func message(_ m: String) -> AlertBuilder { var b = self; b.message = m; return b }
    func action(_ a: UIAlertAction) -> AlertBuilder { var b = self; b.actions.append(a); return b }

    func build() -> UIAlertController {
        let alert = UIAlertController(title: title, message: message, preferredStyle: .alert)
        actions.forEach { alert.addAction($0) }
        return alert
    }
}
```

### Prototype（原型）

通过克隆现有对象创建新对象。Swift `Codable` 的 encode→decode 是一种原型式复制。

---

## 结构型模式（Structural）— 如何组合对象

### Adapter（适配器）

将现有接口转换为客户端期望的接口：

```swift
// UIViewRepresentable 就是 Adapter：将 UIKit 视图适配为 SwiftUI View
struct MapViewRepresentable: UIViewRepresentable {
    func makeUIView(context: Context) -> MKMapView { MKMapView() }
    func updateUIView(_ mapView: MKMapView, context: Context) {}
}
```

### Decorator（装饰器）

动态为对象添加职责，SwiftUI 的修饰符链即装饰器模式：

```swift
Text("Hello")
    .bold()
    .foregroundColor(.blue)
    .padding()
```

### Facade（外观）

为子系统提供统一的简洁接口：

```swift
class MediaManager {
    private let camera = CameraController()
    private let storage = PhotoStorage()
    private let processor = ImageProcessor()

    func captureAndSave() {
        let image = camera.capture()
        let processed = processor.process(image)
        storage.save(processed)
    }
}
```

### Composite（组合）

将对象组合成树形结构，统一处理单个对象与组合：SwiftUI 的 `View` 体系就是 Composite。

### Proxy（代理）

为对象提供代理/占位符控制访问：

```swift
// Lazy 加载代理
class LazyImageLoader {
    private var image: UIImage?
    func loadIfNeeded() -> UIImage {
        if image == nil { image = fetchFromNetwork() }
        return image!
    }
}
```

### Bridge（桥接）

将抽象部分与实现部分分离，使二者可以独立变化。

### Flyweight（享元）

共享大量细粒度对象：`UITableViewCell` 的重用池（`dequeueReusableCell`）。

---

## 行为型模式（Behavioral）— 如何通信和协作

### Observer（观察者）

一对多依赖关系，状态变化通知所有观察者：

```swift
// NotificationCenter（传统方式）
NotificationCenter.default.addObserver(self, selector: #selector(handle),
    name: .UIApplicationDidBecomeActive, object: nil)

// Combine/SwiftUI（现代方式）
@Published var items: [Item] = []   // items 变化时自动通知订阅者
```

### Delegate（委托）

协议委托是 iOS 中最常见的通信模式：

```swift
protocol TableDataDelegate: AnyObject {
    func didSelectRow(at index: Int)
}

class TableView {
    weak var delegate: TableDataDelegate?
    func userTappedRow(at index: Int) {
        delegate?.didSelectRow(at: index)
    }
}
```

**弱引用 delegate** 防止循环引用。

### Strategy（策略）

定义算法族，封装可互换：

```swift
protocol SortStrategy {
    func sort(_ array: [Int]) -> [Int]
}

class BubbleSort: SortStrategy { func sort(_ a: [Int]) -> [Int] { /* ... */ } }
class QuickSort: SortStrategy  { func sort(_ a: [Int]) -> [Int] { /* ... */ } }

class Sorter {
    var strategy: SortStrategy = QuickSort()
    func sort(_ array: [Int]) -> [Int] { strategy.sort(array) }
}
```

### Command（命令）

将请求封装为对象，支持撤销/重做：

```swift
protocol Command { func execute(); func undo() }
class TextEditor {
    private var history: [Command] = []
    func execute(_ cmd: Command) { cmd.execute(); history.append(cmd) }
    func undoLast() { history.popLast()?.undo() }
}
```

### Template Method（模板方法）

在父类定义算法骨架，子类重写特定步骤：`viewDidLoad` / `viewWillAppear` 体系。

### Iterator（迭代器）

Swift `Sequence` 协议实现迭代器模式。

### Chain of Responsibility（责任链）

请求沿链传递直到被处理：UIKit 的 **Responder Chain** 即此模式。

### State（状态）

对象在内部状态改变时改变行为：

```swift
enum CallState { case idle, ringing, active, onHold }
// 参见 xk-ai-talk-desk-ui 的坐席状态机
```

### Mediator（中介者）

用中间对象封装一组对象的交互：`NotificationCenter` 充当中介者角色。

### Memento（备忘录）

保存/恢复对象状态：iOS `UndoManager`。

### Visitor（访问者）

在不修改类的情况下增加新操作：Swift `extension` 是一种类似机制。

---

## iOS 常见反模式

| 反模式 | 症状 | 解决思路 |
|---|---|---|
| Massive View Controller | VC 超过 500 行，包含网络/数据/UI 逻辑 | 提取 ViewModel、Service、Repository |
| Singleton 滥用 | 全局状态难追踪，单元测试困难 | 依赖注入替代 |
| Pyramid of Doom | 多层嵌套回调（Callback Hell） | async/await + Swift Concurrency |
| Retain Cycle | 内存泄漏，对象无法释放 | `[weak self]` 捕获列表 |
| Force Unwrap 泛滥 | `!` 遍布代码，运行时崩溃 | 可选绑定、guard let、`??` 默认值 |
| Magic Number | 代码中硬编码数字/字符串 | 命名常量、枚举、Config 文件 |
| God Object | 一个类知道太多/做太多 | 拆分职责，遵循单一职责原则 |

---

## 关联页面

- [[concepts/ios-app-architecture]] — MVC/MVVM/VIPER/Redux 架构模式
- [[concepts/arc-memory-management]] — Retain Cycle 解决方案
- [[concepts/swift-concurrency]] — 取代 Callback Hell
- [[entities/ios17-app-development-book]] — 来源书籍
