---
title: "Hephaestus Agent"
category: entities
tags:
  - omo
  - agent-orchestration
  - gpt-5.6-sol
  - openai
  - entity
sources:
  - "https://github.com/code-yeongyu/oh-my-openagent"
created: "2026-08-05T07:30:00Z"
updated: "2026-08-05T07:30:00Z"
summary: "omo 自主 deep worker agent：gpt-5.6-sol（OpenAI / GitHub Copilot / Vercel / OpenCode，medium effort）。给目标不给 recipe，自主探索 + 端到端执行。The Legitimate Craftsman。"
provenance:
  extracted: 0.90
  inferred: 0.06
  ambiguous: 0.04
base_confidence: 0.72
lifecycle: draft
lifecycle_changed: "2026-08-05"
tier: supporting
relationships:
  - target: "[[entities/sisyphus-agent]]"
    type: related_to
  - target: "[[entities/oh-my-openagent]]"
    type: related_to
  - target: "[[concepts/omo-agent-category-routing]]"
    type: related_to
---

# Hephaestus Agent

> omo 的**自主 deep worker**——Hephaestus（希腊神话锻造之神），"The Legitimate Craftsman"。**给目标不给 recipe**：自主探索 codebase、研究 patterns、端到端执行。**默认模型**：gpt-5.6-sol（多 provider），medium effort。

## 命名

**Hephaestus**——希腊神话中的锻造之神，为诸神打造武器与装备。

> "**Hephaestus** (`gpt-5.6-sol` through OpenAI, GitHub Copilot, Vercel, or OpenCode at medium effort) is your autonomous deep worker. Give him a goal, not a recipe. He explores the codebase, researches patterns, and executes end-to-end without hand-holding. *The Legitimate Craftsman.*"

> "Anthropic blocked OpenCode because of us. That's why Hephaestus is called 'The Legitimate Craftsman.' The irony is intentional."

## 角色

**autonomous deep worker**——不是需要 hand-holding 的 subagent，是给目标就跑完的 worker：

1. **接收目标**（goal, not recipe）
2. **自主探索** codebase
3. **研究 patterns**
4. **端到端执行**——不间断

## Provider 选项

README 列出 4 个 provider（都跑 gpt-5.6-sol，medium effort）：

- **OpenAI** —— 直接 API
- **GitHub Copilot** —— 通过 Copilot
- **Vercel** —— 通过 Vercel AI Gateway
- **OpenCode** —— medium effort setting

## 与 Sisyphus 的关系

Sisyphus 委派 → Hephaestus 干。详见 [[entities/sisyphus-agent]]。

| | Sisyphus | Hephaestus |
|---|---|---|
| 角色 | Orchestrator | Deep Worker |
| 模型 | Opus 5 / Kimi K3 / GLM 5 | GPT-5.6 Sol（多 provider） |
| 工作 | 规划 + 委派 + 持续推进 | 自主探索 + 端到端执行 |

## 与 vault 已有概念的关系

| vault 已有 | 在 Hephaestus 中的体现 |
|---|---|
| [[entities/openlore]] | "端到端执行"哲学与 OpenLore "确定性 fact layer" 互补 |
| [[concepts/deterministic-agent-memory]] | Hephaestus 的工作记忆需求 |
| [[concepts/ai-tool-specialization]] | Hephaestus 是"深度 worker"专精 |
| [[concepts/agent-team-cost-overhead]] | GPT-5.6 Sol 的成本/性能权衡 |

## Open Questions

- 4 个 provider（OpenAI / Copilot / Vercel / OpenCode）的**性能差异**——README 列出但未给 benchmark
- "medium effort" 在 OpenCode 中的具体定义——是 model config 还是 prompt wrapper？[[ambiguous]]
- Hephaestus 失败时的 fallback 模型链——是否会自动降级到 Sonnet/Haiku？README 未给 [[ambiguous]]

## Related

- [[entities/oh-my-openagent]] — 框架本体
- [[entities/sisyphus-agent]] — Orchestrator
- [[concepts/omo-discipline-agents]] — Hephaestus 是 Sisyphus 协调的 specialists 之一
- [[concepts/omo-agent-category-routing]] — `deep` category 路由到 Hephaestus