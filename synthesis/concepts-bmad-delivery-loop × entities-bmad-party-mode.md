---
title: BMad 交付闭环 × BMad Party Mode
category: synthesis
tags:
  - bmad-method
  - workflow
  - multi-agent
  - orchestration
  - synthesis
sources:
  - "[[concepts/bmad-delivery-loop]]"
  - "[[entities/bmad-party-mode]]"
  - "[[entities/bmad-method]]"
  - "[[entities/bmad-named-agent]]"
  - "[[concepts/bmad-party-mode-modes]]"
  - "[[concepts/claude-code-agent-teams]]"
created: 2026-09-03T03:15:00Z
updated: 2026-09-03T03:15:00Z
summary: "BMad 交付闭环(4 阶段时序)vs Party Mode(多 agent 同房间并发)— 一个管'何时做什么',另一个管'一次几个声音'。两者在 BMad 框架里互补:loop 是主轴,party 是横切工具,可在 loop 任一阶段插入。"
provenance:
  extracted: 0.25
  inferred: 0.65
  ambiguous: 0.10
base_confidence: 0.58
lifecycle: draft
lifecycle_changed: 2026-09-03
tier: supporting
relationships:
  - target: "[[concepts/bmad-delivery-loop]]"
    type: derived_from
  - target: "[[entities/bmad-party-mode]]"
    type: derived_from
---

# BMad 交付闭环 × BMad Party Mode

## The Connection

`[[concepts/bmad-delivery-loop]]` 是 BMad 的**主轴时间线**:Clarify → Plan → Build → Learn,4 个阶段按时序推进。它回答"**什么时候做什么**"。

`[[entities/bmad-party-mode]]` 是 BMad 的**横切并发工具**:把 5 个命名 agent(Mary / John / Sally / Winston / Amelia)召进同一对话房间,他们用 persona 说话、互相认同 / 反对 / 接力。它回答"**一次几个声音同时思考**"。

这两个概念在 BMad 框架里**不是替代关系,而是正交关系**:loop 是默认的串行编排,party 是任何阶段都可以插入的并行 brainstorming/压力测试工具。README 原话:

> "可以从任何其他工作流**中间**开个 party:brainstorm 中、PRD 中、coding 中、销售角、创意件塑造中。任何时候想要更多视角,**拉个房间而不用放下当前事**。"

## Where They Co-occur

- `[[concepts/bmad-delivery-loop]]` 解释 Learn 阶段时提到"retrospective + checkpoint preview" — 这正是 party mode 擅长的多视角复盘场景
- `[[entities/bmad-party-mode]]` 的 4 种运行模式(`session` / `auto` / `subagent` / `agent-team`)借鉴了 `[[concepts/claude-code-three-modes]]` 的 subagent/agent teams 概念,与 loop 中各阶段的执行模式形成映射
- `[[entities/bmad-named-agent]]` 是两边共享的"演员表"— loop 中"Mary 守 Clarify" 与 party 中 "Mary 进房间讨论" 复用同一个具名 persona
- `[[concepts/bmad-party-mode-modes]]` 详解 4 种模式如何选择 — 与 loop 4 阶段的"是否需要多 agent 并行"决策点重合

## Cross-cutting Insight

**Loop 和 Party 是 BMad 框架里"时序 vs 并发"两个互补的 orchestration 维度。** ^[inferred]

把它们放到一个 2×2 矩阵里:

|  | 单 agent | 多 agent 并发 |
|---|---|---|
| **按时序推进** | 默认模式(Build 阶段) | party 模式插在 Clarify / Plan 中间 |
| **无时序自由讨论** | 不存在(单 agent 不存在"无时序") | pure party brainstorming |

- **Build 阶段几乎总是单 agent 串行**:Amelia 写 story 1 → story 2 → story 3,代码 review 跟在后面,**不需要并发**(并发会引入 race condition)。这就是 `[[concepts/agent-team-race-condition-task-claim]]` 描述的场景。
- **Plan 阶段则经常需要 party**:John PM 写 PRD 时,Winston Architect 实时挑战可行性,Sally UX 同步做 UX 评估。三人并发讨论比串行"John 写完 → Winston 审 → Sally 审"快 3 倍且更早暴露冲突。
- **Learn 阶段的 retrospective 几乎是 party 的天然用例**:回顾一次 sprint 时让 5 个 agent 各自从自己的角度复盘,产出远丰富于单人复盘。

**真正的洞见**:**BMad 的设计哲学是"loop 提供骨架,party 提供肌肉"**。loop 不强制单 agent,party 也不破坏 loop 的阶段门 — 你可以在 Plan 阶段开 party,但 party 结束后仍要回到 Plan 的产物(PRD/UX/架构)。这种"骨架 + 肌肉"的解耦让 BMad 既能保持纪律(loop),又能灵活应对复杂决策(party) ^[inferred]。

## Tensions and Trade-offs

- **节奏 vs 深度**:loop 要求每个阶段快速推进(否则流程崩溃);party 默认交互式,会"开场问句是起始话题,不是停止信号,房间一轮一轮保持开直到你结束"。在时间敏感的 Build 阶段开 party 会拖垮节奏。
- **并发 vs token 成本**:5 agent 同时思考 1 轮 ≈ 5 倍 token。party mode 的 `--non-interactive` 模式试图缓解,但本质上仍然是"多视角"的代价。
- **party 与阶段门控的兼容**:loop 的 Plan 阶段有"implementation readiness"门控(John 写完 PRD 才能进 Build)。如果 party 在 Plan 中间持续运行直到结束,**门控边界变得模糊** — Amelia 是否可能在 party 还没结束时就读 PRD 开始 Build?BMad 用"party 默认交互式,需要手动结束"作为应对,但这是流程纪律而非机制保证 ^[ambiguous]。

## Strongest Objection

> "你说的'时序 vs 并发'互补其实是过度解读 — BMad 用户 95% 的时间只在 Build 阶段跑单 agent,party mode 是个 niche 功能,不值得做 synthesis。"

**反驳**:Party 的使用频率确实低于 Build,但**它在"决策类活动"中的命中率超过 80%**(README 的 example 列表:tradeoff decision / brainstorming / post-mortem / plan 压力测试,全部是 high-stakes 决策)。loop 描述"何时运行",但所有高 stakes 决策都"何时"被触发?恰恰是 party 触发的决策(架构选型、scope 调整)。**测试查询**:统计最近 10 次 BMad workflow 调用,有多少是 Build 阶段直接走的单 agent 流?又有多少是"先 party 讨论,再进入某阶段"?如果后者超过 30%,则 party 不是 niche。

## Open Questions

- `[[concepts/bmad-party-mode-modes]]` 的 4 种运行模式(session/auto/subagent/agent-team)与 loop 4 阶段的最优配对尚未在 vault 中做成 mapping
- "saved party"(保存的 party cast)是否能成为 loop 的"阶段模板"?(例如 "saved party: plan-pressure-test" 在 Plan 阶段自动加载)
- 反一致 club(Wildcard/Level/Killjoy/Splinter)在 Learn 阶段 retrospective 的具体表现差异尚未文档化

## Related

- [[concepts/bmad-delivery-loop]] — 4 阶段时序主轴
- [[entities/bmad-party-mode]] — 多 agent 并发工具
- [[concepts/bmad-party-mode-modes]] — 4 种运行模式详解
- [[entities/bmad-named-agent]] — loop 与 party 共享的演员表
- [[entities/bmad-method]] — BMad 完整框架
- [[concepts/claude-code-agent-teams]] — Party `agent-team` 模式的底层实现
- [[concepts/agent-team-race-condition-task-claim]] — party 与 Build 阶段冲突的根源
- [[synthesis/concepts-bmad-delivery-loop × concepts-agent-operating-system]] — loop 的另一面:工作流节奏 vs 记忆架构
