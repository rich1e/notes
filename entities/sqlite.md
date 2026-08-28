---
title: SQLite
category: entities
tags:
  - sqlite
  - database
  - embedded-database
  - open-source
summary: 全球部署量最大的数据库引擎，公有领域，嵌入式，进程内函数调用而非网络 daemon。2000 年首发，支持承诺至 2050 年，内置 FTS5 全文检索、JSON、递归 CTE，可通过扩展支持向量检索。
sources:
  - "https://joecode.com/2026-08-19-sqlite3/"
  - "https://sqlite.org/fts5.html"
created: 2026-08-26T00:00:00Z
updated: 2026-08-26T00:00:00Z
tier: core
lifecycle: verified
lifecycle_changed: "2026-08-28"
base_confidence: 0.85
provenance:
  extracted: 0.85
  inferred: 0.12
  ambiguous: 0.03
relationships:
  - target: "[[concepts/database-as-platform]]"
    type: exemplified_by
  - target: "[[entities/postgresql]]"
    type: related_to
  - target: "[[references/sqlite-for-everything]]"
    type: derived_from
  - target: "[[skills/sqlite-queue-pattern]]"
    type: related_to
  - target: "[[concepts/sqlite-as-file-format]]"
    type: related_to
---

# SQLite

> "Contrary to popular belief, the answer to everything is NOT 42. It's SQLite." — JoeCode

SQLite 是地球上**部署量最大的数据库引擎**，比其他所有数据库加起来还多。它在你的手机里、浏览器里、汽车里、飞机上。

## 基本信息

| 属性 | 值 |
|---|---|
| 首发年份 | 2000 年 |
| 授权 | **公有领域（Public Domain）** — 无 CLA、无供应商 |
| 支持承诺 | 至 **2050 年** |
| 架构 | 嵌入式库，进程内，**不是 daemon** |
| 存储 | 单文件（或 `:memory:`） |
| 测试覆盖 | 100% MC/DC branch coverage（航空电子软件标准），测试代码量约为库代码的 **500 倍** |

## 核心特性

### 零基础设施成本
- 随每个主流 Linux 发行版、Python、Ruby、PHP、Go、Rust、.NET、Android、iOS、macOS 预装
- 测试：`:memory:` 数据库，微秒级创建，无 Docker，无端口，无配置
- 服务器运行 SQLite = 已经在运行了，随 OS 而来

### 性能特性
- **无网络跳转**：查询是函数调用，延迟从 ms 级降到 μs 级
- vs Redis GET (localhost)：SQLite 点查热缓存约 **1μs**，Redis 约 **100μs**（快约 100 倍）
- vs 文件系统：≤100KB blob 读写比原始文件系统**快 35%**（官方基准），因为省去了 open/close/目录遍历

### 并发模型
- **单写者**（WAL 模式下读者不阻塞写者）
- 写操作序列化，并发消费者在写锁上等待
- 不支持 `SKIP LOCKED`（[[entities/postgresql|PostgreSQL]] 队列模式的核心，见 [[skills/postgres-queue-pattern]]）
- 适合读多写少、中低并发场景

## 内置能力（无需扩展）

| 能力 | 技术 | 替代哪类系统 |
|---|---|---|
| 全文检索 | **FTS5**（BM25 排名/NEAR/snippet） | Solr / Elasticsearch |
| JSON 存储 | `->` / `->>` / `jsonb`（3.45+）| MongoDB |
| 消息队列 | `BEGIN IMMEDIATE` + `RETURNING` | Kafka（低吞吐量） |
| 时序数据 | 按文件分区 + ATTACH + 批写 | ClickHouse（中等量级）|
| 缓存 | `PRAGMA synchronous=OFF` / `:memory:` | Redis |
| 文件存储 | BLOB 列 | 文件系统（小 blob）|
| 层次/图数据 | 递归 CTE + materialized path | Neo4j（小图）|

## 生态扩展

| 扩展 | 功能 |
|---|---|
| **sqlite-vec** | 向量检索，单文件 C，支持 WASM，RAG 场景 |
| **Litestream** | WAL 持续流式备份到 S3 |
| **LiteFS** | 分布式读，跨节点 SQLite |
| **DuckDB** | 直接读 SQLite 文件，向量化 OLAP（无 ETL）|
| **Turso** | 托管 SQLite，边缘分发 |
| **Cloudflare D1** | SQLite 托管，Cloudflare Workers 集成 |
| **rqlite** | 分布式 SQLite，Raft 共识 |
| **simple-graph** | 基于 SQLite 表实现属性图（节点/边/遍历）|

## 使用边界与升级路径

```
SQLite
  → 遇到单写者并发瓶颈（数万 msg/s 队列，高并发写入）
  → 迁移到 PostgreSQL（仍是单机，但多写者）
      → 遇到单机瓶颈
      → 引入专用系统（Kafka / ClickHouse / Pinecone）
```

**升级信号**（何时离开 SQLite）：
- 并发写者数量使单写者成为真实瓶颈（不是假想的）
- 需要 Consumer Group Rebalancing（Kafka 特有语义）
- 需要多数据中心的分布式写入协调
- 数据量超出单机 SSD 的合理范围（通常是数百 GB 到 TB 级）

## 为什么 SQLite 能做到这些

**核心原因**：SQLite 消除了"系统边界"。你的数据不需要跨越进程、网络、序列化协议才能被处理。

- 搜索索引 + 数据 = 同一事务，永远不会 stale
- 嵌入向量 + 文档 + 元数据 + FTS = 同一个文件，hybrid search = JOIN
- 缓存 + 业务数据 = 同一进程，无网络开销
- 队列 + 业务状态 = 同一事务，消息永远不离开机器

## 相关

- [[entities/postgresql]]
- [[concepts/database-as-platform]]
- [[references/sqlite-for-everything]]
- [[skills/sqlite-queue-pattern]]
- [[concepts/sqlite-as-file-format]]
- [[synthesis/entities-sqlite × entities-postgresql]] — synthesis: 同一哲学的进程内端与网络端
