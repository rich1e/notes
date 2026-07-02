---
title: iOS 架构模式
category: concepts
tags: [ios, architecture, swiftui]
sources: ["buckets/books/iOS 17 App Development for Beginners.epub"]
created: 2026-07-01T00:00:00Z
updated: 2026-07-01T00:00:00Z
summary: iOS 主流架构模式对比：MVC（UIKit 默认）、MVVM（SwiftUI 推荐）、VIPER（大型项目）、Redux/MVI（单向数据流）及反模式速查。
base_confidence: 0.86
lifecycle: draft
lifecycle_changed: "2026-07-01"
tier: core
provenance:
  extracted: 0.80
  inferred: 0.20
  ambiguous: 0.00
---

# iOS 架构模式

## MVC（Model-View-Controller）

UIKit 的**默认架构**，Apple 官方推荐用于 Storyboard 开发。

```
Model ←→ Controller ←→ View
```

- **Model**：数据与业务逻辑（struct/class）
- **View**：UIView、XIB、Storyboard
- **Controller**：UIViewController，协调 Model 与 View

**痛点**：Controller 过重（Massive View Controller），难以测试；View 与 Controller 紧耦合。

## MVVM（Model-View-ViewModel）

SwiftUI 与 Combine 的**天然搭档**，dayfold 采用此架构。

```
Model ← ViewModel → View（双向绑定）
```

- **Model**：纯数据（Core Data NSManagedObject、API 响应 struct）
- **ViewModel**：`ObservableObject`，持有 `@Published` 属性，处理业务逻辑
- **View**：SwiftUI View，通过 `@ObservedObject`/`@StateObject` 绑定 ViewModel

```swift
class PostViewModel: ObservableObject {
    @Published var posts: [Post] = []
    @Published var isLoading = false

    func fetchPosts() async {
        isLoading = true
        posts = await PostService.shared.fetchAll()
        isLoading = false
    }
}

struct PostListView: View {
    @StateObject var viewModel = PostViewModel()

    var body: some View {
        List(viewModel.posts) { post in PostRow(post: post) }
            .task { await viewModel.fetchPosts() }
    }
}
```

**优势**：可测试（ViewModel 不依赖 UI）；SwiftUI 双向绑定原生支持。  
**参见**：[[projects/dayfold/concepts/architecture-overview]]

## VIPER

适合**大型复杂项目**，职责划分极细：

| 层 | 职责 |
|---|---|
| **V**iew | 只负责展示，无逻辑 |
| **I**nteractor | 业务逻辑 |
| **P**resenter | View ↔ Interactor 的协调者 |
| **E**ntity | 数据模型 |
| **R**outer | 导航/路由 |

优势：各层可独立测试，职责单一。  
缺点：样板代码量大，小项目过度设计。

## Redux / MVI（单向数据流）

受 React/Flux 启发，适合状态复杂的 App：

```
Action → Reducer → Store(State) → View → Action（循环）
```

- **State**：单一不可变状态树
- **Action**：描述"发生了什么"的 enum
- **Reducer**：纯函数 `(State, Action) -> State`

```swift
enum AppAction {
    case incrementCounter
    case setUsername(String)
}

struct AppState {
    var counter = 0
    var username = ""
}

func reducer(state: AppState, action: AppAction) -> AppState {
    var newState = state
    switch action {
    case .incrementCounter:   newState.counter += 1
    case .setUsername(let n): newState.username = n
    }
    return newState
}
```

常用库：`TCA`（The Composable Architecture）、`ReSwift`。

## 架构对比速查

| 维度 | MVC | MVVM | VIPER | Redux |
|---|---|---|---|---|
| 复杂度 | 低 | 中 | 高 | 高 |
| 可测试性 | 低 | 高 | 高 | 高 |
| SwiftUI 适配 | 差 | 原生 | 可用 | 可用 |
| 适用规模 | 小型 | 中型 | 大型 | 状态复杂 |
| 学习曲线 | 平缓 | 中等 | 陡峭 | 中等 |

## 常见反模式

- **Massive View Controller**：把所有逻辑堆在 ViewController，违反单一职责
- **Service Locator 滥用**：隐式依赖，难以测试
- **Singleton 滥用**：全局状态难以追踪，循环引用风险
- **直接在 View 层调用网络**：跳过 ViewModel/Presenter，耦合 UI 与 IO

详细反模式速查参见 [[references/ios-design-patterns]]。

## 关联页面

- [[concepts/swiftui-framework]] — SwiftUI 状态管理
- [[concepts/swift-concurrency]] — async/await 与架构
- [[projects/dayfold/concepts/architecture-overview]] — dayfold 实际 MVVM 架构
- [[references/ios-design-patterns]] — 23 种设计模式分类
- [[entities/ios17-app-development-book]] — 来源书籍
