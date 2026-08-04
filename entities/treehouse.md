---
title: treehouse — AI agent 并行 worktree 池 CLI
category: entities
tags:
  - cli
  - git
  - worktree
  - ai-agent
  - pool-manager
  - treehouse
sources:
  - https://github.com/kunchenguid/treehouse
  - _raw/_archived/github-kunchenguid-treehouse.txt (gitingest export, kunchenguid/treehouse, commit 939cb59b, 2026-08-03)
created: 2026-08-03T11:15:00Z
updated: 2026-08-03T11:15:00Z
summary: Go 编写的 git worktree 池管理 CLI,为并行 AI 编码 agent 提供可重用、预热的隔离工作树,无守护进程,支持 durable lease、原子 state 自愈、safe-by-default destroy。
tier: supporting
lifecycle: draft
lifecycle_changed: 2026-08-03
base_confidence: 0.85
provenance:
  extracted: 0.95
  inferred: 0.05
  ambiguous: 0
relationships:
  - target: "[[concepts/git-worktree-pool-pattern]]"
    type: related_to
  - target: "[[concepts/worktree-durable-lease]]"
    type: related_to
  - target: "[[concepts/safe-destroy-by-default]]"
    type: related_to
  - target: "[[concepts/atomic-state-recovery]]"
    type: related_to
  - target: "[[concepts/ai-agent-sandbox]]"
    type: related_to
  - target: "[[concepts/agent-operating-system]]"
    type: related_to
---

# treehouse — AI agent 并行 worktree 池 CLI

**treehouse** 是 [kunchenguid](https://github.com/kunchenguid) 开发的 Go CLI,用于管理 **git worktree 池**:让多个并行任务(包括 AI agent)各自获得一个已就绪、可重用、独立的 worktree,而不必为每个新任务重新 `git clone` 或等待依赖/构建缓存重建。

## 它解决的问题

> Are you starting a new worktree for every agent session, losing all your installed dependencies and build cache each time, and wondering why your agents are slow?

- 每个 agent session 全新 worktree → 每次重装 `node_modules` / 重建 SwiftPM 缓存。
- 多个 agent 共享一个 worktree → 文件编辑互相冲撞,无法并发。
- 手工管理 worktree 路径 → 心智负担 + 协作冲突。

treehouse 把 worktree 池化:**acquire → 用 → return**,worktree 自动 reset 到 default branch HEAD、保留依赖与构建缓存、下一个 agent 拿到即可立刻动手。

## 基本事实

| 项 | 值 |
|---|---|
| 版本 | v2.1.1(2026-07-31,commit `939cb59b`) |
| 语言 | Go(cobra CLI + 标准库为主) |
| 平台 | macOS / Linux / Windows |
| 许可证 | MIT |
| 安装 | `curl …install.sh \| sh`、`go install`、`nix run github:kunchenguid/treehouse` |
| 池目录默认 | `~/.treehouse/<repo-hash>/<slot>/<worktree>` |
| 状态文件 | `<poolDir>/treehouse-state.json`,原子写入 |
| 锁定文件 | `<poolDir>/treehouse-state.lock`(flock,平台分支) |
| 核心命令 | `get` / `enter` / `return` / `status` / `prune` / `destroy` / `init` / `update` |
| Git 实现 | shell out 到 `git`(因 go-git 对 worktree 支持不完整) |

## 一次典型的"acquire → 用 → return"

```sh
$ cd myproject
$ treehouse                 # 等价于 treehouse get
🌳 Entered worktree at ~/.treehouse/myproject-a1b2c3/1/myproject. Type 'exit' to return.

# 在这个 worktree 里跑 agent / 跑测试 / 改代码 —— 全是隔离的
$ claude 'implement feature X'   # 或 opencode、shell 脚本…都行
$ exit                           # 退出 subshell
🌳 Terminated lingering processes: opencode (pid 12345)
🌳 Worktree returned to pool.
```

## 核心机制

- **Detached HEAD 工作树** —— 用 `git worktree add --detach`,避免分支名与多个并行任务互相冲突;acquire 时 reset 到 local/origin default branch 中"更前进"的那个分支(优先 origin,矛盾时倾向 origin,见 AGENTS.md)。
- **无守护进程** —— 所有操作都是内联 CLI 命令,池状态保存在磁盘上、由每个命令持锁写入。
- **In-use 检测** —— 扫描运行中进程的 cwd 落在 worktree 内;另外配合短期 persisted owner reservation(`OwnerPID`/`OwnerStartedAt`)识别 `get`/`destroy`/`prune` 自身生命周期产生的短期锁。
- **Durable lease(`get --lease`)** —— 不开 subshell,直接持久化地"租"一个 worktree,**无需任何进程在里头**;后续 `get` 不会发它,`prune` 也不会删它,直到 `treehouse return <path>` 显式释放。
- **状态原子写** —— `temp file → fsync → rename`,崩溃中段绝不会留下截断/空文件(详见 [[concepts/atomic-state-recovery]])。
- **State 自愈** —— 文件存在但解析失败时,扫描池目录里仍在的 worktree 子目录重建条目,全部标记 `leased`(`LeaseHolder = "recovered: state file was corrupt or truncated"`),`Acquire`/`prune` 跳过这些条目,`destroy` 必须显式 `--include-leased` 单路径才能删除 —— 防止在不知道真实用途时误删。
- **安全清理** —— `prune` 默认 dry-run,只删 idle + clean + HEAD 已合入 default branch 的;`prune --prune-orphans --yes` 才能处理 backing repo 缺失的孤儿;`prune --all`/`--global` 跨池扫描但仍读用户级 config。
- **Safe-by-default destroy(v2.0.0 重大变更)** —— 完全删除了 `--force`(曾同时覆盖全部安全检查);改为三类独立 opt-in:`--include-unlanded`(脏/未合/不可验证)、`--include-in-use`(运行进程/owner reservation,先优雅终止)、`--include-leased`(单路径,绝不允许 `--all`)。`destroy <pool> --all` 没有跨池/全局作用域,`--all` 不带 pool 路径即报错(见 [[concepts/safe-destroy-by-default]])。

## Config 与 Hook

- **Repo 级** `treehouse.toml`(在仓库根):只放 repo-safe 设置(`max_trees`、可选 `root`)。
- **用户级** `~/.config/treehouse/config.toml`:还允许 `[hooks]` —— `post_create`(拿到 worktree 后跑,如 `./scripts/setup-venv.sh`)、`pre_destroy`(删除前跑,如清理缓存)。Repo 级 config **不读** hooks,以防仓库控制代码自动执行。

## 演进

| 版本 | 日期 | 关键变化 |
|---|---|---|
| 1.0.0 | 2026-03-14 | 初始发布 |
| 1.3.x | 2026-04 | Nix flake、subshell 进程安全清理、detach before reuse |
| 1.5.0 | 2026-06-19 | `prune`(安全陈旧 worktree 清理) |
| 1.6.0 | 2026-06-20 | `prune --all` 全局模式 |
| 1.7.0 | 2026-06-20 | 孤儿工作树分类 |
| 1.8.0 | 2026-06-22 | **durable worktree leases**(非进程型持久预留) |
| 2.0.0 | 2026-06-24 | **breaking**:`destroy --force` 删除,替换为三类 `--include-*` opt-in |
| 2.0.1 | 2026-07-14 | state 持久化原子化与可恢复化 |
| 2.1.0 | 2026-07-20 | stable lease identities(128-bit random `lease_id`、`--if-lease-id` 条件 return) |
| 2.1.1 | 2026-07-31 | CI 抑制 release-please PR 上的 `pull_request` 触发 |

## 设计态度(摘自 `VISION.md`)

- **职责单一** —— 拥有 worktree lifecycle,不做 agent 编排,不做开发工作流。
- **隔离 ≠ 安全沙箱** —— 隔离工作目录和生命周期归属,不隔离外部攻击面。
- **不确定时,不删** —— 操作前查 git / 进程 / lifecycle 状态,不可验证时保留并解释;删除前再验一次。
- **破坏性操作默认 dry-run**,每个风险类别各自独立 opt-in;拒绝 blanket force、跨池 wildcard、global delete-everything。
- **恢复先于复用** —— state 崩溃时把条目标 `leased` 而不是清空,等用户显式确认。

## 替代 / 对比

- `git worktree` 原生命令 —— 适合 1–2 个并发,多了心智负担;无池、自动 reset、lease 机制。
- `git-worktree-mcp` 等 MCP server —— 把 worktree 暴露给 AI agent;和 treehouse 不冲突,但缺少池、原子 state、跨平台 CLI。
- 自建脚本 —— 容易踩状态原子写、flock、跨平台 syscall 这些坑。

## 引用

- 仓库: <https://github.com/kunchenguid/treehouse>
- 原始抓取: `_raw/_archived/github-kunchenguid-treehouse.txt`
- AGENTS.md(项目内 agent 指南)
- VISION.md(项目愿景)
