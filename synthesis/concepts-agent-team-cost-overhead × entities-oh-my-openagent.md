---
title: Agent Team 成本 × omo 编排器
category: synthesis
tags: [ai-agents, agent-teams, cost, omo, synthesis]
sources:
  - concepts/agent-team-cost-overhead
  - entities/oh-my-openagent
  - concepts/omo-agent-category-routing
  - concepts/omo-discipline-agents
  - concepts/omo-team-mode
  - concepts/omo-ultrawork-mode
  - entities/hephaestus-agent
  - entities/sisyphus-agent
  - references/omo-team-mode-config-schema
  - skills/omo-install-and-setup
summary: "把 agent team token 成本随 teammate 数线性扩展这条抽象约束,对照 omo 把它产品化为 4-category 路由 + 模型分级 + Team Mode 11 字段硬 cap。结论是 omo 用结构吸收线性成本的不可控性,但并未消除它。"
created: 2026-08-23T09:00:00Z
updated: 2026-08-23T09:00:00Z
summary: 把"agent team token 成本随 teammate 数线性扩展"这个抽象成本约束,对照 omo 把成本转译为路由(4 category)+ 模型分级 + Team Mode cap 的产品化实战。结论是 omo 用结构吸收了纯线性成本的不可控性,但并未消除它。
provenance:
  extracted: 0.15
  inferred: 0.75
  ambiguous: 0.10
base_confidence: 0.65
lifecycle: draft
lifecycle_changed: "2026-08-23"
---

# Agent Team 成本 × omo 编排器

## The Connection

`[[concepts/agent-team-cost-overhead]]` 描述一个抽象事实:Agent Teams 的 token 成本随 teammate 数线性扩展,Claude Code 官方推荐 3-5 teammates 区间。`[[entities/oh-my-openagent]]`(omo)是把这条线性曲线变成"产品级可控成本曲线"的第一个具名产品化尝试:它把"扩展"这件事从放任自流重写成 4-category 路由 + 模型分级 + Team Mode 11 字段硬 cap + Opus 主+Sonnet/Haiku/Kimi 子 agent 的层级化结构。

## Where They Co-occur

8 个页面同时提到 token 成本与 omo 编排器:`[[concepts/omo-agent-category-routing]]`(4 类自动选模型)、`[[concepts/omo-discipline-agents]]`(5 specialists 协调)、`[[concepts/omo-team-mode]]`(11 字段 cap)、`[[concepts/omo-ultrawork-mode]]`(单 keyword 全 agent 接管)、`[[entities/hephaestus-agent]]`(gpt-5.6-sol 多 provider deep worker)、`[[entities/sisyphus-agent]]`(claude-opus-5 主 orchestrator)、`[[references/omo-team-mode-config-schema]]`(11 字段详解)、`[[skills/omo-install-and-setup]]`(推荐 $49/月 vs Claude Code $200)。

每个 co-occurring 页面都是"成本控制"的具体技术手段。

## Cross-cutting Insight

`cost-overhead` 的核心抽象是"linear scaling = 不可控"——理论上每加一个 teammate 账单就翻一倍。但 omo 的实战证明:**线性曲线可以被结构压扁成准对数曲线**。具体做法是:

1. **路由吸收成本**:omo 把"主对话"和"子 agent"切到不同模型。Opus 4 推理一次 $5/M input,Sonnet $3/M,Haiku $0.80/M。把 80% 的工具调用下沉到 Haiku,总成本可以是 Opus-only 的 1/3 到 1/5。
2. **硬 cap 取代警告**:Agent Teams 文档说"推荐 3-5";omo 用 `max_members: 8 / max_parallel_members: 4 / max_wall_clock_minutes: 120` 把推荐变成可执行的硬约束。线性曲线在 x>8 处被截断。
3. **类别路由取代 uniform 模型**:visual-engineering/deep/quick/ultrabrain 4 类的存在意味着"同一个任务在 omo 下可能被路由到 Haiku 做 quick、用 Kimi 做 deep、用 Sonnet 做 ultrabrain",而不像 Agent Teams 默认全 Opus。

但 **omo 没有消除线性,只是把线性预算从"用户钱包"转移到"配置字段"**。开启 8 members + 120min wall clock 的 omo Team Mode 单次会话账单仍是 4-8 teammate 单 agent 的数倍。这是产品可接受的(用户主动 opt-in),但仍是 linear。

## Tensions and Trade-offs

- **cap 越紧,效用越低**:`max_members: 8` 是 omo 工程权衡——但有些任务需要 10+ specialists 协同(全代码审查 + 测试 + 部署监控),此时 omo 会拒绝执行;Agent Teams 默认无 cap 但会让用户吃 linear 成本
- **多模型增加测试矩阵复杂度**:Haiku 出错 vs Opus 出错的失败模式不同,debug 时需要分别建模;Agent Teams 同模型下失败模式更可预测
- **Haiku/Kimi 在 deep reasoning 任务上的质量**:quick 任务下沉到 Haiku 是 win,但"ultrabrain"路由到 Kimi K3 时质量是否真等同 Opus,文档没说 ^[ambiguous]

## Strongest Objection

> 反对者:omo 的"成本可控"是营销叙事。linear scaling 是 LLM 物理事实(每次 tool call 都要发请求),任何上层抽象都不能违反这物理约束。omo 只是在"什么时候调用"做选择,而不是降低单次调用的成本。3-5 teammates 区间之外的执行,在 omo 下仍是 linear scaling,只是用户接受了 cap 而已。

> 反驳:但 cap 本身就是价值——把"用户决策"前置到"配置决策",降低决策疲劳。Agent Teams 的"3-5 推荐"是 post-hoc 警告;omo 的 cap 是 pre-flight 拒绝。两者账单可能一样,UX 天差地别。

> test: 用 30 个等价 task benchmark(同样 10-step research task),对比 omo Team Mode cap=8 与 Claude Code Agent Teams 默认 5 teammates 的**平均成本**与**平均完成时间**。omo 是否真的成本更低?若两者差不多,omo 的 cap 就只是 UX 包装。

## Open Questions

- 4 category 路由的判定标准是什么?文档说"auto",但分类器本身的成本是否被计算? ^ambiguous
- `max_wall_clock_minutes: 120` 是 wall clock 还是 active CPU time?若前者,120 min 在 8 agents × 并发下相当于 16h-agent-time 上限,实际线性在哪?
- `$49/月订阅` 包含多少 Opus 4.6 token?若无限,omo 实际上把 linear cost 移到了产品定价而非用户决策。

## Related

- [[concepts/agent-team-cost-overhead]] — token 成本抽象约束
- [[entities/oh-my-openagent]] — omo 产品本体
- [[concepts/omo-team-mode]] — 11 字段 cap 实操
- [[concepts/omo-agent-category-routing]] — 4 类别自动选模型
- [[synthesis/concepts-bmad-named-agent-architecture × concepts-omo-discipline-agents]] — BMad persona 三腿凳 vs omo capability-defines-persona