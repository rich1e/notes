---
title: "omo Agent Category Routing（4 类工作自动选模型）"
category: concepts
tags:
  - omo
  - model-routing
  - multi-model
  - ai-tool-specialization
  - concept
sources:
  - "https://github.com/code-yeongyu/oh-my-openagent"
created: "2026-08-05T07:30:00Z"
updated: "2026-08-05T07:30:00Z"
provenance:
  extracted: 0.88
  inferred: 0.10
  ambiguous: 0.02
base_confidence: 0.68
lifecycle: draft
lifecycle_changed: "2026-08-05"
tier: supporting
relationships:
  - target: "[[concepts/omo-discipline-agents]]"
    type: related_to
  - target: "[[concepts/ai-tool-specialization]]"
    type: related_to
  - target: "[[entities/hephaestus-agent]]"
    type: related_to
summary: "omo 根据工作类型自动选模型的路由机制：visual-engineering / deep / quick / ultrabrain 四 category，避免每次手动指定模型。"
---

# omo Agent Category Routing（4 类工作自动选模型）

> omo 的 4 个工作 category → 模型自动路由。Sisyphus 委派时**不挑模型，挑 category**。harness 按 category 自动选对模型。**用户不动手**。

## 4 个 Category

| Category | 用途 | 当前路由 |
|---|---|---|
| **`visual-engineering`** | 前端 / UI/UX / 设计 | Opus 5 / Kimi K3 / GLM 5.2（视觉强） |
| **`deep`** | 自主研究 + 执行 | **GPT-5.6 Sol xhigh**（via OpenAI / Vercel），fallback GPT-5.6 Sol xhigh |
| **`quick`** | 单文件改动 / typo | Kimi 高速 / Haiku 级 |
| **`ultrabrain`** | 硬逻辑 / 架构决策 | **GPT-5.6 Sol xhigh**（via OpenAI / Vercel），fallback GPT-5.6 Sol xhigh |

> "The agent says what kind of work it needs; the harness picks the right model. ultrabrain now routes to GPT-5.6 Sol xhigh through OpenAI or Vercel when available, then GPT-5.6 Sol xhigh. You touch nothing."

## 设计哲学

**agent 说工作类型 → harness 选模型**——这是 [[concepts/ai-tool-specialization]] 的**自动化版本**：

| 手动版（vault 已有） | 自动版（omo） |
|---|---|
| 用户说"用 Opus 5 做架构" | Sisyphus 说"ultrabrain" → harness 自动选 GPT-5.6 Sol xhigh |
| 用户说"用 Sonnet 写测试" | agent 说"quick" → Kimi 高速 |
| 用户懂模型差异 | **用户不懂也 OK**——harness 知道 |

## 关键设计点

### 1. Agent 不挑模型

> "When Sisyphus delegates to a subagent, it doesn't pick a model. It picks a **category**."

**人类用户**也无需关心模型——只说"做架构" / "改 typo" / "前端" / "深度研究"。

### 2. Harness 自动选

`visual-engineering` → 视觉强模型（Opus 5 / K3）
`deep` → 深度推理模型（GPT-5.6 Sol xhigh）
`quick` → 速度优先
`ultrabrain` → 极限推理（GPT-5.6 Sol xhigh）

### 3. Fallback 链

> "`ultrabrain` now routes to GPT-5.6 Sol xhigh through OpenAI or Vercel when available, then GPT-5.6 Sol xhigh."

**两层 fallback**：
1. OpenAI / Vercel 渠道
2. 直接 GPT-5.6 Sol xhigh

与 vault [[concepts/agent-team-cost-overhead]] 的"lead 给 Opus + 干活给 Sonnet/Haiku"哲学**反转**——omo 默认**全模型都能用**，按 category 而非"贵/便宜"分。

## 与 vault 已有概念的关系

| vault 已有 | 在 Category Routing 中的体现 |
|---|---|
| [[concepts/ai-tool-specialization]] | Category Routing = 自动版"工具栈专业化分工" |
| [[concepts/agent-team-cost-overhead]] | omo 推荐 $49/月 = vault token 优化的实证数据 |
| [[entities/hephaestus-agent]] | `deep` category 路由到 Hephaestus |
| [[entities/sisyphus-agent]] | Sisyphus 委派时挑 category 而非模型 |

## Open Questions

- 4 个 category 的**触发语义** —— 是由 agent 显式说，还是 harness 看任务内容自动判断？README 未详 ambiguous
- category 路由的**性能数据** —— "GPT-5.6 Sol xhigh 比 Opus 5 强 30% 在 `ultrabrain` 上" 这类 benchmark 是否公开？ambiguous

## Related

- [[entities/oh-my-openagent]] — 框架本体
- [[concepts/omo-discipline-agents]] — 5 disciplines 的 category 路由
- [[concepts/omo-ultrawork-mode]] — 触发整个 category 路由链
- [[concepts/ai-tool-specialization]] — 上层抽象