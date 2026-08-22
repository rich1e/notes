---
title: 设计系统作为 AI 上下文 × Claude Code 消费
category: synthesis
tags: [design-system, ai-context, claude-code, mcp, synthesis]
sources:
  - concepts/design-system-as-ai-context
  - entities/claude-code
  - concepts/ai-tool-specialization
  - entities/google-stitch
  - entities/openlore
  - misc/web-medium-com-devsecops-ai-how-google-stitch-claude-codes-mcp-integration
  - skills/claude-code-token-optimization
created: 2026-08-23T09:00:00Z
updated: 2026-08-23T09:00:00Z
summary: 把 DESIGN.md 从"文档"升级为"AI 硬约束输入",消除 agent 在 padding/spacing 等决策上的 token 浪费;Claude Code 作为当前最大消费方,通过 Stitch MCP/Figwright MCP/Cursor 等 7+ 集成消费 DESIGN.md。
provenance:
  extracted: 0.20
  inferred: 0.70
  ambiguous: 0.10
base_confidence: 0.70
lifecycle: draft
lifecycle_changed: "2026-08-23"
---

# 设计系统作为 AI 上下文 × Claude Code 消费

## The Connection

`[[concepts/design-system-as-ai-context]]` 把 DESIGN.md 从"designers 读的文档"重定义为"AI 硬约束输入":YAML tokens(色/字号/spacing/radius/transition)+ 8 必备 prose 章节(do's and don'ts 等),让 agent 不用反复 token 决策。该概念的本质是**把设计纪律编译成 LLM 可读的 schema**,避免每次生成都"重新讨论审美"。

`[[entities/claude-code]]` 是这个概念的**最大消费方**:Anthropic 终端式 AI 编码 agent,通过 MCP 接外部服务(Stitch/Figwright/Dev Mode MCP 等),通过提示缓存控制 token。Claude Code 不"创造"设计系统,但它是 DESIGN.md → 代码 → DESIGN.md 闭环的执行端。

## Where They Co-occur

5 个 co-occurring 页都围绕"设计纪律 → AI → 代码"这条链:

- `[[concepts/ai-tool-specialization]]` — 每个 agent 守一段,Stitch 守视觉输出,Claude Code 守逻辑与代码
- `[[entities/google-stitch]]` — Google Labs AI 设计工具(Gemini 2.5 Pro 驱动),输出 DESIGN.md + 结构化 HTML/CSS,**它是 DESIGN.md 的**主要**生产者**
- `[[entities/openlore]]` — 静态分析驱动的代码知识图谱,与 DESIGN.md 形成"代码层 schema"(design spec)而非视觉层
- `[[misc/web-medium-com-devsecops-ai-how-google-stitch-claude-codes-mcp-integration]]` — Stitch + Claude Code MCP 协作实操
- `[[skills/claude-code-token-optimization]]` — 提示缓存 + 会话管理,DESIGN.md 作为长上下文 anchor 节省 token

## Cross-cutting Insight

DESIGN.md 作为 AI 硬约束是**单向的"编译时优化"**:

| 没有 DESIGN.md 时 | 有 DESIGN.md 时 |
|---|---|
| Claude Code 生成 `<div class="card">` | Claude Code 生成 `<div class="card" style="bg-paper-100 radius-8 p-6">` |
| 用户必须解释 "用暖色调",花 ~50 tokens | DESIGN.md 已有 token 引用,Claude 直接读 |
| 每次 design critique 重新决策 | critique 对照 DESIGN.md ## Do's and Don'ts,1-2 轮收敛 |
| 设计产出与代码产出风格不一致 | 一份 DESIGN.md 串起 Stitch(出设计) + Claude Code(落代码) + Cursor(编辑) |

**核心 insight**:**DESIGN.md 是 vault 现有 3 个 AI 时代基础设施模式之一**(与 claude-code-token-optimization 的"分层缓存"+ ai-tool-specialization 的"专业化分工"并列)。三者的共同主题都是**"让 AI 不做重复决策"**:DESIGN.md 编译视觉决策,token caching 编译 prompt 决策,tool specialization 编译能力决策。

具体到 Claude Code:`[[misc/web-medium-com-devsecops-ai-how-google-stitch-claude-codes-mcp-integration]]` 展示了两种鉴权路径(API key header vs OAuth proxy),都是为了让 Claude Code 能**自动消费** Stitch 产出的 DESIGN.md——而不是让用户每次手动 copy-paste。

## Tensions and Trade-offs

- **DESIGN.md 越详细,维护成本越高**:74 个真实站点的 awesome-design-md 显示,DESIGN.md 平均 200-400 行;每次视觉改版都要更新
- **硬约束 vs 创作空间**:DESIGN.md 强调"Do's and Don'ts"(vault [[concepts/design-md-anti-patterns]] 详述),但创作性 UI 实验可能故意违反"Don't"。给 AI 的硬约束可能扼杀灵感
- **YAML token 引用 vs 视觉直觉**:token interpolation(`{path.to.token}`)让机器可读,但设计师可能更喜欢 hex 值直接写。Vault 现有 [[concepts/design-md-token-interpolation]] 是借鉴 DTCG 2025.10 规范的选择,但仍非主流
- **Stitch 输出 vs 手工 DESIGN.md**:Stitch 自动产出的 DESIGN.md 与人类设计师写的可能风格迥异。Vault 现有 [[synthesis/Research: DESIGN.md 工作流]] 显示 Stitch 自动产出正在成为主流,但未必与既有设计系统对齐

## Strongest Objection

> 反对者:DESIGN.md 是"伪工程化"的过度结构化。LLM 已经能从训练数据学到视觉决策模式,DESIGN.md 只是让用户**心理安慰**"AI 在按规范做事"。实际产出可能与无 DESIGN.md 时差异 < 10%,但维护成本 5x。

> 反驳:但训练数据学到的是"业界均值"(gradient / glow / emoji),DESIGN.md 的 Do's and Don'ts 章节正是为了**反均值审美**。没有 DESIGN.md 时,AI 默认漂向渐变 + glow + emoji 的"AI taste",DESIGN.md 是显式对抗这个漂移。

> test: 跑 50 个 UI task,对比有/无 DESIGN.md 的产出。(a) 设计一致性(配色/spacing 是否在 ±5% 容差内);(b) 创作多样性(是否产生过 gradient/glow 默认审美)。两者任一显著差异,DESIGN.md 就有价值;两者都不显著,是真伪工程化。

## Open Questions

- Stitch 自动产出的 DESIGN.md 与人类设计师写的,哪个 token 引用粒度更适合 Claude Code 消费? ^[ambiguous]
- DESIGN.md 是否会被 LLM 训练 pipeline 吸收(类似 system prompt),变成"内置风格",届时显式 DESIGN.md 是否仍必要?
- Figwright MCP 的 `provider-first codegen` 是否会把 DESIGN.md 作为默认约束来源,降低 Claude Code 用户的配置成本?

## Related

- [[concepts/design-system-as-ai-context]] — DESIGN.md 作为 AI 硬约束
- [[entities/claude-code]] — 主要消费方
- [[entities/google-stitch]] — 主要生产方
- [[concepts/ai-tool-specialization]] — 工具栈专业化
- [[synthesis/concepts-mcp-server-protocol-quirks × entities-google-stitch]] — Stitch OAuth proxy 鉴权