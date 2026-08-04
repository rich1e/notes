---
title: 原子化状态文件与 corrupt state 自愈
category: concepts
tags:
  - file-io
  - durability
  - crash-recovery
  - treehouse
  - state-management
sources:
  - https://github.com/kunchenguid/treehouse
  - _raw/_archived/github-kunchenguid-treehouse.txt (gitingest export, kunchenguid/treehouse, 2026-08-03)
created: 2026-08-03T11:30:00Z
updated: 2026-08-03T11:30:00Z
summary: 用 temp + fsync + rename 三段式保证状态文件 crash-safe;解析失败时不硬错,而是扫描池目录里仍在的 worktree 重建条目,全部默认 leased,等用户显式确认,绝不冒险"释放未知的占用"。
tier: supporting
lifecycle: draft
lifecycle_changed: 2026-08-03
base_confidence: 0.83
provenance:
  extracted: 0.95
  inferred: 0.05
  ambiguous: 0
relationships:
  - target: "[[entities/treehouse]]"
    type: derived_from
  - target: "[[concepts/git-worktree-pool-pattern]]"
    type: extends
  - target: "[[concepts/worktree-durable-lease]]"
    type: related_to
---

# 原子化状态文件与 corrupt state 自愈

> treehouse v2.0.1 引入:池的 state file 永远 crash-safe;一旦解析失败,**不**硬失败,**不**默默返回空 state —— 而是保守自愈。

## 写:crash-safe 三段式

```text
  1.  create <poolDir>/treehouse-state.json.tmp
  2.  tmp.Write(data)
  3.  tmp.Sync()        // fsync 内容到磁盘
  4.  tmp.Close()
  5.  os.Rename(tmp, target)  // POSIX atomic / Windows MoveFileEx(MOVEFILE_REPLACE_EXISTING)
  6.  parent.Sync()     // 父目录 fsync(在支持平台,如 Linux)
```

源码:`internal/pool/state.go::atomicWriteFile`。

核心保证:

- `rename(2)` 在 POSIX 上是原子的 —— 中段崩溃要么看到完整旧文件,要么看到完整新文件,绝不看到空/半截。
- Windows 用 `MoveFileEx(MOVEFILE_REPLACE_EXISTING)`,效果等价。
- 父目录 fsync 让 rename 在崩溃后也持久化(避免 page cache 没刷盘,重启后文件"消失")。

写出还有 `defer` 兜底:如果中途任意步骤失败,defer 会删 `.tmp`,不留垃圾文件。

## 锁:读 / 写全程串行化

- 锁文件:`<poolDir>/treehouse-state.lock`。
- POSIX:Go 用 `syscall.Flock`(`LOCK_EX` / `LOCK_UN`),放在 `//go:build !windows` 文件里。
- Windows:`LockFileEx` / `UnlockFileEx`(`lock_windows.go`)。
- 所有读、写 state 的入口都 `WithStateLock` 包起来 —— 命令之间不会撕裂。

## 读:corrupt ≠ 硬错

```go
func ReadState(poolDir string) (State, error) {
  data, err := os.ReadFile(stateFilePath(poolDir))
  if err != nil {
    if os.IsNotExist(err) {
      return State{}, nil  // 全新空池
    }
    return State{}, err    // 真的 IO 错误
  }
  var s State
  if err := json.Unmarshal(data, &s); err != nil {
    return recoverCorruptState(poolDir, err)  // ← 关键分支
  }
  return s, nil
}
```

**关键认知**:state 文件存在但 JSON 解析失败 = 几乎都是"上一次写中崩了留下截断"。如果硬报 `parse error`,每个命令都得跪,而且**用户**需要手工修。treehouse 选择:**乐观自愈**,并显式警告。

### recoverCorruptState 的保守原则

```text
- 扫 pool 目录里的所有子目录
- 对每个含有 .git 的"slot/worktree"目录,重建一个 WorktreeEntry
- 不知道是 idle spare、in-use,还是持久 lease
- 默认:全部标记 leased
- LeaseHolder = "recovered: state file was corrupt or truncated; verify before reuse"
- 打印大声警告到 stderr
- 返回 State{Worktrees: recovered}
```

为什么默认标记 **leased** 而不是 **idle**:

- idle → 立即被下次 `get` 拿走 → 可能覆盖一个无人值守租约的真占用者的状态。
- leased → `Acquire` 与 `prune` 跳过,`destroy` 必须显式 `--include-leased` 单路径才删 → **多一步人工兜底**,符合 VISION.md 的 "Under uncertainty, leave the worktree in place with an actionable explanation, and verify the safety facts again at deletion time"。

### 用户处置流程

```sh
$ treehouse status    # 看看哪些 entry 显示 leased,带 "recovered: ..." 占位
🌳 Path: ~/.treehouse/.../1/worktree  Status: leased (recovered: state file was corrupt ...)

$ treehouse return <path>     # 确认是 idle 后,清掉这条假 lease
# 或
$ treehouse destroy <path> --include-leased --yes   # 不想要,显式销毁
```

`Acquire` 永远不会把 recovered entry 发出去,直到用户显式 return / destroy。

## 与 lease 的关系

- **正常路径**:LeaseID + LeaseHolder 标明租用方 → `return <path>` 精确归还。
- **恢复路径**:LeaseHolder = "recovered: ..." 占位 → `return <path>` 用占位语义清掉,**不会**触发 `--if-lease-id` 的 ABA 检查(因为 LeaseID 是空的);`status` 输出让用户能看出来"这些不是真 lease"。

## 这个模式可以复用到哪

任何"小型本地配置 state 文件 + 不能丢数据 + 偶尔会写中崩"的场景,都用得上:

- 浏览器 cookie / session store 持久层(显然需要类似保护)。
- key/value 索引(ripgrep 自身的 metadata、sqlite WAL)。
- 多写者模型下用同样的 lock + rename,顺序很重要。

核心口诀:**不假设写成功、不假设读是真值、写前持锁、失败保守、让用户兜底**。

## 相关

- 池机制总览:[[concepts/git-worktree-pool-pattern]]
- Lease 字段与 ABA 安全:[[concepts/worktree-durable-lease]]
- 删除相关的安全默认:[[concepts/safe-destroy-by-default]]
- 实现:[[entities/treehouse]]
