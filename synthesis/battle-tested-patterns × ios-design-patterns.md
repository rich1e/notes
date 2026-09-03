---
title: battle-tested-patterns × iOS 设计模式速查
category: synthesis
tags: [design-patterns, mobile, swift, develop, reference]
sources:
  - "entities/battle-tested-patterns"
  - "references/ios-design-patterns"
  - "concepts/programming-pattern-categories"
  - "concepts/ios-app-architecture"
created: 2026-07-23T00:00:00Z
updated: 2026-07-23T00:00:00Z
summary: "GoF 23 种对象级设计模式 vs battle-tested-patterns 46 种代码级编程模式：两套语言的坐标轴不同，组合使用才能覆盖'对象如何协作'和'数据如何存活'两个维度。"
provenance:
  extracted: 0.35
  inferred: 0.55
  ambiguous: 0.10
base_confidence: 0.75
lifecycle: reviewed
lifecycle_changed: "2026-08-24"
relationships:
  - target: "[[entities/battle-tested-patterns]]"
    type: derived_from
  - target: "[[references/ios-design-patterns]]"
    type: derived_from
  - target: "[[concepts/programming-pattern-categories]]"
    type: related_to
---

# battle-tested-patterns × iOS 设计模式速查

## The Connection

两套模式系统经常被混为一谈，但它们回答的是不同的问题：

- **GoF（iOS 设计模式）** 问的是："这几个对象应该如何互相调用？"（Observer、Factory、Delegate）
- **battle-tested-patterns** 问的是："这块数据应该如何在内存中存活和变化？"（LRU、Copy-on-Write、Bloom Filter）

前者的单位是**对象关系**，后者的单位是**数据生命周期**。^[inferred]

## Where They Co-occur

在 iOS 开发的实际场景中，两套模式经常在同一个功能里同时出现：

| 功能 | GoF 模式 | battle-tested 模式 |
|---|---|---|
| 图片缓存 | Proxy（缓存代理）| LRU Cache（淘汰策略）|
| 通知推送 | Observer（消息广播）| Ring Buffer（高频写入存储）|
| UI 主题切换 | Strategy（运行时替换算法）| Copy-on-Write（主题 struct 修改）|
| CoreData 堆栈 | Singleton（全局访问点）| B+ Tree（底层索引结构）|
| Combine/Rx 流 | Iterator（遍历序列）| Actor（并发安全访问）|

两者在 [[references/pattern-catalog-battle-tested-patterns]] 和 [[references/ios-design-patterns]] 中均有详细条目，但均未交叉引用。^[extracted]

## Cross-cutting Insight

**GoF 模式决定"谁调用谁"，battle-tested 模式决定"存在多久、存多少、怎么变"。** ^[inferred]

一个完整的系统需要两类问题都有答案。但工程上的常见缺陷是：

- 用 GoF 的 Singleton 回答"全局缓存放哪儿"，却没有配套的 LRU 或 TTL——对象图干净了，但内存增长无界
- 用 battle-tested 的 Copy-on-Write 回答"值类型安全"，却没有 Observer 在值变化时通知 UI——数据安全了，但 UI 不更新

在 Swift 生态中，`@Published`（Observable 模式，属于 GoF 的 Observer 变体）和 struct 的 Copy-on-Write（battle-tested 的内存模式）经常同时出现在同一个 `@ObservableObject` 中，形成一个两层模式的组合。^[extracted]

## Tensions and Trade-offs

**命名冲突**

GoF 的"行为型模式"（Behavioral）和 battle-tested-patterns 的行为分类名字相同，含义不同。前者指对象响应变化的协作协议（Strategy、Command、State），后者指代码在运行时的内存访问行为（Lazy Init、Flyweight 式共享）。在代码评审中不澄清语境，两种"行为模式"会引发无效争论。^[inferred]

**粒度错配**

GoF 的 Factory 模式创建**对象**，battle-tested 的 Object Pool 管理**对象集合的生命周期**——两者可以叠加：用 Factory 创建对象，用 Object Pool 控制是否复用。但分别学习两套模式的开发者可能只知道其中一半。^[inferred]

## Strongest Objection

"GoF 和 battle-tested-patterns 的关系不需要综合，因为它们没有重叠——一个讲结构，一个讲算法，分开用就行。这篇合成页描述的'两层组合'只是把两个独立工具放在一起使用的常识，不构成洞见。"

> test: 从 [[references/pattern-catalog-battle-tested-patterns]] 取 10 个模式，从 [[references/ios-design-patterns]] 取 10 个模式，检查它们是否能在实际代码中独立应用（互不依赖）。如果 90% 的模式可以独立使用，则"组合使用才完整"的论点不成立，两套系统确实是独立的工具箱。

## Open Questions

- SwiftUI 的 `@Observable` macro（Swift 5.9）是否是 GoF Observer 的官方 Swift 实现？与 Combine 的 `@Published` 有何本质区别？
- battle-tested-patterns 的 46 种模式中，有多少在 Swift 标准库或 Foundation 中已有官方实现（如 `Array` 的 Copy-on-Write）？这些隐式实现的模式是否需要开发者显式了解？
- iOS 新的 SwiftData 框架是否引入了新的代码级模式，还是复用了 Core Data 时代的 battle-tested 方案？

## Related

- [[entities/battle-tested-patterns]] — 46 种代码级模式目录
- [[references/ios-design-patterns]] — GoF 23 种模式 iOS 速查
- [[concepts/programming-pattern-categories]] — battle-tested 的五分类框架
- [[concepts/ios-app-architecture]] — 架构层的 MVC/MVVM/VIPER
- [[references/pattern-catalog-battle-tested-patterns]] — 完整模式目录（含源码引用）
