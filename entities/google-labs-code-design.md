---
title: "google-labs-code/design.md"
category: entities
tags: [github-repo, google-labs, design-system, open-spec, ai-coding, entity]
sources:
  - "https://github.com/google-labs-code/design.md"
  - "https://registry.npmjs.org/@google/design.md"
source_url: "https://github.com/google-labs-code/design.md"
created: "2026-07-28T01:00:00Z"
updated: "2026-07-28T01:00:00Z"
summary: "Google Labs 出品的 DESIGN.md 官方规范仓库与 npm CLI（@google/design.md, v0.4.0）。Apache-2.0 许可、26.5K stars，权威定义文件 schema 与 token 语法。"
tier: core
lifecycle: draft
lifecycle_changed: "2026-07-28"
base_confidence: 0.92
provenance:
  extracted: 0.95
  inferred: 0.03
  ambiguous: 0.02
relationships:
  - target: "[[entities/google-stitch]]"
    type: related_to
  - target: "[[entities/awesome-design-md]]"
    type: related_to
  - target: "[[concepts/design-md-format-spec]]"
    type: derived_from
---

# google-labs-code/design.md

> DESIGN.md 官方规范仓库与 CLI 工具——Google Labs 出的"参考实现"。

## 仓库信息

| 字段 | 值 |
|------|----|
| 仓库 | [google-labs-code/design.md](https://github.com/google-labs-code/design.md) |
| 组织 | Google Labs Code |
| Stars / Forks | 26.5K / 2.1K（截至 2026-07-28） |
| 许可证 | Apache-2.0 |
| 创建日期 | 2026-04-10 |
| 最新提交 | 2026-07-28 |
| 当前版本 | 文件 schema `version: alpha`；npm `@google/design.md` v0.4.0 |
| npm 主页 | https://www.npmjs.com/package/@google/design.md |

## 仓库产出

1. **DESIGN.md 格式规范**（[`docs/spec.md`](https://github.com/google-labs-code/design.md/blob/main/docs/spec.md)）：15K 字节完整规范。
2. **`@google/design.md` CLI 工具**：lint / diff 两个子命令。
3. **README + 简短示例**：演示一个最小 DESIGN.md 文件。
4. **`docs/spec.md` 自动生成**：`<!-- Generated from spec.mdx + spec-config.ts | version: alpha -->`——单源真相。

## 与 Stitch 的关系

仓库由 Google Labs Code 维护，而 [[entities/google-stitch]] 是 Google Labs 出品的 AI 设计工具。两者关系：

| 维度 | Stitch | google-labs-code/design.md |
|------|--------|----------------------------|
| 形态 | 商业产品（带 Web UI / MCP server） | 开源规范仓库 |
| 角色 | 用自然语言生成 UI，自动产出 DESIGN.md | 规范 DESIGN.md 文件 schema 与 token 语法 |
| 关系 | **是** DESIGN.md 的原始生产者 | **定义** DESIGN.md 的格式 |
| License | 服务条款 | Apache-2.0 |

简言之：Stitch 把 DESIGN.md 作为**输出产物**输出，google-labs-code/design.md 把 DESIGN.md 作为**输入规范**定义。两者配套使用——Stitch 生成的文件通过本仓库的 lint 工具验证。

## CLI 工具用法

```bash
# 安装
npm install @google/design.md

# 验证（结构 + WCAG + 引用闭环）
npx @google/design.md lint DESIGN.md

# diff 两份 DESIGN.md
npx @google/design.md diff DESIGN.md DESIGN-v2.md

# Windows 兼容（避免 .md 文件关联冲突）
npx -p @google/design.md designmd lint DESIGN.md
```

详见 google-design-md-spec。

## 在 vault 中的位置

本仓库是 [[concepts/design-md-format-spec]] 的**权威定义来源**——所有 8 必备章节、token 类型、引用语法、consumer 行为都从这里规定。也是 [[entities/awesome-design-md]] 仓库遵循的规范来源。两个仓库构成 "规范 + 样本" 的双层结构。

## 相关页面

- google-design-md-spec — 来源详情
- [[entities/google-stitch]] — DESIGN.md 的原始生产者
- [[entities/awesome-design-md]] — 最大样本集
- [[concepts/design-md-format-spec]] — 本仓库定义的规范
- [[concepts/design-md-token-interpolation]] — `{path.to.token}` 引用语法