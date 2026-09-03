---
title: figma-codegen 工作流
category: skill
tags: [figma, codegen, mcp, skill, figwright, ai-agents, design-tools]
sources:
  - https://github.com/awdr74100/figwright
created: 2026-08-14T08:00:00Z
updated: 2026-08-14T08:00:00Z
summary: figma-codegen skill 的 5 步工作流:get_design_context → component_map → token_map → icon_map+assets → emit code;严格规则:复用>verify-me>重建
base_confidence: 0.55
lifecycle: draft
lifecycle_changed: 2026-08-14
tier: supporting
provenance:
  extracted: 0.90
  inferred: 0.05
  ambiguous: 0.05
---

# figma-codegen 工作流

Figwright 官方 `figma-codegen` skill 的 5 步工作流(Figma → code)。

## 触发条件

- 用户粘贴 Figma URL/选择并请求代码("code this"、"build this component")
- 用户希望扩展已有组件去匹配 Figma frame

## 工作流(顺序严格)

```
1. get_design_context(detail='full', dedupeComponents=true)
       ↓ 节点结构树 + token 名 + globalVars + componentProperties
2. component_map
       ↓ Figma 组件 → 本地代码组件(status: high/medium/low/unmapped + candidate.filePath)
3. token_map
       ↓ Figma variable → 本地 token(ref + matchedBy,含 theme-aware figmaModes)
4. export assets 接地(save_image_fills + icon_map + get_screenshot)
       ↓ 真正像素资产(logo/photo/icon)
5. emit code  ← 由模型根据 profile 自由发挥,但遵守复用规则
```

## 步骤 1: get_design_context

详见 [[projects/figwright/concepts/design-context-grounding]]

- **必传**:`detail: 'full'` + `dedupeComponents: true`
- **不要**depth-limit 将构建的子树
- **不要**单独信任截图;context 才是 ground truth
- Dev Mode annotations 是 ground truth 的一部分
- 大页面超出一次调用:`get_design_context` on 子节点

## 步骤 2: component_map 复用规则

| status | 动作 |
|---|---|
| `high` / `medium` | **直接复用** `candidate.filePath`(import 那个组件) |
| `low`(verify-me pick) | 先看 `candidate.ambiguousWith` 列出多个候选;**确认后** 才复用;确认后写进 map file 让下次运行确定 |
| `unmapped`(无对应代码组件) | 用项目风格**新建**;若 `instanceCount > 1`,从**首个 instance 子树**构建;若首个子树 dedupe/truncated,`get_design_context` on `instances[0].nodeId` 重读一次 |
| (写组件**自身定义**) | 用 `get_component_api` 拿完整 property API(VARIANT option + BOOLEAN/TEXT/INSTANCE_SWAP 默认值) |

**严禁**:
- 发明 `component_map` 没报告的组件名
- 把 `ambiguousWith` 候选项当确认复用(会成 silent visual bug)
- 重复 unmapped 组件时"凭眼睛看"重建

## 步骤 3: token_map 复用规则

| matchedBy | 动作 |
|---|---|
| `['name']` | 直接复用 `candidate.ref`(如 `var(--color-primary-500)`);**但若值漂移,标 warning** |
| `['value']`(name-blind 等值) | **hypothesis, 不是 binding**;语义对则用 ref,语义错则保留 raw value 并标 gap;**bound Figma variable 永远 outranks raw value match** |
| `ambiguousWith` | 多个 project token 共享同一值 → verify-me pick,按语义选 |
| `framework-builtin`(Tailwind scale) | 用 `builtin: {scale, step}` 组合 utility(`p-4`/`gap-4`/`leading-7`/`font-bold`)**不**用 arbitrary `p-[16px]` |
| `unmapped` | 用 raw value + 主动 surface gap(提议加进 token source) |
| `figmaModes: {Light, Dark}` | theme-dependent;emitted ref 必须配合项目 dark 机制(`.dark` / `[data-theme]` / `prefers-color-scheme` / Tailwind `dark:`) |

## 步骤 4: assets

- **`save_image_fills`**:`IMAGE`-fill 节点的**原始资产**(不是被裁剪/重渲染的)
- **`icon_map`** first:复用策划的 `.svg`
- **`get_screenshot`**:仅看合成视觉

## 步骤 5: emit code

- **profile 来自 `component_map`/`token_map` 的响应**(不调用 `analyze_project` 自身)
- 复用组件 wire 各 instance props(variant/boolean/text/instance-swap 解析值)
- 颜色/间距/圆角/字体 一律用 token ref
- `unmapped` 部分用项目风格构建 + surface 提议(加进 token source)

## 增量编辑(非 one-shot)

设计会动。第二次不要整页重做 —— 用 `design_diff` 对 baseline 报告变更,**只在变了的子树上重跑**上面 5 步。

## 关键失败模式

| 失败 | 表现 | 修复 |
|---|---|---|
| `dedupeComponents: false` | instance 重复展开,token 爆 | 永远 `true` |
| `matchedBy: ['value']` 当作 binding | 用了语义错的 token | 保留 raw value + 标 gap |
| 重复 unmapped 组件"凭眼睛看" | 多 instance 生成不一致 | 用 `instances[0]` 子树统一生成 |
| 忽略 `figmaModes` | 单一主题渲染,Dark mode 失效 | 配合项目 dark 机制 |
| `unmapped` 硬编码 | 设计 token 体系被绕过 | 主动提议加进 source |

## 集成链路

```
claude code / cursor / codex
       │ (MCP stdio)
       ▼
  @figwright/mcp ──── WebSocket ────→ Figma plugin
       │
       ▼
  figma-codegen skill 自动加载 ← 当 task description 匹配
       │
       ▼
  按上面 5 步生成代码到本地项目
```

## 相关

- [[projects/figwright/figwright]] 项目主页
- 反向方向 [[projects/figwright/skills/figma-build-workflow]]
- 工具速查 [[projects/figwright/references/figwright-tool-taxonomy]]
- 设计哲学 [[projects/figwright/concepts/provider-first-codegen]]