---
title: 三仓组件注册契约 — 新增业务组件的 9 步 SOP
category: concepts
tags:
  - design-system
  - formily
  - f2e
  - designable
  - ai-coding
  - protocol-design
sources:
  - "_raw/2026-08-07-153809-flowimage-1.txt (Claude Code 多仓会话, 2026-08-07)"
created: 2026-08-07T15:38:09Z
updated: 2026-08-07T15:38:09Z
summary: ACME 司 商品中心新增一个 display 业务组件的 9 步 SOP：核心仓建目录+config/schema/tsx/index/样式、设计器仓注册+索引+分类、AI 后端仓建 config/schema+汇总、最终 ts/curl 验证。三方 `name` 字段与目录名严格对齐。
tier: core
lifecycle: draft
lifecycle_changed: "2026-08-07"
base_confidence: 0.88
provenance:
  extracted: 0.90
  inferred: 0.08
  ambiguous: 0.02
relationships:
  - target: "[[projects/flow-design-system/flow-design-system]]"
    type: related_to
  - target: "[[projects/flow-design-system/concepts/designable-iframe-component-bridge]]"
    type: related_to
  - target: "[[projects/flow-design-system/concepts/ai-component-library-runtime]]"
    type: related_to
  - target: "[[projects/flow-design-system/concepts/ai-vs-core-component-source-routing]]"
    type: related_to
  - target: "[[projects/flow-design-system/skills/add-new-builtin-component-three-repo-sop]]"
    type: related_to
  - target: "[[concepts/ai-tool-specialization]]"
    type: related_to
---

# 三仓组件注册契约 — 新增业务组件的 9 步 SOP

> CLAUDE.md 第 274 行「新增业务组件需在 `src/modules/template/builtin-components/` 注册，并保证组件类型与设计器侧一致」只有一句话，但**实际涉及的工位跨 3 个工程、共 9 步**。本页是这 9 步的展开版。

## 完整 9 步

> 案例：新增「保险条款卡片」`terms-card`（display 类）。

### 步骤 1-5：在 `acme-dplatform-flow-v2-core` 仓（核心运行时 / iframe 上送源）

| 步 | 路径 | 作用 | 关键约束 |
|----|------|------|---------|
| 1 | `src/modules/template/builtin-components/terms-card/` | 新建组件目录 | 目录名 = `terms-card` = `name` 字段；渲染器用 `require.resolveWeak('@/modules/template/builtin-components/terms-card')` 按目录名动态加载 |
| 2 | 同目录 `config.ts` | 元数据注册 | `name: 'terms-card'` / `title: '保险条款卡片'` / `categories: [CATEGORIES_KEY.DISPLAY]` / 引用 `schema` |
| 3 | 同目录 `schema.ts` | Formily 设计器配置面板 | `import { ISchema } from '@formily/json-schema'`；用 `FormLayout` + `Input` + `ArrayCollapse` 等 x-component 描述 props |
| 4 | 同目录 `index.ts` | 运行时入口 | `import './style.scss'; export default TermsCard;`（设计器 `require.resolveWeak` 加载的就是这个文件） |
| 5 | `TermsCard.tsx` + `style.scss`（+ 可选 `types.ts` / `constants.ts`） | 组件实现 | BEM 命名 `buildin-terms-card__*`；复用通用 `Part` 容器与全局 `--theme-primary`；`url` 跳转按 `http(s)://` / `//` / 其他 三档区分 `window.location.href` / `window.open` |

### 步骤 6：核心仓内的「设计器侧注册中心」

| 路径 | 作用 |
|------|------|
| `src/modules/preview/config.ts` | **第 1 处追加**：`import TermsCardConfig from '../template/builtin-components/terms-card/config';`<br>**第 2 处追加**：在 `DESIGNABLE_INITIALIZE_MESSAGE.components` 数组里紧跟 `TermsDisplay` 追加 `TermsCardConfig`（本仓第 1057-1060 行附近） |

> 这一步**不是**设计器侧的注册，是「核心仓作为 iframe 上送源」必须做的事 —— 设计器通过 iframe `postMessage` 收 `DESIGNABLE_INITIALIZE_MESSAGE` 来发现组件。

### 步骤 7：核心仓内的组件知识库（可选但推荐）

| 路径 | 作用 |
|------|------|
| `llm-wiki/docs/terms-card.md` | 按 `llm-wiki/TEMPLATE.md` 写组件文档（frontmatter: `name` / `title` / `categories` / `updated`） |
| `llm-wiki/wiki/index.md` | 组件索引表追加一行 |
| `llm-wiki/wiki/categories.md` | 分类表追加一行（按 `categories: [DISPLAY]` 对应到「展示组件」分类） |

### 步骤 8：在 `acme-dplatform-flow-v2` 仓（设计器父窗，可选）

CLAUDE.md 的「组件类型与设计器侧一致」**字面**意思是设计器侧要登记一份。但实际看代码：

- 设计器拖拽面板 `getSources(value)` 的 `components` 数据**完全由外部上送**（iframe 或 AI 后端）
- 设计器侧没有显式的「白名单注册入口」 —— 它从 `DESIGNABLE_INITIALIZE_MESSAGE` 拿
- 设计器侧 `dnOpenSchema/index.ts` 的 schema 副本**只在 `tenantFrom=tenantA` 或 `tenantB` 时作为兜底覆盖**用，不影响面板可见性

**所以设计器侧的真实必要动作**是：

1. 启动 `acme-dplatform-flow-v2-core` 的开发服务器（`npm run dev` / `npm run dev:ssr`），让 iframe 重新打包
2. 在设计器页面强制刷新（清 iframe 缓存 + 清 `localStorage` / `sessionStorage`）
3. 在 Network 监听 `INITIALIZE` 消息确认 `terms-card` 在 components 数组里

> **可选但建议**：在 `src/components/dnOpenSchema/compents/termsCard.ts` 加一份 schema 兜底（与 `builtin-components/terms-card/schema.ts` 字段一一对应），并在 `dnOpenSchema/index.ts` 汇总对象里加 `'terms-card': termsCard` —— 这是 schema 副本对齐，不是面板可见性的必要条件。

### 步骤 9：在 `acme-core-goods-ai` 仓（AI 组件库后端）

**仅当** 当前设计器环境命中 AI 组件库分支（`tenantFrom ∈ {tenantA, tenantB}` 且 `versionNum≠3` 且 `gcVersion≠v3`）才需要做。

| 路径 | 作用 |
|------|------|
| `app/controller/component-library/library/components/terms-card/config.ts` | 组件注册：`name` / `title` / `categories: [CategoriesKey.DISPLAY]` / 引用 `./schema` |
| `app/controller/component-library/library/components/terms-card/schema.ts` | schema 副本（与核心仓 `builtin-components/terms-card/schema.ts` 字段一一对应） |
| `app/controller/component-library/library/components/index.ts` | **第 1 处**：`import TermsCardConfig from './terms-card/config';`<br>**第 2 处**：在 `buildComponents()` 数组里紧跟 `TermsDisplay` 追加 `TermsCardConfig` |

## 验证（端到端）

### 核心仓类型校验

```bash
cd acme-dplatform-flow-v2-core
npx tsc --noEmit -p tsconfig.json 2>&1 | grep -E "terms-card|TermsCardConfig"
# 期望：空输出（零类型错误；项目既有的 libpag 类型问题与本组件无关）
```

### AI 后端接口验证

```bash
# 注意完整路径是 /public/v1/component-library/...（不是 /component-library/...）
curl -s -X POST http://localhost:8080/public/v1/component-library/query-config \
     -H "Content-Type: application/json" -d '{"isLimitUser":false}' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); \
    comps=d['data']['components']; \
    print('total:', len(comps)); \
    print('terms-card in list?', any(c['name']=='terms-card' for c in comps)); \
    [print(c['name'], c.get('categories')) for c in comps if 'term' in c.get('name','')]"
```

期望：107 个组件，terms-card 在列表里，与 terms / terms-display 同属 `['display']` 分类。

### 设计器面板显示验证

1. `pnpm dev` 启动 `acme-core-goods-ai`（默认 8080）
2. `npm run dev` 启动 `acme-dplatform-flow-v2`（默认 8000）
3. 临时改 `acme-dplatform-flow-v2/config/config.ts` 的 `/ai/` proxy target 为 `http://localhost:8080`（**记得测完改回**）
4. 访问 `http://localhost:8000/insure-config/<id>?tenantFrom=tenantB&...`
5. Cmd+Shift+R 强制刷新，展开"展示组件"分组，应看到「保险条款卡片」可拖拽节点

### 完整路径 / 关键中间件

| 端到端链路 | 关键中间件 |
|----------|----------|
| 浏览器 → `localhost:8000/ai/public/v1/component-library/query-config` | Umi dev proxy（`config/config.ts:108-115`）：`/ai/` → 剥掉 `/ai` 前缀 → 转发到 `target` |
| 转发到 → `localhost:8080/public/v1/component-library/query-config` | Koa BFF：路由前缀 `/public/v1`（`app/router/public.ts:6`）+ controller 装饰器 `@controller('/component-library')` |
| Controller → `ComponentLibraryController.queryConfig` | 调用 `buildComponentLibrary()` → `buildComponents(isLimitUser)` 返回数组 |
| 设计器 `useBroadcastEffect` 收到 `INITIALIZE` | 调 `applyLibrary(library)` → `engine.resource.from({presets, categories, components})` |
| 设计器 `getSources('display')` | 过滤 `categories.includes('display')` → 返回 `terms-card` resource 进面板 |

## 三处 schema 副本的对齐原则

**字面完全相同是错的**（因为 schema 里有 `categories: [CATEGORIES_KEY.DISPLAY]` 这种枚举引用，在三个仓的 `constants.ts` 都各自定义）。正确原则是**字段语义一一对应**：

- `properties.*.type` / `title` / `description` 完全相同
- `x-component` 引用同名字符串（在三个仓的 `@formily/json-schema` 解析层都认识）
- `categories` 数组的元素必须是各仓 `CATEGORIES_KEY.DISPLAY` 的字符串值（'display'）—— 不是枚举 import

## 失败模式速查

| 现象 | 根因 | 修复 |
|------|------|------|
| 核心仓 `tsc` 报错指向 `terms-card` | 组件 types.ts 漏了 `export` 或 import path 错 | 优先用 `npx tsc --noEmit` 加 `--strict` 失败再排查 |
| 接口返回 404 | 漏了 `/public/v1` 前缀 | 完整路径是 `POST /public/v1/component-library/query-config` |
| 接口通了但 terms-card 不在列表 | `components/index.ts` 的数组里没追加 | 检查 `import` + 数组 push 两处都加 |
| 设计器面板没显示 | iframe 缓存 + 走的是 AI 源（后端没同步） | Network 看 Server IP 是 test 还是 localhost；监听 `INITIALIZE` 消息 |
| 改了本地 AI 后端但设计器看不到 | Umi dev proxy target 写死 test 环境 | 临时改 target 为 `http://localhost:8080`，测完改回 |

## 相关页面

- [[projects/flow-design-system/flow-design-system]] — 项目总览与三仓角色表
- [[projects/flow-design-system/concepts/designable-iframe-component-bridge]] — iframe postMessage 桥的细节
- [[projects/flow-design-system/concepts/ai-component-library-runtime]] — AI 组件库 controller 结构
- [[projects/flow-design-system/concepts/dynamic-require-resolveweak-loading]] — 运行时按目录名动态加载
- [[projects/flow-design-system/concepts/ai-vs-core-component-source-routing]] — CORE/AI 双源判定
- [[projects/flow-design-system/skills/add-new-builtin-component-three-repo-sop]] — 9 步 SOP 的实操清单版
