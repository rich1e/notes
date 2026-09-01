---
title: 确定性 agent 记忆 × OpenLore — 哲学与其参考实现
category: synthesis
tags:
  - ai-agent
  - memory
  - deterministic
  - openlore
  - static-analysis
  - knowledge-graph
  - claude-mem
  - commit-gate
  - no-llm-hot-path
sources:
  - "[[concepts/deterministic-agent-memory]]"
  - "[[entities/openlore]]"
  - "[[concepts/static-analysis-knowledge-graph]]"
  - "[[concepts/no-llm-hot-path]]"
  - "[[concepts/commit-gate-guardrails]]"
  - "[[concepts/claude-mem-memory-architecture]]"
  - "[[entities/claude-mem]]"
  - "[[skills/openlore-cli]]"
  - "[[synthesis/Research: OpenLore]]"
created: 2026-08-31T04:27:59Z
updated: 2026-08-31T04:27:59Z
summary: 确定性 agent 记忆是 vault 的"事实层"哲学(同问同答、显式失败、引用回源码);OpenLore 是它在 2026 年的参考实现——TypeScript + MCP + 静态分析 + hot path 无 LLM。两者的耦合揭示了"哲学 → 实体"对子的成熟路径。
tier: supporting
lifecycle: draft
lifecycle_changed: 2026-08-31
base_confidence: 0.82
provenance:
  extracted: 0.55
  inferred: 0.40
  ambiguous: 0.05
relationships:
  - target: "[[entities/openlore]]"
    type: synthesizes
  - target: "[[concepts/deterministic-agent-memory]]"
    type: synthesizes
  - target: "[[concepts/claude-mem-memory-architecture]]"
    type: related_to
  - target: "[[concepts/commit-gate-guardrails]]"
    type: related_to
  - target: "[[concepts/no-llm-hot-path]]"
    type: related_to
---

# 确定性 agent 记忆 × OpenLore

## The Connection

确定性 agent 记忆是一个 _哲学命题_:agent 的"事实层"应当由确定性算法(图分析 / BM25 / grep / git diff / 签名比对)而不是 embedding 检索来支撑。OpenLore 是这条命题的 _首条可运行实现_——TypeScript 编写的本地优先静态分析记忆层,通过 MCP 暴露 73 个工具、hot path 完全不调用 LLM、输出可做 commit gate。两者不是同一回事:哲学可以脱离实现存在(其他实现可能走不同路径),但 OpenLore 是迄今为止最完整的"原型样本",其工程取舍(_哪些动作被省略、哪些被显式断言失败_)反过来校准了哲学的边界。

## Where They Co-occur

15 个 wiki 页同时引用两者,典型语境:

- **失败分桶哲学**:[[concepts/claude-mem-memory-architecture]] 和 [[concepts/auth-status-semantics]] 都讲"显式失败 vs 假成功",OpenLore 的 RPC drift 错误类型化(`RPCDriftError`)是同一哲学的工程化。
- **静态分析作为基底**:[[concepts/static-analysis-knowledge-graph]] 直接被 OpenLore 实现;OpenLore 通过它产出 call graph / types / tests / decisions / IaC 五类事实,反过来证明"事实层"可以无需 embedding。
- **commit gate 与 hot path**:[[concepts/commit-gate-guardrails]] 和 [[concepts/no-llm-hot-path]] 是 OpenLore 的两条运行约束——commit gate 走校验,hot path 不走 LLM。
- **跨框架的 agent 记忆**:[[entities/claude-mem]] 的 SQLite+Chroma 路径与 OpenLore 的静态分析路径形成"概率 vs 确定性"对照。

## Cross-cutting Insight

哲学 → 实体 的成熟路径有四个可识别阶段,这对在 vault 里出现任何"新哲学"都适用:

1. **概念页抽象**——只讲 _为什么_ 和 _什么时候_ (deterministic-agent-memory)
2. **参考实现页**——一个具体的工具,带 CLI / MCP / 命令清单 (openlore)
3. **使用 skill 页**——把工具塞进 agent 工作流的最小可行步骤 (openlore-cli)
4. **研究综合页**——用一次 wiki-research 把它们与其他对照实体并列 (Research: OpenLore)

跳级会出现"哲学空转"(只有概念没有实现)或"实现孤儿"(只有工具没有哲学定位)。OpenLore 是 vault 里第一个完整走完四阶段的实体,也是后续 `commit-gate-guardrails × ...` 类哲学实体的范本。^[inferred]

## Tensions and Trade-offs

| 维度 | 哲学主张 | OpenLore 实现 | 张力 |
|---|---|---|---|
| 检索确定性 | 同问同答 | 静态图 + BM25 | 实现层允许近似排序(BM25 分数),哲学层要求"完全可重现"——存在落差点 |
| 冷启动 | 不应需要 embedding | TypeScript 编译产物 + git history | 对未构建项目返回空,这是 _正确的失败_ 但 UX 上令人困惑 |
| 漂移感知 | 必须显式标注 stale | 通过 `RPCDriftError` 抛错 | 哲学说"显式",实现层只能做到 _在已知漂移类型上显式_;未知 API 变化还是静默降级 |
| 与概率记忆的关系 | "确定性优于概率" | 未实现 vector store | OpenLore 选择 _不_ 兼容概率路径,意味着用户必须二选一——这是哲学的纯度,也是工具的局限 |

## Strongest Objection

**批评**:确定性 agent 记忆作为哲学是 _稻草人_——它把"概率记忆"塑造成"无脑 embedding 检索"的反派,但生产级 RAG 系统(claude-mem, OpenAI retrieval)早已用 BM25 + rerank + 元数据过滤做出 _类确定性_ 输出。OpenLore 之所以看起来"确定性优于概率",只是因为它的应用场景是 _代码图_ ——天然适合静态分析;换成自然语言场景(用户邮件、客服对话)确定性记忆就退化成精确字符串匹配,反而不如 embedding。

> test: 把 OpenLore 的 BM25 + call graph 模式套到一个 _不含 call graph_ 的语料(比如用户原始聊天记录)。如果事实层的回答准确率从 ~85% 跌到 ~50% 以下,说明"确定性"是 _领域适配_ 的副产品,而非普适哲学。

## Open Questions

- OpenLore 的 73 个 MCP 工具中,有多少比例会被 agent 真正调用?是否是"为了完整性而设计"vs"为了高频场景而优化"?
- 同一哲学下的第二实现会出现吗?比如一个 Go 重写版或 Rust 版,跨语言对比能反推哲学里 _语言相关_ 与 _语言无关_ 的部分。
- `deterministic-agent-memory` 与 [[concepts/agent-operating-system]] 的关系(co=9,顶级未覆盖对):AOS 是"把记忆、tooling、permission、session 都持久化到文件系统"的 _运行时哲学_;确定性记忆是 AOS 在"记忆"子系统上的具体实施吗?
- vault 当前缺少"概率记忆作为 fallback"的页——当确定性路径失败时,合理策略是 _回退到 embedding 还是直接拒绝回答_?

## Related

- [[concepts/deterministic-agent-memory]]
- [[entities/openlore]]
- [[concepts/static-analysis-knowledge-graph]]
- [[concepts/no-llm-hot-path]]
- [[concepts/commit-gate-guardrails]]
- [[concepts/claude-mem-memory-architecture]]
- [[entities/claude-mem]]
- [[skills/openlore-cli]]
- [[synthesis/Research: OpenLore]]
- [[concepts/agent-operating-system]]