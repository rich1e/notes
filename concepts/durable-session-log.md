---
title: "Durable Session Log — Model History 的 Source of Truth"
category: concepts
tags:
  - session-log
  - session-event
  - durability
  - model-history
  - event-sourcing
  - concept
summary: "dsh 的 durable session log：append-only 的 SessionEvent 序列，是 model history 的 source of truth（不是 message buffer）。fork / resume / transcript / telemetry 全部从 log 派生。invariant：「Model-visible ⟺ logged」— 任何到模型的内容必须能从 log 重建。"
sources:
  - "https://github.com/deepseek-ai/deepseek-harness/blob/main/docs/architecture.md"
  - "https://github.com/deepseek-ai/deepseek-harness/blob/main/AGENTS.md"
created: "2026-08-14T01:28:00Z"
updated: "2026-08-14T01:28:00Z"
provenance:
  extracted: 0.95
  inferred: 0.04
  ambiguous: 0.01
base_confidence: 0.78
lifecycle: draft
lifecycle_changed: "2026-08-14"
tier: core
relationships:
  - target: "[[entities/deepseek-harness]]"
    type: derived_from
  - target: "[[concepts/turn-step-flow]]"
    type: related_to
  - target: "[[concepts/deterministic-agent-memory]]"
    type: related_to
  - target: "[[entities/sqlite]]"
    type: related_to
  - target: "[[entities/postgresql]]"
    type: related_to
---

# Durable Session Log — Model History 的 Source of Truth

> dsh 的核心数据抽象：`SessionEvent` 的 append-only 序列。不是 message buffer — 是 **facts 序列**。所有 model history、fork、resume、transcript、telemetry 都从它派生。

## 核心 invariant

> "**Model-visible means logged.** Anything that reaches a model request must be reconstructable from the log, and a runtime invariant asserts it. This is why a new model-visible input requires a new session event: extend `SessionEventMap` and render from the log."

**「Model-visible ⟺ logged」**：如果你想让模型看到某事：
1. 定义新的 SessionEvent 类型（extend `SessionEventMap`）
2. 在某个时间点 emit 它
3. 在 `deriveMessages()` 中渲染
4. 模型下次请求时自动看到

**反之亦然**：如果不写 log，模型看不见。

## SessionEvent 分类

### 必需 logged 的（model-visible）

| Event | 用途 |
|---|---|
| `turn/start` / `turn/end` | turn 边界 |
| `step/start` / `step/end` | step 边界 |
| `user/message` | 用户输入 |
| `assistant/chunk*` | 模型流式输出（保留 replay / UI fidelity）|
| `assistant/message` | 完整助手消息 |
| `tool/call*` | 工具调用 |
| `tool/result*` | 工具结果 |

### Live-only（不 logged）

- `agent/pre-step`、`agent/request`、`llm/stream` 等 waterfall 事件
- `agent/turn-stopping` 等 serial 事件
- 它们是**操作**而非事实

### Registry-subject（不 logged，registry 变化）

- 工具注册 / 移除
- plugin mount / unload

## SessionEventMap — 类型化扩展点

```typescript
declare module '@deepseek-ai/dsh' {
  interface SessionEventMap {
    'session/start': SessionStartEvent;
    'session/end': SessionEndEvent;
    'turn/start': TurnStartEvent;
    // ... 
  }
}
```

**机制**：TypeScript declaration merging — 新增一个事件 = 写一个 declare 文件扩展 `SessionEventMap`：
- `SessionEventMap` 成员默认 **required-on-read**
- 不知道事件类型的构建（早于 declare）会**拒绝 log** 除非 envelope 带 `ignorable: true`
- 仅**结构化格式变化**触发 `SESSION_FORMAT_VERSION` bump

## deriveMessages() — 从 log 派生 model history

```
session log (SessionEvent[])
       │
       ▼
  deriveMessages()
       │
       ▼
  model history (Message[])  ←─ 模型实际看到的
```

**关键属性**：
- `assistant/chunk*` 保留 — 用于 replay / UI 还原
- 不是「压缩到 message buffer」— 是「保留完整事实 + 重新渲染」
- fork 时从某 boundary 截取，resume 时从某 checkpoint 截取

## 三大反直觉设计

### 1. Fork 不复制 state，而是定义 boundary

```typescript
const childSession = ctx.sessions.fork(
  source,                    // 父 session id
  boundary: SessionId,       // 从哪个事件开始 fork
  childSessionId: SessionId, // 新 session id
);
```

- Fork 是**逻辑操作**，不是物理复制
- 物理：两个 session 共享 log 段直到 boundary
- 之后各自 append 自己的 events

### 2. Resume = 重新 derive

```typescript
const resumedSession = ctx.sessions.resume(sessionId);
// 自动 deriveMessages + 在 next-step 触发
```

不需要「保存 current state」—— log 是 source of truth，resume 就是 re-derive。

### 3. Telemetry 是 log 的纯函数

```typescript
const tokensUsed = ctx.sessions
  .query(sessionId)
  .reduce((sum, event) => sum + (event.tokens || 0), 0);
```

telemetry / billing / debugging 都是 log 的 query。

## Pre-release 兼容性策略

> "Remove this section at the first tagged release. With no external consumers, prefer the correct foundation over compatibility shims."

- `SESSION_FORMAT_VERSION = 0`（无兼容性承诺）
- 字段重命名、event type 删除 = 自由做
- [[entities/sqlite|SQLite]] 同样用 monotonic `SCHEMA_VERSION`
- 旧的 on-disk 格式直接 reject（不写迁移代码）

## 与其他 session 抽象对比

| 维度 | dsh | LangGraph | Claude Code |
|---|---|---|---|
| **数据模型** | append-only SessionEvent 序列 | state graph（节点 + edge）| conversation messages |
| **Source of truth** | log（event sourcing）| state 值 | messages buffer |
| **Fork 模型** | | boundary 截取 | 复制 messages |
| **Resume 模型** | re-derive | re-execute graph | 重读 messages |
| **Model-visible input** | 必须 logged | 必须 in state | 在 messages |

## 反向论证

| 误区 | 实际 |
|---|---|
| 「log 只是 message buffer」 | 是 facts 序列 |
| 「fork 复制数据」 | log-level boundary |
| 「resume 需要 save state」 | re-derive |
| 「可以偷偷给模型塞东西」 | invariant 会 reject（除非 logged）|

## Open Questions

1. **Log 的 storage backend** — [[entities/sqlite|SQLite]] 默认？是否支持 [[entities/postgresql|PostgreSQL]]？^[ambiguous]
2. **Retention policy** — session 多久过期？可配置吗？^[ambiguous]
3. **Streaming render 策略** — chunks 是否在 fork 时合并？^[inferred] 应合并

## 相关页面

- [[concepts/turn-step-flow]] — log 中的事件流
- [[concepts/cordis-plugin-framework]] — events 的 Cordis 类型化机制
- [[concepts/deterministic-agent-memory]] — vault 已有相似主题
- [[entities/deepseek-harness]] — dsh 实现
- [[synthesis/concepts-sqlite-as-file-format × concepts-durable-session-log]] — synthesis: SQLite fopen() 哲学与 session log 可重建性的交汇