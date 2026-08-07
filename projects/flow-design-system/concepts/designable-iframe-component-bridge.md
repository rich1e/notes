---
title: Designable iframe 组件桥 — postMessage 上送组件库
category: concepts
tags:
  - designable
  - formily
  - f2e
  - design-system
  - protocol-design
  - iframe
sources:
  - "_raw/2026-08-07-153809-flowimage-1.txt (Claude Code 多仓会话, 2026-08-07)"
created: 2026-08-07T15:38:09Z
updated: 2026-08-07T15:38:09Z
summary: 核心仓（acme-dplatform-flow-v2-core）通过 `DESIGNABLE_INITIALIZE_MESSAGE` 把组件列表（categories/presets/components）一次性 `postMessage` 给设计器父窗，设计器 `useBroadcastEffect` 收消息 → `engine.resource.from()` → 拖拽面板可显示。CORE 源的核心机制。
tier: core
lifecycle: draft
lifecycle_changed: "2026-08-07"
base_confidence: 0.85
provenance:
  extracted: 0.88
  inferred: 0.10
  ambiguous: 0.02
relationships:
  - target: "[[projects/flow-design-system/flow-design-system]]"
    type: related_to
  - target: "[[projects/flow-design-system/concepts/triple-repo-component-contract]]"
    type: related_to
  - target: "[[projects/flow-design-system/concepts/ai-component-library-runtime]]"
    type: related_to
  - target: "[[projects/flow-design-system/concepts/ai-vs-core-component-source-routing]]"
    type: related_to
  - target: "[[concepts/ai-tool-specialization]]"
    type: related_to
---

# Designable iframe 组件桥 — postMessage 上送组件库

> acme-dplatform-flow-v2-core 作为 iframe 被设计器父窗嵌入。组件列表是**一次性**通过 `postMessage` 上送的，不是每次拖拽都重发。这条机制决定了「改了核心仓组件后必须重启核心仓 + 强制刷新设计器才能看到新组件」。

## 消息格式

```ts
// 核心仓 src/modules/preview/config.ts 末尾
DESIGNABLE_INITIALIZE_MESSAGE = {
  type: 'INITIALIZE',
  payload: {
    presets: [...],          // 设计器侧 designable 内置元素（容器/布局）
    categories: [
      { name: 'basic', ... },
      { name: 'layout', ... },
      { name: 'display', ... },
      ...
    ],
    components: [            // 业务组件库（CORE 源时这里是核心仓的 components 数组）
      { name: 'terms', title: '条款阅读', categories: ['display'], schema: {...} },
      { name: 'terms-display', title: '条款展示组件', categories: ['display'], schema: {...} },
      { name: 'terms-card', title: '保险条款卡片', categories: ['display'], schema: {...} },
      ...
    ]
  }
};
```

## 发送时机与单次性

设计器侧 `useBroadcastEffect` 监听 `message` 事件，**只在 iframe `useEffect` 首次挂载时收一次**（不是每次拖拽都重发）。这导致：

- 核心仓改了 `preview/config.ts` 的 `components` 数组 → **必须重启核心仓 dev 服务器 + 强制刷新设计器** 才能让设计器侧拿到新 `INITIALIZE` 消息
- 设计器侧不会主动 `postMessage` 反向请求组件库（只接收）
- 设计器面板缓存了 `applyLibrary` 的 `library` 对象 → 改完即生效是错觉

## 设计器侧接收流程

```
useBroadcastEffect（acme-dplatform-flow-v2/src/components/dn/effects/useBroadcastEffect.ts）
  │
  ├─ window.addEventListener('message', e => { ... })
  │
  ├─ if (e.data?.type === 'INITIALIZE') { ... }
  │
  ├─ applyLibrary(library) {
  │     const components = library.components || [];
  │     engine.resource.from({ presets, categories, components });
  │     engine.behavior.register(...convertBehavior(components));
  │  }
  │
  └─ (CORE 源 vs AI 源分支见 [[projects/flow-design-system/concepts/ai-vs-core-component-source-routing]])
```

## components 数组排序的隐含约定

| 顺序位置 | 含义 | 案例 |
|---------|------|------|
| 数组前面 | 通常是基础业务组件（terms / image / button） | `TermsConfig` 在 1058 |
| 数组中段 | 同一类目的衍生组件 | `TermsDisplay` 紧跟 `TermsConfig`（1059） |
| **紧跟同前缀组件** | 命名空间内聚（建议） | 新增 `terms-card` 应紧跟 `TermsDisplay`（1060） |

> 「紧跟同前缀」不是强制规则，但能避免「`terms-card` 跑到数组最后」这种认知干扰。

## 与「AI 源」的消息链路对比

| 维度 | CORE 源（iframe） | AI 源（fetch） |
|------|------------------|----------------|
| 数据发送方 | iframe `DESIGNABLE_INITIALIZE_MESSAGE` | 后端 `POST /ai/public/v1/component-library/query-config` |
| 接收点 | `useBroadcastEffect` 的 `message` listener | `useBroadcastEffect` 的 `applyLibrary` 直传 `coreLibrary` / `aiLibCache` |
| 失效条件 | iframe 缓存 + dev server 未重启 | 后端没同步 + 运营表漏配 |
| 何时生效 | 重启核心仓 + 强制刷新设计器 | 后端改完发版后强制刷新 |
| 调试入口 | `window.addEventListener('message', ...)` 监 INITIALIZE 消息 | `fetch('/ai/public/v1/component-library/query-config', ...).then(r => r.json())` |

## 调试技巧：监听 INITIALIZE 消息

在设计器 DevTools Console 粘贴：

```js
window.addEventListener('message', e => {
  if (e.data?.type === 'INITIALIZE') {
    const comps = e.data.payload.components;
    console.log('total components:', comps.length);
    console.log('display 分类下:', comps.filter(c => c.categories?.includes('display')).map(c => c.name));
    console.log('terms-card in list?', comps.some(c => c.name === 'terms-card'));
  }
});
```

- 能看到 `terms-card` → CORE 源链路 OK，问题在 AI 源（运营表漏配）
- 看不到 `terms-card` → iframe 缓存或核心仓没重启

## 已知脆性

1. **不热重载**：改了 `preview/config.ts` 后必须重启核心仓 + 强制刷新设计器，没有 HMR 路径
2. **消息单次性**：设计器侧没有重新拉取按钮，若 iframe 缓存只收到旧消息只能清 localStorage 强制刷新
3. **proxy target 写死 test**：开发态改了本地 BFF 不生效，必须同步改 `acme-dplatform-flow-v2/config/config.ts` 的 `/ai/` target

## 相关页面

- [[projects/flow-design-system/flow-design-system]] — 项目总览
- [[projects/flow-design-system/concepts/triple-repo-component-contract]] — 9 步 SOP
- [[projects/flow-design-system/concepts/ai-vs-core-component-source-routing]] — CORE/AI 双源判定
- [[projects/flow-design-system/concepts/ai-component-library-runtime]] — AI 后端的 controller 结构
- [[concepts/ai-tool-specialization]] — AI 工具栈分工的更抽象视角
