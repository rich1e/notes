---
title: Figwright
category: entity
tags: [figma, mcp, codegen, design-tools, figwright, typescript]
sources:
  - https://github.com/awdr74100/figwright
created: 2026-08-14T08:00:00Z
updated: 2026-08-14T08:00:00Z
summary: 双向 Figma MCP server(awdr74100, MIT, Node+TypeScript+Vue 3 pnpm monorepo):provider-first codegen + 本地 WebSocket 中继 + 112 tool,免 Dev Mode 付费座位
base_confidence: 0.55
lifecycle: draft
lifecycle_changed: 2026-08-14
tier: supporting
provenance:
  extracted: 0.85
  inferred: 0.10
  ambiguous: 0.05
---

# Figwright

**Figwright** = `Where Playwright drives the browser, Figwright drives Figma.`

双向 Figma MCP server,让 AI agent(Claude Code/Cursor/Codex/任意 MCP client)直接读写 Figma 画布。

## 关键属性

| 维度 | 值 |
|---|---|
| 作者 | Roya(@awdr74100) |
| License | MIT |
| 主仓 | github.com/awdr74100/figwright |
| 发布包 | `@figwright/mcp`(npx 启动) |
| 运行时 | Node.js(engines 矛盾 ^[ambiguous]:README "20.19+/22.12+" vs `package.json` `>=24.0.0`) |
| 语言 | TypeScript(Vue 3 plugin UI)+ Node MCP server |
| 包管理 | pnpm 11(workspace + Corepack 锁) |
| 工具数 | 112(README:684) |

## 三大组件

1. **`@figwright/mcp`**(MCP server,stdio 启动)
   - `election/`: leader/follower 选举
   - `relay/`: WebSocket relay
   - `tokens/` + `join/` + `scan/`: 探测代码库 + 映射 Figma→code
   - `tools/`: 112 个 MCP tool 实现
2. **Figma plugin**(Vue 3 iframe + sandbox)
   - `src/handlers/`: Figma Plugin API 调用封装
   - `src/relay/`: WebSocket client
   - `ui/`: Vue 3 面板 UI
3. **`shared`** package: 跨仓协议(codec/envelope/heartbeat/rpc/protocol/serialized-node/queries)

## 核心差异点

- **vs Figma 官方 Dev Mode MCP**: 官方只读 + 付费门槛;Figwright 双向 + 零成本
- **vs Google Stitch**: Stitch 输出 DESIGN.md + 静态 HTML;Figwright 操作活的 Figma canvas
- **vs 截图转代码工具**: Figwright 用结构化 MCP 工具 + token 解析,不是 OCR

## 相关

- 项目页 [[projects/figwright/figwright]]
- 设计哲学 [[projects/figwright/concepts/provider-first-codegen]]
- 中继架构 [[projects/figwright/concepts/mcp-local-relay-architecture]]
- 安全设计 [[projects/figwright/concepts/loopback-security-host-origin-headers]]
- 工具分类 [[projects/figwright/references/figwright-tool-taxonomy]]
- 同类 [[entities/google-stitch]]