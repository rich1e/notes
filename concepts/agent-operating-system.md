---
title: "Agent Operating System (AOS)"
category: concepts
tags: [agent-architecture, memory, handoff, compact, ai-agents, llm]
sources:
  - "_raw/agent-operating-system.txt"
source_url: "_raw/agent-operating-system.txt"
created: "2026-07-31"
updated: "2026-07-31"
summary: "AOS 是支持多会话连续 AI 工作流的 agent 架构框架：五层 memory 分工(Handoff / Auto / claude-mem / ADR / Knowledge Base)+ compact checkpoint 模板 + 事件驱动更新策略。"
provenance:
  extracted: 0.85
  inferred: 0.10
  ambiguous: 0.05
base_confidence: 0.70
lifecycle: draft
lifecycle_changed: "2026-07-31"
tier: supporting
---

# Agent Operating System (AOS)

## 核心命题

**多会话连续 AI 工作流**是 agent 系统的根本难题——单次会话窗口有限、上下文会丢、跨任务无连续性、跨 session 无 handoff。AOS 是把"agent 当操作系统"的设计框架:把 memory 拆成**职责单一的五层**,用**事件驱动**而非 end-of-session 总结来更新,并把 **compact 当同步点**而非"备份点"。

> 区别于 [[concepts/claude-mem-memory-architecture]](只解决 observation 压缩注入的局部问题),AOS 是把整个 agent 的 memory 子系统当操作系统内核来设计。

## 五层架构

每层**单一职责**——一种信息只存在最合适的一层,避免重复与互相覆盖。

| 层 | 作用 | 存储 | 何时更新 | 不应存 |
|---|---|---|---|---|
| **Handoff (Task Memory)** | 任务进展 + 当前上下文交接 | 任务状态、进度、待办、上下文摘要 | 任务进展 / handoff / compact 前后 | 详细推理、长期知识、历史决策 |
| **Auto Memory (Working Memory)** | 当前 session 工作记忆 | 短期推理、步骤、临时信息 | 每次推理 / 任务推进 | 长期知识、标准、决策记录 |
| **claude-mem (Semantic Memory)** | 长期语义知识沉淀 | 稳定知识点、通用事实、可迁移经验 | 发现长期有用知识 / compact 后筛选 | 任务特定细节、一次性信息 |
| **ADR Memory (Decision Memory)** | 重要决策及其理由 | 架构决策、理由、权衡、替代方案 | 重大决策时 / compact 后回顾 | 实现细节、未决策内容 |
| **Knowledge Base (Knowledge Memory)** | 标准、规范、长期知识库 | 设计标准、规范、通用规则、最佳实践 | 知识沉淀、标准变更 | 临时推理、任务状态、个人偏好 |

### 拓扑

```
Human
  │
  ▼
Handoff (Task Memory)
  │
  ▼
Auto Memory (Working Memory)
  │
  ▼
claude-mem (Semantic Memory)
  │
  ▼
ADR Memory (Decision Memory)
  │
  ▼
Knowledge Base (Knowledge Memory)
  │
  ▼
Git Repository（事实层沉淀）
```

### 各层在已有 vault 中的对应物 ^[inferred]

| AOS 层 | vault 已有页面 |
|---|---|
| Handoff | [[skills/claude-code-token-optimization]] 中"compact checklist"思路;`hot.md` 续接机制 |
| Auto Memory | 当前 session 的对话上下文(无显式存档) |
| claude-mem | [[concepts/claude-mem-memory-architecture]] · [[entities/claude-mem]] · [[skills/claude-mem-memory-usage]] · [[synthesis/Research: claude-mem 长期记忆]] |
| ADR Memory | `projects/*` 中"决策记录"型段落;`hot.md` Flagged Contradictions 段 |
| Knowledge Base | `concepts/` + `references/` + `synthesis/` + `_meta/taxonomy.md` |

## Compact 的影响

**Compact 丢的不只是信息,而是推理轨迹**——未完成细节、失败尝试、隐含约束全失。Compact 后 agent 只能保留精简后的核心知识与决策,过程性内容被吞。

因此 memory 层设计时必须区分:
- **应沉淀**(过程会复现的):决策理由、关键证据、未解之谜
- **可丢弃**(临时性):本次尝试的命令、失败的探索路径

## Compact Checkpoint 模板

把 compact 当同步点(checkpoint 而非 backup),推以下模板:

```
## Done
- 已完成的任务、阶段性成果

## Todo
- 待办事项、后续任务

## Decisions
- 已作出的关键决策及理由

## Risks
- 已识别的风险与不确定性

## Open Questions
- 尚未解决的问题

## Next Actions
- 下一步具体行动

## Candidate Long-term Memories
- 候选的长期知识点/经验
```

> 这是本框架的核心交付物——一个可复用的 compact 时刻输出格式,把 7 个固定段落当 handoff 协议使用。

## 事件驱动的 Memory Workflow

**反对** end-of-session 大总结模式(信息衰减严重),改成事件驱动:

| 事件 | 触发更新到 |
|---|---|
| 重要决策 | ADR Memory |
| 长期知识发现 | claude-mem |
| 标准/规范变更 | Knowledge Base |
| 任务进展/交接 | Handoff |
| compact 发生 | checkpoint(触发 Handoff 同步) |

## 设计原则

- **单一职责**:每层只负责一种信息
- **避免重复**:信息只存最合适的一层
- **增量更新**:事件驱动 > end-of-session 总结
- **compact 是同步点而非备份点**:确保关键进展已 checkpoint
- **与模型无关**:memory 结构应支持多种模型/agent 互操作

## 实操判断 ^[inferred]

- **小任务 / 单 session**:五层架构"过度工程化",用 Auto Memory + 偶尔 checkpoint 足够
- **多 session 持续任务**:五层必须有,否则上下文丢失
- **团队 / 跨人协作**:Handoff 与 ADR 必须显式化(不能让"在脑子里")
- **端到端长流程**(几周到几个月):Knowledge Base 必须有 owner 与 review 节奏,否则会变成垃圾场

## 与现有工具栈的关系 ^[inferred]

- **claude-mem 插件**:对应 Semantic Memory 层(observation 压缩 + 注入);不能单独承担其他四层
- **Claude Code hooks lifecycle**:天然适合做"事件驱动"的载体——`PostToolUse` 触发观察、`SessionStart` 注入、`Stop` 触发 checkpoint
- **Git Repository**:Knowledge Base 的事实层(决策、规范、标准最终落到文件可追溯)
- **`hot.md` 续接机制**:本质是手工版的 Handoff 同步,本框架可视为其形式化
- **Agent Handoff Kit**:**Handoff (Task Memory) 层的工具化落地**——`SESSION_HANDOFF.md` 交接文件 = Task Memory,「收工」= compact checkpoint 同步点,`RULE_PACKS.md` = 按任务加载工作规则;补足了 claude-mem 未覆盖的 Handoff/治理层 ^[inferred] [[misc/web-adamchanadam-github-io-agent-handoff-kit]]

## 相关

- [[misc/web-adamchanadam-github-io-agent-handoff-kit]] — Handoff 层的现成工具实现(npm 包)
- [[concepts/claude-mem-memory-architecture]] — Semantic Memory 层的技术实现
- [[concepts/claude-code-hooks-lifecycle]] — 事件驱动机制的载体
- [[synthesis/Research: claude-mem 长期记忆]] — 单层深度研究,本框架覆盖更广
- [[entities/claude-mem]] — 插件实体
- [[skills/claude-code-token-optimization]] — Token 维度的 compact 纪律
- [[concepts/ai-agent-node-pattern]] — AI agent 节点范式(本框架适用对象)

## 关联关系

```yaml
extends:
  - "[[concepts/claude-mem-memory-architecture]]"  # 把单层扩展为多层
related_to:
  - "[[concepts/claude-code-hooks-lifecycle]]"    # 事件驱动载体
  - "[[concepts/ai-agent-node-pattern]]"          # 适用对象
  - "[[misc/web-adamchanadam-github-io-agent-handoff-kit]]"  # Handoff 层工具化落地
uses:
  - "[[entities/claude-mem]]"                     # Semantic Memory 实现
```