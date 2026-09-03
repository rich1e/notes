---
title: Research: OpenLore — 把代码编译成 agent 的确定性记忆
category: synthesis
tags:
  - synthesis
  - openlore
  - ai-agent
  - static-analysis
  - mcp
  - commit-gate
  - ai-safety
sources:
  - https://github.com/clay-good/OpenLore
  - _raw/_archived/github-clay-good-OpenLore.txt (gitingest export, clay-good/OpenLore, 2026-08-03)
created: 2026-08-03T12:35:00Z
updated: 2026-08-03T12:35:00Z
summary: OpenLore 把"代码考古学"做到极致:静态分析驱动的知识图谱 + 确定性 fact layer + hot path 0 LLM + 编辑时架构 guardrail + commit gate。3 条独立但勾连的设计线 + 4 条可复用原则,与 vault 已有 agent-os / claude-mem / treehouse 形成连贯基础设施图。
tier: core
lifecycle: reviewed
lifecycle_changed: 2026-09-03
lifecycle_reason: "auto-promoted by wiki-lint --consolidate: age>30d, confidence>0.88"
lifecycle_changed: 2026-08-03
base_confidence: 0.88
provenance:
  extracted: 0.94
  inferred: 0.06
  ambiguous: 0
relationships:
  - target: "[[entities/openlore]]"
    type: related_to
  - target: "[[concepts/static-analysis-knowledge-graph]]"
    type: related_to
  - target: "[[concepts/deterministic-agent-memory]]"
    type: related_to
  - target: "[[concepts/no-llm-hot-path]]"
    type: related_to
  - target: "[[concepts/commit-gate-guardrails]]"
    type: related_to
  - target: "[[concepts/agent-operating-system]]"
    type: related_to
  - target: "[[concepts/claude-mem-memory-architecture]]"
    type: related_to
  - target: "[[entities/treehouse]]"
    type: related_to
---

# Research: OpenLore — 把代码编译成 agent 的确定性记忆

> 一次性整合 entities/openlore 与 4 个相关 concept,提炼 **"为什么这套设计形成闭环"** 与 **"它解决的是哪类问题"**。

## 一句话总结

**OpenLore** 把"agent 记忆"拆成两层:claude-mem 管 session 间**经验**,OpenLore 管**代码事实**——后者用**一次离线静态分析 + 知识图谱 + MCP** 把仓库编译成可查询的事实层,hot path 0 LLM,确定性可重放,显式 stale,失败可追 Evidence。可作为 agent OS 五层 memory 框架中 **Knowledge Memory 层的参考实现**。

## 4 条独立但勾连的设计线

### 线 A:静态分析驱动的代码知识图谱

详见 [[concepts/static-analysis-knowledge-graph]]。

- FileWalker → SignificanceScorer → ImportParser → DependencyGraph → RepositoryMapper → ArtifactGenerator
- 关键算法:文件 significance 评分(4 维加权)、PageRank 风格 importance、Louvain modularity 域聚类、Tarjan SCC 循环检测
- 输出:`.openlore/analysis/` JSON + `llm-context.json` 主索引,gitignorable,删了不影响仓库
- **关键决策**:图是骨架,embedding 是配菜(可关)。无 embedding 时 BM25 自动兜底。

### 线 B:hot path 0 LLM

详见 [[concepts/no-llm-hot-path]]。

- `analyze` / `drift` / `orient` / `search_code` / `analyze_impact` 全本地静态算法
- watch mode 默认开,batched flush + 增量 reverse-dep closure + INCREMENTAL_CLOSURE_BUDGET 边界(超出显式 stale)
- LLM 只在 `generate` / `verify` / `record_decision consolidate` 三个 cold path opt-in
- **直接证据**:README 与 benchmark 公开同步发亏损(小仓库浅任务 +59%)

### 线 C:commit gate 双 hook + 架构不变量

详见 [[concepts/commit-gate-guardrails]]。

- **Drift hook**(reactive):git-changed files ↔ spec source-file 列表对比,5 类 finding(gap / stale / uncovered / orphaned / adr_gap / adr_orphaned)
- **Decisions gate**(proactive):pending 决策等人审,4 类 reason(verified / approved_not_synced / drafts_pending_consolidation / no_decisions_recorded)
- **check_architecture**(编辑时):`layers` / `forbidden` / `allowedOnly` 三种确定性规则,跑在跨语言统一图而非单语种 AST
- 共同特征:显式 finding + Evidence + 风险独立 opt-in(参考 [[concepts/safe-destroy-by-default]] 思路)

### 线 D:确定性 fact layer 的失败语义

详见 [[concepts/deterministic-agent-memory]]。

- 同 query 永远同答案
- `locate_symbol_span` 返回 `fresh / stale / ambiguous / not-found`,**永不模糊猜** —— stale 时不给 offset,只给 re-analyze 提示
- 引用追到 file:line + commit hash,无 embedding 余弦相似度
- 无 embedding 服务时 BM25 兜底(确定但弱),有 embedding 时增强
- **Honesty contract**:不发布 benchmark 没给出的节省数字,亏损挨着赢一起发

## 它们为什么必须同时存在

```text
              acquire task "改 X"
                       │
                       ▼
                ┌──────────────┐
                │  orient()    │  ← 线 A:静态分析图 (relevantFiles/insertPoints)
                │  (430µs p50) │     线 B:hot path,无 LLM
                └──────┬───────┘
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
  search_code    blast_radius   verify_claim
        │              │              │
        └──────────────┼──────────────┘
                       ▼
              change 之前:certify_public_surface / change_impact_certificate
                       │
                       ▼
              pre-commit hook:
                drift (spec coverage)
                + decisions gate (decision approval)
                       │
                       ▼
              post-commit:analyze_impact 重算 + 可选 verify
```

- 没有 **线 A** → 每次任务靠 grep,agent 反复 rediscover 结构,benchmark 亏
- 没有 **线 B** → 每次任务烧 token + 概率性 stale
- 没有 **线 C** → agent 自动改的代码过 commit 时无人把关
- 没有 **线 D** → 失败模式静默,review 时一起赔
- **任何一条缺**,整套就退化成"加速 grep"

## 4 条可复用原则(可被任何"agent infra 工具"借用)

### 原则 1:hot path 不放 LLM

LLM 在 hot path 必输:**成本 + 性能 + 可靠性 + 安全 + 诚实**五维全亏。每次都付 token + 每次都拿"看起来对" + 服务挂了全瘫 + stale 静默。

详见 [[concepts/no-llm-hot-path]]。

### 原则 2:确定性 + 显式失败

同一 query 永远同答案;失败模式分桶:`fresh / stale / ambiguous / not-found` / `verified / approved_not_synced / drafts_pending_consolidation` / `gap / stale / uncovered / orphaned` / `confirmed / refuted / unverifiable`。

绝不"模糊对",绝不"静默 stale"。Agent 拿不到"看起来对",就只能回去查或停下来问。

### 原则 3:风险独立 opt-in,不 blanket force

drift / decisions / architecture invariants / certify_public_surface / change_impact_certificate **每个独立开关**。每个 gate 一个 finding 一个 reason,失败显式可追。

参考 [[concepts/safe-destroy-by-default]] 与 [[concepts/atomic-state-recovery]] 的设计思路。

### 原则 4:Honesty contract

> 不发布 benchmark 没给出的节省数字,亏损挨着赢一起发,每个 token claim 都有可执行命令追源。

具体落地:`openlore prove --estimate` 让用户在自己仓库里预测 orientation tax;benchmark 公开同步发"chalk −32% vs express +59%"这种反向 case;`reason` 字段必带可执行修复命令。

## 与 vault 已有基础设施的关系

```text
                  ┌─────────────────────────────────┐
                  │     Agent Operating System      │
                  │   (五层 memory 框架,concept)    │
                  └────────────┬────────────────────┘
                               │
       ┌───────────────────────┼───────────────────────┐
       │                       │                       │
       ▼                       ▼                       ▼
┌─────────────┐         ┌─────────────┐         ┌──────────────┐
│ claude-mem  │         │  OpenLore   │         │  treehouse   │
│ (经验层)    │         │ (代码事实层)│         │ (worktree    │
│ hook 捕获   │         │ 静态分析图  │         │   池)        │
│ SQLite+Chroma│        │ JSON+可选vec│         │ 池化复用     │
│ haiku 压缩  │         │ 0 LLM hot   │         │ durable lease│
└──────┬──────┘         └──────┬──────┘         └──────┬───────┘
       │                       │                       │
       └───────────────────────┼───────────────────────┘
                               │
                               ▼
                ┌─────────────────────────────────┐
                │   AI 编码 agent(Claude Code     │
                │   / Cursor / Cline / Codex...)  │
                └─────────────────────────────────┘
```

- **claude-mem** 补 session 间**经验**("我们上次怎么修的")
- **OpenLore** 补**代码结构**("X 函数被谁调用,改它会怎样")
- **treehouse** 补**写在哪**("这个 agent 任务在哪个 worktree 跑")
- **三者正交,组合即 AI agent 的本地基础设施三件套**

## 谁该用 OpenLore

| 角色 | 用法 |
|---|---|
| 个人开发者 + AI agent | `openlore install`,agent 自动获 `orient()` 单调用入口 |
| 团队 + 私有代码 | 同上,加 `drift --install-hook` 保证 spec 同步 |
| 大型 monorepo + 多 agent 并行 | + `decisions gate` + `check_architecture` + `--preset memory` 启用 write 面 |
| CI / pre-commit | `openlore drift --fail-on error --json` |
| audit / 保密环境 | 完全离线,无 API key,无遥测,opt-in 上云 |
| AI 工具作者 | 接入 MCP,73 tools 按 6 family 选用,substrate 默认避免 schema prefix 过大 |

## 未来可扩展的方向

- **更大 monorepo**:`analyze` 分钟级一次性构建,watch mode 已有 stale 边界,但 vector index 在 > 5000 文件时自动降级
- **更多语言**:当前 18 + IaC 12;specs 已规划 SPEC 08(additional languages)
- **federation / spec store**:跨仓库结论共享,`federation_status` / `working_set_context`
- **decision as graph node**(SPEC 16):决策也入图,`orient` 可"按决策相关度"过滤

## 参考

### 本地页面

- [[entities/openlore]] —— 实体
- [[concepts/static-analysis-knowledge-graph]] —— 图骨架
- [[concepts/deterministic-agent-memory]] —— fact layer 原则
- [[concepts/no-llm-hot-path]] —— hot/cold 划分
- [[concepts/commit-gate-guardrails]] —— CI/pre-commit 拦截
- [[skills/openlore-cli]] —— 命令速查

### 外部

- <https://github.com/clay-good/OpenLore>
- <https://www.npmjs.com/package/openlore>
- `docs/PHILOSOPHY.md` —— "Archaeology over Creativity"(本文档最值得引用的 41 行)
- `docs/mcp-tools.md` —— 73 工具 + 6 family + substrate preset
- `docs/ALGORITHMS.md` —— significance / PageRank / Louvain / Tarjan SCC / truncation
- `docs/AGENT-BENCHMARKS.md` —— 公开 benchmark 数据(含亏)
- `docs/architecture-invariants.md` —— check_architecture 设计