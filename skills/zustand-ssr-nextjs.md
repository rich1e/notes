---
title: Zustand SSR 与 Next.js 集成
category: skills
tags:
  - nextjs
  - ssr
  - react
  - state-management
sources:
  - "_raw/zustand.txt (Gitingest export, pmndrs/zustand, 2026-07-02)"
created: 2026-07-02T01:00:00Z
updated: 2026-07-02T01:00:00Z
summary: Next.js 中 Zustand store 是模块级全局变量，必须按请求创建（per-request store）并通过 Context 传递，以避免跨请求状态污染和水化不匹配。
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
  - target: "[[concepts/zustand-react-integration]]"
    type: uses
  - target: "[[concepts/zustand-middleware-system]]"
    type: uses
---

# Zustand SSR 与 Next.js 集成

## 核心挑战

Zustand store 是**模块级全局状态**（module state）。在 Next.js 服务端环境中，这带来三个问题：

| 问题 | 说明 |
|---|---|
| **跨请求状态污染** | 服务器同时处理多个请求，模块级 store 会在请求间共享，导致用户 A 的数据泄漏给用户 B |
| **水化不匹配** | 应用在服务端和客户端各渲染一次，若状态不一致，React 会报 hydration error |
| **SPA 路由重置** | Next.js 客户端路由不刷新模块，需要按组件树重置 store |

## 解决方案：Per-Request Store + Context

**核心规则：**
- 不创建全局 store（不在模块顶层调用 `createStore`）
- 使用**工厂函数**创建 store，在组件树注入点实例化
- 通过 React Context 向下传递 store 实例
- RSC（React Server Components）不读写 store

## 完整实现模式

### Step 1：Store 工厂函数

```typescript
// src/stores/counter-store.ts
import { createStore } from 'zustand/vanilla'

export type CounterState = { count: number }
export type CounterActions = {
  decrementCount: () => void
  incrementCount: () => void
}
export type CounterStore = CounterState & CounterActions

const defaultInitState: CounterState = { count: 0 }

// 工厂函数：每次调用创建新 store 实例
export const createCounterStore = (initState = defaultInitState) =>
  createStore<CounterStore>()((set) => ({
    ...initState,
    decrementCount: () => set((s) => ({ count: s.count - 1 })),
    incrementCount: () => set((s) => ({ count: s.count + 1 })),
  }))
```

### Step 2：Context Provider

```typescript
// src/providers/counter-store-provider.tsx
'use client'  // Next.js App Router：Provider 必须是 Client Component

import { createContext, useState, useContext, type ReactNode } from 'react'
import { useStore } from 'zustand'
import { createCounterStore, type CounterStore } from '@/stores/counter-store'

type CounterStoreApi = ReturnType<typeof createCounterStore>
const CounterStoreContext = createContext<CounterStoreApi | undefined>(undefined)

export const CounterStoreProvider = ({ children, initialCount = 0 }: {
  children: ReactNode
  initialCount?: number
}) => {
  // useState 确保 store 只创建一次（不在每次渲染时重建）
  const [store] = useState(() => createCounterStore({ count: initialCount }))
  
  return (
    <CounterStoreContext.Provider value={store}>
      {children}
    </CounterStoreContext.Provider>
  )
}

// 自定义 Hook，简化消费端代码
export const useCounterStore = <T>(selector: (store: CounterStore) => T): T => {
  const context = useContext(CounterStoreContext)
  if (!context) throw new Error('useCounterStore must be used within CounterStoreProvider')
  return useStore(context, selector)
}
```

### Step 3：在 Layout/Page 注入

```typescript
// app/layout.tsx（App Router）
import { CounterStoreProvider } from '@/providers/counter-store-provider'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <CounterStoreProvider>
          {children}
        </CounterStoreProvider>
      </body>
    </html>
  )
}
```

### Step 4：在组件中消费

```typescript
// app/some-page/page.tsx
'use client'
import { useCounterStore } from '@/providers/counter-store-provider'

export default function Counter() {
  const count = useCounterStore((state) => state.count)
  const increment = useCounterStore((state) => state.incrementCount)
  
  return (
    <div>
      <span>{count}</span>
      <button onClick={increment}>+</button>
    </div>
  )
}
```

## Server Components 传递初始数据

RSC 可以获取服务端数据，通过 Provider 的 props 注入初始状态：

```typescript
// app/page.tsx（RSC）
import { CounterStoreProvider } from '@/providers/counter-store-provider'
import Counter from './Counter'

export default async function Page() {
  // 服务端获取初始数据
  const initialCount = await fetchInitialCount()
  
  return (
    // 通过 props 传递初始值，Provider 在客户端初始化 store
    <CounterStoreProvider initialCount={initialCount}>
      <Counter />
    </CounterStoreProvider>
  )
}
```

## persist 中间件与 SSR

`persist` 默认在初始化时同步水化（从 localStorage 读取），SSR 会导致错误（服务端没有 localStorage）。

两种解法：

### 方案 A：skipHydration

```typescript
const useStore = create(
  persist(
    (set) => ({ count: 0 }),
    {
      name: 'my-store',
      skipHydration: true,  // 跳过自动水化
    }
  )
)

// 在客户端组件的 useEffect 中手动水化
useEffect(() => {
  useStore.persist.rehydrate()
}, [])
```

### 方案 B：createJSONStorage + 条件存储

```typescript
const useStore = create(
  persist(
    (set) => ({ count: 0 }),
    {
      name: 'my-store',
      storage: createJSONStorage(() =>
        typeof window !== 'undefined' ? localStorage : noopStorage
      ),
    }
  )
)
```

## App Router vs Pages Router

| 场景 | 推荐方案 |
|---|---|
| App Router + RSC | 工厂函数 + Context Provider（Client Component） |
| App Router 服务端缓存 | 模块级 store 兼容（服务端缓存不影响客户端 store 隔离） |
| Pages Router (`_app.tsx`) | 在 `_app.tsx` 中创建 store，通过 Context 传递 |
| 多页面共享状态 | Provider 放在 `_app.tsx` 或 `app/layout.tsx` |
| 页面级独立状态 | Provider 放在对应 Page 组件 |

## 反模式：不要这样做

```typescript
// ❌ 模块级全局 store：多请求共享，服务端不安全
const useGlobalStore = create((set) => ({ user: null }))

// ❌ 在 RSC 中使用 store
// app/page.tsx（RSC）
export default function Page() {
  const user = useGlobalStore(s => s.user)  // ❌ RSC 不能用 hooks
}

// ❌ 将 Hook 直接作为 Context value
const StoreContext = createContext(useBearStore)  // ❌ 违反 Rules of Hooks
```

## 相关页面

- [[entities/zustand]] — Zustand 概览
- [[concepts/zustand-react-integration]] — Context 模式（React 通用版）
- [[concepts/zustand-middleware-system]] — persist 中间件详解
- [[skills/zustand-patterns]] — Slices 模式
