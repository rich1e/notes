---
title: "Research: n8n"
category: synthesis
tags: [workflow-automation, n8n, ai-agents, mcp, langchain, research]
sources:
  - "https://github.com/n8n-io/n8n"
  - "https://n8n.io/"
  - "https://docs.n8n.io/hosting/scaling/queue-mode/"
  - "https://github.com/n8n-io/n8n-hosting"
  - "https://blog.n8n.io"
  - "https://github.com/czlonkowski/n8n-mcp"
created: "2026-07-30"
updated: "2026-07-30"
summary: "n8n 三轮调研综合：开源 + AI 优先的工作流自动化平台，2.0 升 multi-agent + MCP + Data Tables，自托管有 Queue Mode 成熟方案；fair-code 许可限制商用转售。"
provenance:
  extracted: 0.70
  inferred: 0.20
  ambiguous: 0.10
base_confidence: 0.74
lifecycle: draft
lifecycle_changed: "2026-07-30"
tier: core
---

# Research: n8n

## Overview

n8n 是一款以「**fair-code 开源 + 自托管 + AI 原生**」为核心定位的工作流自动化平台。三轮调研覆盖：①产品定位与生态（n8n.io / GitHub / 主流对比），②生产架构（Queue Mode 三角色 + Redis + Postgres），③AI agent 与 MCP 集成（n8n 2.0）。n8n 在 2025 年中估值 4 个月涨 6.5× 至 $2.3B，反映 AI agent 浪潮把工作流自动化从「SaaS 替代」重定义为「**AI agent 编排底座**」。

## Key Findings

- **三主流差异化清晰**——Zapier 集成最多最易用但纯云；Make 视觉最强但纯云；n8n 是唯一同时支持自托管、代码注入、AI 优先的开源选项 [[sources/n8n-github-repo]] [[sources/n8n-official-home]]
- **License 是关键决策点**——Sustainable Use License 不是 OSI 开源，可自托管、可改、可用于内部 / 咨询 / 工作流解决方案，但**禁止做同质化竞品**转售 [[concepts/fair-code-license]]
- **生产架构成熟**——Queue Mode 把 main + webhook + worker 解耦，Redis (BullMQ) 任务队列 + Postgres 元数据，官方 docker-compose 与 Helm chart 可用；常见 6 类可靠性陷阱都有明确解法 [[sources/n8n-queue-mode]]
- **n8n 2.0 是「AI agent 平台化」分水岭**——multi-agent 编排 + MCP client/server 一等节点 + Data Tables，把 LangChain / MCP / 轻量 stateful 全包进 canvas [[sources/n8n-2-0-release]]
- **AI agent 节点模式**是把 LLM + 工具 + 记忆 + RAG + 编排作为可视化节点，trace 与审计天然友好；n8n 是该模式的主流商业实现 [[concepts/ai-agent-node-pattern]]
- **反身性生态**：czlonkowski/n8n-mcp 让 Claude 用自然语言搭 n8n workflow——n8n 不仅让用户搭 agent 工作流，自身工作流也可由 agent 来搭 [[entities/czlonkowski-n8n-mcp]]
- **数据点**：198.7K stars · 500+ 商业集成 / 1500+ 全社区节点 · 9000+ workflow 模板 · 4.7/5 G2 · SOC 2 + GDPR · Microsoft/NVIDIA/Meta 客户 [[entities/n8n]]
- **生态风险**：MCP 协议版本分裂（`2024-11-05` vs `2025-03-26`）导致 Claude Desktop ↔ n8n MCP 不稳，需要 supergateway 代理——MCP 标准化未完成是潜在阻力 [[sources/czlonkowski-n8n-mcp]]

## Core Concepts

- [[concepts/workflow-automation-platform]] — 工作流自动化平台：节点 + 连线 + DAG 的低代码抽象，主流三家对比
- [[concepts/fair-code-license]] — 受限源码可用许可：可自托管可改可商用，但禁同质竞品
- [[concepts/ai-agent-node-pattern]] — 把 LLM/工具/记忆/RAG/MCP 作为可视化节点

## Entities & Tools

- [[entities/n8n]] — 主体：n8n-io 开源项目，TypeScript 编写，fair-code 双许可
- [[entities/czlonkowski-n8n-mcp]] — 反身性 MCP 工具：让 Claude 用自然语言搭 n8n workflow

## Contradictions & Open Questions

- **C1 集成数**：n8n.io 主页口径「500+」，GitHub README 口径「1500+」。最可能解释：500+ 是「主流商业 SaaS」，1500+ 含社区自定义节点。采纳 1500+ 作 README 主线数据点（GitHub 仓库更权威）
- **C2 License 详细条款**：本研究多次尝试 fetch `docs.n8n.io/reference/license/` 返回 404。完整条款需查 [LICENSE.md in repo](https://github.com/n8n-io/n8n/blob/master/LICENSE.md)，本综合页只能基于 README + 创始人 blog 描述。结论「不能做同质竞品 SaaS」为社区共识而非逐条法务解析
- **C3 MCP 协议成熟度**：MCP 协议版本分裂（`2024-11-05` vs `2025-03-26`）在 Claude Desktop ↔ n8n MCP 路径上暴露问题。需要 supergateway 代理——意味着「MCP 一等节点」的实际落地仍有协议兼容性门槛
- **Q1 自托管 vs Cloud 的运维成本**：n8n 自托管需要 Queue Mode（Redis + Postgres + main/webhook/worker 三角色）+ 监控。$0 平台费 vs 数百美元/月云费 vs 运维工时，需个案测算
- **Q2 n8n 在「AI agent 工作流」与「裸 LangChain / LlamaIndex」的边界**：可视化与表达力取舍；何时该 wrap Python 调外部 LangChain，何时画 canvas，本研究未做定量比较

## Sources Consulted

### 一手

- [[sources/n8n-github-repo]] — GitHub 仓库 README（198.7K stars / 1500+ 集成 / 双许可声明）
- [[sources/n8n-official-home]] — n8n.io 官方主页（产品定位 / 商业客户 / 合规）
- [[sources/n8n-queue-mode]] — docs.n8n.io Queue Mode 文档 + n8n-hosting docker-compose（生产架构）
- [[sources/czlonkowski-n8n-mcp]] — czlonkowski/n8n-mcp GitHub 仓库（反身性 MCP 工具）
- [[sources/n8n-2-0-release]] — n8n blog 2.0 release highlights + 二手汇编

### 二手

- [Zapier vs Make vs n8n 2025 Comparison — c-sharpcorner.com](https://www.c-sharpcorner.com/article/zapier-vs-make-vs-n8n-the-ultimate-comparison-for-workflow-automation-in-2025/#comments)
- [n8n AI Agents with LangChain & RAG Vector Stores](https://docs.n8n.io/ai-agents)
- [n8n blog 官方](https://blog.n8n.io)
- [n8n 估值 $350M → $2.3B（腾讯新闻 2025-08）](https://new.qq.com/rain/a/20250808A03TXP00)
- [n8n 2.0 发布（腾讯新闻 2025-12-15）](https://new.qq.com/rain/a/20251215A027VP00)

### 未直接获取（404 或无实质内容）

- `docs.n8n.io/reference/license/` —— 返回 404，完整 license 文本需查 GitHub LICENSE.md
- `docs.n8n.io/sitemap.xml` —— 仅是 sitemap 索引，无 license 实质内容