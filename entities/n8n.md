---
title: "n8n"
category: entities
tags: [workflow-automation, open-source, ai-agents, mcp, langchain]
sources:
  - "https://github.com/n8n-io/n8n"
  - "https://n8n.io/"
created: "2026-07-30"
updated: "2026-07-30"
summary: "n8n-io/n8n：开源工作流自动化平台，TypeScript/Node.js，fair-code 许可（[[concepts/fair-code-license]]），1500+ 集成，2.0 起原生 multi-agent + MCP + Data Tables。"
provenance:
  extracted: 0.80
  inferred: 0.15
  ambiguous: 0.05
base_confidence: 0.83
lifecycle: draft
lifecycle_changed: "2026-07-30"
tier: core
---

# n8n

## 基本信息

| 项 | 值 |
|---|---|
| 全名 | n8n (pronounced "nodemation") |
| 创始人 | Jan Oberhauser |
| 仓库 | github.com/n8n-io/n8n |
| 仓库统计 | 198.7k stars · 59.8k forks · TypeScript |
| License | **Sustainable Use License**（fair-code）+ Enterprise License |
| 总部 | 德国柏林 |
| 估值（2025-08） | $2.3B（4 个月前 $350M） |
| 投资方 | Accel 领投，Insight Partners 等 |

## 产品形态

- **自托管**（npm/Docker）—— 完全免费、完全数据主权
- **n8n Cloud**（app.n8n.cloud）—— 托管版，$20/mo 起
- **Enterprise**——加 SSO、审计、RBAC、SOC 2

## 关键能力

- 500+ 主流商业集成（n8n.io 口径）/ 1500+ 全社区节点（GitHub README 口径）^[extracted]
- 9000+ workflow 模板
- JS / Python 代码节点任意注入
- 自定义节点 + npm 包扩展
- AI agent（LangChain 集成） + RAG（PGVector/Pinecone/Qdrant/Chroma/Milvus/Weaviate/Zep 等）
- 2.0 起：multi-agent 编排 + MCP client/server 节点 + Data Tables

## 企业客户

Microsoft · NVIDIA · Meta · Deutsche Telekom · Vodafone · Mercedes-Benz · Dell · Novo Nordisk · Cummins · Amadeus · Fender

## 合规

SOC 2 · GDPR

## 与同类对比

n8n 在 [[concepts/workflow-automation-platform]] 中是「自托管 + 代码注入 + AI 优先」定位的代表：

- vs Zapier：n8n 自托管 + 代码 + 数据主权；Zapier 集成最多但纯云
- vs Make：n8n 自托管 + 开源；Make 视觉化最强但仅云
- vs LangChain（裸库）：n8n 可视化 + 集成现成；LangChain 表达力最强但需自己拼

## 相关

- [[concepts/workflow-automation-platform]] · [[concepts/fair-code-license]] · [[concepts/ai-agent-node-pattern]]
- n8n-github-repo · n8n-official-home · n8n-queue-mode · n8n-2-0-release
- [[entities/czlonkowski-n8n-mcp]]
- [[synthesis/Research: n8n]]