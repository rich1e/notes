---
title: treehouse CLI 日常用法
category: skills
tags:
  - cli
  - worktree
  - treehouse
  - ai-agent
  - parallel-workflow
sources:
  - https://github.com/kunchenguid/treehouse
  - _raw/_archived/github-kunchenguid-treehouse.txt (gitingest export, kunchenguid/treehouse, 2026-08-03)
created: 2026-08-03T11:45:00Z
updated: 2026-08-03T11:45:00Z
summary: treehouse 命令速查:install / get / enter / status / return / prune / destroy 的常见用法、关键 flag、ABA-safe 条件 return、与 GitHub Actions release 渠道。
tier: peripheral
lifecycle: reviewed
lifecycle_reason: "auto-promoted by wiki-lint --consolidate: age>30d, confidence>0.9"
lifecycle_changed: 2026-08-03
base_confidence: 0.9
provenance:
  extracted: 0.95
  inferred: 0.05
  ambiguous: 0
relationships:
  - target: "[[entities/treehouse]]"
    type: derived_from
  - target: "[[concepts/git-worktree-pool-pattern]]"
    type: related_to
  - target: "[[concepts/worktree-durable-lease]]"
    type: related_to
  - target: "[[concepts/safe-destroy-by-default]]"
    type: related_to
  - target: "[[concepts/atomic-state-recovery]]"
    type: related_to
  - target: "[[skills/openlore-cli]]"
    type: related_to
---

# treehouse CLI 日常用法

> 单 page cheat-sheet,涵盖安装、acquire / return / prune / destroy / lease 操作模式,以及出错时的恢复路径。底层概念见相关 concept 页。

## 安装

| OS | 命令 |
|---|---|
| macOS / Linux | `curl -fsSL https://kunchenguid.github.io/treehouse/install.sh \| sh` |
| Windows (PowerShell) | `irm https://kunchenguid.github.io/treehouse/install.ps1 \| iex` |
| Nix | `nix run github:kunchenguid/treehouse` |
| Go | `go install github.com/kunchenguid/treehouse@latest` |
| 从源码 | `git clone` + `make install` |

> 部分场景会因安装脚本拿不到 PATH 写错位置 → 用 `go install`(写到 `$HOME/go/bin`)或源码 `make install` 兜底。`make` 目标:`build` / `test` / `lint` / `dist` / `install` / `clean`。

## 起点:init + Config(可选)

```sh
cd myrepo
treehouse init          # 在仓库根写一份示例 treehouse.toml
```

`treehouse.toml` 字段(`internal/config/config.go`):

```toml
max_trees = 16
# root = "$HOME/worktrees"     # 相对路径=相对仓库根;绝对路径用于全局 prune
```

用户级 `~/.config/treehouse/config.toml` 还能放 `[hooks]`(`post_create` / `pre_destroy`)。**Repo 级 config 忽略 hook**(安全:不让仓库控制代码自动跑)。

## 核心命令

### `treehouse`(无参数)

等价于 `treehouse get` —— acquire 一个工作树并 spawn subshell,`exit` 时自动 reset + return。

### `treehouse get` —— acquire

```sh
# 交互:进 subshell
treehouse get

# 非交互 + 持久 lease(只输出路径到 stdout)
path=$(treehouse get --lease)

# 带 holder 标签
path=$(treehouse get --lease --lease-holder "ci-runner-42")

# JSON 输出(retry-safe 自动化)
treehouse get --lease --lease-holder "ci-runner-42" --json
# {"path":"...","lease_id":"...","lease_holder":"ci-runner-42","leased_at":"..."}
```

要点:

- `--json` 必须配合 `--lease`,否则报错。
- 全程 stderr 是 human 文本,stdout 只有路径/JSON → `$(treehouse get --lease)` 干净。

### `treehouse enter <name>`

打开或进入**已存在的**某个工作树(从 `status` 看编号)。即便 in-use 也可 attach;**不**改归属,**不**改 state。

```sh
treehouse status                         # 看到 "3" 是一个空闲的
cd "$(treehouse enter --print-path 3)"   # 或打开 subshell
```

### `treehouse return [path]` —— 释放

```sh
# 当前 worktree(必须在 worktree 目录或带子路径)
treehouse return

# 显式路径(可在仓库外)
treehouse return /abs/path/to/worktree

# 无条件快速(脏变更也清)
treehouse return --force

# ABA 安全的条件 return
treehouse return --force \
  --if-lease-id "$lease_id" \
  --if-lease-holder "$lease_holder" \
  "$path"
```

行为:清理残留进程、reset working tree、清 lease、回到 idle 池。

### `treehouse status`

```sh
treehouse status
treehouse status --json    # 数组,字段含 name/path/status/lease_id/lease_holder/leased_at/processes
```

> 非 leased 工作树的 lease 字段是空串 + `null` 时间戳;旧版本 state 文件 JSON 里没这些字段也会被正常读出。

### `treehouse prune`

```sh
# dry-run,只列出当前 repo 池里 "可删" 的
treehouse prune

# 真删
treehouse prune --yes

# 全用户级 root 下所有托管 pool
treehouse prune --all --yes
# alias
treehouse prune --global --yes

# 把 backing repo 缺失的孤儿也列入(每个候选标 "content could not be verified")
treehouse prune --prune-orphans --yes

# 详细 skip 原因
treehouse prune -v
```

跳过类别:已被引用(in-use / leased / reserve)、脏、未合入 default branch、不可达 origin 的全部跳过。

### `treehouse destroy`(v2.0.0 起)

```sh
# 单个
treehouse destroy <worktree-path>
treehouse destroy <worktree-path> --yes

# 整个 pool(--all 不带 pool 路径 = 报错)
treehouse destroy . --all --yes          # 仓库根 . 也算 pool
treehouse destroy /path/to/pool --all --yes

# 风险分桶 opt-in(各取所需,绝不"全选")
treehouse destroy <path> --yes --include-unlanded       # 脏 / 未合 / 不可验证
treehouse destroy <path> --yes --include-in-use         # 有进程(先优雅终止)
treehouse destroy <path> --yes --include-leased         # 单路径租约

# ❌ 不允许
treehouse destroy --all --include-leased   # 命令直接拒绝
```

退出码:单目标被 skip → 非零;批量 skip → 零;靠 summary 看清实际动了什么。

## 长期 agent / 无人值守模式(`get --lease`)

```sh
# 拿一个长期持有的 worktree 给一个长跑的 agent runner
path=$(treehouse get --lease --lease-holder "opencode-runner")

# runner 用 $path 工作,后台跑很久
opencode --workdir "$path" &

# 自动化想做"我手里的 lease 才能 return",加 --if-lease-id
treehouse return --force --if-lease-id "$lease_id" --if-lease-holder "opencode-runner" "$path"
```

详见 [[concepts/worktree-durable-lease]]。

## 出了问题怎么办

### State corrupt

```sh
$ treehouse status
treehouse: WARNING: state file ~/.treehouse/.../treehouse-state.json is corrupt or truncated (...); recovering from worktrees found on disk ...

# 看到很多 leased 且 LeaseHolder = "recovered: ..."
$ treehouse status --json
# 逐个核查:

$ treehouse return /abs/path   # 确认是 idle,清掉假 lease
# 或
$ treehouse destroy /abs/path --include-leased --yes   # 不要它,显式销毁
```

详见 [[concepts/atomic-state-recovery]]。

### worktree 进程死不掉

退出 subshell 时 treehouse 会扫 inside-cwd 进程并优雅终止。某些进程(opencode server,deamon 化)会忽略 SIGHUP——treehouse 用 `process.TerminateWorktreeProcesses(wtPath, 2*time.Second)` 兜底,详情看 `internal/process/terminate*.go`。

### Prune 把"还能用"的也列在 dry-run 里?

`treehouse prune -v` 看每条的 skip 原因。常见:

- `uncommitted tracked changes` —— dirty,被跳过。
- `untracked files even when status is hidden` —— treehouse 用更严格的 dirty check(忽略 `status.showUntrackedFiles`)。
- `HEAD commit is not merged into the default branch` —— 未合,跳过。
- `origin unreachable (cannot verify)` —— origin 不通,即便是脏也跳过(避免远程孤儿被当本地孤儿删)。

### `destroy` 删不动

按 summary 的标签加 `--include-*`,然后 `--yes` 即可。**别想**用旧 `--force` —— 已经被移除。

## CI / Release

- release 流程走 `release-please` + `release.yml`,tags 触发 goreleaser。
- 升级: `treehouse update`(从 GitHub release 取新版替身)。
- 关掉 update check: `TREEHOUSE_NO_UPDATE_CHECK=1`。

## 配置 default branch 冲突

worktree 总是 detached HEAD,reset 到"local 或 origin default branch 中**更前进**的"那条。直接用 main 就行;自定义 default branch 时只要 git 自身认就行。

## 跨平台提示

- **路径分隔符**:`filepath.Join`、`filepath.ToSlash` —— 不要硬编码 `/`。
- **shell**:Windows 上不要假设 `/bin/sh`,代码走 `internal/shell/shell.go` 抽象。
- **flock**:`internal/pool/lock_unix.go` / `lock_windows.go` 用 build tag 切。

## 相关

- [[entities/treehouse]] —— 实现总览
- [[concepts/git-worktree-pool-pattern]]
- [[concepts/worktree-durable-lease]]
- [[concepts/atomic-state-recovery]]
- [[concepts/safe-destroy-by-default]]
- [[skills/openlore-cli]] —— 同为 AI agent 本地基础设施 CLI 速查;treehouse 管"在哪写"（worktree 池），OpenLore 管"该写哪里"（静态分析 orient）
