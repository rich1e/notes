---
title: Hot Cache
updated: 2026-08-31T14:00:00Z
---

# Hot Cache

*A ~500-word semantic snapshot of recent activity. Updated after every major write operation.*

## Recent Activity

- [2026-08-31 14:00] WIKI_CAPTURE — darwin-skill 9 维评估实战沉淀，**6 页新建**。**核心**：[[synthesis/darwin-skill-brew-weekly-blog-optimization]]（brew-weekly-blog 从 78.0 → 86.5 的完整两轮记录，0 回滚）+ [[concepts/three-segment-fallback-table]]（从本次实战提炼的「触发条件 / 一线修复 / 仍失败兜底」三段式设计模式，比两列式「症状/解法」多一层决策路径，符合 SkillLens meta-skill failure-mechanism encoding 维度）+ [[concepts/darwin-ratchet-mechanism]]（棘轮机制 + HL-4 触顶信号：连续 2 轮 Δ<2 见好就收，防为凑分增冗余）+ [[skills/darwin-skill-evaluation-rubric]]（9 维速查表 + HL 操作精髓 + 实战数据）+ [[skills/skill-runtime-neutrality-grep]]（Runtime 红线 grep 命令 + 修复模板，P0 gate 项不是可选）+ [[entities/homebrew-weekly-blog-skill]]（brew-weekly-blog 实体页）+ [[journal/2026-08-31-darwin-brew-weekly-optimization]]（本次 session 总结）。**关键发现**：(1) 三段式 fallback 表是 dim3 的核心杠杆；(2) Runtime 红线是隐性 P0 gate,Phase 0 应启动就跑而不是优化后才发现；(3) HL-4 触顶信号在 dim5(具体性)维度最容易误判,要区分真涨分 vs 凑字数。本实战 Round 1 Δ=+7.7 / Round 2 Δ=+0.8 → 触顶 break,**+8.5 是有意义改进**。index.md 已追加 6 条新 wikilink。

## Active Threads

- [2026-08-31 04:27] WIKI_SYNTHESIZE — vault 466 页共现扫描，产 **5 个跨域 synthesis 页**。填补 hot.md 上次 Active Threads 留的两个候补（确定性记忆 × OpenLore），并对 hot Agent Teams 簇（cost/display-modes/race-condition）和 DESIGN.md 簇（format-spec × awesome-design-md）做了深度合成。**(1) [[synthesis/concepts-deterministic-agent-memory × entities-openlore]]** — 哲学 → 实体的成熟路径（概念页 → 参考实现 → 使用 skill → 研究综合 四阶段），OpenLore 是 vault 第一个完整走完的实体；hot.md Active Threads 'openlore × claude-mem' 候补落地为本合成。**(2) [[synthesis/concepts-agent-team-display-modes × entities-claude-code-agent-teams-feature]]** — 5 个 teammateMode 实际是 _隔离域_ 选择（in-process 共享内存 → tmux/iterm2 OS 进程），不是平行 UI；推荐 tmux 因为同时满足可观测性+可介入性。**(3) [[synthesis/concepts-agent-team-cost-overhead × entities-claude-code-agent-teams-feature]]** — 线性扩展成本 × 实验特性门控 = 同一约束方程两侧；3-5 teammates 推荐数字背后是特性能力与经济曲线的拐点，不是软建议。**(4) [[synthesis/concepts-agent-team-race-condition-task-claim × concepts-deterministic-agent-memory]]** — 文件锁是确定性哲学在 _动态调度_ 上的延伸，OpenLore 静态分析（读时确定性）与 Agent Teams task claim（写时确定性）共用文件系统作为协调总线。**(5) [[synthesis/concepts-design-md-format-spec × entities-awesome-design-md]]** — 规范（8 章节）vs 最大下游样本集（74 站点扩展到 11 章节）的校准回路；awesome 列表是规范的 _校准数据源_ 而非单纯参考集合。**8 源页已添加反向链接**（deterministic-agent-memory/openlore/agent-team-cost-overhead/claude-code-agent-teams-feature/agent-team-display-modes/agent-team-race-condition-task-claim/design-md-format-spec/awesome-design-md）。skipped 30 候选（同域高 co 但已覆盖 + 低 co）。vault KG net +5 synthesis +10 反向链。QMD skipped(unset)。

- [2026-08-27 08:30] WIKI_SYNTHESIZE — vault 400+ 页共现扫描，产 **5 个跨域 synthesis 页**，主题全部围绕「数据库即平台 × agent 架构」哲学族。(1) [[synthesis/concepts-database-as-platform × concepts-no-llm-hot-path]] — 「Complexity Budget」原则：database-as-platform 和 no-llm-hot-path 都在回答「我已有的工具够用吗？」，在 agent 场景中两者形成闭环（SQLite 存储 + 确定性热路径）；(2) [[synthesis/concepts-agentic-design × concepts-design-md-shared-memory]] — DESIGN.md 是 agentic design 的「已编译状态」，parallel to deterministic-agent-memory（代码事实住文件，设计决策住 DESIGN.md）；(3) [[synthesis/skills-postgres-queue-pattern × skills-sqlite-queue-pattern]] — 队列选型是「部署规模」函数：SQLite BEGIN IMMEDIATE（<5K msg/s 进程内）→ PostgreSQL SKIP LOCKED（多消费者）→ Kafka，升级触发条件明确；(4) [[synthesis/concepts-sqlite-as-file-format × concepts-durable-session-log]] — SQLite fopen() 零基础设施 + session log 可重建性：append-only INSERT + 单文件 = 零基础设施 session memory；(5) [[synthesis/entities-sqlite × entities-postgresql]] — 同哲学谱系两端，升级触发器具体（多进程并发写/pgvector/复制需求）。**10 源页已添加反向链接**。skipped 10 候选。vault KG net +5 synthesis +10 反向链。QMD skipped(unset)。

- [2026-08-27 08:00] CROSS_LINK — 针对 2026-08-26/27 新建的 PostgreSQL/SQLite/tmux/herdr/opencoworkai 14 页集群，links_added=28（全为 EXTRACTED/INFERRED 级）。snapshot=a75c0b9ea7fe8d8f263b7f5feb358efcfede9d5e。QMD skipped(unset)。

- [2026-08-27 00:00] WIKI_RESEARCH topic="tmux join-pane & swap-pane 用法" rounds=2 sources_fetched=4。**核心发现**：(1) join-pane/move-pane 等价（break-pane 逆操作）；(2) swap-pane 只交换同 window 内位置槽；(3) Marked pane 机制是跨 window 操作关键；(4) Pane ID（%N）终身不变，优于编号；(5) 三层重排：swap/join/break+join。vault KG net +2。QMD skipped(unset)。

## Active Threads

- **Agent Teams 簇深化**：5 个 synthesis 页已覆盖 cost/display-modes/race-condition × feature 三角，下一步可考虑 `concepts/claude-code-three-modes × entities/claude-code-agent-teams-feature`（正交 vs 替代）或 9 个已知限制的集中页面（lint 候选）。
- **DESIGN.md 校准回路**：format-spec × awesome-design-md 已建，邻近候选 `concepts/design-md-format-spec × entities/google-stitch`（co=6 同未覆盖）或 `concepts/design-system-as-ai-context × entities/google-stitch`（co=6）可继续延伸生态图。
- **确定性哲学的子系统全集**：deterministic-agent-memory ↔ OpenLore + Agent Teams race 已覆盖；下一步候选 `concepts/agent-operating-system × concepts/deterministic-agent-memory`（co=9 顶级未覆盖对）以解释 AOS 作为"哲学的全集框架"。
