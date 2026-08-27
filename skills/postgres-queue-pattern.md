---
title: PostgreSQL 消息队列模式（SKIP LOCKED）
category: skills
tags:
  - postgresql
  - queue
  - patterns
  - database
summary: 用 PostgreSQL 的 SKIP LOCKED / FOR UPDATE 实现轻量级消息队列，无需 Kafka/RabbitMQ/SQS，支持持久化、多消费者、至少一次投递语义，适合中低吞吐量任务队列场景。
sources:
  - "https://www.raphaelbauer.com/posts/postgresql-everything/"
  - "https://www.crunchydata.com/blog/message-queuing-using-native-postgresql"
created: 2026-08-26T00:00:00Z
updated: 2026-08-26T00:00:00Z
tier: core
lifecycle: established
lifecycle_changed: "2026-08-26"
base_confidence: 0.85
provenance:
  extracted: 0.80
  inferred: 0.17
  ambiguous: 0.03
relationships:
  - target: "[[entities/postgresql]]"
    type: pattern_of
  - target: "[[concepts/database-as-platform]]"
    type: example_of
---

# PostgreSQL 消息队列模式（SKIP LOCKED）

> PostgreSQL 可以实现生产级消息队列，无需引入 Kafka/RabbitMQ/SQS。核心是两个 SQL 子句：`FOR UPDATE` + `SKIP LOCKED`。

## 核心机制

### 为什么 `SKIP LOCKED` 是关键

普通 `SELECT ... FOR UPDATE` 会**阻塞**其他消费者直到行锁释放。  
`SKIP LOCKED` 告诉 PostgreSQL：**已被锁定的行直接跳过**，不等待。

这实现了"每个 job 只被一个 worker 消费"的互斥，且不产生阻塞等待。

## 完整实现

### 1. 表结构

```sql
CREATE TABLE job_queue (
  id          BIGSERIAL PRIMARY KEY,
  payload     JSONB     NOT NULL,
  status      TEXT      NOT NULL DEFAULT 'pending',  -- pending / processing / done / failed
  priority    INT       NOT NULL DEFAULT 0,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  scheduled_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  attempts    INT       NOT NULL DEFAULT 0,
  max_attempts INT      NOT NULL DEFAULT 3,
  error_msg   TEXT
);

-- 索引：消费者扫描 pending 行的热路径
CREATE INDEX idx_job_queue_consume
  ON job_queue (status, priority DESC, scheduled_at)
  WHERE status = 'pending';
```

### 2. 消费者（原子 pick-and-lock）

```sql
-- 原子性：选取 + 锁定 + 状态更新在一个语句内完成
WITH locked_job AS (
  SELECT id
  FROM job_queue
  WHERE status = 'pending'
    AND scheduled_at <= NOW()
  ORDER BY priority DESC, created_at ASC
  LIMIT 1
  FOR UPDATE SKIP LOCKED   -- 跳过已被其他 worker 锁住的行
)
UPDATE job_queue
SET status = 'processing',
    attempts = attempts + 1,
    updated_at = NOW()
WHERE id = (SELECT id FROM locked_job)
RETURNING id, payload, attempts;
```

如果返回空（无行），说明当前没有可消费的 job，worker 等待后重试。

### 3. 完成 / 失败处理

```sql
-- 成功完成
UPDATE job_queue
SET status = 'done',
    updated_at = NOW()
WHERE id = $1;

-- 失败（未超出重试次数 → 回到 pending；超出 → 标记 failed）
UPDATE job_queue
SET status = CASE
               WHEN attempts < max_attempts THEN 'pending'
               ELSE 'failed'
             END,
    error_msg = $2,
    scheduled_at = CASE
                     WHEN attempts < max_attempts
                     THEN NOW() + (INTERVAL '1 minute' * attempts)  -- 指数退避
                     ELSE scheduled_at
                   END,
    updated_at = NOW()
WHERE id = $1;
```

### 4. 生产者（发布消息）

```sql
INSERT INTO job_queue (payload, priority)
VALUES ($1, $2)
RETURNING id;
```

## 两种消费模式

### 模式 A：一次性消费（Work Queue）
每条消息只被一个 worker 处理一次（上方示例）。适合：任务执行、邮件发送、异步处理。

### 模式 B：扇出（Fan-out / Pub-Sub）
多个订阅者各自维护一个游标，每个都收到同一条消息：

```sql
-- 每个订阅者维护自己的 last_processed_id
CREATE TABLE subscriptions (
  subscriber_id TEXT PRIMARY KEY,
  last_id       BIGINT NOT NULL DEFAULT 0
);

-- 订阅者拉取未读消息
SELECT jq.*
FROM job_queue jq
WHERE jq.id > (SELECT last_id FROM subscriptions WHERE subscriber_id = $1)
ORDER BY jq.id
LIMIT 100
FOR UPDATE SKIP LOCKED;

-- 更新游标
UPDATE subscriptions SET last_id = $last_id WHERE subscriber_id = $1;
```

## 投递语义

| 语义 | 实现 |
|---|---|
| **至少一次（At-least-once）** | 默认行为：worker 崩溃未 ack → 超时后重新 pending |
| **最多一次（At-most-once）** | 不推荐（需要先 delete 再处理） |
| **恰好一次（Exactly-once）** | 需要幂等消费者（在 job 完成前不 commit，失败回滚）|

## 死消息处理（Heartbeat / Visibility Timeout）

Worker 崩溃不会自动释放 `processing` 状态——需要一个清理任务：

```sql
-- 定期运行（cron / pg_cron）：超时的 processing 任务重置回 pending
UPDATE job_queue
SET status = 'pending',
    updated_at = NOW()
WHERE status = 'processing'
  AND updated_at < NOW() - INTERVAL '5 minutes'
  AND attempts < max_attempts;
```

## 性能参考

| 条件 | 吞吐量参考 |
|---|---|
| 单 worker，无索引 | 数百 jobs/s |
| 多 worker + 合适索引 | 数千 jobs/s |
| UNLOGGED 表（可容忍数据丢失）| 接近 Redis 速度 |
| 需要 >1万 jobs/s | 考虑 PGMQ 扩展 或 Kafka |

## 何时超出 PostgreSQL 队列的能力

- 吞吐量持续 >10k 消息/秒
- 需要 Consumer Group Rebalancing（Kafka 的分区语义）
- 需要精确的消息重放（replay by offset）
- 多数据中心复制的队列语义

上述场景下，考虑迁移到 Kafka/RabbitMQ，或使用 **PGMQ**（Tembo 出品的 Postgres 消息队列扩展，比手写 SKIP LOCKED 更完善）。

## 相关工具

- **PGMQ** — Postgres 消息队列扩展，开箱即用，比手写更完整
- **pg_cron** — 在 Postgres 内运行定时任务，配合心跳/清理任务使用
- **CrunchyData 文章** — 详细讲解 PostgreSQL 消息队列的各种模式

## Related

- [[entities/postgresql]]
- [[concepts/database-as-platform]]
- [[concepts/postgres-extensions-ecosystem]]
- [[references/postgresql-for-everything]]
