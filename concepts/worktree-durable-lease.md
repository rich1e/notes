---
title: Worktree durable lease — 进程无关的持久租约
category: concepts
tags:
  - worktree
  - lease
  - concurrency
  - ai-agent
  - treehouse
sources:
  - https://github.com/kunchenguid/treehouse
  - _raw/_archived/github-kunchenguid-treehouse.txt (gitingest export, kunchenguid/treehouse, 2026-08-03)
created: 2026-08-03T11:25:00Z
updated: 2026-08-03T11:25:00Z
summary: 把 worktree 占用与"进程是否在里头运行"解耦的持久租约:LeaseID(128-bit 随机)、LeaseHolder(标签)、LeasedAt 时间戳三件套,持锁原子写;带 ABA 防护的 conditional return(--if-lease-id)。
tier: supporting
lifecycle: reviewed
lifecycle_reason: "auto-promoted by wiki-lint --consolidate: age>30d, confidence>0.82"
lifecycle_changed: 2026-08-03
base_confidence: 0.82
provenance:
  extracted: 0.95
  inferred: 0.05
  ambiguous: 0
relationships:
  - target: "[[entities/treehouse]]"
    type: derived_from
  - target: "[[concepts/git-worktree-pool-pattern]]"
    type: extends
  - target: "[[concepts/atomic-state-recovery]]"
    type: related_to
  - target: "[[concepts/safe-destroy-by-default]]"
    type: related_to
---

# Worktree durable lease

> treehouse v1.8.0 引入、v2.1.0 加 identity,把 worktree"占用"从"进程是否还活着"中独立出来,并支持 ABA 安全的条件归还。

## 为什么需要 durable lease

普通 `treehouse get` 模式:开 subshell,subshell 退出 = 自动 return。对自动化调用(持续运行的 agent runner、CI worker、长期 daemon 反向调用 AI)不友好 —— 想要一个 worktree **常驻**,没有进程住在里头也能维持占用,直接用 subshell 模式会有两类问题:

1. 进程被外部 kill / 崩溃,worktree 跟着释放,下次拿到就被 reset,丢失缓存与未提交状态。
2. 进程本就不该存在(无人值守、容器内多租户分配)。

durable lease(`get --lease`)解决:不 spawn subshell,只在 state 文件里持久化一条 lease,直到显式 `return` 才释放。

## 三件套字段

```go
type WorktreeEntry struct {
  // ...
  Leased      bool      `json:"leased,omitempty"`         // 简化的"被租走"位
  LeaseID     string    `json:"lease_id,omitempty"`        // 128-bit 随机身份(16-byte hex)
  LeaseHolder string    `json:"lease_holder,omitempty"`    // 持有者标签(可选)
  LeasedAt    time.Time `json:"leased_at,omitempty,omitzero"`
}
```

- **`LeaseID`** 每次 acquire 重新生成,16 字节 crypto-rand → 32 字符 hex。
- **`LeaseHolder`** 默认从环境变量 `TREEHOUSE_LEASE_HOLDER` 读,可用 `--lease-holder` 覆盖。
- 旧版本 state 文件没这些字段也能读,LeaseID 为空时降级为"旧式无条件 return"语义。

## acquire 流程(简化)

```go
func getLeaseRunE(...) error {
  holder := getLeaseHolder
  if holder == "" { holder = os.Getenv("TREEHOUSE_LEASE_HOLDER") }
  lease, err := pool.AcquireLeaseInfo(repoRoot, poolDir, cfg.MaxTrees, cfg.Hooks.PostCreate, holder)
  if err != nil { return err }
  fmt.Fprintf(stderr, "🌳 Leased worktree at %s ...\n", ui.PrettyPath(lease.Path))
  if getJSON { return json.NewEncoder(stdout).Encode(lease) }
  fmt.Fprintln(stdout, lease.Path) // 唯一 stdout 输出
  return nil
}
```

要点:

- 路径(或 JSON)是 stdout **唯一**内容,所有 human 文本走 stderr —— 避免污染下游命令的 `$(...)` 捕获。
- 全程持 `treehouse-state.lock`。

## ABA 防护:条件归还

```sh
treehouse return --force \
  --if-lease-id "$lease_id" \
  --if-lease-holder "$lease_holder" \
  "$path"
```

逻辑:`pool.ReleaseConditional` 先在持锁状态下比对 supplied `lease_id` 与当前 state:

- 不匹配 → exit nonzero,**不**做任何 reset / 终止进程 / state 清理。
- 匹配 → 同把锁从头串到 reset + clear 防重入,身份在一次归还中匹配,不可能误释放后续重新 acquire 的同路径。

`--if-lease-holder` 是可选(便于自动化复用 holder),`--if-lease-id` 是 ABA 保护 —— 即便同 holder 名被新 acquire 复用,id 变了就拒绝归还。

向后兼容:`return <path>` 不带条件保持"原版只比路径"行为,旧脚本不变。

## 与 Owner / DestroyReservation 的关系

- **Owner**(`OwnerPID` + `OwnerStartedAt`)是 subshell 模式的活进程凭证,subshell 退出 = 自然 return。
- **Destroy reservation**(`Destroying` 字段)是 `destroy` / `prune` 自身生命周期内的短期互斥。
- **Leased** 字段是独立的"持久租约"位 —— **不能由前两者推断出来**,反之亦然。
- v2.1.0 `healState` 也只清 owner 类,永不清 lease —— 这是 VISION.md "A live process, a short lifecycle reservation, and a durable lease represent different facts and should not be inferred from one another" 的字面落实。

## 用法

```sh
# 拿一个持久的 worktree 路径给脚本/agent 用
path=$(treehouse get --lease)

# 加 holder 标签
path=$(treehouse get --lease --lease-holder "worker-A")

# 拿 JSON 用于 retry 安全的脚本
treehouse get --lease --lease-holder automation-A --json
# {"path":"...","lease_id":"...","lease_holder":"automation-A","leased_at":"..."}
```

`treehouse status --json` 暴露同样的字段,所有工作树的 lease 元数据集中可查。

## 状态机

```text
                  +-- subshell alive --> OwnerPID set
   idle ──get──►  |
                  +-- --lease -->   Leased=true, LeaseID=NEW_RAND
                  ...
                  +-- subshell exit --> return to idle, OwnerPID cleared
                  +--  return -->  release lease, LeaseID cleared
                  +--destroy (not --all) + --include-leased ──> 被销毁
```

lease 的关键不变量:**没有任何进程运行的 worktree 仍可处于 leased;lease 与进程存在性无关**。

## 失败的反模式(从 README 与 VISION.md 推出)

- ❌ 用 PID 字段 + heartbeat 模拟 lease —— 心跳窗口竞态依然能丢锁。
- ❌ 用 git branch 占位做隔离 —— 多并发、状态检查、机器读出都难。
- ❌ lease 随进程退出自动失效 —— 失去"长期无人值守持有"语义。
- ❌ 不持锁读 lease 字段 —— 两个 `return` 可能同时通过判断。

## 相关

- 池架构基础:[[concepts/git-worktree-pool-pattern]]
- state 原子写 + corrupt 自愈:[[concepts/atomic-state-recovery]]
- 安全删除(含 leased 处理):[[concepts/safe-destroy-by-default]]
- 实现:[[entities/treehouse]]

## Related

- [[synthesis/concepts-agent-operating-system × concepts-worktree-durable-lease]]
