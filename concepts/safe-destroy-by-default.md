---
title: 破坏性操作的默认安全设计
category: concepts
tags:
  - cli-design
  - safety
  - destructive-ops
  - treehouse
  - api-design
sources:
  - https://github.com/kunchenguid/treehouse
  - _raw/_archived/github-kunchenguid-treehouse.txt (gitingest export, kunchenguid/treehouse, 2026-08-03)
created: 2026-08-03T11:35:00Z
updated: 2026-08-03T11:35:00Z
summary: 破坏性 CLI 默认 dry-run + 风险类别独立 opt-in;拒绝 blanket --force、跨池 wildcard、global delete-everything;treehouse v2.0.0 移除 --force 是教科书式安全 API 演进。
tier: supporting
lifecycle: reviewed
lifecycle_changed: 2026-09-03
lifecycle_reason: "auto-promoted by wiki-lint --consolidate: age>30d, confidence>0.85"
lifecycle_changed: 2026-08-03
base_confidence: 0.85
provenance:
  extracted: 0.93
  inferred: 0.07
  ambiguous: 0
relationships:
  - target: "[[entities/treehouse]]"
    type: derived_from
  - target: "[[concepts/git-worktree-pool-pattern]]"
    type: extends
  - target: "[[concepts/worktree-durable-lease]]"
    type: related_to
---

# 破坏性操作的默认安全设计

> treehouse v2.0.0 拆掉"一刀切 `--force`",改为三类风险各自独立 opt-in,加 `--yes` 才真执行。

## 默认原则

```text
默认行为   : dry-run,只读,展示预览
接受默认  : 不需要任何 flag
真删      : 显式 --yes + 至少一个 --include-*
```

每个破坏性命令的预览都打印"风险揭示标签"——`[disposable]`、`[leased]`、`[in-use:<pid>]`、`[unmerged]`、`[dirty]`、`[unverified]`,必要时 `,` 分隔。**不要**让"全部已删"成为唯一退出文案——明确告知哪些实际删除、哪些被跳过。

## 命令的形状

### `prune`

- 默认 dry-run,只打 idle + clean + HEAD 已合入 default branch 的。
- `--all` / `--global`:跨用户级 root 下所有托管 pool 扫描,但**仍读用户级 config**,不读 repo 级(因为可以脱离 repo 跑)。
- `--prune-orphans`:把 backing repo 缺失的孤儿列入候选项(每个候选项标 `content could not be verified`)。
- `--yes`:真删。
- 当 origin 不可达时,prune **不会**把远程孤儿当可删候选(`origin unreachable (cannot verify)`);真正的孤儿必须用户显式 `--prune-orphans`。

### `destroy`(v2.0.0 重写)

- 默认 dry-run。
- `--yes`:真删。
- `--all`:**只能**配合显式 pool 路径(`destroy <pool> --all`),无池路径 = 错误;**绝无**跨池全局 destroy。
- 风险分三类,各自独立 opt-in:

| Flag | 含义 |
|---|---|
| `--include-unlanded` | 脏 / 未合 / 不可验证的 worktree(**不可逆数据丢失**)|
| `--include-in-use` | 有运行进程 / owner reservation 的(进程先优雅终止)|
| `--include-leased` | **仅当指定精确 worktree 路径时**才生效;**不允许**与 `--all` 组合 |

`--include-leased` + `--all` → 命令直接拒绝,**永远不**让批量删租约成为可能。

### 为什么干掉 `--force`

旧 `--force` 一举覆盖所有保护(in-use、unmerged、dirty、leased)—— 这是危险的:

- 用户在 cron / 自动化里写成 `treehouse destroy --force` 等同于定时炸弹。
- 安全是默认权重,不应让"再加一个 flag"成为去激活所有防御的快捷方式。
- 替代:每个具体风险,显式 opt-in + `--yes`。**取错代价是显式 opt-in 的代价**,而不是模糊 `--force` 的代价。

迁移表(README 显式给出):

| 旧 | 新 |
|---|---|
| `destroy <path> --force` | `destroy <path> --yes`(脏/未合/不可验证 再加 `--include-unlanded`,有进程再加 `--include-in-use`,租约时再加 `--include-leased`)|
| `destroy --all --force` | `destroy <pool> --all --yes`(脏/未合/不可验证 加 `--include-unlanded`;有进程加 `--include-in-use`;**租约永不被 `--all` 删除**)|

## 退出码语义

- 单工作树被 skip(因缺某 `--include-*`) → 非零退出 → 脚本能感知"啥都没干"。
- 批量 `--all` skip → 零退出 → 正常;细节靠 inspect summary。
- 这样脚本既能 dry-run,也能用 status 判断要不要补加 flag。

## 跨命令一致的两阶段 reservation(`destroy` / `prune`)

```text
1. flock 拿锁 + 把目标 entry 标 Destroying=true,落盘
2. 跑 pre_destroy hook
3. 检查 sameDestroyReservation 仍持有 → 删 → 解锁
```

第 3 步保护一种 race:hook 跑得很慢,期间该 worktree 被另一个 `get` 重新 acquire —— destroy 会发现 reservation 已被覆盖,**不再删**。这是用状态字段做时间戳级别互斥的精髓。

## 设计哲学(摘自 VISION.md)

> Treehouse should delete or reset user work only when the scope is clear and the required facts can be verified against current Git, process, and lifecycle state.
> Under uncertainty, leave the worktree in place with an actionable explanation, and verify the safety facts again at deletion time.
> Destructive commands should preview their effect by default, require explicit intent to act, and gate independent risks separately.
> Blanket force options, ambiguous targets, and global delete-everything paths should be resisted.

逐句要点:

- 删除前要 **现在** 验证 Git / 进程 / state,**不**信任陈旧信息。
- 不确定 → 留下 + 解释,而不是冒险。
- 默认 preview;独立 opt-in;拒绝 blanket force + wildcard target + global nuke。

## 这套模式可以用到任何破坏性 CLI 上

推广原则(可作为通用 checklist):

```markdown
[ ] 默认是 dry-run,执行需 --yes
[ ] 风险分桶而不是"全/无":每桶一个 --include-*
[ ] 拒绝 blanket --force;迁移文档写明每个旧 flag → 新 flag 对应
[ ] target 必须显式:不允许 "对一切生效" 的隐含作用域
[ ] 退出码表达"实际做了什么":命中跳过 ≠ 命中删除
[ ] 删除前再二次验证 fact(state/磁盘/进程 之一)
[ ] pre-delete hook(如有)在两阶段 reservation 内跑
[ ] 一致原则:同一类 operation 的所有命令(`prune` / `destroy`)对同一桶风险用同一个 --include-* 名字
```

## 相关

- [[entities/treehouse]]
- 池机制:[[concepts/git-worktree-pool-pattern]]
- Lease 字段(含 `--include-leased` 边界):[[concepts/worktree-durable-lease]]
- State 安全:[[concepts/atomic-state-recovery]]
