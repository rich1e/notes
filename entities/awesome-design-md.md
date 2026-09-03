---
title: "VoltAgent/awesome-design-md"
category: entities
tags: [github-repo, ux, voltagent, ai-coding, entity]
sources:
  - "https://github.com/VoltAgent/awesome-design-md"
source_url: "https://github.com/VoltAgent/awesome-design-md"
created: "2026-07-28T01:00:00Z"
updated: "2026-07-28T01:00:00Z"
summary: "VoltAgent 团队的 awesome-design-md 仓库，74 个真实站点 DESIGN.md 精选集（Claude / Vercel / Notion / Stripe / Linear 等），是 Stitch DESIGN.md 规范的最大下游样本集。"
tier: core
lifecycle: draft
lifecycle_changed: "2026-07-28"
base_confidence: 0.78
provenance:
  extracted: 0.92
  inferred: 0.05
  ambiguous: 0.03
    type: derived_from
relationships:
  - target: "[[entities/voltagent]]"
    type: related_to
  - target: "[[entities/google-stitch]]"
    type: related_to
  - target: "[[entities/google-labs-code-design]]"
    type: related_to

---

# VoltAgent/awesome-design-md

> 74 个真实站点的 DESIGN.md "inspired interpretation"。

## 仓库信息

| 字段 | 值 |
|------|----|
| 仓库 | [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md) |
| Stars / Forks | 105K / 12K（截至 2026-07-28）^[inferred] |
| 许可证 | MIT |
| 站点数 | 74 |
| 收录站点类型 | AI / 开发工具 / 后端 / SaaS / 设计工具 / Fintech / 电商 / 媒体 / 汽车 / Retro Web |
| 配套服务 | [getdesign.md](https://getdesign.md/) 目录站点 + `/request` 私人订制 |
| 配套官方规范 | [[entities/google-labs-code-design]] |
| 维护组织 | [[entities/voltagent]] |

## 关键事实

- 仓库**严格遵循** entities/google-labs-code-design.md|google-labs-code/design(https://github.com/google-labs-code/design.md) 规范（`version: alpha` + 完整 YAML + 8 必备章节）。
- **扩展** spec：每个文件额外加 `Iteration Guide`（修改守则）与 `Known Gaps`（透明度声明）——spec 允许未知章节保留，所以扩展不会被 lint 拒绝。
- **品牌保护**：所有 DESIGN.md 自称 `Inspired design analysis of [品牌]` 而非 "the official DESIGN.md"；README 末尾 *"We do not claim ownership of any site's visual identity"*。
- **不收 PR**：CONTRIBUTING.md 明确 *"We cannot accept DESIGN.md pull requests"*——内容由团队 reverse-engineer 产出，保持质量一致。
- **目录服务**：[getdesign.md](https://getdesign.md/) 把同一批文件以 URL 形式对外暴露（`/<site>/design-md`）；同时提供 `/request` 私人订制入口。

## 在 vault 中的位置

仓库是 [[concepts/design-md-format-spec]] 的最大样本来源——所有 8 必备章节的实操样例（colors hierarchy、typography scale、component variants、Do's and Don'ts）都从这里来。它也是 [[concepts/design-system-as-ai-context]] 的**现实验证**——把 DESIGN.md 从 Google Labs 的抽象概念变成 74 个可直接 copy-paste 用的具体文件。

## 相关页面

- awesome-design-md-repo — 来源详情
- getdesign-md-marketplace — 配套目录服务
- [[entities/voltagent]] — 维护组织
- [[entities/google-labs-code-design]] — 官方规范仓库
- [[entities/google-stitch]] — DESIGN.md 的原始生产者
- [[concepts/design-md-format-spec]] — 仓库遵循的规范
- [[synthesis/concepts-design-md-format-spec × entities-awesome-design-md|DESIGN.md 格式规范 × awesome-design-md]] — synthesis(规范 vs 最大下游样本集的校准回路)
