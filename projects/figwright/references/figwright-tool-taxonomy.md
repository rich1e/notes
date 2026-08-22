---
title: Figwright 112 tool 分类
category: reference
tags: [figma, mcp, tool, figwright, reference]
sources:
  - https://github.com/awdr74100/figwright
created: 2026-08-14T08:00:00Z
updated: 2026-08-14T08:00:00Z
summary: Figwright 暴露 112 MCP tool,三分类(Read/Write/Grounding);本表按 README 描述 + packages/mcp/src/tools/ 文件名索引
base_confidence: 0.50
lifecycle: draft
lifecycle_changed: 2026-08-14
tier: supporting
provenance:
  extracted: 0.75
  inferred: 0.20
  ambiguous: 0.05
---

# Figwright 112 tool 分类

Figwright 暴露 112 MCP tool,分三组(README:829)。

> Your MCP client lists every tool at connect time — that's always the authoritative, up-to-date catalog.

实际 catalog 以 `tools/list` 响应为准。本表基于 README 描述 + `packages/mcp/src/tools/` 实际文件清单 ^[inferred]。

## 三分类

| 分类 | 工具数 | 职责 |
|---|---|---|
| Read | ~30 | 选择/文档/节点检视、样式、变量、组件、字体、reactions、Motion 状态、截图、原 image-fill 资产、PDF 导出、动画视频导出(MP4/GIF/WebM) |
| Write | ~75 | 创建编辑 frame/text/shape/auto-layout/effects/styles/variables/components(含 boolean/text/instance-swap properties)/pages/reactions/Motion(keyframes/animation-style presets/timelines)+ `batch` 批量应用 |
| Grounding | ~7 | `get_design_context`(去重上下文)+ `component_map`/`token_map`/`icon_map`(Figma → codebase 映射)+ `design_diff`(vs baseline 增量报告) |

> 注:精确分类与计数基于代码文件清单推断,不是从 `tools/list` 实时抓取 ^[ambiguous]。

## Read 工具(部分)

| 工具 | 文件 | 用途 |
|---|---|---|
| `get_selection` | `get-selection.ts` | 当前选择节点 |
| `get_document` | `get-document.ts` | 整个文档 |
| `get_node` / `get_nodes_info` | `get-node.ts` / `get-nodes-info.ts` | 节点详情 |
| `get_metadata` | `get-metadata.ts` | 元信息 |
| `get_pages` | `get-pages.ts` | 页面列表 |
| `get_viewport` | `get-viewport.ts` | 视口 |
| `get_styles` | `get-styles.ts` | 样式列表 |
| `get_fonts` | `get-fonts.ts` | 字体列表 |
| `get_variable_defs` | `get-variable-defs.ts` | 变量定义 |
| `get_local_components` | `get-local-components.ts` | 本地组件 |
| `get_reactions` / `get_annotations` | `get-reactions.ts` / `get-annotations.ts` | 反应/批注 |
| `get_motion_styles` / `get_node_motion` | `get-motion-styles.ts` / `get-node-motion.ts` | Motion |
| `get_screenshot` | `get-screenshot.ts` | 截图 |
| `export_pdf` | `export-pdf.ts` | PDF |
| `export_video` | `export-video.ts` | 视频(MP4/GIF/WebM) |
| `list_files` | `list-files.ts` | 本地 Figma 文件 |
| `scan_text_nodes` / `scan_nodes_by_types` | `scan-text-nodes.ts` / `scan-nodes-by-types.ts` | 节点扫描 |
| `search_nodes` | `search-nodes.ts` | 节点搜索 |

## Write 工具(部分)

### 创建(`create-*`)

- `create_frame`、`create_rectangle`、`create_ellipse`、`create_text`、`create_section`
- `create_component`、`create_instance`
- `create_paint_style`、`create_text_style`、`create_effect_style`、`create_grid_style`
- `create_variable`、`create_variable_collection`

### 设置(`set-*`)

- `set_fills`、`set_strokes`、`set_effects`、`set_corner_radius`、`set_opacity`、`set_blend_mode`、`set_mask`、`set_visible`、`set_constraints`
- `set_position`、`set_arc`、`set_auto_layout`、`set_layout_grids`、`set_layout_props`、`set_text`、`set_text_properties`、`set_text_range`
- `set_variable_value`、`set_variable_code_syntax`
- `set_reactions`、`set_instance_properties`
- `set_timeline_duration`、`apply_animation_style`、`apply_manual_keyframe_track`、`remove_animation_style`、`remove_manual_keyframe_track`

### 编辑

- `clone_node`、`reparent_nodes`、`resize_nodes`、`rotate_nodes`、`move_nodes`、`reorder_nodes`、`rename_node`、`delete_nodes`、`group_nodes`、`ungroup_nodes`、`lock_nodes`
- `bind_variable_to_node`、`bind_variable_to_paint`
- `combine_as_variants`、`detach_instance`、`swap_component`、`import_image`、`import_svg`、`find_replace_text`
- `batch_rename_nodes`、`batch`(批量多 edits)
- 组件属性:`add_component_property`、`edit_component_property`、`delete_component_property`、`bind_component_property`、`component_property`
- 页面:`add_page`、`rename_page`、`delete_page`、`navigate_to_page`
- 样式:`update_paint_style`、`update_text_style`、`update_effect_style`、`delete_style`
- 变量:`rename_variable`、`delete_variable`、`delete_variable_collection`、`add_variable_mode`
- 应用样式:`apply_style_to_node`

## Grounding 工具(关键 5)

| 工具 | 职责 |
|---|---|
| `get_design_context` | **最核心**:结构化节点树 + token 名 + globalVars + componentProperties |
| `component_map` | Figma 组件 → 本地代码组件(status + candidate.filePath + matchedProps) |
| `token_map` | Figma variable → 本地 token(ref + matchedBy,含 figmaModes theme-aware) |
| `icon_map` | Figma icon → 本地 `.svg` |
| `design_diff` | 与 baseline 比,报告变更(用于增量更新代码) |

## 其他

- `ping`:健康检查
- `analyze_project`:探测代码库栈(返回 profile 给 component_map/token_map 用)
- `design_context_guard`:防止 design context 失真的守卫 ^[inferred]
- `save_image_fills` / `save_screenshots`:保存原始资产

## 完整清单权威来源

```
npx -y @figwright/mcp@latest
# 启动后,mcp client 的 tools/list 返回完整 catalog(动态)
```

## 相关

- [[projects/figwright/figwright]] 项目主页
- 设计哲学 [[projects/figwright/concepts/provider-first-codegen]]
- 工作流 [[projects/figwright/skills/figma-codegen-workflow]]
- 协议 [[projects/figwright/references/figwright-shared-protocol]]