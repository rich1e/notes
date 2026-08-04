---
title: git worktree 池模式 — 可重用、预热的并行工作树
category: concepts
tags:
  - git
  - worktree
  - ai-agent
  - pool-manager
  - treehouse
sources:
  - https://github.com/kunchenguid/treehouse
  - _raw/_archived/github-kunchenguid-treehouse.txt (gitingest export, kunchenguid/treehouse, 2026-08-03)
created: 2026-08-03T11:20:00Z
updated: 2026-08-03T11:20:00Z
summary: 把 git worktree 池化为可重用资源:acquire 拿到一个已就绪的、保留依赖/缓存、互相不冲突的工作树,用完 return,reset 到 default branch HEAD 供下次 acquire。
tier: supporting
lifecycle: draft
lifecycle_changed: 2026-08-03
base_confidence: 0.85
provenance:
  extracted: 0.92
  inferred: 0.08
  ambiguous: 0
relationships:
  - target: "[[entities/treehouse]]"
    type: derived_from
  - target: "[[concepts/ai-agent-sandbox]]"
    type: related_to
  - target: "[[concepts/agent-operating-system]]"
    type: related_to
  - target: "[[concepts/worktree-durable-lease]]"
    type: extends
  - target: "[[concepts/safe-destroy-by-default]]"
    type: related_to
---

# git worktree 池模式

> 为并行任务(包括 AI agent)提供 **"acquire → 用 → return"** 的可重用 git 工作树。

## 一句话定义

把 `git worktree add` 的产物当 **池元素** 管理:`acquire` 拿一个闲置的 worktree,使用完毕 `return` 让它 reset 后回到池中,下一个 acquire 立即复用——保留依赖目录、构建缓存、可信 `.gitignore`。

## 与"每个任务一个 worktree"的区别

| 维度 | 朴素 worktree | worktree 池 |
|---|---|---|
| 创建成本 | 每次 `git worktree add` + 重装依赖/缓存 | 一次性预热,后续 acquire ~即时 |
| 并发隔离 | ✅ | ✅(detached HEAD + lock + 状态文件) |
| 依赖/缓存 | 每次重建 | 跨任务保留 |
| 退出 / 归还 | 手工 `git worktree remove` | 自动 reset + return |
| Lease(进程外) | 只能靠分支名占位 | `get --lease` + lock + status 显示 |
| 崩溃恢复 | 看 git 自身状态 | 原子 state + 自愈(扫描 on-disk 子目录重建) |

参考实现:[[entities/treehouse]]。

## 关键设计选择

### 1. Detached HEAD

- 不用分支名,避免多个并行任务创建同名分支互相冲突。
- acquire 时 reset 到 **local 或 origin default branch 中更靠前的那个**(detached),即"哪个有更新的 commit 就用哪个",origin 优先。
- readme 中明确:worktree 不是分支而是工作目录 + 独立 HEAD。

### 2. 无守护进程

- 所有生命周期动作都是内联 CLI(`get`/`return`/`status`/`prune`/`destroy`),不依赖后台进程。
- 池状态写在 `<poolDir>/treehouse-state.json`,由每个命令持 `treehouse-state.lock`(POSIX `flock` / Windows `LockFileEx`)原子写。
- 杀掉 shell 不影响池状态 —— reaper 模式天然适合无人值守/CI/agent。

### 3. Slot 命名

布局:`~/.treehouse/<repo-hash>/<slot-index>/<worktree-dir>`。

- repo-hash 由仓库 origin URL 计算(本地仓库用本地路径),让同一仓库在不同机器/不同 clone 的池能区分。
- slot-index 是池内编号,池满(`max_trees`)时无法 `add`,需先 `prune` 或 `destroy`。

### 4. 进程 / 持有者 / Lease 三种"占用"分开

这是重要的设计抉择 —— **不能从一个推出另一个**:

| 状态字段 | 含义 | 来去 |
|---|---|---|
| `OwnerPID` + `OwnerStartedAt` | `get`(subshell 模式)期间,subshell 进程的 PID + 启动时间戳 | subshell 退出 = 自然归还 |
| Destroy 临时 reservation | `destroy` / `prune` 自身生命周期内避免 race | 动作结束即清 |
| `Leased` + `LeaseID` + `LeaseHolder` + `LeasedAt` | **durable lease**——进程无关的持久预留 | 显式 `treehouse return` 才清 |

进程死了不会自动取消 lease(vs. owner 字段)。Lease 独立存活,直到 `return` 释放。

### 5. State 文件原子写

`temp + fsync + rename` 三段:

1. 写到 `<poolDir>/<name>.json.tmp`。
2. `Sync()`(fsync)+ `Close()`。
3. 平台替换原语(POSIX `rename(2)` / Windows `MoveFileEx(MOVEFILE_REPLACE_EXISTING)`)。
4. 父目录 `Sync()`(支持平台)。

崩溃中段留下完整旧文件或新文件,绝无中间状态。

### 6. State 自愈(recoverCorruptState)

解析失败(空/截断)不硬失败 —— 扫描池目录里仍在的 worktree 子目录,逐个重建条目,**全部标记 leased**(`LeaseHolder = "recovered: ..."`):

- 原因:磁盘上单凭目录看不出是 idle spare、in-use,还是真正的 lease —— 不能冒险随便发出去。
- `Acquire` 与 `prune` 跳过这些条目,`status` 显示让用户看见,`destroy` 必须显式 `--include-leased` 单路径才能删。
- 用户用 `treehouse status` 排查,`treehouse return <path>` 或 `destroy <path> --include-leased --yes` 显式清场。

## 失败的常见反模式

- ❌ 用分支名做隔离 —— N 个并行任务可能撞名。
- ❌ 用 PID 文件做长期 reservation —— 进程死/被 kill/重启都会让逻辑乱了。
- ❌ 把池状态以追加日志追加而不快照 —— `git pull --rebase` 后追加日志顺序会乱。
- ❌ 让 daemon 持有锁 —— 守护进程崩了等于全局不可用。
- ❌ `prune` / `destroy` 默认"全部删除" —— 哪怕 dry-run 的输出用户也没看,误删一次便万劫不复。

## 适用场景

- **AI 编码 agent**(Claude Code / Codex / opencode / Cursor CLI)并行跑多个会话时,每个会话需要独立隔离工作树。
- **CI 多任务并行** —— 同一仓库的多个 PR 构建。
- **本地多分支实验** —— 切换分支不丢依赖/缓存。
- **任何 "N 个并发任务共用一份依赖但互不串扰" 的场景**。

详见 [[concepts/ai-agent-sandbox]] 与 [[concepts/agent-operating-system]]。
