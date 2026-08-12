---
title: bmad-delivery-loop × agent-operating-system
category: synthesis
tags:
  - bmad-method
  - agent-orchestration
  - workflow
  - memory
  - architecture
sources:
  - "[[concepts/bmad-delivery-loop]]"
  - "[[concepts/agent-operating-system]]"
  - "[[concepts/bmad-preventing-agent-conflicts]]"
  - "[[entities/bmad-method]]"
  - "[[concepts/claude-mem-memory-architecture]]"
created: 2026-08-12T05:49:00Z
updated: 2026-08-12T05:49:00Z
summary: "BMad 4 阶段交付闭环（Clarify→Plan→Build→Learn）vs AOS 5 层持续 memory 框架：前者管工作流节奏，后者管状态跨会话持久化——两者互补而非竞争，合体才能让 AI agent 交付跨越单次会话。"
provenance:
  extracted: 0.20
  inferred: 0.72
  ambiguous: 0.08
base_confidence: 0.62
lifecycle: draft
lifecycle_changed: "2026-08-12"
---

# BMad 交付闭环 × Agent Operating System

## 关联

两个概念来自不同来源，但在 vault 中被同一批页面反复共同引用：

- `concepts/bmad-preventing-agent-conflicts` 同时引用两者——BMad 用 ADR 防止多 agent 冲突决策，AOS 用 Handoff/Auto memory 跨会话延续决策上下文
- `entities/bmad-method` 提到 Learn 阶段的"checkpoint preview"可类比 AOS 的 compact checkpoint 模板
- `misc/web-youtube-com-watch-v-cskoa-ccmq0w` 讨论多会话 AI 工作时同时涉及两个视角

## 跨框架洞见

**BMad 描述工作流节奏（何时做什么），AOS 描述记忆架构（在哪里存什么）—— 两者各解决一半问题，合体才能让 AI agent 真正跨会话持续交付。** ^[inferred]

BMad 的 4 阶段是时序的："先 Clarify（澄清）再 Plan（计划）再 Build（构建）再 Learn（学习）"。它很好地描述了单次工作节律，但**沉默于一件事**：如果 Build 阶段用掉了 Claude 的整个上下文窗口怎么办？Clarify 阶段的决策在 compact 后还能被下一个会话访问吗？

AOS 的 5 层 memory 恰好填补这一沉默：

| AOS 层 | 对应 BMad 阶段 | 具体内容 |
|---|---|---|
| Handoff memory | Clarify → Plan 边界 | 澄清阶段的决策、需求、约束记录到 HANDOFF.md |
| Auto memory (claude-mem) | Build 阶段 | PostToolUse/Stop hook 自动捕获 30 分钟以上的 Build 活动 |
| ADR memory | Plan → Build 边界 | 架构决策记录在 ADR，防止多 agent 并行 Build 时冲突 |
| KB（知识库）memory | Learn → Clarify | 跨项目 pattern、lessons learned |
| compact checkpoint | Learn 阶段 | Retrospective 产出写入 HANDOFF.md，供下一轮 Clarify 继承 |

**第二个洞见：两框架对"Learn 阶段"的理解相互强化。** BMad 的 Learn 是"retrospective + checkpoint preview + 调整回 Plan"，偏定性；AOS 的 compact checkpoint 是一个精确的 markdown 模板（当前目标 / 已读文件 / 测试结果 / 决策理由 / 失败原因）。把 AOS 的模板用在 BMad 的 Learn 阶段，可以把 retrospective 从"感觉复盘"升级为"可被下一会话 agent 直接消费的结构化上下文" ^[inferred]。

## 张力与权衡

- **主动 vs 被动记忆写入**：BMad 的 Clarify/Plan 产物需要人工 review 后手动写入 ADR；AOS 的 claude-mem 层是自动 hook 捕获，可能捕获噪声（每次工具调用都记录）。两种策略在高速 Build 阶段会产生结构性冲突——hook 记录太细，ADR 记录太慢。
- **框架深度**：BMad 要求团队接受一套完整的敏捷 vocabulary（epics/stories/sprints）；AOS 是 memory 抽象，与工作流无关。前者适合有组织纪律的团队，后者适合独立开发者 ^[ambiguous]。
- **"Learn → Clarify" 的回路速度**：BMad 假设每个闭环结束后有人工 review；AOS 的 SessionStart hook 是自动触发，下一会话直接继承记忆而不需要人工审批。两种回路速度对 agent 自主性的要求不同。

## 最强质疑

**AOS 实际上比 BMad 更激进 —— 两者真的兼容吗？** 质疑：AOS 设计的最终目标是"无限 AI 工作流"（compact → inject → 继续），需要最小化人工介入；而 BMad 的闭环是明确以"人工 review"作为阶段门（Clarify 结束前产品 owner 必须确认）。如果把 AOS 的 auto-memory 塞进 BMad，实际上是在绕过 BMad 要求的人工门控，让 AI 在没有显式确认的情况下"记住并继续" —— 这破坏了 BMad 的"右 sized process"原则。

> **test：** 找一个已经在用 BMad 的团队，让 claude-mem hook 在 Build 阶段自动记录，然后问他们"下一轮 Clarify 之前，你们有没有 review 过 claude-mem 注入的内容？"如果答案是"没有"，则说明 AOS auto-memory 确实绕过了 BMad 的阶段门。

## 未解问题

1. BMad 的 SKILL 文件与 AOS 的 KB（knowledge base）层有多少重叠？能否把 BMad SKILL 文件直接作为 AOS KB 的内容？
2. BMad 的 `bmad-build` workflow 与 AOS 的 compact checkpoint 模板能否合并为单一模板？
3. 在高频 Build 场景（每天多次 PR），AOS 的 5 层 memory 该如何决定写入哪一层？是否需要一个"layer router"？

## Related

- [[concepts/bmad-delivery-loop]] — BMad 4 阶段详解
- [[concepts/agent-operating-system]] — AOS 5 层 memory 架构
- [[concepts/bmad-preventing-agent-conflicts]] — ADR 防冲突机制（AOS ADR 层的最直接对应）
- [[concepts/claude-mem-memory-architecture]] — Auto memory 层的实现机制
- [[concepts/bmad-build-workflow]] — Build 阶段在两框架中的角色
- [[entities/bmad-method]] — BMad 完整框架
