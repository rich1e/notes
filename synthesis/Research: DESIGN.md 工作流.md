---
title: "Research: DESIGN.md 工作流"
category: synthesis
tags: [design-system, ai-coding, stitch, mcp, research]
sources:
  - "https://github.com/VoltAgent/awesome-design-md"
  - "https://github.com/google-labs-code/design.md"
  - "https://stitch.withgoogle.com/docs/design-md/overview/"
  - "https://getdesign.md/"
  - "https://medium.com/devsecops-ai/how-google-stitch-claude-codes-mcp-integration-changed-the-way-i-build-products-63ecb8ed7f5a"
created: "2026-07-28T01:00:00Z"
updated: "2026-07-28T01:00:00Z"
summary: "DESIGN.md 三轮研究综合：Google Labs 规范 + VoltAgent 74 个真实样本 + Stitch 自动产出 + Claude Code MCP 集成。提炼出 'YAML tokens + Markdown prose' 二层结构、8 必备章节、{path.to.token} 引用、Do's and Don'ts 反模式机制。"
base_confidence: 0.85
lifecycle: draft
lifecycle_changed: "2026-07-28"
provenance:
  extracted: 0.80
  inferred: 0.15
  ambiguous: 0.05
relationships:
  - target: "[[concepts/design-system-as-ai-context]]"
    type: extends
  - target: "[[concepts/ai-tool-specialization]]"
    type: extends
  - target: "[[entities/google-stitch]]"
    type: related_to
  - target: "[[entities/awesome-design-md]]"
    type: related_to
  - target: "[[entities/google-labs-code-design]]"
    type: related_to
---

# Research: DESIGN.md 工作流

> Google Labs 提出的"AI 友好的设计系统格式"——YAML tokens + Markdown prose，让任何 AI coding agent 都能像设计师一样产出品牌一致 UI。

## Overview

DESIGN.md 是 Stitch（Google Labs 的 AI 设计工具）首次引入的格式：一个**自包含的 markdown 文件**，上半部分是机器可读的 design tokens（YAML），下半部分是人类可读的设计 rationale（markdown prose）。它把"设计系统"从设计师的工具（CSS 变量 / Figma variables）扩展成**所有 AI agent 都能读**的输入物——Stitch 自己生成、Claude Code 读它来生成匹配代码、awesome-design-md 仓库提供 74 个真实站点的样本。

研究覆盖：仓库结构、文件 schema、token 引用语法、与 Stitch 工作流集成、与 Claude Code MCP 集成、迭代工作流、IP / 局限性。

## Key Findings

### F1. DESIGN.md 是二层结构（YAML + Markdown）

DESIGN.md 文件由两层组成：

1. **YAML frontmatter**：`version: alpha` + `name` + `description` + 4 类 token groups（colors / typography / rounded / spacing）+ 可选 `components`。机器可读。
2. **Markdown body**：按 8 章节顺序的 `##` 标题（Overview / Colors / Typography / Layout / Elevation & Depth / Shapes / Components / Do's and Don'ts）。人类可读，提供"为什么"。

来源：[google-labs-code/design.md spec](https://github.com/google-labs-code/design.md/blob/main/docs/spec.md)。详见 [[concepts/design-md-format-spec]]。

### F2. awesome-design-md 把章节扩展到 11 节

VoltAgent/awesome-design-md 仓库（74 个真实站点 DESIGN.md 精选集）在 spec 的 8 必备之外**额外**加：

- `## Responsive Behavior`（从 Layout 拆出）
- `## Iteration Guide`（给 agent 的修改守则，如 *"Focus on ONE component at a time"*、*"Run `npx @google/design.md lint DESIGN.md` after edits"*）
- `## Known Gaps`（透明度声明，列出未能捕获的细节）

spec 允许未知章节保留，所以扩展不会被 lint 拒绝。这是 VoltAgent 团队对规范的最佳实践贡献。

### F3. 引用语法 `{path.to.token}` 让组件保持"换主题 = 改一处"

```yaml
colors:
  primary: "#1A1C1E"

components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.sm}"
```

改 `colors.primary` 会自动传播到所有 component。语法借鉴 [Design Tokens Community Group 2025.10 规范](https://www.designtokens.org/tr/2025.10/format/#abstract)，可以无损转换到 `tokens.json` / Figma variables / Tailwind theme。

来源：[google-labs-code/design.md README](https://github.com/google-labs-code/design.md) + [spec.md](https://github.com/google-labs-code/design.md/blob/main/docs/spec.md)。详见 [[concepts/design-md-token-interpolation]]。

### F4. Do's and Don'ts 章节是反 "AI taste" 的硬约束

DESIGN.md 第 8 必备章节 `Do's and Don'ts` 给出明确允许与禁止的设计决策。这是**避免 AI 生成 UI 漂向通用 gradient/glow/emoji 默认审美**的关键段——只靠 token 表，agent 仍会按训练数据均值漂移；加上 Do's and Don'ts 才有"决策依据"。

示例（来自 Notion DESIGN.md）：

```markdown
### Do
- Pair the navy hero with pastel-tinted feature cards
- Treat the purple pill button as the highest-priority CTA only

### Don't
- Don't use the purple pill for inline links (use link-blue instead)
- Don't apply the pastel tints to anything other than feature cards
```

详见 [[concepts/design-md-anti-patterns]]。

### F5. Google Labs 提供官方 CLI 工具

`@google/design.md` npm 包（v0.4.0）提供 lint 与 diff：

```bash
npx @google/design.md lint DESIGN.md   # 结构 + WCAG + 引用闭环
npx @google/design.md diff DESIGN.md DESIGN-v2.md   # 两份之间做 token-level + prose regression
```

输出 JSON，severity ∈ {error, warning, info}。仓库 [google-labs-code/design.md](https://github.com/google-labs-code/design.md) 26.5K stars、Apache-2.0。

详见 [[sources/google-design-md-spec]] + [[entities/google-labs-code-design]]。

### F6. 与 Claude Code 集成的完整链路

```text
┌────────────────────┐                                  ┌────────────────┐
│  getdesign.md      │  GET /<site>/design-md           │  DESIGN.md     │
│  (VoltAgent)       │ ──────────────────────────────→  │  项目根目录    │
│  或                │                                  └───────┬────────┘
│  awesome-design-md │                                          │ agent 读
│  仓库              │                                          ↓
└────────────────────┘                                  ┌────────────────┐
                                                        │  Claude Code   │
┌────────────────────┐  claude mcp add stitch --transport│  + Stitch MCP │
│  Google Stitch     │  http https://stitch.googleapis…  │                │
│  (MCP server)      │ ──────────────────────────────→  └────────────────┘
└────────────────────┘
```

详见 [[skills/claude-code-mcp-auth-patterns]]（Stitch MCP 鉴权）+ [[misc/web-medium-com-devsecops-ai-...-integration]]（端到端实操）。

### F7. "Inspired interpretation" 措辞是品牌保护

awesome-design-md 的每个 DESIGN.md 文件**不是**官方品牌产物，而是 VoltAgent 团队 reverse-engineer 的 "inspired interpretation"：

- README 末尾 *"We do not claim ownership of any site's visual identity"*
- 文件名 / description 自称 *"Inspired design analysis of [品牌]"*
- CONTRIBUTING.md *"We cannot accept DESIGN.md pull requests"*——质量由团队把控

这是 IP 风险规避姿态，**不是**法律背书——用 Stripe / Linear / Vercel 的 DESIGN.md 生成竞品 UI 的合法性目前**无明确判例**。

### F8. awesome-design-md 10 天 4 万星——但本质是营销驱动

WebSearch 报告该项目 2026-04 上线后 10 天内涨到 40K stars，最终 105K stars。背后驱动：

- 解决真实痛点（AI 生成 UI 不一致）
- 与 Stitch / Claude Code 工作流完美契合
- 商业化路径清晰（私人订制 + LaunchKit banner 广告）
- "Inspired interpretation" 措辞规避品牌法律风险

## Core Concepts

- [[concepts/design-md-format-spec]] — 文件 schema、8 必备章节、章节顺序
- [[concepts/design-md-token-interpolation]] — `{path.to.token}` 引用机制
- [[concepts/design-md-anti-patterns]] — Do's and Don'ts 与 "AI taste"
- [[concepts/design-system-as-ai-context]] — 上游：DESIGN.md 为何是 AI agent 的硬约束输入（与上一轮 ingest 的 [[misc/web-medium-com-devsecops-ai-...-integration]] 互链）
- [[concepts/ai-tool-specialization]] — 上下游：把视觉决策与代码执行分离到不同 agent

## Entities & Tools

- [[entities/google-stitch]] — DESIGN.md 的原始生产者（Google Labs 商业产品）
- [[entities/google-labs-code-design]] — 官方规范仓库与 CLI（Google Labs Code 组织）
- [[entities/awesome-design-md]] — VoltAgent 维护的 74 个真实样本
- [[entities/voltagent]] — 维护组织
- `@google/design.md`（npm v0.4.0，Apache-2.0）— 官方 CLI 工具 ^[inferred]
- `getdesign.md` — VoltAgent 运营的目录服务 ^[inferred]

## Contradictions & Open Questions

### C1. Stitch 官方 docs 是 JS-rendered SPA，机器读不到

https://stitch.withgoogle.com/docs/design-md/overview/ 与 /specification/ 返回 200 但 defuddle/WebFetch 拿不到正文（Angular SPA）。本研究的 Stitch 相关信息主要靠下游交叉验证（awesome-design-md README、google-labs-code/design.md spec、Sachin Sharma 的 [[misc/web-medium-com-devsecops-ai-...-integration]] 文章）。**这是客观限制，不是工具缺陷。** 详见 [[sources/stitch-design-md-docs]]。

### C2. "300+ DESIGN.md" vs "74 个" 的数字脱节

getdesign.md 首页自述 *"300+"*，但其仓库只含 74 个 DESIGN.md 文件（README badge `DESIGN.md count-73`，2026-07-28 取）。可能是营销数字与仓库数字的口径不同（历史版本、合并请求中的草稿等），或单纯夸饰。

### C3. `version: alpha` 仍在 alpha

截至 2026-07-28，DESIGN.md schema 与 `@google/design.md` CLI 都是 alpha。token 类型可能演进，章节顺序理论上可以变化——但当前主结构稳定。

### C4. Stitch 实际生成的 DESIGN.md 覆盖范围未公开

awesome-design-md 仓库的 74 个文件覆盖 11 章节（含 Iteration Guide + Known Gaps）；但**Stitch 自己生成的 DESIGN.md 是否也覆盖全部 8 必备章节**——目前没有 Stitch 端输出样本可对比。^[ambiguous]

### C5. IP / 商标风险

用 Stripe DESIGN.md 生成外观类似的金融产品 UI 是否侵权？目前无明确判例。awesome-design-md 的 "inspired interpretation" 措辞是规避姿态而非法律背书。^[ambiguous]

### C6. WebSearch 二手汇编的错误

研究 Round 1 时 WebSearch 报 `github.com/google/design.md`——该仓库实际**不存在**（404）。正确仓库是 `google-labs-code/design.md`。这是 hot.md 上次 wiki-research 警告的 *"二手汇编质量参差"* 的具体例子。**判断准则**：研究时不能依赖 WebSearch 报出的仓库名 / 版本号，必须直接 fetch 验证。

## Sources Consulted

- [[sources/awesome-design-md-repo]] — 主仓库 README + 4 个站点样本（Vercel / Notion / Claude / Stripe）
- [[sources/google-design-md-spec]] — 官方规范仓库 README + docs/spec.md
- [[sources/stitch-design-md-docs]] — Stitch 官方 docs 入口（JS-rendered，机器读不到正文）
- [[sources/getdesign-md-marketplace]] — VoltAgent 目录服务
- [[misc/web-medium-com-devsecops-ai-...-integration]] — 上轮 ingest 的 Stitch + Claude Code 端到端实操文章

## 在 vault 中的位置

本合成页是"Stitch + Claude Code 工作流"知识集群的**第二轮加深**：

- **上轮**（2026-07-28 INGEST_URL）：Sachin Sharma 的端到端实操 → [[misc/web-medium-com-devsecops-ai-...-integration]]
- **本轮**（2026-07-28 WIKI_RESEARCH）：DESIGN.md 格式 + 仓库 + 工具链的实证

未来如扩展，可触发：
- 合成页"DESIGN.md × MCP × Claude Code 完整链路"——把 [[concepts/design-system-as-ai-context]] / [[concepts/design-md-format-spec]] / [[skills/claude-code-mcp-auth-patterns]] 串成单页 SOP。
- 案例研究：实测用 [awesome-design-md 的 vercel/DESIGN.md] + Claude Code 生成 Vercel-lookalike 落地页，对比无 DESIGN.md 时的 token 消耗。