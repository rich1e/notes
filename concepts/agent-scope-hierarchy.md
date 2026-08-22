---
title: "Agent Scope Hierarchy — Per-Agent Registration & Scoped Dispatch"
category: concepts
tags:
  - cordis
  - agent-scope
  - scope-key
  - shadowing
  - scoped-dispatch
  - concept
summary: "Cordis agent scope 模型：scope = 单 agent 注册的 per-agent 注册单位（global vs scoped 两层，扁平）；scope key = opaque 标识（habit：live agent 自己）；agent.ctx = scope-scoped 上下文；scoped dispatch 按 scope carrier 过滤；shadowing 解决同名注册；setup window 是创建期 slot。"
sources:
  - "https://github.com/deepseek-ai/deepseek-harness/blob/main/docs/glossary.md"
created: "2026-08-14T01:28:00Z"
updated: "2026-08-14T01:28:00Z"
provenance:
  extracted: 0.93
  inferred: 0.05
  ambiguous: 0.02
base_confidence: 0.75
lifecycle: draft
lifecycle_changed: "2026-08-14"
tier: supporting
relationships:
  - target: "[[concepts/cordis-plugin-framework]]"
    type: extends
  - target: "[[entities/deepseek-harness]]"
    type: derived_from
---

# Agent Scope Hierarchy — Per-Agent Registration & Scoped Dispatch

> Cordis 的 agent scope 模型：scope = 单 agent 注册的 per-agent 注册单位。dsh 用这套机制支持 per-agent persona、per-agent tool-variant、subagent delegation 等。

## 核心定义

| 术语 | 定义 |
|---|---|
| **scope** | per-agent 注册单位。贡献（tool、prompt section、variable、restriction、listener）要么 **global**（所有 agent 可见）要么 **scoped**（只一个 agent 可见）。 |
| **scope key** | opaque 标识，对象身份比较。**约定**：live agent 是它自己 scope 的 key。 |
| **agent.ctx** | agent 的 scoped context。通过它注册的 = scope-visible AND scope-lifetime（一个事实驱动两者）。 |
| **scope carrier** | scope-filtered dispatch 的 `thisArg`（`scopeTarget` 构建）。**subject-less** carrier（无 key）只接收 untagged listener。 |
| **scoped dispatch** | 关于一个 agent 的事件 = 用那个 agent 的 carrier dispatch。关于注册表的事件（工具被加入）= **registry-subject**，保持 unfiltered。 |
| **shadowing** | most-specific-wins：scoped tool/section/variable 替换同名 global，但只对该 scope 替换。 |
| **restriction** | `tools.restrict` 过滤 GLOBAL tool 集合（按 intersection 组合），scoped-local 注册在 filter 之后合并。 |
| **scope-local registration** | scoped 注册，scope 内可见 |
| **setup window** | 创建 slot（`CreateAgentOptions.setup`）：scope + agent 对象已存在但未发布前，注册用。`agent/session-start` 触发或首次 prompt 组装前。Setup 注册；不驱动 agent。 |
| **lineage** | parent/child 事实作为数据（`parentSession`、durable `delegationDepth`、runtime `subagentDepth`）。**不影响可见性**。 |

## 两层模型

```
┌─────────────────────────────────┐
│         GLOBAL context          │  所有 agent 可见
│  - tools, prompt sections, ...   │
└─────────────────────────────────┘
            │
            ▼ scope visibility filter
┌─────────────────────────────────┐
│         AGENT scope             │  只此 agent 可见
│  - tools.restrict: [subset]     │
│  - shadowed tools/sections      │
└─────────────────────────────────┘
```

**关键反直觉点**：

> "Scoped registrations do not inherit down to subagents; subtree behavior is expressed with lineage data, never scope structure."

- 子 agent **不**继承父 agent 的 scope
- 「家族树」行为用 **lineage data** 表达（parentSession / delegationDepth / subagentDepth）
- lineage 不影响可见性 — 它是数据，不是结构

## Shadowing — 同名解析

```
Global:  tool "Bash"      (registered globally)
Scope A: tool "Bash"      (replaces Global for A only)
Scope B:                   (uses Global)
```

**shadowing 规则**：
- 工具请求在 scope A 时 → Scope A 的 Bash（如果存在），否则 Global
- 工具请求在 scope B 时 → Global 的 Bash
- **不修改 Global**，只是 A 的请求被替换

这是 per-agent persona 和 per-agent tool-variant 的实现机制。

## Restriction — 全局工具的子集过滤

```typescript
ctx.agent(agentKey).restrict({
  tools: ['Bash', 'Read']   // 只允许这 2 个 tool
});
```

**行为**：
- Global tool set 先按 intersection 过滤
- 然后 scope-local 注册**合并**（追加，不是替换）
- 被过滤掉的全局 tool：
 - **不显示在 prompt 中**
 - **执行请求也拒绝**（与「不存在」行为一致 — 用户无法区分）

**安全含义**：restriction = 强边界，agent **不知道**有被禁的工具。

## Scope-local Registration

```typescript
// 创建 agent
ctx.createAgent({
  setup: (agentCtx) => {
    // scope-local: 只此 agent 可见
    agentCtx.effect(() => {
      agentCtx.tools.register(myCustomTool);
      agentCtx.prompt.addSection('myAgentPersona', personaPrompt);
    });
  },
});
```

**生命周期**：agent unload 时 scope-local 注册自动 dispose。

## Scope Carrier — Dispatch 过滤机制

事件 dispatch 时带一个 `scope carrier`：

```
agent/pre-step fires
  → carrier = agent.ctx  (subject = this agent)
  → dispatch to:
     - untagged listeners (always receive)
     - listeners registered to this agent's scope (always receive)
     - listeners registered to other scopes (skipped)
```

**Subject-less carrier**（无 scope key）：
- 只接收 untagged listener
- 用于「关于注册表本身」的事件（tool 注册 / 移除）

**Registry-subject events**：明确 unfiltered，**意图**就是通知所有 listener（无论 scope）。

## Setup Window — 创建期 Slot

```typescript
ctx.createAgent({
  setup: (agentCtx) => {
    // 这里是 setup window
    // agent + scope 已存在，但还没发布
    // agent/session-start 没触发
    // 首次 prompt 没组装
    agentCtx.tools.register(scopeOnlyTool);
  },
});
```

**规则**：
- Setup 只 **注册**；不**驱动** agent（不发事件、不跑 prompt）
- 在 setup 完成前可注册；在 setup 后到首次 publish 之间的窗口很窄
- 用途：构造 agent 的 scoped world（persona + tools + restrictions）

## Lineage — 家族树数据

```typescript
{
  parentSession: 'session-A',     // 父 session id
  delegationDepth: 2,            // 委托深度（durable）
  subagentDepth: 1               // 运行时深度（不存）
}
```

**重要**：lineage 是**数据**，不是结构。

> "Subtree behavior is expressed with lineage data, never scope structure."

如果想实现「子 agent 看不到父 agent 的某个工具」—— **不是**用 scope，是用 lineage + filter 显式做。

## dsh 中的实际应用

| 场景 | 实现 |
|---|---|
| **Per-agent persona** | scoped prompt section |
| **Per-agent tool variant** | shadowing（同名 scoped tool 替换 global）|
| **Subagent 隔离** | setup window 里 restrict + scoped tools |
| **Delegation 上下文** | lineage + 子 agent setup 时引用父 |
| **Goal 路由** | scope carrier 让 goal 事件只到 relevant agent |

## 与传统 OOP 继承对比 (^[inferred])

| 维度 | dsh Scope | OOP 继承 | React Context |
|---|---|---|---|
| **嵌套** | 扁平（两层）| 多层继承树 | Provider tree |
| **数据传递** | **显式 lineage** | 隐式（super.method()）| Provider value |
| **可见性** | 严格 scope 边界 | 受保护 | 默认向下 |
| **替换** | shadowing | override | re-render |

dsh 的设计哲学：**所有 family 关系都是数据，不是结构** — 这让测试和调试更简单。

## 反向论证

| 误区 | 实际 |
|---|---|
| 「子 agent 继承父 agent 的 tool」 | **不**继承 — 要显式传 |
| 「scope 是树」 | 扁平两层，lineage 是数据 |
| 「restriction 是 soft 限制」 | **硬**限制 — 工具既不在 prompt 也不能执行 |
| 「scope-local 注册 = global 注册」 | scope-local 有自己的生命周期（agent unload 时清）|

## Open Questions

1. **跨 agent 的 event 多播** — 是否要全 broadcast？当前是 scope-filtered ^[ambiguous]
2. **Scope 的 garbage collection** — agent unload 后 scope 还存在吗？^[ambiguous]
3. **Lineage 的循环检测** — A 是 B 的父，B 是 A 的父会怎样？^[inferred] 应该报错

## 相关页面

- [[concepts/cordis-plugin-framework]] — 三件套的基础
- [[concepts/capability-seam]] — 服务定义层面的扩展
- [[concepts/turn-step-flow]] — event 在 agent 循环中如何 dispatch
- [[entities/deepseek-harness]] — dsh 实现