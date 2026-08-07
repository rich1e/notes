---
title: 商品中心模板组件系统 — 三仓协作的项目卡
category: projects
tags:
  - design-system
  - f2e
  - react
  - formily
  - designable
  - umi
  - koa
  - ai-coding
sources:
  - _raw/2026-08-07-153809-flowimage-1.txt (Claude Code 多仓会话, 2026-08-07)
created: 2026-08-07T15:38:09Z
updated: 2026-08-07T15:38:09Z
summary: ACME 司 商品中心（保单投保页/落地页）模板组件系统：3 仓协作——核心运行时（flow-v2-core）+ 设计器（flow-v2）+ AI 组件库后端（goods-ai）。新增一个 display 类业务组件需在 3 仓分别注册，组件名与 schema 三方严格对齐。
tier: core
lifecycle: draft
lifecycle_changed: 2026-08-07
base_confidence: 0.85
provenance:
  extracted: 0.75
  inferred: 0.2
  ambiguous: 0.05
relationships:
  - target: "[[projects/flow-design-system/concepts/triple-repo-component-contract]]"
    type: related_to
  - target: "[[projects/flow-design-system/concepts/designable-iframe-component-bridge]]"
    type: related_to
  - target: "[[projects/flow-design-system/concepts/ai-component-library-runtime]]"
    type: related_to
  - target: "[[projects/flow-design-system/concepts/dynamic-require-resolveweak-loading]]"
    type: related_to
  - target: "[[projects/flow-design-system/concepts/ai-vs-core-component-source-routing]]"
    type: related_to
  - target: "[[projects/flow-design-system/skills/add-new-builtin-component-three-repo-sop]]"
    type: related_to
  - target: "[[concepts/design-system-as-ai-context]]"
    type: related_to
---

# 商品中心模板组件系统

> ACME 司 平台商品中心（保单投保页、落地页）的「业务展示组件」三仓协作项目卡。新增一个 display 类组件（条款卡片、被保人表单、卖点、常见问题等）需要在 3 个工程里同时注册，缺一则面板里看不到、运行时不识别。

## 三仓角色

| 工程 | 角色 | 关键路径 |
|------|------|---------|
| `acme-dplatform-flow-v2-core` | 核心运行时 / iframe 上送 | `src/modules/template/builtin-components/<name>/`（运行时按目录名动态加载），`src/modules/preview/config.ts`（上送父窗的 DESIGNABLE_INITIALIZE_MESSAGE） |
| `acme-dplatform-flow-v2` | 设计器父窗（拖拽面板 + 画布） | `src/components/dn/`（@designable 渲染器），`src/components/dnOpenSchema/`（tenant=tenantA/tenantB 时的 schema 本地兜底副本），`config/config.ts`（Umi dev proxy `/ai/` → acme-core-goods-ai） |
| `acme-core-goods-ai` | AI 组件库运营后端（Koa BFF） | `app/controller/component-library/library/components/<name>/`（每个组件 `config.ts` + `schema.ts` 两个文件），`library/components/index.ts`（汇总数组），`app/router/public.ts`（路由前缀 `/public/v1`） |

## 组件名是全链路锚点

> 「组件类型与设计器侧一致」(CLAUDE.md 274) —— 这条字面约束的工程含义 = **目录名 = `name` 字段 = iframe 上送 `componentType` = 设计器 Dn 面板显示名 = AI 后端 query-config 过滤键**，5 处必须严格一致。

| 层 | 字段 | 来源 |
|----|------|------|
| 运行时目录 | `src/modules/template/builtin-components/<name>/` | 物理路径 |
| 运行时注册 | `config.ts` `name: '<name>'` | 必须等于目录名 |
| 设计器侧 iframe | `preview/config.ts` `components` 数组里的 `TermsCardConfig` | 运行时输出 |
| 设计器侧 tenant=tenantA 兜底 | `dnOpenSchema/index.ts` 的 `'<name>': xxx` | 设计器侧可选 |
| AI 后端 | `app/controller/component-library/library/components/<name>/config.ts` `name: '<name>'` | 运营配置 |

## 设计器侧组件面板的数据源（CORE vs AI）

设计器组件面板的「源」由 `shouldUseAiComponentLibrary()` 决定（`acme-dplatform-flow-v2/src/utils/component-library/index.ts`）：

```ts
shouldUseAiComponentLibrary = () =>
  (tenantFrom === 'tenantA' || tenantFrom === 'tenantB') &&
  versionNum !== '3' && gcVersion !== 'v3';
```

| 命中分支 | 数据源 | 流程 |
|---------|-------|------|
| **CORE 源** | iframe `postMessage`（本仓库 `preview/config.ts` 的 `DESIGNABLE_INITIALIZE_MESSAGE`） | 设计器只收一次（在 iframe `useEffect` 首次挂载时） |
| **AI 源** | `POST /ai/public/v1/component-library/query-config` | 对方前端从 `/ai` 路径打，Umi dev proxy 剥掉 `/ai` → `acme-core-goods-ai/public/v1/component-library/query-config` |

**生产环境坑**：`config/config.ts` 的 `/ai/` proxy target 写死 `http://8636-w-acme-core-goods-ai.test.example.com`（test 环境域名）。本地 `pnpm dev` 起的 8080 BFF 改完后，前端默认仍打 test 环境 —— 想立刻联调本机 BFF，需把 proxy target 临时改 `http://localhost:8080`，测完改回。

## 三仓的运行时/构建/类型栈

| 工程 | 栈 | Node | 备注 |
|------|----|------|------|
| acme-dplatform-flow-v2-core | React + UmiJS 4.x + Formily + TypeScript | 14 | `tsc --noEmit` 校验零类型错误（项目本身有 `node_modules/libpag` 旧类型与本组件无关） |
| acme-dplatform-flow-v2 | UmiJS 3.5 + React 17 + @designable/* + @formily/* + reactive | — | Dn = designable；`useBroadcastEffect.ts` 收 `DESIGNABLE_INITIALIZE_MESSAGE` |
| acme-core-goods-ai | Koa.js v3 + TypeScript | — | `@controller('/component-library')` + `app/router/public.ts` 的 `prefix: '/public/v1'` = 真路径 `/public/v1/component-library/query-config` |

## 当前已知的脆性

1. **面板不显示 = iframe 缓存 + 缺失 schema 兜底 + AI 后端没同步** 三种原因之一。诊断顺序：先看 Network 里 `query-config` 的 `Server IP` 是 test 还是 localhost；再看返回 JSON 有没有该组件；最后看设计器侧 `applyLibrary` 走的是 `coreLibrary` 还是 `aiLibCache`。
2. **开发态 proxy target 写死** = 团队里任何同学改了本地 BFF，其他人拉不到。临时改 target 必须独立 commit 标注 revert，或 `git stash` 处理。
3. **三处 schema 副本**（`builtin-components/<name>/schema.ts` + `dnOpenSchema/compents/<name>.ts` + `library/components/<name>/schema.ts`）手工保持一致，schema 改动一处忘改其余两处是常事。

## 相关页面

- [[projects/flow-design-system/concepts/triple-repo-component-contract]] — 三仓协作契约的完整 9 步 SOP
- [[projects/flow-design-system/concepts/designable-iframe-component-bridge]] — iframe postMessage 桥的细节
- [[projects/flow-design-system/concepts/ai-component-library-runtime]] — AI 组件库 controller 结构
- [[projects/flow-design-system/concepts/dynamic-require-resolveweak-loading]] — 运行时按目录名动态加载机制
- [[projects/flow-design-system/concepts/ai-vs-core-component-source-routing]] — CORE/AI 双源判定逻辑
- [[projects/flow-design-system/skills/add-new-builtin-component-three-repo-sop]] — 新增业务组件的端到端操作清单
