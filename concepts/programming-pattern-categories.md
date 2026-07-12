---
title: "编程模式五大分类（数据结构/并发/系统/内存/行为）"
category: concepts
tags:
  - design-patterns
  - programming-patterns
  - taxonomy
  - concepts
sources:
  - "https://github.com/Totoro-jam/battle-tested-patterns"
created: 2026-07-08T07:14:00Z
updated: 2026-07-08T07:14:00Z
summary: battle-tested-patterns 提出的"代码级"模式分类法：数据结构/并发/系统/内存/行为，按运行时职责切分，与 GoF 设计模式互补而非替代。
tier: supporting
lifecycle: draft
lifecycle_changed: 2026-07-08
base_confidence: 0.7
provenance:
  extracted: 0.5
  inferred: 0.5
  ambiguous: 0
visibility: public
relationships:
  - target: "[[entities/battle-tested-patterns]]"
    type: related_to
  - target: "[[references/pattern-catalog-battle-tested-patterns]]"
    type: related_to
  - target: "[[references/ios-design-patterns]]"
    type: related_to
---

# 编程模式五大分类

> 源自 [Totoro-jam/battle-tested-patterns](https://github.com/Totoro-jam/battle-tested-patterns) 的 46 模式分类视角 ^[extracted]。这是一种**代码级**（code-level）的模式分类法，关注"运行时职责"，与 GoF 的**对象级**（object-level）设计模式互补。

## 五大分类 ^[extracted]

| 分类 | 数量 | 关注点 | 典型模式 |
|---|---|---|---|
| 🧠 **数据结构** | 11 | 数据如何在内存/磁盘组织 | Bitmask, LRU, B+ Tree, Trie, Bloom Filter |
| ⚡ **并发** | 9 | 多执行单元如何安全协作 | Actor Model, Work Stealing, MVCC, Event Loop |
| 🏗️ **系统** | 12 | 分布式/服务间如何通信与容错 | Circuit Breaker, Rate Limiter, WAL, Consistent Hashing |
| ♻️ **内存** | 8 | 如何减少分配/释放开销 | Object Pool, Arena Allocator, Free List, COW, RC |
| 🔄 **行为** | 6 | 对象/节点之间如何交互 | State Machine, Observer, Iterator, Visitor |

## 切分逻辑 ^[inferred]

切分维度是**运行时职责**，不是**抽象层次**：

- 数据结构回答：**"数据放哪儿、怎么找"**
- 并发回答：**"多线程/多协程怎么不打架"**
- 系统回答：**"服务/进程之间怎么不挂"**
- 内存回答：**"分配/释放怎么不慢"**
- 行为回答：**"控制流怎么走、不走错"**

一个具体实现可能跨多个分类（PostgreSQL 的 MVCC 既是并发也是系统），但每个模式只挂在最能解释它"为什么存在"的那一类 ^[inferred]。

## 与 GoF 设计模式的关系

| | GoF | battle-tested-patterns |
|---|---|---|
| **关注层** | 对象/类 | 函数/数据结构/协议 |
| **抽象度** | 高度抽象（"做什么"） | 具体实现（"在哪个源文件哪一行"） |
| **覆盖范围** | 23 个模式，OOP 为主 | 46 个模式，横跨多语言多领域 |
| **证明方式** | 教科书示例 | 真实开源项目（React/Linux/Go…）精确行号 |
| **典型读者** | 面向对象开发者 | 系统/后端/基础设施工程师 |

**两套体系并不冲突，而是正交** ^[inferred]：
- 一个 Event Loop 实现内部，**用** Observer 模式解耦事件源与处理器
- 一个 Merkle Tree 实现，**用** Visitor 模式遍历节点
- 一个 Actor Model 框架，**用** State Machine 管理 actor 生命周期

> vault 内已有 [[references/ios-design-patterns]] 记述 Apple 生态的常用设计模式（更多是对象/类层级），与本页面所讲的代码级模式分类形成对照。

## 五大分类的边界争议 ^[ambiguous]

不是所有模式都只属于一类 ^[inferred]：

- **Iterator** 可以放数据结构（数据结构视图）也可以放行为（控制流视图）
- **MVCC** 介于并发（隔离性）和系统（事务持久化）之间
- **Dirty Flag** 既是行为（何时触发），也是性能优化（内存视图）

项目自己的处理方式是：**给每个模式定一个"主类别"+ 在"by-project"和"pattern-connections"两个维度里再建立横向链接** ^[extracted]。

## 为什么这个分类法值得记

- **不再以"OOP/FP/过程"分** — 现代代码仓库里这些边界是模糊的，按职责分更直接
- **面试时比 GoF 更有杀伤力** — 面试官多半读过 GoF，但很少有人能讲清 MVCC 在 PostgreSQL 和 etcd 实现的差异
- **工程导向** — 每个模式都对应一段"如果你的场景长这样，就该用这个"的判断

## 相关页面

- [[entities/battle-tested-patterns]] — 项目本体
- [[references/pattern-catalog-battle-tested-patterns]] — 46 模式完整目录
- [[skills/pattern-study-method]] — 怎么用这套分类法系统学习
- [[references/ios-design-patterns]] — Apple 生态的对象级设计模式（对照）
