---
title: Database as Platform × No-LLM Hot Path
category: synthesis
tags:
  - database
  - ai-architecture
  - determinism
  - infrastructure-simplification
  - architecture
sources:
  - "[[concepts/database-as-platform]]"
  - "[[concepts/no-llm-hot-path]]"
  - "[[concepts/deterministic-agent-memory]]"
  - "[[entities/sqlite]]"
  - "[[entities/openlore]]"
created: 2026-08-27T08:30:00Z
updated: 2026-08-27T08:30:00Z
summary: "两种「以简驭复」设计原则的同构性：用数据库替代专用系统，用确定性算法替代 LLM——都是把不必要的复杂度推出热路径。"
provenance:
  extracted: 0.15
  inferred: 0.75
  ambiguous: 0.10
base_confidence: 0.72
lifecycle: draft
lifecycle_changed: "2026-08-27"
relationships:
  - target: "[[concepts/database-as-platform]]"
    type: derived_from
  - target: "[[concepts/no-llm-hot-path]]"
    type: derived_from
---

# Database as Platform × No-LLM Hot Path

## The Connection

表面上，"用 SQLite/PostgreSQL 替代 Kafka/Redis/Elasticsearch" 和 "用静态分析图替代 LLM 调用" 是两个不同领域的设计建议——前者关于基础设施选型，后者关于 AI agent 架构。但它们共享同一个底层设计直觉：**当你引入一个专用系统（无论是 Kafka 还是 LLM），你就在为它的运维/不确定性/延迟买单；而这笔账很多时候不值得付**。

两个原则都是在回答同一类问题：

> "我需要一个新组件（专用工具 / AI 调用）来解决这个问题吗？或者，我已有的确定性工具能直接解决？"

^[inferred]

## Where They Co-occur

这两个概念在以下页面中同时出现，指向彼此：

- **[[concepts/deterministic-agent-memory]]** — OpenLore 把「LLM 不上 hot path」推到极限：每次 agent query（orient/search/impact analysis）都是确定性 BM25 + 静态分析图，**存储层就是 JSON 图文件**——这是 database-as-platform 精神在 agent 记忆层的投影（用一个简单的确定性持久层替代嵌入向量+API 依赖）
- **[[concepts/no-llm-hot-path]]** 的实现依赖 **[[entities/sqlite]]** 作为 claude-mem 的存储后端——LLM 被推到 cold path，但 hot path 的数据仍需要持久化，而 SQLite 的进程内特性使得它成为"不需要运维的持久层"
- **[[references/postgresql-for-everything]]** 的核心论点（"用 PostgreSQL 替代 11 种专用系统"）与 no-llm-hot-path 的逻辑结构完全同构：_先评估已有工具能否处理，遇到真实瓶颈才引入专用方案_

## Cross-cutting Insight

两个原则可以合并成一条更基本的设计规则：^[inferred]

> **「Complexity Budget」原则：每引入一个非确定性或专用组件，都要确认"可承受的最小复杂度"是否已被用尽。**

- Database-as-platform 问：**「我的数据库能解决这个问题吗？」**——在引入 Kafka 之前先问 `SKIP LOCKED`
- No-LLM-hot-path 问：**「我的确定性算法能解决这个问题吗？」**——在调用 LLM 之前先问 BM25 + git diff

两者都把"专用高性能组件"视为 **last resort 而非 first choice**，并且都要求在引入之前先证明简单方案已经不够。

这两个原则在同一个系统中相互加强：一个把 LLM 推到 cold path 的 agent（no-llm-hot-path）仍然需要存储 observation / graph——而用 SQLite 或 JSON 文件而非向量数据库服务，完成了从"热路径不引入 LLM"到"热路径不引入任何不必要的外部依赖"的闭环（database-as-platform）。^[inferred]

## Tensions and Trade-offs

两个原则在极端情况下有张力：

- **数据库即平台**的论据是"减少专用系统数量"——但 [[skills/postgres-queue-pattern]] 本身也是一种抽象，当流量超过 10k msg/s 时 PostgreSQL 队列会成为瓶颈，必须引入 Kafka。这个「升级压力」在 no-llm-hot-path 中也存在：静态分析图对于超大 polyglot monorepo 可能缺少语义理解能力，这时 LLM-enhanced 模式（cold path opt-in）才有意义。
- 两者都需要一个「何时升级」的判断机制——database-as-platform 说「遇到真实瓶颈才引入专用工具」，no-llm-hot-path 说「LLM 只在 generate/verify/consolidate 等 cold path opt-in」。判断边界本身就是个设计挑战。

## Strongest Objection

**"这是用相似的词汇包装两件不相关的事"：一个是选基础设施，一个是选算法；把它们放在一起只是文字游戏，实践中没有共同的操作建议。**

> test: 找一个系统，它同时遵循了 database-as-platform（用 PostgreSQL 替代了某专用系统）又遵循了 no-llm-hot-path（热路径零 LLM 调用）——这样的系统是否有独特的设计特征，与只遵循其中一个的系统不同？

如果找不到这样的系统，或者找到了但它的设计特征可以用其他框架解释，这个 synthesis 就是多余的。

## Open Questions

- **哪个维度更难放弃？** 大多数团队在压力下会先引入 LLM（"加个 AI 调用很快"）还是先引入专用数据库（"加个 Redis 很快"）？两个原则的违反模式是否有不同的触发条件？
- **单调性**：随着系统规模增长，「数据库能处理的场景范围」和「确定性算法能处理的场景范围」是否同向收缩，还是各自独立？
- **agent 系统的特殊性**：在 agent 场景下，这两个原则的结合是否产生了超出简单叠加的效果？[[entities/openlore]] + [[entities/claude-mem]] 的组合（静态分析图 + SQLite 记忆层）是否是这个 synthesis 的实证？

## Related

- [[concepts/database-as-platform]] — 基础设施简化哲学
- [[concepts/no-llm-hot-path]] — AI 架构热路径原则
- [[concepts/deterministic-agent-memory]] — 两原则在 agent 记忆层的交汇
- [[entities/sqlite]] — 进程内极简数据库，两原则共同指向的实现
- [[entities/openlore]] — no-llm-hot-path 的参考实现，依赖 SQLite/JSON 持久层
- [[skills/postgres-queue-pattern]] — database-as-platform 的典型落地：消息队列
- [[synthesis/Research: OpenLore]] — OpenLore 研究综合（no-llm-hot-path 来源）
