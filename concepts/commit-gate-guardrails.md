---
title: Commit gate guardrails — 把 agent 行为关进 CI
category: concepts
tags:
  - ci-cd
  - ai-agent
  - commit-gate
  - safety
  - drift-detection
  - openlore
sources:
  - https://github.com/clay-good/OpenLore
  - _raw/_archived/github-clay-good-OpenLore.txt (gitingest export, clay-good/OpenLore, 2026-08-03)
created: 2026-08-03T12:25:00Z
updated: 2026-08-03T12:25:00Z
summary: 在 commit 前用确定性工具拦住"不该过的提交":drift hook(代码改了 spec 没改)+ decision gate(决策未经人审)+ 架构不变量 guardrail(新 import 违反 layer 规则),失败显式可追。
tier: supporting
lifecycle: reviewed
lifecycle_reason: "auto-promoted by wiki-lint --consolidate: age>30d, confidence>0.83"
lifecycle_changed: 2026-08-03
base_confidence: 0.83
provenance:
  extracted: 0.93
  inferred: 0.07
  ambiguous: 0
relationships:
  - target: "[[entities/openlore]]"
    type: derived_from
  - target: "[[concepts/deterministic-agent-memory]]"
    type: extends
  - target: "[[concepts/no-llm-hot-path]]"
    type: related_to
  - target: "[[concepts/static-analysis-knowledge-graph]]"
    type: related_to
  - target: "[[concepts/safe-destroy-by-default]]"
    type: related_to
  - target: [[concepts-agent-operating-system × concepts-deterministic-agent-memory]]
    type: related_to
---

# Commit gate guardrails — 把 agent 行为关进 CI

> AI agent 自动改代码时,默认它会**保守**地通过所有 gate。我们用确定性工具(且每个风险独立 opt-in)在 commit 前把"该拦"的事显式拦下。

## 一句话定义

commit gate = 一个**确定性 + 显式 + 默认安全**的拦截器,在 commit 触达远程前判定"这次改动是否触发了你说过要拦的事",用 git hook 串进流水线。

## 三大类别(参考 OpenLore + treehouse 思路)

### 类别 A:**Drift / 覆盖门** —— 代码改了 spec 没改

工具:`openlore drift` —— 比较 git-changed files ↔ 每个 spec 的 source-file 列表。

- **方向**:Reactive(代码改了 spec 没改)
- **速度**:毫秒级,无 API key
- **检测 5 类问题**:
  - `gap`:代码改了 spec 没改
  - `stale`:spec 引用了已删 / 重命名的文件
  - `uncovered`:新文件没有 spec domain 覆盖
  - `orphaned`:spec 声明的文件已不存在
  - `adr_gap` / `adr_orphaned`:ADR ↔ spec ↔ source 三方不一致

```bash
openlore drift --install-hook     # 装
openlore drift --fail-on error --json   # CI 模式
```

### 类别 B:**Decision gate** —— 决策未经人审

工具:`openlore decisions` + `record_decision` / `sync_decisions`。

- **方向**:Proactive(pending 决策等人审)
- **速度**:瞬时,无 LLM(consolidation 已在 background 跑完)
- **失败原因**(`reason` 字段):

| Reason | 含义 | 修复命令 |
|---|---|---|
| `verified` | consolidation + verify 完成,等人审 | `approve_decision` / `reject_decision` + `--sync` |
| `approved_not_synced` | 已批但未写 spec | `openlore decisions --sync`,重 commit |
| `drafts_pending_consolidation` | 草稿未 consolidation | `openlore decisions --consolidate --gate` |
| `no_decisions_recorded` | source 改了但没记决策 | 同上(走 fallback extractor) |

哨兵文件 `.git/OPENLORE_GATE_RAN`(pre-commit 写) + post-commit 检查;`--no-verify` 绕过会被 post-commit hook 报警。

### 类别 C:**架构不变量 guardrail** —— 新 import 违反 layer

工具:`check_architecture`(SPEC 23)。

- **方向**:Pre-edit query + 全仓扫
- **速度**:毫秒,无 API key
- **三种确定性规则**:`layers` / `forbidden` / `allowedOnly`
- **声明位置**:`.openlore/architecture.json` 或 synced ADR 的 `Invariant:` 标记
- **关键差异**:运行在**编辑时**(`check_architecture({from, to})` → yes/no + 规则),而不是 CI 后置
- **跨语言图**:不依赖某一语种 AST,而是统一 dependency graph

```bash
check_architecture({ directory, from: "src/core/thing.ts", to: "src/cli/view.ts" })
// → { allowed: false, rule: { kind: "forbidden", reason: "core stays UI-agnostic" }, ... }
```

未声明规则时工具**完全 inert** —— 无输出、无副作用、不干扰现有 CI。

## 共同设计原则

### P1:确定性 + 离线

所有 gate 都必须能在 CI 容器里无网络跑完。任何依赖外网 / API key 的 gate 在 audit / private repo / airgapped 环境直接挂。

### P2:失败显式,可追 Evidence

每条 finding 必须带证据(文件 + 行 + commit / spec section / ADR id)。Agent 看到 finding 后要么改代码、要么改 spec / ADR / 规则,**没有第三个选项**(不能"忽略"或"我说不算")。

### P3:风险独立 opt-in(参考 [[concepts/safe-destroy-by-default]])

每个 gate 都是独立开关:

```text
--fail-on error      # 默认,只 fail error 级 finding
--fail-on warning    # warning 也 fail
--domains auth,user  # 只审特定 spec domain
```

任何"一键全过"的设计都是反模式 —— blanket skip flag 比没有 gate 更危险(让人误以为"过 CI = 安全")。

### P4:不与 LLM 混淆

LLM 可以在 cold path(consolidate / verify)做语义判断,**不能**在 gate 处做。Gate 必须 deterministic,LLM 哪怕 99.9% 准确,1 次失误就是 merged 错代码。

### P5:parallel 安装、不互斥

```bash
openlore drift --install-hook     # A 类
openlore setup --tools claude     # B 类(同时装 Claude Code skills)
# A + B 同时存在,关注点正交
```

drift hook 看 spec coverage,decision gate 看决策审批;一个 commit 可同时触发两者失败(纯重构也撞 drift、新决策也撞 gate)。

## CI 集成形态

```yaml
# .github/workflows/spec-drift.yml
name: Spec Drift Check
on: [pull_request]
jobs:
  drift:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }    # git diff 需要全历史
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: npm install -g openlore
      - run: openlore drift --fail-on error --json
```

`--json` 让 CI 解析方便,`--no-color` 让日志干净。Bootstrap 用共享 bundle:`openlore import .openlore/index-bundle.olbundle` 验证导入,失败 fallback 到 `openlore analyze`。

## 反面案例(让 gate 失效的反模式)

- ❌ `--no-verify` 跳过 hook,post-commit 不检查 —— 绕过就完事
- ❌ gate 在 LLM 服务里跑,服务 down 就跳过 —— 静默绕开
- ❌ gate 输出不可解析的字符串,人 review 一眼关掉 —— 没起到 gate 作用
- ❌ blanket skip flag(`--force` / `--no-validate`) —— 同 treehouse 的 `--force` 已删
- ❌ 把 finding 改成"warning 后默认 allow" —— warning 应该 fail-on 才对
- ❌ drift / decisions / architecture 三类都用同一个 `--skip-all` —— 等于没 gate
- ❌ 只看 changed lines,不看 callers —— 漏掉跨文件影响

## 何时该装哪类 gate

| 团队/项目阶段 | 建议 |
|---|---|
| 0 → 1(早期快速迭代)| drift hook(装,默认 fail error)|
| 1 → 10(开始多人协作)| + decision gate |
| 10 → 100(规模 + 长期维护)| + architecture invariants(慢慢加规则) |
| 100+(多团队 monorepo)| + cross-domain impact + structural-diff + reachability dead-code |

逐步加,不要一次装齐——规则不成熟时 gate 太严会拖慢迭代。

## 谁在做相关的工作(2026 年视角)

- **OpenLore**:drift + decisions + architecture invariants(spec 23),最完整
- **treehouse**:`destroy --include-*` 系列也是"风险独立 opt-in"的 commit-after-merge 安全范式
- **dependency-cruiser / ArchUnit / import-linter**:CI 后置层做架构验证;OpenLore 是编辑时
- **pre-commit / husky + custom scripts**:用户层最常见但容易写得不严格

## 相关

- [[entities/openlore]] —— 实现
- [[concepts/deterministic-agent-memory]] —— 确定性数据源
- [[concepts/no-llm-hot-path]] —— gate 必须在 hot path 之外
- [[concepts/static-analysis-knowledge-graph]] —— 架构规则依赖的统一图
- [[concepts/safe-destroy-by-default]] —— 同样"风险 opt-in"的删除哲学
- [[concepts/agent-operating-system]] —— 上层框架