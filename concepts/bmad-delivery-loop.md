---
title: "BMad 交付闭环（Clarify → Plan → Build → Learn）"
category: concepts
tags:
  - bmad-method
  - workflow
  - agile
  - concept
summary: "BMad Method 的核心交付闭环：从模糊想法到能运行的软件分 4 阶段（Clarify 澄清 → Plan 计划 → Build 构建 → Learn 学习）。大小工作共享同一闭环，仅深度不同。"
sources:
  - "https://github.com/bmad-code-org/bmad-method"
created: "2026-08-05T07:00:00Z"
updated: "2026-08-05T07:00:00Z"
provenance:
  extracted: 0.85
  inferred: 0.10
  ambiguous: 0.05
base_confidence: 0.68
lifecycle: draft
lifecycle_changed: "2026-08-05"
tier: supporting
relationships:
  - target: "[[concepts/bmad-build-workflow]]"
    type: related_to
  - target: "[[entities/bmad-method]]"
    type: related_to
  - target: "[[entities/bmad-named-agent]]"
    type: related_to
  - target: [[concepts-agent-operating-system × concepts-deterministic-agent-memory]]
    type: related_to
---

# BMad 交付闭环（Clarify → Plan → Build → Learn）

> BMad 的整个交付由这 4 阶段组成循环：**Clarify 澄清 → Plan 计划 → Build 构建 → Learn 学习**，闭环回 Plan。周末 prototype 和有几年历史的系统走**同一闭环**，仅深度不同。

## 4 阶段

| 阶段 | 触发 | 主要工作 |
|---|---|---|
| **Clarify** 澄清 | 模糊想法 | brainstorming / research / 产品简报 / PRFAQ |
| **Plan** 计划 | 大而清晰的想法 | PRD / UX 设计 / 架构 / epics / stories / sprint 计划 |
| **Build** 构建 | 小改动 / 已 plan 故事 | 实现 + review + 验证 |
| **Learn** 学习 | 完成 / 出错 | retrospective / checkpoint preview / 调整回 Plan |

## 大小工作的入口

README 的核心承诺：

> "Right-sized process — Go directly to implementation for clear changes or add deeper planning for larger initiatives."

| 工作量 | 入口 |
|---|---|
| 清晰小改动 | 直进 **Build** |
| 复杂 initiative | **Clarify → Plan → Build → Learn** |
| 周末 prototype | 完整闭环但每阶段轻量 |
| 有历史的系统 | 完整闭环 + `bmad-document-project` 建立 verified context |

## 命名 Agent × 阶段映射

| Agent | 阶段 |
|---|---|
| 📊 **Mary**, Business Analyst | Clarify |
| 📋 **John**, Product Manager | Plan |
| 🎨 **Sally**, UX Designer | Plan |
| 🏗️ **Winston**, System Architect | Plan / Solutioning |
| 💻 **Amelia**, Senior Engineer | Build |

每个 agent **锚定到 BMad Method 的一个阶段**——名字、阶段、模块，三位一体。

## "Start Anywhere"

> "Start anywhere. Use BMad end to end, or carry its briefs, specifications, and architecture into your existing delivery workflow."

**不是必须从 Clarify 开始**——已有 PRD / 设计 / 架构？直接从 Plan 或 Build 起。BMad 的 artifacts 是**可携带的**：briefs、specs、architecture 都能带进现有的 delivery 工作流。

## v6.10+ 的 phase 文件夹结构变化

```
# 旧 (v6.9)
skills/1-analysis/...
skills/2-planning/...
skills/3-solutioning/...
skills/4-implementation/...

# 新 (v6.10 / #2658)
skills/agents/...        # agent skills
skills/plan/...          # 1-analysis + 2-planning + 3-solutioning
skills/ship/...          # 4-implementation
```

Phase 编号文件夹 collapse 成两条 lane——按字母序对应概念顺序。Installed skill ID 不变，只 source-tree 路径移动。

## 闭环 vs Learn

**Learn 不是结束**——它**回环到 Plan**。Learn 阶段产出（retrospective、checkpoint preview）成为下一轮 Plan 的输入。这是 [[concepts/agent-operating-system]] 的"事件驱动更新"在交付级别的体现。

## 与 vault 已有概念的关系

| vault 已有 | 在 BMad 闭环中的体现 |
|---|---|
| [[concepts/ai-agent]] | 闭环每阶段由 AI agent 主推 |
| [[concepts/agent-operating-system]] | 5 层 memory 映射到 4 阶段——KB（CLAUDE.md）持续携带 context |
| [[concepts/deterministic-agent-memory]] | sprint-planning.py 把 epic 解析 / status 合并做成 deterministic 步骤 |
| [[concepts/ai-tool-specialization]] | 5 agent 各守一阶段 = 工具栈专业化分工 |

## Related

- [[entities/bmad-method]] — 框架本体
- [[concepts/bmad-build-workflow]] — Build 阶段详解
- [[entities/bmad-named-agent]] — 各阶段的主人
- [[concepts/bmad-advanced-elicitation]] — Learn 阶段的 reasoning 工具
- [[concepts/bmad-preventing-agent-conflicts]] — 闭环在多 agent 实施时的架构护栏
- [[synthesis/concepts-bmad-delivery-loop × concepts-agent-operating-system]] — synthesis：BMad 4 阶段工作流节奏 vs AOS 5 层跨会话 memory 架构