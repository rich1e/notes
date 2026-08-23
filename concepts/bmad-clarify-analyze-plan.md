---
title: "BMad Clarify & Analyze 阶段（Idea → Foundation）"
category: concepts
tags:
  - bmad-method
  - analysis
  - brainstorming
  - concept
summary: "BMad Analysis 阶段：从模糊想法到 Foundation。brainstorming / research / product brief / PRFAQ 4 种 artifact 的差异与何时用哪个。"
sources:
  - "https://github.com/bmad-code-org/bmad-method"
created: "2026-08-05T07:00:00Z"
updated: "2026-08-05T07:00:00Z"
provenance:
  extracted: 0.78
  inferred: 0.15
  ambiguous: 0.07
base_confidence: 0.62
lifecycle: draft
lifecycle_changed: "2026-08-05"
tier: supporting
relationships:
  - target: "[[concepts/bmad-delivery-loop]]"
    type: related_to
  - target: "[[entities/bmad-named-agent]]"
    type: related_to
---

# BMad Clarify & Analyze 阶段（Idea → Foundation）

> BMad **Analysis 阶段**（闭环第一阶段）—— 把模糊想法变成 Foundation。核心 4 种 artifact：**brainstorming / research / product brief / PRFAQ**。每种有明确触发场景。

## 4 种 Artifact

| Artifact | 何时用 | 主要产出 |
|---|---|---|
| **Brainstorming** | 想法没成型 / 想压力测试 / 想"漏了什么" | 探索问题域 / 多视角 |
| **Research** | 想搞清楚现状 / 用户 / 市场 / 技术 | 调查报告 |
| **Product Brief** | 想法清晰但想文档化产品定位 | 简明产品概述 |
| **PRFAQ** | 想给 stakeholder 演示 / 拉支持 | PR + FAQ 组合文档（Amazon 风格） |

## 何时选哪个

| 情况 | 推荐 artifact |
|---|---|
| 想法模糊 | **Brainstorming** |
| 想压力测试已有想法 | **Brainstorming**（特别 party-mode 配合） |
| 想从零开始市场调研 | **Research** |
| 想内部定位文档 | **Product Brief** |
| 想让 stakeholder 批准 | **PRFAQ** |
| 已有 brainstorm + research 产出 | **Product Brief** 或 **PRFAQ** |

## v6.10 的 forge-idea 与 brainstorm

v6.10 新增 `bmad-forge-idea` —— **用 Socratic 问题** 一次一个压力测试半成形想法：

- 配对抗 attack mode
- 可选 persona rooms
- 直到想法**硬化 / 验证通过 / 廉价死亡**

这是 brainstorming 的"半成形想法硬化"变体。

## Mary（Business Analyst）的工具箱

📊 **Mary** 是 BMad 5 命名 agent 之一，锚定 **Analysis 阶段**。她的核心能力：

- brainstorming
- market research
- product briefs
- PRFAQs

她**只在需要时**直接调用相关 skill——`Hey Mary, let's brainstorm` 跳过菜单直接 dispatch `bmad-brainstorming`。

## 与 vault 已有概念的关系

| vault 已有 | 在 BMad Analysis 阶段中的体现 |
|---|---|
| [[concepts/bmad-delivery-loop]] | Analysis 是闭环第一阶段 |
| [[entities/bmad-named-agent]] | Mary 守 Analysis 阶段 |
| [[entities/bmad-party-mode]] | Brainstorming 配合 Party Mode = 多视角探索 |
| [[concepts/bmad-advanced-elicitation]] | Analysis 阶段产出后可用 Elicitation 二次审视 |
| [[concepts/ai-tool-specialization]] | "专用分析 agent"是工具栈分工的体现 |

## Artifact 的"轻 vs 重"

| Artifact | 轻重 | 何时重做 |
|---|---|---|
| Brainstorming | 轻 | 任何方向变化 |
| Research | 重 | 用户 / 市场变化 |
| Product Brief | 中 | 定位变化 |
| PRFAQ | 重 | 想大规模改方向 |

轻 artifact 频繁迭代，重 artifact 较少迭代——这是 BMad "**Right-sized process**" 的 Analysis 阶段体现。

## Open Questions

- "product brief" 与 "PRFAQ" 的**功能边界**——两者都可作 stakeholder 文档，具体差异未在 README 详述 ambiguous
- `bmad-forge-idea` 与 `bmad-brainstorming` 的**触发判断**——何时该走 Socratic 硬化、何时直接 brainstorm？

## Related

- [[entities/bmad-named-agent]] — Mary 是 Analysis 阶段的主人
- [[concepts/bmad-delivery-loop]] — Analysis 在闭环的位置
- [[entities/bmad-party-mode]] — brainstorming 配合多视角
- [[concepts/bmad-advanced-elicitation]] — 产出后二次审视
- [[entities/bmad-method]] — 框架本体