---
title: "Sisyphus Agent"
category: entities
tags:
  - omo
  - agent-orchestration
  - opus-5
  - kimi-k3
  - glm-5
  - entity
sources:
  - "https://github.com/code-yeongyu/oh-my-openagent"
created: "2026-08-05T07:30:00Z"
updated: "2026-08-05T07:30:00Z"
summary: "omo 主 orchestrator agent：claude-opus-5 / kimi-k3 / glm-5 任选驱动。规划、委派 specialists、激进并行执行、不中途停止。Opus 5 + Kimi K3 推荐默认。"
provenance:
  extracted: 0.90
  inferred: 0.06
  ambiguous: 0.04
base_confidence: 0.72
lifecycle: draft
lifecycle_changed: "2026-08-05"
tier: supporting
relationships:
  - target: "[[entities/oh-my-openagent]]"
    type: related_to
  - target: "[[entities/hephaestus-agent]]"
    type: related_to
  - target: "[[concepts/omo-discipline-agents]]"
    type: related_to
---

# Sisyphus Agent

> omo 的**主 orchestrator agent**——Sisyphus 推石上山，"doesn't stop halfway"。规划、委派 specialists、激进并行执行直到任务完成。**推荐默认模型**：claude-opus-5 / kimi-k3 / glm-5 任选。

## 命名

**Sisyphus 推石上山**——希腊神话中永远推石上山的国王。比喻：任务永远不半途停下。

> "Sisyphus (`claude-opus-5` / **`kimi-k3`** / **`glm-5`** ) is your main orchestrator. He plans, delegates to specialists, and drives tasks to completion with aggressive parallel execution. He does not stop halfway. Claude Opus 5 and Kimi K3 are the recommended defaults."

## 角色

**主协调者**——不是 worker，是 leader：

1. **理解任务** —— 用户说 `ultrawork` 或具体目标
2. **拆任务 + 委派** —— 调 Hephaestus / Oracle / Librarian / Explore
3. **并行执行** —— 5+ specialists 同时跑
4. **持续推进** —— 不停直到审计说 done

## 与 Hephaestus 的关系

| 角色 | Sisyphus | Hephaestus |
|---|---|---|
| 身份 | Orchestrator / Lead | Autonomous Deep Worker |
| 模型 | Opus 5 / Kimi K3 / GLM 5 | GPT-5.6 Sol（多 provider） |
| 工作模式 | 调度 + 规划 | 自主探索 + 端到端执行 |
| 触发 | 用户说 ultrawork | Sisyphus 委派 |
| 关键行为 | "drives tasks to completion" | "explores codebase, researches patterns, executes end-to-end" |

详见 [[entities/hephaestus-agent]]。

## 推石哲学与 vault 概念

> "Anthropic blocked OpenCode because of us. That's why Hephaestus is called 'The Legitimate Craftsman.' The irony is intentional."

omo 维护者把"被 Anthropic 屏蔽"变成品牌——Sisyphus / Hephaestus 都被希腊神话包装。

## 推荐订阅成本

Sisyphus 默认跑 Opus 5 是贵的。**官方推荐**：

- ChatGPT Subscription ($20)
- Kimi Code Subscription ($19)
- GLM Coding Plan ($10)

判断：$49/月 vs Claude Code $200/月 → vault [[concepts/agent-team-cost-overhead]] 的实战示例。

## 与 vault 已有概念的关系

| vault 已有 | 在 Sisyphus 中的体现 |
|---|---|
| [[entities/bmad-named-agent]] | Sisyphus = BMad "named agent" 哲学的 om o 实现（persona + customizable model） |
| [[entities/claude-code-agent-teams-feature]] | Sisyphus 的协调 = Claude Code Team lead |
| [[concepts/agent-team-cost-overhead]] | "Opus 5 vs Kimi K3 + GPT-5.6 Sol" 是成本对比的实战数据 |
| [[concepts/ai-tool-specialization]] | Sisyphus 知道每个 specialist 擅长什么，按需委派 |

## Open Questions

- "Hephaestus + Prometheus + Sisyphus 三角关系"的精确工作流——README 给出名字但未给完整 task flow [[ambiguous]]
- Sisyphus 是否会自动**切换模型**（如 token 用完时降级到 Kimi）——README 暗示但未明说 [[ambiguous]]

## Related

- [[entities/oh-my-openagent]] — 框架本体
- [[entities/hephaestus-agent]] — 自主 deep worker
- [[concepts/omo-discipline-agents]] — Sisyphus 协调 4 个 specialists
- [[concepts/omo-agent-category-routing]] — 4 category → model 自动选择