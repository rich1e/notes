---
title: AI 编码 agent 的工作树隔离
category: concepts
tags:
  - ai-agent
  - sandbox
  - isolation
  - worktree
  - treehouse
  - parallel-agents
sources:
  - https://github.com/kunchenguid/treehouse
  - _raw/github-kunchenguid-treehouse.txt (gitingest export, kunchenguid/treehouse, 2026-08-03)
created: 2026-08-03T11:40:00Z
updated: 2026-08-03T11:40:00Z
summary: 为同时运行的多个 AI 编码 agent 各自分配一个隔离、可重用、可清理的 git worktree:detached HEAD 避免分支冲突,池复用保留依赖/构建缓存,durable lease 支持无人值守 long-running agent。
tier: supporting
lifecycle: draft
lifecycle_changed: 2026-08-03
base_confidence: 0.83
provenance:
  extracted: 0.88
  inferred: 0.12
  ambiguous: 0
relationships:
  - target: "[[entities/treehouse]]"
    type: derived_from
  - target: "[[concepts/git-worktree-pool-pattern]]"
    type: extends
  - target: "[[concepts/worktree-durable-lease]]"
    type: related_to
  - target: "[[concepts/agent-operating-system]]"
    type: related_to
  - target: "[[concepts/ai-agent]]"
    type: related_to
---

# AI 编码 agent 的工作树隔离

> "Manage worktrees without managing worktrees." —— 当多个 AI 编码 agent 同时改同一个仓库时,谁拥有哪个工作树、写哪里、谁清场,需要一套轻量 runtime。

## 为什么这成了一个独立的工程问题

过去的人(单 IDE + 单分支)心智模型是"切换分支就行"。当出现下面任一种时,朴素模式开始不够用:

- **多 AI agent 并行**(Claude Code + Codex + opencode + 自家脚本),每个 agent 都会 stash、commit、reset、推分支。
- **agent session 重启频繁**:每个新会话从空 worktree 开始 → 重新装 `node_modules` / SwiftPM / Python venv / 重新 fetch pnpm store → 算力大量浪费在 setup。
- **异步 / 长期 agent**:agent runner(后台 daemon、CI worker)希望"持有一个 worktree 持续写",而不是每次都 spawn subshell。
- **错误恢复**:agent 半路崩了、用户误 ctrl-c、整批调度死锁,需要"怎样都能从一个明确 state 重新 acquire"。

treehouse 这一类工具的答案:**池化 worktree** —— 见 [[concepts/git-worktree-pool-pattern]]。

## 必须满足的属性

### 隔离

- 一个 acquire 的工作树不能被另一个 acquire 拿到,直到显式 return。
- dirty / in-use / leased / 不可验证 的工作树不应该被"偷偷"复用。
- guest 命令(`enter <name>`)可"看",但**不**改归属、**不**改 lifecycle state。

### 复用

- acquire 要快到"agent 几乎察觉不到",靠保留 `node_modules`、构建缓存、`.venv`、预编译产物。
- 不是"每次新建";是"reset 到 default branch HEAD,然后还回去时不清依赖缓存"。

### Lease(进程无关的长期持有)

- agent 持有 worktree 跑一段时间后,后台 daemon 想接管——不能要求 agent 一直活。
- durable lease 解决"无进程在工作树里也能保持占用"——见 [[concepts/worktree-durable-lease]]。
- 配合 ABA 防护(`--if-lease-id`)防止同类自动化在 lease 重建时误释放老 lease。

### 安全

- 破坏性操作默认 dry-run;真正删除需显式 `--yes` + 风险类别 opt-in——见 [[concepts/safe-destroy-by-default]]。
- state file 原子写 + corrupt 自愈——见 [[concepts/atomic-state-recovery]],即便一次崩溃也不该让所有 agent 失去工作树。
- 一个 agent 半路写坏 working tree,被 reset 时应当**提示**残留变更,而不是"我帮你删了"。

### 无 daemon / 可组合

- AI agent 调度框架(临时切换 Claude 模型、临时关掉一切)不需要依赖一个长跑 daemon 才能用。
- 与 `git`、`bash`、shell 工具天然组合——和 multiplexer(tmux / zellij / screen)不冲突,不取代它们。

## 常见反模式

| 反模式 | 后果 |
|---|---|
| 用 `git clone` per agent session | 每个 agent 首次 acquire 等十分钟;没有复用 |
| 让 N 个 agent 共享同一个 worktree | 文件编辑 racer;git index 互相污染;cherry-pick/rebase 永远失败 |
| 用脚本 `git worktree add` + 文件标记 owner | owner 字段没用、跨进程死锁、状态不原子 |
| 用 git branch 占位做隔离 | 分支名冲突多;`status` 难以反映真实 agent 占用;destroy 容易误删 |
| 让 agent 直接改 `~/.config` 等用户态 | 跨项目污染;agent 沙箱失败时无法 revert |
| 让 daemon 持有全局锁 | daemon 崩了等于全面不可用 |

## Agent OS 与 treehouse 的关系

- treehouse 不是 agent OS,只是它生命周期里的 **worktree 层 primitive**。
- 真正的 agent OS 还要管:prompt queue、tool 权限、人在循环 (HITL)、memory 跨 session 持久化、跨多个 repo 协调。
- 但是,**agent 要写出可见变更**,总得有地方写 —— treehouse 给的就是"安全、并发、缓存友好"的写入位置。

详见 [[concepts/agent-operating-system]]。

## 工具对比

| 工具 | 模型 | 取舍 |
|---|---|---|
| `git worktree`(原生)| 静态,1-2 个时好用 | 多了心智负担,不池化 |
| treehouse | 池 + lease + 状态原子 + safe destroy | 适合多 AI 并行、长期 agent、Cron worker |
| `git-worktree-mcp` 类 MCP server | 把 worktree 暴露给 agent(很多 LLM) | 适合在 agent 内部调用;**常常拿 treehouse 当后端**更稳 |
| 自建 bash 脚本 | 灵活 | 容易忘记 lock、原子写、平台分支;recovery 写得粗糙 |

## 相关

- [[entities/treehouse]] —— 实现
- [[concepts/git-worktree-pool-pattern]]
- [[concepts/worktree-durable-lease]]
- [[concepts/atomic-state-recovery]]
- [[concepts/safe-destroy-by-default]]
- [[concepts/agent-operating-system]] —— 上层
- [[concepts/ai-agent]] —— 更大的 AI agent 生态
