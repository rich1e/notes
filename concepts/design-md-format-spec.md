---
title: "DESIGN.md 格式规范"
category: concepts
tags: [design-system, design-tokens, ai-coding, format-spec, concept]
summary: "DESIGN.md 是 Google Labs 提出的设计系统格式：YAML frontmatter 承载机器可读 token（colors/typography/rounded/spacing/components），Markdown body 按 8 个必备章节顺序承载人类可读 rationale。awesome-design-md 扩展到 11 章节（加 Iteration Guide 与 Known Gaps）。"
sources:
  - "https://github.com/google-labs-code/design.md"
  - "https://github.com/VoltAgent/awesome-design-md"
created: "2026-07-28T01:00:00Z"
updated: "2026-07-28T01:00:00Z"
tier: supporting
lifecycle: draft
lifecycle_changed: "2026-07-28"
base_confidence: 0.85
provenance:
  extracted: 0.92
  inferred: 0.05
  ambiguous: 0.03
    type: related_to
relationships:
  - target: "[[concepts/design-system-as-ai-context]]"
    type: related_to
  - target: "[[concepts/design-md-token-interpolation]]"
    type: related_to
  - target: "[[entities/awesome-design-md]]"
    type: related_to
  - target: "[[entities/google-labs-code-design]]"
    type: related_to

---

# DESIGN.md 格式规范

> YAML tokens + Markdown prose——DESIGN.md 是机器可读与人类可读的二层结构。

## 文件结构

一个 DESIGN.md 由**两层**组成：

```text
┌─────────────────────────────────────────────────────┐
│  YAML frontmatter（机器可读 token）                   │
│  ---                                                │
│  version: alpha                                     │
│  name: <品牌/系统名>                                 │
│  colors:        { primary: "#1A1C1E", ... }         │
│  typography:    { h1: {fontFamily, fontSize, ...} }  │
│  rounded:       { sm: 4px, md: 8px, ... }            │
│  spacing:       { sm: 8px, md: 16px, ... }           │
│  components:    { button-primary: { ... } }          │
│  ---                                                │
├─────────────────────────────────────────────────────┤
│  Markdown body（人类可读 rationale，按顺序的章节）      │
│  ## Overview                                        │
│  ## Colors                                          │
│  ## Typography                                      │
│  ## Layout                                          │
│  ## Elevation & Depth                               │
│  ## Shapes                                          │
│  ## Components                                      │
│  ## Do's and Don'ts                                 │
└─────────────────────────────────────────────────────┘
```

来源：[[entities/google-labs-code-design.md|google-labs-code/design.md]](https://github.com/google-labs-code/design.md) 官方 spec。

## Token 类型

| 类型 | 格式 | 示例 |
|------|------|------|
| **Color** | 任意 CSS 颜色 | `"#1A1C1E"`、`"oklch(62% 0.18 250)"`、`"rebeccapurple"` |
| **Dimension** | 数字 + 单位 | `48px`、`-0.02em`、`0.5rem` |
| **Typography** | 对象 | `{fontFamily, fontSize, fontWeight, lineHeight, letterSpacing, fontFeature, fontVariation}` |
| **Token Reference** | `{path.to.token}` | `{colors.primary}`、`{typography.body-md}`、`{rounded.lg}` |

详见 [[concepts/design-md-token-interpolation]]。

## 强制 8 章节（可省略，但出现时必须按序）

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

章节顺序与别名由 [google-labs-code/design.md spec](https://github.com/google-labs-code/design.md/blob/main/docs/spec.md) 规定。重复章节 → 报错拒绝；未知章节 → 保留不报错。

## 章节内容（来自 [[entities/awesome-design-md.md|awesome-design-md]] 真实样本）

### Overview（必备）

> "Notion presents itself as the all-in-one workspace through a confident, illustration-rich brand voice — anchored by a deep navy hero band..."

——一段 prose 描述品牌的 mood / voice / philosophy。AI agent 读它来理解"为什么"。

### Colors（必备）

按 role 分小节：Brand / Surface / Text / Semantic。例如 Vercel DESIGN.md 的 `### Brand & Accent`、`### Surface`、`### Text`、`### Semantic`、`### Brand Gradient`。

### Typography（必备）

`### Font Family` + `### Hierarchy`（完整的 display/body/caption 字号阶梯表）+ `### Principles`（行高、字间距、字体替换策略）+ `### Note on Font Substitutes`（缺字时如何 fallback）。

### Layout（必备）

`### Spacing System` + `### Grid & Container` + `### Whitespace Philosophy` + `### Responsive Strategy`（Breakpoints / Touch Targets / Collapsing Strategy / Image Behavior）。

### Elevation & Depth（必备）

Shadow / surface hierarchy。包含 `### Decorative Depth`（品牌特殊装饰元素）。

### Shapes（必备）

Border radius scale + Photography geometry（图片形状约束）。

### Components（必备）

按组件类型分小节：Buttons / Cards & Containers / Inputs & Forms / Navigation / Signature Components（品牌独有组件）。每个组件用 `{path.to.token}` 引用前文 token。

### Do's and Don'ts（必备）

`### Do` + `### Don't`——明确允许与禁止的反模式。这是 agent 在没有显式规则时避免"AI taste"漂移的关键段。详见 [[concepts/design-md-anti-patterns]]。

## 扩展章节（awesome-design-md 自加）

| # | Section | 用途 |
|---|---------|------|
| 9 | Responsive Behavior | 拆出 Layout 中的 responsive 子项，独立成节 |
| 10 | Iteration Guide | 给 AI agent 的修改守则（如 "Focus on ONE component at a time"、"Reference component names and tokens directly"、"Run `npx @google/design.md lint DESIGN.md` after edits"） |
| 11 | Known Gaps | 透明度声明——明确哪些细节 *未能* 捕获（如 dark-mode token 值、动画时长） |

spec 允许未知章节保留，所以扩展不会被 lint 拒绝。Iteration Guide 与 Known Gaps 是 awesome-design-md 团队的**最佳实践贡献**，不是规范要求。

## 版本与迁移

- **当前 `version: alpha`**：spec 仍在演进，schema 可能在升级时变化。
- **升 alpha 时未破坏主结构**：截至 2026-07-28 8 必备章节结构稳定。
- **与 Design Tokens Community Group 兼容**：token 语法借鉴 [DTCG 2025.10 规范](https://www.designtokens.org/tr/2025.10/format/#abstract)，可以无损转换到 `tokens.json` / Figma variables / Tailwind theme configs。

## 验证工具

```bash
npx @google/design.md lint DESIGN.md         # 结构 + WCAG + 引用闭环
npx @google/design.md diff DESIGN.md DESIGN-v2.md   # 两份之间做 token-level + prose regression
```

CLI 输出 JSON，severity ∈ {error, warning, info}。详见 [[sources/google-design-md-spec]]。

## 相关页面

- [[sources/google-design-md-spec]] — 官方规范来源
- [[sources/awesome-design-md-repo]] — 74 个真实样本
- [[concepts/design-md-token-interpolation]] — `{path.to.token}` 引用机制
- [[concepts/design-md-anti-patterns]] — "AI taste" 与反模式
- [[concepts/design-system-as-ai-context]] — 上游：为什么 DESIGN.md 是 AI agent 的硬约束
