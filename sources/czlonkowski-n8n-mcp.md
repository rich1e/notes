---
title: "czlonkowski/n8n-mcp — 让 Claude 用自然语言搭工作流"
category: sources
tags: [mcp, n8n, ai-agents, claude, dev-tools]
sources:
  - "https://github.com/czlonkowski/n8n-mcp"
source_url: "https://github.com/czlonkowski/n8n-mcp"
created: "2026-07-30"
updated: "2026-07-30"
summary: "czlonkowski 出品的 n8n-mcp：把 n8n API 包成 MCP server，让 Claude Desktop / Claude Code / Windsurf / Cursor 用自然语言构建 n8n workflow，npx 一行配置。"
provenance:
  extracted: 0.65
  inferred: 0.30
  ambiguous: 0.05
base_confidence: 0.55
lifecycle: draft
lifecycle_changed: "2026-07-30"
---

# czlonkowski/n8n-mcp

> 来源：GitHub `czlonkowski/n8n-mcp`（一手） + 多篇 CSDN 教程（二手实操）

## 项目定位

一个 **MCP server**，让 AI 编程 agent（Claude Desktop / Claude Code / Windsurf / Cursor）通过 MCP 协议直接操作 n8n：用自然语言描述要做什么 → agent 调用 n8n API 创建 / 查询 / 修改 workflow。

## 一行配置

```json
{
  "mcpServers": {
    "n8n-mcp": {
      "command": "npx",
      "args": ["-y", "n8n-mcp@latest"],
      "env": {
        "N8N_API_URL": "https://your-n8n.example",
        "N8N_API_KEY": "..."
      }
    }
  }
}
```

## 同类项目对比

| 项目 | 用途 |
|---|---|
| `czlonkowski/n8n-mcp` | 一手权威，节点/模板/凭据工具集最完整 |
| `ifmelate/n8n-workflow-builder-mcp` | 精简版，更专注 workflow CRUD |
| `salacoste/mcp-n8n-workflow-builder` | AI 自然语言建工作流入口 |

## 已知坑：Claude Desktop ↔ n8n MCP 连不上

- **Cursor**：连接正常
- **Claude Desktop**：连接后立刻断开

根因：MCP 协议版本不兼容（`2024-11-05` vs `2025-03-26`）+ SSE transport 行为差异。解法：用 `supergateway` 做协议代理转译。

## 衍生命题：Claude + MCP 调试 n8n 工作流

新出现的用法模式——Claude 通过 webhook 拿到 n8n 失败执行数据 → 自然语言分析根因。是 [[concepts/ai-agent-node-pattern]] 的一个具体应用。

## 相关

- [[entities/n8n]]
- [[entities/czlonkowski-n8n-mcp]]
- [[concepts/ai-agent-node-pattern]]
- [[synthesis/Research: n8n]]