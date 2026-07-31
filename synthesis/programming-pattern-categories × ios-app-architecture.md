---
title: 编程模式五大分类 × iOS 架构模式
category: synthesis
tags: [design-patterns, app-architecture, ios, swift, programming]
sources:
  - "concepts/programming-pattern-categories"
  - "concepts/ios-app-architecture"
  - "entities/battle-tested-patterns"
  - "references/ios-design-patterns"
  - "concepts/swift-fundamentals"
created: 2026-07-23T00:00:00Z
updated: 2026-07-23T00:00:00Z
summary: "battle-tested-patterns 的代码级五分类与 iOS MVC/MVVM/VIPER 架构模式在不同抽象层操作——两套语言描述同一个软件的不同截面，用对工具避免混淆两层问题。"
provenance:
  extracted: 0.25
  inferred: 0.65
  ambiguous: 0.10
base_confidence: 0.72
lifecycle: draft
lifecycle_changed: 2026-07-23
relationships:
  - target: "[[concepts/programming-pattern-categories]]"
    type: derived_from
  - target: "[[concepts/ios-app-architecture]]"
    type: derived_from
  - target: "[[entities/battle-tested-patterns]]"
    type: related_to
  - target: "[[references/ios-design-patterns]]"
    type: related_to
---

# 编程模式五大分类 × iOS 架构模式

## The Connection

开发者经常把两个问题混在一起问："我应该用 MVVM 还是 VIPER？"和"我怎么管理这个缓存？"这是两个不同层次的问题，对应两套不同的模式语言。^[inferred]

[[concepts/programming-pattern-categories]]（battle-tested-patterns）的五分类关注**运行时职责**：数据在内存中怎么存，并发任务怎么调度，系统资源怎么管理。[[concepts/ios-app-architecture]]（MVC/MVVM/VIPER）关注**组件间职责边界**：Model、View、Controller/ViewModel 各自负责什么，信息如何单向或双向流动。

这两套语言操作的是同一个代码库的不同截面——横切面（代码级模式）vs 纵切面（架构层次）。^[inferred]

## Where They Co-occur

**Dayfold 项目是两层同时出现的典型**：[[projects/dayfold/dayfold]] 采用 MVVM 架构（组件职责边界），同时内部使用了多个代码级模式——`CoreDataStack.shared` 是 Singleton（行为模式）；软删除用 `deletedAt` 时间戳是 Tombstone（系统模式）；图片脏标记是 Dirty Flag（内存模式）。^[extracted]

**[[references/ios-design-patterns]] 的 GoF 23 种**处在两者之间的中间层：Factory、Observer、Delegate 是对象级模式，描述类的协作关系，比架构模式细，比代码级模式粗。

## Cross-cutting Insight

**三层模式语言覆盖了软件设计问题的不同粒度。** ^[inferred]

| 层次 | 代表 | 粒度 | 典型问题 |
|---|---|---|---|
| 架构模式 | MVVM, VIPER, MVC | 模块/组件 | 谁拥有数据？谁驱动 UI 更新？ |
| 对象模式（GoF） | Factory, Observer, Singleton | 类/对象 | 如何创建对象？如何传递变更通知？ |
| 代码级模式（battle-tested） | LRU, Actor, Copy-on-Write | 数据结构/算法 | 内存如何分配？并发如何安全？ |

问题出在：选错抽象层解决问题。用 MVVM 解决"如何缓存网络图片"是在架构层解决代码级问题；用 LRU 解决"ViewModel 和 View 谁应该持有数据"是在代码级解决架构层问题。^[inferred]

iOS 开发中最常见的混淆：把 `CoreDataStack.shared`（代码级 Singleton 模式）当成架构决策讨论，实际上 Singleton 在三种架构（MVC/MVVM/VIPER）下都可以存在，它是实现细节，不是架构选择。^[extracted]

## Tensions and Trade-offs

**语言互借的混乱**

battle-tested-patterns 的"行为模式"（Behavioral）和 GoF 的"行为型模式"同名但范畴不同。前者指内存访问行为（Copy-on-Write、Lazy Initialization），后者指对象协作行为（Observer、Strategy）。在团队讨论中不澄清层次，两种"行为模式"会被混用。^[inferred]

**VIPER 的过度分层**

VIPER 在大型项目中引入了 5 层（View/Interactor/Presenter/Entity/Router），与 battle-tested-patterns 的代码级分层叠加，导致一个功能可能需要在 10+ 个文件中追踪。代码级模式的横切性质（一个 LRU 可能被多个 Interactor 共享）在 VIPER 的纵向分层中变得难以安置。^[inferred]

## Strongest Objection

"两套模式分别出自不同作者和生态——battle-tested-patterns 是开源社区归纳，iOS 架构模式是 Apple 官方 + 社区实践——它们的'共现'只是 iOS 开发者同时需要两者，而不是两者之间有理论连接。类比：厨师同时需要刀工技巧和菜谱，但刀工和菜谱不构成'交叉综合'。"

> test: 找一个非 iOS 的 Swift 项目（如 Vapor 后端），检查 battle-tested-patterns 的分类在其中的使用密度是否与 iOS 前端相近。如果后端项目的代码级模式使用率相似但架构模式完全不同（无 MVVM），则说明两套语言是独立的，本页的"互补"关系是偶然并置而非必然连接。

## Open Questions

- Swift 5.9 的 Macros 是否开辟了第四层——"语言级模式"（语法变换），需要在三层框架之外单独处理？
- [[concepts/programming-pattern-categories]] 的内存分类（Copy-on-Write、Reference Counting）与 ARC 的关系：ARC 是一个内存管理*机制*，Copy-on-Write 是一个内存管理*模式*，两者如何在 Swift 中协同？
- 在 SwiftData（Swift 5.9 新增）取代 Core Data 的场景下，Soft Delete 等传统 Core Data 模式是否有对应的 SwiftData 版本？

## Related

- [[concepts/programming-pattern-categories]] — 代码级五分类体系
- [[concepts/ios-app-architecture]] — MVC/MVVM/VIPER/Redux 对比
- [[entities/battle-tested-patterns]] — 46 模式目录项目
- [[references/ios-design-patterns]] — GoF 23 种模式速查
- [[projects/dayfold/dayfold]] — 两层模式同时出现的实例
