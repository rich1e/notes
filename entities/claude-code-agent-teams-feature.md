---
title: "Claude Code Agent Teams 功能"
category: entities
tags:
  - claude-code
  - ai-agents
  - anthropic
  - experimental
  - entity
summary: "Claude Code Agent Teams 是 Anthropic 的实验性多 agent 协作功能（v2.1.178+），需 env var CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 启用，4 组件架构 + 5 显示模式 + 9 已知限制。"
sources:
  - "https://docs.claude.com/en/docs/claude-code/agent-teams"
created: "2026-08-05T04:30:00Z"
updated: "2026-08-05T04:30:00Z"
provenance:
  extracted: 0.92
  inferred: 0.06
  ambiguous: 0.02
base_confidence: 0.85
lifecycle: draft
lifecycle_changed: "2026-08-05"
tier: supporting
relationships:
  - target: "[[entities/claude-code]]"
    type: related_to
  - target: "[[concepts/claude-code-three-modes]]"
    type: related_to
  - target: "[[concepts/claude-code-agent-teams]]"
    type: related_to
  - target: "[[concepts/agent-team-display-modes]]"
    type: related_to
  - target: "[[concepts/agent-team-mailbox-protocol]]"
    type: related_to
  - target: "[[concepts/agent-team-race-condition-task-claim]]"
    type: related_to
  - target: "[[concepts/agent-team-cost-overhead]]"
    type: related_to
  - target: [[concepts-agent-operating-system × concepts-deterministic-agent-memory]]
    type: related_to
---

# Claude Code Agent Teams 功能

> Claude Code 的**实验性多 agent 协作功能**（v2.1.178+）。由 [[entities/claude-code]] 主产品提供的"多 Claude Code 实例协作"能力——一个 lead session 协调多个 teammate sessions。

## 是什么

Agent Teams 是 Claude Code 在 Opus 4.6 时代（2026-02）引入的实验性功能。**核心定位**：

- **多 Claude Code 实例协作**——不只是主+子（subagent），而是真正对等通信
- **共享任务列表**——所有 teammate 看到同一个 TaskList，自己认领
- **直接消息系统**——Mailbox JSON 文件让 teammate 间对等通信
- **可选 split-pane 可视化**——每个 teammate 一个 tmux pane

## 启用方式

环境变量 / settings.json env 块：

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

**默认值**：关闭。`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` 是唯一开启方式。

## 4 组件架构

| 组件 | 角色 |
|---|---|
| Team lead | 主 session，spawn + 协调 |
| Teammates | 独立 Claude Code 实例，各自 context |
| Task list | 共享任务，file lock 防 race |
| Mailbox | teammate 间 JSON inbox 文件 |

## 何时用 / 何时不用

**强适用**：
- 多角度并行研究（多 teammate 各查一个方面）
- 独立模块并行开发
- 对抗式 debug（5 teammate 互驳找真因）
- 跨层协作（前端/后端/测试各归一个）

**不适用**：
- 串行任务
- 同文件多人编辑（overwrites）
- 依赖密集工作
- 简单日常任务（成本不划算）

## 5 种显示模式

`teammateMode` setting 5 种值：`in-process`（默认）/ `split-panes` / `auto` / `tmux` / `iterm2`。详见 [[concepts/agent-team-display-modes]]。

## 9 项已知限制

1. 无 session resumption with in-process teammates（`/resume` `/rewind` 不恢复 teammates）
2. Task status can lag（teammates 有时不标 completed）
3. Shutdown can be slow（teammates 等当前请求完才退）
4. One team per session（不能跨 session 共享）
5. No nested teams（flat hierarchy）
6. No background subagents from in-process teammates
7. Lead is fixed（不能 promote teammate）
8. Permissions set at spawn（不能 spawn 时给独立 mode）
9. Split panes require tmux or iTerm2（不支持 VS Code 集成 / Windows Terminal / Ghostty）

## 版本演进（重要）

- **v2.1.178+**：自动建队（无需 TeamCreate 工具）；session 退出自动清理
- **v2.1.179+**：`"in-process"` 成为默认（之前是 `"auto"`）
- **v2.1.181-198**：idle 行 30s 后隐藏（即便其他 teammate 在工作）
- **v2.1.186+**：split-pane teammates 继承 lead effort level
- **v2.1.198+**：turn 结束在 API error 时通知 lead 失败
- **v2.1.199+**：idle 行在整个 panel 都 idle 才隐藏；`/model` `/fast` 在 teammate 视图内显示"apply to lead"提示
- **v2.1.207+**：mailbox 单条 malformed 不再阻塞整个 mailbox

## 历史

Anthropic 演示了用 **16 个 agents** 自主构建 C 编译器的用例（anthropic.com/engineering/building-c-compiler）——证明 Agent Teams 的并行能力上限。

## 与 vault 已有知识簇的关系

| vault 已有 | 在 Agent Teams 的延伸 |
|---|---|
| [[entities/claude-code]] | 主体产品 |
| [[concepts/ai-agent]] | Agent Teams 是 multi-agent 模式的具体实现 |
| [[concepts/agent-operating-system]] | Handoff 层（CLAUDE.md）天然支持 teammates |
| [[concepts/deterministic-agent-memory]] | race lock 是其"动态调度"延伸 |
| [[concepts/claude-code-hooks-lifecycle]] | 3 个新 hooks（TeammateIdle/TaskCreated/TaskCompleted） |
| [[entities/gpakosz-tmux]] | tmux 配置哲学应用到 split-pane mode |
| [[concepts/ai-tool-specialization]] | 按模型分级调度是成本控制核心 |

## Related

- [[synthesis/Research: Claude Code Agent Teams]] — 综合分析
- anthropic-claude-code-agent-teams-docs — 官方一手文档
- [[concepts/claude-code-agent-teams]] — 概念抽象
- [[misc/web-youtube-com-watch-v-cskoa-ccmq0w]] — 视频教程（与官方多处矛盾，已修正）
- [[synthesis/concepts-agent-team-display-modes × entities-claude-code-agent-teams-feature|Agent Teams 显示模式 × Agent Teams 特性]] — synthesis(隔离域选择)
- [[synthesis/concepts-agent-team-cost-overhead × entities-claude-code-agent-teams-feature|Agent Teams 成本曲线 × Agent Teams 特性]] — synthesis(线性扩展与功能门控)