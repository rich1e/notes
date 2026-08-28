---
title: SQLite × PostgreSQL — 同一哲学的两个端点
category: synthesis
tags:
  - sqlite
  - postgresql
  - database-as-platform
  - architecture
  - infrastructure
sources:
  - "[[entities/sqlite]]"
  - "[[entities/postgresql]]"
  - "[[concepts/database-as-platform]]"
  - "[[references/sqlite-for-everything]]"
  - "[[references/postgresql-for-everything]]"
  - "[[concepts/sqlite-as-file-format]]"
created: 2026-08-27T08:30:00Z
updated: 2026-08-27T08:30:00Z
summary: "SQLite（进程内，零基础设施）与 PostgreSQL（多用户网络，全功能）不是竞争者——它们是同一「数据库替代专用系统」哲学的两个端点，覆盖从嵌入式单文件到多机网络服务的全部场景。"
provenance:
  extracted: 0.30
  inferred: 0.60
  ambiguous: 0.10
base_confidence: 0.80
lifecycle: draft
lifecycle_changed: "2026-08-27"
relationships:
  - target: "[[entities/sqlite]]"
    type: derived_from
  - target: "[[entities/postgresql]]"
    type: derived_from
---

# SQLite × PostgreSQL — 同一哲学的两个端点

## The Connection

[[entities/sqlite]] 和 [[entities/postgresql]] 常被当作「轻量级 vs. 重量级」的取舍问题处理——但这个框架是误导性的。^[inferred]

更准确的视角是：它们是同一条「数据库即平台」（[[concepts/database-as-platform]]）哲学谱系上的**两个端点**：

- **SQLite**：进程内端（`zero administration`，in-process function call，单文件，Public Domain）
- **PostgreSQL**：网络服务端（多用户，MVCC，扩展生态可替代 11 种专用系统）

两者都致力于用「关系型数据库」取代更专用的系统：SQLite 取代文件系统和嵌入式数据格式，PostgreSQL 取代 Kafka/Redis/Elasticsearch/MongoDB 等网络专用服务。

## Where They Co-occur

- **[[concepts/database-as-platform]]** — 主要来源页，明确把 SQLite 和 PostgreSQL 都列为「用单一数据库替代专用系统」论点的正例，各自覆盖不同的规模区间
- **[[skills/sqlite-queue-pattern]] 和 [[skills/postgres-queue-pattern]]** — 这两个技能页是同一队列模式在两个数据库上的镜像实现（详见 [[synthesis/skills-postgres-queue-pattern × skills-sqlite-queue-pattern]]）
- **[[concepts/sqlite-as-file-format]]** — 引用 PostgreSQL 的「35% faster than filesystem」基准作为对照——实际上该基准的 SQLite 版本先于 PostgreSQL 版本出现，说明两者在不同规模上重复验证了同一设计直觉
- **[[concepts/durable-session-log]]** — 同时在 `relationships` 中引用两者（`related_to`），表明 agent 系统在规模增长时确实需要从 SQLite 迁移到 PostgreSQL

## Cross-cutting Insight

**SQLite 和 PostgreSQL 形成了一条完整的「数据库即平台」升级路径，两者之间的跨越是触发条件明确的工程决策，而非架构重写。**^[inferred]

| 维度 | SQLite | PostgreSQL |
|---|---|---|
| **部署模型** | 进程内函数调用 | 独立网络 daemon |
| **并发模型** | 单写，WAL 多读 | MVCC 多写多读 |
| **基础设施成本** | 零（随 OS 内置）| 需运维（或托管服务）|
| **最大合理规模** | ~1-2 GB 数据，~5K QPS 写 | TB 级数据，数万 QPS |
| **「替代目标」** | 文件系统、嵌入式 kv、配置文件 | Kafka/Redis/ES/Mongo/Neo4j |
| **开发体验** | `:memory:`，无 docker，微秒启动 | docker compose，端口，配置 |

**升级触发器是具体的，不是「感觉数据变大了」**：

```
SQLite → PostgreSQL 的触发条件（任一）：
  - 多进程并发写同一数据库
  - 数据量 > 1-2 GB（磁盘 I/O 开始成为瓶颈）
  - 需要 row-level security 或多用户权限
  - 需要 pg 特有扩展（pgvector, TimescaleDB, SKIP LOCKED 多消费者）
  - 需要 streaming replication 或 standby
```

在这个阈值之前，SQLite 更好（零基础设施、更快测试、更简单 backup）；在阈值之后，PostgreSQL 接管。两者有清晰的交接点，不是模糊的偏好问题。^[inferred]

## Tensions and Trade-offs

- **迁移摩擦的方向性**：从 SQLite 到 PostgreSQL 是单向路径——不是因为 PostgreSQL 更好，而是 PostgreSQL 在 ≤1 GB 场景下引入了真实的运维成本（连接管理、pg_hba.conf、vacuum、备份策略）。选择 SQLite 就是在赌「永远不需要多进程并发写」，这个赌注在单应用场景里通常是合理的，在平台化服务里通常不是。
- **生态宽度不对称**：PostgreSQL 的扩展生态（pgvector/TimescaleDB/Apache AGE）让它在向量、时序、图场景都能「够用」；SQLite 的扩展生态（cr-sqlite/sqlite-vec）在追赶但还未成熟。如果用例在 SQLite 的合理规模内，这个差距不重要；如果正好卡在边界上，可能需要更早迁移。

## Strongest Objection

**"两个数据库在同一篇文章里被提到不代表它们属于同一个概念族——这个 synthesis 只是因为它们都是数据库而强行把它们放在一起，任何两个数据库都可以用这个框架写一个同样空洞的 synthesis 页"。**

> test: 取另外两个数据库（比如 MySQL 和 DuckDB），用这个页面的同样框架——「哲学谱系的两端」、「升级触发器」、「共同替代目标」——写一个 synthesis 页。如果结论和这里的一样 generic，说明这个 synthesis 没有具体的洞见，是结构性模板而非真实知识蒸馏。「SQLite ↔ PostgreSQL」的具体性在于：同一作者 ([Richard Hipp](https://sqlite.org/about.html) 不是，但 [[concepts/database-as-platform]] 的论据把它们明确对照)，且存在一条被 [[concepts/database-as-platform]] 提倡的「先 SQLite 后 PostgreSQL」升级路径。

## Open Questions

- **中间层存在吗？** SQLite（进程内）和 PostgreSQL（独立 daemon）之间，是否有一个「本地 socket 但无网络暴露」的中间方案？（libSQL/Turso 在探索这个方向）
- **同构升级工具**：从 SQLite 升级到 PostgreSQL 时，schema 和数据的迁移工具是否足够成熟？`pgloader` 支持 SQLite 源，但复杂 schema（JSON 列、FTS 表达式）迁移还需手工？
- **边界场景**：当应用「够 SQLite 但团队更熟 PostgreSQL」时，生产率和运维成本哪个占优？这是否在不同团队规模下有不同答案？

## Related

- [[entities/sqlite]] — SQLite 实体详情
- [[entities/postgresql]] — PostgreSQL 实体详情
- [[concepts/database-as-platform]] — 两者共同的哲学来源
- [[concepts/sqlite-as-file-format]] — SQLite 的「文件格式」应用面
- [[references/sqlite-for-everything]] — SQLite 替代论参考
- [[references/postgresql-for-everything]] — PostgreSQL 替代论参考
- [[synthesis/skills-postgres-queue-pattern × skills-sqlite-queue-pattern]] — 同一队列模式在两库上的落地
- [[synthesis/concepts-database-as-platform × concepts-no-llm-hot-path]] — database-as-platform 在 agent 场景的延伸
