---
title: "Agent Team Mailbox 协议"
category: concepts
tags:
  - claude-code
  - ai-agents
  - ipc
  - json
  - mailbox
  - concept
summary: "Claude Code Agent Teams 的 teammate 间消息系统：每个 agent 一个 JSON inbox 文件，路径 ~/.claude/teams/{team-name}/inboxes/{agent-name}.json，逐条校验 + 错误条目自动丢弃。"
sources:
  - "https://docs.claude.com/en/docs/claude-code/agent-teams"
created: "2026-08-05T04:30:00Z"
updated: "2026-08-05T04:30:00Z"
provenance:
  extracted: 0.90
  inferred: 0.08
  ambiguous: 0.02
base_confidence: 0.78
lifecycle: draft
lifecycle_changed: "2026-08-05"
tier: supporting
---

# Agent Team Mailbox 协议

> Claude Code Agent Teams 的 teammate 间**直接消息**系统：每个 agent 一个 JSON 文件作 inbox。这是 subagent 模式"只能单向汇报"的关键差异——agent teams 让 teammate 间**对等通信**。

## 文件位置

```
~/.claude/teams/{team-name}/inboxes/{agent-name}.json
```

其中：
- `{team-name}` = `session-` + session ID 前 8 字符
- `{agent-name}` = lead 分配的名字（如 `researcher` / `security-reviewer` / `qa-tester`）

## 协议行为（官方）

> "Each agent's mailbox is a JSON file at `~/.claude/teams/{team-name}/inboxes/{agent-name}.json`. Claude Code validates every entry when it reads a mailbox file. **Entries that don't match the message format are reported as errors and removed from the file**; the valid messages are still delivered."

> "Before v2.1.207, a single malformed mailbox entry caused a repeated error every second and blocked delivery for that mailbox until you deleted the file manually."

## 关键工程含义

| 性质 | 含义 |
|---|---|
| **文件即队列** | 写文件 = 发消息，读文件 = 收消息 |
| **逐条校验** | 损坏条目自动丢弃而非整文件失败 |
| **v2.1.207+ 自愈** | 损坏不再阻塞整个 mailbox |
| **v2.1.207 前** | 单条损坏会让整个 mailbox 每秒报错，需手删文件 |

## 与 TaskList / Team Config 的对比

| 文件 | 路径 | 用途 | 持久性 |
|---|---|---|---|
| **Mailbox** | `~/.claude/teams/{team-name}/inboxes/*.json` | 队友消息 | session 内 |
| **TaskList** | `~/.claude/tasks/{team-name}/` | 共享任务 | 持久（cleanupPeriodDays） |
| **Team config** | `~/.claude/teams/{team-name}/config.json` | 运行时状态 | session 结束删 |

## 与 vault 已有 IPC 模式的关系

| 系统 | 通道 | 用途 |
|---|---|---|
| [[concepts/worktree-durable-lease]] | `lease-id` 文件 + 128-bit 身份 | worktree 持久租约 |
| **Agent Team Mailbox** | inbox JSON 文件 | teammate 间消息 |
| [[concepts/deterministic-agent-memory]] | query → 内存 | 单 agent 查询 |

三者都是 vault "**文件系统当 IPC**" 哲学的具体实现：避开网络协议 / RPC 复杂度，靠文件 + 锁 = 简洁可靠。

## 实现细节（推测）

官方未公开 inbox JSON 的精确 schema。但合理推测：

```json
[
  {
    "from": "researcher",
    "to": "qa-tester",
    "type": "message",
    "content": "Found this in auth/jwt.ts line 42: ...",
    "timestamp": "2026-08-05T04:30:00Z"
  },
  ...
]
```

可能是**追加式数组**（append-only array），处理时按数组下标消费 + 删除已读条目。

## 调试建议

- `ls -la ~/.claude/teams/{team-name}/inboxes/` — 看消息流
- `cat ~/.claude/teams/{team-name}/inboxes/researcher.json | jq` — 检查某 teammate 收件箱
- 若 v2.1.207 前遇 mailbox stuck → 直接 `rm` 文件（手动 reset）

## Related

- [[concepts/claude-code-agent-teams]] — Agent Teams 总体概念
- [[concepts/agent-team-race-condition-task-claim]] — File lock 防 race（同 IPC 通道）
- [[concepts/worktree-durable-lease]] — 同 vault 文件系统 IPC 哲学
- [[sources/anthropic-claude-code-agent-teams-docs]] — 官方一手