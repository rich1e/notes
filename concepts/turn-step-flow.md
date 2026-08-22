---
title: "Turn-Step Flow — Agent Loop 执行模型"
category: concepts
tags:
  - agent-loop
  - turn
  - step
  - waterfall
  - session-event
  - concept
summary: "dsh agent loop 的 turn/step 模型：turn = drain admitted input（一次 drain）；step = 一次模型请求 + 它引发的工具调用；turn 包含 0+ steps。turn 内的事件流：turn/start → agent/pre-step → step/start → agent/request → llm/stream → assistant/chunk* → tool/call* → tools/* → step/end → turn/end。"
sources:
  - "https://github.com/deepseek-ai/deepseek-harness/blob/main/docs/architecture.md"
created: "2026-08-14T01:28:00Z"
updated: "2026-08-14T01:28:00Z"
provenance:
  extracted: 0.95
  inferred: 0.04
  ambiguous: 0.01
base_confidence: 0.78
lifecycle: draft
lifecycle_changed: "2026-08-14"
tier: supporting
relationships:
  - target: "[[entities/deepseek-harness]]"
    type: derived_from
  - target: "[[concepts/cordis-plugin-framework]]"
    type: extends
  - target: "[[concepts/durable-session-log]]"
    type: related_to
---

# Turn-Step Flow — Agent Loop 执行模型

> dsh 的 agent 循环抽象：turn 是单位执行，step 是 turn 内的模型请求。三种事件语义：durable session event / live waterfall / serial。

## 三层时间单位

| 单位 | 定义 | 持续时间 |
|---|---|---|
| **step** | 一次模型请求 + 它引发的所有工具执行 | ~秒-分钟 |
| **turn** | drain admitted input 的整个过程（0+ steps）| ~分钟-小时 |
| **round** | 外层策略迭代（如 goal round 或 Ralph 一次 fresh agent attempt）| 多 turn |

**关键区别**：
- **step counter** 按每个 step 自增
- **round counter** 属于外层策略，不数 turn
- **goal round counter** 同 round counter

## 完整 turn 流

```
turn/start
  claim next-step input + one queued message
  assemble prompt sections + tool schemas
  → agent/pre-step                    reject | enter(messages)
     reject, or first enter rewritten empty → close turn with no step
     step/start
     append entered messages as user/message
     derive model history from session log
     → agent/request → llm/stream → assistant/chunk* → assistant/message
     → tool/call* → tools/pre-execute → tools/execute → tools/post-execute → tool/result*
     step/end
     tools owe another request, or next-step input arrived → claim → next step
  → agent/turn-stopping
turn/end
```

## 事件分类

### Durable session events（写入 log）

| Event | 时机 |
|---|---|
| `turn/start` | turn 打开 |
| `turn/end` | turn 关闭 |
| `step/start` | step 打开 |
| `step/end` | step 关闭 |
| `user/message` | 用户消息 appended |
| `assistant/chunk*` | 模型流式输出 |
| `assistant/message` | 完整助手消息 |
| `tool/call*` | 工具调用 |
| `tool/result*` | 工具结果 |

### Live waterfall events（可拦截 + 必须 next()）

| Event | 用途 |
|---|---|
| `agent/pre-step` | 改写 / 拒绝 next-step input |
| `agent/request` | 拦截模型请求 |
| `llm/stream` | 拦截模型流 |
| `tools/pre-execute` | 工具执行前 |
| `tools/execute` | 工具执行中 |
| `tools/post-execute` | 工具执行后 |

**关键约束**：不调 `next()` = short-circuit 链路。

### Live serial events（通知类，无 next()）

| Event | 用途 |
|---|---|
| `agent/turn-stopping` | turn 终止（无 next()）|

## 输入分发

- **Input reaches the driver through one inbox** — 单一 inbox
- **Some messages wake it immediately** — 立即唤醒
- **Injected context waits in the inbox until another message does** — 注入的 context 等其他消息

> "The driver materializes a goal round as one goal-sourced turn, which can contain zero or more steps; unrelated human turns in the same session do not consume the goal-round cap."

- Goal round = 一个 goal-sourced turn
- 无关的人类 turn 不消耗 goal-round 配额
- Session log 仍是 source of truth

## 关键语义点

### 1. `agent/pre-step` 决定模型看见什么

```
agent/pre-step fires
  → listener may rewrite claimed messages
  → listener may reject outright
  → rejected / empty first claim → close durable turn (no step spent)
```

**重要**：即使 turn 没产生 step（input 被拒绝），也会写一条 durable `turn/end`（session log 记录这个 attempt）。

### 2. Model history 从 log 派生

```
session log ──deriveMessages()──→ model history
```

不是「每次重新构建 history」，而是**从 log 重放**。这是 dsh 实现 fork / resume / transcript / telemetry 的基础。

### 3. 多个 step 在同一 turn

```
turn
  step 1 (model request + 5 tool calls)
  step 2 (model request + 0 tool calls, final)
  step 3 (model request, goal achieved)
turn/end
```

**何时新增 step**：
- tools owe another request（工具结果触发了下一步模型调用）
- next-step input arrived（用户中途输入）

### 4. Cancel / Error recovery

→ 详细机制见 `core/agent` `core/agent-loop` 的 `the-agent-handle` 文档

## 与其他 agent loop 对比 (^[inferred])

| 维度 | dsh | Claude Code | LangGraph |
|---|---|---|---|
| **Turn 抽象** | explicit | implicit | node-level |
| **Step 抽象** | explicit (model request + tools) | implicit | per-node |
| **取消机制** | `agent/turn-stopping` | SIGINT/Ctrl+C | node interrupt |
| **事件可拦截** | waterfall events | 无 | state hooks |
| **历史来源** | session log replay | context buffer | state graph |
| **Goal 抽象** | explicit (goal round) | none | none |

dsh 的独特之处：**显式 turn/step 抽象 + waterfall 可拦截 + log replay** — 三件套组合让 fork / resume / telemetry 成为免费副产品。

## 反向论证

| 误区 | 实际 |
|---|---|
| 「turn = 一个用户消息」 | 可能是 0 个（被拒绝）或多个 steps |
| 「step = 一个 tool call」 | step 是「一次模型请求」，可能 0+ tool call |
| 「tool 不响应就 crash」 | `tools/post-execute` waterfall 可恢复 |
| 「Session log 是 message buffer」 | 是 **facts 序列**，不是 message buffer |

## Open Questions

1. **Subagent 的 turn 是否独立计数** — 大概率是，但 lineage 怎么算 ^[ambiguous]
2. **Goal round 嵌套** — 同一 turn 内能否有 sub-goal？^[ambiguous]
3. **`assistant/chunk*` 的粒度** — token 级 / sentence 级 / 段落级 ^[inferred] token 级

## 相关页面

- [[entities/deepseek-harness]] — dsh 实现
- [[concepts/cordis-plugin-framework]] — waterfall 事件机制
- [[concepts/durable-session-log]] — log 作为 model history 源
- [[concepts/ralph-loop]] — Ralph round 与 turn 的关系