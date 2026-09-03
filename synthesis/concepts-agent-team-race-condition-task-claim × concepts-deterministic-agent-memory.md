---
title: Agent Teams 任务竞态保护 × 确定性 agent 记忆 — 静态锁即动态真理
category: synthesis
tags:
  - claude-code
  - agent-teams
  - race-condition
  - file-locking
  - deterministic
  - memory
  - scheduling
  - openlore
sources:
  - "[[concepts/agent-team-race-condition-task-claim]]"
  - "[[concepts/deterministic-agent-memory]]"
  - "[[concepts/agent-team-mailbox-protocol]]"
  - "[[concepts/agent-team-cost-overhead]]"
  - "[[entities/claude-code-agent-teams-feature]]"
  - "[[entities/openlore]]"
created: 2026-08-31T04:27:59Z
updated: 2026-08-31T04:27:59Z
summary: 文件锁作为 task claim 防 race 的机制,是确定性 agent 记忆哲学在 _动态调度_ 子系统上的具体落地——同一哲学既能回答"代码事实可重现"也能回答"任务认领不可冲突"。
tier: supporting
lifecycle: draft
lifecycle_changed: 2026-08-31
base_confidence: 0.80
provenance:
  extracted: 0.70
  inferred: 0.25
  ambiguous: 0.05
relationships:
  - target: "[[concepts/agent-team-race-condition-task-claim]]"
    type: related_to
  - target: "[[concepts/deterministic-agent-memory]]"
    type: related_to
  - target: "[[concepts/agent-team-mailbox-protocol]]"
    type: related_to
  - target: "[[entities/openlore]]"
    type: related_to
---

# Agent Teams 任务竞态保护 × 确定性 agent 记忆

## The Connection

`agent-team-race-condition-task-claim` 源页已经把自身定位为"vault deterministic-agent-memory 哲学的『动态调度』延伸"——但 vault 里 _没有一个页面把这条延伸讲透_。文件锁(file-locking)是确定性记忆的具体形态在 _运行时调度_ 这一新维度上的复用:不靠 Redis、不靠 DB 事务,只靠 POSIX 文件锁 + 文件系统原子 rename,实现"同任务只能被一个 teammate claim"。这是哲学的 _领域迁移_ 案例,也是 vault 里少见的"概念 ↔ 概念"型合成(都是 concepts)——合成价值在于揭示同一抽象如何在不同子系统各取所需。

## Where They Co-occur

6 个 wiki 页同时引用两者,典型语境:

- **共享文件系统作为调度底座**:[[concepts/agent-team-mailbox-protocol]] 的 JSON inbox 文件(`~/.claude/teams/{team-name}/inboxes/{agent-name}.json`)与 task claim 文件在同一目录——共用 OS 文件系统语义作为协调介质
- **静态分析对照**:[[entities/openlore]] 用静态分析产出 _代码事实_,本质上是 _读时确定性_;task claim 用文件锁产出 _调度事实_,本质上是 _写时确定性_——读写两端同一哲学
- **成本与错误恢复**:[[concepts/agent-team-cost-overhead]] 的"3-5 teammates + 5-6 tasks"预算与 race-condition 防护 _相互放大_——teammate 越多,task 越多,race 概率越高,锁机制必要性越强
- **架构完整性**:[[entities/claude-code-agent-teams-feature]] 的 4 组件架构中 mailbox + IPC 都靠文件系统,但只有 task claim 被显式说明为"file-locking"——其他组件是 _隐式_ 借用同一介质

## Cross-cutting Insight

确定性 agent 记忆的 _三段式形态_ 在这个对照里变得清晰:

| 维度 | 静态记忆(OpenLore) | 动态调度(Agent Teams) | 共享要素 |
|---|---|---|---|
| 介质 | git history + 编译产物 | inbox + task 文件 | 文件系统 |
| 一致性保证 | 同问同答(检索确定性) | 单写单读(写时确定性) | POSIX 文件锁 + 原子 rename |
| 失败模式 | 静态分析失败 → 返回空 | lock 竞争失败 → 重试或拒绝 | 显式失败,无静默降级 |
| 漂移检测 | `RPCDriftError` 类型化 | mailbox 损坏条目丢弃 | 显式标注 stale |
| 维护成本 | 静态分析 5 分钟/项目 | 文件锁 < 1ms/claim | _廉价到值得_ |

**核心结论**:确定性哲学不是"非概率检索"这一种形态,而是 _廉价、显式、可在 OS 层落地_ 的协调机制的统称。OpenLore 是 _读时_ 实例,Agent Teams task claim 是 _写时_ 实例——两者共同把"文件系统作为 agent 协调总线"提升为 vault 的一类 _基础设施_。^[inferred]

## Tensions and Trade-offs

- **静态 vs 动态的边界**:OpenLore 可以在 _离线_ 跑完整个分析;task claim 必须 _在线_ 在 teammate 进程间协调。这条边界由"是否需要进程隔离"决定,反过来推论:同一哲学在 _无需进程隔离_ 的子系统上会 _退化_ 为 in-memory 实现(如 in-process Agent Teams)
- **锁的尺度**:POSIX 文件锁在单机文件系统上是免费的,在 NFS/容器共享卷上退化成 _可用性赌博_ ——Agent Teams 没有内置跨机调度能力,因为锁机制 _强依赖_ 本机 fs
- **失败显式性 ↔ UX**:文件锁失败时必须显式重试或拒绝,但 UX 上 _期待_ "Agent Teams 一定能跑"的用户会感到"系统坏了"——这是显式哲学的代价
- **静态分析的静态性**:OpenLore 假设代码 _已编译_,那 git submodule 未初始化、容器内没装工具链时,事实层返回 _空_,而 Agent Teams task claim 不会有 _空_ 这种失败模式

## Strongest Objection

**批评**:把"文件锁"和"静态分析"塞进同一个"确定性哲学"框是 _归纳过度_——它们只是 _恰好_ 都用文件系统 + 都 _恰好_ 强调显式失败,不代表它们 _必然_ 共享底层设计原则。OpenLore 用文件系统是因为 _代码事实_ 本身就是文件系统产物;Agent Teams 用文件系统是因为 _沙箱约束_ (无 Redis、无 DB)。一旦去掉沙箱假设,两者都会迁去更合适的介质——OpenLore 可能用专用 RAG 索引,Agent Teams 可能用 Redis Streams。

> test: 找一个 _非沙箱_ 的生产环境(配齐 Redis + Postgres),对比同一哲学在两介质上的延迟分布。如果文件系统的 p99 延迟 _系统性高于_ Redis 实现 ≥ 30%,说明文件系统是 _约束的产物_ 而非 _哲学的载体_。

## Open Questions

- vault 没有 _跨机 Agent Teams_ 的页——Anthropic 是否计划把文件系统锁换成 etcd/Consul?
- `agent-team-race-condition-task-claim` 提到"lock 失败 → 重试或拒绝",但 _重试策略_ 没有权威描述——指数退避?固定延时?best-effort?值得补一篇 <!-- broken link: no agent-team-claim-retry-strategy page found -->
- `deterministic-agent-memory` 与 `agent-operating-system` 的 co=9 未覆盖对:本合成是"哲学 × 子系统"案例,AOS 是"子系统全集"——本合成页是否应该被并入 AOS 主线?
- 是否有 _第三方工具_(如 [[entities/hephaestus-agent]])实现了 _同一哲学的不同子系统_?对比能反推哲学的边界

## Related

- [[concepts/agent-team-race-condition-task-claim]]
- [[concepts/deterministic-agent-memory]]
- [[concepts/agent-team-mailbox-protocol]]
- [[concepts/agent-team-cost-overhead]]
- [[entities/claude-code-agent-teams-feature]]
- [[entities/openlore]]
- [[synthesis/Research: OpenLore]]
- [[concepts/agent-operating-system]]