---
title: "Cordis — Spatiotemporal Plugin Framework"
category: entities
tags:
  - cordis
  - plugin-framework
  - typescript
  - agent-framework
  - entity
summary: "Cordis 框架：基于「Core Dispatch System」的服务 / 事件 / 可逆 effects 三件套；论文 _A Programming Paradigm for Spatiotemporal Composability_。被 DeepSeek Harness (dsh) vendored 作为插件基座。"
sources:
  - "https://github.com/cordiverse/cordis"
  - "https://github.com/cordiverse/paper"
source_url: "https://github.com/cordiverse/cordis"
created: "2026-08-14T01:28:00Z"
updated: "2026-08-14T01:28:00Z"
provenance:
  extracted: 0.75
  inferred: 0.20
  ambiguous: 0.05
base_confidence: 0.55
lifecycle: draft
lifecycle_changed: "2026-08-14"
tier: peripheral
relationships:
  - target: "[[entities/deepseek-harness]]"
    type: related_to
  - target: "[[concepts/cordis-plugin-framework]]"
    type: related_to
---

# Cordis — Spatiotemporal Plugin Framework

> Cordis（可能是「Core Dispatch System」缩写）的 TypeScript 插件框架：服务 + 事件 + 可逆 effects 三件套，是 DeepSeek Harness（dsh）的 vendored 基座。

## 已知信息

| 维度 | 值 |
|---|---|
| **作者** | cordiverse 团队（具体待确认 ^[ambiguous]）|
| **License** | 待 `cordiverse/cordis` 仓库确认 ^[ambiguous] |
| **vendored by** | DeepSeek Harness（manifest + sync 流程在 `vendor/README.md`）|
| **论文** | [_A Programming Paradigm for Spatiotemporal Composability_](https://github.com/cordiverse/paper) |

## 核心抽象（从 dsh 描述推导）

> "Cordis: plugins contribute services, typed events, and reversible effects to a shared context. Every part of the product is a plugin, including the model adapter, the tool registry, the session log, and the agent loop itself."

**三个原始概念**：

1. **Service** — 共享 context 上的命名服务（`ctx.<key>`）
2. **Typed events** — 类型化事件流（waterfall / serial 不同语义）
3. **Reversible effects** — 注册时可逆（plugin unload 自动 cleanup）

**核心反直觉点**：

> "There is no privileged core to patch: you extend dsh by mounting a plugin beside the others, and registrations are effects that unwind when their plugin unloads."

- 没有 privileged core — 任何一部分（包括 agent loop 本身）都是 plugin
- "Extending" = 装载 plugin 即可，不用 fork
- Cleanup 是自动的（effect unwinds on unload）

## 与其他 plugin framework 的对比 (^[inferred])

| 维度 | Cordis | Koa/Middleware | NestJS Module | Spring Bean |
|---|---|---|---|---|
| **生命周期** | 显式 `effect()` + dispose | 中间件链 | Module 装饰器 | 容器管理 |
| **Cleanup 语义** | 自动（effect unwinds）| 手动 | 手动 | 自动（容器）|
| **上下文共享** | shared `ctx` | request-scoped ctx | DI container | DI container |
| **事件模型** | Typed events + waterfall/serial | 无 | 无 | ApplicationEvent |
| **Goal** | 长期运行的 plugin composition | HTTP 请求链 | 完整应用骨架 | 完整应用骨架 |

→ 详细机制见 [[concepts/cordis-plugin-framework]]

## vendoring 模式

DeepSeek Harness 不依赖 npm 上的 Cordis — 而是把整个 Cordis 源码**拉到 `vendor/`** ：

- `vendor/README.md` 包含 manifest + upstream SHAs
- sync procedure 让 vendor 与 upstream 同步
- re-apply 或 retire logged local modifications
- 每次 vendor 更新跑 `pnpm run test && pnpm run build`

> **vendoring 的工程理由** (^[inferred])：
> 1. **基础可控** — 在 pre-release 阶段，core framework 不能自由发版
> 2. **修补空间** — 可以加本地修改而不发 PR 到 upstream
> 3. **性能与体积** — 不引入 npm 间接依赖，便于 monorepo 打包

## 与 vault 已有页面的呼应

- [[entities/deepseek-harness]] — 主要使用方
- [[concepts/cordis-plugin-framework]] — 完整抽象与机制

## Open Questions

1. **Cordis 自身的定位** — 是 dsh 内部项目的开源版，还是独立项目？^[ambiguous]
2. **Spatiotemporal 范式的具体含义** — 论文标题暗示时空组合性；具体机制待读论文 ^[ambiguous]
3. **是否有同类项目的类似抽象**（如 dependency injection / service container 的可逆版本）？^[inferred]
4. **Cordis 自身的成熟度** — 文档、测试、release cadence 等 ^[ambiguous]

## 相关页面

- [[concepts/cordis-plugin-framework]] — 详细抽象
- [[entities/deepseek-harness]] — vendored 使用方
- [Cordiverse paper](https://github.com/cordiverse/paper)