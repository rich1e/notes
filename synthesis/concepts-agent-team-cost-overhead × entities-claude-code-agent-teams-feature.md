---
title: Agent Teams 成本曲线 × Agent Teams 特性 — 线性扩展与功能门控的权衡
category: synthesis
tags:
  - claude-code
  - agent-teams
  - token-cost
  - feature-flag
  - experimental
  - linear-scaling
  - subagent
sources:
  - "[[concepts/agent-team-cost-overhead]]"
  - "[[entities/claude-code-agent-teams-feature]]"
  - "[[concepts/agent-team-display-modes]]"
  - "[[concepts/agent-team-mailbox-protocol]]"
  - "[[concepts/agent-team-race-condition-task-claim]]"
  - "[[concepts/claude-code-three-modes]]"
created: 2026-08-31T04:27:59Z
updated: 2026-08-31T04:27:59Z
summary: Agent Teams 启用 env var + 4 组件架构 = 功能上限;每个 teammate 独立 context window + 线性 token 增长 = 经济上限。两个上限相互独立又相互制约,推荐 3-5 teammates 不是"软建议"而是 _硬约束_:再少浪费特性,再多破产成本。
tier: supporting
lifecycle: draft
lifecycle_changed: 2026-08-31
base_confidence: 0.78
provenance:
  extracted: 0.68
  inferred: 0.27
  ambiguous: 0.05
relationships:
  - target: "[[concepts/agent-team-cost-overhead]]"
    type: synthesizes
  - target: "[[entities/claude-code-agent-teams-feature]]"
    type: synthesizes
  - target: "[[concepts/agent-team-display-modes]]"
    type: related_to
  - target: "[[concepts/agent-team-mailbox-protocol]]"
    type: related_to
---

# Agent Teams 成本曲线 × Agent Teams 特性

## The Connection

`agent-team-cost-overhead` 给出 _经济学_ 答案:每个 teammate 独立 context window,token 随 teammate 数线性扩展,推荐 3-5 teammates + 5-6 tasks per teammate,作为对照 subagent 的 summarized-back 模型。`claude-code-agent-teams-feature` 给出 _功能学_ 答案:v2.1.178+ 实验特性,需要 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` env var 启用,4 组件架构 + 5 显示模式 + 9 已知限制。两个页面单看都 _不_ 互相解释:成本页看不到 _为什么_ 是 3-5 而不是 10-20,功能页看不到 _为什么_ 还没默认开启。两者合在一起才显出 vault 里反复出现的"实验特性 × 经济学约束"模式。

## Where They Co-occur

8 个 wiki 页同时引用两者,典型语境:

- **subagent ↔ agent-teams 对照**:[[concepts/claude-code-three-modes]] 在 Plan / Explore / subagent / Agent Teams 四种调用模式间横切;本合成聚焦 subagent vs Agent Teams 这条边——前者 _summarized-back_ 后者 _共享文件系统_
- **架构组件 vs 成本单元**:entity 页的 4 组件中 mailbox 是 _每个 teammate 一个 JSON 文件_ ,数量随 teammate 线性扩展——这是成本增长的 _物理载体_
- **race-condition 与成本**:[[concepts/agent-team-race-condition-task-claim]] 的 file-locking 锁机制在 teammate 越多时 _价值越大_ ——但成本模型给 teammate 数上界,锁机制只在下界起作用
- **显示模式 ↔ 成本可见性**:[[concepts/agent-team-display-modes]] 的 tmux/iterm2 模式 _把成本可见化_ ——每个 pane 一个独立窗口,token 燃烧看得见

## Cross-cutting Insight

**特性门控与成本上限是同一道 _约束方程_ 的两侧**。把它写成公式:

```
total_cost ≈ teammate_count × (context_window_per_teammate × token_price)
            + mailbox_count × (inbox_io × fs_latency)
            + race_retry_count × (lock_retry_overhead)
```

四个变量中:

- `teammate_count` 是用户可控,推荐 3-5 是 _在特性能力(组件数 vs 任务并行度)与成本曲线(线性扩展)的拐点_
- `context_window_per_teammate` 是 Anthropic 决定——每个 teammate 是独立 claude 会话,无法共享 system prompt / tool definitions
- `mailbox_count = teammate_count`,因为一对一;inbox I/O 用文件系统 = _免费_
- `race_retry_count` 与任务分布有关,但受 file-locking 控制上界

**核心推论**:实验特性 × 线性成本 = 必须门控。如果 Agent Teams 默认开启,3-5 teammates × 长会话 = 单次任务 $5-50,与单 subagent 的 $0.10-1 差 1-2 个数量级——这是为什么 env var _必须_ 显式开启,而不是默认在 settings.json 提供。^[inferred]

## Tensions and Trade-offs

| 维度 | 成本视角 | 功能视角 | 张力 |
|---|---|---|---|
| 默认开启 | 应默认关闭(保护用户钱包) | 体验更顺(用户无需翻文档) | 文档 vs 默认 |
| Teammate 上限 | 越少越好(线性成本) | 越多越好(并行度) | 经济 vs 性能 |
| Context sharing | subagent 的 summarized-back 更便宜 | Agent Teams 共享 mailbox 更强大 | 共享 vs 经济 |
| 锁机制 | 增加成本(retry overhead) | 降低 bug 率(race condition) | 安全 vs 速度 |
| 显示模式 | 越简单越便宜(in-process) | 越丰富越好(tmux/iTerm) | UX vs 成本 |

## Strongest Objection

**批评**:把"3-5 teammates"包装成 _拐点_ 是 _后合理化_——很可能 Anthropic 内部只是 _觉得_ 这个数量"够用",而不是做过严格的成本/性能拐点计算。线性扩展是 _给定_ 的(物理事实),但 _推荐数字_ 完全可以是 _保守建议_——若官方做 100 次实验发现 7-9 teammates 在多数任务上 _更快_,数字就会改。本合成页把推荐数字当成 _硬约束_ 是过度解读。

> test: 跑一个固定的"代码调研 + 单元测试"任务,teammate 数 3 / 5 / 7 / 9,记录 _完成时间_ 和 _token 消耗_。如果 7 teammates 的时间 < 3 teammates 的 1.5 倍但 token < 2 倍,推荐数字就 _不是_ 拐点,而是 _保守下限_。

## Open Questions

- vault 没有 `claude-code-three-modes` vs `agent-teams` 的合成页——三种 Plan/Explore 模式与 Agent Teams 是 _正交_ 还是 _替代_ 关系?
- `mailbox_count` 是否可以 _共享_ ——多个 teammate 共用一个 inbox + 自动分发?这会打破当前 1:1 模型但降低成本
- token 消耗的 _具体数字_ 在 vault 里没有出现(只有定性"线性")——值得补一个实测 [[references/claude-code-agent-teams-token-bench]]
- 9 个已知限制的 _具体清单_ 是 wiki-lint 候选

## Related

- [[concepts/agent-team-cost-overhead]]
- [[entities/claude-code-agent-teams-feature]]
- [[concepts/agent-team-display-modes]]
- [[concepts/agent-team-mailbox-protocol]]
- [[concepts/agent-team-race-condition-task-claim]]
- [[concepts/claude-code-three-modes]]
- [[synthesis/Research: Claude Code Agent Teams]]
- [[synthesis/concepts-agent-team-display-modes × entities-claude-code-agent-teams-feature]]