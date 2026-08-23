---
title: "omo Ultrawork 模式（一词触发全 agent）"
category: concepts
tags:
  - omo
  - keyword
  - ultrawork
  - workflow
  - concept
sources:
  - "https://github.com/code-yeongyu/oh-my-openagent"
created: "2026-08-05T07:30:00Z"
updated: "2026-08-05T07:30:00Z"
provenance:
  extracted: 0.85
  inferred: 0.10
  ambiguous: 0.05
base_confidence: 0.65
lifecycle: draft
lifecycle_changed: "2026-08-05"
tier: supporting
relationships:
  - target: "[[entities/oh-my-openagent]]"
    type: related_to
  - target: "[[entities/sisyphus-agent]]"
    type: related_to
  - target: "[[concepts/omo-discipline-agents]]"
    type: related_to
  - target: "[[concepts/omo-intent-gate]]"
    type: related_to
summary: "omo Ultrawork 模式：输入单词 ultrawork（或 ulw）触发全 agent 流水线，Sisyphus 接管持续推进直到审计确认 done，用户无需了解底层细节。"
---

# omo Ultrawork 模式（一词触发全 agent）

> `ultrawork`（或 `ulw`）是 omo 的**单 keyword 触发器**——装好 omo 后只打这词，Sisyphus 自动规划、委派、并行执行，**不停直到完成审计说 done**。

## 一句话机制

> "Install. Type `ultrawork` (or `ulw`). Done. Everything below, every feature, every optimization: you don't need to know any of it. It just works."

## Light Edition 只识别 `ultrawork`/`ulw`

> "IntentGate ... (Light edition only recognises the `ultrawork`/`ulw` keyword.)"

IntentGate 在 Light Edition 上**降级为关键词识别**——只有 Ultimate 才做完整意图分析。

## 工作流（用户视角）

1. **打开项目**（已装 omo Ultimate）
2. **说 `ultrawork`** + 可选任务描述
3. **Sisyphus 自动**：
   - 探索 codebase
   - 研究 patterns
   - 委派 specialists（Hephaestus / Oracle / Librarian / Explore）
   - 持续推进
4. **直到 Todo Enforcer + Goal Audit 说 done**

## 推荐最低订阅

> "Even with only the following subscriptions, ultrawork works well"

- [ChatGPT Subscription ($20)](https://chatgpt.com/) — Hephaestus（GPT-5.6 Sol）
- [Kimi Code Subscription ($19)](https://www.kimi.com/code) — Sisyphus 默认 / GLM 备援
- [GLM Coding Plan ($10)](https://z.ai/subscribe) — Sisyphus fallback

**$49/月 vs Claude Code $200/月**。

## 5 种 Modes（更细控制）

README 列出的 modes（不只是 `ultrawork`）：

| Mode | 用途 |
|---|---|
| **`ultrawork`** | 默认——所有 agent 全开，不停直到 done |
| **`search`** | 检索模式 |
| **`analyze`** | 分析模式 |
| **`team`** | Team Mode（lead + 8 members） |
| **`hyperplan`** | 5 hostile critics 拆 plan |

按 **Tab** 进入 Prometheus mode（interview-based planning）→ 然后 `/start-work` 全 orchestration。

## 设计哲学

> "You're actually reading this? Wild. Install. Type `ultrawork` (or `ulw`). Done. Everything below, every feature, every optimization: you don't need to know any of it. It just works."

**反 README 文化**——README 自己说"如果你真的读到这里算你牛"。

## 与 vault 已有概念的关系

| vault 已有 | 在 ultrawork 中的体现 |
|---|---|
| [[concepts/agent-team-display-modes]] | Team Mode 用 tmux 可视化 |
| [[concepts/agent-team-cost-overhead]] | $49/月 vs $200/月 = 成本优化的实证 |
| [[entities/claude-code-agent-teams-feature]] | "Team Mode (v4.0)" = Claude Code Agent Teams 的 omo 实现 |
| [[concepts/agent-team-race-condition-task-claim]] | 5+ 并行 specialists 必依赖 task lock |

## 关键风险

| 风险 | 缓解 |
|---|---|
| 用户不知道 agent 在干什么 | tmux 可视化（Ultimate） |
| Token 失控 | Todo Enforcer + Goal Audit |
| 失败无限循环 | Completion audit 强制说 done 才停 |
| 用户指令模糊 | IntentGate（Ultimate） |

## Open Questions

- "ultrawork" 与 slash commands 的优先级——`/ultrawork` 与 `ultrawork` 是否等效？README 未给 ambiguous
- 5 种 modes 的精确触发语法——是否都必须配 Prometheus interview？ambiguous

## Related

- [[entities/oh-my-openagent]] — 框架本体
- [[entities/sisyphus-agent]] — 主 orchestrator
- [[concepts/omo-intent-gate]] — Ultrawork 之前的意图分析
- [[concepts/omo-discipline-agents]] — Ultrawork 激活的所有 specialists
- [[concepts/omo-team-mode]] — Team Mode 是另一种 mode