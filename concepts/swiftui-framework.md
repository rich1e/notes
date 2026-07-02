---
title: SwiftUI 框架
category: concepts
tags: [swiftui, ios, design-system, swift, architecture]
sources: ["buckets/books/iOS 17 App Development for Beginners.epub"]
created: 2026-07-01T00:00:00Z
updated: 2026-07-01T00:00:00Z
summary: SwiftUI 声明式 UI 框架核心：View 协议、布局容器（VStack/HStack/ZStack）、状态管理（@State/@Binding/@ObservedObject/@EnvironmentObject）、修饰符链式调用。
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

`some View` 是不透明返回类型（Opaque Type），编译器推断具体类型。

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

- [[concepts/swift-fundamentals]] — Swift 语言基础
- [[concepts/swift-concurrency]] — async/await 在 SwiftUI 中的使用
- [[projects/dayfold/dayfold]] — 实际 SwiftUI 项目参考
- [[projects/dayfold/concepts/swiftui-context-propagation]] — sheet context 注入陷阱
- [[projects/dayfold/concepts/fetchrequest-vs-observedobject]] — FetchRequest vs ObservedObject
- [[entities/ios17-app-development-book]] — 来源书籍
- [[skills/ios-multithreading]] — iOS 多线程
- [[skills/ios-networking]] — iOS 网络编程

- [[skills/ios-networking]] — iOS 网络编程
