---
title: "omo Discipline Agents（Sisyphus 协调 specialists）"
category: concepts
tags:
  - omo
  - agent-orchestration
  - parallel
  - concept
sources:
  - "https://github.com/code-yeongyu/oh-my-openagent"
created: "2026-08-05T07:30:00Z"
updated: "2026-08-05T07:30:00Z"
provenance:
  extracted: 0.88
  inferred: 0.08
  ambiguous: 0.04
base_confidence: 0.70
lifecycle: draft
lifecycle_changed: "2026-08-05"
tier: supporting
relationships:
  - target: "[[entities/sisyphus-agent]]"
    type: related_to
  - target: "[[entities/hephaestus-agent]]"
    type: related_to
  - target: "[[entities/oh-my-openagent]]"
    type: related_to
---

# omo Discipline Agents（Sisyphus 协调 specialists）

> omo "Discipline Agents" = Sisyphus 协调 4 个 specialists（Hephaestus / Oracle / Librarian / Explore）+ Prometheus planner。**完整 AI dev team 并行**。

## 5 个 Disciplines

| Agent | 模型 | 角色 |
|---|---|---|
| **Sisyphus** | claude-opus-5 / kimi-k3 / glm-5 | **Orchestrator** —— 规划、委派、并行、持续推进 |
| **Hephaestus** | gpt-5.6-sol（多 provider, medium effort）| **Autonomous Deep Worker** —— 给目标，端到端执行 |
| **Prometheus** | claude-fable-5 / kimi-k3 | **Strategic Planner** —— interview mode，问问题、识别 scope、写详细 plan |
| **Oracle** | （README 未列具体模型）^[ambiguous] | 推测：架构 / 决策顾问 |
| **Librarian** | （README 未列具体模型）^[ambiguous] | 推测：知识库 / 文档检索 |
| **Explore** | （README 未列具体模型）^[ambiguous] | 推测：codebase 探索 / 类似 Claude Code 的 Explore subagent |

> Oracle / Librarian / Explore 的**精确角色 + 模型**在 README 未详述——仅 highlights 表列出名字。[[ambiguous]]

## 工作流（Sisyphus 视角）

```
User: ultrawork + (optional task)
   ↓
Sisyphus (Opus 5): 理解任务
   ↓
Prometheus (Fable 5 / K3): 战略规划（可选）
   ↓
Sisyphus: 拆任务，parallel spawn
   ├── Hephaestus (GPT-5.6 Sol): deep execution
   ├── Oracle: 架构决策（运行中）
   ├── Librarian: 文档检索
   └── Explore: codebase 扫描
   ↓
Sisyphus: 收集结果 + 持续推进
   ↓
Todo Enforcer + Goal Audit: done?
```

## "Aggressive Parallel Execution"

> "He plans, delegates to specialists, and drives tasks to completion with **aggressive parallel execution**."

与 [[concepts/agent-team-mailbox-protocol]] 的 mailbox IPC 直接对应——5+ specialists 同时跑时**不能两 agent 改同一文件**。

## 模型选择哲学

> "Every agent is tuned to its model's specific strengths. No manual model juggling."

| Agent | 选它的理由 |
|---|---|
| Sisyphus (Opus 5) | 强规划 + 综合能力 |
| Sisyphus (Kimi K3) | 性价比 + 中文场景 |
| Hephaestus (GPT-5.6 Sol) | 强深度推理 + 端到端执行 |
| Prometheus (Fable 5) | 长上下文 + interview 模式 |
| Prometheus (Kimi K3) | 备援 |

## "Discipline" 这个词

"Discipline agent" 强调**纪律性**——不会"中途放弃"。与 Sisyphus 的"推石上山"寓意呼应：

> "He does not stop halfway."

## 与 vault 已有概念的关系

| vault 已有 | 在 Discipline Agents 中的体现 |
|---|---|
| [[entities/bmad-named-agent]] | "named agent" 哲学在 omo 的 5 discipline 上落地 |
| [[entities/claude-code-agent-teams-feature]] | Sisyphus 协调 5 specialists = Claude Code Team lead |
| [[concepts/agent-team-cost-overhead]] | 5+ specialists = linear token scaling |
| [[concepts/ai-tool-specialization]] | 每个 agent tuned to its model's strengths = 工具专业化 |
| [[concepts/claude-code-three-modes]] | Sisyphus orchestrator = Default 模式；specialists = Agent Teams 子集 |
| [[concepts/claude-code-token-optimization]] | Skill-Embedded MCPs 让 specialists 不重复加载 MCP context |

## Related

- [[entities/oh-my-openagent]] — 框架本体
- [[entities/sisyphus-agent]] — 主 orchestrator
- [[entities/hephaestus-agent]] — Deep Worker
- [[concepts/omo-ultrawork-mode]] — 触发机制
- [[concepts/omo-team-mode]] — Team Mode 是 5 disciplines 的并行升级版
- [[synthesis/concepts-bmad-named-agent-architecture × concepts-omo-discipline-agents]] — synthesis：BMad persona 三腿凳 vs omo 5 专家分工的设计哲学对比