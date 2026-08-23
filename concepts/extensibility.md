---
title: "扩展性模式 (Extensibility Patterns)"
category: concepts
tags: [extensibility, plugin, hook, capability-seam, architecture]
sources: []
summary: 软件系统通过扩展点（plugin / hook / capability seam / 模块加载器）允许第三方扩展而无需修改核心代码。常见模式：插件注册表（registry）、依赖反转（DI 容器）、事件总线、零注册中心 require.resolveWeak。
base_confidence: 0.6
provenance:
  extracted: 0.0
  inferred: 0.0
  ambiguous: 0.0
lifecycle: draft
lifecycle_changed: 2026-08-24
tier: supporting
---

# 扩展性模式

## 占位说明

此页面是 **stub**，由 `/wiki-lint --consolidate` cross-linker 阶段自动创建，用于满足 `[[concepts/extensibility]]` 的 3 处引用（来自 [[projects/flow-design-system]] 子页）。

## 概要

扩展性是软件系统在**不修改核心代码**的前提下被第三方扩展的能力。常见模式：

| 模式 | 例子 | 优缺点 |
|---|---|---|
| **Plugin Registry** | webpack plugins、babel plugins、cordis plugins | 显式、静态可发现；耦合到 registry |
| **Hook / Lifecycle** | WordPress actions/filters、tap、mocha hooks | 灵活；调用顺序与并发语义隐式 |
| **Capability Seam** | dsh / cloud IDE 接口、Anthropic Agent Teams | 替换 provider 时整个产品栈跟着换；接口契约成本高 |
| **零注册中心 require** | `require.resolveWeak('@/modules/...')` | 无 registry，目录即配置；运行时错误才能发现缺页 |
| **事件总线 / Event Bus** | Cordis event、Node EventEmitter | 解耦；但事件流难以调试 |

## 相关

- [[projects/flow-design-system/concepts/dynamic-require-resolveweak-loading]] — 零注册中心的运行时动态加载
- [[concepts/cordis-plugin-framework]] — Cordis 三件套 (Service/Event/Effect)
- [[concepts/capability-seam]] — dsh 的 capability 设计