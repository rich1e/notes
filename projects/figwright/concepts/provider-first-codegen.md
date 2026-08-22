---
title: provider-first codegen
category: concept
tags: [codegen, ai-agent, design-tools, mcp, figwright, provider-first]
sources:
  - https://github.com/awdr74100/figwright
created: 2026-08-14T08:00:00Z
updated: 2026-08-14T08:00:00Z
summary: provider-first codegen 哲学:不输出固定模板,先 analyze_project 探测代码库栈+样式+组件+token+icon,再让模型生成与现有 codebase 风格一致的代码
base_confidence: 0.55
lifecycle: draft
lifecycle_changed: 2026-08-14
tier: supporting
provenance:
  extracted: 0.75
  inferred: 0.20
  ambiguous: 0.05
---

# provider-first codegen

**Provider-first codegen** = Figwright 的核心设计哲学,与"固定模板编译器 pipeline"路线对立。

## 核心命题

> rather than a fixed compiler pipeline, the tools surface honest design context and let the model generate code that matches _your_ codebase.

不是"输出固定 React + Tailwind 模板",而是:
1. **探测**(`analyze_project` 工具 + `component_map`/`token_map`/`icon_map` 返回的 profile)
2. **暴露结构化上下文**(`get_design_context` 给节点树 + token + 组件实例)
3. **让模型生成** 与现有 codebase 风格一致的代码

## 三层基础

| 工具 | 职责 |
|---|---|
| `get_design_context(detail: 'full', dedupeComponents: true)` | 节点结构树 + token 名(`Primary/500`/`spacing/4`)+ 样式 dedupe 成 `globalVars` + 每个 instance 的 `mainComponent`/`componentProperties` |
| `component_map` | Figma 组件 → 本地代码组件(status: high/medium/low/unmapped + candidate.filePath + matchedProps) |
| `token_map` | Figma variable → 本地 token(ref + matchedBy) |
| `icon_map` | Figma icon → 本地 `.svg` 资产 |

## 复用 vs 新建 的判定规则

```
candidate.status='high'/'medium' → 复用:import from candidate.filePath(不重新生成)
candidate.status='low'           → 验证后再决定(ambiguousWith 列出多个候选项)
candidate.status='unmapped'      → 新建:用项目风格构建;若 instanceCount>1,从首个 instance 子树构建
```

**严格禁止**:
- 发明 `component_map` 没报告的组件名
- 把 `ambiguousWith` 候选项当确认复用(必须先 verify)
- 硬编码 hex/px 而忽略 `token_map` 的 `ref`
- 重复 unmapped 组件时"凭眼睛看"重建(必须 `get_design_context` on `instances[0].nodeId`)

## 与 vault 已有知识的对应

| vault 已有 | provider-first 对应 |
|---|---|
| [[concepts/design-md-token-interpolation]] `{path.to.token}` 引用 | `token_map.candidate.ref` 引用 |
| [[concepts/design-md-anti-patterns]] Do's and Don'ts 决策规则 | `token_map.matchedBy: ['name']` 漂移警告 + `verify-me pick` 提醒 |
| [[entities/google-stitch]] DESIGN.md 自动化产出 | `component_map`/`token_map` 探测回 profile |

## 设计哲学背后

- **诚实失败分桶**:`matchedBy: ['name']`(name 漂移)/ `matchedBy: ['value']`(值相等但名字不匹配)/ `ambiguousWith`(多个候选无法判断)/ `unmapped`(无对应)—— 不输出模糊对
- **theme-aware**:`figmaModes: { Light, Dark }` 处理文件的主题轴;无 native modes 的 plan-limited workaround(paired collections / name groups)同样处理
- **framework built-in vs arbitrary**:`tailwind spacing/4` 用 `p-4` 而非 `p-[16px]`;`line-height/7` 用 `leading-7`

## 相关

- [[projects/figwright/figwright]] 项目主页
- [[projects/figwright/concepts/design-context-grounding]] `get_design_context` 抽象
- [[projects/figwright/skills/figma-codegen-workflow]] 完整工作流
- 同类概念 [[concepts/design-md-format-spec]] / [[concepts/design-md-anti-patterns]]