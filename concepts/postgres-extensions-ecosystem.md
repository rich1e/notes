---
title: PostgreSQL 扩展生态全景
category: concepts
tags:
  - postgresql
  - extensions
  - database
  - ecosystem
summary: PostgreSQL 核心扩展生态总览：pgvector（向量检索）、pgai（AI 集成）、TimescaleDB（时序）、Apache AGE（图数据库/openCypher）、LTREE（层次树）、pg_search/ParadeDB（全文检索增强）——将 PostgreSQL 从 RDBMS 扩展为多模型数据平台。
sources:
  - "https://www.raphaelbauer.com/posts/postgresql-everything/"
  - "https://github.com/pgvector/pgvector"
  - "https://github.com/timescale/timescaledb"
  - "https://github.com/apache/age"
created: 2026-08-26T00:00:00Z
updated: 2026-08-26T00:00:00Z
tier: reference
lifecycle: verified
lifecycle_changed: "2026-08-28"
base_confidence: 0.82
provenance:
  extracted: 0.88
  inferred: 0.10
  ambiguous: 0.02
relationships:
  - target: "[[entities/postgresql]]"
    type: extends
  - target: "[[concepts/database-as-platform]]"
    type: uses
---

# PostgreSQL 扩展生态全景

> PostgreSQL 的真正护城河不只是核心功能，而是**扩展生态**——通过 `CREATE EXTENSION` 按需加载能力，将一个 RDBMS 变成多模型数据平台。

## 快速对照表

| 扩展 | 场景 | 替代 | 成熟度 |
|---|---|---|---|
| **pgvector** | 向量/相似度检索 | Pinecone/Milvus/Weaviate | 生产就绪（Supabase/Neon 标配）|
| **pgai** | LLM 调用 + AI 工作流 | 独立 AI 中间层 | 较新（Timescale 出品）|
| **TimescaleDB** | 时序数据、分析聚合 | ClickHouse/InfluxDB | 生产就绪，广泛使用 |
| **Apache AGE** | 图数据库/openCypher | Neo4j | Apache 顶级项目，较新 |
| **LTREE** | 层次/树形标签 | 图数据库（树形场景）| 内置扩展，非常稳定 |
| **pg_search** / **ParadeDB** | 增强全文检索（BM25）| Elasticsearch | ParadeDB 较新但增长快 |
| **PostGIS** | 地理空间数据 | 专用 GIS 系统 | 最成熟的 Postgres 扩展之一 |

## 各扩展详解

### pgvector — 向量检索

```sql
-- 安装
CREATE EXTENSION vector;

-- 存储 1536 维向量（OpenAI ada-002）
CREATE TABLE embeddings (
  id BIGSERIAL PRIMARY KEY,
  content TEXT,
  embedding VECTOR(1536)
);

-- 创建 IVFFlat 索引
CREATE INDEX ON embeddings USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- 相似度查询
SELECT content, 1 - (embedding <=> '[0.1, 0.2, ...]'::vector) AS similarity
FROM embeddings
ORDER BY embedding <=> '[0.1, 0.2, ...]'::vector
LIMIT 5;
```

**适用场景**：RAG（检索增强生成）、语义搜索、推荐系统
**不适合**：超大规模（>1亿向量）高并发实时检索场景，此时考虑 Qdrant/Pinecone

### pgai — AI 工作流集成

- Timescale 出品，在 PostgreSQL 内直接调用 LLM API（OpenAI/Cohere 等）
- 可在 SQL 查询中嵌入向量化、文本生成
- 实现 RAG 工作流无需额外中间服务
- **状态**：较新（2024 年发布），生产使用需评估

### TimescaleDB — 时序数据

```sql
-- 将普通表转为超表（按时间自动分区）
SELECT create_hypertable('metrics', 'time');

-- 连续聚合（类似物化视图，实时更新）
CREATE MATERIALIZED VIEW hourly_stats
WITH (timescaledb.continuous) AS
SELECT time_bucket('1 hour', time) AS bucket,
       avg(value) AS avg_val
FROM metrics
GROUP BY bucket;
```

**优势**：查询和写入均针对时序优化；Chunks（分块）自动压缩；连续聚合减少查询开销
**适用**：Web 分析、IoT 指标、监控数据、金融数据

### Apache AGE — 图数据库

```sql
-- 加载扩展
CREATE EXTENSION age;
SET search_path = ag_catalog, "$user", public;

-- 创建图
SELECT create_graph('my_graph');

-- openCypher 查询（与 Neo4j 语法兼容）
SELECT * FROM cypher('my_graph', $$
    CREATE (alice:Person {name: 'Alice'})
    CREATE (bob:Person {name: 'Bob'})
    CREATE (alice)-[:KNOWS]->(bob)
$$) AS (result agtype);

-- 图遍历
SELECT * FROM cypher('my_graph', $$
    MATCH (p:Person)-[:KNOWS*1..3]-(connected)
    WHERE p.name = 'Alice'
    RETURN connected.name
$$) AS (name agtype);
```

**优势**：openCypher 与 Neo4j 语法高度兼容；Apache 顶级项目，持续维护
**当心**：与 Neo4j 相比功能仍有差距；社区规模较小；生产案例少于 pgvector/TimescaleDB

### LTREE — 层次树数据类型

```sql
-- 启用扩展
CREATE EXTENSION ltree;

CREATE TABLE categories (
  id BIGSERIAL PRIMARY KEY,
  path LTREE
);

-- 存储层次路径
INSERT INTO categories VALUES (1, 'Science');
INSERT INTO categories VALUES (2, 'Science.Computer');
INSERT INTO categories VALUES (3, 'Science.Computer.Database');
INSERT INTO categories VALUES (4, 'Science.Computer.Database.SQL');

-- 查询某节点的所有后代
SELECT * FROM categories WHERE path <@ 'Science.Computer';

-- 查询父节点
SELECT * FROM categories WHERE path @> 'Science.Computer.Database.SQL';

-- GiST/GIN 索引加速层次查询
CREATE INDEX ON categories USING gist(path);
```

**优势**：内置扩展（标准 PostgreSQL 自带）；比递归 CTE 更可读且有索引加速
**适用**：标签分类树、组织架构、评论线程、文件系统路径

### pg_search / ParadeDB — 增强全文检索

- ParadeDB 基于 Tantivy（Rust 写的 Lucene 级搜索引擎）
- 支持 BM25 排名（比 PostgreSQL 原生 ts_rank 更接近 Elasticsearch）
- `pg_search` 是其核心扩展

```sql
-- ParadeDB BM25 索引
CREATE INDEX ON documents USING bm25 (content)
WITH (key_field = 'id');

-- BM25 排名检索
SELECT id, paradedb.score(id), content
FROM documents
WHERE content @@@ 'database query optimization'
ORDER BY paradedb.score(id) DESC;
```

**状态**：增长迅速，2024 年获得关注；适合想要比原生 FTS 更强但又不想上 Elasticsearch 的场景

## 扩展选择决策树

```
需要向量检索？
  → pgvector（先用）→ 超百万向量且 QPS 高 → 考虑 Qdrant/Pinecone

需要图数据库？
  → 层次/树形 → LTREE（简单、稳定）
  → 通用图（关系网络） → Apache AGE + openCypher
  → AGE 能力不足 → Neo4j

需要时序数据？
  → TimescaleDB（先用）→ 超大规模 + 极高 QPS → ClickHouse

需要增强全文检索？
  → 先用原生 tsvector → 需要 BM25/Facets → ParadeDB/pg_search
  → 需要完整 ES 功能 → Elasticsearch
```

## 安装模式

大多数扩展通过以下方式安装：
```sql
-- 1. 系统层面安装（需要 apt/brew 安装对应包）
-- 2. 数据库层面启用
CREATE EXTENSION IF NOT EXISTS vector;    -- pgvector
CREATE EXTENSION IF NOT EXISTS timescaledb;  -- TimescaleDB
CREATE EXTENSION IF NOT EXISTS age;       -- Apache AGE
CREATE EXTENSION IF NOT EXISTS ltree;     -- LTREE（通常预装）
```

云托管服务（Supabase/Neon/Timescale Cloud/CrunchyData）通常预装了主要扩展，点击启用即可。

## Related

- [[entities/postgresql]]
- [[concepts/database-as-platform]]
- [[skills/postgres-queue-pattern]]
- [[references/postgresql-for-everything]]
