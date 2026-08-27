---
title: 数据库即平台 — Database as Platform
category: concepts
tags:
  - database
  - architecture
  - postgresql
  - infrastructure-simplification
summary: "数据库即平台"是一种基础设施设计哲学：优先用单一数据库（SQLite 或 PostgreSQL）替代专用系统（Elasticsearch/Redis/Kafka/Neo4j），以降低运维复杂度为首要目标。核心原则：先用数据库，遇到真实瓶颈才引入专用工具。SQLite 是进程内极简端，PostgreSQL 是功能丰富多用户端，按需升级。
sources:
  - "https://www.raphaelbauer.com/posts/postgresql-everything/"
  - "https://amazingcto.com/posts/postgres-for-everything/"
  - "https://joecode.com/2026-08-19-sqlite3/"
created: 2026-08-26T00:00:00Z
updated: 2026-08-26T12:00:00Z
tier: core
lifecycle: established
lifecycle_changed: "2026-08-26"
base_confidence: 0.80
provenance:
  extracted: 0.75
  inferred: 0.20
  ambiguous: 0.05
relationships:
  - target: "[[entities/postgresql]]"
    type: exemplified_by
  - target: "[[entities/sqlite]]"
    type: exemplified_by
  - target: "[[concepts/postgres-extensions-ecosystem]]"
    type: enabled_by
---

# 数据库即平台 — Database as Platform

> 与其为每类数据问题引入一个专用系统，不如问：**"我的数据库能直接解决这个问题吗？"** 大多数时候，答案是肯定的。

## 核心论点

**专用工具的代价**不是功能，而是：
- 每多一个系统 → 多一套运维、监控、备份、升级流程
- 多一种部署依赖 → 本地开发/测试环境更复杂
- 多一个网络边界 → 延迟、序列化开销、一致性挑战
- 多一门技术 → 团队学习曲线、招聘要求

**数据库即平台的收益**：
- 一套备份恢复逻辑
- 一套监控告警
- ACID 事务跨越本来需要分布式协调的操作
- SQL 作为统一接口，无需学习多套查询语言

## 覆盖的专用工具场景

### PostgreSQL 方案

| 场景 | 替代对象 | PostgreSQL 方案 |
|---|---|---|
| 全文检索 | Elasticsearch / Solr | `tsvector`/GIN + pg_search/ParadeDB |
| 文档存储 | MongoDB | `jsonb` + GIN 索引 |
| 消息队列 | Kafka / RabbitMQ / SQS | `SKIP LOCKED` 模式 |
| 时序分析 | ClickHouse / InfluxDB | TimescaleDB 扩展 |
| 向量检索 | Pinecone / Milvus / Weaviate | pgvector / pgai |
| 高速缓存 | Redis | `UNLOGGED TABLE` + 触发器 TTL |
| 树形 / 层级数据 | 图数据库（树形场景）| LTREE 扩展 |
| 完整图数据库 | Neo4j | Apache AGE + openCypher |

### SQLite 方案（进程内，零网络跳转）

| 场景 | 替代对象 | SQLite 方案 |
|---|---|---|
| 全文检索 | Elasticsearch / Solr | 内置 **FTS5**（BM25/NEAR/snippet） |
| 文档存储 | MongoDB | `->` / `->>` / `jsonb`（3.45+）|
| 消息队列 | Kafka / RabbitMQ | `BEGIN IMMEDIATE` + `RETURNING` |
| 时序数据 | ClickHouse（中等量级）| 按文件分区 + ATTACH + DuckDB |
| 向量检索 | Pinecone / Milvus | **sqlite-vec** 扩展（支持 WASM）|
| 缓存 | Redis | `PRAGMA synchronous=OFF` / `:memory:` |
| 文件存储（小 blob）| 文件系统（≤100KB）| BLOB 列（快 35%，省 20% 空间）|
| 图数据（小规模）| Neo4j | 递归 CTE + **simple-graph** |

## 决策原则

### 何时用数据库替代专用工具

**适合**：
- 数据量未超过 PostgreSQL 的合理扩展上限（单机几十 TB 量级）
- 团队规模小（< 10 工程师）
- 需要跨数据类型的事务一致性
- 初创期，基础设施简单最重要

**不适合**：
- 已经遇到真实性能瓶颈（不是假想的）
- 数据规模超出单实例或扩展能力
- 需要专用系统的特定功能（例：Kafka 的消费者组 rebalancing、精确的 stream replay）

### 渐进原则

```
SQLite（嵌入式，进程内，单文件）
    → 并发写者真实瓶颈 / 多机部署需求
    → PostgreSQL（多写者，网络连接，功能丰富扩展）
        → 单机扩展上限 / 数亿级 QPS
        → 专用系统（Kafka / ClickHouse / Pinecone）
```

每一步迁移都需要"真实的、已经发生的"性能或功能瓶颈作为触发条件，而非预防性判断。

## 反模式

- **预防性复杂化**：在还没写第一行业务代码时就决定"肯定需要 Kafka 和 Elasticsearch"
- **工具信仰驱动**："这是 LinkedIn 的技术栈，所以我们也要用 Kafka" — 忽略了 LinkedIn 的规模前提
- **架构博士论文**：为了在简历上写"微服务 + Kafka + Redis + MongoDB"而过度工程化

## 代价与权衡

这个哲学并非没有代价：

| 代价 | 说明 |
|---|---|
| `jsonb` 的锋利性 | 用文档存储替代 MongoDB 需要谨慎的 schema 设计 |
| 扩展的成熟度差异 | Apache AGE（图）比 pgvector（向量）更新，社区规模更小 |
| PostgreSQL 本身的扩展上限 | 超大规模写入场景（亿级 QPS）确实需要专用系统 |
| 运维耦合 | 所有功能共享一个数据库实例，一个问题可能影响全部 |

## 典型案例

来源均已记录在 [[references/postgresql-for-everything]]：
- **Contentful** 从 Elasticsearch 迁回 Postgres 全文检索
- **The Guardian** 从 MongoDB 迁到 jsonb
- **Instacart** 将搜索基础设施迁到 Postgres

## Related

- [[entities/postgresql]]
- [[entities/sqlite]]
- [[concepts/postgres-extensions-ecosystem]]
- [[concepts/sqlite-as-file-format]]
- [[skills/postgres-queue-pattern]]
- [[skills/sqlite-queue-pattern]]
- [[references/postgresql-for-everything]]
- [[references/sqlite-for-everything]]
