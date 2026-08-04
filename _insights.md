# Wiki Insights — 2026-08-04T12:40:00Z

> KG 范围:仅统计 concepts/entities/skills/references/synthesis/journal/projects/misc/sources 九类图谱页(共 273),排除 `.obsidian/`、`buckets/`、`Clippings/`、`Chronicle/`、`Dashboard/`、`_raw/`、`_archives/` 等聚合/daily/系统文件。`obsidian-wiki graph-analyse` 全库口径为 1176 nodes / 4565 edges / 545 communities(含 daily bucket + Clippings,不代表 KG 结构),故 hub/tier 分析以 KG 手算口径为准。

## 核心结论(针对 ~319K token footprint)

⚠️ **降 tier 减 token 这条路当前走不通。** 硬规则「demote:in≤1 AND 90d+ 未更新」下 **0 个合规候选** —— vault 全部内容 < 90 天(最早 7 月),没有可安全降级的 stale 长尾。

真正的图谱信号恰好**相反**:**100+ 个页 in≥5 却仍标 supporting**,这才是 143 个 supporting 页 / ~167K token 的成因。但全升 core 会让 core tier 失去筛选意义。**结论**:token 优化应改走 wiki-query fast mode / 索引优先,而非 tier 降级(详见末尾建议)。

## Anchor Pages(KG top 12 hubs)

| Page | In | Out | Note |
|---|---|---|---|
| [[concepts/agent-operating-system]] | 33 | 11 | connector hub(core ✓) |
| [[entities/chezmoi]] | 30 | 16 | connector hub(core ✓) |
| [[entities/zustand]] | 29 | 7 | core ✓ |
| [[concepts/claude-mem-memory-architecture]] | 28 | 6 | core ✓ |
| [[entities/google-stitch]] | 28 | 11 | connector hub(core ✓) |
| [[concepts/swiftui-framework]] | 28 | 13 | connector hub(core ✓) |
| [[concepts/mcp-server-protocol-quirks]] | 26 | 5 | 偏 sink hub(core ✓) |
| [[concepts/dotfile-manager]] | 25 | 11 | connector hub(core ✓) |
| [[concepts/ptp-ieee1588]] | 25 | 9 | core ✓ |
| [[concepts/design-system-as-ai-context]] | 24 | 8 | core ✓ |
| [[skills/claude-code-token-optimization]] | 23 | 6 | core ✓ |
| [[entities/treehouse]] | 23 | 6 | **tier=supporting → 建议升 core** |

Top 11 已全是 core,健康。唯一漏网的顶层枢纽是 `treehouse`(in=23)。

## Tag Cluster Cohesion

### 最凝聚(well-linked)
- **#openlore** — 7 页,cohesion **1.000**(全互链)
- **#treehouse** — 8 页,cohesion **0.964**
- **#worktree** — 8 页,cohesion 0.750
- **#memory** — 6 页,cohesion 0.733
- **#f2e** — 7 页,cohesion 0.667

### 最碎片化(cross-linker 目标)
- **#synthesis** — 6 页,cohesion 0.000 ⚠️ —— synthesis 报告是终端节点,天然不互链,**属正常,无需 cross-linker**

19 个 n≥5 的 tag 里只有 #synthesis 落在 <0.15,且是良性。tag 结构整体健康。

## Surprising Connections(KG 跨类目)

- [[concepts/agent-operating-system]] × [[concepts/ai-agent]] → [[concepts/ai-tool-specialization]] — score 0.71,合成页向工具专精概念的外延
- [[entities/gpakosz-tmux]] 跨簇进入 tmux 概念群 — 8 月新 ingest 把 gpakosz 簇接入 skills/tmux 主干

## Graph Delta(对比 2026-08-03T16:25 快照)

- **口径变化**:上次 KG 327 页 → 本次 273 页(差异主要是清理了 daily bucket 混入 + `_raw/` 归档,不是删知识页)
- **hub 排名重排**:上次顶 hub 是 mcp-server-protocol-quirks(40 in),本次 agent-operating-system 升至第一(33 in)—— mcp-quirks 的入链下降反映 daily bucket 页被移出 KG 口径
- **新连接**:gpakosz-tmux 簇(8 页)、Ar9av/obsidian-wiki 自指 3 页已并入图谱
- **无丢失入链**告警(consolidation 修复的双前缀断链已复挂)

## Tier Suggestions

**升 core(选择性,只列真枢纽 in≥14 且当前 supporting/unset)**:

```
↑ core  [[entities/treehouse]]                        — in=23, tier=supporting
↑ core  [[concepts/safe-destroy-by-default]]          — in=19, tier=supporting
↑ core  [[concepts/worktree-durable-lease]]           — in=19, tier=supporting
↑ core  [[concepts/git-worktree-pool-pattern]]        — in=18, tier=supporting
↑ core  [[skills/claude-code-mcp-auth-patterns]]      — in=17, tier=supporting
↑ core  [[concepts/atomic-state-recovery]]            — in=16, tier=supporting
↑ core  [[concepts/zustand-middleware-system]]        — in=15, tier=supporting
↑ core  [[concepts/claude-code-hooks-lifecycle]]      — in=14, tier=supporting
↑ core  [[entities/claude-mem]]                       — in=14, tier=supporting
↑ core  [[entities/sebastienrousseau-dotfiles]]       — in=14, tier=supporting
↑ core  [[concepts/zustand-core-architecture]]        — in=14, tier=supporting
↑ core  [[concepts/static-analysis-knowledge-graph]]  — in=14, tier=supporting
↑ core  [[concepts/workflow-automation-platform]]     — in=14, tier=supporting
↑ core  [[entities/gpakosz-tmux]]                     — in=14, tier=supporting
```

> in 5-13 之间还有 ~80 页也满足「≥5 incoming」的宽松 promote 门槛,但为保 core tier 的筛选意义,**建议只升 in≥14 的 14 个真枢纽**。全部升 core 反而稀释 tier 语义。

**降 peripheral**:**0 个合规候选**(硬规则需 in≤1 AND 90d+ stale;vault 全部 <90 天)。

## Questions Worth Asking

1. **Link:** `concepts/asciidoc-markup` 有 0 入链(Clippings 产物)—— 哪个页该引用它?或它是否该合入 markdown 相关概念页?
2. **Audit:** 143 个 supporting 页里 100+ 个 in≥5 —— tier 门槛是否需要重定义(例如 in≥10 才 core,in 3-9 才 supporting,in<3 才 peripheral)?
3. **Explore:** `agent-operating-system` 为何成为跨 AI-agent / MCP / worktree 三簇的第一枢纽?
4. **Resolve:** #synthesis 的 0 cohesion 是终端节点特性,是否该把 synthesis 页排除出 tag cohesion 统计口径?

<!-- GRAPH_SNAPSHOT: {"run":"2026-08-04T12:40:00Z","full_pages":1176,"full_edges":4565,"kg_pages":273,"top_hubs":[["concepts/agent-operating-system",33,11],["entities/chezmoi",30,16],["entities/zustand",29,7],["concepts/claude-mem-memory-architecture",28,6],["entities/google-stitch",28,11],["concepts/swiftui-framework",28,13],["concepts/mcp-server-protocol-quirks",26,5],["concepts/dotfile-manager",25,11],["concepts/ptp-ieee1588",25,9],["concepts/design-system-as-ai-context",24,8]],"tier_promote_in14plus":14,"tier_demote":0} -->
