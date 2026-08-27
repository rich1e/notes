---
title: "Open CoDesign — MIT 开源设计 agent 桌面应用"
category: entities
tags: [open-codesign, opencoworkai, electron, design-agent, byok, mit-license]
sources:
  - "[[references/open-codesign-readme]]"
  - "[[references/open-codesign-changelog]]"
created: 2026-08-24
updated: 2026-08-24
summary: OpenCoworkAI/open-codesign 是 MIT 开源桌面应用,作为 Claude Design / v0 / Lovable / Bolt.new 的替代品。Electron + React 19 + Vite 6 + Tailwind v4 monorepo(pnpm workspace),BYOK 多模型(Claude/GPT/Gemini/Kimi/GLM/Ollama),基于 pi-coding-agent 的 workspace-backed agent loop。
base_confidence: 0.90
provenance:
  extracted: 0.85
  inferred: 0.10
  ambiguous: 0.05
lifecycle: draft
lifecycle_changed: 2026-08-24
tier: supporting
relationships:
  - target: "[[entities/pi-coding-agent]]"
    type: uses
  - target: "[[concepts/agentic-design]]"
    type: implements
  - target: "[[projects/figma/figma]]"
    type: related_to
  - target: "[[entities/opencoworkai]]"
    type: part_of
---

# Open CoDesign

## 概述

**仓库**: `[[entities/opencoworkai|OpenCoworkAI]]/open-codesign`(GitHub)
**协议**: MIT
**类型**: Electron 桌面应用
**定位**: Claude Design / v0 / Lovable / Bolt.new 的开源替代品

## 关键属性

| 属性 | 值 |
|---|---|
| 技术栈 | Electron + React 19 + Vite 6 + Tailwind v4 |
| 包管理 | pnpm workspace monorepo |
| AI 基础 | @mariozechner/pi-ai + pi-coding-agent |
| 模型 | BYOK 多模型:Claude / GPT / Gemini / Kimi / GLM / Ollama |
| 安装 | brew cask / scoop / 直接 DMG(winget 待 Microsoft review) |
| 当前版本 | v0.2.0 "Agentic Design" (2026-05-09) |
| 安全 | SVG 清洗 + Electron safeStorage + 私网探测 opt-in |

## 仓库结构

```
apps/                       # 桌面应用
packages/                   # 共享包(pi 集成、core 工具、skills)
docs/                       # 文档
examples/                   # 示例设计
scripts/                    # 构建/发布脚本
website/                    # 官网源
packaging/                  # brew/scoop/winget manifest
```

## 演进时间线

- **v0.1.0** (2026-04-18) — 首次公开 release,SQLite + 加密 TOML 一次性生成
- **v0.1.1** — JSX preview 解锁
- **v0.1.2 / 0.1.3** — SHA256SUMS.txt + CycloneDX SBOM
- **v0.1.4** — AI image generation, ChatGPT Plus 登录
- **v0.2.0** (2026-05-09) — **Agentic Design**:workspace-backed sessions + permissioned tool use + JSONL 历史

## 与 vault 已有 figma 项目

[[projects/figma/figma]] 是用户本地运行于 open-codesign 的 figma 项目。open-codesign 提供:
- 自包含 JSX artifact 的渲染宿主
- session JSONL 存于 `~/Library/Application Support/@open-codesign/desktop/sessions/<designId>.jsonl`
- 屏 8 等设计可直接 preview

## 与同类产品对比

| 产品 | 类型 | 关系 |
|---|---|---|
| **Anthropic Claude Design** | 闭源 SaaS | open-codesign 的"替代目标" |
| **Google Stitch** | 闭源 SaaS | 同源(design + AI),不同范式 |
| **v0.dev** | 闭源 SaaS | 同替代目标 |
| **Lovable** | 闭源 SaaS | 同替代目标 |
| **Bolt.new** | 闭源 SaaS | 同替代目标 |

open-codesign 是该领域少数开源且 BYOK 选项,适合不愿锁定 SaaS 厂商的设计师 / 设计团队。

## 相关

- [[references/open-codesign-readme]]
- [[references/open-codesign-changelog]]
- [[entities/opencoworkai]] — 发布此工具的组织
- [[concepts/agentic-design]]
- [[concepts/jsonl-session-tree]]
- [[concepts/skill-progressive-disclosure]]
- [[concepts/design-md-shared-memory]]
- [[entities/pi-coding-agent]]
- [[projects/figma/figma]]