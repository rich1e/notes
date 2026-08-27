---
title: "PostgreSQL for Everything — Raphael Bauer"
category: references
tags:
  - postgresql
  - database
  - reference
summary: Raphael Bauer 的文章，论证 PostgreSQL 凭借稳定性、易安装性和生态扩展，可替代 Elasticsearch/MongoDB/Kafka/Redis/Neo4j 等 11 种专用系统，是基础设施简化的默认选择。
sources:
  - "https://www.raphaelbauer.com/posts/postgresql-everything/"
created: 2026-08-26T00:00:00Z
updated: 2026-08-26T00:00:00Z
tier: supporting
lifecycle: draft
lifecycle_changed: "2026-08-26"
base_confidence: 0.55
provenance:
  extracted: 0.90
  inferred: 0.08
  ambiguous: 0.02
relationships:
  - target: "[[entities/postgresql]]"
    type: derived_from
  - target: "[[concepts/database-as-platform]]"
    type: derived_from
  - target: "[[concepts/postgres-extensions-ecosystem]]"
    type: derived_from
---

# PostgreSQL for Everything — Raphael Bauer

> 作者核心论点：**遇到新技术需求，先问「PostgreSQL 能不能做到？」，确认真的遇到瓶颈再引入专用系统，而不是预防性地叠加工具栈。**

## 作者背景

- Raphael Bauer，从 **2003 年**（ColumbaDB 研究项目）就开始用 PostgreSQL
- 当时 MySQL 主导市场，但缺全文检索、SQL 合规性差；PostgreSQL 像"开源版 Oracle 的缩影"

## 三大支柱论点

### 1. Rock Solid & Stable
- 第一版发布：**1996 年**，Bug 被 30 年社区打磨掉
- 社区持续添加功能（JSON 存储、分区、CTE）而不破坏已有功能

### 2. 安装与扩展便捷
| 场景 | 方案 |
|---|---|
| Linux | `apt-get install postgresql` |
| macOS | Homebrew / **PostgresApp** |
| 测试 | **Testcontainers**（与生产完全一致的真实 DB）|
| 容器 | `docker pull postgres` |
| 托管云 | AWS RDS / GCP Cloud SQL / Azure / ElephantSQL / CrunchyData / Timescale |

### 3. 极简化基础设施
用一个系统覆盖 11 种使用场景（详见下方各节），大幅降低运维复杂度。

## 11 个使用场景

### 场景 1：全文检索（替代 Solr/Elasticsearch）
- 内置 `tsvector` / `tsquery` + **GIN 索引**
- 真实案例：Contentful、Instacart 均迁移到 Postgres 全文检索
- 如果还需要更强：`pg_textsearch`（BM25 排名）/ `pg_search` / ParadeDB（基于 Tantivy，Elasticsearch 级）
- **建议**：先用原生 → 真正遇到瓶颈再用扩展

### 场景 2：JSON 文档存储（替代 MongoDB）
- 原生 `jsonb` 类型 + GIN 索引让 JSON 查询快
- 真实案例：The Guardian 公开记录从 MongoDB 迁移到 PostgreSQL
- **警告**：作者称 `jsonb` 是"一把锋利的刀"——需谨慎使用

### 场景 3：消息队列（替代 Kafka/RabbitMQ/SQS）
关键 SQL：
```sql
SELECT ... FOR UPDATE
SELECT ... SKIP LOCKED
```
- 支持持久化扇出（cursor + 多消费者）或一次性读取模式
- 详细方案见 CrunchyData 文档
- **建议**：先用 Postgres → 真正性能不足再迁 Kafka/RabbitMQ

### 场景 4：时序 / 分析（替代 ClickHouse）
- 扩展：**TimescaleDB**
- 作者亲身在 Privatracker 项目用于高量 web 分析聚合统计

### 场景 5：向量数据库（AI/LLM 场景）
- 扩展：**pgvector** / **pgai**（含 LLM 模型调用 + 相似度检索）
- 可实现 RAG 工作流，无需单独向量数据库

### 场景 6：缓存（替代 Redis）
- 核心技术：**UNLOGGED 表**（无 WAL = 写入快得多）+ **触发器**模拟 TTL/过期
- 适合 session 等临时数据

### 场景 7：二进制 / 文件存储（替代文件系统）
- 特定工作负载下可超越原始文件系统读写
- 作者方案：blob 列 + **Flatbuffers** 序列化，客户端侧反序列化

### 场景 8：层次 / 树形数据（替代图数据库的树形场景）
- 扩展：**LTREE 数据类型**
- 比递归 CTE 更可读、更快、有索引；适合标签层次、分类树

### 场景 9：完整图数据库（替代 Neo4j）
- 扩展：**Apache AGE**（Apache 顶级项目）
- 实现 **openCypher** 查询语言（与 Neo4j 相同）

```sql
SELECT * FROM cypher('my_graph', $$
    MATCH (a:Person)-[:WORKS_AT]->(c:Company)
    RETURN a.name, c.name
$$) AS (person agtype, company agtype);
```

- **建议**：同消息队列 —— 先 Postgres+AGE，只有确实超出能力才上专用图数据库

### 场景 10：中间件 / 微服务替代
- PostgreSQL 可直接把查询结果序列化为 JSON 输出
- 实质上消除了简单 model-fetch-serialize 微服务的需求
- 存在权衡但展示了平台灵活性

### 场景 11：游戏引擎（趣味）
- 有人用 CTE 实现了完整的俄罗斯方块 —— 作者明确说这不是正经建议

## 关键技术对照表

| 技术 | 用途 |
|---|---|
| `tsvector`/`tsquery` | 全文检索原语 |
| `SKIP LOCKED` | 非阻塞队列消费 |
| `UNLOGGED TABLE` | 高速临时存储 |
| GIN Index | JSON / 全文检索高效索引 |
| LTREE | 层次标签树 |
| openCypher | 图查询语言（via AGE）|
| Flatbuffers | 二进制序列化（blob 存储用）|
| TimescaleDB | 时序超表 |
| pgvector | 向量/相似度检索 |

## 推荐延伸阅读

- "SQL is Agile" — Armin Ronacher
- "Postgres for Everything" — Stephan Schmidt (amazingcto.com)
- "What I Wish Someone Told Me About Postgres" — Hazel Bachrach
- CrunchyData：PostgreSQL 消息队列方案
- Lukas Eder：通过 SQL JSON 运算符消除中间件

## Related

- [[entities/postgresql]]
- [[concepts/database-as-platform]]
- [[concepts/postgres-extensions-ecosystem]]
- [[skills/postgres-queue-pattern]]
