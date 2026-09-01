---

title: "Agent Team 的 Token 成本权衡"
category: concepts
tags:
  - claude-code
  - ai-agents
  - cost
  - token-optimization
  - concept
summary: "Claude Code Agent Teams token cost 随 teammate 数线性扩展（每个 teammate 独立 context window）；官方推荐 3-5 teammates + 5-6 tasks per teammate；与 subagent 的 summarized-back 模型对比。"
sources:
  - "https://docs.claude.com/en/docs/claude-code/agent-teams"
created: "2026-08-05T04:30:00Z"
updated: 2026-08-23T09:05:00Z
provenance:
  extracted: 0.92
  inferred: 0.06
  ambiguous: 0.02
base_confidence: 0.82
lifecycle: draft
lifecycle_changed: "2026-08-05"
tier: supporting

---
# Agent Team 的 Token 成本权衡

> Agent Teams 的 token 成本**随 teammate 数线性增长**——每个 teammate 独立 context window。这是与 subagent 模式的**根本性成本差异**，也是 vault token 优化知识簇的新维度。

## 官方核心论断

> "Agent teams use significantly more tokens than a single session. Each teammate has its own context window, and token usage scales with the number of active teammates."

> "For research, review, and new feature work, the extra tokens are usually worthwhile. For routine tasks, a single session is more cost-effective."

> "Token costs scale linearly: each teammate has its own context window and consumes tokens independently."

## 三模式 token 模型对比

| 模式 | Token 模型 | 适用 |
|---|---|---|
| **单 session** | 1x 你的 context | 日常任务 |
| **Subagents** | 主 + 子 agents 各自 context，但子结果**summarized back** | 独立子任务 |
| **Agent Teams** | N teammates × **各自独立** context | 复杂任务 |

**核心差异**:
- Subagents 的子 agent **压缩汇报**——主 context 只增加 1 条总结
- Agent Teams 的 teammates **不向 lead 汇报中间过程**——他们自己有自己的 context 自己花

## 官方推荐规模

### 团队大小

| 数量 | 推荐 |
|---|---|
| **3-5 teammates** | **多数工作流最佳** |
| 6+ | 协调成本上升，需明确任务边界 |
| 15+ | **不建议**（协调爆炸） |

### 任务粒度

> "Start with 3-5 teammates for most workflows. This balances parallel work with manageable coordination."

> "Having 5-6 tasks per teammate keeps everyone productive without excessive context switching."

> "If you have 15 independent tasks, 3 teammates is a good starting point."

## 何时不该用 agent teams

官方明确**反例**：

> "For sequential tasks, same-file edits, or work with many dependencies, a single session or subagents are more effective."

| 任务特征 | 推荐 |
|---|---|
| 串行 | 单 session |
| 多人改同文件 | 单 session / subagent |
| 依赖密集 | 单 session |
| 独立多角度并行 | **Agent Teams** |
| 独立模块并行开发 | **Agent Teams** |
| 对抗式 debug | **Agent Teams** |

## 模型选择的 token 影响

按 anthropic-claude-code-agent-teams-docs，teammates 默认**不**继承 lead 的 `/model` 选择：

- **Default teammate model** in `/config` — 改默认 teammate 模型
- **`Default (leader's model)`** — 让 teammate 跟 lead
- spawn 时显式指定：`Use Sonnet for each teammate`

**实战建议**（综合官方 + vault 知识）：
- **Lead 给 Opus** — 做正确 plan + 拆任务 + 写 prompt
- **简单干活 agent 给 Sonnet/Haiku** — 任务清单清楚后不需要顶级模型
- **可混合** — 关键 backend agent 用 Sonnet，QA agent 用 Haiku 即够

**Opus 4.6 价格**（Round 2 验证）: $5/M input, $25/M output（anthropic-claude-code-agent-teams-docs 上下文推断）。这与 [[misc/web-youtube-com-watch-v-cskoa-ccmq0w]] 提到的 "$10/$37.5" 1M context premium 价不同——后者可能指 1M context premium tier。

## Token 监控

### 单 session 层

`/cost` 或 `/usage` 看主 lead session 的账单。

### dashboard 限制（重要）

YouTube 教程 [[misc/web-youtube-com-watch-v-cskoa-ccmq0w]] 提到 "$1.15 / 4 分钟 / 5 agent" 但 dashboard 只显示约 5 分钟——**可能是 dashboard 只算主 lead 时长**，不计所有 teammate。官方未明确说但**确认 token 是线性扩展**，所以**真实账单应远高于 dashboard 显示**。

> **结论**：以 Anthropic Console 账单为准，dashboard 时长是误导信号。

## 与 vault token 优化知识簇的关系

| 概念 | 在 agent teams 的角色 |
|---|---|
| [[skills/claude-code-token-optimization]] | 提示缓存 + context 管理 → 也适用于 teammates |
| [[concepts/ai-tool-specialization]] | 按模型分级调度 = "Lead Opus + 干活 Sonnet" |
| [[concepts/deterministic-agent-memory]] | race lock 防 token 双扣 |
| **本概念页** | linear scaling + 团队规模决策 |

## 经验法则

```
任务并行价值 > 线性 token 成本？
├── 是 → Agent Teams（3-5 teammates）
├── 否（日常任务）→ 单 session
└── 中间（独立子任务不需互通信）→ Subagents
```

## Related
- [[concepts/claude-code-agent-teams]] — Agent Teams 总体
- [[concepts/agent-team-race-condition-task-claim]] — File lock 防双扣 token 浪费
- [[skills/claude-code-token-optimization]] — 通用 token 优化
- [[concepts/ai-tool-specialization]] — 按模型分级调度
- anthropic-claude-code-agent-teams-docs — 官方一手
- [[synthesis/concepts-agent-team-cost-overhead × entities-oh-my-openagent|Agent Team 成本 × omo 编排器]] — synthesis
- [[synthesis/concepts-agent-team-cost-overhead × entities-claude-code-agent-teams-feature|Agent Teams 成本曲线 × Agent Teams 特性]] — synthesis(线性扩展与功能门控的权衡)
