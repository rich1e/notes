---
title: AsciiDoc 标记语言
category: concepts
tags: [documentation, markdown]
summary: 比 Markdown 更结构化的文本标记语言，= 标题层级、表/脚注/交叉引用开箱即用、include 拆分、属性 + 条件内容支持多版本输出；适合大型技术文档与 docs-as-code。
sources:
  - https://www.git-tower.com/blog/asciidoc-quick-guide/
created: 2026-07-07
updated: 2026-07-07
tier: peripheral
lifecycle: draft
lifecycle_changed: "2026-07-07"
base_confidence: 0.45
provenance:
  extracted: 0.90
  inferred: 0.08
  ambiguous: 0.02
---

# AsciiDoc 标记语言

## 定位

AsciiDoc 是面向**大型/复杂技术文档**设计的纯文本标记语言。Markdown 因简单（`#` 标题、`-` 列表、`**` 加粗）而流行，但当文档需要表格、脚注、交叉引用、条件内容、模块化组合时，Markdown 需依赖各平台扩展（GFM、kramdown、CommonMark 各家方言不一），兼容性差。

AsciiDoc 的理念：**统一标准 + 内置高级特性**，不依赖第三方方言。Git 友好（纯文本、表格每行独立 → diff 干净）。

## Markdown vs AsciiDoc

| 维度 | Markdown | AsciiDoc |
|------|----------|----------|
| 入门成本 | 几分钟 | 略高，但基本语法类似 |
| 标题 | `#` 数量 | `=` 数量，文档头可放元数据 |
| 表格 | 依赖方言/扩展 | `\|===\|...\|===\|` 内置 |
| 脚注 | 依赖方言 | 内置 |
| 交叉引用 | 依赖方言 | `<<anchor>>` 内置 |
| 文档组合 | 依赖外部工具 | `include::file.adoc[]` 内置 |
| 条件内容 | 不可 | `ifdef::attr[]...endif::[]` 内置 |
| 属性/变量 | 不可 | `:var-name:` 复用 |
| 方言数量 | 多个，互相不兼容 | 单一标准规范 |

## 核心特性

### 文档头（无需 YAML/TOML）

```asciidoc
= User Guide for adoc Studio
Author: Marvin Blome
Date: 2025-01-21
```

标题、作者、日期直接写在文档顶部。

### 标题层级

```asciidoc
= 一级（文档级）
== 二级
=== 三级
```

### 文本格式

```asciidoc
*Bold Text*
_Italicized Text_
`Monospaced Text`
```

与 Markdown 几乎一致，迁移成本低。

### 表格

```asciidoc
|===
| Task | Status | Due Date
| Write draft | In Progress | Jan 20, 2025
| Review draft | Pending | Jan 22, 2025
|===
```

**关键优势**：每行独立 → Git diff 清晰；有序列表自动重编号。

### 属性（变量）

```asciidoc
:app-name: adoc Studio
:version: 1.2.3
```

在文档任意处 `{app-name}` 引用，**改一处全文档生效**——适合版本号、URL、版权年份。

### 文档组合（include 指令）

```asciidoc
include::introduction.adoc[]
include::features.adoc[]
```

适合分章节/多人协作，按需拼装。

### 条件内容

```asciidoc
ifdef::beginner[]
== Welcome, New Users!
endif::[]

ifdef::advanced[]
== Advanced Tips and Tricks
endif::[]
```

通过属性切换，单一源文件输出多个版本（初学者指南/高级指南、企业版/社区版）。

## 工具链

- **AsciiDoc 源文件** (.adoc)
- **导出**：`asciidoctor -b html5 myfile.adoc`（命令行）→ HTML/PDF/EPUB
- **GUI 工具**：adoc Studio（Mac/iPad/iPhone，三平台，14 天试用 + 订阅）—— 把属性、格式、样式表打包为"产品"，避免每个格式维护不同脚本
- **样式**：HTML 与 PDF 共享同一 CSS
- **Git 协作**：纯文本天然版本化；与 Tower 等 Git 客户端配合

## Docs-as-Code 优势

把 `.adoc` 文件纳入 Git 仓库：

1. 每个 PR 显示文档 diff（与代码一致）
2. 分支开发未来版本
3. 回滚/历史追踪

## 适用场景

- 大型技术文档（用户指南、API 文档、运维手册）
- 同源多版本（初学者/高级、社区/企业）
- 需要表格/脚注/交叉引用的复杂结构
- 团队规模 ≥ 3 人协作

## 不适用

- 极简 README、博客短文——Markdown 更轻
- 仅作快速记录——AsciiDoc 学习成本无收益

## 参考资源

- [Tower Blog: AsciiDoc Quick Guide](https://www.git-tower.com/blog/asciidoc-quick-guide/)（本文主要来源）
- adoc Studio 完整指南：<https://www.adoc-studio.app/blog/asciidoc-guide>
## 相关页面

- references/chezmoi-templating-guide
- concepts/fabric-patterns
