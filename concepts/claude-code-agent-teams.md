---
title: "Claude Code Agent Teams 工程机制"
category: concepts
tags:
  - claude-code
  - ai-agents
  - opus-4
  - multi-agent
  - concept
summary: "Claude Code Agent Teams（Opus 4.6 / Claude Code v2.1.178+ 引入）的工程机制：team lead 委派、teammate 独立 context、File lock 防 race、Mailbox JSON 通信、5 显示模式、9 已知限制、按 agent 模型分级调度。"
sources:
  - "https://www.youtube.com/watch?v=cSkoaCCmq0w"
  - "https://docs.claude.com/en/docs/claude-code/agent-teams"
created: "2026-08-05T03:30:00Z"
updated: "2026-08-05T04:30:00Z"
provenance:
  extracted: 0.88
  inferred: 0.08
  ambiguous: 0.04
base_confidence: 0.80
lifecycle: draft
lifecycle_changed: "2026-08-05"
tier: supporting
relationships:
  - target: "[[concepts/agent-team-race-condition-task-claim]]"
    type: related_to
  - target: "[[concepts/agent-team-mailbox-protocol]]"
    type: related_to
  - target: "[[concepts/agent-team-display-modes]]"
    type: related_to
  - target: "[[concepts/agent-team-cost-overhead]]"
    type: related_to
  - target: "[[entities/claude-code-agent-teams-feature]]"
    type: related_to
  - target: "anthropic-claude-code-agent-teams-docs"
    type: derived_from
  - target: [[concepts-agent-operating-system × concepts-deterministic-agent-memory]]
    type: related_to
---

# Claude Code Agent Teams 工程机制

> Agent Teams 是 Claude Code 在 Opus 4.6（Claude Code v2.1.178+）引入的多会话团队模式。与 Subagents 的"主会话 + 短命子"不同，**每个 teammate 拥有独立 Claude Code session（独立 context window）**——可被独立 inspect、interact、shutdown。下面是 6+ 个工程机制，每一个都对应 vault 已有概念的延伸。

> **调研依据**：本概念页综合 [[misc/web-youtube-com-watch-v-cskoa-ccmq0w]]（22 分钟视频教程）与 anthropic-claude-code-agent-teams-docs（Anthropic 官方文档）。**多处与 YouTube 矛盾的细节已按官方文档修正**（详见 [[synthesis/Research: Claude Code Agent Teams]] 的 Contradictions 段）。

## 机制 1：必须显式触发

> "Anthropic tells us specifically that we must tell Claude to create an agent team. In all the examples... it always says create an agent team."

可用的触发措辞：
- `Create an agent team` —— 让 leader 自决 agent 数与分工
- `Create three different team members that focus on A, B, and C` —— 显式指定
- `Use Sonnet for all the agents` —— 顺便指定模型

## 机制 2：Team Leader 委派模型

Team leader 收到你的请求后：

1. **理解问题** —— "what's the job to be done here?"
2. **拆任务列表** —— "what are the different tasks that we need to complete?"
3. **为每个 agent 写专属 prompt** —— "what are the different prompts that we need for each of these agents"
4. **逐个 spool up agent** —— 直到所有 agent 都进入"房间"（tmux pane）
5. **监控进度** —— agent 完成后回收资源

**leader 自己不干活**——纯调度者。

## 机制 3：Agent 上下文隔离

> "these guys do not get access to the entire conversation thread"

默认 agent **只看到自己被分配的 prompt**。如果你已经跟 Default 会话聊了 30 分钟做 web search + 读代码，**这些上下文 agent 都看不到**。

**工程含义**：

- 用户必须在 Default 会话里把核心结论落 MD 文件
- 然后用 "create an agent team to investigate X, please read the MD file <path> first" 这样的措辞
- agent 才能"用相同的上下文"开工

这与 [[concepts/agent-operating-system]] 的 Handoff 层同构——但从"单 session 交接"扩展到"多 agent 团队交接"。

## 机制 4：Race-Condition Task Lock

> "there is a list of tasks that have to be completed... if I finish my task at the same time that you do, we both reach for the next task. How do we know that we're both not wasting tokens working on the same task?"

Anthropic 内置**任务级悲观锁**："whenever I take the task if I'm just incrementally faster than you, it's already blocked off."

这把 [[concepts/deterministic-agent-memory]] 的"同 query 同答案 / 失败显式分桶"哲学从"静态查询"扩展到"动态调度"——多 agent 抢任务时绝不会"两个 agent 同时改一个文件"。

## 机制 5：按 Agent 模型分级调度

> "you can also define which model you want to use for those team members"

Opus 4.6 价格 $5/M input, $25/M output（Round 2 验证——基本 200K context tier；1M context premium 价 ambiguous）。**不是每个 agent 都需要 Opus**——简单任务用 Sonnet/Haiku 显著省钱且通常更快。

策略：
- **Opus 给 team lead** —— 它要做正确的 plan + 拆任务 + 写 prompt
- **Sonnet/Haiku 给具体干活 agent** —— 任务清单清楚后，执行不需要顶级模型
- **可混合** —— 关键模块 backend agent 用 Sonnet，QA agent 用 Haiku 即够
- **官方**：`teammates 不继承 lead 的 /model` 默认行为；可改 `/config` → "Default teammate model" 或 spawn 时显式 `Use Sonnet for each teammate`

详见 [[concepts/agent-team-cost-overhead]]。

## 机制 6：Graceful Shutdown

视频展示的 shutdown 有三种：

1. **手动停单个 agent** —— "Ask the [agent name] teammate to shut down"，agent 可拒绝（"我还在做关键工作"）并说明理由
2. **自动全关（research 场景）** —— leader 默认行为
3. **保留 idle 等 review（coding 场景）** —— leader 关团队但保留关键 agent 等用户测试，发现 bug 让对应 agent 继续修

> "you maintain like that backend agent maintains the context of what they were working on... they should be able to just jump back into the project and fix whatever you're telling them"

这把 [[concepts/agent-operating-system]] 的 Handoff 层做成"实时"——不需要"收工"动作，agent 保持会话上下文等你下次下指令。

**官方限制**：shutdown may be slow——teammates 等当前请求/tool 完成才退。

## 机制 7（官方新增）：File Lock + Mailbox IPC

> 官方 anthropic-claude-code-agent-teams-docs 明确：

- **Task claim** 用 file locking 防多 teammate 抢同一任务（[[concepts/agent-team-race-condition-task-claim]]）
- **Mailbox** JSON 文件作 teammate 间 IPC（[[concepts/agent-team-mailbox-protocol]]）

## 机制 8（官方新增）：5 种显示模式

`teammateMode` setting 5 值：`in-process` / `split-panes` / `auto` / `tmux` / `iterm2`。详见 [[concepts/agent-team-display-modes]]。

## 机制 9（官方新增）：3 个新 hooks 事件

`TeammateIdle` / `TaskCreated` / `TaskCompleted`——退出码 2 = 给反馈阻止。把 [[concepts/claude-code-hooks-lifecycle]] 延伸到 agent teams。

## 与 YouTube 教程的关键差异（已修正）

| 项 | YouTube | 官方实际 |
|---|---|---|
| 启用字段 | `experimentalAgents: "on"` | `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` env var |
| tmux 配置字段 | `tmux.splitPanes: true` | `teammateMode: "tmux"` 字符串 |
| TeamCreate 工具 | 仍可用 | **v2.1.178 后不存在**，自动建队 |
| Dashboard 时长 | 准确反映 5 agent | **只算主 lead**，真实成本更高 |

## 共享记忆 MD：跨 session 桥

视频明确建议的"shared memory MD file"模式：

```
project/
└── .team-shared/
    └── issues-and-fixes.md    ← 所有 agent 实时落盘的 bug / 修复记录
```

下次再开新 session 或新 agent 团队，**直接读这份 MD 就能延续上下文**——这是 [[concepts/agent-operating-system]] Knowledge Base 层在多 agent 团队的具体实现。

## 成本可观测性的坑

视频展示的 4 分钟研究跑完 $1.15，但 API duration 显示只约 5 分钟而非理论 4 agent × 5 分钟 = 20 分钟。**作者承认 dashboard 不准**：

> "Typically when you're running multiple different agents, their API duration will compound. So if you have five agents running for 5 minutes, it'll typically say 25 minute duration."

**结论**：以账单为准，dashboard 时长只算主 leader 不算所有 agent。

## Related

- [[misc/web-youtube-com-watch-v-cskoa-ccmq0w]] — 视频源（与官方多处矛盾，已修正）
- [[synthesis/Research: Claude Code Agent Teams]] — 三轮调研综合（10 页）
- anthropic-claude-code-agent-teams-docs — 官方一手文档（v2.1.178+）
- [[entities/claude-code-agent-teams-feature]] — Agent Teams 功能实体
- [[concepts/claude-code-three-modes]] — 三模式抽象，Agent Teams 是其中之一
- [[concepts/tmux-pane-split-for-agents]] — tmux 配置（已与官方字段对齐）
- [[concepts/agent-team-display-modes]] — 5 种 teammateMode
- [[concepts/agent-team-race-condition-task-claim]] — File lock 防 race
- [[concepts/agent-team-mailbox-protocol]] — Mailbox JSON IPC
- [[concepts/agent-team-cost-overhead]] — Linear scaling token 成本
- [[concepts/agent-operating-system]] — Handoff / KB 层在多 agent 团队的扩展
- [[concepts/deterministic-agent-memory]] — race lock 是其"动态调度"延伸
- [[concepts/ai-tool-specialization]] — 按模型分级调度是 AI 工具栈专业化的成本工程体现
- [[entities/claude-code]] — 主体工具