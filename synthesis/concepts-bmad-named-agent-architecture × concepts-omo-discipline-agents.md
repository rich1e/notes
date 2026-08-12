---
title: bmad-named-agent-architecture × omo-discipline-agents
category: synthesis
tags:
  - bmad-method
  - omo
  - agent-orchestration
  - persona
  - architecture
sources:
  - "[[concepts/bmad-named-agent-architecture]]"
  - "[[concepts/omo-discipline-agents]]"
  - "[[entities/bmad-method]]"
  - "[[entities/oh-my-openagent]]"
  - "[[entities/bmad-named-agent]]"
  - "[[entities/sisyphus-agent]]"
  - "[[concepts/agent-operating-system]]"
created: 2026-08-12T05:49:00Z
updated: 2026-08-12T05:49:00Z
summary: "BMad 命名 agent 三腿凳（Skill/Persona/Customization）vs omo 5 专家分工（Sisyphus+4 disciplines）：同一 agent 框架目标下两种截然不同的「agent persona」设计哲学对比。"
provenance:
  extracted: 0.25
  inferred: 0.65
  ambiguous: 0.10
base_confidence: 0.68
lifecycle: draft
lifecycle_changed: "2026-08-12"
---

# BMad 命名 Agent 架构 × omo Discipline Agents

## 关联

两个框架各自解决了同一问题："当你有多个 AI agent 协同工作时，如何让每个 agent 知道自己是谁、该做什么？"

- **BMad** 的答案是"三腿凳"：Skill（能力文件）+ Named Agent（persona 身份连续性）+ Customization（个性化层）—— 每个 agent 先有明确 persona，能力是挂载在 persona 上的插件。
- **omo** 的答案是"角色专业化 + 单中央调度者"：Sisyphus 作为 orchestrator，Hephaestus/Oracle/Librarian/Explore/Prometheus 各守一个 discipline —— persona 即角色，角色即能力边界，边界即路由规则。

两条路都不从"工具调用"出发，而都从"人格化身份"出发 —— 这是它们与 LangChain/AutoGen 流派的共同区别 ^[inferred]。

## 共现场景

两个框架在以下情境中被同时提及：

- 讨论"如何组建 AI 团队"时（`entities/bmad-method` + `entities/oh-my-openagent`）
- 讨论"哪款框架适合 Claude Code"时（`skills/omo-install-and-setup`、`concepts/omo-discipline-agents`）
- 讨论"multi-agent 框架的 persona 设计"时（`concepts/bmad-named-agent-architecture` 里提到"命名 agent 使体验完整"，`concepts/omo-discipline-agents` 里 Sisyphus 即是 orchestrator persona）
- `_staging/misc/claude-code-agent-teams-ppt-content.md` 同时引用了两个框架

## 跨框架洞见

**BMad 是"persona 先于能力"，omo 是"能力定义 persona"。** ^[inferred]

- BMad 先命名 5 个人物（Mary BA / John PM / Sally UX / Winston Architect / Amelia Dev），再往每个人物上挂 SKILL 文件。改变能力 = 换 SKILL 文件，persona 身份不变。
- omo 先定义 5 种 discipline（Hephaestus 做事 / Oracle 查知识 / Librarian 管文档 / Explore 勘探 / Prometheus 计划），再把模型绑到 discipline 上。persona = 职能范围，换模型不换职能。

这一区别在实践中有重要影响：

| 维度 | BMad | omo |
|---|---|---|
| persona 稳定性 | 人物身份固定，能力热插拔 | 职能固定，运行时 model 可换 |
| 扩展方式 | 给 agent 加新 SKILL 文件 | 新增一个 discipline 角色 |
| 适合规模 | 中型项目，需要持续迭代同一 agent | 并行大任务，各角色无状态 |
| 定制粒度 | TOML override：个人/团队双层 | agent 级别模型参数覆盖 |

**第二个洞见：协调者的定位不同。** BMad 的 orchestrator 是"所有 agent 都可以成为协调者"（bmad-build-workflow 里任何命名 agent 都能 handoff）；omo 的 Sisyphus 是唯一协调者，并且持续工作直到完成（"推石上山"）。前者分布式委派、后者集中控制 —— 即使任务失败，Sisyphus 也会再尝试，BMad 则由人类 review 后决定是否重走 Clarify。

## 张力与权衡

- **persona 一致性 vs 灵活模型绑定**：BMad 的 named agent 在不同会话间保持人物连贯性，但这要求维护 persona 文件；omo 的 discipline 无状态，换模型无感知，但跨会话无"记忆"。
- **学习曲线**：BMad 三腿凳概念清晰，但安装涉及 407 个文件；omo Ultimate Edition 需要选择 11 个 agent 的模型，且订阅费 $49/月 vs BMad 的 $200 Claude Code 已包含。
- **framework lock-in**：BMad 深度绑定 BMad Method 的 agile 流程；omo 是通用 AI dev 框架，工作流无硬编码 ^[ambiguous]。

## 最强质疑

**这两个框架真的在解决同一问题吗？** 质疑：BMad 是"项目管理方法论"的 AI 实现（从 Clarify → Plan → Build → Learn 的工作流），omo 是"并行 AI 工程执行"框架（Ultrawork = 不停工作直到完成）—— 它们的 persona 设计看起来相似，但服务于完全不同的目标。BMad 的"Mary BA 做需求分析"是角色扮演型 persona；omo 的"Hephaestus 做深度执行"是功能路由型 persona。两者的 agent 根本就不是同类 persona。

> **test：** 找一个同时运行 BMad + omo 的团队，看他们如何处理角色冲突（BMad 的 Amelia Dev 和 omo 的 Hephaestus 在同一 repo 上同时工作时，哪个 persona 的决策优先？）

## 未解问题

1. BMad 的 named agent persona 跨会话一致性依赖什么机制？（SKILL 文件 + CLAUDE.md 注入？还是需要 claude-mem 这类外部记忆？）
2. omo 的 Sisyphus "推石不停"在 token 消耗上与 BMad"人工 review 后循环"相比，长任务上哪个更省？
3. 两框架能否混用？即用 BMad 的三腿凳 persona 系统 + omo 的 discipline 路由规则？

## Related

- [[concepts/bmad-named-agent-architecture]] — BMad 三腿凳原语详解
- [[concepts/omo-discipline-agents]] — omo 5 专家角色详解
- [[entities/bmad-method]] — BMad Method 框架总体
- [[entities/oh-my-openagent]] — omo 框架总体
- [[concepts/agent-operating-system]] — 两框架都可映射到 AOS 的五层 memory 框架中
- [[concepts/bmad-delivery-loop]] — BMad 工作流与 omo Ultrawork 的协调模式对比入口
- [[entities/sisyphus-agent]] — omo orchestrator 角色详解
