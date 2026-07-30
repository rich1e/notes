---
title: "getdesign.md — VoltAgent DESIGN.md 目录与私人订制"
category: references
tags: [design-system, ai-coding, voltagent, marketplace, source]
sources:
  - "https://getdesign.md/"
  - "https://github.com/VoltAgent/awesome-design-md"
source_url: "https://getdesign.md/"
created: "2026-07-28T01:00:00Z"
updated: "2026-07-28T01:00:00Z"
summary: "VoltAgent 团队运营的 DESIGN.md 目录服务，把 awesome-design-md 仓库的 74 个站点以 /<site>/design-md URL 形式对外暴露；提供 /request 入口支持私人订制。"
base_confidence: 0.70
lifecycle: draft
lifecycle_changed: "2026-07-28"
provenance:
  extracted: 0.70
  inferred: 0.25
  ambiguous: 0.05
---

# getdesign.md — VoltAgent DESIGN.md 目录与私人订制

> 把 awesome-design-md 仓库的 74 个 DESIGN.md 文件以可访问 URL 暴露，并提供私人订制入口。

## 服务概述

| 字段 | 值 |
|------|----|
| 域名 | [getdesign.md](https://getdesign.md/) |
| 维护者 | VoltAgent 团队（与 [[sources/awesome-design-md-repo]] 同团队） |
| 主要入口 | 首页 + `/<site>/design-md` 路径 + `/request` 私人订制入口 |
| 收录站点数 | "300+" 自报，awesome-design-md 仓库实际 74 个 ^[inferred] |
| 商业化模式 | 私人订制（"We craft one for any website you want"）+ LaunchKit banner 广告（README 中） |

## URL 命名

每个站点的 DESIGN.md 通过 `getdesign.md/<site-slug>/design-md` 暴露。示例：

| 站点 | URL |
|------|-----|
| Claude | https://getdesign.md/claude/design-md |
| Vercel | https://getdesign.md/vercel/design-md |
| Notion | https://getdesign.md/notion/design-md |
| Linear | https://getdesign.md/linear.app/design-md |
| Stripe | https://getdesign.md/stripe/design-md |
| Cursor | https://getdesign.md/cursor/design-md |
| Raycast | https://getdesign.md/raycast/design-md |
| Cohere | https://getdesign.md/cohere/design-md |
| Cohere 之 Mistral | https://getdesign.md/mistral.ai/design-md |
| ... | https://getdesign.md/<slug>/design-md（74 个） |

URL 列表与 [[sources/awesome-design-md-repo]] README 的 Collection 表格一一对应。

## 主页标语（直接引用）

> "Give your coding agent a reusable design reference: colors, type, spacing, components, and the reasoning behind them."

> "Style your site without being a designer / Match a style you like from any reference site / Keep new pages in the same visual language / Restyle existing pages without starting over / Give your AI coder a reusable design brief."

> "Pick a DESIGN.md from a real site and hand it to your AI coder. It already carries the colors, type, and spacing, so you don't need to know any of it."

> "Follows Google's official DESIGN.md spec"

> "Maintained by VoltAgent team"

## 与 awesome-design-md 仓库的关系

- **同一团队**：foot 显式标注 *"Maintained by VoltAgent team"*，GitHub 链接指向 [[sources/awesome-design-md-repo]]。
- **同一素材**：每个 `getdesign.md/<site>/design-md` 返回的内容与仓库 `design-md/<site>/DESIGN.md` 等价。
- **私人订制**：仓库不收新 DESIGN.md（CONTRIBUTING.md 明确 *"We cannot accept DESIGN.md pull requests"*），但 getdesign.md 提供 `/request` 付费服务为你定做——这是单一团队的封闭内容生产链路。

## 客观局限

- **服务端 JS 渲染**：直接 fetch `/<site>/design-md` 拿到的是 SPA HTML，不一定返回原始 markdown 内容；目前从仓库 `raw.githubusercontent.com` 直接 curl 更可靠。
- **"300+" 自述**：首页声称 "300+"，但仓库实际只有 74 个——可能是营销数字与仓库数字脱节，或统计口径含历史版本。^[ambiguous]
- **私人订制价格不透明**：`/request` 入口存在但定价 / 交付时间未在抓到的页面里出现。

## 相关页面

- [[sources/awesome-design-md-repo]] — 主仓库
- [[entities/voltagent]] — 运营组织
- [[concepts/design-system-as-ai-context]] — DESIGN.md 作为 AI 上下文