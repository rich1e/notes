---
title: MCP local-relay 架构
category: concept
tags: [mcp, websocket, figma, leader-election, figwright, relay]
sources:
  - https://github.com/awdr74100/figwright
created: 2026-08-14T08:00:00Z
updated: 2026-08-14T08:00:00Z
summary: Figwright 的 stdio+WebSocket 中继架构:MCP client ↔ @figwright/mcp (stdio) ↔ 127.0.0.1:3055 WebSocket ↔ Figma plugin;多 client 通过 leader/follower 选举共享一个 plugin 连接
base_confidence: 0.55
lifecycle: draft
lifecycle_changed: 2026-08-14
tier: supporting
provenance:
  extracted: 0.85
  inferred: 0.10
  ambiguous: 0.05
---

# MCP local-relay 架构

Figwright 的本地中继架构——让多个 MCP client 共享一个 Figma plugin 连接,所有流量 loopback。

## 三层拓扑

```
┌─────────────────────────────────────────────────────────────────────┐
│ MCP CLIENTS  —  one per agent                                       │
│ Claude Code · Cursor · Claude · any MCP-capable client              │
└─────────────────────────────────────────────────────────────────────┘
                                  │  MCP protocol over stdio
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│ @figwright/mcp  —  your client launches one; they elect a leader    │
│                                                                     │
│ LEADER   (owns the single plugin connection)                        │
│    • WebSocket relay · request idempotency                          │
│    • routes to the most-recently-active file                        │
│    • session resume · "busy ≠ dead" heartbeat                       │
│    • endpoints:  /ws (plugin) · /ping (health) · /rpc (followers)   │
│                                                                     │
│ FOLLOWERS                                                           │
│    • forward tool calls to the leader over HTTP /rpc                │
│    • take over automatically if the leader exits                    │
└─────────────────────────────────────────────────────────────────────┘
                                  │  local WebSocket · msgpack (binary)
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│ FIGMA  (desktop or browser)                                         │
│                                                                     │
│ ┌─────────────────────────────────────────────────────────────────┐ │
│ │ Figwright plugin                                                │ │
│ │   • UI (Vue 3 iframe): WebSocket client + heartbeat             │ │
│ │   • sandbox: executes Figma Plugin API calls                    │ │
│ └─────────────────────────────────────────────────────────────────┘ │
│              │ Figma Plugin API                                     │
│              ▼                                                      │
│            Canvas                                                   │
└─────────────────────────────────────────────────────────────────────┘
```

## Leader/Follower 选举

**触发**:多个 MCP client 同时连同一个 `@figwright/mcp` 进程时。

**Leader 拥有**:
- 与 Figma plugin 的唯一 WebSocket 连接
- 接收所有 client 的 tool call 请求并路由
- 维护 session(`heartbeat.ts` + `session.ts`)+ idempotency(`idempotency.ts`)

**Follower**:
- 仅持有到 leader 的 HTTP `/rpc` 通道
- 不直接连 Figma
- 转发 tool call + 接收响应
- **自动接管**:leader 退出时,follower 升级为新 leader

**选举依据**:README 提到 "routes to the most-recently-active file"——可能基于最近活动时间戳或 lease(`packages/mcp/src/election/election.ts`)^[inferred]

## Session 韧性

- **heartbeat**: leader ↔ plugin 持续心跳,plugin 短暂繁忙 ≠ 死亡
- **session resume**: 长任务中断后续上而非重新跑
- **idempotency**:相同 request ID 不重复执行(Figma Plugin API 副作用操作关键)
- **request idempotency** 在 `packages/plugin/src/idempotency.ts` + `packages/mcp/src/.../idempotency.ts` 两边各有一份

## 与 vault 已有知识对应

| vault 已有 | 本架构对应 |
|---|---|
| [[concepts/mcp-server-protocol-quirks]] MCP 鉴权 | stdio 启动无鉴权问题(本地进程) |
| [[concepts/cdp-cookie-extraction]] CDP 作为浏览器↔外部 桥 | WebSocket relay 是同类(本地桥) |
| [[concepts/mcp-multi-tool-installer]] `nlm setup add` | `npx -y @figwright/mcp@latest` 同模式(无全局安装) |
| [[entities/gemini-notebook-mcp-cli]] 多 profile auth | 多 client 共存(leader/follower)解决同类问题 |

## 关键技术细节

- **transport**:WebSocket 二进制 + msgpack(`packages/shared/src/codec.ts`)
- **envelope**:RPC 包装(`packages/shared/src/envelope.ts`)
- **protocol**:消息类型定义(`packages/shared/src/protocol.ts`)
- **heartbeat**:心跳协议(`packages/shared/src/heartbeat.ts`)
- **serialized-node**:Figma node 序列化(`packages/shared/src/serialized-node.ts`)

## Open Questions

- 选举算法具体实现(lease?heartbeat?file-mtime?)^[inferred]
- leader/follower 切换延迟(<1s?5s?)
- 跨进程锁机制(node IPC?文件?Redis?)
- plugin 重启后 session resume 的容错粒度

## 相关

- [[projects/figwright/figwright]] 项目主页
- 安全设计 [[projects/figwright/concepts/loopback-security-host-origin-headers]]
- 协议速查 [[projects/figwright/references/figwright-shared-protocol]]