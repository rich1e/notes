---
title: Zustand — 轻量级 React 状态管理库
category: entities
tags:
  - state-management
  - react
  - f2e
  - zustand
sources:
  - _raw/zustand.txt (Gitingest export, pmndrs/zustand, 2026-07-02)
created: 2026-07-02T01:00:00Z
updated: 2026-08-03T05:47:33Z
summary: Zustand 是 pmndrs 出品的小型 React 状态管理库，基于简化 Flux 原则，无需 Provider，以 Hook 为核心 API，支持 Vanilla/React 双模式。
tier: core
lifecycle: reviewed
lifecycle_changed: 2026-08-03
lifecycle_reason: "auto-promoted by wiki-lint --consolidate: age>30d, confidence>0.7"
base_confidence: 0.85
provenance:
  extracted: 0.9
  inferred: 0.1
  ambiguous: 0
relationships:
  - target: "[[concepts/zustand-core-architecture]]"
    type: related_to
  - target: "[[concepts/zustand-middleware-system]]"
    type: related_to
  - target: "[[concepts/zustand-react-integration]]"
    type: related_to
  - target: "[[synthesis/zustand-core-architecture × zustand]]"
    type: related_to
---

# Zustand — 轻量级 React 状态管理库

**Zustand**（德语"状态"）是由 [pmndrs](https://github.com/pmndrs) 团队开发的小型、快速、可扩展的 React 状态管理库。

- **npm**: `zustand`
- **GitHub**: `pmndrs/zustand`
- **许可证**: MIT
- **理念**: 基于简化 Flux 原则，以 Hook 为核心 API，无样板代码，不强制意见

## 核心特点

- **无 Provider** — store 是全局模块状态，组件无需被 `Context.Provider` 包裹
- **Hook 驱动** — `create()` 返回的是 React Hook，用法极其简洁
- **选择器订阅** — 组件只订阅关心的 state 切片，其他部分变化不触发重渲染
- **React 外可用** — 通过 `createStore()` 创建无 React 依赖的 vanilla store
- **中间件系统** — 通过类型安全的中间件链扩展能力（persist、devtools、immer 等）
- **极小体积** — bundle size 约 1KB（gzip）

## 解决的问题

Zustand 明确处理了 React 状态管理的三个经典难题：

1. **Zombie child problem** — stale props 和 zombie children（react-redux 常见坑）
2. **React Concurrency** — 并发模式下 `useMutableSource` 的正确性
3. **Context loss** — 混合渲染器之间的 context 丢失

## 版本历史要点

- **v4** — 引入 `useStore` hook 用于 vanilla store；推荐用 `createStore` 替代 `createContext`
- **v5** — 默认移除自定义 equality function；`createWithEqualityFn` 作为显式替代

## 与同类库对比

| 对比维度 | Zustand | Redux | Context API |
|---|---|---|---|
| 样板代码 | 极少 | 多 | 少 |
| Provider | 不需要 | 需要 | 需要 |
| 订阅粒度 | 选择器级别 | 选择器级别 | 整个 context |
| 包体积 | ~1KB | 较大 | 内置 |
| 中间件 | 有 | 有 | 无 |
| DevTools | 支持 | 原生支持 | 无 |

## 相关页面

- [[concepts/zustand-core-architecture]] — createStore 内部实现与 StoreApi 设计
- [[concepts/zustand-middleware-system]] — 中间件类型系统与内置中间件
- [[concepts/zustand-react-integration]] — useSyncExternalStore 集成与 useShallow
- [[skills/zustand-patterns]] — Slices 模式、Flux 实践、重置状态等最佳实践
- [[skills/zustand-ssr-nextjs]] — SSR 与 Next.js 集成
- [[skills/zustand-typescript]] — TypeScript 使用指南
