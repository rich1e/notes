---
title: Hot path 不放 LLM — 确定性 + 可选增强
category: concepts
tags:
  - ai-architecture
  - ai-agent
  - hot-path
  - determinism
  - openlore
  - safety
sources:
  - https://github.com/clay-good/OpenLore
  - _raw/_archived/github-clay-good-OpenLore.txt (gitingest export, clay-good/OpenLore, 2026-08-03)
created: 2026-08-03T12:20:00Z
updated: 2026-08-03T12:20:00Z
summary: 把昂贵 / 非确定性 / 依赖网络的 LLM 调用挪出 hot path(每次 agent 都跑):确定性算法跑 hot,LLM 只在生成 / 验证 / 整合等冷路径 opt-in 介入。
tier: supporting
lifecycle: draft
lifecycle_changed: 2026-08-03
base_confidence: 0.85
provenance:
  extracted: 0.95
  inferred: 0.05
  ambiguous: 0
relationships:
  - target: "[[entities/openlore]]"
    type: derived_from
  - target: "[[concepts/deterministic-agent-memory]]"
    type: extends
  - target: "[[concepts/static-analysis-knowledge-graph]]"
    type: related_to
  - target: "[[concepts/claude-mem-memory-architecture]]"
    type: related_to
---

# Hot path 不放 LLM — 确定性 + 可选增强

> OpenLore 设计原则:把 LLM 调用完全移到 cold path(generate / verify / consolidation),hot path(每次 agent 操作都跑的工具)全部确定性。

## 一句话定义

hot path = agent **每次会话每次任务**都会走的那条路(orientation / search / call graph query / impact analysis / freshness check)。LLM 一旦出现在 hot path,**每次任务都要付 token + 每次都拿"看起来对"的概率性回答**——这是性能 + 安全双输。

## 三个区分

| 路径 | 触发频率 | 理想特性 | OpenLore 的实现 |
|---|---|---|---|
| **Hot path** | 每个任务 N 次 | 确定性 + 廉价 + 离线 | 静态分析图 + BM25 + 签名比对 + git diff |
| **Cold path**(可选) | 项目级一次或人工触发 | 可消耗 token、引入语义理解 | `generate` (LLM spec 抽取) / `verify` / `consolidate` |
| **Decision gate** | commit 时一次 | 显式 yes/no + Evidence | `certify_public_surface` / `change_impact_certificate` |

OpenLore 的 `docs/ci-cd.md` 直接列了对照表:

```text
            | Deterministic (Default) | LLM-Enhanced
API key     | No                       | Yes
Speed       | Milliseconds             | Seconds per LLM call
Commands    | analyze / drift / init   | generate / verify / drift --use-llm
Reproducibility | Identical every run | May vary
Best for    | CI / pre-commit / quick  | Initial generation / 减少 false positive
```

## 为什么 hot path 必须确定性

### 成本维度

一个中型 monorepo 的 agent 任务,可能调用 `orient` + `search_code` + `analyze_impact` + `find_path` 数十次。如果每次都走 LLM:

- 单次 LLM 调用 ~1-3 秒、$0.001-0.01
- 一个 session 几十次 = 几十秒延迟 + 几美元
- 月度量 100-1000 倍

### 可靠性维度

- LLM 输出不可重放,benchmark 无法复现
- "X 函数在 /src/foo.ts" 这种**事实问题**容错率为 0;概率回答 = 必然某次错
- model upgrade / model swap 让旧 benchmark 失效

### 离线能力

- airplane mode、保密环境、CI 无网络 —— hot path 挂 = 全员停摆
- LLM 服务 down = agent 全瘫

### 安全 / 诚实

- agent 拿到 LLM "X 是 dead code" 这种含糊回答会自信地改,review 时一起赔
- 确定性工具的失败是显式的(stale / unresolved / no-evidence),agent 必须回去查

## OpenLore 的具体实现

### 1. Watch mode 默认开,**纯本地增量更新**

```
per-file save → batched flush(400ms debounce)→ patched signatures 直接进 MCP read cache
                → vector index row-level ops(全表 rewrite 不需要)
                → call graph 反向依赖闭包重算
                → 超过 INCREMENTAL_CLOSURE_BUDGET(40 files)→ 显式 stale
```

零 API key、零网络、毫秒级。

### 2. 无 embedding 时 BM25 自动兜底

`search_code` / `orient` / `suggest_insertion_points` 在没配 embedding 服务时自动降级到 BM25 + 签名级 matching。结果弱于 embedding,但**确定 + 离线 + 0 成本**。

### 3. capability family 隔离

`--preset navigation`(10 tools)/ `--preset substrate`(13,默认) / `--preset memory` / `--preset full`(73 tools)。

每次 MCP `tools/list` 客户端会取全部 tool schema。默认 `substrate` 让 schema prefix ~22k tokens → 优化后大幅缩小。schema 顺序固定、deterministic,provider KV-cache 可命中。

### 4. Optional LLM 走冷路径

- `record_decision`:consolidation 阶段可 LLM,失败 fallback 到 git diff extractor
- `drift --use-llm`:LLM-based semantic filter(可选)
- `generate` / `verify`:**必须** LLM,且只跑一次(项目级)

LLM 从不在 hot path,但 cold path 可用,绝不被强制。

## 反面:LLM 在 hot path 的危害

| 症状 | 后果 |
|---|---|
| 每次 `orient()` 都调 LLM | 单次 1-3 秒 × N 次/任务 = agent 慢 + token 烧 |
| LLM "X 在 src/foo.ts" 报错位置 | agent 编辑失败 / 文件不存在 |
| LLM 答不出报"可能 stale" | agent 不知道是真 stale 还是 LLM 不会 |
| LLM 服务 down | hot path 全瘫,CI 红屏 |
| benchmark 不可重放 | 模型一升,赢变亏,无法 A/B |
| 私有代码 + LLM | 保密违规,法律风险 |

## 推广:任何"agent infra 工具"的 hot path 准则

```text
[ ] hot path 不调 LLM
[ ] hot path 不调外网(API / SaaS)
[ ] hot path 同一 query 同答案
[ ] hot path 每次 < 100ms(本地算)
[ ] 显式失败语义(stale / not-found / unresolved)
[ ] LLM 只在 cold path opt-in,且必须 fallback 到无 LLM 路径
[ ] schema / 描述输出 deterministic,顺序固定 → KV-cache 友好
[ ] benchmark 在模型升级后仍可重放
```

## 与 vault 已有架构的关系

- **claude-mem**:PostToolUse **async** hook(不阻塞主交互)+ 失败可降级 + 本地 SQLite / Chroma——已经是 async 旁路而非 hot path 阻塞。OpenLore 是把同一原则推到更底层(graph)。
- **treehouse**:`get --lease` / `prune` / `destroy` 全是 hot path 操作,纯文件系统,无网络依赖。同源思路。
- **agent-os 五层**:Knowledge Memory 层应该是确定性 fact layer(OpenLore);Semantic Memory 可以是 claude-mem 这种轻量概率层;二者在 hot/cold 上的取舍不同。

详见 [[concepts/deterministic-agent-memory]] 与 [[concepts/static-analysis-knowledge-graph]]。

## 相关

- [[entities/openlore]] —— 实现
- [[concepts/deterministic-agent-memory]] —— 为什么这层必须是确定性
- [[concepts/static-analysis-knowledge-graph]] —— hot path 的算法骨架
- [[concepts/commit-gate-guardrails]] —— decision gate 在 hot/cold 之间
- [[concepts/claude-mem-memory-architecture]] —— 异步概率记忆的互补方案
- [[concepts/agent-operating-system]] —— 五层框架
- [[entities/treehouse]] —— 同思路的另一基础设施