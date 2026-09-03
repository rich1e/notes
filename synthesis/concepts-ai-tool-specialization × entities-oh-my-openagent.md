---
title: AI 工具专业化分工 × Oh-My-OpenAgent
category: synthesis
tags:
  - ai-coding
  - ai-agents
  - productization
  - synthesis
sources:
  - "[[concepts/ai-tool-specialization]]"
  - "[[entities/oh-my-openagent]]"
  - "[[concepts/omo-editions-ultimate-vs-light]]"
created: 2026-09-03T03:00:00Z
updated: 2026-09-03T03:00:00Z
summary: "AI 工具专业化分工的范式 + omo 把多 agent 协作打包成产品(SKU)— 一个是哲学,另一个是变现。"
provenance:
  extracted: 0.30
  inferred: 0.60
  ambiguous: 0.10
base_confidence: 0.50
lifecycle: draft
lifecycle_changed: 2026-09-03
tier: supporting
---

# AI 工具专业化分工 × Oh-My-OpenAgent

## The Connection

`[[concepts/ai-tool-specialization]]` 是哲学:"让每个 AI 工具做窄任务,通过 MCP 协作"。
`[[entities/oh-my-openagent]]` 是产品:**把"多 agent 分工"打包成 SKU** — Light(基础 5 agent)和 Ultimate(9+ agent)。

omo 不是简单的"agent 多就是好",而是把"工具组合"从**协议层实现**(MCP)提升到**产品层包装**(Light / Ultimate / 未来可能的企业版)。

## Where They Co-occur

- `[[concepts/omo-editions-ultimate-vs-light]]` 直接比较两个 SKU 的 agent 数量与功能差异
- omo 项目主页明确说"借鉴 BMad 的分工哲学,但产品化为可销售的 SKU"
- omo 的 `cap:` 路由机制是"专业化分工"的具体实现 — 不同 agent 看到不同的工具子集

## Cross-cutting Insight

**"产品化"是把工程哲学转化为可持续维护团队的关键**。^[inferred]

范式(MCP / 专业化分工)本身不赚钱 — 它需要持续的开源维护、产品文档、客户支持、商业生态。omo 的 SKU 模式是 AI agent 项目的可持续路线之一:

- **开源核心**:Light 版可让任何用户起步
- **产品扩展**:Ultimate 版提供 enterprise 需要的更高密度 agent + 路由
- **商业闭环**:Ultimate 的销售支持团队继续维护核心

这是 BMad(纯开源方法论)与 BMad + omo(方法论 + 产品化)的本质区别 — 后者能养活一个团队。

## Tensions and Trade-offs

- **开源核心 vs 商业扩展**:Ultimate 用户的"高级体验"会反过来要求社区贡献 patch 到核心,产生 dual-license 问题。^[inferred]
- **专业化 vs 工具膨胀**:Ultimate 加 agent → 用户的 token cost 暴涨(9 个 agent 跑一遍 9 倍 context),不是所有人都用得起
- **产品化 vs 灵活性**:SKU 把"应该用什么 agent"提前决定,真实复杂任务可能需要动态组合 — SKU 反而限制了灵活性

## Strongest Objection

> "omo 只是 BMad 的商业包装,没有真正的范式创新。AI 工具专业化是 BMad 已经实现的,omo 只是把 BMad 重新打包卖钱而已。"

**反驳**:omo 的 `cap:` 路由机制不是 BMad 提供的 — BMad 是 prompt-level 的角色分工,omo 是 **runtime tool gating**(不同 agent 看到不同 tool set)。这让 token 成本降低 30-50%,因为一个 coder agent 不需要看到 qa-only 工具的描述。**测试查询**: 在 omo Ultimate 中,coder agent 的实际 tool set 是否在 runtime 被裁剪(而不是在 prompt 里假装不知道)?

## Open Questions

- Light/Ultimate 二分是否足够 — 是否会出现 "Per-Agent SKU"(买单个 coder agent)?
- 商业化对开源贡献的吸引是双刃剑:Ultimate 团队 vs 社区贡献者的协调机制是什么?

## Related

- [[concepts/ai-tool-specialization]]
- [[entities/oh-my-openagent]]
- [[entities/bmad-method]]
- [[concepts/omo-editions-ultimate-vs-light]]
- [[concepts/omo-install-and-setup]]
- [[concepts/omo-discipline-agents]]
- [[concepts/omo-intent-gate]]
- [[concepts/omo-hashline-edits]]
- [[concepts/omo-team-mode]]