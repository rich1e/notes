---
title: Photo Album Mobile UI 项目
category: project
tags: [figma, react, codesign, mobile-ui, journal]
sources:
  - store/project for X/figma/App.jsx
  - store/project for X/figma/DESIGN.md
  - store/project for X/figma/SCREEN08_PATCH_NOTE.md
  - store/project for X/figma/MEMORY.md
created: 2026-08-23T16:15:00Z
updated: 2026-08-23T16:15:00Z
base_confidence: 0.85
lifecycle: active
lifecycle_changed: "2026-08-23"
summary: iOS 移动端相册 UI 项目,八屏 React artifact 在 CoDesign 客户端内渲染,iPhone 14/15 Pro/Max 三机型并列预览,七屏+屏8(手账 · 相册墙)已验证
---

# Photo Album Mobile UI 项目

iOS 移动端相册应用的多设备预览原型 — 自包含 React artifact 在 CoDesign desktop 客户端内渲染,每屏同时显示在 iPhone 14 Pro / 15 Pro / 15 Pro Max 三个机型框中。^[extracted:DESIGN.md 项目定位]

## 项目元信息

- **路径**:`/Users/rich1e/store/project for X/figma/`
- **设计 ID**:`482ad7d4-a010-43d3-8517-078c4701af91`(CoDesign session)
- **运行时**:CoDesign desktop plugin host(自包含 JSX,不依赖外部资源)
- **本地调试**:Vite scaffold at `/tmp/figma-scaffold/`
- **MEMORY.md**:项目内的结构化状态追踪(workspace scope,本项目独有)

## 八屏架构

| # | 屏幕 | 中文 | 设计 token |
|---|---|---|---|
| 01 | Inner Album | UNTITLED 封面 | `cover.mint #58a89f` + `spine.orange #c7502a` |
| 02 | Album Library | 我的相册 | 6 个 thumb variant |
| 03 | Photo Viewer | 单张照片详情 | coastal landscape 调色 |
| 04 | Settings | 设置 / 关于 | cyan-on-cream icons |
| 05 | Memories | 回忆 / 时刻 | 5 种 `mem.palette.*` 风景 |
| 06 | Memories Map | 回忆地图 | `map.continent #58a89f` + 5 cluster pins |
| 07 | Journal Entry | 手账 · 日记详情 | journal.* + cursive stack |
| 08 | Photo Wall | 手账 · 相册墙 | 复用屏7 原语 + PaperClip/ThumbPin |

## 关键约束(代码以外的隐性知识)

- **TWEAK_DEFAULTS** 是 CoDesign 编辑器的注入点,值保留在源文件头部,改了会被插件覆盖还原
- **JOURNAL_PALETTE 是扁平结构**:`washiMint`/`washiRose`/`washiPink`/`washiCream` 等平铺,**没有**嵌套的 `washi.*` 子对象(屏8 探索早期版本踩过这个坑)
- **手账 cursive stack**:`Snell Roundhand, Bradley Hand, Segoe Script, Comic Sans MS, cursive` — 只用于手写感标题/正文/极坐标,UI chrome 仍用 SF Pro
- **纯内联 SVG**:无外部字体/图片/图标 URL,所有插画(Sun/Cloud/Rain/Sprout/Character/Polaroid/Washi/PaperClip/ThumbPin)都是 inline `<svg>`

## 项目本地知识

- [[projects/figma/concepts/screen-08-photo-wall]] — 屏8 三段分区 + 4 原语的结构与已知坑
- [[projects/figma/skills/codesign-session-jsonl-recovery]] — 当 artifact.jsx 被破坏时,从 CoDesign session JSONL 完整恢复
- [[projects/figma/skills/codesign-artifact-vite-scaffold]] — artifact.jsx 在本地 Vite 上跑起来的两处改造 + 最小脚手架

## 相关通用概念

- [[entities/figwright]] — 与本项目无关的另一套 Figma 集成方案(MCP server)
- [[concepts/atomic-state-recovery]] — 类似思路:状态被破坏时的二次证据路径
- [[concepts/design-md-format-spec]] — 项目用 DESIGN.md 做设计系统说明书,符合此规范