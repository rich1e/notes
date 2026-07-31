---
title: "AI Agent 节点模式"
category: concepts
tags: [ai-agents, llm, langchain, mcp, n8n, workflow]
sources:
  - "https://docs.n8n.io/ai-agents/"
  - "https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/langchain"
  - "https://blog.n8n.io"
created: "2026-07-30"
updated: "2026-07-30"
summary: "把 LLM 调用 + 工具调用 + 记忆 + RAG 检索 + 多 agent 编排作为工作流一等公民节点的模式。n8n 2.0 原生 multi-agent + MCP client/server 是该模式主流实现。"
provenance:
  extracted: 0.70
  inferred: 0.25
  ambiguous: 0.05
base_confidence: 0.70
lifecycle: draft
lifecycle_changed: "2026-07-30"
tier: supporting
---

# AI Agent 节点模式

## 概念

在**工作流自动化平台**（[[concepts/workflow-automation-platform]]）里，把「LLM 调用 + 工具调用 + 记忆 + 检索 + 多 agent 编排」作为可视化一等节点暴露出来，让用户画 canvas 即可拼出 agent 应用——而不是写代码调 LangChain。

## n8n 里的 5 类核心 agent 节点

| 节点 | 行为 |
|---|---|
| **AI Agent (Tools Agent)** | 调用工具取上下文，再让 LLM 推理 |
| **Conversational Agent** | 跨轮维持 chat memory |
| **ReAct Agent** | 显式 reasoning + acting 步骤 |
| **SQL Agent** | 用自然语言查数据库 |
| **MCP Client Trigger / MCP Server Tool**（n8n 2.0） | 把 MCP server 当工具接入；或把本工作流暴露为 MCP server |

## 标准 RAG 流水线（在 n8n 上的画法）

```
Trigger (Chat/Schedule/Webhook)
    │
    ▼
Document ingestion (PDF / Web / Notion)
    │
    ▼
Embeddings node (OpenAI / HF / 本地)
    │
    ▼
Vector Store (PGVector / Pinecone / Qdrant / Supabase / Chroma / Milvus / Weaviate / Zep / In-Memory)
    │
    ▼
Retrieval: Query → Embed → Top-k → 与 Prompt 拼接
    │
    ▼
LLM 生成（带 source 引用）
    │
    ▼
Chat memory 节点（保留对话状态）
```

## 与「裸 LangChain」的差异 ^[inferred]

- **可视化**：trace、retrieval 结果、工具调用都画在 canvas 上，可解释性强
- **集成现成**：节点即工具（Slack、Notion、Airtable、Google Sheets、Gmail 等），不必为每个 SaaS 写工具封装
- **短板**：复杂链路由、自定义 retriever 受限；需要时仍要 wrap Python / 调外部 LangChain API

## n8n 2.0 的关键升级

- multi-agent 编排从「可选」升为「一等公民」
- MCP client/server 一等节点（参 [[sources/n8n-2-0-release]]）
- Data Tables 把「轻量 stateful」场景内化（无需外部 DB）

## 设计取舍

- **可视化优先**：易调试、易审计，但牺牲一些表达力
- **LLM 多供应商切换**：「架构层不绑定」，换模型不必重画 workflow
- **human-in-the-loop**：approval / rule-based gating 内建，适合 AI governance 场景

## 相关

- [[entities/n8n]]
- [[concepts/workflow-automation-platform]]
- [[sources/n8n-2-0-release]]
- [[sources/czlonkowski-n8n-mcp]]（反向应用：让 Claude 帮你搭 n8n workflow）
- [[synthesis/Research: n8n]]