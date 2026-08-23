---
title: "Research: Claude Code Agent Teams"
category: synthesis
tags:
  - claude-code
  - ai-agents
  - anthropic
  - opus-4
  - multi-agent
  - research
sources:
  - "https://docs.claude.com/en/docs/claude-code/agent-teams"
  - "https://www.youtube.com/watch?v=cSkoaCCmq0w"
  - "https://www.cnblogs.com/dhcn/p/19694044"
  - "https://blog.csdn.net/2501_92593481/article/details/161169482"
created: "2026-08-05T04:30:00Z"
updated: "2026-08-05T04:30:00Z"
summary: "Claude Code Agent Teams 三轮调研综合：Opus 4.6 引入的多 agent 实验功能，与 subagent 的核心差异是对等通信 + 独立 context window；9 项官方限制 + 5 显示模式 + 3 hooks 事件 + linear scaling token 成本。"
provenance:
  extracted: 0.85
  inferred: 0.10
  ambiguous: 0.05
base_confidence: 0.78
lifecycle: draft
lifecycle_changed: "2026-08-05"
tier: core
---

# Research: Claude Code Agent Teams

> 三轮调研综合（2026-08-05）。**调研主题**：Claude Code Agent Teams 这一多 agent 实验功能的架构、机制、版本演进、成本权衡、与 subagent 模式差异。**首要来源**：Anthropic 官方文档（v2.1.178+），辅以中文教程、CSDN 工程视角解析、22 分钟视频教程。

## Overview

Claude Code Agent Teams 是 Anthropic 在 Opus 4.6（2026-02）引入的**实验性多 agent 协作功能**。它与已有 subagent 模式的根本差异不是"能不能多 agent"，而是 **teammates 是否能直接通信 + 是否各自独立 context window**。每个 teammate 是独立 Claude Code 进程，靠 Mailbox JSON 文件通信 + TaskList 文件锁防 race。token 成本随 teammate 数**线性增长**，官方推荐 3-5 teammates。功能仍标 experimental，有 9 项已知限制（无 session resumption / no nested teams / 不能跨 session 共享等）。

## Key Findings

### (K1) 启用方式：环境变量，非 settings 字段

官方原话（anthropic-claude-code-agent-teams-docs）：

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

> **修正 YouTube 教程**：[[misc/web-youtube-com-watch-v-cskoa-ccmq0w]] 的 `experimentalAgents: "on"` camelCase 字段是错的——官方只接受环境变量形式。

### (K2) 4 组件架构 vs subagent 单向汇报

| 维度 | Subagent | Agent Team teammate |
|---|---|---|
| Context | 独立窗口，结果回到主 | 独立窗口，**完全独立** |
| 通信 | 单向（向主汇报） | **双向**（teammate 间 Mailbox） |
| 协调 | 主 agent 全管 | **共享 TaskList + 自协调** |
| Token | Summarized back（low cost） | **Linear scaling**（high cost） |
| 适用 | 专注任务 | 需要讨论/协作的复杂任务 |

### (K3) 5 种显示模式

`teammateMode` setting 5 值：`"in-process"`（默认）/ `"split-panes"` / `"auto"` / `"tmux"` / `"iterm2"`。详见 [[concepts/agent-team-display-modes]]。

> **修正 YouTube 教程**：[[misc/web-youtube-com-watch-v-cskoa-ccmq0w]] 的 `tmux.splitPanes: true` settings 字段是错的——官方字段是 `teammateMode` 字符串。

### (K4) Token 成本：线性扩展

每个 teammate 独立 context window，token 用量随 teammate 数线性增长。官方建议：

- **3-5 teammates** 多数工作流最佳
- **5-6 tasks per teammate** 保持高效
- **15+ 不推荐**（协调爆炸）

> **修正 YouTube 教程**：[[misc/web-youtube-com-watch-v-cskoa-ccmq0w]] 提到 "$1.15 / 4 分钟 / 5 agent"——dashboard 时长只算主 lead，**真实账单应远高**。以 Anthropic Console 账单为准。

### (K5) 3 个新 hooks 事件

`TeammateIdle` / `TaskCreated` / `TaskCompleted`——退出码 2 = 给反馈阻止。这把 [[concepts/claude-code-hooks-lifecycle]] 体系延伸到 agent teams 场景。

### (K6) 9 项官方限制（experimental 性质）

详见 [[entities/claude-code-agent-teams-feature]]。**最影响实践的 3 个**：

1. **No session resumption** — `/resume` `/rewind` 后 lead 联系已不存在的 teammates
2. **No nested teams** — flat hierarchy，teammates 不能 spawn own teammates
3. **Permissions set at spawn** — 不能 spawn 时给独立 mode（spawn 后可改）

### (K7) File lock 防 race

> "Task claiming uses file locking to prevent race conditions when multiple teammates try to claim the same task simultaneously."

把 [[concepts/deterministic-agent-memory]] 的"同 query 同答案 / 失败显式分桶"哲学从"静态查询"扩到"动态调度"。详见 [[concepts/agent-team-race-condition-task-claim]]。

### (K8) Mailbox 协议：每个 agent 一个 JSON 文件

`~/.claude/teams/{team-name}/inboxes/{agent-name}.json`——逐条校验，损坏条目自动丢弃。v2.1.207 前单条 malformed 会让整个 mailbox 每秒报错。详见 [[concepts/agent-team-mailbox-protocol]]。

### (K9) Opus 4.6 + 1M context 是触发条件

Agent Teams 在 Opus 4.6（2026-02 发布）引入。1M token context window 让 teammates 能各自持有大 codebase 视图而互不挤占。

### (K10) 官方 4 类典型用例 + 1 类反例

**适用**：研究 / 评审、新模块开发、对抗式 debug、跨层协作。
**不适用**：sequential tasks、same-file edits、依赖密集工作。

## Core Concepts

| 概念 | 一句话 |
|---|---|
| [[concepts/claude-code-three-modes]] | Default / Subagents / Agent Teams 三模式分工 |
| [[concepts/claude-code-agent-teams]] | Agent Teams 总体机制 |
| [[concepts/agent-team-display-modes]] | 5 种 teammateMode 显示模式 |
| [[concepts/agent-team-race-condition-task-claim]] | File lock 防多 teammate 抢任务 |
| [[concepts/agent-team-mailbox-protocol]] | Mailbox JSON 文件 IPC 协议 |
| [[concepts/agent-team-cost-overhead]] | Linear scaling token 成本 |
| [[concepts/tmux-pane-split-for-agents]] | tmux 配置（已与官方字段对齐） |
| [[concepts/ai-agent]] | 通用 AI agent 框架，本文是 Claude Code 内具体落地 |
| [[concepts/agent-operating-system]] | AOS Handoff 层（CLAUDE.md）在 teammates 间天然工作 |
| [[concepts/deterministic-agent-memory]] | race lock 是其"动态调度"延伸 |

## Entities & Tools

| 实体 | 一句话 |
|---|---|
| [[entities/claude-code-agent-teams-feature]] | Agent Teams 功能实体 |
| [[entities/claude-code]] | 主体工具（Anthropic 终端编码 agent） |
| [[entities/gpakosz-tmux]] | tmux 配置哲学（vault 已有 6 个 tmux 概念页） |
| [[entities/openlore]] | "确定性 + 失败显式分桶"哲学与 race lock 同源 |
| [[entities/claude-mem]] | 跨会话记忆——agent teams 的"跨 session 共享"工具基础 |

## Contradictions & Open Questions

### 与 YouTube 教程的 3 处矛盾（已修正）

| YouTube 主张 | 官方实际 | 来源 |
|---|---|---|
| `experimentalAgents: "on"` settings 字段 | `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` 环境变量 | anthropic-claude-code-agent-teams-docs |
| `tmux.splitPanes: true` settings 字段 | `teammateMode: "tmux"` 字符串值 | anthropic-claude-code-agent-teams-docs |
| "$1.15 / 4 分钟 / 5 agent" 准确 | dashboard 只算主 lead，真实成本应线性扩展 | anthropic-claude-code-agent-teams-docs |

### Opus 4.6 价格未完全核实

- Round 2 搜到"$5/M input, $25/M output"——可能是基础 200K context 价
- YouTube 提到 "$10/$37.5" 1M context premium——可能真实存在但未独立验证
- **Open**：等 Anthropic 官方 pricing 页确认

### 中文教程的"3 层 teammates 模型"

cnblogs-agent-teams-complete-guide 提出 lead / 同事 / 观察员 3 层——**官方文档未采纳**，vault 暂不作为主框架。可能只是作者个人心智模型。

### 16-agent C 编译器演示

Anthropic engineering blog 有演示（`anthropic.com/engineering/building-c-compiler`），证明 Agent Teams 的并行能力上限。**未独立 fetch 验证**——anthropic-claude-code-agent-teams-docs 也未提及具体数字。

### 文档版本演进快

- v2.1.178 / v2.1.179 / v2.1.181-198 / v2.1.186 / v2.1.198 / v2.1.199 / v2.1.207
- **Open**：每次小版本都可能改变行为，本文是 v2.1.178+ 的快照

## Sources Consulted

| 来源 | 类型 | 关键贡献 |
|---|---|---|
| anthropic-claude-code-agent-teams-docs | 官方一手（paper） | 4 组件 / 5 显示模式 / 9 限制 / 版本演进 |
| [[misc/web-youtube-com-watch-v-cskoa-ccmq0w]] | YouTube 教程（blog） | 22 分钟演示，多处矛盾已修正 |
| cnblogs-agent-teams-complete-guide | 中文教程（blog） | 中文读者友好 + 3 层模型（不被官方采纳） |
| csdn-agent-teams-multi-process | CSDN 工程视角（blog） | IPC / 多进程视角（推测） |

## 调研方法论

**3 轮调研**（per `wiki-research` skill）：

- **Round 1 (broad survey)**: 10 searches × 5 angles（官方 / Opus 4.6 / 三模式对比 / race lock / tmux / pricing / shutdown / shared memory / flag 字段名）
- **Round 2 (gap fill)**: 5 targeted searches（pricing / effort levels / official docs / teammateMode / self-claim）
- **Round 3 (synthesis check)**: 1 fetch 官方 docs（v2.1.178+ 完整页面 36KB）— 解决 Round 1-2 的 5 处 Open Questions

**关键决策**：
- 不读太多二手——官方 doc 是权威
- 与 vault 已有概念对比（agent teams vs subagent vs AOS）
- 显式列出与 YouTube 教程的矛盾作为可信度信号

## Related

- [[entities/claude-code]] — 主体
- [[concepts/claude-code-three-modes]] — 三模式抽象
- [[concepts/agent-operating-system]] — Handoff 层支持
- [[skills/claude-code-token-optimization]] — token 优化（成本敏感）
- [[concepts/ai-tool-specialization]] — 按模型分级调度（成本控制）