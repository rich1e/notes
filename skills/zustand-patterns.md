---
title: Zustand 最佳实践与常见模式
category: skills
tags:
  - state-management
  - react
  - patterns
  - frontend
sources:
  - "_raw/zustand.txt (Gitingest export, pmndrs/zustand, 2026-07-02)"
created: 2026-07-02T01:00:00Z
updated: 2026-07-02T01:00:00Z
summary: Zustand 推荐的模式：Slices 拆分大型 store、Flux 风格 colocate actions、外部 actions 模式、状态重置、Map/Set 使用、URL hash 同步等。
tier: supporting
lifecycle: draft
lifecycle_changed: "2026-07-02"
base_confidence: 0.85
provenance:
  extracted: 0.85
  inferred: 0.15
  ambiguous: 0.00
relationships:
  - target: "[[entities/zustand]]"
    type: related_to
  - target: "[[concepts/zustand-core-architecture]]"
    type: uses
  - target: "[[concepts/zustand-middleware-system]]"
    type: uses
  - target: "[[projects/trek/concepts/architecture-overview]]"
    type: related_to
---

# Zustand 最佳实践与常见模式

## Flux 推荐实践

Zustand 是无意见库，但官方推荐以下约定（受 Flux/Redux 启发）：

### 1. 单一 Store

全局状态应放在**单一** Zustand store 中。大型应用通过 Slices 模式（见下文）拆分，而非创建多个独立 store。

### 2. 始终用 set/setState 更新

所有状态更新必须通过 `set`（或 `setState`），确保浅合并和通知监听者正确执行。

### 3. Actions 与状态共置（Colocate）

官方推荐将 actions 定义**在 store 内部**：

```js
const useBoundStore = create((set) => ({
  count: 0,
  text: 'hello',
  inc: () => set((state) => ({ count: state.count + 1 })),
  setText: (text) => set({ text }),
}))
```

### 4. 外部 Actions 模式（可选）

另一种方式是将 actions 定义为**模块级函数**：

```js
// store 只含纯状态
export const useBoundStore = create(() => ({ count: 0, text: 'hello' }))

// actions 是独立函数，无需 Hook 即可调用
export const inc = () =>
  useBoundStore.setState((state) => ({ count: state.count + 1 }))

export const setText = (text) => useBoundStore.setState({ text })
```

**优势：** 无需 Hook 就能调用（非 React 环境、事件处理器中）；方便代码分割。  
**劣势：** 封装性差，状态和行为分离，代码分散。

## Slices 模式 — 拆分大型 Store

当 store 变大时，用 **Slice** 函数拆分领域：

```js
// bearSlice.js
export const createBearSlice = (set) => ({
  bears: 0,
  addBear: () => set((state) => ({ bears: state.bears + 1 })),
  eatFish: () => set((state) => ({ fishes: state.fishes - 1 })),
})

// fishSlice.js
export const createFishSlice = (set) => ({
  fishes: 0,
  addFish: () => set((state) => ({ fishes: state.fishes + 1 })),
})

// 跨 slice 的 action
export const createBearFishSlice = (set, get) => ({
  addBearAndFish: () => {
    get().addBear()   // 通过 get() 调用其他 slice 的 actions
    get().addFish()
  },
})

// boundStore.js — 合并所有 slice
export const useBoundStore = create((...a) => ({
  ...createBearSlice(...a),
  ...createFishSlice(...a),
  ...createBearFishSlice(...a),
}))
```

**关键规则：**
- 中间件只在最终 `create()` 的顶层应用，不在单个 slice 内
- 跨 slice 调用通过 `get()` 实现，不直接导入其他 slice

```js
// ✅ 中间件在顶层
export const useBoundStore = create(
  persist(
    (...a) => ({
      ...createBearSlice(...a),
      ...createFishSlice(...a),
    }),
    { name: 'bound-store' }
  )
)

// ❌ 错误：在 slice 内使用中间件
export const createBearSlice = persist((set) => ({ bears: 0 }), { name: 'bears' })
```

## 重置状态

### 单 Store 重置

```js
const initialState = { salmon: 0, tuna: 0 }

const useFishStore = create((set) => ({
  ...initialState,
  reset: () => set(initialState),  // 重置到初始值
}))
```

### 重置所有 Store（多 store 场景）

```js
// 维护所有 store 的重置函数列表
const resetters = []

// 每个 store 注册自身的重置函数
export const useBearStore = create((set) => {
  const initialState = { bears: 0 }
  resetters.push(() => set(initialState))
  return { ...initialState, addBear: () => set(s => ({ bears: s.bears + 1 })) }
})

// 全局重置
export const resetAllStores = () => resetters.forEach(reset => reset())
```

### 使用 replace=true 完全重置

```js
// ⚠️ 会清除 actions，只在确认状态结构一致时使用
store.setState(initialState, true)
```

## Map 和 Set 的使用

Zustand 要求不可变更新，Map/Set 需要创建新实例：

```js
const useMapStore = create((set) => ({
  map: new Map([['first', 1]]),
  actions: {
    addEntry: (key, value) =>
      set((state) => ({ map: new Map(state.map).set(key, value) })),  // 先复制再修改
    removeEntry: (key) =>
      set((state) => {
        const newMap = new Map(state.map)
        newMap.delete(key)
        return { map: newMap }
      }),
  },
}))
```

> **注意：** `useShallow` 对 Map/Set 使用 `compareEntries`（无序比较），可以正确处理 Map/Set 的浅比较。

## 自动生成选择器

为避免重复写 `(state) => state.xxx`，可自动生成：

```typescript
// 生成所有 key 的选择器 Hook
const createSelectors = <S extends UseBoundStore<StoreApi<object>>>(
  _store: S,
) => {
  let store = _store as WithSelectors<typeof _store>
  store.use = {}
  for (let k of Object.keys(store.getState())) {
    ;(store.use as any)[k] = () => store((s: any) => s[k as never])
  }
  return store
}

const useStoreWithSelectors = createSelectors(useBearStore)

// 使用
const bears = useStoreWithSelectors.use.bears()
const honey = useStoreWithSelectors.use.honey()
```

## URL Hash 同步状态

```js
import { create } from 'zustand'

const useHashStore = create((set) => {
  // 初始化：从 URL hash 恢复状态
  const searchParams = new URLSearchParams(location.hash.slice(1))
  const initialState = Object.fromEntries(searchParams)

  return {
    ...initialState,
    setParam: (key, value) => {
      set((state) => {
        const newState = { ...state, [key]: value }
        // 写回 URL hash
        location.hash = new URLSearchParams(newState).toString()
        return newState
      })
    },
  }
})
```

## 订阅外部系统（非 React）

```js
// 在非 React 代码中监听 store 变化
const unsubscribe = useSomeStore.subscribe(
  (state, prevState) => {
    // 响应状态变化，如更新 canvas、WebSocket 等
    if (state.position !== prevState.position) {
      updateCanvas(state.position)
    }
  }
)

// 组件卸载时清理
onDestroy(() => unsubscribe())
```

## 读取异步数据

actions 可以是异步的，Zustand 不关心同步/异步：

```js
const useFishStore = create((set) => ({
  fishies: {},
  fetch: async (pond) => {
    const response = await fetch(pond)
    set({ fishies: await response.json() })
  },
}))
```

异步 action 中通过 `get()` 读取最新状态（不要捕获旧 state 闭包）：

```js
const useStore = create((set, get) => ({
  data: null,
  process: async () => {
    await doSomething()
    const currentData = get().data  // ✅ 始终读取最新值
    set({ result: transform(currentData) })
  },
}))
```

## 相关页面

- [[entities/zustand]] — Zustand 概览
- [[concepts/zustand-core-architecture]] — setState replace 参数详解
- [[concepts/zustand-middleware-system]] — persist 持久化模式
- [[concepts/zustand-react-integration]] — useShallow、Transient Updates
- [[skills/zustand-typescript]] — TypeScript 中的 Slices 类型
- [[projects/trek/concepts/architecture-overview]] — Trek 项目对 Zustand Slices 的实际运用
