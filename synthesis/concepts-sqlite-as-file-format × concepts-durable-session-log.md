---
title: SQLite as File Format × Durable Session Log
category: synthesis
tags:
  - sqlite
  - session-log
  - durability
  - event-sourcing
  - append-only
sources:
  - "[[concepts/sqlite-as-file-format]]"
  - "[[concepts/durable-session-log]]"
  - "[[entities/sqlite]]"
  - "[[entities/deepseek-harness]]"
  - "[[concepts/database-as-platform]]"
created: 2026-08-27T08:30:00Z
updated: 2026-08-27T08:30:00Z
summary: "SQLite 的「更好的 fopen()」哲学与 durable session log 的「model-visible ⟺ logged」invariant 指向同一个设计选择：让持久化对 agent 完全透明、零基础设施、可直接读取。"
provenance:
  extracted: 0.25
  inferred: 0.65
  ambiguous: 0.10
base_confidence: 0.70
lifecycle: draft
lifecycle_changed: "2026-08-27"
relationships:
  - target: "[[concepts/sqlite-as-file-format]]"
    type: derived_from
  - target: "[[concepts/durable-session-log]]"
    type: derived_from
---

# SQLite as File Format × Durable Session Log

## The Connection

[[concepts/sqlite-as-file-format]] 的核心论点是：SQLite 不是数据库服务——它是"更好的 `fopen()`"，一种比原始文件系统更可靠、更快速的**持久化载体**。

[[concepts/durable-session-log]] 的核心 invariant 是：`Model-visible ⟺ logged`——所有模型可见的内容必须能从一个 append-only 的 `SessionEvent` 序列重建。

两者的连接不是偶然的：**durable session log 如果要「更好的 fopen()」，SQLite 就是那个答案**。^[inferred]

- SessionEvent append-only 写入 → SQLite `INSERT` 天然 append-only，行有全局 `rowid` 顺序
- 「从 log 派生一切」→ SQLite 支持任意 SQL 查询，无需单独的派生层或索引服务
- 「单文件备份」→ 一个 `.db` 文件 = 整个会话历史，`cp` 就是完整 backup
- 「零崩溃时部分写」→ SQLite 事务保证，session log 不会因 crash 写入半截 event

## Where They Co-occur

- **[[entities/sqlite]]** — 既是 sqlite-as-file-format 的核心实体，也出现在 durable-session-log 的 `relationships`（`related_to`）里——表明 dsh 作者已经把 SQLite 视为 session log 的自然存储后端
- **[[concepts/deterministic-agent-memory]]** — 同时引用两者：session log 是 facts 序列（确定性）；SQLite 是确定性存储（无随机化读写语义）
- **[[entities/deepseek-harness]]** — durable session log 的来源项目，其 architecture.md 中的存储层与 sqlite-as-file-format 的「配置/状态文件」场景完全重叠

## Cross-cutting Insight

**「可重建性」是两个概念的共同设计目标，SQLite 是实现这个目标最简单的基础设施选择。**^[inferred]

durable session log 要求：给定 log，能完整重建任何时间点的 model history——fork、resume、transcript 都是派生，不是原始数据。

sqlite-as-file-format 提供：给定 `.db` 文件，能用 SQL 重建任何视图——不需要单独的 index 服务、不需要序列化/反序列化层、不需要 migration daemon。

两者组合产生一个「**零基础设施 session memory**」架构：

```
SessionEvent → SQLite INSERT (append-only, transactional)
                ↓
        单一 .db 文件（整个 session 历史）
                ↓
        SQL 查询 → model history / fork / transcript / telemetry
                ↓
        cp / Litestream → 备份/复制（单文件语义）
```

这个架构在 agent 场景下有特殊价值：**agent 可以直接 query 自己的 session log**——用 SQL 分析历史 tool 调用、找重复模式、检测 stuck 状态——这些在 flat file 或消息缓冲里需要额外的解析层。^[inferred]

## Tensions and Trade-offs

- **Write-ahead log vs append-only semantics**：SQLite 的 WAL 模式实际上是「append to WAL, checkpoint to main db」——这与 durable session log 的「append-only，永不修改」有一个细微冲突。SQLite 允许 `DELETE` 和 `UPDATE`，这会破坏 session log 的 immutability invariant。需要应用层约束（只允许 `INSERT`），SQLite 本身不强制这一点。
- **并发读写**：sqlite-as-file-format 在单进程场景表现最好；durable session log 在多 agent 并发写入时会遇到 SQLite 的写锁争用（`BEGIN IMMEDIATE` 序列化写）。高并发多 agent 场景可能需要 PostgreSQL 替代 SQLite——但这正是 [[concepts/database-as-platform]] 的「先用数据库，遇到真实瓶颈再升级」逻辑的体现。

## Strongest Objection

**"这两个概念只是碰巧都用了 SQLite，SQLite 只是实现细节——它们的核心设计模式（file-as-better-fopen vs. event-sourcing invariant）是完全不同的抽象层次，这个 synthesis 是把存储层选型误读为概念关联"。**

> test: 把 durable session log 的存储后端换成 PostgreSQL 或 append-only flat log file（如 `.jsonl`），session log 的「model-visible ⟺ logged」invariant 完全不变；把 sqlite-as-file-format 换成 HDF5 或 Parquet，file-format 的优势论点同样成立。如果两者都可以独立替换底层存储而不影响其核心概念，这个 synthesis 捕获的只是「都适合用 SQLite」而非「两个概念互相依赖」。

## Open Questions

- **Immutability 强制**：SQLite 有没有办法在表级别禁止 `UPDATE`/`DELETE`（触发器？CHECK constraint？）来真正强制 append-only 语义？
- **Event sourcing 工具**：现有 event sourcing 框架（如 Marten、EventStore）是否有 SQLite 后端？还是 session log 场景太专门化，需要自己实现？
- **Log compaction**：durable session log 的「永远 append，永远可重建」在长 session 中会让 `.db` 文件无限增长——SQLite 的 `VACUUM` 操作能否在不破坏 immutability invariant 的情况下压缩日志？

## Related

- [[concepts/sqlite-as-file-format]] — SQLite 作为通用文件格式的论据
- [[concepts/durable-session-log]] — append-only SessionEvent 序列的设计模式
- [[entities/sqlite]] — SQLite 实体
- [[entities/deepseek-harness]] — durable session log 的来源实现
- [[concepts/database-as-platform]] — 两者的哲学上游
- [[concepts/deterministic-agent-memory]] — 确定性存储 + session 重建的交汇点
- [[synthesis/concepts-database-as-platform × concepts-no-llm-hot-path]] — 同哲学族的另一 synthesis
