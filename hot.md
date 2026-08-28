---
title: Hot Cache
updated: 2026-08-27T08:30:00Z
---

# Hot Cache

*A ~500-word semantic snapshot of recent activity. Updated after every major write operation.*

## Recent Activity

- [2026-08-27 08:30] WIKI_SYNTHESIZE — vault 400+ 页共现扫描，产 **5 个跨域 synthesis 页**，主题全部围绕「数据库即平台 × agent 架构」哲学族。(1) [[synthesis/concepts-database-as-platform × concepts-no-llm-hot-path]] — 「Complexity Budget」原则：database-as-platform 和 no-llm-hot-path 都在回答「我已有的工具够用吗？」，在 agent 场景中两者形成闭环（SQLite 存储 + 确定性热路径）；(2) [[synthesis/concepts-agentic-design × concepts-design-md-shared-memory]] — DESIGN.md 是 agentic design 的「已编译状态」，parallel to deterministic-agent-memory（代码事实住文件，设计决策住 DESIGN.md）；(3) [[synthesis/skills-postgres-queue-pattern × skills-sqlite-queue-pattern]] — 队列选型是「部署规模」函数：SQLite BEGIN IMMEDIATE（<5K msg/s 进程内）→ PostgreSQL SKIP LOCKED（多消费者）→ Kafka，升级触发条件明确；(4) [[synthesis/concepts-sqlite-as-file-format × concepts-durable-session-log]] — SQLite fopen() 零基础设施 + session log 可重建性：append-only INSERT + 单文件 = 零基础设施 session memory；(5) [[synthesis/entities-sqlite × entities-postgresql]] — 同哲学谱系两端，升级触发器具体（多进程并发写/pgvector/复制需求）。**10 源页已添加反向链接**。skipped 10 候选。vault KG net +5 synthesis +10 反向链。QMD skipped(unset)。

- [2026-08-27 08:00] CROSS_LINK — 针对 2026-08-26/27 新建的 PostgreSQL/SQLite/tmux/herdr/opencoworkai 14 页集群，links_added=28（全为 EXTRACTED/INFERRED 级）。snapshot=a75c0b9ea7fe8d8f263b7f5feb358efcfede9d5e。QMD skipped(unset)。

- [2026-08-27 00:00] WIKI_RESEARCH topic="tmux join-pane & swap-pane 用法" rounds=2 sources_fetched=4。**核心发现**：(1) join-pane/move-pane 等价（break-pane 逆操作）；(2) swap-pane 只交换同 window 内位置槽；(3) Marked pane 机制是跨 window 操作关键；(4) Pane ID（%N）终身不变，优于编号；(5) 三层重排：swap/join/break+join。vault KG net +2。QMD skipped(unset)。

## Active Threads

- **Database-as-Platform 哲学族**：5 个 synthesis 页已覆盖核心对照，下一步可考虑 `concepts/commit-gate-guardrails × concepts/no-llm-hot-path` 或 `entities/openlore × entities/claude-mem` 继续深化。
- **open-codesign v0.2.0 跟踪**：Agentic Design 三支柱（workspace/permission/DESIGN.md）已入库，synthesis 已建，后续可关注 v0.3 changelog 变化。
