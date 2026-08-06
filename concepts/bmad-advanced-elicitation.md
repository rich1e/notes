---
title: "BMad 高级 Elicitation（结构化推理方法）"
category: concepts
tags:
  - bmad-method
  - reasoning
  - elicitation
  - concept
summary: "BMad 高级 Elicitation 让 LLM 用命名推理方法（Pre-mortem / 第一性原理 / 红蓝对抗 / 苏格拉底式质疑等）对自己的输出做结构化二次审视。比『try again』更系统。"
sources:
  - "https://github.com/bmad-code-org/bmad-method"
created: "2026-08-05T07:00:00Z"
updated: "2026-08-05T07:00:00Z"
provenance:
  extracted: 0.85
  inferred: 0.10
  ambiguous: 0.05
base_confidence: 0.65
lifecycle: draft
lifecycle_changed: "2026-08-05"
tier: supporting
relationships:
  - target: "[[concepts/bmad-delivery-loop]]"
    type: related_to
  - target: "[[entities/bmad-method]]"
    type: related_to
  - target: "[[concepts/bmad-build-workflow]]"
    type: related_to
---

# BMad 高级 Elicitation（结构化推理方法）

> 让 LLM **用命名推理方法重新审视**刚生成的内容。你选方法 → AI 用那个 lens 重新检查 → 你决定是否保留改进。比"try again"或"make it better"更系统。

## 是什么

**结构化二次审视**。不是让 AI "再试一次"，而是选一个**特定推理方法**让它从那个 lens 看自己的输出。

> "Vague requests produce vague revisions. A named method forces a particular angle of attack, surfacing insights that a generic retry would miss."

## 何时用

- 工作流生成内容后想要替代
- 输出看似 OK 但怀疑有更多深度
- 压力测试假设 / 找弱点
- 高 stakes 内容，重新思考帮得上

工作流在**决策点**提供高级 Elicitation——LLM 生成完东西后，会问你要不要跑。

## 流程

1. LLM 提议 5 个对你内容相关的方法
2. 你选一个（或 reshuffle 换选项）
3. 方法应用，改进展示
4. 接受 / 丢弃，重复 / 继续

## 内置方法（部分）

- **Pre-mortem Analysis** —— 假设项目已失败，倒推为何失败。**Spec / plan 起步好选**，一致能找到标准 review 漏的 gap。
- **First Principles Thinking** —— 剥掉假设，从 ground truth 重建
- **Inversion** —— 问"如何保证失败"，然后避开那些
- **Red Team vs Blue Team** —— 自己攻击自己的工作，再防御
- **Socratic Questioning** —— 每个 claim 用 "why?" 和 "how do you know?" 挑战
- **Constraint Removal** —— 扔掉所有约束，看变化，再选择性加回
- **Stakeholder Mapping** —— 从每个 stakeholder 视角重评估
- **Analogical Reasoning** —— 找其他领域的对应关系，应用它们的教训

v6.10 新增两个：**[Subtraction](#)**（对抗 additive bias）和 **[Map Is Not the Territory](#)**（防止过度信任 lossy 模型）。

## 为什么"命名方法"重要

Vague requests 产生 vague revisions。**命名方法强制特定攻击角度**，浮出通用 retry 会漏的洞察。

例：
- "Try again" → LLM 重写，方向一样，结果差不多
- "Pre-mortem this" → LLM **假设项目已失败**，从"为什么失败"倒推——找出原始 review 漏的早期假设错

## 与 vault 已有概念的关系

| vault 已有 | 在 BMad 高级 Elicitation 中的体现 |
|---|---|
| [[concepts/agent-team-party-mode]] | Party Mode 多 persona 对话 = elicitation 的"多视角"变体 |
| [[entities/openlore]] | OpenLore 的"deterministic verification"是更硬的 elicitation；BMad 高级 Elicitation 是软的 LLM-based |
| [[concepts/deterministic-agent-memory]] | Elicitation 改善**生成**——deterministic agent memory 保证**查询**——两者互补 |
| [[concepts/bmad-delivery-loop]] | Elicitation 在 Learn 阶段特别有价值——retrospective 反复追问根因 |

## 与"build 阶段的 review findings"区别

| 维度 | 高级 Elicitation | Build 阶段的 review |
|---|---|---|
| 触发时机 | 工作流生成完内容**之后立即** | Build 完成后 |
| 审视对象 | LLM 自己刚生成的内容 | 实际 code diff |
| 方法 | LLM 提议 5 个 reasoning 方法任你挑 | 静态规则 + LLM 审查（Edge Case Hunter / Blind Hunter 等） |
| 适用阶段 | Learn / Plan 阶段 | Build 阶段 |

## Open Questions

- 5 个 LLM 提议的方法**如何排序**——是按历史命中率还是按内容匹配？README 未给具体算法 [[ambiguous]]
- "Accept or discard, repeat or continue" 中的"重复"是**用同一方法**重看还是**换方法**重看？

## Related

- [[entities/bmad-method]] — 框架本体
- [[concepts/bmad-delivery-loop]] — 在闭环哪一阶段用
- [[concepts/bmad-build-workflow]] — Build 阶段的硬 review 互补
- [[entities/openlore]] — "deterministic verification"哲学的另一极