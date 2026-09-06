---
title: AI 组件库运行时 — acme-core-goods-ai 的 controller 结构
category: concepts
tags:
  - koa
  - bff
  - api-design
  - system-architecture
  - design-system
  - ai-coding
sources:
  - "_raw/2026-08-07-153809-flowimage-1.txt (Claude Code 多仓会话, 2026-08-07)"
created: 2026-08-07T15:38:09Z
updated: 2026-08-07T15:38:09Z
summary: acme-core-goods-ai（BFF）的 AI 组件库 controller 结构：`library/components/<name>/{config,schema}.ts` 双文件、汇总数组 `components/index.ts` 的 `buildComponents(isLimitUser)`、路由前缀 `/public/v1` + controller 装饰器 `@controller('/component-library')` = 完整路径 `/public/v1/component-library/{query-config,components/query-schema}`。
tier: core
lifecycle: draft
lifecycle_changed: "2026-08-07"
base_confidence: 0.88
provenance:
  extracted: 0.92
  inferred: 0.06
  ambiguous: 0.02
relationships:
  - target: "[[projects/flow-design-system/flow-design-system]]"
    type: related_to
  - target: "[[projects/flow-design-system/concepts/triple-repo-component-contract]]"
    type: related_to
  - target: "[[projects/flow-design-system/concepts/designable-iframe-component-bridge]]"
    type: related_to
  - target: "[[projects/flow-design-system/concepts/ai-vs-core-component-source-routing]]"
    type: related_to
---

# AI 组件库运行时 — acme-core-goods-ai 的 controller 结构

> acme-core-goods-ai（Koa.js v3 + TypeScript BFF）作为「AI 组件库」的运营配置来源。每个业务组件用「双文件」描述（`config.ts` 元数据 + `schema.ts` Formily 配置面板 schema），由汇总数组 `buildComponents(isLimitUser)` 返回；设计器侧 `applyLibrary` 直接消费。**关键路径不在前端也不在设计器，而在 BFF 的运营配置目录**。

## 目录布局

```
acme-core-goods-ai/app/controller/component-library/
├── library/
│   ├── types.ts                           # DesignableComponent / CategoriesKey
│   ├── categories/                        # （可选）分类的 schema 副本
│   └── components/
│       ├── index.ts                       # 汇总数组 buildComponents()
│       ├── terms/config.ts                # { name, title, categories, schema }
│       ├── terms/schema.ts
│       ├── terms-display/config.ts
│       ├── terms-display/schema.ts
│       ├── terms-card/config.ts           # ← 新增
│       ├── terms-card/schema.ts           # ← 新增
│       ├── question/config.ts
│       ├── question/schema.ts
│       └── ... (~107 个组件目录)
└── controller/                            # 实际 Koa controller 装饰器
    ├── index.ts                           # @controller('/component-library') 装饰
    └── ...
```

## 双文件 contract

```ts
// config.ts
import type { DesignableComponent } from '../../types';
import { CategoriesKey } from '../../types';
import schema from './schema';

const config: DesignableComponent = {
  name: 'terms-card',                         // 字符串必须与目录名一致
  title: '保险条款卡片',
  schema,                                     // 引用同目录 schema.ts
  categories: [CategoriesKey.DISPLAY],         // = ['display']
};

export default config;
```

```ts
// schema.ts
import type { ISchema } from '../../types';

const schema: ISchema = {
  type: 'object',
  properties: {
    title: { type: 'string', title: '卡片标题' },
    terms: { type: 'array', 'x-component': 'ArrayCollapse', /* ... */ },
    // ... 与核心仓 builtin-components/terms-card/schema.ts 字段一一对应
  },
};

export default schema;
```

> `CategoriesKey` 来自 BFF 仓的 `library/types.ts` —— 跟核心仓的 `CATEGORIES_KEY` 是不同文件，**字符串值相同**（'display' / 'layout' / 等）但不是同一个 import 路径。

## 汇总与构建

```ts
// library/components/index.ts
import { buildConfig as ImageConfig } from './image/config';
import TermsConfig from './terms/config';
import TermsDisplay from './terms-display/config';
import TermsCardConfig from './terms-card/config';           // ← 新增 import
import ToolbarConfig from './toolbar/config';
// ... ~107 个 import

export function buildComponents(isLimitUser = false): DesignableComponent[] {
  return [
    ImageConfig(isLimitUser),                                // 部分组件需要 isLimitUser 参数
    TermsConfig,
    TermsDisplay,
    TermsCardConfig,                                          // ← 新增位置
    ToolbarConfig,
    // ...
  ];
}
```

`isLimitUser` 是该 BFF 的「是否受限用户」开关 —— 部分组件（如内部灰度组件）会基于这个参数有条件返回。`buildComponents(false)` 返回全量 ~107 个组件。

## 路由与 controller 装饰器

| 层 | 路径 | 文件 | 作用 |
|----|------|------|------|
| 路由前缀 | `/public/v1` | `app/router/public.ts` | 把所有公开接口挂到统一前缀 |
| Controller 装饰器 | `@controller('/component-library')` | `app/controller/component-library/controller/index.ts:13` | 标注路由段名 |
| Endpoint 1 | `POST /public/v1/component-library/query-config` | `ComponentLibraryController.queryConfig` | 返回 `{ data: { globalConfig, presets, categories, components } }` |
| Endpoint 2 | `POST /public/v1/component-library/components/query-schema` | `ComponentLibraryController.querySchema` | 单组件 schema 查询（懒加载场景） |

> **路径拼装小坑**：`/public/v1`（路由前缀）+ `/component-library`（controller 装饰器）+ `/query-config`（方法路径）= **`POST /public/v1/component-library/query-config`**。前端 fetch 走 `/ai/public/v1/component-library/query-config`，开发代理剥掉 `/ai` 前缀才命中本路径。

## 端到端验证

```bash
# 1. 启动 BFF
cd acme-core-goods-ai && pnpm dev    # 默认 8080

# 2. 验证 query-config 包含 terms-card
curl -s -X POST http://localhost:8080/public/v1/component-library/query-config \
     -H "Content-Type: application/json" -d '{"isLimitUser":false}' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); \
    comps=d['data']['components']; \
    print('total:', len(comps)); \
    print('terms-card in list?', any(c['name']=='terms-card' for c in comps)); \
    print([c['name'] for c in comps if 'term' in c.get('name','')])"
```

期望：`total: 107`、`terms-card in list? True`、列表含 `['terms', 'terms-display', 'terms-card']`。

```bash
# 3. 验证 query-schema 单独返回 terms-card schema
curl -s -X POST http://localhost:8080/public/v1/component-library/components/query-schema \
     -H "Content-Type: application/json" -d '{"name":"terms-card"}' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); \
    print('success:', d.get('success')); \
    print('component keys:', list(d.get('data',{}).get('component',{}).keys()))"
```

## 与 vault 已有概念的对应

| BFF 仓模式 | vault 类似模式 | 差异 |
|----------|-------------|------|
| 双文件 `config.ts` + `schema.ts` | 单纯一页 frontmatter | 本模式把元数据与 schema 分开，便于 schema 复用 + 跨多组件 |
| `buildComponents(isLimitUser)` | 普通工厂函数 | isLimitUser 让一个汇总函数处理多套组件库（受限/全量） |
| 路由前缀 + controller 装饰器 | 单文件 router | Koa 装饰器风格，**端点路径是两层拼接**（易漏前缀） |
| `applyLibrary(library)` 直接吃数组 | vault 的 manifest | 设计器不持久化，每次 refresh 都重拉 |

## 相关页面

- [[projects/flow-design-system/flow-design-system]] — 项目总览
- [[projects/flow-design-system/concepts/triple-repo-component-contract]] — 9 步 SOP
- [[projects/flow-design-system/concepts/designable-iframe-component-bridge]] — iframe 上送机制
- [[projects/flow-design-system/concepts/ai-vs-core-component-source-routing]] — CORE/AI 双源判定