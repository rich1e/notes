---
title: Zustand React 集成 — useSyncExternalStore 与选择器
category: concepts
tags:
  - react
  - state-management
  - hooks
  - frontend
sources:
  - "_raw/zustand.txt (Gitingest export, pmndrs/zustand, 2026-07-02)"
created: 2026-07-02T01:00:00Z
updated: 2026-07-02T01:00:00Z
summary: Zustand React 层基于 React.useSyncExternalStore 实现，通过选择器订阅细粒度状态切片；useShallow 用稳定引用防止对象/数组选择器触发多余重渲染。
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
  - target: "[[concepts/zustand-core-architecture]]"
    type: derived_from
  - target: "[[concepts/zustand-middleware-system]]"
    type: related_to
---

# Zustand React 集成 — useSyncExternalStore 与选择器

## React 绑定的底层实现

`react.ts` 中的 `useStore` 直接基于 `React.useSyncExternalStore`：

```typescript
export function useStore<TState, StateSlice>(
  api: ReadonlyStoreApi<TState>,
  selector: (state: TState) => StateSlice = identity,
) {
  const slice = React.useSyncExternalStore(
    api.subscribe,                           // subscribe
    React.useCallback(                       // getSnapshot
      () => selector(api.getState()), [api, selector]
    ),
    React.useCallback(                       // getServerSnapshot（SSR）
      () => selector(api.getInitialState()), [api, selector]
    ),
  )
  React.useDebugValue(slice)  // DevTools 显示选中值
  return slice
}
```

**`useSyncExternalStore` 为何重要：**
- React 18 并发模式的官方外部存储集成 API
- 解决了 tearing（撕裂）问题：并发渲染中不同优先级渲染"看到"不同版本状态
- `getServerSnapshot` 参数让 Zustand 天然支持 SSR（服务端快照 = 初始状态）

## create 的简洁封装

`create()` 只是将 `createStore + useStore` 封装为一步操作：

```typescript
const createImpl = <T>(createState: StateCreator<T, [], []>) => {
  const api = createStore(createState)  // vanilla store

  const useBoundStore: any = (selector?: any) => useStore(api, selector)

  Object.assign(useBoundStore, api)  // 将 getState/setState/subscribe 挂到 hook 上

  return useBoundStore  // 返回的是一个同时是 Hook 和 StoreApi 的对象
}
```

因此 `useBearStore` 既能作为 Hook 调用（`useBearStore(selector)`），也能直接访问 store 方法（`useBearStore.getState()`）。

## 选择器与重渲染控制

### 基本选择器

Zustand 默认用 `Object.is` 比较选择器输出，只有值变化才触发重渲染：

```js
// ✅ 原子值选择：高效
const bears = useBearStore((state) => state.bears)
const honey = useBearStore((state) => state.honey)

// ⚠️ 每次渲染都返回新对象，总是重渲染
const { nuts, honey } = useBearStore((state) => ({
  nuts: state.nuts,
  honey: state.honey,
}))
```

### useShallow — 浅比较防止无效重渲染

当选择器返回**对象、数组或 Map/Set** 时，每次调用都创建新引用，`Object.is` 永远不相等 → 无限重渲染。`useShallow` 通过 `useRef` 缓存上次结果，用浅比较决定是否返回新引用：

```typescript
export function useShallow<S, U>(selector: (state: S) => U): (state: S) => U {
  const prev = React.useRef<U>(undefined)
  return (state) => {
    const next = selector(state)
    return shallow(prev.current, next)
      ? (prev.current as U)   // 浅等：返回缓存的旧引用
      : (prev.current = next) // 不等：更新缓存并返回新值
  }
}
```

```js
import { useShallow } from 'zustand/react/shallow'

// ✅ 对象 pick：nuts 或 honey 其一变化才重渲染
const { nuts, honey } = useBearStore(
  useShallow((state) => ({ nuts: state.nuts, honey: state.honey }))
)

// ✅ 数组 pick
const [nuts, honey] = useBearStore(
  useShallow((state) => [state.nuts, state.honey])
)

// ✅ Map/Set 的 key 列表
const treats = useBearStore(useShallow((state) => Object.keys(state.treats)))
```

### shallow 函数的类型感知实现

`vanilla/shallow.ts` 中的 `shallow` 函数支持多种类型：

```
shallow(a, b):
├── Object.is(a, b) → true：直接返回 true
├── 非对象/null → false
├── 原型不同 → false
├── Iterable（Map/Set/Array）：
│   ├── 有 entries()（Map/Set 类）→ compareEntries（无序键值对）
│   └── 无 entries（Array/迭代器）→ compareIterables（有序元素）
└── 普通对象 → compareEntries（Object.entries）
```

这意味着 `shallow` 对 `Map`、`Set`、`Array`、普通对象都有正确的比较语义。

## traditional.ts：自定义 equality function

`react.ts` 的 `create` 不支持自定义 equality function（v5 移除）。需要自定义时用 `createWithEqualityFn`（来自 `zustand/traditional`）：

```typescript
import { createWithEqualityFn } from 'zustand/traditional'
import { shallow } from 'zustand/vanilla/shallow'

const useBearStore = createWithEqualityFn(
  (set) => ({ bears: 0, ... }),
  shallow  // 默认 equality function
)

// 或在选择器级别指定
const treats = useBearStore(
  (state) => state.treats,
  (oldTreats, newTreats) => compare(oldTreats, newTreats)
)
```

`useStoreWithEqualityFn` 基于 `useSyncExternalStoreWithSelector`（来自 `use-sync-external-store/shim/with-selector`），支持在订阅层应用 equality function。

## Transient Updates — 订阅而非渲染

高频状态（如动画帧、鼠标坐标）避免 re-render 的模式——用 `subscribe` 直接写入 ref：

```typescript
const Component = () => {
  const scratchRef = useRef(useScratchStore.getState().scratches)
  
  useEffect(
    () => useScratchStore.subscribe(
      state => (scratchRef.current = state.scratches)
    ),
    []  // subscribe 返回取消订阅函数，useEffect 返回值自动调用
  )
  
  // scratchRef.current 始终最新，但组件不因状态变化重渲染
}
```

## React Context 模式（依赖注入）

当需要按请求创建独立 store（Next.js SSR、测试隔离）时，用 vanilla store + Context：

```typescript
import { createContext, useContext } from 'react'
import { createStore, useStore } from 'zustand'

const StoreContext = createContext(null)

const App = ({ initialData }) => {
  const [store] = useState(() => createStore(
    (set) => ({ ...initialData, update: (v) => set({ value: v }) })
  ))
  
  return (
    <StoreContext.Provider value={store}>
      {children}
    </StoreContext.Provider>
  )
}

const Component = () => {
  const store = useContext(StoreContext)
  const value = useStore(store, (state) => state.value)
}
```

**注意：** 不要将 `create()` 返回的 Hook 直接放入 Context（违反 Rules of Hooks），应使用 vanilla store。

## 相关页面

- [[entities/zustand]] — Zustand 项目概览
- [[concepts/zustand-core-architecture]] — createStore vanilla 核心
- [[concepts/zustand-middleware-system]] — persist、devtools 等中间件
- [[skills/zustand-patterns]] — 最佳实践与常见模式
- [[skills/zustand-ssr-nextjs]] — SSR / Next.js 场景下的 Context 模式
