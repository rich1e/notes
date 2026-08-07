---
title: AI 源 vs CORE 源 — 设计器组件面板的双源路由
category: concepts
tags:
  - designable
  - protocol-design
  - f2e
  - design-system
  - configuration
sources:
  - "_raw/2026-08-07-153809-flowimage-1.txt (Claude Code 多仓会话, 2026-08-07)"
created: 2026-08-07T15:38:09Z
updated: 2026-08-07T15:38:09Z
summary: 设计器侧组件面板的数据源由 `shouldUseAiComponentLibrary()` 决定：tenantFrom ∈ {tenantA, tenantB} 且 versionNum≠3 且 gcVersion≠v3 → 走 AI 后端 query-config；否则走 iframe postMessage 的 CORE 源。`engine.resource.from()` 透明消费两源。
tier: core
lifecycle: draft
lifecycle_changed: "2026-08-07"
base_confidence: 0.85
provenance:
  extracted: 0.90
  inferred: 0.08
  ambiguous: 0.02
relationships:
  - target: "[[projects/flow-design-system/flow-design-system]]"
    type: related_to
  - target: "[[projects/flow-design-system/concepts/triple-repo-component-contract]]"
    type: related_to
  - target: "[[projects/flow-design-system/concepts/designable-iframe-component-bridge]]"
    type: related_to
  - target: "[[projects/flow-design-system/concepts/ai-component-library-runtime]]"
    type: related_to
  - target: "[[concepts/auth-status-semantics]]"
    type: related_to
---

# AI 源 vs CORE 源 — 设计器组件面板的双源路由

> acme-dplatform-flow-v2 设计器的「拖拽面板」里显示哪些业务组件，**不是写死**的，而是按 `shouldUseAiComponentLibrary()` 判定从两个完全不同的源拉取：iframe `postMessage`（核心仓本地）vs `POST /ai/public/v1/component-library/query-config`（AI 后端）。同一个 `engine.resource.from()` 透明消费两源 —— 业务方看到的是同一个面板，但底层数据来源完全两套。

## 判定函数

```ts
// acme-dplatform-flow-v2/src/utils/component-library/index.ts
const shouldUseAiComponentLibrary = (): boolean =>
  (tenantFrom === 'tenantA' || tenantFrom === 'tenantB') &&
  versionNum !== '3' &&
  gcVersion !== 'v3';
```

| 输入 | 来源 | 取值 |
|------|------|------|
| `tenantFrom` | URL query `?tenantFrom=tenantB` | 必传 |
| `versionNum` | URL query 或全局配置 | 缺省/非 '3' |
| `gcVersion` | URL query 或全局配置 | 缺省/非 'v3' |

## 决策矩阵

| `tenantFrom` | `versionNum` | `gcVersion` | 走源 | 面板数据来源 |
|-------------|-------------|------------|------|------------|
| `tenantB` | 缺省 | 缺省 | **AI 源** | AI 后端 query-config |
| `tenantB` | '3' | 缺省 | CORE 源 | iframe postMessage |
| `tenantB` | 缺省 | 'v3' | CORE 源 | iframe postMessage |
| `tenantA` | 缺省 | 缺省 | **AI 源** | AI 后端 query-config |
| `tenantB` | '3' | 'v3' | CORE 源 | iframe postMessage |
| 其它 (`other` / 缺省) | 任意 | 任意 | CORE 源 | iframe postMessage |

> **关键含义**：`tenantFrom=tenantB` 是产品/保单路径的默认场景，**默认走 AI 源**。这意味着团队里大部分保单模板组件的新增/修改，**必须**在 BFF（`acme-core-goods-ai`）的 `library/components/` 同步加一份，单改核心仓没用。

## 设计器侧消费链

```ts
// acme-dplatform-flow-v2/src/components/dn/effects/useBroadcastEffect.ts:142-159
const applyLibrary = (library: ComponentLibraryPayload) => {
  const components = library.components || [];
  engine.resource.from({ presets, categories, components });
  engine.behavior.register(...convertBehavior(components));
};

if (componentLibrarySource === COMPONENT_LIBRARY_SOURCE.CORE) {
  applyLibrary(coreLibrary);          // ← 来自 iframe postMessage
} else if (aiLibCache) {
  applyLibrary(aiLibCache);           // ← 来自 fetch('/ai/public/v1/.../query-config')
} else {
  prefetchAiLib().then(applyLibrary); // ← 异步预取 AI 源
}
```

> 两个分支都把 `library` 喂给 `applyLibrary`，**对 engine 而言是同一接口**。`getSources(value)` 只关心 `library.components` 数组里有啥，**不关心**这数组来自 iframe 还是 fetch。

## 调试：判断当前走哪个源

```ts
// 在设计器页面 DevTools Console 粘贴
console.log({
  location: window.location.href,
  tenantFrom: new URLSearchParams(location.search).get('tenantFrom'),
  versionNum: new URLSearchParams(location.search).get('versionNum'),
  gcVersion: new URLSearchParams(location.search).get('gcVersion'),
});
// 然后调用本仓 utils/component-library 导出的 shouldUseAiComponentLibrary
// （在浏览器里 import 不到，需要在源码里打 console.log 或在 network 里看 query-config 是否被调用）
```

更直接的方式 —— **看 Network 面板**：

| 现象 | 走源 |
|------|------|
| Network 里有 `POST /ai/public/v1/component-library/query-config`（或 dev proxy 转发的 localhost:8080）| **AI 源** |
| Network 没有任何 `query-config` 请求 | CORE 源（用 iframe postMessage） |
| Network 有 query-config，但 Server IP 是 `http://8636-w-acme-core-goods-ai.test.example.com` | AI 源，**且**走 test 环境 BFF（不是本地） |

## dev proxy 改 target 的工作流

设计器 `config/config.ts:108-115` 的 `/ai/` proxy 默认 target 写死 test 环境：

```ts
'/ai/': {
  target: 'http://8636-w-acme-core-goods-ai.test.example.com',  // ← test 环境域名
  changeOrigin: true,
  pathRewrite: { '^/ai': '' },                          // 剥掉 /ai 前缀
  logLevel: DEBUG ? 'debug' : 'error',
}
```

**本地改了 BFF 想立刻验证？** 改 target 为 `http://localhost:8080`：

```ts
'/ai/': {
  target: 'http://localhost:8080',                       // ← 临时改
  changeOrigin: true,
  pathRewrite: { '^/ai': '' },
  logLevel: DEBUG ? 'debug' : 'error',
}
```

**然后**：

1. 重启 `acme-dplatform-flow-v2`（Umi 改了 config 必须重启）
2. 本地 `acme-core-goods-ai` 在 8080 跑着
3. Cmd+Shift+R 强制刷新设计器

**测完务必改回** —— 否则团队其他同学拉代码会被代理到你本机。最稳妥的做法：

```bash
git stash
# 改完测完
git checkout config/config.ts
git stash pop
```

## 三源不一致的常见故障

| 故障 | 走源 | 根因 |
|------|------|------|
| 核心仓 `preview/config.ts` 改了但设计器面板没变化 | 可能是 CORE 源 | iframe 缓存 + 核心仓 dev server 没重启 → 设计器没收到新 INITIALIZE |
| BFF `library/components/` 加了但设计器面板没变化 | 可能是 AI 源 | `index.ts` 的 `buildComponents()` 数组里没追加 |
| 全部都加了但面板仍没显示 | CORE 源 | 核心仓 dev server 没重启（iframe 还发旧消息）|
| 改了本地 BFF 看不到 | AI 源 | proxy target 写死 test 环境，改 target 后没重启 Umi |
| 改完 proxy target 团队其他同学报错 | 任意 | 你把 target 改成 localhost 但没改回去（其他人会代理到你的本机） |

## 跨源 schema 不一致

CORE 源（核心仓）的 schema 来自 `builtin-components/<name>/schema.ts`，AI 源（BFF）的 schema 来自 `library/components/<name>/schema.ts`。**两份 schema 字段必须一一对应**，但实际是两份独立代码（不共享），所以 schema 改动时**两处都要改**。

`dnOpenSchema/compents/<name>.ts` 是设计器侧 `tenantFrom=tenantA/tenantB` 时的**第三份** schema 副本（兜底用），同样需要同步。

> 详见 [[projects/flow-design-system/concepts/triple-repo-component-contract]] 的「三处 schema 副本的对齐原则」。

## 与 vault 已有概念的对应

| 本概念 | vault 概念 | 类比 |
|------|----------|------|
| 双源路由（AI vs CORE） | [[concepts/auth-status-semantics]] | 同样是"对外一个接口，对内两套状态"，关键是让消费者透明 |
| proxy target 临时改 localhost | [[concepts/cdp-cookie-extraction]] | 同为「本地调试时绕过远程/正式环境」的工程技巧 |
| 三处 schema 副本 | [[concepts/deterministic-agent-memory]] | 多副本的 stale 显式标注思想：哪份是 Source of Truth，其它是 Mirror |
| 缺省走 AI 源 | [[concepts/mcp-server-protocol-quirks]] | 同为"看似简单的协议层在工程上有大量隐含分支" |

## 相关页面

- [[projects/flow-design-system/flow-design-system]] — 项目总览
- [[projects/flow-design-system/concepts/triple-repo-component-contract]] — 9 步 SOP
- [[projects/flow-design-system/concepts/designable-iframe-component-bridge]] — iframe 上送机制
- [[projects/flow-design-system/concepts/ai-component-library-runtime]] — AI 后端 controller 结构
- [[concepts/auth-status-semantics]] — 状态语义设计的更抽象视角
