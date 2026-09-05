---
title: 静态分析驱动的代码知识图谱
category: concepts
tags:
  - static-analysis
  - knowledge-graph
  - code-archaeology
  - ai-agent
  - openlore
  - rag
sources:
  - https://github.com/clay-good/OpenLore
  - _raw/_archived/github-clay-good-OpenLore.txt (gitingest export, clay-good/OpenLore, 2026-08-03)
created: 2026-08-03T12:10:00Z
updated: 2026-08-03T12:10:00Z
summary: 用 import/导出 + 函数签名 + 控制流 + IaC 声明构建仓库级知识图谱(call graph / types / tests / decisions / specs),不依赖 LLM,确定性可重放,可 query 也可 evaluate。
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
  - target: "[[entities/openlore]]"
    type: derived_from
  - target: "[[concepts/deterministic-agent-memory]]"
    type: related_to
  - target: "[[concepts/no-llm-hot-path]]"
    type: related_to
  - target: "[[concepts/commit-gate-guardrails]]"
    type: related_to
  - target: [[concepts-agent-operating-system × concepts-deterministic-agent-memory]]
    type: related_to
---

# 静态分析驱动的代码知识图谱

> 用图算法替代 embedding 做代码检索与定位 —— 同一仓库每次重跑结果完全一致,无需 GPU / 无需 token。

## 一句话定义

把仓库编译(分析)成一张**确定性可重放**的图:节点是文件 / 函数 / 类 / 类型 / IaC 资源 / spec requirement,边是 import / call / extends / implements / test-covers / spec-traces-to,再用图算法算出 hub / 入口 / 死代码 / 影响半径 / 决策轨迹。

## 节点与边(参考 OpenLore 的统一结构性子基)

```text
节点类型                  边类型
─────────────────       ───────────────────────────
File (path)             file-contains → Function
Function (sig+body)     function-calls → Function
Class                   class-extends → Class
Type / Interface        function-defines → Symbol
Test                    test-covers → Function
Spec Requirement        spec-traces-to → Function (via Evidence)
Decision (ADR)          decision-concerns → Module
IaC Resource            resource-managed-by → Module
HTTP Route              route-handled-by → Function
ORM Schema              schema-field-of → Table
```

输出:JSON 文件树(`.openlore/analysis/...`) + `llm-context.json` 主索引,gitignorable,删了不影响仓库。

## 关键算法(确定性,无 LLM)

### 1. 文件 significance scoring(用于把高价值文件喂给后续步骤)

```
TotalScore = NameScore + PathScore + StructureScore + ConnectivityScore
```

| 维度 | 范围 | 关键特征 |
|---|---|---|
| Name | 0-30 | `schema/model/entity`=30、`service/controller/handler`=28、`util/helper`=10、`test/spec`=5 |
| Path | 0-25 | `src/models`=25、`src/services`=23、`test/`=5 |
| Structure | 0-25 | class 定义 +5、interface +3、function exports +2(各项有 max)|
| Connectivity | 0-20 | import/export 关系,高 in-degree 加分 |

### 2. 依赖图 + PageRank 风格 importance

```
PR(A) = (1-d) + d × Σ(PR(T) / OutDegree(T))     # d = 0.85,~20 iterations 收敛
```

+ **In-degree / Out-degree**:hub vs orchestrator 判定
+ **Betweenness centrality**:模块间桥梁
+ **Tarjan SCC**:循环依赖检测

### 3. Domain clustering(Louvain-style modularity)

```
Q = (1/2m) × Σ[(Aij − kikj/2m) × δ(ci, cj)]
```

启发式增强(对代码):

- 同目录文件 +affinity bonus
- 共享命名约定 +affinity
- 双向 import = 强同域

### 4. 上下文窗口裁剪(给 LLM 的"配菜"用)

```python
def select_files(files, limit):
    selected, tokens = [], 0
    for f in sorted(files, key=lambda f: -f.score):
        if tokens + count_tokens(f.content) <= limit:
            selected.append(f); tokens += count_tokens(f.content)
    return selected
```

超长文件保留 imports/exports/signatures,截断 body,标 `// ... implementation ...`。

## 为什么用图而不用 embedding

| 维度 | 静态分析图 | 向量 embedding |
|---|---|---|
| 确定性 | 同一仓库每次一致 | 取决于模型权重 / 服务可用性 |
| 成本 | 本地 CPU,毫秒 | API token / GPU 时 |
| 网络依赖 | 无 | embedding 服务在线才完整 |
| 失败模式 | 显式 unresolved / stale | 静默给"看起来对"的近邻 |
| 可证伪 | 每条边可追到源码 | 隐式向量,不可回放 |
| 大型 monorepo | 分钟级一次性构建 | 持续 API 费用 |

OpenLore 的选择:**图是骨架,embedding 是可选配菜**(`search_code` / `orient` 无 embedding 时 BM25 兜底)。

## 增量更新(SPEC 13.1:watch mode)

MCP server 默认开 `--watch-auto`,每次 file save:

1. 合并到 batched flush(`--watch-debounce 400ms`)
2. 改了的签名直接进 MCP read cache(下一次调用即 cache hit)
3. vector index 用 row-level ops(不全表重写)
4. bulk event(branch switch / rebase / formatter)折叠成一次 refresh
5. **call graph 反向依赖闭包**:改了 A → 重算 A 的 direct callers + 之前 unresolved 现在该绑定的潜在 callers
6. **有界预算** `INCREMENTAL_CLOSURE_BUDGET`(默认 40 文件);超出预算的"未重算文件"标记为**显式 stale**,freshness verdict 永远非 silent wrong
7. `openlore analyze --force` 全量重建,清 stale 标记

大仓(>5000 源文件)live embedding 自动降级到 signature-only,embeddings commit 时再刷。

## 应用接口(`orient()`)

```json
{
  "relevantFiles": ["src/.../blast-radius.ts", "src/.../mcp-handlers/blast-radius.ts"],
  "relevantFunctions": [{
    "name": "computeBlastRadius",
    "signature": "async function computeBlastRadius(input: BlastRadiusInput): Promise<BlastRadiusBriefing>",
    "fanIn": 5, "isHub": true, "language": "TypeScript"
  }],
  "callPaths": [{"function": "computeBlastRadius", "callers": ["handleBlastRadius", "computeImpactCertificate", ...]}],
  "insertionPoints": [{"rank": 2, "name": "computeBlastRadius", "role": "hub", "strategy": "cross_cutting_hook", "reason": "called by 5 functions"}],
  "suggestedTools": ["record_decision", "analyze_impact", "get_subgraph", "check_spec_drift"]
}
```

每个字段都从图算出来,**不靠模型推断**。

## 失败的常见反模式

- ❌ 用 git grep 替代图分析 —— 找不到"这个函数被哪些路径调用"
- ❌ 用向量检索替代图分析 —— 静态导出变更悄无声息
- ❌ 把 graph 当 LLM 上下文传 —— 浪费 token,LLM 还会"在图之外发明"
- ❌ 图算法里塞 transformer embedding —— 失去确定性,benchmark 无法重现
- ❌ watch mode 不设 stale 边界 —— hub 文件编辑后 silent wrong

## 适用场景

- AI 编码 agent 在**陌生 / 大型 / 多语言**仓库里**首个动作**
- CI / pre-commit 上做 spec coverage check
- 老项目 review / 重构前的依赖结构可视化
- 私有代码(模型从未训练过)+ polyglot IaC

## 与 vault 已有页面的关系

- 实现:[[entities/openlore]]
- 配套原则:[[concepts/deterministic-agent-memory]]、[[concepts/no-llm-hot-path]]
- 落地到 CI:[[concepts/commit-gate-guardrails]]
- 上层:[[concepts/agent-operating-system]] Knowledge Memory 层
- 并列 runtime:[[entities/treehouse]] 解决"在哪写",OpenLore 解决"该写哪"