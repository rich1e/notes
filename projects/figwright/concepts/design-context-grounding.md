---
title: design context grounding
category: concept
tags: [grounding, design-context, mcp-tool, figwright, ai-agent]
sources:
  - https://github.com/awdr74100/figwright
created: 2026-08-14T08:00:00Z
updated: 2026-08-14T08:00:00Z
summary: get_design_context 工具:把 Figma 选择转成结构化上下文树(节点+token 名+样式 dedupe+组件实例属性),让模型不靠截图猜
base_confidence: 0.55
lifecycle: draft
lifecycle_changed: 2026-08-14
tier: supporting
provenance:
  extracted: 0.85
  inferred: 0.10
  ambiguous: 0.05
---

# design context grounding

`get_design_context` = Figwright 的核心 grounding 工具。设计哲学的工程化体现:**让模型基于结构化真值生成,而非基于截图 OCR**。

## 工具调用形态

```
get_design_context({
  detail: 'full',
  dedupeComponents: true   // 强烈建议
})
```

输出是结构化树,包含:
- **layout**:节点几何信息(x/y/width/height + auto-layout/grid 配置)
- **tokens**:token **名**而非裸 hex/px(`Primary/500`、`spacing/4` 而非 `#6266F0`/`16px`)
- **styles**:dedupe 后的 `globalVars`(相同 paint/effect/text style 全局共享一个 ID)
- **components**:每个 instance 的 `mainComponent` + `componentProperties`(VARIANT/BOOLEAN/TEXT/INSTANCE_SWAP 的解析值)

## 与"按截图生成"对比

| 维度 | 截图 OCR | design context grounding |
|---|---|---|
| 输入 | PNG/JPG | Figma 实时结构 |
| token 名 | 看不到 | `Primary/500`(可对应 `var(--color-primary-500)`) |
| 组件复用 | 不知道 | `mainComponent: 'Button'`(可对应 `import Button from './Button'`) |
| 样式 dedupe | 重复识别 | 全局共享一次 |
| auto-layout 配置 | 推断 | 真实值 |
| per-side border / corner radius | 难判 | 精确 |
| blend / mask / gradient | 难判 | 精确 |
| Dev Mode annotations | 不可见 | ground truth |

## figma-codegen skill 的硬规则

> trust them over the rendered image.

**严格**:
1. 永远 `dedupeComponents: true`(否则 instance 重复展开浪费 token)
2. 不要 depth-limit 你将构建的子树
3. 与 `component_map`/`token_map` 配合使用,不要单独 `get_design_context` 然后"凭印象"写代码
4. 当 token `matchedBy: ['value']` 而非 `['name']` 时,必须 verify 而非直接复用

## Dev Mode annotations 的角色

Dev Mode annotations(设计师在 Figma 中标注的语义提示)是 ground truth 的一部分:
- "实际渲染时 padding 是 16,但设计稿画的是 20" → annotation 是 16
- 不读 annotation 等于丢掉设计师明确传达的意图^[inferred]

## 何时用 `get_screenshot` 而非 `get_design_context`

- 校验视觉:用 `get_screenshot` 看合成的视觉
- **不要用 screenshot 替代 context** —— OCR 不可靠(token 名/组件名/auto-layout 配置都拿不到)

## 增量编辑的设计变更追踪

`design_diff` 工具:把当前 Figma 状态与已保存的 baseline 比,返回变更列表。配合 `get_design_context` 在变了的子树上重新生成,**避免整页重做**。

## 与 vault 已有 grounding 概念对应

| vault 已有 | 本概念对应 |
|---|---|
| [[concepts/design-md-format-spec]] DESIGN.md schema | Figwright 是活体 grounding,DESIGN.md 是静态 grounding |
| [[concepts/static-analysis-knowledge-graph]] OpenLore 代码知识图谱 | 都是"用结构化算法替代 embedding 检索" |
| [[concepts/no-llm-hot-path]] hot path 0 LLM | `get_design_context` 在 LLM 调用前由 Figma API 完成结构化 |

## 相关

- [[projects/figwright/figwright]] 项目主页
- 设计哲学 [[projects/figwright/concepts/provider-first-codegen]]
- 完整工作流 [[projects/figwright/skills/figma-codegen-workflow]]