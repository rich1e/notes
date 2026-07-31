---
title: "n8n GitHub 仓库"
category: sources
tags: [workflow-automation, open-source, ai-agents, n8n]
sources:
  - "https://github.com/n8n-io/n8n"
source_url: "https://github.com/n8n-io/n8n"
created: "2026-07-30"
updated: "2026-07-30"
summary: "n8n-io/n8n 官方仓库：198.7k stars，TypeScript/Node.js 编写，双许可（Sustainable Use License + Enterprise），1500+ 集成，MCP client/server、LangChain 集成。"
provenance:
  extracted: 0.70
  inferred: 0.15
  ambiguous: 0.15
base_confidence: 0.83
lifecycle: draft
tier: supporting
lifecycle_changed: "2026-07-30"
---

# n8n GitHub 仓库

> 一手来源：[github.com/n8n-io/n8n](https://github.com/n8n-io/n8n)

## 仓库画像

| 项 | 值 |
|---|---|
| Star | 198.7k ^[extracted]（同一时段不同搜索结果在 162K~198.7K 之间漂移，反映不同时间快照） |
| Fork | 59.8k |
| 主语言 | TypeScript（Node.js 运行时） |
| 架构 | pnpm workspaces + Turbo monorepo（`/packages`、`/docker`、`/docs`、`/scripts`） |
| 测试 / Lint | Vitest / Biome |
| 提交数 | 22,471（master 分支） |

## 许可证（关键！）

**双许可**：

- **Sustainable Use License**（默认，用于 source-available 项目）
- **n8n Enterprise License**（用于追加企业特性）

这不是 OSI 开源定义（OSD）意义上的开源——本质上是「source-available + 受限商用」。详见 [[concepts/fair-code-license]]。

## 关键产品指标（仓库 README 声明）

- **1500+ 集成** ^[extracted]（n8n.io 主页营销页口径 500+，存在表述差异；以仓库 README 为准）
- **9000+ 工作流模板**
- **MCP client + server 内建支持**
- **LangChain 集成**
- 多模型支持：OpenAI / Anthropic / Google / 开源模型
- 自定义节点 + npm 包扩展机制

## 局限性

- README 是营销+技术混合描述，单一来源不可全信；具体技术细节（如 queue mode 内部机制、execution 模型）需查官方文档与源码
- "1500+ 集成"含社区自定义节点，不等于官方维护节点数
- Star 数在不同二手汇编里差异较大（75K / 162K / 198.5K / 198.7K），以仓库实时数据为准

## 相关

- [[entities/n8n]] — 主体对象
- [[concepts/fair-code-license]] — 解读其许可证
- [[synthesis/Research: n8n]] — 综合页