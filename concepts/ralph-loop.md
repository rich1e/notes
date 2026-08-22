---
title: "Ralph Loop — Fresh-Agent Workflow Toward Immutable Objective"
category: concepts
tags:
  - ralph-loop
  - fresh-agent
  - workflow
  - immutable-objective
  - handoff
  - concept
summary: "dsh 的 Ralph loop 抽象：一个 fresh-agent workflow run 朝向 immutable objective 推进；不是 same-session goal、不是 agent-loop mode、不是 scheduler、不是通用 workflow 脚本。核心：每个 round = 新建 child session，child 收不到父 / prior-child conversation seed，跨 round 状态靠 shared workspace + bounded Ralph handoff 传递。"
sources:
  - "https://github.com/deepseek-ai/deepseek-harness/blob/main/docs/glossary.md"
created: "2026-08-14T01:28:00Z"
updated: "2026-08-14T01:28:00Z"
provenance:
  extracted: 0.92
  inferred: 0.06
  ambiguous: 0.02
base_confidence: 0.65
lifecycle: draft
lifecycle_changed: "2026-08-14"
tier: supporting
relationships:
  - target: "[[entities/deepseek-harness]]"
    type: derived_from
  - target: "[[concepts/turn-step-flow]]"
    type: related_to
---

# Ralph Loop — Fresh-Agent Workflow Toward Immutable Objective

> dsh 的「Ralph loop」设计模式：一个 foreground fresh-agent workflow run 朝向**immutable objective** 推进。不是 same-session goal、不是 agent-loop mode、不是 scheduler、不是通用 workflow 脚本。

## 显式「不是什么」

> "Ralph loop: one foreground fresh-agent workflow run toward an immutable objective. It is a model-facing tool policy composed from workflow and subagent primitives, **not** a same-session goal, agent-loop mode, scheduler, or generic workflow-script feature."

| 相似概念 | 区别 |
|---|---|
| **same-session goal** | goal 在同一 session 持续推进；Ralph **新建 session** |
| **agent-loop mode** | loop 是循环策略（autonomous / delegate）；Ralph 是 workflow run |
| **scheduler** | scheduler 调度任务在固定时间；Ralph 是 **fresh agent 模式** |
| **workflow-script feature** | workflow 是 dsh 原语；Ralph 是用 workflow + subagent 组装而成 |

## 三个核心术语

| 术语 | 定义 |
|---|---|
| **Ralph loop** | 一个 foreground fresh-agent workflow run，朝向 immutable objective |
| **Ralph round** | 一个 fresh child session。**child 收不到 parent / prior-child conversation seed** |
| **Ralph handoff** | 跨 round 传递的标准化 bounded structured report：status / summary / evidence / next steps / blocker text |

## 为什么 child 收不到 prior conversation

设计哲学：

> "The child receives no parent or prior-child conversation seed; the shared workspace and one bounded Ralph handoff carry cross-round state."

- **不传染上下文污染**：fresh agent 不受之前对话的措辞 / 假设 / 偏见影响
- **强制 explicit handoff**：状态必须由 handoff 结构化传递，而不是隐式继承
- **workspace 是 source of truth**：跨 round 的代码 / 文件 / 中间产物存在 shared workspace
- **handoff 是 supplement**：handoff 补充 workspace，不是替代

## Ralph handoff 结构

```typescript
type RalphHandoff = {
  status: 'in_progress' | 'blocked' | 'complete';
  summary: string;          // 简短总结
  evidence: Evidence[];      // 验证材料（命令输出、文件 diff、测试结果）
  nextSteps: string[];       // 下一步要做什么
  blocker?: string;          // 如果 blocked，写明原因
};
```

**bounded**：handoff 不是任意长度的对话，而是**结构化字段**。这迫使 child agent 不依赖 verbatim 对话，而是**自己理解证据**。

## 与其他「长任务」设计对比 (^[inferred])

| 维度 | Ralph loop | LangGraph | Cursor Composer | AutoGPT |
|---|---|---|---|---|
| **子任务 session** | 新 session（fresh）| 同一 graph | 同一 agent | 同一 agent |
| **上下文传递** | workspace + handoff | graph state | shared buffer | shared memory |
| **Handoff 形式** | 结构化 bounded | 任意 state | arbitrary | freeform |
| **上下文污染防御** | fresh agent | 无 | 无 | 无 |

Ralph 的关键创新：**fresh child + bounded handoff** 组合把「长任务」拆成多个独立、可审计的小任务。

## Ralph 与 Goal 的区别

| 维度 | Ralph loop | Goal |
|---|---|---|
| **状态位置** | fresh child session | same session |
| **跨 round 状态** | workspace + handoff | session log |
| **轮次语义** | Ralph round = child session | Goal round = continuation cycle in same session |
| **可重入性** | 高（每个 round 独立） | 低（续接前一回合）|

→ Goal 适合「同一个会话里的持续任务」；Ralph 适合「需要 clean slate 的多步任务」。

## 典型应用场景

| 场景 | 为什么 Ralph |
|---|---|
| **大型重构（multi-PR）** | 每个 PR fresh，证据可审计 |
| **多步骤研究 + 实施** | 每步 fresh 避免 anchor 偏差 |
| **「构建 X 全套」** | 子任务无 cross-contamination |
| **Benchmark / 评测** | 干净环境复现 |

## 反向论证

| 误区 | 实际 |
|---|---|
| 「Ralph = Autonomous mode」 | 不一样；Ralph 是 workflow，autonomous 是 loop mode |
| 「Ralph 自动重试失败」 | 不一定 — 由 handoff status 决定 |
| 「Ralph handoff 越长越好」 | 越 bounded 越好 — 强制 child 理解而非复读 |
| 「Ralph 适合所有长任务」 | 不是 — 需要 continuity 的任务用 goal |

## Open Questions

1. **Ralph 与 fork 的关系** — Ralph round 是不是 fork 的特例？^[inferred] 大概率是
2. **Handoff validation** — schema 校验？还是 freeform？^[ambiguous]
3. **Workspace 冲突** — 多 child 并行时如何仲裁 ^[ambiguous]

## 相关页面

- [[entities/deepseek-harness]] — dsh 实现
- [[concepts/turn-step-flow]] — turn / step / round 关系
- [[concepts/durable-session-log]] — session log 作为 cross-round state 后备
- [[concepts/agent-scope-hierarchy]] — subagent delegation