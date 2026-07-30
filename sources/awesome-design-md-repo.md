---
title: "VoltAgent/awesome-design-md — 74 个真实站点的 DESIGN.md 精选集"
category: references
tags: [design-system, ai-coding, stitch, awesome-list, voltagent, source]
sources:
  - "https://github.com/VoltAgent/awesome-design-md"
source_url: "https://github.com/VoltAgent/awesome-design-md"
created: "2026-07-28T01:00:00Z"
updated: "2026-07-28T01:00:00Z"
summary: "VoltAgent 团队维护的 DESIGN.md 精选集，含 74 个真实站点（Claude / Vercel / Notion / Linear / Stripe 等）的 design analysis，遵循 Google Labs 官方 DESIGN.md 规范。"
base_confidence: 0.75
lifecycle: draft
lifecycle_changed: "2026-07-28"
provenance:
  extracted: 0.90
  inferred: 0.05
  ambiguous: 0.05
---

# VoltAgent/awesome-design-md

> 74 个真实站点的 DESIGN.md "inspired interpretation"，遵循 [Google Stitch DESIGN.md 规范](https://github.com/google-labs-code/design.md)。

## 仓库概述

| 字段 | 值 |
|------|----|
| 仓库 | [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md) |
| 维护者 | [VoltAgent](https://github.com/VoltAgent/voltagent) 组织 |
| Stars / Forks | 105K / 12K（截至 2026-07-28）^[inferred] |
| 许可证 | MIT |
| 站点数 | 74（badge 标注 "DESIGN.md count-73"，2026-07-28 取自 README） |
| 目录布局 | `design-md/<site>/DESIGN.md` + `preview.html` + `preview-dark.html` |
| 收录范围 | AI/LLM 平台、开发工具、后端/数据库、SaaS、设计工具、Fintech、电商、媒体、汽车、Retro Web（1996 Dell / 2001 Nintendo.com） |

## 关键事实

- **遵循官方规范**：每个文件 `version: alpha` + 完整 YAML frontmatter（colors/typography/rounded/spacing/components）+ 8 个必备 prose 章节 + **扩展两节** `Iteration Guide` 与 `Known Gaps`。官方 spec 在 [[sources/google-design-md-spec]] 中给出 8 必备章节，awesome-design-md 在此基础上加 `Iteration Guide`（给 AI agent 的修改守则）与 `Known Gaps`（透明度声明）。
- **命名保护**：所有文件自称 `Inspired design analysis of [品牌]`，README 末尾明确声明 *"We do not claim ownership of any site's visual identity"*——避免品牌商标 / 版权争议。
- **目录服务配套**：每个 `DESIGN.md` 同时托管在 [getdesign.md](https://getdesign.md/)（同团队运营），提供 `/request` 私人订制入口（"We craft one for any website you want"）。
- **执行守则**：每个 `DESIGN.md` 都有一段 `Iteration Guide`，例如 Notion 版本给出 7 条规则（专注单组件、引用 token、`npx @google/design.md lint DESIGN.md`、新增变体作独立 components 条目、默认 `{typography.body-md}`、保持 `{colors.primary}` 唯一定位、`{rounded.md}` vs `{rounded.lg}` vs `{rounded.full}` 各司其职）。
- **透明声明**：每个文件还含 `Known Gaps` 段，列出 *未能* 准确捕获的细节（如 dark-mode token 值、动画时长、pastel-tint 映射的猜测性）。
- **占位符插值**：组件定义里 `{colors.primary}`、`{typography.body-md}`、`{rounded.lg}` 这种 `{path.to.token}` 引用是 AI agent 读取时的实时刻画——这一机制来自 [Design Tokens Community Group spec](https://www.designtokens.org/tr/2025.10/format/#abstract)。

## 使用流程

1. **选**：从 README Collection 列表挑一个站点的 DESIGN.md（按场景：开发者平台 → Vercel；金融 → Stripe；编辑型 → WIRED）。
2. **下载**：`npx degit VoltAgent/awesome-design-md/design-md/vercel` 或直接 curl。
3. **落到项目根**：把 `DESIGN.md` 复制到你的项目根目录。
4. **验证**：`npx @google/design.md lint DESIGN.md`（Google 官方工具，会做 WCAG 对比度、结构校验、token 引用闭环检查）。
5. **驱动 agent**：

   ```text
   Build a landing page in the style of my DESIGN.md.
   Use only the colors, typography, spacing, and components defined there.
   Open preview.html as a reference for how the design system reads visually.
   ```

6. **迭代时跑 lint**：每次改动后 `npx @google/design.md lint DESIGN.md`，避免引入与规范不符的字段。

## 限制

- **覆盖偏向英文科技品牌**：74 个里 ~70 是英文站点、~10 是 fintech/AI，国内产品基本缺位。
- **不是 Stitch 官方产出**：每个文件是 VoltAgent 团队 reverse-engineer 出来的 "inspired interpretation"，与官方品牌的实际 CSS / Figma token 不一定 100% 对齐——README 明确写 *"the extracted design tokens represent publicly visible CSS values"*。
- **个人商用合法性**：用 Stripe / Linear / Vercel 的 DESIGN.md 生成竞品 UI 是否侵犯商标或著作权？目前无明确判例；README 的 "inspired" 措辞是规避姿态，不是法律背书。
- **不是规格演进指针**：仓库固定在 `version: alpha`，不主动同步 `google-labs-code/design.md` 的 spec 演进（截至 2026-07-28 官方 spec 也在 alpha，未升级）。

## 相关页面

- [[sources/google-design-md-spec]] — 官方规范仓库
- [[sources/stitch-design-md-docs]] — Stitch 官方文档入口
- [[sources/getdesign-md-marketplace]] — 同团队目录服务
- [[concepts/design-md-format-spec]] — DESIGN.md 文件 schema 与规范
- [[concepts/design-md-token-interpolation]] — `{path.to.token}` 占位符机制
- [[concepts/design-system-as-ai-context]] — 上游概念：为什么 DESIGN.md 是 AI agent 的硬约束输入
- [[entities/awesome-design-md]] — 仓库本身实体页
- [[entities/voltagent]] — 维护组织