---
title: agent-operating-system × worktree-durable-lease
category: synthesis
tags:
  - synthesis
  - agent-os
  - worktree
  - lease
  - concurrency
sources:
  - "[[concepts/agent-operating-system]]"
  - "[[concepts/worktree-durable-lease]]"
created: 2026-08-03T13:50:00Z
updated: 2026-08-03T13:50:00Z
summary: treehouse 的 durable lease 是 AOS "Handoff (Task Memory)"层的具体运行时实现 —— 128-bit LeaseID + ABA 防护条件 return + 进程无关持久预留,把"agent 持有 worktree"从 subshell 模式推到长期无人值守。
tier: supporting
lifecycle: draft
lifecycle_changed: 2026-08-03
base_confidence: 0.78
provenance:
  extracted: 0.25
  inferred: 0.65
  ambiguous: 0.1
relationships:
  - target: "[[concepts/agent-operating-system]]"
    type: related_to
  - target: "[[concepts/worktree-durable-lease]]"
    type: extends
  - target: "[[concepts/git-worktree-pool-pattern]]"
    type: related_to
---

# agent-operating-system × worktree-durable-lease

## The Connection

[[concepts/agent-operating-system]] 的"Handoff (Task Memory)"层是**任务级持久化**——把任务进展 / 上下文 / 决策交接写到 markdown 文件,供下一 session 续。

[[concepts/worktree-durable-lease]] 是**物理级持久化**——把 worktree 占用与"进程是否还活着"解耦,通过 `Leased` + `LeaseID` + `LeaseHolder` + `LeasedAt` 四元组,让"agent 持有 worktree"可以**没有进程在住**也能持续有效。

二者交集的核心命题:**Handoff 层的"任务"与 lease 的"持有"是同一概念的不同面**——任务级 Handoff 触发时,lease 必须同步;lease 释放时,Handoff 必须收尾。 ^[inferred]

## Where They Co-occur

- [[concepts/git-worktree-pool-pattern]] 通过 `get --lease` 给长期 agent runner 一个持久 worktree,AOS Handoff 写入的文件**就在这个 worktree 的 vault 内**(如果 worktree 是 vault 仓库的 worktree)
- [[concepts/atomic-state-recovery]] 描述的"corrupt state 默认 leased 等用户 return" 与 AOS 的"Handoff 没收尾时显式标记待确认"是同一哲学
- [[entities/treehouse]] 是 lease 的具体实现,[[entities/openlore]] 是 AOS Knowledge Memory 层的实现 —— 两者可同时挂在同一个 long-running agent 上

## Cross-cutting Insight

**Durable lease 让 AOS Handoff 有了"原子承诺"语义**。 ^[inferred]

具体:

```text
session A:
  treehouse get --lease --lease-holder "session-A"  # lease acquired, lease_id = abc
  ... do work ...
  claude-mem captures observations
  /compact writes Handoff.md with next-action
  exit session A

session B (next day, same agent):
  treehouse status --json  # check lease_id = abc still bound
  ... resume work in same worktree
  read Handoff.md from session A
  ... do work ...
  treehouse return --if-lease-id abc  # atomic: lease cleared only if still mine
```

`--if-lease-id` 把"我是上次那个人"的判断写成**状态文件上的原子 CAS**:同一 lease_id 时 return 成功,否则拒绝。这就让 AOS 的"session 续"有强保证——不会出现"我以为是续,但别人的 lease 已经覆盖我的"。

## Tensions and Trade-offs

| 维度 | AOS Handoff 视角 | lease 视角 |
|---|---|---|
| 持久层 | markdown 文件 | state file JSON |
| 谁写 | agent / hook | treehouse CLI |
| 谁读 | 下一 session agent | treehouse CLI(防止并发发同 worktree)|
| 失败恢复 | corrupt Handoff → 重写 | corrupt state → 全标 leased |
| 并发安全 | 文件 lock(若有) | flock + 持锁读 lease 字段 |

**两者的并发模型不同**:AOS 假设单 agent(写入冲突罕见);lease 显式支持多并发(flock + ABA)。

## Strongest Objection

> **lease 是 AOS 不需要的复杂度**。AOS 已经假设"agent 是单人作业",加 lease 等于在 OS 之上再造 OS,增加学习曲线与失败模式。

反驳路径: AOS 的"compact 当同步点"在**多人/多 agent 协作**场景必然撕裂。一个人续写 Handoff 时,另一个人用同一 lease_id return → 谁赢?lease 提供原子 CAS,AOS 单层没有。

**Test**: 在 [concepts/agent-operating-system] 的五层上加"Lease 状态"作为隐式第六层,看 Handoff 写入时是否同时检查"lease 是否被外部篡改"。如果检查,AOS 已经隐式依赖 lease 了 —— 不显式建模是延迟决策。

## Open Questions

- AOS 的 Handoff 文件名应不应该编码 lease_id?(如 `HANDOFF-abc123.md`)?还是用单一 HANDOFF.md + 文件内 metadata?
- 多 agent 并行时,lease 与 Handoff 如何 partition?每个 agent 独立 lease + 独立 Handoff,还是共享 lease + 分片 Handoff?
- Lease 过期(超过 N 天无 return)时,AOS 应主动 archive Handoff 还是强制要求 human review?

## Related

- [[concepts/agent-operating-system]] — 五层 memory 框架
- [[concepts/worktree-durable-lease]] — durable lease 机制
- [[concepts/git-worktree-pool-pattern]] — 池化复用底层
- [[concepts/atomic-state-recovery]] — lease 与 AOS 共用的自愈策略
- [[entities/treehouse]] — lease 实现
- [[concepts/claude-mem-memory-architecture]] — Semantic Memory 层具体实现