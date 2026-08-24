---
title: "OpenCoworkAI/open-codesign README — 项目总览"
category: references
tags: [open-codesign, electron, react, vite, tailwind, byok, monorepo]
sources:
  - "https://github.com/OpenCoworkAI/open-codesign"
source_url: "https://github.com/OpenCoworkAI/open-codesign"
created: 2026-08-24
updated: 2026-08-24
summary: open-codesign README:Electron+React 19+Vite 6+Tailwind v4 monorepo(pnpm workspace),AI 基于 @mariozechner/pi-ai + pi-coding-agent,BYOK 多模型(Claude/GPT/Gemini/Kimi/GLM/Ollama)。
base_confidence: 0.85
provenance:
  extracted: 0.85
  inferred: 0.10
  ambiguous: 0.05
lifecycle: draft
lifecycle_changed: 2026-08-24
tier: supporting
---

# OpenCoworkAI/open-codesign README

## 项目定位

MIT 开源桌面应用(Electron),作为 Claude Design / v0 / Lovable / Bolt.new 的替代品。BYOK(自带 Key)模式连接多模型,local-first,MIT 协议。

## 技术栈

| 层 | 技术 |
|---|---|
| 桌面壳 | Electron |
| UI | React 19 + Vite 6 + Tailwind v4 |
| 打包 | electron-builder |
| 包管理 | pnpm workspace |
| AI 基础 | @mariozechner/pi-ai + pi-coding-agent |

## 仓库结构

pnpm workspace:

```
apps/                  # 桌面应用
packages/              # 共享包(pi 集成、core 工具、skills)
docs/                  # 文档
examples/              # 示例设计
scripts/               # 构建/发布脚本
website/               # 官网源
packaging/             # brew/scoop/winget manifest
```

隐藏根目录配置: `.Codex/` / `.claude/` / `.changeset/` / `.husky/` / `.vscode/` / `.github/`。

## 关键声明(原文摘录)

> Each design is a pi session with JSONL history and a workspace folder on disk.

> Built-in tools gated by Open CoDesign's permission UI: read, write, edit, bash, grep, find, ls.

> On-demand design tools: ask, scaffold, skill, preview, gen_image, tweaks, todos, done.

> Twelve built-in design skill modules ship with the app (slides, dashboards, landing pages, SVG charts, glassmorphism, editorial typography, heroes, pricing, footers, chat UIs, data tables, calendars).

> Custom taste: add a SKILL.md to any project to teach the model your own taste.

> Brand tokens and design-system decisions become editable files, not model memory.

## 安装

```bash
# macOS
brew install --cask opencoworkai/tap/open-codesign

# Windows
scoop bucket add opencoworkai https://github.com/OpenCoworkAI/scoop-bucket
scoop install open-codesign/open-codesign
```

直接 DMG 下载(winget 等待 Microsoft review: microsoft/winget-pkgs#372310)。

## 与 vault 已有 figma 项目的关系

vault 中 [[projects/figma/figma]] 是用户本地的 figma 项目(使用 open-codesign 渲染)。open-codesign 是该项目运行所在的桌面客户端本身。本研究补全了 [[projects/figma/figma]] 之外的运行时知识(AI loop、skill 系统、JSONL session 结构)。

## 相关

- [[entities/open-codesign]] — open-codesign 项目实体
- [[synthesis/Research: open-codesign]] — 综合分析
- [[projects/figma/figma]] — 本机 figma 项目,运行于 open-codesign 客户端