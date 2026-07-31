---
title: Zustand 核心架构 — createStore 与 StoreApi
category: concepts
tags:
  - state-management
  - react
  - frontend
sources:
  - "_raw/zustand.txt (Gitingest export, pmndrs/zustand, 2026-07-02)"
created: 2026-07-02T01:00:00Z
updated: 2026-07-02T01:00:00Z
summary: Zustand 的 vanilla 核心是约 30 行代码：一个闭包持有 state + listeners Set，setState 做浅合并并通知订阅者，StoreApi 是唯一的公共接口。
tier: supporting
lifecycle: draft
lifecycle_changed: "2026-07-02"
base_confidence: 0.88
provenance:
  extracted: 0.88
  inferred: 0.12
  ambiguous: 0.00
relationships:
  - target: "[[entities/zustand]]"
    type: related_to
  - target: "[[concepts/zustand-middleware-system]]"
    type: related_to
  - target: "[[concepts/zustand-react-integration]]"
    type: uses
  - target: "[[synthesis/zustand-core-architecture × zustand]]"
    type: related_to
---

# Zustand 核心架构 — createStore 与 StoreApi

## 双层架构：Vanilla + React

Zustand 的代码分为两层：

```
zustand/
├── vanilla.ts      ← 核心：无 React 依赖，纯 JS store 引擎
├── react.ts        ← React 层：将 vanilla store 绑定到 React Hook
├── traditional.ts  ← 传统层：支持自定义 equalityFn 的版本
├── shallow.ts      ← re-export vanilla/shallow + react/shallow
├── middleware.ts   ← re-export 所有中间件
└── middleware/
    ├── combine.ts
    ├── devtools.ts
    ├── immer.ts
    ├── persist.ts
    ├── redux.ts
    ├── ssrSafe.ts
    └── subscribeWithSelector.ts
```

导入路径映射：
- `zustand` → `react.ts`（带 React 绑定）
- `zustand/vanilla` → `vanilla.ts`（无 React 依赖）
- `zustand/middleware` → `middleware.ts`
- `zustand/react/shallow` → `react/shallow.ts`

## StoreApi 接口

```typescript
export interface StoreApi<T> {
  setState: SetStateInternal<T>    // 更新状态
  getState: () => T                // 读取当前状态
  getInitialState: () => T         // 读取初始状态（用于 SSR 水化）
  subscribe: (listener: (state: T, prevState: T) => void) => () => void
}
```

`subscribe` 返回一个取消订阅的函数，遵循 React `useSyncExternalStore` 约定。

## createStore 实现（核心约 30 行）

```typescript
const createStoreImpl: CreateStoreImpl = (createState) => {
  let state: TState
  const listeners: Set<Listener> = new Set()  // 监听器集合

  const setState = (partial, replace) => {
    const nextState =
      typeof partial === 'function' ? partial(state) : partial
    
    if (!Object.is(nextState, state)) {       // 引用相等则跳过
      const previousState = state
      state = (replace ?? typeof nextState !== 'object' || nextState === null)
        ? nextState                           // replace=true 或非对象：直接替换
        : Object.assign({}, state, nextState) // 默认：浅合并
      listeners.forEach((listener) => listener(state, previousState))
    }
  }

  const getState = () => state
  const getInitialState = () => initialState
  const subscribe = (listener) => {
    listeners.add(listener)
    return () => listeners.delete(listener)   // 返回取消订阅函数
  }

  const api = { setState, getState, getInitialState, subscribe }
  const initialState = (state = createState(setState, getState, api))
  return api
}
```

**关键设计决策：**

1. **`Object.is` 相等性检测** — 与 `===` 的区别：`Object.is(NaN, NaN) === true`，`Object.is(+0, -0) === false`，更符合值语义
2. **浅合并（shallow merge）** — `setState({ x: 1 })` 等同于 `{ ...prev, x: 1 }`，无需手动展开。`replace=true` 时完全替换，用于清空 store
3. **`Set<Listener>`** — 使用 Set 防止重复订阅，O(1) 添加/删除
4. **initialState 双重初始化** — `initialState = (state = createState(...))` 同时设置 `state`（运行时当前值）和 `initialState`（不变的初始快照），后者供 SSR 水化用

## setState 的 replace 参数

```typescript
type SetStateInternal<T> = {
  // replace=false（默认）：浅合并
  _(partial: T | Partial<T> | ((state: T) => T | Partial<T>), replace?: false): void
  // replace=true：完全替换（删除所有 actions）
  _(state: T | ((state: T) => T), replace: true): void
}['_']
```

`replace=true` 是危险操作——会删除 store 中的 actions：

```js
// ⚠️ 清空整个 store（包括 actions）
set({}, true)

// ✅ 只保留部分字段
set(({ tuna, ...rest }) => rest, true)
```

## StateCreator 与中间件类型系统

Zustand 的中间件类型系统通过 **StoreMutators** 接口实现开放扩展（Open/Closed Principle）：

```typescript
// 全局可扩展的类型映射
export interface StoreMutators<S, A> {}
export type StoreMutatorIdentifier = keyof StoreMutators<unknown, unknown>

// 中间件通过 module augmentation 注册自身
declare module 'zustand/vanilla' {
  interface StoreMutators<S, A> {
    'zustand/persist': WithPersist<S, A>
    'zustand/devtools': WithDevtools<S>
    'zustand/immer': WithImmer<S>
    // ...
  }
}
```

`Mutate<S, Ms>` 类型递归应用中间件变换：

```typescript
export type Mutate<S, Ms> = Ms extends []
  ? S
  : Ms extends [[infer Mi, infer Ma], ...infer Mrs]
    ? Mutate<StoreMutators<S, Ma>[Mi & StoreMutatorIdentifier], Mrs>
    : never
```

中间件链在类型层面是**类型态射的组合**，每个中间件变换 StoreApi 类型并传递给下一层。^[inferred]

## create vs createStore

| | `create` | `createStore` |
|---|---|---|
| 来源 | `zustand` (`react.ts`) | `zustand/vanilla` |
| 返回 | React Hook（`useBearStore`） | 原始 StoreApi 对象 |
| React 依赖 | 有 | 无 |
| 使用场景 | 直接在 React 组件中使用 | 共享实例、Context 注入、测试 |

```js
// create：返回 Hook，直接用
const useBearStore = create((set) => ({ bears: 0 }))

// createStore：返回 StoreApi，通过 useStore 连接 React
const bearStore = createStore((set) => ({ bears: 0 }))
const useBearStore = (selector) => useStore(bearStore, selector)
```

## 组件外访问 Store

由于 store 本身是模块级对象，可直接调用其方法：

```js
// 读取当前状态（非响应式）
const paw = useDogStore.getState().paw

// 订阅所有变化（同步触发）
const unsub = useDogStore.subscribe(console.log)

// 更新状态（触发所有监听者）
useDogStore.setState({ paw: false })

// 取消订阅
unsub()
```

> **注意：** 经过中间件修改的 `set`/`get` 不会反映在 `getState`/`setState` 上。

## 相关页面

- [[entities/zustand]] — Zustand 项目概览
- [[concepts/zustand-middleware-system]] — 中间件机制详解
- [[concepts/zustand-react-integration]] — React 绑定与 useSyncExternalStore
