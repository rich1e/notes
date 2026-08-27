---
title: PostgreSQL — 开源关系数据库的首选默认项
category: entities
tags:
  - postgresql
  - database
  - infrastructure
summary: PostgreSQL 是业界最稳定、功能最丰富的开源 RDBMS，自 1996 年起发展，凭借扩展生态（pgvector/TimescaleDB/Apache AGE）可替代 Elasticsearch/MongoDB/Kafka/Redis/Neo4j 等专用系统，是现代基础设施的首选默认数据库。
sources:
  - "https://www.raphaelbauer.com/posts/postgresql-everything/"
  - "https://www.postgresql.org/"
created: 2026-08-26T00:00:00Z
updated: 2026-08-26T00:00:00Z
tier: core
lifecycle: established
lifecycle_changed: "2026-08-26"
base_confidence: 0.90
provenance:
  extracted: 0.85
  inferred: 0.12
  ambiguous: 0.03
relationships:
  - target: "[[concepts/database-as-platform]]"
    type: exemplifies
  - target: "[[concepts/postgres-extensions-ecosystem]]"
    type: has_component
  - target: "[[skills/postgres-queue-pattern]]"
    type: enables
---

# PostgreSQL — 开源关系数据库的首选默认项

> **"遇到任何数据存储需求，先问：PostgreSQL 能解决吗？"** — 这条经验法则背后是 30 年社区打磨的稳定性和不断扩展的生态能力。

## 核心特性

| 维度 | 内容 |
|---|---|
| 诞生年份 | **1996**（前身 POSTGRES 1986 年由 UC Berkeley 开始）|
| 开源协议 | PostgreSQL License（类 BSD，极宽松）|
| 最新稳定版 | PostgreSQL 17（截至 2026）|
| 安装方式 | apt/brew/PostgresApp/Docker/云托管（RDS/CloudSQL/Timescale）|

## 原生能力

### 结构化数据（SQL 核心）
- ACID 事务、多版本并发控制（MVCC）
- 复杂查询：窗口函数、CTE、递归查询
- 分区表、并行查询

### 半结构化 / 文档存储
- `jsonb` 类型 — 二进制 JSON，支持 GIN 索引查询
- `hstore` — 键值对存储
- 数组类型、范围类型

### 全文检索
- `tsvector` / `tsquery` — 内置全文检索原语
- GIN / GiST 索引加速
- 多语言词典支持（中文需额外配置）

### 时序 / 分析
- 窗口函数 + 分区表可处理中等时序数据
- **TimescaleDB** 扩展：超表（hypertable）、连续聚合、数据分片

### 地理空间
- **PostGIS** 扩展：空间数据类型、地理计算（PostgreSQL 最知名扩展之一）

## 扩展生态（关键）

见 [[concepts/postgres-extensions-ecosystem]] — pgvector（向量）、Apache AGE（图）、LTREE（树）、pgai（AI 集成）等共同构成"数据库即平台"能力。

## 高级功能

### SKIP LOCKED（消息队列基础）
```sql
SELECT id, payload FROM jobs
WHERE status = 'pending'
ORDER BY created_at
LIMIT 1
FOR UPDATE SKIP LOCKED;
```
无需 Kafka/RabbitMQ 的轻量队列消费模式，详见 [[skills/postgres-queue-pattern]]。

### UNLOGGED 表（高速缓存）
```sql
CREATE UNLOGGED TABLE session_cache (
  key TEXT PRIMARY KEY,
  value JSONB,
  expires_at TIMESTAMPTZ
);
```
绕过 WAL 日志，写入速度接近 Redis。崩溃后数据截断，适合临时/缓存数据。

### LTREE（层次数据）
```sql
-- 存储：'Science.Computer.Database.SQL'
-- 查询所有子节点：
SELECT * FROM topics WHERE path <@ 'Science.Computer';
```

## 部署选项

| 类型 | 方案 |
|---|---|
| 本地开发 | Homebrew / PostgresApp / `docker compose` |
| CI 测试 | Testcontainers（与生产一致的真实 DB）|
| 自托管 | Debian/Ubuntu `apt install postgresql` |
| 托管云 | AWS RDS、GCP Cloud SQL、Azure DB for PostgreSQL、Supabase、Neon、CrunchyData |

## 典型迁移案例（来源：Raphael Bauer 文章）

| 公司 | 从 | 迁到 Postgres 功能 |
|---|---|---|
| Contentful | Elasticsearch | `tsvector` 全文检索 |
| Instacart | 独立搜索系统 | Postgres 全文检索 |
| The Guardian | MongoDB | `jsonb` 文档存储 |

## 选择 PostgreSQL 的决策框架

```
新需求 → 能用 Postgres 原生解决? → 是 → 用原生
              ↓ 否/不够
        有对应扩展（pgvector/AGE/LTREE…）? → 是 → 用扩展
              ↓ 否/性能确实到瓶颈
        再考虑专用系统（Kafka/Neo4j/ES…）
```

**关键**：先用 → 遇到真实瓶颈 → 再迁。不要"预防性"叠加工具栈。

## Related

- [[concepts/database-as-platform]]
- [[concepts/postgres-extensions-ecosystem]]
- [[skills/postgres-queue-pattern]]
- [[references/postgresql-for-everything]]
