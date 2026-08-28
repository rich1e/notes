---
title: SQLite 消息队列模式（BEGIN IMMEDIATE）
category: skills
tags:
  - sqlite
  - queue
  - patterns
  - database
summary: 用 SQLite 的 BEGIN IMMEDIATE 锁 + RETURNING 子句实现单机消息队列，无 broker，无网络跳转，消息永不离开进程，适合中低吞吐量任务队列（通常够用到数千 msg/s）。
sources:
  - "https://joecode.com/2026-08-19-sqlite3/"
created: 2026-08-26T00:00:00Z
updated: 2026-08-26T00:00:00Z
tier: supporting
lifecycle: draft
lifecycle_changed: "2026-08-26"
base_confidence: 0.70
provenance:
  extracted: 0.75
  inferred: 0.22
  ambiguous: 0.03
relationships:
  - target: "[[entities/sqlite]]"
    type: pattern_of
  - target: "[[concepts/database-as-platform]]"
    type: example_of
  - target: "[[skills/postgres-queue-pattern]]"
    type: related_to
---

# SQLite 消息队列模式（BEGIN IMMEDIATE）

> SQLite 没有 `SKIP LOCKED`，但 `BEGIN IMMEDIATE` 提前取写锁 + `RETURNING` 原子交出认领行，同样实现"恰好一个 worker 消费"的互斥。

## 核心机制

### PostgreSQL vs SQLite 队列对比

| 方面 | PostgreSQL | SQLite |
|---|---|---|
| 互斥原语 | `FOR UPDATE SKIP LOCKED` | `BEGIN IMMEDIATE` 写锁 |
| 并发消费者 | 并行，跳过已锁行 | 序列化，等待写锁 |
| 读者影响 | WAL 模式下读不阻塞写 | WAL 模式下读不阻塞写 |
| 消息是否离开机器 | 可能（网络连接到 DB server）| 从不（进程内） |
| 最大吞吐量 | 数万 msg/s | 数千 msg/s（受单写者限制）|

### 为什么 `BEGIN IMMEDIATE` 有效

普通 `BEGIN` 是 deferred（延迟获取锁），可能在第一次写时才获取。  
`BEGIN IMMEDIATE` 立即获取写锁，保证：
1. 事务开始时就独占写入权限
2. 没有其他 writer 能介入选择同一行
3. `RETURNING` 在同一语句内交回已认领的行

## 实现

### 1. 表结构

```sql
CREATE TABLE jobs (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  payload     TEXT    NOT NULL,
  status      TEXT    NOT NULL DEFAULT 'pending',  -- pending / running / done / failed
  worker      TEXT,
  priority    INTEGER NOT NULL DEFAULT 0,
  created_at  TEXT    NOT NULL DEFAULT (datetime('now')),
  updated_at  TEXT    NOT NULL DEFAULT (datetime('now')),
  attempts    INTEGER NOT NULL DEFAULT 0,
  max_attempts INTEGER NOT NULL DEFAULT 3,
  error_msg   TEXT
);

-- 消费者热路径索引
CREATE INDEX idx_jobs_pending
  ON jobs (status, priority DESC, id)
  WHERE status = 'pending';
```

### 2. 消费者（原子认领）

```sql
BEGIN IMMEDIATE;
UPDATE jobs
SET    status  = 'running',
       worker  = ?,
       attempts = attempts + 1,
       updated_at = datetime('now')
WHERE id = (
    SELECT id FROM jobs
    WHERE  status = 'pending'
    ORDER  BY priority DESC, id ASC
    LIMIT  1
)
RETURNING id, payload, attempts;
COMMIT;
```

如果 `RETURNING` 返回空 → 当前无 pending job，等待后重试。

### 3. 完成/失败

```sql
-- 成功
UPDATE jobs SET status = 'done', updated_at = datetime('now') WHERE id = ?;

-- 失败（带退避重试）
UPDATE jobs
SET status     = CASE WHEN attempts < max_attempts THEN 'pending' ELSE 'failed' END,
    error_msg  = ?,
    updated_at = datetime('now')
WHERE id = ?;
```

### 4. 生产者

```sql
INSERT INTO jobs (payload, priority) VALUES (?, ?) RETURNING id;
```

## WAL 模式配置（推荐）

```sql
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;  -- 队列通常不需要 FULL 持久性
```

WAL 模式下：
- 读者从不阻塞写者（监控查询不影响 worker）
- 写者不阻塞读者
- 并发读取性能显著提升

## 超时清理（Heartbeat）

Worker 崩溃不会自动释放 `running` 状态，需要定时清理：

```sql
-- 定时运行（cron）：超时任务重置为 pending
UPDATE jobs
SET status     = 'pending',
    updated_at = datetime('now')
WHERE status   = 'running'
  AND updated_at < datetime('now', '-5 minutes')
  AND attempts < max_attempts;
```

## 性能参考

| 场景 | 吞吐量参考 |
|---|---|
| 单 worker，NVMe | 数百～数千 jobs/s |
| 多 worker（序列化等锁） | 受单写者限制，写并发高时退化 |
| `synchronous = OFF`（可丢失）| 接近内存速度 |
| `:memory:` 数据库 | 极高，纯 CPU 限制 |

## 何时超出 SQLite 队列能力

- 并发写者真实遇到写锁争抢（通常 >数千 msg/s 才触发）
- 需要消费者组 rebalancing（Kafka 分区语义）
- 需要多机消费者（SQLite 单文件，网络共享文件系统性能极差）
- 需要 at-most-once 极高吞吐（无法用简单 BEGIN IMMEDIATE 实现）

此时升级到 [[skills/postgres-queue-pattern]]（PostgreSQL `SKIP LOCKED`）。

## 相关

- [[entities/sqlite]]
- [[skills/postgres-queue-pattern]]
- [[concepts/database-as-platform]]
- [[references/sqlite-for-everything]]
- [[synthesis/skills-postgres-queue-pattern × skills-sqlite-queue-pattern]] — synthesis: 同一队列模式在两种规模下的落地
