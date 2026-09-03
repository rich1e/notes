---
title: OpenLore CLI 日常用法
category: skills
tags:
  - cli
  - openlore
  - ai-agent
  - static-analysis
  - mcp
  - commit-gate
sources:
  - https://github.com/clay-good/OpenLore
  - _raw/_archived/github-clay-good-OpenLore.txt (gitingest export, clay-good/OpenLore, 2026-08-03)
created: 2026-08-03T12:30:00Z
updated: 2026-08-03T12:30:00Z
summary: OpenLore 命令速查:install/orient/review/prove/enforce/mcp/drift,核心 MCP 工具族(navigate/change/remember/verify/coordinate/federate),6 capability family,substrate preset 默认。
tier: peripheral
lifecycle: reviewed
lifecycle_changed: 2026-09-03
lifecycle_reason: "auto-promoted by wiki-lint --consolidate: age>30d, confidence>0.9"
lifecycle_changed: 2026-08-03
base_confidence: 0.9
provenance:
  extracted: 0.96
  inferred: 0.04
  ambiguous: 0
relationships:
  - target: "[[entities/openlore]]"
    type: derived_from
  - target: "[[concepts/static-analysis-knowledge-graph]]"
    type: related_to
  - target: "[[concepts/deterministic-agent-memory]]"
    type: related_to
  - target: "[[concepts/no-llm-hot-path]]"
    type: related_to
  - target: "[[concepts/commit-gate-guardrails]]"
    type: related_to
  - target: "[[skills/treehouse-cli]]"
    type: related_to
---

# OpenLore CLI 日常用法

> 单 page cheat-sheet,涵盖安装、analyze/orient/MCP/preset/治理三件套/commit gate。底层概念见相关 concept 页。

## 安装

| 渠道 | 命令 |
|---|---|
| npm(推荐)| `npm install -g openlore && openlore install` |
| Homebrew | `brew install openlore` |
| npx | `npx openlore init` |
| Nix | flake 输入 `github:clay-good/OpenLore` |
| 从源码 | `git clone` + `npm install && npm run build` |

`openlore install` 是单命令开箱:自动检测 agent(Claude Code / Cursor / Cline / Continue / AGENTS.md)、注册 MCP server、构建本地 BM25 索引(`node_modules/` / `dist/` / `target/` 自动 prune)。无 API key,无 config,无问题。

## 一次性命令

```bash
openlore install --no-analyze   # 只 wire,索引以后建
openlore install --dry-run      # 预览所有改动不写
openlore doctor                 # 检查 config / index / MCP / embeddings
openlore features               # 列出所有可选能力(embeddings / commit gate / spec store / ...)是否启用、一行启用命令
openlore update                 # 升级(检测 npm / Homebrew / npx)
```

## 仓库内命令(`cd <repo>`)

```bash
openlore init                   # 写 .openlore/ 配置
openlore analyze                # 全量静态分析
openlore analyze --force        # 强制重算(清 stale)
openlore drift                  # dry-run 报 spec 覆盖 gap
openlore drift --yes            # 真应用变更
openlore prove --estimate       # 在自己仓库预测 orientation tax(秒级、无 key)
openlore prove                  # 跑完整 WITH/WITHOUT 测(需 claude + key)
openlore prove --json --markdown # 粘贴到 README 的 scorecard + badge
openlore enforce                # commit gate,只拦标了 blocking 的 finding
openlore review                 # 检视当前 diff 是否撞已声明约束
```

## MCP server

```bash
openlore mcp                    # stdio MCP,默认 substrate preset (13 tools)
openlore mcp --preset navigation  # 10 tools 极简导航
openlore mcp --preset substrate   # 默认,导航 + governance reads
openlore mcp --preset minimal     # + commit gate writes
openlore mcp --preset full        # 全部 73 tools
openlore mcp --watch-auto         # 默认开,watch + 增量更新
openlore mcp --no-watch-auto      # 一次性 CLI,不开 watcher
openlore mcp --watch-debounce 400 # ms 静默延迟(默认 400)
```

### Claude Code 注册

在项目根写 `.mcp.json`:

```json
{
  "mcpServers": {
    "openlore": {
      "command": "openlore",
      "args": ["mcp", "--watch-auto"]
    }
  }
}
```

Claude Code 支持 `alwaysLoad: false`(deferred schema),推荐用 —— 73 tools 不付 schema 成本,只在使用时加载。

## 6 capability family + 默认 substrate

```text
navigate   | 读结构/spec 图返回结论         | orient / find_path / analyze_impact / select_tests / find_dead_code
change     | 推演某次 diff 的影响          | structural_diff / blast_radius / change_impact_certificate / certify_public_surface
remember   | 记录/取回 code-anchored 事实 | remember / recall / record_decision
verify     | 在断言触达人类之前裁决         | verify_claim
coordinate | 并行任务的排程与冲突消解       | plan_parallel_work / map_in_flight_conflicts
federate   | 跨仓库 / spec store           | federation_status / spec_store_status / working_set_context
```

每个工具在描述里点其"近邻兄弟",CI guard `tool-contract.test.ts` 在漏声明时 fail。

## 必知 5 个 MCP 工具

### `orient(task)`

**任何新任务的首个调用**。一次返回:relevant files、relevant functions、call paths、insertion points、matching specs、`suggestedTools` 下一调用清单。

```text
orient("add a payment method")
→ 一次拿到要碰哪些函数、调用链、contract、spec 段、推荐下个工具
```

### `search_code(query)`

自然语言语义检索;无 embedding 时 fallback BM25。返回带 call-graph 邻居和 spec-linked peer functions。

### `analyze_impact(symbol)`

从某函数/类出发的影响半径;同时给 "scope this diff" 形态给"这次改动会触碰哪些下游"。

### `verify_claim(claim, evidence)`

返回 `confirmed / refuted / unverifiable` + Evidence。挡住 agent "X 是 dead code" 这种猜测。

### `blast_radius(symbol, changeSet)`

更精细的影响分析 —— 给"tests to run"清单 + "consumers this change breaks, by name"。

## 治理三件套(commit 前必查)

| 工具 | 用法 |
|---|---|
| `certify_public_surface(changedExports)` | 分类 `breaking / non-breaking / potentially-breaking`,**点名被破坏的 consumer**;保守,绝不悄悄"safe" |
| `change_impact_certificate(fromPath, toPath)` | diff **打开新路径**到敏感边界时报警(改后可达,改前不可达)|
| `verify_claim(claim, evidence)` | `confirmed / refuted / unverifiable` + 引用 |

外加 CLI:`openlore enforce` = commit gate,默认 advisory,只拦 `blocking` finding。

## pre-commit 双 hook

```bash
openlore drift --install-hook     # A:drift gate(代码改了 spec 没改)
openlore setup --tools claude     # B:decision gate + Claude Code skills
openlore drift --uninstall-hook
openlore decisions --uninstall-hook
```

二者关注点正交:**drift = spec coverage staleness,decisions = 决策审批**。一个 commit 可同时撞两者失败。

## 架构不变量(`check_architecture`)

`.openlore/architecture.json`:

```json
{
  "layers": {
    "cli":  ["src/cli"],
    "core": ["src/core"],
    "utils": ["src/utils"]
  },
  "forbidden": [
    { "from": "src/core", "to": "src/cli", "reason": "core stays UI-agnostic" }
  ],
  "allowedOnly": [
    { "module": "src/api", "mayDependOn": ["src/core", "src/types"] }
  ]
}
```

3 种规则:`layers`(有序 layer,下层依赖上层 = violation)、`forbidden`({from, to, reason})、`allowedOnly`({module, mayDependOn[]})。

pre-edit query:

```jsonc
check_architecture({ directory, from: "src/core/thing.ts", to: "src/cli/view.ts" })
// → { allowed: false, rule: { kind: "forbidden", reason: "..." }, reason: "..." }
```

未声明规则时**完全 inert**。

## Cline / Roo Code / Kilocode slash command

```bash
mkdir -p .clinerules/workflows
for cmd in analyze-codebase check-spec-drift plan-refactor execute-refactor implement-feature refactor-codebase; do
  curl -sL "https://raw.githubusercontent.com/clay-good/openlore/main/examples/cline-workflows/openlore-${cmd}.md" -o ".clinerules/workflows/openlore-${cmd}.md"
done
```

## 常见故障

### `orient()` 报"index stale"

文件改了但分析没更新。`openlore analyze --force` 或确认 MCP 启动了 `--watch-auto`。

### `search_code` 结果很弱

大概率是 BM25 兜底(没配 embedding)。要 embedding 走:`openlore features` 看启用命令(可能要本地 embedding server 或 opt-in 上云)。

### pre-commit hook 不触发

确认装了 `openlore drift --install-hook` + `openlore setup --tools claude`;若用 `git commit --no-verify`,post-commit 会报警。

### MCP server schema prefix 太大

73 tools 在客户端 `tools/list` 一次发完 ~22k tokens。两种解法(按优先度):
1. **Deferred schemas**:Claude Code 支持 `alwaysLoad: false`,把 tool 名字先返回,schema 用时再发
2. **`--preset navigation`** 降到 10 tools 极简导航

### decision gate 报 `drafts_pending_consolidation`

agent 调 `record_decision` 但 consolidation 没在 background 跑完。`openlore decisions --consolidate --gate` 立即跑。

### drift gate 误报

`openlore drift --domains auth,user` 限定只审特定 domain;或先 `--fail-on warning` 不 fail,看清楚 finding 再调规则。

## 私有仓库 + 保密环境

OpenLore 默认:
- 不打网络(API key 不需要)
- 不传源码到任何服务
- 不开遥测(opt-in only)
- `.openlore/` 目录 gitignorable,删了不影响仓库

适合 airgapped / 私有 / 模型未训过的代码。`openlore features` 看哪些 opt-in 能力能关。

## 相关

- [[entities/openlore]] —— 实现总览
- [[concepts/static-analysis-knowledge-graph]] —— 算法骨架
- [[concepts/deterministic-agent-memory]] —— 确定性 fact layer 原则
- [[concepts/no-llm-hot-path]] —— hot/cold 路径划分
- [[concepts/commit-gate-guardrails]] —— CI/pre-commit 拦截范式
- [[skills/treehouse-cli]] —— 同为 AI agent 本地基础设施 CLI 速查;treehouse 管"在哪写"(worktree 池),OpenLore 管"该写哪里"（静态分析 orient）