---
title: AI 工具专业化分工 × BMad 方法论
category: synthesis
tags:
  - ai-coding
  - ai-agents
  - specialization
  - framework
  - synthesis
sources:
  - "[[concepts/ai-tool-specialization]]"
  - "[[entities/bmad-method]]"
  - "[[concepts/bmad-delivery-loop]]"
  - "[[concepts/omo-editions-ultimate-vs-light]]"
  - "[[concepts/bmad-build-workflow]]"
  - "[[concepts/bmad-clarify-analyze-plan]]"
  - "[[concepts/bmad-named-agent-architecture]]"
  - "[[entities/bmad-named-agent]]"
  - "[[entities/oh-my-openagent]]"
created: 2026-09-03T03:00:00Z
updated: 2026-09-03T03:00:00Z
summary: AI 工具专业化(底层范式)与 BMad 方法论(上层包装)在 vault 7 个 BMad 簇页中同时出现 — 它们从两个方向回答"如何让 AI agent 高效协作"这个问题。
provenance:
  extracted: 0.25
  inferred: 0.65
  ambiguous: 0.10
base_confidence: 0.55
lifecycle: draft
lifecycle_changed: 2026-09-03
tier: supporting
---

# AI 工具专业化分工 × BMad 方法论

## The Connection

**AI 工具专业化分工**(concepts/ai-tool-specialization)是底层范式:每个 AI 工具承担自己擅长的窄任务,通过 MCP 协议协作。**BMad 方法论**(entities/bmad-method)是上层产品化包装:Clarify→Plan→Build→Learn 闭环 + 5 个命名 agent + 命名技能。

这两个 concept 在 vault 7 个 BMad 簇页(bmad-delivery-loop / omo-editions-ultimate-vs-light / bmad-build-workflow / bmad-clarify-analyze-plan / bmad-named-agent-architecture / bmad-named-agent / oh-my-openagent)同时出现 — 它们从**协议层** 和**流程层** 两个方向回答同一个问题:"如何让多个 AI agent 在一个项目里高效协作而不混乱"。

## Where They Co-occur

- `[[concepts/bmad-delivery-loop]]` — BMad 的核心 4 阶段,每个阶段由专门的 agent 角色承担(analyzer / pm / architect / dev / qa)
- `[[entities/oh-my-openagent]]` — 把"分工"哲学从 BMad 的 5 agent 扩展到 9+ agent(orchestrator / architect / coder / tester / ...)
- `[[concepts/bmad-named-agent-architecture]]` — 命名 agent 通过结构化 persona 实现"工具专业化"
- `[[concepts/omo-editions-ultimate-vs-light]]` — 把"工具组合"产品化为 SKU
- `[[concepts/bmad-clarify-analyze-plan]]` — 早期 Clarify/Analyze 阶段强制了"分工"纪律
- `[[concepts/bmad-build-workflow]]` — Build 子流程继续维持分工
- `[[entities/bmad-named-agent]]` — BMad 的命名 agent 实现

## Cross-cutting Insight

**"专业化"既是协议范式也是流程纪律**。^[inferred]

- 协议层:MCP 让两个 AI 工具交换结构化消息而不是塞进同一个 prompt
- 流程层:BMad 让一个 agent 只做自己阶段的任务,不让 analyzer 去写代码
- 产品层:omo 把"工具组合"卖成 SKU(light / ultimate)

**真正的高效 AI agent 协作**不是"做最大的那个 agent",而是"用 MCP 做协议级分工 + 用 BMad 做角色级流程 + 用 omo 之类产品把组合打包"。三个层面缺一不可。

## Tensions and Trade-offs

- **专业化 vs 上下文连贯**:每个 agent 只看自己的输入,跨阶段知识丢失 — BMad 通过 doc/artifact(Plan / Story 文件)在 agent 间传递,但增加 token 成本。^[inferred]
- **MCP 标准化 vs 工具专有优化**:协议统一让工具可互换,但某些工具(如 Stitch 的视觉理解)如果不绑死 Claude Code 会失去上下文。^[inferred]
- **产品化 SKU vs 灵活组合**:omo 的 ultimate-vs-light 是 "营销" 简化,真实复杂任务可能需要混合 9+ 不同工具的不同子集。

## Strongest Objection

> "你说的'专业化分工'只是营销话术,真实的 BMad 实现里 analyst agent 仍然在同一个 Claude Code 实例里,本质上还是 mega-agent 内的 prompt 切换,不是真正的协议级分工。"

**反驳**:[[concepts/cordis-plugin-framework]] 的 "everything is a plugin" 架构证明:即使是同一进程,通过 capability-seam / typed events / reversible effects 可以实现"逻辑上的多 agent"(每个 plugin 一个生命周期,dispose 由 framework 保证)。协议级分工不必等于多进程 — service 注册 + event filter 已经是真正的能力分割。**测试查询**: 在 omo Light 中,`/orchestrator` 命令在 claude-code 里的 system prompt 是否真的把"我不能调用 dev 工具"作为硬约束,还是只是软建议?

## Open Questions

- BMad 的"命名 agent" 与 Claude Code Agent Teams 的"teammate" 在 token 隔离 / 文件锁 / 上下文传递上的对比还没在 vault 中做成 synthesis
- "专业化分工" 是否能 scale 到 ≥9 个 agent 仍未知 — 9-agent omo 是当前实证上限

## Related

- [[concepts/ai-tool-specialization]]
- [[entities/bmad-method]]
- [[concepts/cordis-plugin-framework]] — plugin 架构如何实现"协议级分工"
- [[concepts/mcp-server-protocol-quirks]] — 协议层现实
- [[entities/oh-my-openagent]] — 产品化实现