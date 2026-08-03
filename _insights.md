# Wiki Insights — 2026-08-03T16:25:00Z

> KG 范围:仅统计 concepts/entities/skills/references/synthesis/journal/projects/misc/sources 九类图谱页(共 327),排除 `.obsidian/`、`buckets/`、`Clippings/`、`Chronicle/`、`Dashboard/` 等聚合/daily/系统文件。

## Anchor Pages (top 10 hubs)

| Page | In | Out | Note |
|---|---:|---:|---|
| [[concepts/mcp-server-protocol-quirks]] | 40 | 8 | connector hub — Claude Code + Stitch 的鉴权/作用域陷阱集 |
| [[concepts/agent-operating-system]] | 37 | 22 | connector hub — AOS 五层记忆 |
| [[concepts/claude-mem-memory-architecture]] | 35 | 8 | connector hub — 6 hook 流水线 |
| [[entities/chezmoi]] | 34 | 21 | connector hub — dotfile 哲学锚点 |
| [[entities/google-stitch]] | 34 | 15 | connector hub — DESIGN.md 出处 |
| [[entities/zustand]] | 32 | 10 | connector hub — React 状态管理 |
| [[concepts/swiftui-framework]] | 30 | 18 | connector hub — iOS/Swift 簇 |
| [[concepts/design-system-as-ai-context]] | 30 | 13 | connector hub — DESIGN.md 抽象 |
| [[entities/ios17-app-development-book]] | 20 | 25 | connector hub — Swift 书 + 多合成 |
| [[synthesis/Research: Kimi K3]] | 10 | 35 | source-heavy hub — K3 唯一综合页 |

> 注:hub 排名按无向 degree in + out。MCP-quirks 入链最高(40),但 AOS 同时高入链 + 高出链是最强 connector。
> Kimi K3 综合页"入链 10 / 出链 35"是典型"综合页"形态——汇聚各方入链,反向引用多个原页。
> **vs 2026-07-31 上轮**:hub 排名从 swiftui-framework/dotfile-manager(16 in)提升到 MCP-quirks/AOS(40/37 in),反映 8 月新增的 ingest(OpenLore / treehouse / gpakosz)与 4 个合成页把 agent 簇拉到第一阵营。

## Communities (cluster ≥3 kg pages, top 10)

graph 报告 547 簇,但 99% 是单页 daily。kg 簇 25 个,top 10:

| c# | 主题 | size | 代表页 |
|---|---|---:|---|
| c3 | **AI agent 操作系统簇(新)** | 22 | [[concepts/agent-operating-system]], [[concepts/ai-agent]], [[concepts/ai-agent-sandbox]], [[concepts/atomic-state-recovery]], [[concepts/claude-code-hooks-lifecycle]] |
| c2 | **Claude Code 工具栈簇** | 25 | [[concepts/ai-tool-specialization]], [[entities/claude-code]], [[skills/claude-code-mcp-auth-patterns]], [[skills/claude-code-settings]], [[skills/claude-code-token-optimization]] |
| c1 | **iOS 架构 + 文档工具簇** | 29 | [[concepts/arc-memory-management]], [[concepts/asciidoc-markup]], [[projects/dayfold/concepts/core-data-cloudkit-fallback]], [[references/cs193p-spring-2025]] |
| c4 | **chezmoi 完整知识簇** | 21 | [[entities/chezmoi]], [[concepts/chezmoi-attribute-prefixes]], [[references/chezmoi-bitwarden-keychain]], [[skills/chezmoi-bitwarden-secrets]], [[references/chezmoi-encryption-backends]] |
| c5 | **LLM 学习路径簇** | 18 | [[entities/andrej-karpathy]], [[sources/andrej-karpathy-zero-to-hero]], [[concepts/instruction-tuning]] |
| c6 | **PTP / 精确时间协议簇** | 15 | [[synthesis/concepts-ptp-clock-types × entities-white-rabbit]], [[entities/linuxptp]], [[concepts/ptp-bmca]] |
| c8 | **iQue DSi 簇** | 12 | [[entities/ique-dsi]], [[skills/ique-dsi-camera]], [[skills/ique-dsi-parental-control]] |
| c9 | **Kimi K3 + MoE 簇** | 12 | [[concepts/kimi-delta-attention]], [[entities/kimi-k3]], [[references/kimi-k3-geopolitical-context]] |
| c10 | **n8n 工作流自动化簇** | 12 | [[concepts/ai-agent-node-pattern]], [[entities/czlonkowski-n8n-mcp]], [[concepts/fair-code-license]], [[entities/make]], [[entities/n8n]] |
| **c12** | **gpakosz-tmux 簇(新)** | 9 | [[entities/gpakosz-tmux]], [[concepts/tmux-config-importance-override]], [[concepts/tmux-installer-safety-pattern]], [[concepts/tmux-local-override-pattern]], [[skills/tmux-gpakos-config]] |

> 今日 ingest 让 vault **净增 2 个新簇**(c3 agent-OS 簇 + c12 gpakosz 簇),c3 取代上轮 hub 排名成为最大新簇。

## Tag Cluster Cohesion

### 最紧密 ✅

| Tag | Pages | Actual links | Cohesion |
|---|---:|---:|---:|
| `#openlore` | 7 | 15 | **0.714** ✅ |
| `#treehouse` | 8 | 19 | **0.679** ✅ |
| `#memory` | 6 | 9 | 0.600 ✅ |
| `#worktree` | 8 | 14 | 0.500 ✅ |
| `#state-management` | 9 | 16 | 0.444 ✅ |

> 今日 ingest 的 OpenLore(7 页)和 treehouse(8 页)由于是同源同主题同步摄入,**cohesion 高达 0.71 / 0.68** —— 这是新 ingest 的"应有模样":一次 ingest 的多个概念页天然互相引用,无碎片化问题。

### 最松散 ⚠️

| Tag | Pages | Actual links | Cohesion |
|---|---:|---:|---:|
| `#tools` | 7 | 2 | 0.095 ⚠️ |
| `#clippings` | 40 | 0 | 0.000 ⚠️ |
| `#chezmoi` | 12 | 0 | 0.000 ⚠️ |
| `#macos` | 5 | 0 | 0.000 ⚠️ |
| `#synthesis` | 6 | 0 | 0.000 ⚠️ |

> ⚠️ **假阳性较多**:`#chezmoi` 实有大量互链(entities/chezmoi 与 11 个 chezmoi-* 概念页全部双向),但脚本 slug 大小写处理把 `chezmoi` 当独立词组匹配时,**0.0 不反映真实碎片度**。`#clippings` 同理(40 页是 archived clippings,本来就 inbound 1 页被引)。`#synthesis` 6 页"不互链"是因为 synthesis 页本来就该"被引用而不互引",本身是终端节点。
> **真正碎片化** 是 **`#tools`**(7 页仅 2 内链)—— 是个真问题,应触发 cross-linker。

## Surprising Connections

graph 工具给的 surprising_connections 偏噪音(daily + weekly 之间互引)。**本轮最有价值的"非平凡跨层"连接**(手工梳理):

- [[entities/gpakosz-tmux]] ↔ [[concepts/safe-destroy-by-default]] —— cross-layer (entity ↔ concepts),`#treehouse` 设计哲学与 gpakosz installer 都强调"风险 opt-in 而非 blanket force"。
- [[concepts/agent-operating-system]] ↔ [[concepts/ai-agent-sandbox]] ↔ [[concepts/worktree-durable-lease]] —— 三页 7p / 4p / 4p co-occurrence,已在 c3 簇内,并已合成 4 个 synthesis 页(AOS × ai-agent, AOS × ai-agent-sandbox, AOS × worktree-durable-lease, ai-agent × mcp-quirks)。
- [[concepts/mcp-server-protocol-quirks]] ↔ [[entities/google-stitch]] —— 5 页同引,从 Stitch 的 OAuth proxy 鉴权链路反向解释 MCP 协议的鉴权职责分配。

## Orphan-Adjacent (dead-ends near hubs)

> graph 报 dead_ends 数量大(389 个 kg 页),但多数是 daily bucket / clippings / 项目页已被 wikilink 但本身无出链(典型 sink 端)。
> **真正"hub-adjacent 但 0 出链"的页**:本次检测未发现 —— Top 10 hub 都至少有 8 个出链,知识结构健康。

## Graph Delta Since Last Run

| 维度 | 上轮(2026-07-31) | 本轮(2026-08-03) | Δ |
|---|---:|---:|---:|
| KG pages | 237 | 327 | **+90** |
| edges | 1130 | 4514 | +3384 |
| communities | — | 547 | (工具口径) |
| kg-rich communities | — | 25 | — |
| top hub in_degree | 16 | 40 | **+24** |

> edge 数从 1130 → 4514 是 **graph 工具口径变化**:上轮自建统计(只扫 wiki/),本轮 obsidian-wiki 全扫(含 .obsidian/buckets/Clippings/daily)。kg-only 仍稳定增长,但 tool-driven 全扫描揭示更多连接面。

### 新连接(本轮 ingest 引入)

- [[entities/gpakosz-tmux]] ↔ [[concepts/safe-destroy-by-default]] ↔ [[entities/treehouse]] —— 设计哲学互通
- [[entities/openlore]] ↔ [[entities/treehouse]] ↔ [[entities/claude-mem]] —— AI agent 基础设施三件套合成 3 次
- 4 个新合成页: AOS × ai-agent / AOS × ai-agent-sandbox / AOS × worktree-durable-lease / mcp-quirks × google-stitch

## Tier Suggestions

### ↑ Promote to `core` (in ≥5, currently not core)

```
↑ core   [[concepts/agent-operating-system]]              in=37   current=supporting
↑ core   [[concepts/claude-mem-memory-architecture]]      in=35   current=supporting
↑ core   [[entities/chezmoi]]                             in=34   current=unset
↑ core   [[entities/google-stitch]]                       in=34   current=unset
↑ core   [[entities/zustand]]                             in=32   current=unset
↑ core   [[concepts/swiftui-framework]]                   in=30   current=unset
↑ core   [[concepts/design-system-as-ai-context]]         in=30   current=unset
↑ core   [[entities/ios17-app-development-book]]          in=20   current=unset
```

> 这 8 页实际就是 graph 的 Top 10 anchor —— 全都应该 `tier: core`。当前它们 tier=supporting 或 unset,降了 wiki-query 时 hub 页被优先加载的概率。**推荐 batch 应用**。

### ↓ Demote to `peripheral` (in ≤1 AND ≥90d stale)

> **0 页候选** —— vault 整体更新活跃,所有 ≥5 in 的页都在 90 天内有更新。无降 tier 目标。

## Questions Worth Asking

1. **Explore:** gpakosz-tmux 簇(c12, 9 页)与 chezmoi 簇(c4, 21 页)都强调"上游不可改 + 用户层覆写",但走完全不同的实现(gpakosz = shell + tmux source-file, chezmoi = Go + 加密 backend)。这是不是同一个"immutable source + mutable target"模式在 dotfile 工具栈的两次独立收敛?
2. **Resolve:** [[synthesis/Research: DESIGN 工作流]] 因 basename 含 `:` 与空格被 wikilink 解析误判,实际应指向 [[synthesis/Research: DESIGN.md 工作流]] —— 是否需要重命名该页去掉特殊字符?
3. **Audit:** `#tools` 标签(7 页,cohesion 0.095)是真碎片化,应触发 cross-linker 还是直接 tag-normalize 拆为 `cli`/`editor`/`build`?
4. **Link:** [[concepts/frontend-storage-cache]] 在多个 vitepress/sanyue-imghub 关联页有出链,但入链为 0 —— 是否在 `sanyue-imghub` / `vitepress-multilingual-docs` 加 back-link?

---

<!-- GRAPH_SNAPSHOT: {"run":"2026-08-03T16:25:00Z","pages":1170,"edges":4514,"communities":547,"kg_pages":327,"kg_communities":25,"top_hubs":[["concepts/mcp-server-protocol-quirks",40,8],["concepts/agent-operating-system",37,22],["concepts/claude-mem-memory-architecture",35,8],["entities/chezmoi",34,21],["entities/google-stitch",34,15],["entities/zustand",32,10],["concepts/swiftui-framework",30,18],["concepts/design-system-as-ai-context",30,13],["entities/ios17-app-development-book",20,25],["synthesis/Research: Kimi K3",10,35]]} -->