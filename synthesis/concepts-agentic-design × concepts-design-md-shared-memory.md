---
title: Agentic Design × DESIGN.md Shared Memory
category: synthesis
tags:
  - ai-agent
  - design-system
  - agentic-design
  - shared-memory
  - open-codesign
sources:
  - "[[concepts/agentic-design]]"
  - "[[concepts/design-md-shared-memory]]"
  - "[[entities/open-codesign]]"
  - "[[references/open-codesign-prompt-system-deepwiki]]"
  - "[[entities/google-labs-code-design]]"
created: 2026-08-27T08:30:00Z
updated: 2026-08-27T08:30:00Z
summary: "DESIGN.md 是 agentic design 的「已编译状态」——把设计决策从人脑转移到文件，使 agent 能在不重复问设计问题的情况下持续工作。"
provenance:
  extracted: 0.20
  inferred: 0.70
  ambiguous: 0.10
base_confidence: 0.70
lifecycle: draft
lifecycle_changed: "2026-08-27"
relationships:
  - target: "[[concepts/agentic-design]]"
    type: derived_from
  - target: "[[concepts/design-md-shared-memory]]"
    type: derived_from
---

# Agentic Design × DESIGN.md Shared Memory

## The Connection

[[concepts/agentic-design]] 描述了 open-codesign 的三大支柱：workspace-backed sessions、permissioned tool use、以及 **DESIGN.md shared memory**。但"DESIGN.md 作为 shared memory"不只是 agentic design 的一个实现细节——它指向了一个更深的问题：**agent 如何跨越多次会话持续地"知道"设计意图？**

[[concepts/design-md-shared-memory]] 回答了这个问题：把设计决策（颜色/排版/组件规范）编译成机器可读的文件，让 agent 每次从文件而非从人类对话中读取约束。

两个概念的关系是：agentic design 描述了**需要什么**（agent 需要跨 session 的设计上下文），DESIGN.md shared memory 描述了**怎么做**（把设计约束物化为可读写的文件而非临时的 prompt）。^[inferred]

## Where They Co-occur

- **[[entities/open-codesign]]** — v0.2.0 "Agentic Design" 发布，明确把 DESIGN.md 列为三大支柱之一
- **[[references/open-codesign-prompt-system-deepwiki]]** — DeepWiki 分析：open-codesign 的 skills 系统（YAML frontmatter + body）与 DESIGN.md 的 token 系统共享"结构化人类可读格式 = agent 可读约束"的设计哲学
- **[[synthesis/Research: open-codesign]]** — 研究综合：DESIGN.md 是 workspace-backed session 能持续工作的"设计长期记忆"
- **[[concepts/design-system-as-ai-context]]** — DESIGN.md 把设计系统升级为 AI 硬约束，避免 agent 在 padding/spacing 等细节上每次都重新决策

## Cross-cutting Insight

**DESIGN.md 是 agentic design 的"编译产物"**：^[inferred]

在传统开发工作流中，设计意图住在人脑里（或者设计师的 Figma 评论里），每次开始一个新功能，开发者需要重新问"这个按钮应该用什么颜色？"。这对人类来说只是小摩擦，但对 agent 来说是**系统性问题**——agent 没有跨 session 的记忆，每次都可能做出不同的设计决策。

DESIGN.md 通过把设计约束物化为文件，让 agentic design 工作流中的每个 agent session 都能从同一个设计状态出发，不需要"重新理解"设计系统。

这和 [[concepts/deterministic-agent-memory]] 的逻辑结构完全平行：
- deterministic-agent-memory：代码事实住在索引文件里，不住在 LLM 记忆里
- DESIGN.md shared memory：设计事实住在 DESIGN.md 里，不住在每次 session 的 prompt 里

两者都把"本来需要重新解释的知识"转化成"agent 可以直接读取的持久状态"。

## Tensions and Trade-offs

- **「设计文档腐烂」问题**：DESIGN.md 作为 shared memory 有一个假设——文件是最新的。但实际项目中，设计迭代速度往往快于文档更新速度。如果 DESIGN.md 已经过时，agent 就会在错误的约束下工作。这个问题在纯代码记忆（如 OpenLore）中也存在（stale 需要显式标注），但设计文档的"freshness verdict"机制目前还没有标准化。
- **「设计决策深度」限制**：DESIGN.md 能捕获色彩、排版、间距等 token 级约束，但难以表达复杂的「设计意图」——为什么用这个颜色，这个组件在哪种情绪下才合适。agentic design 的工作流假设 DESIGN.md 已经包含了足够的决策信息，但对于复杂产品，这个假设可能过于乐观。

## Strongest Objection

**"DESIGN.md 只是一个文件，把它叫做'agentic design 的已编译状态'是过度诠释——它的实际效果只是减少了 agent 的 prompt 重复，没有引入新的架构模式"。**

> test: 在有 DESIGN.md 和没有 DESIGN.md 的情况下，分别让同一个 agent 完成 10 次 UI 修改任务，测量（1）设计一致性、（2）token 消耗、（3）需要人工干预的次数——如果差异不显著，"shared memory"的标签就是夸大的。

## Open Questions

- **DESIGN.md 的 lifecycle 管理**：谁负责更新它？什么触发更新？是否可以有"design freshness verdict"机制？
- **与代码记忆的协同**：[[entities/openlore]] 管代码结构记忆，DESIGN.md 管设计约束——这两个"持久状态文件"在 agent workflow 中的协作协议是什么？
- **单向还是双向**：DESIGN.md 目前是 agent 读取的状态，是否可以让 agent 在工作中"写回" DESIGN.md（把临时决策升级为永久约束）？

## Related

- [[concepts/agentic-design]] — 三大支柱设计模式
- [[concepts/design-md-shared-memory]] — DESIGN.md 的机制描述
- [[concepts/design-system-as-ai-context]] — 设计系统升级为 AI 硬约束
- [[concepts/skill-progressive-disclosure]] — 类似的"按需加载约束"模式（skills 系统）
- [[entities/open-codesign]] — 两概念的来源项目
- [[entities/google-labs-code-design]] — DESIGN.md 官方规范
- [[synthesis/Research: open-codesign]] — open-codesign 三轮研究综合
- [[synthesis/concepts-design-system-as-ai-context × entities-claude-code]] — 设计系统 × Claude Code 的 synthesis
