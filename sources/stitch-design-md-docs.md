---
title: "Google Stitch DESIGN.md 官方文档入口"
category: references
tags: [stitch, design-system, ai-coding, google-labs, source]
sources:
  - "https://stitch.withgoogle.com/docs/design-md/overview/"
  - "https://stitch.withgoogle.com/docs/design-md/specification/"
source_url: "https://stitch.withgoogle.com/docs/design-md/"
created: "2026-07-28T01:00:00Z"
updated: "2026-07-28T01:00:00Z"
summary: "Google Stitch 官方的 DESIGN.md 文档站点，包含 overview 与 specification 两页。Stitch 用自然语言生成 UI 时自动产出 DESIGN.md，agent 后续读取该文件保持视觉一致。"
base_confidence: 0.75
lifecycle: draft
lifecycle_changed: "2026-07-28"
provenance:
  extracted: 0.40
  inferred: 0.50
  ambiguous: 0.10
---

# Google Stitch DESIGN.md 官方文档入口

> DESIGN.md 由 Google Stitch 首次引入，作为 AI agent 持久读入的视觉契约。

## 文档站点

| 页面 | 路径 | 状态 |
|------|------|------|
| Overview | https://stitch.withgoogle.com/docs/design-md/overview/ | 200 OK（Angular SPA，defuddle/WebFetch 拿不到正文） |
| Specification | https://stitch.withgoogle.com/docs/design-md/specification/ | 200 OK（同上） |
| Docs 根 | https://stitch.withgoogle.com/docs/ | 200 OK |

## 已知信息（从下游交叉验证）

> **重要**：本页对 Stitch 官方 docs 的具体内容**几乎全部依赖下游来源**（awesome-design-md README、[google-labs-code/design.md](https://github.com/google-labs-code/design.md) 的 spec、Sachin Sharma 的 [[misc/web-medium-com-devsecops-ai-how-google-stitch-claude-codes-mcp-integration]] 文章）。Stitch docs 本身是 JS-rendered SPA，defuddle 与 WebFetch 都拿不到正文——这是本研究的客观限制。^[ambiguous]

| 主题 | 内容 | 来源 |
|------|------|------|
| DESIGN.md 起源 | "A new concept introduced by Google Stitch" | [[sources/awesome-design-md-repo]] README |
| 格式定义 | "A plain-text design system document that AI agents read to generate consistent UI" | 同上 |
| 落地方式 | Stitch 生成 UI 时**自动产出** DESIGN.md，放在项目根目录，agent 后续读取保持一致 | [[misc/web-medium-com-devsecops-ai-how-google-stitch-claude-codes-mcp-integration]] |
| 与 Stitch MCP 集成 | 通过 `claude mcp add stitch --transport http https://stitch.googleapis.com/mcp ...` 让 Claude Code 远程 fetch DESIGN.md | [[skills/claude-code-mcp-auth-patterns]] |
| 完整 spec | 严格以 [[sources/google-design-md-spec]] 为权威（Google Labs 官方 spec 仓库） | [[sources/google-design-md-spec]] |

## 客观局限

- **官方 docs JS-rendered**：defuddle / WebFetch 拿不到正文（这是 Stitch 产品前端的事实，不是我们工具的缺陷）。
- **第三方权威**：google-labs-code/design.md 的 `docs/spec.md` 才是可机器读的规范；Stitch docs 站点主要承担产品级介绍 + UI 截图展示。
- **未必覆盖 8 章节全部**：Stitch 实际生成的 DESIGN.md 是否覆盖所有 8 必备章节？未在公开来源里找到 stitch 端输出的样本文件——`known_gaps` 是真实空白。^[ambiguous]

## 相关页面

- [[entities/google-stitch]] — Stitch 产品本体
- [[sources/google-design-md-spec]] — 官方规范仓库（机器可读 spec）
- [[sources/awesome-design-md-repo]] — 74 个真实站点 DESIGN.md 精选集
- [[concepts/design-md-format-spec]] — 规范总结
- [[misc/web-medium-com-devsecops-ai-how-google-stitch-claude-codes-mcp-integration]] — Stitch → Claude Code 完整集成实操