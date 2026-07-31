---
title: "n8n 2.0 release highlights"
category: sources
tags: [n8n, release-notes, ai-agents, mcp]
sources:
  - "https://blog.n8n.io"
  - "https://new.qq.com/rain/a/20251215A027VP00"
source_url: "https://blog.n8n.io"
created: "2026-07-30"
updated: "2026-07-30"
summary: "n8n 2.0 (2025-12) 关键新特性：原生 multi-agent 编排、内建 Data Tables（无需外部 DB）、MCP Client Trigger + MCP Server Tool 节点、智能项目管理。"
provenance:
  extracted: 0.60
  inferred: 0.30
  ambiguous: 0.10
base_confidence: 0.55
lifecycle: draft
lifecycle_changed: "2026-07-30"
---

# n8n 2.0 Release Highlights

> 来源：n8n blog 官方 changelog（"What's new in n8n 2.0"）+ 二手汇编（QQ/腾讯新闻 2025-12-15 报道）

## 版本时间线

- 2025-04：75K GitHub stars
- 2025-08：估值从 $350M → $2.3B（Accel 领投数亿欧元）
- 2025-12：**n8n 2.0 发布**，162K stars（与最新 198.7K 反映的是不同时间快照）

## 三大特性

### 1. Multi-agent 与 MCP 原生支持

- 内建 **multi-agent 编排**——多 agent 协同工作
- **MCP Client Trigger** + **MCP Server Tool** 节点——可直接连 MCP server/被 MCP 客户端调用
- AI 工具集更新：更易把多个模型串起来 + 接到数据/工具上

> 这是 [[concepts/ai-agent-node-pattern]] 从「可选 LangChain 集成」升级为「一等公民」的分水岭。

### 2. Data Tables（内建数据库表）

- 不再需要外部 DB 即可在工作流里存取结构化数据
- 工作流内可直接 query/update 表
- 极大降低「小工作流 + 小数据」场景的部署门槛

> 现实含义：以前「触发 → 写 SQLite → 读 SQLite → 通知」需要自建 DB；现在一个 n8n 实例闭环。

### 3. 其他改进

- 大规模项目 / workflow 管理更智能（项目化分组）
- 凭据 / 安全处理改进
- 节点属性 UI 重做（更易配置）

## 关键判断 ^[inferred]

- n8n 2.0 把定位从「开源 Zapier 替代」明确升级为「**AI workflow 平台**」——AI 节点、multi-agent、MCP 都是这条线
- Data Tables 是个有战略意义的决定：把"轻量 stateful"场景从外部 DB 拉回平台内，减少用户离开 n8n 的机会
- 估值 4 个月涨 6.5× + 2025 年 162K star 涨幅 2×——AI agent 风口的直接受益者

## 局限性

- 一手 release notes 未直接获取到全文（本会话走的是二手 + 综述），具体 minor features 可能漏列
- "MCP 原生支持"的具体协议版本兼容范围需实测验证（与 [[sources/czlonkowski-n8n-mcp]] 中提到的 MCP 协议版本冲突是潜在雷点）

## 相关

- [[entities/n8n]]
- [[concepts/ai-agent-node-pattern]]
- [[synthesis/Research: n8n]]