---
title: "Google Stitch + Claude Code MCP 工作流"
category: misc
tags: [ai-coding, claude-code, google-stitch, mcp, design-system, agentic-workflow]
sources:
  - "https://medium.com/devsecops-ai/how-google-stitch-claude-codes-mcp-integration-changed-the-way-i-build-products-63ecb8ed7f5a"
source_url: "https://medium.com/devsecops-ai/how-google-stitch-claude-codes-mcp-integration-changed-the-way-i-build-products-63ecb8ed7f5a"
created: "2026-07-28T00:00:00Z"
updated: "2026-07-28T00:00:00Z"
summary: "通过 Stitch MCP 把 Google Stitch 的 UI 设计以结构化形式喂给 Claude Code，消除 design→code 的人工搬运；两种鉴权（API key header vs Google Cloud OAuth proxy）路径。"
affinity:
  "[[skills/claude-code-mcp-auth-patterns]]": 3
  "[[concepts/mcp-server-protocol-quirks]]": 2
  "[[skills/claude-code-token-optimization]]": 2
promotion_status: misc
stub: false
provenance:
  extracted: 0.78
  inferred: 0.15
  ambiguous: 0.07
base_confidence: 0.45
lifecycle: draft
tier: supporting
lifecycle_changed: "2026-07-28"
---

# Google Stitch + Claude Code MCP 工作流

## Overview

Sachin Sharma 在 DevSecOps & AI 发表的一篇实操文章：用 Google Stitch（基于 Gemini 2.5 Pro 的 AI 设计工具）配合 Claude Code 的 MCP 集成，让"提示词生成 UI → agent 直接读设计 → 生成匹配 token 的代码"全程无需人工搬运。文中给出两种鉴权路径（Stitch API key 头 vs Google Cloud OAuth proxy）、一个 `.env` 干扰 OAuth 的踩坑记录，并提炼出"工具专业化优于全能"的更高层观点。

## Key Points

- **Stitch 的差异化产出**：除 HTML/CSS 之外，生成 `DESIGN.md`（颜色 token、字号尺度、布局规则的便携设计系统），AI agent 可原生理解。这是 Stitch + Claude Code 工作流的支点。
- **MCP 是 USB-C 类比**：把外部服务（设计、数据库、CI）以标准化协议接进 agent，取代剪贴板搬运。
- **Token 浪费的真相**：在没有设计系统的情况下让 Claude 调 UI（"padding 多一点"、"sidebar 没必要"），15 轮下来绝大部分上下文被间距/猜测吃掉，而不是逻辑和接线。
- **鉴权路径 1（推荐大多数人）**：
  ```bash
  claude mcp add stitch --transport http https://stitch.googleapis.com/mcp \
    --header "X-Goog-Api-Key: YOUR-API-KEY" -s user
  ```
  - `-s user` ≈ `--global`，写入顶层 `mcpServers`，与 [[concepts/mcp-server-protocol-quirks]] 的"默认项目级"陷阱形成对照。
  - `.claude.json` / `.mcp.json` 含明文 key，必须 `.gitignore`，暴露后立刻 rotate。
- **鉴权路径 2（长期重度使用）**：Google Cloud OAuth + `gcloud beta services mcp enable stitch.googleapis.com` + `npx @_davideast/stitch-mcp init` + `proxy`。优势是 token 自动 refresh；代价是 **项目根目录的 `.env` 文件会让 proxy 报 "invalid character 'd'"** —— 必须先挪开再跑。
- **OAuth 路径额外能力**：`stitch-mcp view --projects` / `--project ... --screen ...` / `serve -p <PROJECT_ID>` 在终端看设计稿或本地 dev server 预览。
- **设计→代码的提示词模板**（直接复用）：
  > "Use the Stitch MCP to fetch the dashboard screen. Extract the design system into a DESIGN.md file in my project root. Then scaffold the React components using Tailwind CSS, matching the design tokens exactly."
- **官方 Stitch 技能栈**：`npx skills add google-labs-code/stitch-skills --list` 列出七个（设计生成到多框架代码转换）。**分批装**——一次全装会让排障变难。
- **总用时**：从首个 Stitch 提示到 React dashboard 跑通不到 2 小时（含两条路径都试 + `.env` 重命名）。

## Concepts

- [[concepts/design-system-as-ai-context]] — `DESIGN.md` 不是给人看的设计文档，是给 AI agent 的"硬约束输入"——本文最值得抽象的一个观点。
- [[concepts/ai-tool-specialization]] — 文章末段"让 Stitch 拥有视觉层，让 Claude Code 拥有逻辑层"是 AI 工具栈组织原则的具体例证。
- [[concepts/mcp-server-protocol-quirks]] — `-s user` 等价 `--global`，本文是这条规则的又一次现身。
- [[skills/claude-code-mcp-auth-patterns]] — 两种鉴权（API key header vs OAuth proxy）的横向对比与故障清单。
- [[skills/claude-code-token-optimization]] — "没设计系统时设计决策吃 token"是本文的另一条支撑证据。

## Entities

- [[entities/google-stitch]] — Google Labs AI 设计工具，文中的视觉层主体。
- [[entities/claude-code]] — 文中承担逻辑与代码生成的 agent。
- `Sachin Sharma` ^[inferred] — 文章作者，linkedin.com/in/rksachin5，Cloud & Business Transformation 方向。
- `google-labs-code/stitch-skills` ^[inferred] — Google 官方的 Stitch 配套 Claude Code 技能仓库，列在 `npx skills add` 命令里。
- `@_davideast/stitch-mcp` ^[inferred] — npm 上的社区 OAuth proxy 包，Path 2 的核心依赖，作者 davideast。

## Open Questions

- Stitch 仍是实验性，API 目前免费——是否会收费、何时收费？文中未给时间表。 ^[ambiguous]
- OAuth path 报 "invalid character 'd'" 的具体根因：是 dotenv 解析器看到 `$VAR` 之外的字符就抛错，还是某个 npm 包对 `.env` 行末字符敏感？文中说是 GitHub 翻到的，未贴 issue 链接。 ^[ambiguous]
- "DESIGN.md 是 Google Stitch 私有格式还是开放规范？" —— `DESIGN.md` 字面上与 [Google 的 Stitch DESIGN.md](https://stitch.withgoogle.com) 提示的设计系统描述一致，但文章没说明是否上游开源、可被其他 agent 复用。 ^[ambiguous]

## Related

- [[skills/claude-code-mcp-auth-patterns]] — 同主题，更细的两条鉴权路径操作步骤。
- [[concepts/design-system-as-ai-context]] — 抽取的核心概念。
- [[concepts/ai-tool-specialization]] — 文章末尾"专业化优于全能"的抽象。
- [[concepts/mcp-server-protocol-quirks]] — `-s user` 行为背景。