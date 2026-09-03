---
title: "SQLite for Everything — JoeCode"
category: references
tags:
  - sqlite
  - database
  - reference
  - infrastructure-simplification
summary: JoeCode 对 Raphael Bauer「PostgreSQL for Everything」的 SQLite 版回应，论证 SQLite 凭借零安装、进程内函数调用、单文件特性，可在更多场景替代 Solr/MongoDB/Kafka/Redis/ClickHouse/Neo4j 和微服务。
sources:
  - "https://joecode.com/2026-08-19-sqlite3/"
created: 2026-08-26T00:00:00Z
updated: 2026-08-26T00:00:00Z
tier: supporting
lifecycle: draft
lifecycle_changed: "2026-08-26"
base_confidence: 0.55
provenance:
  extracted: 0.88
  inferred: 0.10
  ambiguous: 0.02
relationships:
  - target: "[[entities/sqlite]]"
    type: derived_from
  - target: "[[concepts/database-as-platform]]"
    type: derived_from
  - target: "[[references/postgresql-for-everything]]"
    type: related_to
  - target: "[[concepts/postgres-extensions-ecosystem]]"
    type: related_to
---

# SQLite for Everything — JoeCode

> 作者核心论点：**SQLite 的答案比 PostgreSQL 还要极端——数据库不是一个 daemon，而是一个函数调用。** 每一次进程外跳转（网络、序列化、协议）都是你花出去的钱；SQLite 不花这个钱。

本文是对 [[references/postgresql-for-everything]] 的 SQLite 版本平行回应，覆盖完全相同的"多少专用系统可被替代"议题，只是用 SQLite 而非 PostgreSQL 来回答。

## 三大支柱

### 1. 极度稳定（Rock Solid）

- 首发：**2000 年**，26 年工程打磨
- 地球上部署量最大的数据库，没有之一：手机、浏览器、汽车、飞机
- 测试覆盖率：**100% branch coverage（MC/DC 标准）**，与航空电子软件相同
- 测试代码量约为库本身代码的 **500 倍**
- 支持承诺延伸至 **2050 年**
- 授权：**公有领域（Public Domain）**，无 CLA，无供应商风险

### 2. 零成本安装/运行

- 已预装在每个主流 Linux 发行版、Python、Ruby、PHP、Go、Rust、.NET、Android、iOS、macOS
- 测试数据库：`:memory:`，微秒级 spin-up，无 Docker，无端口冲突
- 服务器上"运行" SQLite = 它随 OS 一起来了，不需要再启动任何东西

### 3. 极简化基础设施（且更极端）

进程内函数调用 vs 网络跳转：
- Redis `GET` localhost：**~100μs**
- SQLite 点查询（热页缓存）：**~1μs**
- 没有连接池、TLS 握手、`pgbouncer`、序列化开销

## 11 个替代场景（对应原文）

### 1. 替代 Solr/Elastic：全文检索（FTS5）

内置 **FTS5** 引擎：Tokenizer、前缀/短语/NEAR 查询、BM25 排名、snippet/highlight。

关键优势：**搜索索引与数据在同一事务里更新**，索引永远不会过期（搜索 stale 问题的根本原因是你在运行两个系统）。

代表作：Simon Willison 的 Datasette 对多 GB SQLite 文件跑带刷选的全文搜索，毫秒返回，小 VM，免费。

参考：[SQLite FTS5 文档](https://sqlite.org/fts5.html)

### 2. 替代 MongoDB：JSON 支持

- 内置 JSON 函数：`->` / `->>` 操作符
- 3.45 起有 `jsonb`（二进制，免除每次重解析）
- 生成列 + 索引 = schemaless 写入 + 有索引的读取，一个文件

### 3. 替代 Kafka/RabbitMQ：队列

```sql
BEGIN IMMEDIATE;
UPDATE jobs SET status = 'running', worker = ?
WHERE id = (SELECT id FROM jobs WHERE status = 'pending'
            ORDER BY id LIMIT 1)
RETURNING *;
COMMIT;
```

- `BEGIN IMMEDIATE` 提前获取写锁，`RETURNING` 交还已认领行
- WAL 模式下读者不阻塞，监控查询不抢 worker
- **诚实的局限**：单写者，无 `SKIP LOCKED`，并发消费者在写锁上序列化。真正的数万 msg/s 会出问题。
- **建议**：先 SQLite，遇到真实数字时再去买 Kafka

对比 [[skills/postgres-queue-pattern]]（PostgreSQL SKIP LOCKED 模式）：SQLite 版更简单但并发上限更低。

### 4. 替代 ClickHouse：时序数据

SQLite 不直接复制 TimescaleDB，但给出务实方案：
- **按文件分区**：一 DB per 天/周/租户，存档 = `mv`，删除旧数据 = `rm`（常量时间，不 vacuum），跨库查询 = `ATTACH` + `UNION ALL` 视图
- **批写**：一事务 + 一万行 insert + 一 fsync，普通硬件几十万 rows/s
- **分析层**：用 **DuckDB 直接读 SQLite 文件**（原生支持），向量化 OLAP 无 ETL

### 5. 替代向量数据库（AI 工作流）

**`sqlite-vec`**：单文件、零依赖 C 扩展，支持 WASM（在浏览器里跑）。

核心优势：嵌入向量、原始文档、元数据、FTS 索引都在**同一个文件**，hybrid search = 一条 JOIN，不是三个系统的分布式查询。"RAG 索引 = 一个文件，可以邮件发送/打进 Docker 镜像/离线笔记本使用"。

### 6. 替代 Redis：缓存

```sql
PRAGMA journal_mode = WAL;
PRAGMA synchronous = OFF;  -- 缓存可以丢，放松一点
```

或 `:memory:`，或 `file:cache?mode=memory&cache=shared`。

过期：一列 `expires_at` + 定时 `DELETE WHERE expires_at < unixepoch()`——就是 Redis 替你做的事，只是更近。

性能：Redis localhost ~100μs，SQLite 热缓存 ~1μs，**移除依赖的同时变快了**。

### 7. 替代文件系统：小 blob 存储

SQLite 官方基准：**比文件系统快 35%**（≤100KB blob）。原因：文件系统每次 `open()` + `close()` + 目录遍历，SQLite 是一个已打开的文件句柄 + B-tree 查找。

附加收益：原子多 blob 更新、无崩溃时部分写、无文件名转义 bug、无"目录里 400 万 entry"问题、备份 = 一个文件。

### 8. 替代图数据库（层次/图）

- 递归 CTE 完整支持，官方文档质量是该领域最好的技术写作之一
- Closure table、materialized path（TEXT 列 + GLOB 索引，不如 LTREE 但够快）
- **simple-graph**：几百行 SQL 在 SQLite 上实现属性图（节点/边/遍历）
- "你的图大概有一万个节点，一万个节点放进 L3 cache，不需要 Neo4j"

### 9. 替代微服务

`json_object()` + `json_group_array()` = 查询结果直接序列化 JSON，序列化层消失。

更进一步：微服务是函数调用，没有 health check、retry、circuit breaker、distributed trace、网络 p99。**Datasette** = 指向 SQLite 文件，得到 JSON API + Web UI + 刷选搜索 + 插件生态，两个二进制文件 + 一个文件。

### 10–11. 彩蛋：替代 PS5

官方文档里有用递归 CTE 实现的 Mandelbrot 集渲染器、Conway 生命游戏、数独求解器、迷宫生成器，还有棋类引擎和 Doom 火焰效果。"一个把分形写进示例文档的数据库，你要尊重它。"

## SQLite vs PostgreSQL 的位置

| 维度 | SQLite | PostgreSQL |
|---|---|---|
| 部署模型 | 嵌入库，进程内 | 独立 daemon，网络连接 |
| 写并发 | 单写者（WAL 模式提升读） | 多并发写者 |
| 扩展生态 | 轻量扩展（sqlite-vec/FTS5） | 丰富扩展（[[concepts/postgres-extensions-ecosystem\|pgvector/AGE/TimescaleDB]]）|
| 测试便利性 | `:memory:`，微秒，无 Docker | Testcontainers，秒级 |
| 缩放上限 | 单机，几十 GB 实战 | 多机，PB 级可行 |
| 迁移路径 | 遇到单写者瓶颈 → PostgreSQL | 遇到单机瓶颈 → 分布式 |

两者不对立，是连续谱：SQLite → PostgreSQL → 专用系统，按真实瓶颈逐步升级。

## 相关

- [[entities/sqlite]]
- [[concepts/database-as-platform]]
- [[references/postgresql-for-everything]]
- [[skills/sqlite-queue-pattern]]
- [[concepts/sqlite-as-file-format]]
