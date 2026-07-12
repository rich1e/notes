---
title: "用 battle-tested-patterns 系统学习代码级模式"
category: skills
tags:
  - learning-method
  - design-patterns
  - interview-prep
  - study-plan
sources:
  - "https://github.com/Totoro-jam/battle-tested-patterns"
created: 2026-07-08T07:14:00Z
updated: 2026-07-08T07:14:00Z
summary: 如何把 Totoro-jam/battle-tested-patterns 当系统学习材料：分阶段路径、配套练习、给 AI 编程助手装 adopt-pattern/audit-pattern 技能。
tier: supporting
lifecycle: draft
lifecycle_changed: 2026-07-08
base_confidence: 0.65
provenance:
  extracted: 0.6
  inferred: 0.4
  ambiguous: 0
visibility: public
relationships:
  - target: "[[entities/battle-tested-patterns]]"
    type: related_to
  - target: "[[references/pattern-catalog-battle-tested-patterns]]"
    type: related_to
  - target: "[[concepts/programming-pattern-categories]]"
    type: related_to
---

# 用 battle-tested-patterns 系统学习代码级模式

> 来自 [Totoro-jam/battle-tested-patterns](https://github.com/Totoro-jam/battle-tested-patterns) 项目的 [Learning Paths](https://totoro-jam.github.io/battle-tested-patterns/guide/learning-paths) + [STUDY_PLAN.md](https://github.com/Totoro-jam/battle-tested-patterns/blob/main/STUDY_PLAN.md) 提炼。

## 它能当教科书用的原因 ^[inferred]

一般的"设计模式"书只能告诉你"是什么"，而 battle-tested-patterns 在每个模式页都给出 ^[extracted]：

1. **一句话定义**（One Liner）
2. **真实类比**（Real-World Analogy）
3. **核心图示**（ASCII 框图）
4. **属性表**（并发/可扩展性/失败隔离等）
5. **交互式可视化**（46 个 Vue 组件，可拖拽、可时间旅行回放）
6. **生产证明**（≥ 2 个开源项目的精确行号引用）
7. **4 语言实现**（TypeScript / Rust / Go / Python，idiomatic 而非翻译）
8. **练习题**（2 难度，含 Vitest / cargo / go / pytest 跑得通的测试）
9. **挑战题**（184 个 "Guess what happens" 场景问）

## 推荐学习路径 ^[inferred]

以下路径假设你已经熟悉至少一门静态类型语言。

### 阶段 0：环境（30 分钟）

```bash
git clone https://github.com/Totoro-jam/battle-tested-patterns.git
cd battle-tested-patterns && pnpm install
pnpm dev               # 启文档站 http://localhost:5173
pnpm test              # 跑通所有 1,073+ 测试
```

只需要 Node.js ≥ 22 + pnpm ≥ 9。Rust/Go/Python 是可选 ^[extracted]。

### 阶段 1：数据结构打底（1–2 周）

从最贴近底层硬件/存储的类别开始 ^[inferred]：

1. **Bitmask** — 最简单，5 分钟能看懂可视化，但能引出 React 的 Flags / Linux 的 inode
2. **Ring Buffer** — Disruptor 那一段
3. **LRU Cache** — 几乎所有缓存库的基石
4. **Min Heap** → **Skip List** → **Trie** → **Bloom Filter**
5. **B+ Tree** + **LSM Tree** — 关系型 vs KV 存储的两种索引哲学（可结合 [leveldb-lsm](https://totoro-jam.github.io/battle-tested-patterns/case-studies/leveldb-lsm) 案例）

### 阶段 2：并发与内存（1–2 周）

按"模型 → 调度 → 内存"顺序 ^[inferred]：

1. **Semaphore** — 计数器的最简并发原语
2. **Mutex 缺席** — 项目里没有 Mutex 单独成项，因为锁思想被 Actor / Work Stealing 取代 ^[inferred]
3. **Actor Model** — 消息传递取代共享内存（读 Erlang/OTP 那段）
4. **Work Stealing** — Go 调度器和 Tokio
5. **Event Loop** — 浏览器/Node.js/Redis 都用它
6. **MVCC** — 数据库事务核心（结合 [postgres-mvcc](https://totoro-jam.github.io/battle-tested-patterns/case-studies/postgres-mvcc) 案例）
7. **Object Pool** → **Free List** → **Arena Allocator** — 内存分配三条路线

### 阶段 3：系统与行为（1 周）

这部分最"工程" ^[inferred]：

1. **Middleware Chain** — 任何 Web 框架都用到
2. **Circuit Breaker** + **Retry Backoff** + **Rate Limiter** — 分布式三大件
3. **Write-Ahead Log** + **Checkpointing** — 持久化两大件
4. **State Machine** + **Observer** + **Iterator** + **Visitor** + **Vtable** + **Diff/Patch** — 行为六君子

### 阶段 4：横向打通（持续）

每个模式都对应真实项目的精确代码 ^[extracted]。练手方法 ^[inferred]：

- 在 [[references/pattern-catalog-battle-tested-patterns]] 里挑一个模式，去 GitHub 找那个行号的源码读
- 用 `audit-pattern` 技能让 AI 评估你自己的代码库用了哪些模式
- 用 `adopt-pattern` 技能让 AI 给定一个业务问题推荐该用哪个模式 + 写一个回归测试

## 给 AI 编程助手装技能 ^[extracted]

```bash
# Claude Code 插件市场
/plugin marketplace add Totoro-jam/battle-tested-patterns
/plugin install pattern-skills@battle-tested-patterns

# 或者 npx skills（通用）
npx skills add Totoro-jam/battle-tested-patterns/plugins/pattern-skills
```

两个技能 ^[extracted]：

| 技能 | 用途 |
|---|---|
| **adopt-pattern** | 给定问题 → 推荐模式 + 适配到你的代码库 + 写回归测试 |
| **audit-pattern** | 给定代码库 → 评估模式使用情况 + 标记错用的 |

不安装也能直接用：技能会运行时从仓库拉模式页 URL ^[extracted]。

## 配套资料（站内）^[extracted]

项目自带 11 个指南页（`docs/guide/`）^[extracted]：

- `what-is-this.md` — 项目自我介绍
- `learning-paths.md` — 详细分层路径
- `pattern-comparison.md` — 模式之间怎么选
- `pattern-connections.md` — 模式之间的协作
- `complexity.md` — 时间/空间复杂度速查
- `cheatsheet.md` — 一页速记
- `interview.md` — 面试题整理
- `exercises.md` / `use-cases.md` — 练习与场景
- `how-to-contribute.md` — 想贡献时读
- `timeline.md` — 模式按时间线
- `STUDY_PLAN.md`（仓库根） — 进阶学习计划

## 我的笔记用法（站内联动）^[inferred]

当你已经掌握一个模式后，可以在该模式的 vault 页上记录 ^[inferred]：

- **首次遇到的生产代码** — 不只是"出处链接"，而是"在哪一段、为什么这样写"
- **和你自己代码库的对照** — "我们项目里的 XX 是不是这个模式的实现？"
- **面试时被问到的题** — "如果面试官问 MVCC，你能立刻说出 PostgreSQL 的 heap_page_prune 吗？"

后续可以用 [[concepts/...]] 给单个模式单独开概念页（不是这次 ingest 的目标，避免重复）。

## 提醒

- **不要试图一次学完 46 个** — 按上面的阶段分批，1 个月能覆盖核心
- **TypeScript 实现优先** — 其他 3 种语言是选学，但 TypeScript 是文档站同款
- **每学一个模式都跑一次可视化** — 时间旅行回放（`useVizHistory` composable）能让你看到"为什么这一步会触发这一步"

## 相关页面

- [[entities/battle-tested-patterns]] — 项目本体
- [[references/pattern-catalog-battle-tested-patterns]] — 46 模式完整目录
- [[concepts/programming-pattern-categories]] — 五大分类思路
