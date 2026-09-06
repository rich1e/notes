---
title: agent-operating-system × ai-agent-sandbox
category: synthesis
tags:
  - synthesis
  - agent-os
  - ai-agent
  - worktree
  - isolation
sources:
  - "[[concepts/agent-operating-system]]"
  - "[[concepts/ai-agent-sandbox]]"
created: 2026-08-03T13:45:00Z
updated: 2026-08-03T13:45:00Z
summary: AOS 框架的"工作树运行时"层 = ai-agent-sandbox —— sandbox 不是 AOS 五层之一,但实际承担"agent 在哪里写"的物理位置,AOS 必须把它当作隐式第六层来设计。
tier: supporting
lifecycle: reviewed
lifecycle_reason: "auto-promoted by wiki-lint --consolidate: age>30d, confidence>0.78"
lifecycle_changed: 2026-08-03
base_confidence: 0.78
provenance:
  extracted: 0.2
  inferred: 0.7
  ambiguous: 0.1
relationships:
  - target: "[[concepts/agent-operating-system]]"
    type: extends
  - target: "[[concepts/ai-agent-sandbox]]"
    type: extends
---

# agent-operating-system × ai-agent-sandbox

## The Connection

[[concepts/agent-operating-system]] 设计了五层 memory,**没**显式覆盖"agent 在哪里写代码"——KB / ADR / Handoff / Auto Memory / Semantic Memory 都是**文件层**(markdown 在 vault),但**实际工作目录**(worktree / container / VM)不在五层里。

[[concepts/ai-agent-sandbox]] 是"工作树运行时"层:detached HEAD、durable lease、原子 state 自愈、safe-by-default destroy。它是 agent 的**物理隔离与生命周期归属层**。

二者交集的关键命题:**AOS 必须把 sandbox 当作隐式第六层来设计**,否则 compact checkpoint 写完后,agent 的 working tree 状态可能与 memory 不一致。^[inferred]

## Where They Co-occur

- [[concepts/agent-operating-system]] 引用 [[concepts/ai-agent-sandbox]] 的 `extends` 关系:AOS 五层框架的"Handoff (Task Memory)"具体落地 = sandbox 提供的"acquire/use/return"工作树流
- [[entities/treehouse]] 是 sandbox 的具体实现;treehouse 自身是 AOS 的"工具栈关系"中标注的补充层
- [[concepts/claude-mem-memory-architecture]] 用 hook 捕获工具调用,但**不知道**这些工具调用发生在哪个 worktree(haiku 压成 observation 时,worktree path 应作为 observation metadata)

## Cross-cutting Insight

**AOS 的 compact checkpoint 应该包含 sandbox state**,不只 memory state。 ^[inferred]

具体:

```markdown
## Sandbox state at compact
- worktree path: ~/.treehouse/myproject-a1b2c3/3/myproject
- HEAD: a1b2c3d (main @ 2026-08-03)
- lease: { holder: "opencode-runner-01", lease_id: "..." }
- dirty: false (was clean at last refresh)
- pre_destroy hooks: ran cleanly
```

没有这一段,下次 session resume 时,agent 不知道:
1. 哪个 worktree 是它的"家"
2. HEAD 是否 stale(branch 推进了多少)
3. 是否有未 commit 的 dirty 变更需要 return 处理

## Tensions and Trade-offs

| 维度 | AOS 视角 | sandbox 视角 |
|---|---|---|
| 写入位置 | vault markdown 文件 | worktree 内的 .openlore/ + 真实代码 |
| 状态可见性 | 文件易 diff | worktree 状态要扫 git + 进程 + 持久文件 |
| 跨 session 续 | KB / Handoff 文件 | durable lease 在 state file |
| 失败恢复 | corrupt state 全标 leased 等用户 | parse 失败标 leased 等用户 return |

**两层的自愈策略完全一样**:不知道归属时保守标 leased / 标未审,等用户显式确认。这是相同的"uncertainty 哲学"在两层的字面落实。

## Strongest Objection

> **Sandbox state 与 memory state 应该分开管理**,AOS 不应越界。AOS 管认知(semantic / episodic / decision),sandbox 管物理(worktree / container)。混在一起,会让 AOS 文档膨胀。

反驳路径: AOS 已经用 hook lifecycle 把语义事件(如 record_decision)与系统事件(如 commit / file save)统一处理;同一事件链上,sandbox state 与 memory state 是同一事务的两半。**分开管理 = 失去事务性**,会出现"decision 写了但 sandbox state 没存"的撕裂。

**Test**: 在 [[entities/treehouse]] 上做故障注入 —— kill session mid-compact,然后用 `treehouse status` 看是否报告"sandbox state 未刷新,但 memory 已写入"。如果报告撕裂,AOS 设计就有问题。

## Open Questions

- 是否应该有一个 `worktree_md` 文件(类似 .openlore/ 内的 ARCHITECTURE.md)由 AOS 自动维护,把 sandbox state 翻译为人类可读文本?
- 多 sandbox(agent 同时在 5 个 worktree)时,compact checkpoint 如何聚合 5 个 sandbox state?
- AOS 假设单 agent 单 sandbox —— 多 agent 协作(AOS 升级)时如何处理?

## Related

- [[concepts/agent-operating-system]] — 五层 memory 框架
- [[concepts/ai-agent-sandbox]] — 工作树运行时
- [[entities/treehouse]] — sandbox 的具体实现(worktree pool)
- [[concepts/git-worktree-pool-pattern]] — sandbox 核心抽象
- [[concepts/worktree-durable-lease]] — 跨 session 持有的关键机制
- [[concepts/atomic-state-recovery]] — sandbox 与 AOS 共用的自愈策略