---
title: 动态 require.resolveWeak 加载 — 业务组件按目录名发现
category: concepts
tags:
  - react
  - formily
  - designable
  - f2e
  - protocol-design
  - plugin-system
sources:
  - "_raw/2026-08-07-153809-flowimage-1.txt (Claude Code 多仓会话, 2026-08-07)"
created: 2026-08-07T15:38:09Z
updated: 2026-08-07T15:38:09Z
summary: acme-dplatform-flow-v2-core 运行时通过 `require.resolveWeak('@/modules/template/builtin-components/<name>')` 按目录名动态加载业务组件的 `index.ts`，新增组件无需改运行时入口；与 `preview/config.ts` 的 `components` 白名单（设计器可见性）配合实现「零注册中心」组件系统。
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
  - target: "[[projects/flow-design-system/concepts/designable-iframe-component-bridge]]"
    type: related_to
  - target: "[[concepts/extensibility]]"
    type: related_to
  - target: "[[entities/chezmoi]]"
    type: related_to
---

# 动态 require.resolveWeak 加载 — 业务组件按目录名发现

> acme-dplatform-flow-v2-core 渲染器用 `require.resolveWeak('@/modules/template/builtin-components/<name>')` **按目录名**动态加载组件的 `index.ts`，新增业务组件**完全不用改运行时入口**。这与「`preview/config.ts` 的 `components` 白名单」形成两层 —— 前者是**运行时加载机制**，后者是**设计器可见性机制**，缺一会"运行时报组件不存在"或"设计器看不到"。

## 加载机制

```ts
// acme-dplatform-flow-v2-core/src/components/render/utils.ts:53
const componentPath = `@/modules/template/builtin-components/${name}`;  // name 来自 templateJson.componentType
const Component = require.resolveWeak(componentPath);  // 解析路径，不立即 require
// 在实际渲染时再 require 该路径对应的 index.ts
```

| 步骤 | 何时发生 | 作用 |
|------|---------|------|
| `require.resolveWeak(path)` | 渲染组件时 | 解析路径到模块 ID（弱引用，不打包进 chunk） |
| `require(path)` | 实际渲染 | 加载模块，默认导出 `index.ts` 的 React 组件 |
| `componentMap[componentType]` | 渲染时 | 业务组件通过 `componentType` 字符串查找到 React 组件 |

> **弱引用**（`resolveWeak`）的好处是 webpack 不会把整个 `builtin-components/` 目录打进首屏 bundle —— 按需懒加载，新组件不打乱现有 chunk 切分。

## 与「components 白名单」的关系

| 机制 | 路径 | 负责什么 | 新增组件是否需要改 |
|------|------|---------|------------------|
| 运行时加载 | `render/utils.ts:53` `require.resolveWeak` | **能不能渲染** | **不需要**（按目录名自动发现） |
| 设计器可见 | `preview/config.ts` `components` 数组 | **设计器面板里能不能看到** | **需要**（追加 `TermsCardConfig`） |
| AI 源可见 | `library/components/index.ts` `buildComponents()` | **AI 源设计器面板里能不能看到** | **需要**（追加 `TermsCardConfig`） |
| schema 兜底 | `dnOpenSchema/compents/<name>.ts` | **tenant=tenantA 时的 schema 副本** | **可选**（兜底用） |

> 三个白名单是**三个独立维度** —— 任一缺漏只会影响该维度对应的功能，**不会**全盘崩。诊断时要按"运行时报错 vs 面板看不到 vs 配置面板空白"分情况。

## 与 plugin-system 的对照

| 维度 | 本模式 | [[concepts/extensibility]]（典型 plugin） |
|------|--------|------------------------------------------|
| 注册入口 | 目录 + 三个白名单 | 显式 `plugins: []` 数组 |
| 加载方式 | 弱引用 + 懒加载 | `register(plugin)` 后立即激活 |
| 失败反馈 | `require.resolveWeak` 返回 null → 渲染 fallback | `register` 抛错阻止启动 |
| 发现成本 | 新组件必须知道 3 个白名单的位置 | 新插件必须知道 1 个 `plugins` 数组位置 |
| 适用场景 | 业务组件库（百级） | 通用功能扩展（十级） |

> **本模式优点**：没有"插件管理后台"这种重机制，组件名 + 目录就是合约。
> **本模式缺点**：3 个白名单位置散落，新增组件容易漏一处。

## 命名即合约的脆弱性

由于「目录名 = `name` = `componentType`」是隐性合约，重命名组件时需要同步改 5 处：

| 处 | 文件 | 改什么 |
|----|------|--------|
| 1 | 物理目录 `builtin-components/<old>/` | 改 `<old>` 为 `<new>` |
| 2 | `config.ts` 的 `name` 字段 | 改 `<old>` 为 `<new>` |
| 3 | `preview/config.ts` 的 `components` 数组 import + 数组项 | 改 import 路径 + 变量名 |
| 4 | `library/components/index.ts` 的 import + 数组项 | 改 import 路径 + 变量名 |
| 5 | `dnOpenSchema/compents/<old>.ts` 兜底副本（若有） | 重命名文件 + 更新 `dnOpenSchema/index.ts` 引用 |

> 与 chezmoi 命名前缀哲学（[[entities/chezmoi]]）：本模式是「目录 = 组件类型」的扁平命名，而 chezmoi 是「文件名 = 行为」的嵌套命名。两者都把"命名"提到合约高度，但本模式**多了一份白名单对齐义务**。

## 调试：运行时报组件不存在

| 报错 | 根因 | 修复 |
|------|------|------|
| `Cannot find module '@/modules/template/builtin-components/terms-card'` | 目录没建 / 路径写错 | 检查 `ls src/modules/template/builtin-components/terms-card/` |
| `Component is not a function` | `index.ts` 的 default export 不是 React 组件 | `index.ts` 应该是 `import './style.scss'; export default TermsCard;` |
| 渲染空白但无报错 | `componentMap[componentType]` 拿不到组件 | 确认 `templateJson.componentMap` 里的 `componentType` 与目录名一致 |
| 渲染空白 + 浏览器 console 有 `Module not found` | `preview/config.ts` 的 schema 引用路径错 | 检查 `config.ts` 里 `import schema from './schema';` |

## 相关页面

- [[projects/flow-design-system/flow-design-system]] — 项目总览
- [[projects/flow-design-system/concepts/triple-repo-component-contract]] — 9 步 SOP
- [[projects/flow-design-system/concepts/designable-iframe-component-bridge]] — iframe 上送机制
- [[concepts/extensibility]] — 通用插件系统对比
- [[entities/chezmoi]] — 命名即元数据的另一范式
