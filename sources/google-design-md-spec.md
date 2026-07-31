---
title: "google-labs-code/design.md — DESIGN.md 官方格式规范与 CLI"
category: references
tags: [design-system, ai-coding, stitch, google-labs-code, open-spec, source]
sources:
  - "https://github.com/google-labs-code/design.md"
  - "https://raw.githubusercontent.com/google-labs-code/design.md/main/README.md"
  - "https://registry.npmjs.org/@google/design.md"
source_url: "https://github.com/google-labs-code/design.md"
created: "2026-07-28T01:00:00Z"
updated: "2026-07-28T01:00:00Z"
summary: "Google Labs 出品的 DESIGN.md 规范仓库 + npm CLI（@google/design.md, v0.4.0）。权威定义 DESIGN.md 文件 schema、token 类型、section 顺序，并提供 lint/diff 工具。"
base_confidence: 0.85
lifecycle: draft
tier: supporting
lifecycle_changed: "2026-07-28"
provenance:
  extracted: 0.95
  inferred: 0.03
  ambiguous: 0.02
---

# google-labs-code/design.md — DESIGN.md 官方格式规范与 CLI

> DESIGN.md 的权威规范来源：Google Labs 官方仓库，提供文件 schema、`@google/design.md` CLI 工具，以及与 [Design Tokens Community Group](https://www.designtokens.org/tr/2025.10/format/#abstract) 兼容的 token 语法。

## 仓库概述

| 字段 | 值 |
|------|----|
| 仓库 | [google-labs-code/design.md](https://github.com/google-labs-code/design.md) |
| 维护者 | Google Labs Code 组织 |
| Stars / Forks | ~26.5K / ~2.1K（截至 2026-07-28） |
| 许可证 | Apache-2.0 |
| 创建日期 | 2026-04-10 |
| 最新提交 | 2026-07-28 |
| 当前版本 | `version: alpha`（DESIGN.md 文件 schema）+ `@google/design.md` npm 包 v0.4.0 |
| 配套文档 | `docs/spec.md`（15K 字节完整规范）+ `README.md` |

## 关键事实

### DESIGN.md 文件 schema

一个 DESIGN.md 由两层组成：

1. **YAML frontmatter**（机器可读 token）：
   ```yaml
   ---
   version: alpha
   name: Heritage
   description: ...
   colors:
     primary: "#1A1C1E"
   typography:
     h1:
       fontFamily: Public Sans
       fontSize: 3rem
   rounded:
     sm: 4px
     md: 8px
   spacing:
     sm: 8px
     md: 16px
   components:
     button-primary:
       backgroundColor: "{colors.tertiary}"
       textColor: "{colors.on-tertiary}"
       rounded: "{rounded.sm}"
   ---
   ```
2. **Markdown body**（人类可读 rationale）：按规范顺序的 `##` 章节。

### Token 类型与引用

| 类型 | 格式 | 示例 |
|------|------|------|
| Color | 任意 CSS 颜色（hex / `rgb()` / `oklch()` / named） | `"#1A1C1E"`、`"oklch(62% 0.18 250)"` |
| Dimension | 数字 + 单位 | `48px`、`-0.02em` |
| Typography | `fontFamily` + `fontSize` + `fontWeight` + `lineHeight` + `letterSpacing` + 可选 `fontFeature` / `fontVariation` | 详见面板对象 |
| Token Reference | `{path.to.token}` | `{colors.primary}`、`{typography.body-md}` |

引用语义允许组件定义里跨字段插值（`backgroundColor: "{colors.tertiary}"`）。引用在 `lint` 时会被解析闭环验证。

### 强制 8 章节顺序

`##` 章节可省略，但**出现时必须按此顺序**：

| # | Section | Aliases |
|---|---------|---------|
| 1 | Overview | Brand & Style |
| 2 | Colors | |
| 3 | Typography | |
| 4 | Layout | Layout & Spacing |
| 5 | Elevation & Depth | Elevation |
| 6 | Shapes | |
| 7 | Components | |
| 8 | Do's and Don'ts | |

> **注意**：`awesome-design-md` 仓库在 8 必备之外**额外扩展**了 `Iteration Guide` 与 `Known Gaps` 两节——这是 spec 允许的自由扩展（"Unknown section heading → Preserve; do not error"），不是必备。

### Consumer 行为约束

| 场景 | 行为 |
|------|------|
| 未知章节标题 | 保留，不报错 |
| 未知 color token 名 | 接受（只要 value 是合法颜色） |
| 未知 typography token 名 | 接受 |
| 未知 component property | 接受，但告警 |
| 重复章节标题 | 报错，拒绝文件 |

### `@google/design.md` CLI（v0.4.0）

```bash
# lint：结构 + WCAG 对比度 + 引用闭环
npx @google/design.md lint DESIGN.md
npx @google/design.md lint --format json DESIGN.md
cat DESIGN.md | npx @google/design.md lint -    # stdin

# diff：两份 DESIGN.md 之间做 token-level 与 prose regression
npx @google/design.md diff DESIGN.md DESIGN-v2.md

# Windows 兼容
npx -p @google/design.md designmd lint DESIGN.md   # 用 designmd 别名（避免 .md 文件关联冲突）
npm install "@google/design.md"                       # PowerShell 需要引号
```

`lint` 输出 JSON 形如：

```json
{
  "findings": [
    {
      "severity": "warning",
      "path": "components.button-primary",
      "message": "textColor (#ffffff) on backgroundColor (#1A1C1E) has contrast ratio 15.42:1 — passes WCAG AA."
    }
  ],
  "summary": { "errors": 0, "warnings": 1, "infos": 1 }
}
```

### 与 Design Tokens Community Group 兼容

DESIGN.md 的 token 系统**借鉴** [Design Tokens Community Group 规范](https://www.designtokens.org/tr/2025.10/format/#abstract)：typed token groups（colors / typography / spacing）+ `{path.to.token}` 引用语法。仓库文档明确说 *"These tokens are easily converted from or to `tokens.json`, Figma variables, and Tailwind theme configs."*。

## 局限

- **仍在 alpha**：spec 仍在 `version: alpha`，token schema 与章节顺序可能在升级时变化——但升 alpha 时未破坏 README 主推的 8 章节结构。
- **CLI 仅 lint / diff**：没有 `format`、`init`、`new-component` 这类便利命令；写新 DESIGN.md 主要靠手写。
- **CLI 不强制完整 8 章节**：未指定时 `lint` 不报错——但 awesome-design-md 等下游可能会假设完整覆盖。
- **不是 LLM 微调触发器**：DESIGN.md 是给 LLM 的**输入**（让 agent 一次性读到 design rationale + token），不是用来微调 / 训练模型的数据格式。

## 相关页面

- [[sources/awesome-design-md-repo]] — 74 个真实站点 DESIGN.md 精选集
- [[sources/stitch-design-md-docs]] — Stitch 官方 docs 入口
- [[concepts/design-md-format-spec]] — 本仓库定义的规范详情
- [[concepts/design-md-token-interpolation]] — `{path.to.token}` 引用机制
- [[entities/google-labs-code-design]] — 本仓库实体页