---
title: "Agent Team 任务认领的 File Lock 机制"
category: concepts
tags:
  - claude-code
  - ai-agents
  - concurrency
  - file-locking
  - concept
summary: "Claude Code Agent Teams 的 task claim 用文件系统锁（file locking）防止多个 teammate 同时认领同一任务的 race condition；这是 vault deterministic-agent-memory 哲学的『动态调度』延伸。"
sources:
  - "https://docs.claude.com/en/docs/claude-code/agent-teams"
created: "2026-08-05T04:30:00Z"
updated: "2026-08-05T04:30:00Z"
provenance:
  extracted: 0.88
  inferred: 0.10
  ambiguous: 0.02
base_confidence: 0.75
lifecycle: draft
lifecycle_changed: "2026-08-05"
tier: supporting
relationships:
  - target: "[[concepts/deterministic-agent-memory]]"
    type: extends
---

# Agent Team 任务认领的 File Lock 机制

> Claude Code Agent Teams 在多 teammate 并行认领任务时，**用文件系统锁（file locking）** 保证一次只有一个 teammate 能 claim 同一任务。这把 [[concepts/deterministic-agent-memory]] 的"同 query 同答案 / 失败显式分桶"哲学从"静态查询"扩到"动态调度"。

## 官方原话

> "Task claiming uses file locking to prevent race conditions when multiple teammates try to claim the same task simultaneously."
> —— [[sources/anthropic-claude-code-agent-teams-docs]]

## 3 状态 + 2 模式 + 依赖

**3 状态**:
- `pending` — 未开始
- `in progress` — 已被某 teammate 认领
- `completed` — 完成

**2 种 assignment 模式**:
- **Lead assigns** — 用户告诉 lead 把任务 X 给 teammate Y
- **Self-claim** — teammate 完成当前任务后**自动**认领下一个未分配未阻塞的任务

**依赖**:
- pending 任务若有未完成依赖 → **不能被 claim**
- 某任务完成时，依赖它的任务**自动 unblock**

## 为什么需要 file lock

3 个 teammate 同时完成手头任务 → 3 个都去看 TaskList → 3 个都"想认领 task X"——如果不加锁：

```
T1: read TaskList  → task X is pending  → claim X
T2: read TaskList  → task X is pending  → claim X  ← RACE
T3: read TaskList  → task X is pending  → claim X  ← RACE
```

文件锁让"claim X"成为原子操作——T1 拿锁，T2/T3 等；T1 写完 `in_progress` + T1 的 owner 字段后释放锁；T2/T3 看到 task X 已经是 in_progress 不再 claim。

## 失败的常见模式（官方 Troubleshooting）

- **Task status can lag** — teammates 有时不标 completed → 依赖任务卡住
- **Orphaned tmux sessions** — teammates tmux session 残留未清
- **Lead shuts down before work is done** — lead 误判"团队完工"

## File lock 在 vault 已有概念里的位置

| 概念 | 失败语义 | 与 Agent Team lock 的关系 |
|---|---|---|
| [[concepts/deterministic-agent-memory]] | `fresh/stale/ambiguous/not-found` | 同 query 同答案（静态） |
| [[entities/openlore]] | `verified/approved_not_synced/drafts_pending` | 文档态机 |
| **Agent Team file lock** | `pending/in-progress/completed` | 任务态机（动态） |

三者是 vault "显式失败 / 状态分桶"哲学的**三个应用层**：

- deterministic-agent-memory: 内存查询
- openlore: 代码事实层
- agent team file lock: 多 agent 调度层

## 实现细节（推测）

官方未公开具体实现。可能的技术路径：
- **POSIX `fcntl` lock** (`flock` / `lockf`) — 进程间文件锁标准 API
- **`fs.watch` + inotify 事件** — 文件变化触发 claim
- **轮询 + 写时校验** — 简单但低效

## Related

- [[concepts/claude-code-agent-teams]] — Agent Teams 总体概念
- [[concepts/agent-team-mailbox-protocol]] — Mailbox JSON 文件协议（同级 IPC 通道）
- [[sources/anthropic-claude-code-agent-teams-docs]] — 官方一手
- [[sources/csdn-agent-teams-multi-process]] — IPC 工程视角