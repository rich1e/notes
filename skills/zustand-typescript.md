---
title: Zustand TypeScript 使用指南
category: skills
tags:
  - typescript
  - state-management
  - react
  - f2e
sources:
  - "_raw/zustand.txt (Gitingest export, pmndrs/zustand, 2026-07-02)"
created: 2026-07-02T01:00:00Z
updated: 2026-07-02T01:00:00Z
summary: Zustand TypeScript 的核心是 create<T>()(...)（双括号） 而非 create<T>(...)，因为 State 泛型是不变的（invariant），无法从初始值自动推断。
tier: supporting
lifecycle: draft
lifecycle_changed: "2026-07-02"
base_confidence: 0.87
provenance:
  extracted: 0.87
  inferred: 0.13
  ambiguous: 0.00
relationships:
  - target: "[[entities/zustand]]"
    type: related_to
  - target: "[[concepts/zustand-core-architecture]]"
    type: uses
  - target: "[[concepts/zustand-middleware-system]]"
    type: uses
  - target: "[[skills/zustand-patterns]]"
    type: related_to
---

# Zustand TypeScript 使用指南

## 基础用法：双括号语法

TypeScript 用法与 JavaScript 的区别：`create<State>()(...)` 而非 `create<T>(...)`。

```typescript
import { create } from 'zustand'

interface BearState {
  bears: number
  increase: (by: number) => void
}

const useBearStore = create<BearState>()((set) => ({
  bears: 0,
  increase: (by) => set((state) => ({ bears: state.bears + by })),
}))
```

### 为何需要双括号？

**根本原因：** `State` 泛型 `T` 是**不变的（invariant）**——同时出现在协变（返回位置）和逆变（参数位置），TypeScript 无法自动推断。

```typescript
// TypeScript 推断失败示例
declare const create: <T>(f: (get: () => T) => T) => T

const x = create((get) => ({
  foo: 0,
  bar: () => get(),
}))
// x 被推断为 unknown，而不是 { foo: number; bar: () => ... }
```

`create<T>()((set) => ...)` 使用**currying**：第一次调用 `create<T>()` 固定类型参数，第二次调用接受 initializer，绕过了推断问题。

## 与中间件组合的 TypeScript

```typescript
import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'
import type {} from '@redux-devtools/extension'  // devtools 类型依赖

interface BearState {
  bears: number
  increase: (by: number) => void
}

const useBearStore = create<BearState>()(
  devtools(
    persist(
      (set) => ({
        bears: 0,
        increase: (by) => set((state) => ({ bears: state.bears + by })),
      }),
      { name: 'bear-storage' }
    )
  )
)
```

**注意：** `@redux-devtools/extension` 只是类型声明包，不影响运行时，`import type {}` 即可。

## Slices 模式的 TypeScript 写法

```typescript
import { StateCreator } from 'zustand'

// 定义各 slice 类型
interface BearSlice {
  bears: number
  addBear: () => void
  eatFish: () => void
}

interface FishSlice {
  fishes: number
  addFish: () => void
}

// StateCreator 接受全量 store 类型作为泛型，确保跨 slice 访问安全
const createBearSlice: StateCreator<
  BearSlice & FishSlice,  // 完整 store 类型（含 FishSlice，因为 eatFish 会访问 fishes）
  [],
  [],
  BearSlice               // 此 slice 产出的类型
> = (set) => ({
  bears: 0,
  addBear: () => set((state) => ({ bears: state.bears + 1 })),
  eatFish: () => set((state) => ({ fishes: state.fishes - 1 })),
})

const createFishSlice: StateCreator<
  BearSlice & FishSlice,
  [],
  [],
  FishSlice
> = (set) => ({
  fishes: 0,
  addFish: () => set((state) => ({ fishes: state.fishes + 1 })),
})

// 合并 store
export const useBoundStore = create<BearSlice & FishSlice>()((...a) => ({
  ...createBearSlice(...a),
  ...createFishSlice(...a),
}))
```

## 带中间件的 Slices TypeScript

```typescript
import { StateCreator } from 'zustand'
import { immer } from 'zustand/middleware/immer'
import { devtools } from 'zustand/middleware'

// Slice 使用 immer 中间件
type ImmerStateCreator<T> = StateCreator<T, [['zustand/immer', never]], [], T>

const createBearSlice: ImmerStateCreator<BearSlice> = (set) => ({
  bears: 0,
  addBear: () => set((state) => { state.bears++ }),  // immer 可变写法
})

// 顶层应用中间件
export const useBoundStore = create<BearSlice & FishSlice>()(
  devtools(
    immer((...a) => ({
      ...createBearSlice(...a),
      ...createFishSlice(...a),
    }))
  )
)
```

## 自定义 StoreMutatorIdentifier（扩展中间件类型）

实现自定义中间件时，需要注册类型：

```typescript
import { StateCreator, StoreMutatorIdentifier } from 'zustand'

// 1. 声明中间件标识符和它对 StoreApi 的变换
type Logger = <
  T,
  Mps extends [StoreMutatorIdentifier, unknown][] = [],
  Mcs extends [StoreMutatorIdentifier, unknown][] = [],
>(
  f: StateCreator<T, Mps, Mcs>,
) => StateCreator<T, Mps, Mcs>

// 2. module augmentation 注册
declare module 'zustand' {
  interface StoreMutators<S, A> {
    'custom/logger': S  // logger 不改变 StoreApi 类型
  }
}

// 3. 实现
const loggerImpl = (f) => (set, get, store) => {
  const loggedSet = (...args) => {
    console.log('Applying', args)
    set(...args)
    console.log('New state', get())
  }
  store.setState = loggedSet
  return f(loggedSet, get, store)
}

export const logger = loggerImpl as Logger
```

## ExtractState — 从 store 提取状态类型

```typescript
import { ExtractState } from 'zustand/vanilla'

const useBearStore = create((set) => ({ bears: 0 }))

// 提取 store 的 State 类型（不重写类型定义的情况下使用）
type BearState = ExtractState<typeof useBearStore>
// BearState = { bears: number }
```

## 使用 combine 简化 TypeScript

`combine` 让初始状态的类型自动推断，避免手写接口：

```typescript
import { create } from 'zustand'
import { combine } from 'zustand/middleware'

const useBearStore = create(
  combine(
    { bears: 0 },  // 初始状态——TypeScript 自动推断类型
    (set) => ({
      increase: () => set((s) => ({ bears: s.bears + 1 })),
    })
  )
)
// useBearStore 类型自动为：{ bears: number; increase: () => void }
```

## 常见类型错误与解法

| 错误 | 原因 | 解法 |
|---|---|---|
| `create(...)` 推断为 `unknown` | 未传类型参数，T 是不变的无法推断 | 改为 `create<State>()(...)` |
| 中间件类型报错 | 未 `import type {} from '@redux-devtools/extension'` | 添加该 import |
| Slice 中访问其他 Slice 状态报类型错误 | `StateCreator` 第一个泛型只写了本 Slice 类型 | 改为完整 store 类型 `BearSlice & FishSlice` |
| `devtools` + `immer` 组合报错 | 中间件顺序影响类型，devtools 应在外层 | 顺序：`devtools(persist(immer(...)))` |

## 相关页面

- [[entities/zustand]] — Zustand 概览
- [[concepts/zustand-core-architecture]] — StateCreator 类型定义
- [[concepts/zustand-middleware-system]] — StoreMutators 扩展机制
- [[skills/zustand-patterns]] — Slices 模式（JavaScript 版）
