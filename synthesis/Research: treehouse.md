---
title: Research: treehouse — 把 git worktree 池化成 AI agent runtime
category: synthesis
tags:
  - synthesis
  - treehouse
  - ai-agent
  - worktree
  - cli-design
  - durable-state
sources:
  - https://github.com/kunchenguid/treehouse
  - _raw/_archived/github-kunchenguid-treehouse.txt (gitingest export, kunchenguid/treehouse, 2026-08-03)
created: 2026-08-03T11:50:00Z
updated: 2026-08-03T11:50:00Z
summary: 从 treehouse 的 12 个版本迭代看到一条清晰的演化主线:让 git worktree 池化 + 长期 lease + safe destroy + crash-safe state,每条线都先有"被现实撞出来的痛"再演进。可复用到任何"小型本地 runtime 状态"的工程上。
tier: core
lifecycle: draft
lifecycle_changed: 2026-08-03
base_confidence: 0.85
provenance:
  extracted: 0.92
  inferred: 0.08
  ambiguous: 0
relationships:
  - target: "[[entities/treehouse]]"
    type: related_to
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
---

# Research: treehouse — 把 git worktree 池化成 AI agent runtime

> 一次性整合 entities/treehouse 与全部 5 个相关 concept,提炼 **"为什么这套设计形成闭环"** 与 **"它解决的是哪类问题"**。

## 一句话总结

**treehouse** 不是又一个 `git worktree` 包装,而是把"工作树生命周期"做成了一个**小型本地 runtime**,在"acquire 快、并发安全、崩溃可恢复、删除保守、长期可持有"五点上不靠 daemon、不靠数据库,只用 Git + 几十 KB Go 代码 + 一个 JSON state file 把所有问题齐了。

## 五条独立但相互勾连的设计线

### 线 A:池化复用(`git-worktree-pool-pattern`)

- 1.0.0 起步 → detached HEAD、reset 到更前进的 default branch、保留 `node_modules` 等。
- 核心:**acquire → use → return**,状态完全在用户态,不依赖后台进程。

### 线 B:Dead agent 残留(`process/terminate*`)

- 1.3.1 fix:subshell 退出后,有些 agent(opencode server 等)忽略 SIGHUP 残留,重新 acquire 时撞进程。
- 解法:return 时扫 cwd 命中 worktree 的进程,用 `process.TerminateWorktreeProcesses(wtPath, 2*time.Second)` 兜底。
- 兜底逻辑放在 release 后才被发现 → 1.x 长期小版本维护的真实案例。

### 线 C:Lease 演化(`worktree-durable-lease`)

- 1.8.0:加 `Leased` / `LeaseHolder` / `LeasedAt`,**进程无关**的持久预留。
- 2.1.0:再加 `LeaseID`(128-bit 随机)+ `--if-lease-id` 条件 return,ABA 安全。
- 每一步都对应**新一类调用方**:CI runner、长期 agent daemon、`get --json` 自动化。
- 核心推论:**live process / short reservation / durable lease 是三种独立事实,绝不能互相推断**(VISION.md 原文)。

### 线 D:破坏性操作慢慢收紧(`safe-destroy-by-default`)

- 1.5.0:`prune`(dry-run by default)。
- 1.6.0:`prune --all` 全局扫描。
- 1.7.0:孤儿分类。
- 2.0.0:**breaking** —— 拆掉 `--force`,改成三类独立 opt-in(`--include-unlanded` / `--include-in-use` / `--include-leased`) + 必须 `--yes` 才执行。
- 2.0.1:state 原子化、可恢复化。
- 这条线最值得借鉴:**用 breaking change 把"过去的安全错误"修干净**——同时提供清晰的迁移表(README 旧→新)。

### 线 E:Crash-safe + 自愈(`atomic-state-recovery`)

- v2.0.1 关键 commit:`make state persistence atomic and recoverable`(#55)。
- 写入:`temp + fsync + rename + parent fsync`。
- 读取:`json.Unmarshal` 失败 = **不**报错 = 进 `recoverCorruptState`,扫盘重建 + 全部 `leased` + `LeaseHolder = "recovered: ..."`。
- 核心原则(同 VISION.md):**under uncertainty, leave the worktree in place with an actionable explanation** —— 即使在"最坏情况"也要保守。

## 它们为什么必须同时存在

```text
        acquire  ──►  Pool  ◄──  durable lease
                      │                  │
                      ▼                  ▼
                reset / use        return / rerun
                      │                  │
                      ▼                  ▼
                crash 一半          文件 corrupt
                      │                  │
                      └────► atomic-state-recovery ◄────┘
                              (全部标 leased,等用户 return)

delete:
        safe-destroy-by-default ── 让任何 prune/destroy 都走"预览 + opt-in"
            │
            └─► 与 durable lease 冲突时:
                 单路径 + --include-leased 才能删
                 --all 永远不允许
```

- 没有 **池化** → 每 agent 等十分钟重装依赖。
- 没有 **Lease** → 长期 agent 必须自维护心跳 + 心跳死了就丢失工作树。
- 没有 **Safe destroy** → 一行脚本误删整月工作。
- 没有 **Atomic + Recover** → 一次崩溃 → state 全错 → 后面所有命令全错。
- **任何一条缺**,整套都不可靠。

## 三个"原则提炼"(可以被任何工程借用)

### 原则 1:不同事实不要互相推断

> A live process, a short lifecycle reservation, and a durable lease represent different facts and should not be inferred from one another.

落点:字段独立(`OwnerPID` / `Destroying` / `Leased`/`LeaseID`),判定函数不交叉。任何用"如果 PID 还活着就当 leased"或"如果 state 里没 leased 就当 idle"的逻辑,都会在边缘情况出 bug。treehouse 把这条写进 VISION.md,不是因为它是好品味,是因为历史上别的 runtime 都在这里踩过坑。

### 原则 2:不确定时不删

> Under uncertainty, leave the worktree in place with an actionable explanation, and verify the safety facts again at deletion time.

具体落实:

- `prune` 跳过任何"不能 100% 验明 clean + 已合"的条目。
- `destroy` 默认 dry-run。
- state corrupt 时,所有条目默认成 leased,等用户 return / destroy。
- origin 不可达:绝不把远程候选当孤儿删。

### 原则 3:风险要分开 opt-in,不要 blanket force

- 任何"`--force` 一键跳过全部保护"的设计,都是把"我没看 banner"的成本留给未来。
- 用 `--yes` + `--include-<类别>` 的组合,确保用户**思考了**每一类风险。
- 真正的"全删"是 `--all --yes --include-unlanded --include-in-use`,看到这些 flag 用户就该警觉。

## 谁该用 treehouse

| 角色 | 用 treehouse 的方式 |
|---|---|
| 个人开发者 + 偶尔跑 AI agent | `treehouse`,人工 subshell,subshell 退出自动 return。|
| 团队 CI runner | `treehouse get --lease`,在 lease 里跑 `npm test`,`--if-lease-id` 条件 return。|
| 长跑 opencode-style daemon | `get --lease --lease-holder "oc-runner-01"`,后台 daemon 持有,定期 `treehouse status --json` 健康检查。|
| 本地实验 / 学习新分支 | `treehouse enter 3` attach 一个空闲的,subshell 退出不删。|
| 自动化清理 | `treehouse prune --yes`(只删真正合并的)或 `treehouse prune --all --prune-orphans --yes`(每个候选都审查过)。|

## 可以复用的"小型本地 runtime"原则

如果你也在写一个有本地持久 state 的小 CLI,可以照着这个清单走:

```text
[ ] state file 写在固定路径,锁住(<dir>/<name>.lock)
[ ] 写: temp file + fsync + rename + parent fsync(支持的平台)
[ ] 读: 解析失败 -> 扫描 on-disk 重建,默认保守,显式警告
[ ] 不同语义分开,绝不互相推断
[ ] 破坏性操作默认 dry-run
[ ] 风险类别独立 opt-in,不提供 blanket force
[ ] 退出码区分"啥都没动"和"动了"两种状态
[ ] 操作前 double-check,操作中再 double-check
[ ] 不假设任何系统服务/daemon 一定在跑
[ ] 三平台都跑(linux/macOS/windows),用 build tag 隔离平台差异
```

参考仓库路径:`_raw/_archived/github-kunchenguid-treehouse.txt`(gitingest 导出,commit `939cb59b`),2026-08-03。

## 相关链接

### 本地页

- [[entities/treehouse]] —— 实体
- [[concepts/git-worktree-pool-pattern]] —— 池化复用
- [[concepts/worktree-durable-lease]] —— Lease + ABA
- [[concepts/safe-destroy-by-default]] —— 删除安全
- [[concepts/atomic-state-recovery]] —— 原子写 + 自愈
- [[concepts/ai-agent-sandbox]] —— AI agent 层视角
- [[skills/treehouse-cli]] —— 用法速查

### 外部

- <https://github.com/kunchenguid/treehouse>
- <https://kunchenguid.github.io/treehouse/install.sh>
