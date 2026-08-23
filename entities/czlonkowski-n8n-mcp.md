---
title: "czlonkowski/n8n-mcp"
category: entities
tags: [mcp, n8n, ai-agents, claude, dev-tools]
sources:
  - "https://github.com/czlonkowski/n8n-mcp"
created: "2026-07-30"
updated: "2026-07-30"
summary: "czlonkowski 出品的 n8n-mcp：把 n8n API 暴露为 MCP server，让 Claude Desktop / Claude Code / Windsurf / Cursor 用自然语言构建/查询/修改 n8n workflow。"
provenance:
  extracted: 0.65
  inferred: 0.30
  ambiguous: 0.05
base_confidence: 0.55
lifecycle: draft
lifecycle_changed: "2026-07-30"
tier: peripheral
---

# czlonkowski/n8n-mcp

## 基本信息

| 项 | 值 |
|---|---|
| 仓库 | github.com/czlonkowski/n8n-mcp |
| 类型 | MCP server（stdio） |
| 安装 | `npx -y n8n-mcp@latest` |
| 作用 | 把 n8n API 包成 MCP 工具集 |

## 解决什么问题

n8n 是可视化拖拽工具，但**写复杂 workflow 仍要反复配置几十个节点**。czlonkowski/n8n-mcp 的解法：**让 AI agent 用自然语言搭**——你描述要什么，agent 调用 MCP 工具读写 n8n workflow JSON。

## 配置示例

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

支持的 client：Claude Desktop · Claude Code · Windsurf · Cursor。

## 同类项目

- `ifmelate/n8n-workflow-builder-mcp`——精简版，专注 workflow CRUD
- `salacoste/mcp-n8n-workflow-builder`——另一种 API 暴露方式

## 已知坑

- **Claude Desktop ↔ n8n MCP 易断连**——MCP 协议版本不兼容（`2024-11-05` vs `2025-03-26`）+ SSE transport 差异
- **解法**：`supergateway` 做协议代理转译

## 相关

- [[entities/n8n]]
- [[concepts/ai-agent-node-pattern]]
- czlonkowski-n8n-mcp
- [[synthesis/Research: n8n]]