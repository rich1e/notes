---
title: SwiftUI 框架
category: concepts
tags: [swiftui, ios, ux, swift, architecture]
sources:
  - "buckets/books/iOS 17 App Development for Beginners.epub"
  - "https://www.youtube.com/watch?v=kCjDulwChRQ"
created: 2026-07-01T00:00:00Z
updated: 2026-07-10T14:30:00Z
summary: SwiftUI 声明式 UI 框架核心：View 协议、ViewBuilder tuple 组合、`some View` 不透明类型、布局容器、状态管理、修饰符链式调用。
base_confidence: 0.90
lifecycle: draft
lifecycle_changed: "2026-07-01"
tier: core
provenance:
  extracted: 0.85
  inferred: 0.15
  ambiguous: 0.00
relationships:
  - target: "[[skills/ios-networking]]"
    type: related_to
  - target: "[[skills/ios-multithreading]]"
    type: related_to

  - target: "[[synthesis/arc-memory-management × swift-concurrency]]"
    type: related_to
  - target: "[[references/ios-design-patterns]]"
    type: related_to
---

# SwiftUI 框架

SwiftUI 是 Apple 在 2019 年（iOS 13）推出的**声明式 UI 框架**，用 Swift DSL 描述"UI 应该是什么样子"而非"如何一步步构建"。

## View 协议

所有 SwiftUI 视图都遵从 `View` 协议，要求实现 `body` 属性：

```swift
struct ContentView: View {
    var body: some View {
        Text("Hello, World!")
            .font(.title)
            .foregroundColor(.blue)
    }
}
```

`some View` 是不透明返回类型（Opaque Type），编译器推断具体类型。当 `body` 包含 `if/else` 等分支时，实际返回的是 `ConditionalContent<A, B>` 等复杂泛型，`some View` 让调用者无需知晓这个细节。^[inferred]

## ViewBuilder — 多 View 的 "Lego Bag"

`body` 属性被 `@ViewBuilder` 隐式标注，使 Swift 可以将多个子表达式组合为一个 **tuple View**（类似 Lego 积木的装袋器）：

```swift
struct MyView: View {
    var body: some View {     // body 由 @ViewBuilder 处理
        Text("Line 1")        // 每行都是一个 View 表达式
        Text("Line 2")        // 最终被打包成 TupleView<(Text, Text)>
        if Bool.random() {
            Image(systemName: "star")
        }
    }
}
```

关键点：
- `@ViewBuilder` 是一个 **result builder**，把多个 View 语句编译为 `TupleView`
- **最多支持 10 个直接子视图**（超出需用 `Group` 包裹）
- `if/else`、`switch` 在 ViewBuilder 闭包中被编译为 `ConditionalContent<A, B>`，而非运行时分支

## 尾随闭包语法在 SwiftUI 中的意义

SwiftUI API 大量使用尾随闭包（trailing closure），让代码更贴近 DSL 风格：

```swift
// 标准形式（verbose）
VStack(alignment: .leading, spacing: 8, content: {
    Text("Title")
    Text("Subtitle")
})

// 尾随闭包语法（SwiftUI 风格）
VStack(alignment: .leading, spacing: 8) {
    Text("Title")
    Text("Subtitle")
}
```

当函数最后一个参数是闭包时，可将其移到括号外。若闭包是唯一参数，括号可完全省略：

```swift
Button("Tap me") {          // action 参数是唯一闭包，括号省略
    doSomething()
}
```

这就是为什么 SwiftUI 代码"看起来像声明而非函数调用"——实际上每层嵌套都是一个函数调用 + 尾随闭包。^[inferred]

## 布局容器

### VStack / HStack / ZStack

```swift
VStack(alignment: .leading, spacing: 16) {
    Text("Title").font(.headline)
    HStack {
        Image(systemName: "star.fill")
        Text("Rating: 5")
    }
}

ZStack {                          // 层叠布局
    Color.blue.ignoresSafeArea()
    Text("Overlay").foregroundColor(.white)
}
```

### LazyVGrid / LazyHGrid（懒加载网格）

```swift
let columns = [
    GridItem(.flexible()),
    GridItem(.flexible()),
    GridItem(.flexible())
]

LazyVGrid(columns: columns, spacing: 16) {
    ForEach(items) { item in
        ItemCard(item: item)
    }
}
```

`Lazy` 前缀表示只渲染可见区域，适合长列表。

### List

```swift
List(fruits, id: \.self) { fruit in
    Text(fruit)
}
.listStyle(.insetGrouped)
```

## 状态管理

SwiftUI 数据驱动 UI，状态变化自动触发视图重新渲染。

| 属性包装器 | 用途 | 作用域 |
|---|---|---|
| `@State` | 视图内部私有状态 | 单个视图 |
| `@Binding` | 父子视图共享状态（双向绑定） | 父→子传递 |
| `@ObservedObject` | 外部引用类型状态（需遵从 ObservableObject） | 视图树外 |
| `@StateObject` | 视图拥有的 ObservableObject 实例 | 单个视图 |
| `@EnvironmentObject` | 全局注入的共享状态 | 整个视图树 |
| `@Environment` | 读取系统环境值（colorScheme/locale 等） | 整个视图树 |

```swift
class UserStore: ObservableObject {
    @Published var name = "Alice"
}

struct ProfileView: View {
    @ObservedObject var store: UserStore

    var body: some View {
        TextField("Name", text: $store.name)   // $前缀取 Binding
    }
}
```

## 修饰符（Modifiers）

链式调用，每个修饰符返回新 View：

```swift
Text("Hello")
    .font(.title)
    .fontWeight(.bold)
    .foregroundColor(.primary)
    .padding(.horizontal, 16)
    .background(Color.yellow.opacity(0.3))
    .cornerRadius(8)
    .shadow(radius: 4)
```

**顺序重要**：`padding` 后接 `background` 与反过来效果不同。

## 导航

```swift
NavigationStack {
    List(items) { item in
        NavigationLink(destination: DetailView(item: item)) {
            ItemRow(item: item)
        }
    }
    .navigationTitle("Items")
    .toolbar {
        ToolbarItem(placement: .navigationBarTrailing) {
            Button(action: addItem) { Image(systemName: "plus") }
        }
    }
}
```

## sheet / fullScreenCover

```swift
struct ContentView: View {
    @State private var showSheet = false

    var body: some View {
        Button("Show") { showSheet = true }
            .sheet(isPresented: $showSheet) {
                SheetView()
                    .environment(\.managedObjectContext, context)  // ⚠️ sheet 不继承父视图 context，必须显式注入
            }
    }
}
```

> **已知陷阱**：`sheet`/`fullScreenCover` 中的视图**不继承**父视图的 `@Environment`（如 `managedObjectContext`），必须显式传入。参见 [[projects/dayfold/concepts/swiftui-context-propagation]]。

## PreviewProvider

```swift
struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
            .previewDevice("iPhone 15")
    }
}
```

Xcode 15 支持 `#Preview` 宏简写：

```swift
#Preview { ContentView() }
```

## 与 UIKit 互操作

- `UIViewRepresentable`：将 UIKit 视图包装为 SwiftUI 视图
- `UIHostingController`：将 SwiftUI 视图嵌入 UIKit

## 关联页面

- [[concepts/swift-fundamentals]] — Swift 语言基础（struct / 协议导向 / 尾随闭包）
- [[concepts/swift-concurrency]] — async/await 在 SwiftUI 中的使用
- [[projects/dayfold/dayfold]] — 实际 SwiftUI 项目参考
- [[projects/dayfold/concepts/swiftui-context-propagation]] — sheet context 注入陷阱
- [[projects/dayfold/concepts/fetchrequest-vs-observedobject]] — FetchRequest vs ObservedObject
- [[entities/ios17-app-development-book]] — 来源书籍
- [[references/cs193p-spring-2025]] — Stanford CS193P 课程（ViewBuilder / some View 讲解来源）
- [[skills/xcode-ide-guide]] — Preview Canvas 实时预览工作流
- [[skills/ios-multithreading]] — iOS 多线程
- [[skills/ios-networking]] — iOS 网络编程

## 相关

- [[synthesis/arc-memory-management × swift-concurrency]] — ARC 解决引用类型的生命周期问题（堆上何时释放），Actor 解决引用类型的并发访问问题（多线程何时安全读写）——两套机制作用在同一类型上但维度正交。
- [[references/ios-design-patterns]] — iOS/Swift 设计模式速查：创建型（5种）、结构型（7种）、行为型（11种）GoF 23种模式 + iOS 常见反模式清单。
