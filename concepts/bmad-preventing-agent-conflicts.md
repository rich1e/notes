---
title: "BMad 架构护栏防多 Agent 冲突"
category: concepts
tags:
  - bmad-method
  - architecture
  - multi-agent
  - adr
  - concept
summary: "BMad 用 architecture documentation 防止多 agent 同时实施一个系统时做冲突技术决策：ADR 显式记录每个决策 / FR-NFR 映射 / 标准与约定。"
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
  - target: "[[concepts/bmad-build-workflow]]"
    type: related_to
  - target: "[[entities/bmad-method]]"
    type: related_to
  - target: [[concepts-agent-operating-system × concepts-deterministic-agent-memory]]
    type: related_to
---

# BMad 架构护栏防多 Agent 冲突

> 当多个 AI agent 实施同一系统的不同部分时，它们可能做**冲突技术决策**。BMad 用 **architecture documentation 建立共享标准** 防止。

## 3 类常见冲突

### API 风格冲突

**没有架构**：
- Agent A 用 REST `/users/{id}`
- Agent B 用 GraphQL mutations
- **结果**：API pattern 不一致，消费者糊涂

**有架构**：
- ADR 规定："所有 client-server 通信用 GraphQL"
- **所有 agent 跟同 pattern**

### 数据库设计冲突

**没有架构**：
- Agent A 用 snake_case 列名
- Agent B 用 camelCase 列名
- **结果**：schema 不一致，查询混乱

**有架构**：
- Standards 文档规定命名约定
- **所有 agent 跟同 pattern**

### 状态管理冲突

**没有架构**：
- Agent A 用 Redux 管全局 state
- Agent B 用 React Context
- **结果**：多种 state management 方案，复杂度爆炸

**有架构**：
- ADR 规定 state management 方案
- **所有 agent 一致实施**

## 架构如何防冲突

### 1. 显式 ADR（Architecture Decision Records）

每个重要技术选择文档化：

- **Context** —— 为何这个决策重要
- **Options considered** —— 存在什么替代
- **Decision** —— 我们选了什么
- **Rationale** —— 为何选它
- **Consequences** —— 接受什么 trade-offs

### 2. FR / NFR 特定指南

架构把每个 functional requirement 映射到技术方案：

```
FR-001: 用户管理     → GraphQL mutations
FR-002: 移动应用     → 优化查询
```

### 3. 标准与约定

显式文档：

- 目录结构
- 命名约定
- 代码组织
- 测试 pattern

## 架构作为共享 Context

> "Think of architecture as the shared context that all agents read before implementing"

```
PRD:         "What to build"
              ↓
Architecture: "How to build it"
              ↓
Tasks:        "What each agent does"
```

所有 agent 实施前**都读架构**——架构是统一视角的"宪法"。

## 与 vault 已有概念的关系

| vault 已有 | 在 BMad 防 agent 冲突中的体现 |
|---|---|
| [[concepts/bmad-preventing-agent-conflicts]]（本页）| BMad 用 ADR + standards 实现同一目标 |
| [[concepts/claude-code-hooks-lifecycle]] | hooks 也是"统一行为"的载体——但 hooks 是运行时，ADR 是设计时 |
| [[concepts/agent-team-mailbox-protocol]] | Mailbox 让 agent 间通信**有标准**——避免 ad-hoc schema |
| [[concepts/agent-team-race-condition-task-claim]] | "任务分配冲突"是 BMad 防冲突的另一面——不让多个 agent 抢同一任务 |

## ADR 在工程实践中的地位

ADR 不只是 BMad 的概念——是软件架构的标准模式：

- **MADR** (Markdown ADR) —— 业界常用格式
- **Y-statements** —— "In the context of X, facing Y, we decided for Z, to achieve A, accepting B"
- **Lightweight ADRs** —— 单文件，简单 5 字段

BMad 的 ADR 模板可对应 vault 内 [[concepts/deterministic-agent-memory]] 的"decision memory"层——[[concepts/agent-operating-system]] 五层中的 ADR 层。

## Related

- [[concepts/bmad-build-workflow]] — Build 工作流依赖上游 planning
- [[entities/bmad-named-agent]] — Winston (Architect) 守 Solutioning 阶段
- [[concepts/agent-team-race-condition-task-claim]] — "任务冲突"的运行时另一面
- [[concepts/agent-team-mailbox-protocol]] — "通信 schema 冲突"的护栏