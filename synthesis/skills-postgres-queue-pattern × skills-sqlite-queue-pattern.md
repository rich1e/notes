---
title: PostgreSQL Queue Pattern × SQLite Queue Pattern
category: synthesis
tags:
  - postgresql
  - sqlite
  - queue
  - patterns
  - database
sources:
  - "[[skills/postgres-queue-pattern]]"
  - "[[skills/sqlite-queue-pattern]]"
  - "[[concepts/database-as-platform]]"
  - "[[entities/postgresql]]"
  - "[[entities/sqlite]]"
created: 2026-08-27T08:30:00Z
updated: 2026-08-27T08:30:00Z
summary: "同一个队列模式在两种规模下的落地：SQLite BEGIN IMMEDIATE（进程内，<5K msg/s）vs PostgreSQL SKIP LOCKED（多消费者网络，~10K msg/s）。部署规模而非功能差异决定选型。"
provenance:
  extracted: 0.30
  inferred: 0.60
  ambiguous: 0.10
base_confidence: 0.78
lifecycle: draft
lifecycle_changed: "2026-08-27"
relationships:
  - target: "[[skills/postgres-queue-pattern]]"
    type: derived_from
  - target: "[[skills/sqlite-queue-pattern]]"
    type: derived_from
---

# PostgreSQL Queue Pattern × SQLite Queue Pattern

## The Connection

[[skills/postgres-queue-pattern]] 和 [[skills/sqlite-queue-pattern]] 解决的是**同一个问题**：无需引入专用消息中间件（Kafka/RabbitMQ）实现可靠的任务队列。两者的 SQL 语义有表面差异（`FOR UPDATE SKIP LOCKED` vs `BEGIN IMMEDIATE`），但底层机制完全同构：

- 都依赖**数据库行锁/事务写锁**实现互斥消费
- 都提供**至少一次投递**语义（需要幂等消费者）
- 都有**心跳清理**机制处理 crashed worker
- 都支持**优先级调度**和**指数退避重试**

选型的核心判断不是功能，而是**部署约束**：单进程还是多机多进程？

## Where They Co-occur

- **[[concepts/database-as-platform]]** — 两个 queue pattern 都作为「用数据库替代专用队列系统」的典型例子，以 `pattern_of` 关系链接到 database-as-platform
- **[[entities/sqlite]] × [[entities/postgresql]]** — 两个实体页都交叉引用了对方的 queue pattern，形成「进程内 vs 网络」对照
- **[[references/postgresql-for-everything]]** — Raphael Bauer 的文章把 `SKIP LOCKED` 作为 PostgreSQL 替代 Kafka 的核心论据，而 sqlite-queue-pattern 是同一论点在更小规模下的镜像

## Cross-cutting Insight

**队列模式的选型决策是「部署规模」函数，不是「功能需求」函数**。^[inferred]

| 决策维度 | SQLite 队列 | PostgreSQL 队列 |
|---|---|---|
| **部署单元** | 单进程 / 单机 | 多 worker / 多机 |
| **吞吐上限** | ~5K msg/s（WAL 模式） | ~10K msg/s（含索引） |
| **并发消费者** | 串行（写锁互斥） | 真并发（SKIP LOCKED） |
| **基础设施依赖** | 零（进程内） | PostgreSQL 实例 |
| **升级路径** | → PostgreSQL 队列 → PGMQ → Kafka |

两个 pattern 共同揭示了一条「复杂度阶梯」：

```
无队列（直接函数调用）
  ↓  吞吐 > 100/s 或需要持久化
SQLite BEGIN IMMEDIATE（进程内）
  ↓  需要多 worker 或跨机
PostgreSQL SKIP LOCKED（多消费者）
  ↓  > 10K msg/s 或需要 Consumer Group
PGMQ / Kafka（专用消息系统）
```

每一级的「升级触发条件」都很具体——这个阶梯的存在，本身就是 [[concepts/database-as-platform]] 「先用数据库，遇真实瓶颈再升级」论点的操作化。^[inferred]

## Tensions and Trade-offs

- **迁移摩擦**：从 SQLite 队列升级到 PostgreSQL 队列不是改一个连接字符串那么简单——表结构、事务语义、错误处理都需要调整。这个"迁移成本"是使用 database-as-platform 方案的隐性代价，专用消息系统（Kafka）往往从一开始就提供多级 scale 语义。
- **调试差异**：SQLite 队列的失败完全在进程内可检查，PostgreSQL 队列需要数据库连接和查询权限才能 debug。在 CI/测试环境中，SQLite 队列更容易 mock 和测试——但这恰好与 no-llm-hot-path 的「可重放」需求冲突：mocked queue 可能隐藏实际竞争条件。

## Strongest Objection

**"这个 synthesis 只是把两个已经相互 related 的页面放在一起，没有产生新洞见——那条「复杂度阶梯」在两个单独的页面里已经暗示了，不需要专门的 synthesis 页"。**

> test: 搜索现有的队列选型指南（比如 "when to use SQLite vs PostgreSQL vs Kafka for queues"），检查是否有公开文章把这三级阶梯放在同一框架下描述——如果有，这个 synthesis 就只是在重新发现已有的行业共识，独特价值有限。

## Open Questions

- **一致性升级路径**：是否有现成的迁移工具，能把 SQLite 队列「升级」为 PostgreSQL 队列而不需要 drain and replay？
- **观测性对称**：SQLite 队列的监控/告警与 PostgreSQL 队列的 pgAdmin/pg_cron 监控之间有一个观测性鸿沟——如何在两种模式下保持同等的可观测性？
- **测试策略**：在需要保证「SQLite 和 PostgreSQL 行为一致」的场景下（比如多环境部署），怎么设计测试策略？

## Related

- [[skills/postgres-queue-pattern]] — PostgreSQL SKIP LOCKED 实现
- [[skills/sqlite-queue-pattern]] — SQLite BEGIN IMMEDIATE 实现
- [[concepts/database-as-platform]] — 两者的哲学来源
- [[entities/postgresql]] — PostgreSQL 实体
- [[entities/sqlite]] — SQLite 实体
- [[references/postgresql-for-everything]] — Raphael Bauer 的 PostgreSQL 替代论文章
