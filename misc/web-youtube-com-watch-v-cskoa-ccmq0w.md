---
title: "Claude Code 三种工作模式（Default / Subagents / Agent Teams）"
category: misc
tags:
  - claude-code
  - ai-agents
  - opus-4
  - tmux
  - workflow
sources:
  - "https://www.youtube.com/watch?v=cSkoaCCmq0w"
source_url: "https://www.youtube.com/watch?v=cSkoaCCmq0w"
created: "2026-08-05T03:30:00Z"
updated: "2026-08-05T03:30:00Z"
summary: "视频教程：Claude Code Opus 4.6 引入 Agent Teams 新模式，与 Default / Subagents 形成三模式分工；含 tmux 配置、team leader 委派、race-condition 任务锁、模型分级调度、shared memory MD 等工程细节。"
affinity: {}
promotion_status: misc
stub: false
provenance:
  extracted: 0.78
  inferred: 0.18
  ambiguous: 0.04
base_confidence: 0.45
lifecycle: draft
lifecycle_changed: "2026-08-05"
tier: supporting
---

# Claude Code 三种工作模式（Default / Subagents / Agent Teams）

## Overview

某英文 YouTube 频道（视频标题：*Claude Code Agent Teams Masterclass*）实操讲解 Claude Code 三种工作模式的本质区别：**Default 单会话**、**Subagents 主会话 + 短命子任务**、**Agent Teams 多会话团队**（Opus 4.6 引入）。重点不是按键操作，而是"哪种任务适合哪种模式"的判断逻辑 + tmux split-pane 工程化 + race-condition 防双扣 + shared memory MD 跨会话桥梁。

视频本身是单源二手教程（YouTube 创作者，未必是 Anthropic 官方），下面的判断标注 `^[inferred]` 表示是从视频语言推断出的工程含义，`^[ambiguous]` 表示视频里说模糊或与 vault 已知内容冲突。

## Key Points

### 三模式的核心差异：会话（session）的数量

| 模式 | 会话数 | 何时用 |
|---|---|---|
| **Default** | 1（与你对话的那个） | 通用系统管理员：选模型、看技能、规划项目 |
| **Subagents** | 1 主 + N 短命子 | 主上下文外的 token 节流：让子 agent 跑远活只回总结 |
| **Agent Teams** | 1 主（team leader）+ N 独立长会话 | 大任务、多视角、需要 agent 间互相通信 |

> "Technically speaking, everything you can do in agent team mode and sub agent mode, you can also do in default mode. The biggest difference is in how the session is managed."

### "隧道视野（tunnel vision）"是模式选择的核心判据

每个 LLM agent 在单 session 内都倾向于"锁定一个方向"——这是 hallucination 与 yes-man 综合症的根源。三模式按会话数递增本质上是**强制多视角**的手段：

- **Default** —— 单视角，易 tunnel vision
- **Subagents** —— 主会话省 token，子 agent 视角独立但**不互相通信**
- **Agent Teams** —— N 个独立视角，**互相能通过 team leader 转告**（"三楼五号房有异常，附近的人准备支援"）

视频原话："you can actually deploy each of these agents and tell them you look at this from the left side, you look at this from the right side, and you go upstairs and you look at it from the top down"

### Subagent 模式的 token 节流原理

子 agent 完成复杂任务（如"加 Google 登录"）只回一句总结，**主会话只增加结论**而非中间过程。主会话上下文从"10 轮导航、5 个文件、3 个对话"压缩为 1 条结论。Subagent 失败则回报新 issue 而不是用无效 token 拖累主。

### Agent Teams 的 6 个工程机制

1. **触发关键词必须显式** —— 视频反复强调"You must tell Claude to create an agent team"。可用措辞：`create an agent team`、`create three different team members that focus on A, B, and C`、或更开放让 leader 自决。
2. **Team leader 负责 plan + task list + prompt per agent** —— 它读你的问题，拆任务，给每个 agent 写专属 prompt。
3. **Agent 不共享原始对话上下文** —— 这是关键设计：默认 agent 只看到自己被分配的 prompt，所以**用户必须先把核心上下文落 MD 文件**，再让 leader "read this MD and here's your task"。
4. **Race condition 防双扣** —— Anthropic 内置任务锁："whenever I take the task if I'm just incrementally faster than you, it's already blocked off." 避免两个 agent 同时争同一任务浪费 token。
5. **每 agent 可指定模型** —— Opus 4.6 价格约 $10/$37.5 per M input/output；**不需要每个 agent 都用 Opus**——可在 prompt 里写"用 Sonnet"，5 个 Sonnet 跑 5 分钟会比 1 个 Opus 更便宜且更快出结果。
6. **Graceful shutdown + 保留关键 agent** —— Leader 默认关闭整个 team，但**在 coding/research 场景会保留 idle 等用户 review**：可以发回 QA agent 重新检查某一模块，或保留 backend agent 维持它的会话上下文等下个 bug 报告。

### tmux split-pane 是 Agent Teams 的可视化前提

视频明确：**tmux 不在 VS Code/Cursor 内工作，必须在原生终端**。

```jsonc
// settings.json (全局，推荐)
{
  "tmux.splitPanes": true,
  "experimentalAgents": "on"   // 等价于勾选 agent teams 功能
}
```

启动顺序也强制：

1. `tmux`（先开复用器，分配房间）
2. `claude --dangerously-skip-permissions`（再开 agent）

**不能直接开 claude**——没有 tmux 就只有一个共享终端，5 个 agent 在同一房间互相喊话，根本没法看谁在做什么。

### Opus 4.6 模型与 effort 调节

- **200K 上下文** vs **1M 上下文**（200K 以上按 $10/$37.5 per M 计 premium 价）
- **effort 五档**：low（最便宜，能力降）→ medium（平衡，省 token）→ high（复杂推理）→ **最大**（仅 Opus 4.6 全开）
- 视频推荐：先 Opus + low；遇到速度/质量问题再阶梯往上调

### Shared Memory MD：跨 session 桥

视频明确建议用**共享 MD 文件**让 agent 团队长期持久：

> "you could create a shared memory MD file where you get all the agents to log all their issues like all the bugs they ran into and all the all the stuff they've tried to debug"

这把 [[concepts/agent-operating-system]] 里的 **Handoff (Task Memory)** 模式从"单 session 交接"扩展为"多 agent 团队交接"——同一份 MD 既给 agent 内回看也跨 session 给未来的 agent 引用。

### Skill-as-Team-Template

把"我每次都要 prompt 一个 research team"流程化：

1. 先手动跑一遍完整流程（不只是 `create agent team`，还要 review 结果、改 prompt、要 PDF 等）
2. 完成后 Claude Code 自动归纳："Turn whatever we just did into a skill"
3. 存到 `.claude/skills/research/` 后 `/research <topic>` 即用
4. 流程变了直接 "update the skill"——Claude 改 skill 不需要你重写

视频原话："every time you actually run the skill, if there is an update to the process that you want to make, you can just go back into Claude and just reprompt and say, 'Hey, this new adjustment to the process...'"

### 成本可观测性的坑

视频展示的 4 分钟研究跑完收费 $1.15，**但顶部 API duration 显示只约 5 分钟而非理论上的 4 agent × 5 分钟 = 20 分钟**。视频作者承认"This is not 100% correct"，可能是 dashboard 只算主 leader 时长。**判断**：多 agent 实际成本应按 leader 时长 × agent 数预估，但 dashboard 不一定如实反映——以账单为准。

## Concepts

- [[concepts/claude-code-three-modes]] — Default / Subagents / Agent Teams 三模式抽象
- [[concepts/claude-code-agent-teams]] — Agent Teams 工程机制（race lock、leader delegation、shared memory）
- [[concepts/tmux-pane-split-for-agents]] — tmux split-pane 配置 + 启动顺序
- [[concepts/ai-agent]] — 通用 AI agent 框架；本文是 Claude Code 的具体落地
- [[concepts/agent-operating-system]] — AOS 五层记忆；shared memory MD 是 Handoff 层在多 agent 团队的扩展
- [[concepts/ai-tool-specialization]] — Agent Teams 是"AI 工具栈专业化分工"的运行时体现
- [[concepts/deterministic-agent-memory]] — race-condition task lock = "同 query 永不模糊抢"的具体实现

## Entities

- [[entities/claude-code]] — 主体工具；本页是它的模式分支详解
- [[entities/openlore]] — "失败显式分桶 + 同 query 同答案"哲学与 agent teams race lock 同源
- [[entities/gpakosz-tmux]] — tmux 配置哲学的另一极；本文用其 `.local` 覆写模式扩展 Agent Teams 配置
- `Anthropic` ^[inferred] — Claude Code 与 Opus 4.6 / agent teams 功能出品方

## Open Questions

- 视频里 "$1.15 / 4 分钟 / 5 agent" 的账单数字与"理论应 ~20 分钟 API duration"不一致。**根因未明**——是 dashboard 只算主 leader、还是 Anthropic 并行批价、还是某 agent 提前 idle？^[ambiguous]
- "agent teams 默认 shutdown 还是保留 idle 等 review"是否可配置？视频暗示 coding 场景默认保留 idle，但未说有没有 settings 字段强制。^[ambiguous]
- "shared memory MD"是否需要人为写入 commit hook，或 Agent Teams 是否自动落盘？视频只说"you could create"，未给自动机制。 ^[inferred]
- **Opus 4.6 这个版本号是视频口误还是真名**？当前 (2026-08) Anthropic 公开模型为 Claude 4 Sonnet / Opus 系列；视频里的"Opus 4.6 200K / 1M 双档 + effort 五档"是否能精确对应到现行 model ID，需对照 Anthropic 官方 pricing 页核实。 ^[ambiguous]
- "experimentalAgents: on" 这种 camelCase flag 是否真是 settings.json 字段名？视频未贴完整 settings.json 截图。 ^[ambiguous]

## Related

- [[synthesis/concepts-agent-operating-system × concepts-deterministic-agent-memory]]
- [[skills/claude-code-settings]] — settings.json 四级作用域；本视频建议**全局配置** agent teams
- [[skills/claude-code-token-optimization]] — Subagents 模式的核心动机就是 token 节流
- [[skills/tmux]] — 通用 tmux 速查；本文是 tmux 在 AI agent 场景的具体应用
- [[skills/zellij-terminal-multiplexer]] — Zellij 也能实现类似 split-pane per agent，是否兼容 Agent Teams 模式未验证 ^[inferred]
- [[concepts/tmux-pane-maximize-stateful]] — gpakosz 实现的 pane maximize；Agent Teams 下可能想 maximize 当前 working agent 的 pane