---
title: Zustand 中间件系统
category: concepts
tags:
  - state-management
  - middleware
  - react
  - f2e
sources:
  - "_raw/zustand.txt (Gitingest export, pmndrs/zustand, 2026-07-02)"
created: 2026-07-02T01:00:00Z
updated: 2026-07-02T01:00:00Z
summary: Zustand 中间件通过高阶函数包装 StateCreator，用 StoreMutators 接口在类型层面注册变换，支持任意链式组合，内置 persist/devtools/immer/redux 等。
tier: supporting
lifecycle: draft
lifecycle_changed: "2026-07-02"
base_confidence: 0.87
provenance:
  extracted: 0.85
  inferred: 0.15
  ambiguous: 0.00
relationships:
  - target: "[[entities/zustand]]"
    type: related_to
  - target: "[[concepts/zustand-core-architecture]]"
    type: derived_from
  - target: "[[concepts/zustand-react-integration]]"
    type: related_to
---

# Zustand 中间件系统

## 中间件的本质：高阶函数

Zustand 中间件是包装 `StateCreator` 的高阶函数——接受一个 `StateCreator`，返回一个新的 `StateCreator`：

```typescript
// 中间件签名模板
const myMiddleware = (config) => (set, get, api) => {
  // 可以包装 set/get/api
  const wrappedSet = (...args) => {
    // 前置逻辑
    config(wrappedSet, get, api)
    // 后置逻辑
  }
  return config(wrappedSet, get, api)
}
```

中间件可以：
- **包装 `set`** — 拦截状态更新（devtools 记录 action，persist 写入 storage）
- **扩展 `api`** — 向 StoreApi 添加新方法（persist 添加 `api.persist`，redux 添加 `api.dispatch`）
- **修改初始状态** — 在 store 初始化时注入额外状态

## 类型安全机制：StoreMutators

Zustand 使用 **module augmentation** 让中间件在类型层面注册自身：

```typescript
// 每个中间件在 vanilla.ts 中扩展全局接口
declare module 'zustand/vanilla' {
  interface StoreMutators<S, A> {
    'zustand/persist': WithPersist<S, A>
    'zustand/devtools': WithDevtools<S>
    'zustand/immer': WithImmer<S>
    'zustand/redux': WithRedux<S, A>
    'zustand/subscribeWithSelector': WithSelectorSubscribe<S>
  }
}
```

`StateCreator` 类型参数记录已应用的中间件（`Mis`）和将产生的中间件（`Mos`）：

```typescript
type StateCreator<
  T,
  Mis extends [StoreMutatorIdentifier, unknown][] = [],  // 输入中间件
  Mos extends [StoreMutatorIdentifier, unknown][] = [],  // 输出中间件
  U = T,
> = (setState, getState, store) => U
```

## 内置中间件详解

### persist — 状态持久化

将 store 数据序列化到任意存储（localStorage、sessionStorage、自定义存储）：

```typescript
import { persist, createJSONStorage } from 'zustand/middleware'

const useFishStore = create(
  persist(
    (set, get) => ({
      fishes: 0,
      addAFish: () => set({ fishes: get().fishes + 1 }),
    }),
    {
      name: 'food-storage',           // storage key（必须唯一）
      storage: createJSONStorage(() => sessionStorage),  // 默认 localStorage
      partialize: (state) => ({ fishes: state.fishes }), // 只持久化部分状态
      version: 1,                     // 版本号，不匹配时跳过旧数据
      migrate: (oldState, version) => oldState,  // 版本迁移函数
      merge: (persistedState, currentState) => ({ ...currentState, ...persistedState }),
      skipHydration: false,           // SSR 场景可手动调用 rehydrate()
    }
  ),
)
```

**持久化 API 扩展：** `store.persist` 对象提供：
- `hasHydrated()` — 是否已完成水化
- `rehydrate()` — 手动触发水化（用于 SSR）
- `clearStorage()` — 清除持久化数据
- `onHydrate(fn)` / `onFinishHydration(fn)` — 水化生命周期回调

**`createJSONStorage`** — 将 `StateStorage`（`getItem`/`setItem`/`removeItem`）适配为 `PersistStorage`（支持异步）：

```typescript
export interface StateStorage<R = unknown> {
  getItem: (name: string) => string | null | Promise<string | null>
  setItem: (name: string, value: string) => R
  removeItem: (name: string) => R
}
```

**并发水化保护：** 使用 `hydrationVersion` 计数器防止多次并发 `rehydrate()` 调用的竞争条件。

### devtools — Redux DevTools 集成

```typescript
import { devtools } from 'zustand/middleware'

const useBearStore = create(
  devtools(
    (set) => ({
      bears: 0,
      eatFish: () => set(
        (prev) => ({ fishes: prev.fishes - 1 }),
        undefined,           // replace（第二参数）
        'bear/eatFish'       // action 名（第三参数，用于 DevTools 显示）
      ),
    }),
    {
      name: 'BearStore',     // DevTools 中的 store 名
      enabled: process.env.NODE_ENV !== 'production',
      anonymousActionType: 'anonymous',  // 未命名 action 的默认名
    }
  )
)
```

多个 store 共享一个 DevTools 连接可用 `store` 选项区分：

```js
devtools((set) => ..., { name: 'MyApp', store: 'bears' })
```

### immer — 可变写法更新不可变状态

```typescript
import { immer } from 'zustand/middleware/immer'

const useBeeStore = create(
  immer((set) => ({
    bees: 0,
    addBees: (by) =>
      set((state) => {
        state.bees += by  // 直接修改，immer 保证不可变性
      }),
  })),
)
```

实现极简——包装 `set`，传入 immer `produce`：

```typescript
const immerImpl: ImmerImpl = (initializer) => (set, get, store) => {
  store.setState = (updater, replace, ...a) => {
    const nextState = typeof updater === 'function'
      ? produce(updater as any)
      : updater
    return set(nextState, replace as false, ...a)
  }
  return initializer(store.setState, get, store)
}
```

### redux — Redux 风格 Reducer

```typescript
import { redux } from 'zustand/middleware'

const reducer = (state, { type, by = 1 }) => {
  switch (type) {
    case 'INCREASE': return { grumpiness: state.grumpiness + by }
    case 'DECREASE': return { grumpiness: state.grumpiness - by }
  }
}

const useGrumpyStore = create(redux(reducer, { grumpiness: 0 }))
// 获得 dispatch：useGrumpyStore.dispatch({ type: 'INCREASE', by: 2 })
```

`redux` 中间件在 api 上挂载 `dispatch` 和 `dispatchFromDevtools=true`（供 DevTools 中间件检测）。

### subscribeWithSelector — 带选择器的订阅

扩展 `subscribe` 签名以支持选择器：

```typescript
const unsub = useDogStore.subscribe(
  (state) => state.paw,           // selector
  (paw, previousPaw) => console.log(paw, previousPaw),  // callback
  {
    equalityFn: Object.is,        // 自定义相等性判断
    fireImmediately: true,        // 立即触发一次
  }
)
```

实现机制：包装原始 `api.subscribe`，在每次全量状态变化时，用 `equalityFn` 比较新旧 slice，只在 slice 变化时调用 callback。

### combine — 合并初始状态与 actions

```typescript
import { combine } from 'zustand/middleware'

const useBearStore = create(
  combine(
    { bears: 0 },                  // 初始状态（类型推断友好）
    (set) => ({
      increase: () => set((s) => ({ bears: s.bears + 1 })),
    }),
  )
)
```

`combine` 允许将静态初始状态与动态 actions 分离，方便 TypeScript 类型推断。

### ssrSafe（实验性）

在 SSR 环境下阻止 `setState` 调用（抛出错误），防止服务端渲染时意外修改状态：

```typescript
const useStore = create(ssrSafe((set) => ({ count: 0 })))
// 在 SSR（window === undefined）时，setState 调用会 throw
```

## 中间件组合顺序

多个中间件按**从外到内**的顺序执行，外层中间件先包装：

```typescript
create(devtools(persist(immer((set) => ({ ... })))))
```

执行顺序（setState 调用时）：`devtools.set → persist.set → immer.set → 实际 setState`

**关键注意：** 不要在单个 slice 内使用中间件，只在最终 `create()` 的顶层使用。在 slice 内使用中间件会导致类型错误和运行时异常。^[inferred]

## 相关页面

- [[entities/zustand]] — Zustand 项目概览
- [[concepts/zustand-core-architecture]] — createStore 核心实现
- [[skills/zustand-patterns]] — 中间件使用的实践模式
- [[skills/zustand-ssr-nextjs]] — persist + skipHydration SSR 用法
