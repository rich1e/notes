---

title: >-
  Zustand 5 + Chrome Storage 持久化：chromeStorage 适配器模式
category: skills
tags:
  - chrome-extension
  - zustand
  - persistence
  - react
relationships:
  - target: "[[entities/zustand]]"
    type: uses
sources: [projects/jrfed-zaxd-mediation-tool]
summary: >-
  Chrome 扩展中不能用 localStorage，通过封装 chrome.storage.local 的异步适配器接入 Zustand persist 中间件，实现跨页面状态持久化。
provenance:
  extracted: 0.92
  inferred: 0.06
  ambiguous: 0.02
base_confidence: 0.91
lifecycle: draft
lifecycle_changed: 2026-07-01
created: 2026-07-01T12:00:00Z
updated: 2026-07-01T12:00:00Z
---

# [[entities/zustand|Zustand]] 5 + Chrome Storage 持久化

## 为什么不能用 localStorage

Chrome Extension Content Script 与宿主页面共享 `window.localStorage`，直接使用会造成键名冲突和数据泄漏。必须使用 `chrome.storage.local`，它是扩展私有的隔离存储空间，支持异步读写。

## chromeStorage 适配器

`src/content/utils/storage.ts` 实现了 Zustand `persist` 中间件所需的接口：

```typescript
export const chromeStorage = {
  getItem: async (name: string) => {
    const value = await getStorageItem(name);
    return value || null;
  },
  setItem: async (name: string, value: any) => {
    await setStorageItem(name, value);
  },
  removeItem: async (name: string) => {
    await removeStorageItem(name);
  },
};
```

## 标准持久化 Store 写法

```typescript
import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { chromeStorage } from '@/content/utils/storage';

export const useMenuStore = create<MenuState>()(
  persist(
    (set) => ({
      levalOneSelectedKey: 'trial',
      // ...
    }),
    {
      name: 'za-assistant-menuStore-storage',
      storage: chromeStorage,
    }
  )
);
```

## 大数据量 Store：手动持久化模式

`searchParamsStore` 数据量大，用 `saveToStorage` 手动控制，避免每次任意字段变化都触发完整序列化写入：

```typescript
export const useSearchParamsStore = create<any>()((set, get) => ({
  saveToStorage: (state) => {
    setStorageItem(STORAGE_KEY, stateToSave).catch(error => {
      console.error('Failed to save:', error);
    });
  },

  setEarlyRepaymentParams: (params) =>
    set((state) => {
      const newState = { earlyRepaymentParams: params };
      get().saveToStorage(newState);
      return newState;
    }),
}));
```

## 多页面联动

`searchParamsStore` 的 `setCertNo` / `setMobile` 同时更新多个页面的搜索参数，用户在划词填入身份证号后，所有功能页的查询框会同步刷新：

```typescript
setcertNo: (certNo) =>
  set((state) => {
    const newState = {
      earlyRepaymentParams: { ...state.earlyRepaymentParams, certNo },
      sootheParams: { ...state.sootheParams, certNo },
      couponParams: { ...state.couponParams, certNo },
      rightsParams: { ...state.rightsParams, certNo },
      rightsHistoryParams: { ...state.rightsHistoryParams, certNo },
    };
    get().saveToStorage(newState);
    return newState;
  }),
```

## 注意事项

- `removeItem` 用于登出时清理持久化数据，例如 `resetMenuPermissions()` 同时调用 `useMenuStore.setState` 和 `chromeStorage.removeItem`
- Store 文件命名：`{name}Store.ts`，导出名：`use{Name}Store`（hook 风格）或 `{name}Store`（getState 直接访问风格）

## 关联页面

- [[projects/jrfed-zaxd-mediation-tool/jrfed-zaxd-mediation-tool]] — 项目总览
- [[projects/jrfed-zaxd-mediation-tool/concepts/permission-system]] — 权限持久化
