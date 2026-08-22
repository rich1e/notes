---
title: 确定性 Agent 记忆 × BMad 方法论
category: synthesis
tags: [agent-memory, determinism, bmad, methodology, synthesis]
sources:
  - concepts/deterministic-agent-memory
  - entities/bmad-method
  - concepts/bmad-advanced-elicitation
  - concepts/bmad-build-workflow
  - concepts/bmad-delivery-loop
  - concepts/bmad-preventing-agent-conflicts
  - skills/bmad-install-and-setup
created: 2026-08-23T09:00:00Z
updated: 2026-08-23T09:00:00Z
summary: 确定性 agent 记忆哲学(hot path 0 LLM、显式失败分桶、引用可追源码)在工程层落地;BMad 方法论(4 阶段交付闭环)在产品层落地。两者都拒绝"agent 太自由绕过纪律",但选择不同的纪律落点。
provenance:
  extracted: 0.15
  inferred: 0.75
  ambiguous: 0.10
base_confidence: 0.70
lifecycle: draft
lifecycle_changed: "2026-08-23"
---

# 确定性 Agent 记忆 × BMad 方法论

## The Connection

`[[concepts/deterministic-agent-memory]]` 是工程层哲学:**agent 记忆层的 hot path 不放 LLM**,而用确定性算法(grep/BM25/AST 静态分析)。LLM 只在 generate / verify / consolidate 三个 cold path opt-in。同 query 必须给同答案,stale 显式标注,引用可点回源码。代表实现:OpenLore v2.1.x、treehouse、claude-mem 三件套。

`[[entities/bmad-method]]` 是产品层哲学:**agent 工作流必须遵循 4 阶段纪律**(Clarify → Plan → Build → Learn),每个阶段有 artifact(brainstorming doc / research / product brief / PRFAQ),大工作与小工作共享同一闭环仅深度不同。代表实现:BMad 5 命名 agent + 4 模式 Party Mode + TOML 覆盖系统。

## Where They Co-occur

5 个 co-occurring 页都围绕"agent 必须有纪律":

- `[[concepts/bmad-advanced-elicitation]]` — 命名推理方法(Pre-mortem / 第一性原理 / 红蓝对抗 / 苏格拉底式)对 LLM 输出做结构化二次审视
- `[[concepts/bmad-build-workflow]]` — canonical 5 步:压缩 intent → 路由最小安全路径 → 跑更久少监督 → 在正确层诊断失败
- `[[concepts/bmad-delivery-loop]]` — Clarify → Plan → Build → Learn 4 阶段
- `[[concepts/bmad-preventing-agent-conflicts]]` — ADR + FR-NFR + standards 防冲突
- `[[skills/bmad-install-and-setup]]` — v6+ `npx bmad-method install`,v7+ 必用 uv

## Cross-cutting Insight

确定性记忆与 BMad 方法论是同一问题("如何防止 AI agent 失控")在两个抽象层的解:

| 维度 | 确定性 Agent 记忆(工程层) | BMad 方法论(产品层) |
|---|---|---|
| **抽象** | 记忆层的失败语义 | 工作流的阶段纪律 |
| **纪律落点** | hot path 算法 vs cold path LLM | 4 阶段 artifact vs 自由发挥 |
| **失败处理** | locate_symbol_span → fresh / stale / ambiguous / not-found | elicitation(method 二次审视) |
| **可重放** | 引用追到 file:line + commit hash | ADR 文档 + 阶段 artifact |
| **可证伪** | "同 query 必须同答案" | "每阶段必产 artifact,否则拒绝进入下一阶段" |
| **适用场景** | 知识图谱 / 代码考古 / 失败分桶 | 产品需求 / 设计决策 / 跨团队交付 |

**核心 insight**:**两者本质都是"用结构对抗 AI agent 的自由度"**。确定性记忆用算法结构(grep/BM25/AST)取代 LLM 决策;BMad 用工作流结构(4 阶段 artifact)取代 LLM 自由发挥。两者的敌人都是同一个:**LLM 默认的"做最可能的下一件事"倾向**——这倾向在工具调用上是"猜哪个文件"(确定性记忆的战场),在工作流上是"跳过 Plan 直接 Build"(BMad 的战场)。

更深的连接:`[[entities/openlore]]`(确定性记忆代表实现)的 `sprint_planning.py` 与 BMad 的 `sprint_planning.py` **同名且同用途**——v6.10 BMad 加 mailbox 修正时,epic 解析 + status 合并都走 deterministic。**BMad 在 v6.10 之后部分采用了 OpenLore 同款的 deterministic philosophy**,只是装在工作流层而非记忆层。

## Tensions and Trade-offs

- **确定性牺牲创造性**:hot path 0 LLM 意味着 agent 不能"灵感一现"——必须按文件/符号定位。BMad elicitation(method 二次审视)反方向:鼓励 LLM 用推理方法挑战自己
- **方法论刚性 vs agent 适应**:BMad 4 阶段对"快速 bug fix"过重(那应该 Build-only);确定性记忆对"全新领域探索"过死(没有现成 grep pattern)
- **维护成本**:确定性记忆需要维护 grep pattern + 索引;BMad 需要维护 artifact 模板 + 阶段纪律。两者都是隐性 tax
- **失败可见性的代价**:locate_symbol_span 显式报 stale → 用户必须手动重新 ingest;BMad elicitation 失败 → 用户必须切换 reasoning method。两套机制都把"agent 不知道"显性化,但都让用户多一次决策

## Strongest Objection

> 反对者:确定性记忆和 BMad 都是**给 LLM 戴镣铐**。LLM 的优势是"在大量可能性中找到非显然的解",用确定性 + 工作流纪律框死它,等于买贵电脑跑批处理。Markdown + grep + ADR 是 2010 年代的工具,LLM 时代应该用更强的模型而非更强的纪律。

> 反驳:但 vault 现有 [[concepts/no-llm-hot-path]] 明确列出 hot path 放 LLM 的五维亏损:成本 /可靠性 /安全 /诚实。LLM 不是"更强的工具",是"在确定性可解任务上引入随机性的成本中心"。纪律不是镣铐,是**把 LLM 用在该用的地方**。

> test: 对比同一 100 个工程任务的"全 LLM" vs "deterministic memory + BMad" 的(a)完成率(b)平均成本(c)首因 bug 数(d)可重放率。BMad/discipline 路线应在 (b)(c)(d) 显著胜出,在 (a) 可能略输。

## Open Questions

- BMad 的 elicitation(method 二次审视)是否可以产品化为 deterministic method(如"自动跑 5 个推理方法并投票")?目前是 LLM 自由发挥 ^[ambiguous]
- OpenLore 的 commit gate(drift + decisions + check_architecture)是否可以装进 BMad 的 Plan 阶段?两者现在独立运作,组合能否让"BMad Plan 阶段拒绝 spec 与代码不一致的 commit"?
- 确定性记忆与 claude-mem(概率型长期记忆)是否应该分工?hot path deterministic(OpenLore)+ cold path probabilistic(claude-mem)?

## Related

- [[concepts/deterministic-agent-memory]] — 工程层哲学
- [[entities/bmad-method]] — 产品层方法论
- [[concepts/bmad-delivery-loop]] — 4 阶段闭环
- [[entities/openlore]] — 确定性记忆的代表实现
- [[synthesis/concepts-agent-team-mailbox-protocol × entities-bmad-named-agent]] — BMad 命名 agent 派发