---
title: OpenLore — AI 编码 agent 的静态分析记忆层
category: entities
tags:
  - cli
  - ai-agent
  - static-analysis
  - knowledge-graph
  - rag
  - openlore
  - mcp
sources:
  - https://github.com/clay-good/OpenLore
  - _raw/_archived/github-clay-good-OpenLore.txt (gitingest export, clay-good/OpenLore, commit d3393fa2, 2026-08-03)
created: 2026-08-03T12:05:00Z
updated: 2026-08-03T12:05:00Z
summary: TypeScript 编写的本地优先 agent 记忆与治理工具:静态分析生成代码知识图谱(call graph / types / tests / decisions / IaC),通过 MCP 暴露 73 个工具,hot path 无 LLM,确定性输出,可做 commit gate。
tier: supporting
lifecycle: draft
lifecycle_changed: 2026-08-03
base_confidence: 0.85
provenance:
  extracted: 0.95
  inferred: 0.05
  ambiguous: 0
relationships:
  - target: "[[concepts/static-analysis-knowledge-graph]]"
    type: derived_from
  - target: "[[concepts/deterministic-agent-memory]]"
    type: derived_from
  - target: "[[concepts/no-llm-hot-path]]"
    type: derived_from
  - target: "[[concepts/commit-gate-guardrails]]"
    type: derived_from
  - target: "[[concepts/agent-operating-system]]"
    type: related_to
  - target: "[[concepts/claude-mem-memory-architecture]]"
    type: related_to
  - target: "[[concepts/ai-agent-sandbox]]"
    type: related_to
  - target: "[[entities/claude-code]]"
    type: related_to
---

# OpenLore — AI 编码 agent 的静态分析记忆层

**OpenLore**(`clay-good/openlore`,npm 包名 `openlore`,MIT 协议,Node ≥ 22.13)是面向 AI 编码 agent 的**本地优先、无 API key** 的代码记忆与治理层。它通过**一次离线静态分析**把仓库编译成可查询的知识图谱,然后通过 **MCP** 把导航 / 治理工具暴露给 Claude Code / Cursor / Cline / Roo Code 等 agent,hot path 全部确定性,不消耗 LLM 配额。

> "Deterministic, local-first memory and guardrails for AI coding agents — with no LLM in the hot path."

## 一句话定位

把 `git grep` 升级为 **"agent 一句话问到代码位置 + 影响半径 + 公共 API 契约 + spec 是否落后"** 的查询层。

## 关键事实

| 项 | 值 |
|---|---|
| 包名 | `openlore`(npm / Homebrew / npx / Nix flake) |
| 语言 | TypeScript(Commander.js CLI + 纯函数 API) |
| 协议 | MIT |
| 节点要求 | Node ≥ 22.13 |
| 测试规模 | 5500+(badge 自报) |
| 支持语言 | 18 种代码语言 + 12 种 IaC 生态 |
| MCP 工具数 | 73 个,按 6 capability family 分组;默认 `substrate` 预设只暴露 13 个 |
| 索引存储 | `.openlore/` 目录下 JSON 文件(可 .gitignore,可重建,无锁) |
| 关键命令 | `install` / `orient` / `review` / `prove` / `enforce` / `drift` / `mcp` |
| 数据流 | 全本地,无遥测(默认),opt-in 上云 |
| 哲学 | "Archaeology over Creativity"——只记录代码事实,不发明意图 |

## 一次完整生命周期

```bash
npm install -g openlore
cd your-project
openlore install        # 自动检测 agent(Claude Code/Cursor/Cline/AGENTS.md)、注册 MCP、构建本地索引
openlore doctor         # 检查 config / index / MCP / embeddings
openlore features       # 列出所有可选能力(embeddings / commit gate / spec store...)是否开启、及一条命令启用
```

首次构建在 ripgrep 上测得 13.6 秒、27 MB 磁盘,完全离线,无 API key。

## 核心抽象:一个结构性子基 + 两个面

OpenLore 不是两个产品,是**一个统一结构性子基**(call graph + types + tests + decisions + IaC + specs) 暴露成两个面:

- **Read 面**(navigation / governance reads):`orient`、`search_code`、`get_subgraph`、`trace_execution_path`、`blast_radius`、`verify_claim`、`recall`
- **Write/Check 面**(anchored notes / decision gate):`remember`、`record_decision`、`certify_public_surface`、`change_impact_certificate`、`check_architecture`

默认只暴露 read 面的高频子集(`substrate` preset,13 tools)。write/check 面用 `--preset full` / `--preset minimal` / `--preset memory` 显式 opt-in。

### 6 个 capability family

每个工具声明**且仅声明一个** capability family,在 MCP `annotations.family` 暴露:

| Family | 回答 | 代表工具 |
|---|---|---|
| `navigate` | 读结构 / spec 图,返回结论 | `orient`、`find_path`、`analyze_impact`、`select_tests`、`find_dead_code`、`get_map` |
| `change` | 推演某次 diff 的影响 | `structural_diff`、`blast_radius`、`change_impact_certificate`、`certify_public_surface` |
| `remember` | 记录 / 取回 code-anchored 事实 | `remember`、`recall`、`record_decision` |
| `verify` | 在断言触达人类之前裁决 | `verify_claim` |
| `coordinate` | 并行任务的排程与冲突消解 | `plan_parallel_work`、`map_in_flight_conflicts` |
| `federate` | 跨仓库 / spec store | `federation_status`、`spec_store_status`、`working_set_context` |

每个工具在描述里点名其"近邻兄弟"(如 `find_clones` ↔ `get_duplicate_report`、`blast_radius` ↔ `structural_diff` ↔ `change_impact_certificate`),让 agent 一次会话能选准工具而不是混着调。CI guard `tool-contract.test.ts` 在工具漏声明 family 或漏点兄弟时 fail。

## orient() — 单调用入口

`orient("add a payment method")` 一次调用返回:

```json
{
  "relevantFiles": [...],
  "relevantFunctions": [{"name": "...", "fanIn": 5, "isHub": true, "language": "TypeScript"}],
  "callPaths": [{"function": "...", "callers": [...]}],
  "insertionPoints": [{"rank": 2, "strategy": "cross_cutting_hook", "reason": "..."}],
  "suggestedTools": ["record_decision", "analyze_impact", ...]
}
```

约 430µs p50 on a 15k-node graph(进程内,经 MCP);一次冷 CLI 调用 ~2s,大多花在 Node 启动。

## 治理(governance)三件套

> 三个工具回答 agent 在 commit 前必须被告知的事。

| 工具 | 用途 |
|---|---|
| `certify_public_surface` | 把每次 export 变化分类成 `breaking / non-breaking / potentially-breaking`,**点名每个被破坏的消费者**;保守判定,绝不悄悄给"safe"。 |
| `change_impact_certificate` | 当 diff **打开一条新路径**到你声明的"敏感边界"时报警(改动后才可达,改动前不可达)。 |
| `verify_claim` | 对断言返回 `confirmed / refuted / unverifiable` + 代码引用,挡住 agent "X 是 dead code"或"Y 可安全改"之类猜测。 |

外加 `openlore enforce`:commit gate,只对标了 `blocking` 的 finding 拦截;默认 advisory。

## 架构不变量 guardrail(`check_architecture`)

> "Spec 23 — deterministic, offline, no network."

让仓库在 `.openlore/architecture.json` 声明架构约束(layer / forbidden / allowedOnly),agent 在**编辑前**询问"这里能不能加这条 import",给确定性 yes / no + 规则 + 原因。运行时叠加在 `orient` 的 `architectureViolations` 块。

与 ArchUnit(Java)/ dependency-cruiser(JS)/ import-linter(Python)互补:**编辑时**(不是 CI 后置)**、跨语言**(而不是某一语种 AST)判定。

- **完全 opt-in**:无 rules 文件时工具完全 inert(无输出、无副作用)。
- **作者声明**:规则只在 `.openlore/architecture.json` 或 synced ADR 的 `Invariant:` 标记里。LLM 永不发明规则。
- **确定性词汇**:只对图能判的规则生效,无"语义"模糊规则。

## pre-commit 双 hook

| Hook | 方向 | 速度 | 关注点 |
|---|---|---|---|
| **Drift hook**(`openlore drift --install-hook`) | Reactive | 毫秒,无 API key | 代码改了 spec 没改 |
| **Decisions gate**(`openlore setup --tools claude`) | Proactive | 瞬时,无 LLM | pending 决策未经人审 |

二者关注点正交:drift 看 spec 覆盖,decisions gate 看决策审批。两者都装是官方推荐姿势。

## 性能与诚实

README 与 benchmark 公开宣称 **25 → 16 round-trips**(excalidraw),**−26%** 聚合(深、多跳任务)—— 但**同时公布亏**:
- 小仓库浅任务,小研 chalk **−32%** vs express **+59%**(同 repo 类,反向结果)
- gin(110 文件最小) **+4% ≈ 持平**

**Honesty contract**:不发布 benchmark 没给出的节省数字,亏损挨着赢一起发,每个 token claim 都有可执行命令追源。`openlore prove --estimate`(秒级、无 key)在自己的仓库里预测 orientation tax。

## 工程态度(摘自 `docs/PHILOSOPHY.md`)

> "Archaeology over Creativity"

只记录代码事实,不发明意图。生成 spec 时必须每条 requirement 都能追到一段代码(Evidence 字段)。当代码行为不明确时,显式标 `Confidence: Low` 或 `needs verification`。**Incomplete is better than wrong**。

## 与 vault 已有页面的关系

- **vs [[concepts/claude-mem-memory-architecture]]**:claude-mem 用 hook 捕获工具调用 → haiku 压缩成 observation → 存 SQLite+Chroma。OpenLore 用 **静态分析 + 图算法**,**完全不动 LLM**。两者互补:claude-mem 补 session 间的**经验记忆**,OpenLore 补**代码结构记忆**。
- **vs [[concepts/agent-operating-system]]**:AOS 五层 memory 框架的"Knowledge Memory"层是 OpenLore 的目标地。
- **vs [[entities/treehouse]]**:treehouse 提供"agent 在哪里写"——worktree 池;OpenLore 提供"agent 该写哪里"——静态分析 orient。两者都是 AI agent 的本地基础设施 runtime,互不重叠,常组合使用。
- **vs [[concepts/design-system-as-ai-context]]**:DESIGN.md 把设计系统升级为 agent 硬约束;OpenLore 把代码结构升级为 agent 硬约束。同一种思路的不同对象。

## 演进摘要(CHANGELOG 关键节点)

- 早期:5 阶段 pipeline(init → analyze → generate → verify → drift)反向工程 OpenSpec
- v2.x:加入 ADR、决定(decision)生命周期、cross-domain impact、structural change analysis、architecture invariants(SPEC 23)、governance dogfooding(SPEC 15)、lean tool surface(SPEC 28 → 默认 substrate 13 tools)
- 当前:**hot path 0 LLM**, 默认 substrate preset,BM25 fallback 无 embedding 也能跑,watch mode 默认开

## 引用

- 仓库:<https://github.com/clay-good/OpenLore>
- npm:<https://www.npmjs.com/package/openlore>
- 原始抓取:`_raw/_archived/github-clay-good-OpenLore.txt`
- 设计哲学:`docs/PHILOSOPHY.md`(本文档最值得引用的 41 行)
- MCP 工具清单:`docs/mcp-tools.md`
- 算法细节:`docs/ALGORITHMS.md`
- Benchmark 公开数据:`docs/AGENT-BENCHMARKS.md`