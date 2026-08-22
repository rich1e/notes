---
title: figma-build 工作流
category: skill
tags: [figma, build, mcp, skill, figwright, ai-agent, design-tools]
sources:
  - https://github.com/awdr74100/figwright
created: 2026-08-14T08:00:00Z
updated: 2026-08-14T08:00:00Z
summary: figma-build skill 反向工作流:code/描述 → Figma;复用文件现有组件和样式,在 Figma canvas 上构建设计
base_confidence: 0.45
lifecycle: draft
lifecycle_changed: 2026-08-14
tier: supporting
provenance:
  extracted: 0.50
  inferred: 0.45
  ambiguous: 0.05
---

# figma-build 工作流

Figwright 官方 `figma-build` skill 的反向工作流(code/描述 → Figma)。figma-codegen 的对偶方向。

## 触发条件

- 用户提供 code 或 spec description 并要求"在 Figma 中构建"(`Build a pricing section in Figma from this spec.`)
- 与 `figma-codegen` 形成完整双向循环:设计变 → 代码变 → 设计再变...

## 工作流(对比 codegen)

```
figma-codegen:  Figma ──(read context)──→ Code
figma-build:    Code/Spec ──(plan canvas)──→ Figma
```

`figma-build` 的具体步骤在 `skills/figma-build/SKILL.md`(未在本次 ingest 完整抓取);本笔记基于 README 描述与对称性推断 ^[inferred]。

## 推测的 5 步

```
1. analyze_project / 解析用户提供的 spec/代码
       ↓ 提取意图、布局、组件、token
2. search Figma canvas 已有组件(component_map 反向)
       ↓ 复用 main component,新建只用于真正缺失的
3. 规划 canvas 结构:frames + auto-layout + styles + variables
       ↓ 用 batch tool 一次性应用多个 edits
4. 应用 styles/variables(component_map/token_map 双向都用)
       ↓ 复用已有 styles 而非新建
5. verify: get_design_context 回读检查
       ↓ 确保 canvas 真实反映 spec
```

## 与 codegen 的对称性

| 步骤 | figma-codegen | figma-build |
|---|---|---|
| 1 | `get_design_context` 读 | `analyze_project` 或 spec 解析 |
| 2 | `component_map` 看 Figma 组件能映射到哪些代码组件 | `component_map` 看代码组件能复用哪些 Figma main component |
| 3 | `token_map` 把 Figma token 转代码 ref | `token_map` 把代码 token 映射到 Figma variable |
| 4 | emit code | batch apply frames/styles/variables |
| 5 | get_screenshot 校验 | get_design_context 回读 |

## 关键设计原则

- **复用优先**:文件已有 main component 必须用;已有 style 必须用;不要新建重复资产
- **batch tool** 一次性多个 edits(`packages/mcp/src/tools/batch.ts` + `packages/plugin/src/handlers/batch.ts`):减少 round-trip 与中间态
- **Motion 支持**:keyframes / animation-style presets / timelines 在 Write 工具组中(`apply-animation-style.ts`、`apply-manual-keyframe-track.ts`)
- **Variables first**:dark mode / theme switching 通过 Figma variables 处理,与 codegen 端的 `figmaModes` 对称

## Open Questions

- 真实 SKILL.md 内容本次未完整抓取,本笔记是基于 README + codegen 的对称推断 ^[inferred]
- `batch` tool 的原子性:失败时部分应用是否回滚?
- Motion 编辑的精度:keyframes 是否支持 spring physics?

## 相关

- [[projects/figwright/figwright]] 项目主页
- 正向方向 [[projects/figwright/skills/figma-codegen-workflow]]
- 工具速查 [[projects/figwright/references/figwright-tool-taxonomy]]