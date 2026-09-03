---
title: "Cordis Plugin Framework — Service/Event/Effect 三件套"
category: concepts
tags:
  - cordis
  - plugin-framework
  - typescript
  - capability-seam
  - registry
  - lifecycle
  - concept
summary: "Cordis 插件框架的三件套：Service（ctx.<key> 共享服务）/ Typed Events（waterfall/serial/registry-subject 三种）/ Reversible Effects（注册时 dispose）。dsh 完全基于此实现「everything is a plugin」，agent loop 本身也是 plugin。"
sources:
  - "https://github.com/cordiverse/cordis"
  - "https://github.com/deepseek-ai/deepseek-harness/blob/main/docs/architecture.md"
  - "https://github.com/deepseek-ai/deepseek-harness/blob/main/docs/glossary.md"
created: "2026-08-14T01:28:00Z"
updated: "2026-08-14T01:28:00Z"
provenance:
  extracted: 0.85
  inferred: 0.12
  ambiguous: 0.03
base_confidence: 0.7
lifecycle: draft
lifecycle_changed: "2026-08-14"
tier: supporting
relationships:
  - target: "[[entities/cordis]]"
    type: derived_from
  - target: "[[entities/deepseek-harness]]"
    type: extends
  - target: "[[concepts/capability-seam]]"
    type: related_to
---

# Cordis Plugin Framework — Service/Event/Effect 三件套

> Cordis 是 dsh 的 vendored 框架基础。其核心抽象：services（共享命名服务）、typed events（类型化事件流）、reversible effects（可逆注册）。

## 三件套

### Service — 共享上下文中的命名服务

```typescript
// 定义
class ShellExecutor extends Service {}

// 注册到 ctx
ctx.plugin(ShellExecutor, { /* impl */ });

// 使用
const shell = ctx.get(ShellExecutor);
await shell.run('ls -la');
```

**约定**：
- `Service` 是 **abstract class**（不是 TypeScript `interface`）— 这样可以承载状态 + 类型注册
- `ctx.<key>` 命名（小驼峰 → 复数：`ctx.tools`, `ctx.agents`）
- 可以是「纯抽象类」如 `ShellExecutor`，也可以是「具体注册表」如 `WebRuntime`

### Typed Events — 类型化事件流

dsh 用 TypeScript declaration merging 给每类事件定义类型化 map：

```typescript
// 在文件 declare.ts 中
declare module '@deepseek-ai/dsh' {
  interface SessionEventMap {
    'session/start': SessionStartEvent;
    'session/end': SessionEndEvent;
  }
}
```

**3 种事件语义**：

| 类型 | 调用模式 | 用途 |
|---|---|---|
| **Waterfall** | listener MUST call `next()` | 拦截 + 改写（`agent/pre-step`、`tools/execute`）|
| **Serial** | listener executes in order, no `next()` | 通知类（`agent/turn-stopping`）|
| **Registry-subject** | unfiltered dispatch | 容器自身变化（工具被注册 / 移除）|

→ 不调 `next()` 的 waterfall listener = short-circuit 链路（默认拒绝 / 跳过）

### Reversible Effects — 可逆注册

```typescript
ctx.effect(() => {
  // 注册动作
  const handle = ctx.tools.register(myTool);
  // 返回 dispose
  return () => handle.dispose();
});
```

**关键性质**：
- plugin unload 时 effect 自动 unwind
- 无需手动管理 cleanup 顺序
- **runtime invariants assert owned relationships** — 不靠 service 存在与否判定状态，查权威 event stream

## Capability Seam — 三件套的具体应用

一个 capability = Service Definition + Service Provider + Consumer 三件套：

| 角色 | 抽象 | 实现示例 |
|---|---|---|
| **Service Definition** | `class ShellExecutor extends Service {}` | `dsh-shell` 包 |
| **Service Provider** | 实际实现 | `dsh-bash-local` / `dsh-bash-sandbox` |
| **Consumer** | 注入服务的代码 | `dsh-tool-bash`（model-facing tool）|

> "A seam is a swappable capability with three roles; adding a capability means designing all three."

**示例**：`packages/shell` 的 canonical 三件套：
- `dsh-shell` 抽象 + `ctx.shell`
- `dsh-bash-local` 提供本地 bash
- `dsh-bash-sandbox` 提供沙箱 bash
- `dsh-tool-bash` 模型侧 tool

**换实现 → 整个产品跟着换**：

> "Filesystem and subprocess providers share one execution world, so pointing them at a remote sandbox moves Bash, PTY, and LSP with them, with no provider forks."

→ 这是 capability seam 的核心价值：**接口统一 = 整个执行栈可平移**

## 「没有 privileged core」的工程含义

dsh 把这个哲学贯彻到底：

> "There is no privileged core to patch: you extend dsh by mounting a plugin beside the others, and registrations are effects that unwind when their plugin unloads."

- **agent loop 本身也是 plugin** — `core/agent-loop` 提供默认 driver，但用户可以挂自己的 loop 替代
- **session log 也是 plugin** — `core/session` 是默认实现，但 fork 时可以替换
- **model adapter 也是 plugin** — 不同 LLM provider 共享 `ctx.llm` 接口

## 与传统 plugin / DI framework 对比 (^[inferred])

| 维度 | Cordis + Service | NestJS DI | Spring Bean |
|---|---|---|---|
| **生命周期** | 显式 effect + dispose | 装饰器 + module | 容器 |
| **Cleanup 语义** | **自动 unwind** | 手动 (OnModuleDestroy) | 自动 (DisposableBean) |
| **事件模型** | **Typed events + waterfall** | 无 | ApplicationEvent (basic) |
| **上下文共享** | shared `ctx` | DI by token | DI by type |
| **嵌套 composition** | profiles + bundles + patches | modules | @Configuration |
| **Goal** | 长期 plugin composition | 完整应用骨架 | 完整应用骨架 |

Cordis 的独特之处：**typed events + waterfall 语义 + 自动 unwind** 三件套，比传统 DI 更适合「agent 系统这种长期运行的 plugin 树」。

## 反向论证

| 误区 | 实际 |
|---|---|
| 「plugin 多了性能差」 | Service 是 lazy lookup；events 是 dispatch 优化 |
| 「没有 core 等于没有设计原则」 | 三件套就是设计原则 |
| 「effect dispose 一定会失败」 | dsh 的 `register()` 返回 disposer，标准模式 |

## Open Questions

1. **Cordis 是否有「scope」概念？** — dsh 有 agent scope，但不确定 Cordis 原生是否提供 ^[ambiguous]
2. **Waterfall 与 interceptor pattern 的关系** — 类似 AOP interceptor，但「必须调 next()」的硬约束更严 ^[inferred]
3. **Cordis 是否支持异步 event？** — dsh 大量使用 event，应该是支持的 ^[inferred]

## 相关页面

- [[entities/cordis]] — 框架本体
- [[entities/deepseek-harness]] — 主要使用方
- [[concepts/capability-seam]] — 三件套的具体应用
- [[concepts/agent-scope-hierarchy]] — scope 概念扩展
- [[concepts/turn-step-flow]] — event 在 agent 循环中的应用

## Related

- [[synthesis/concepts-cordis-plugin-framework × entities-deepseek-harness]] — synthesis
