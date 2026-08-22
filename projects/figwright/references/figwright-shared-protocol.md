---
title: Figwright shared 协议层
category: reference
tags: [figma, mcp, protocol, shared-package, figwright, msgpack, websocket]
sources:
  - https://github.com/awdr74100/figwright
created: 2026-08-14T08:00:00Z
updated: 2026-08-14T08:00:00Z
summary: @figwright/shared package 7 个核心协议文件职责速查:codec/envelope/heartbeat/rpc/protocol/serialized-node + queries/components/styles/variables/writes/tool-budgets/version
base_confidence: 0.55
lifecycle: draft
lifecycle_changed: 2026-08-14
tier: supporting
provenance:
  extracted: 0.80
  inferred: 0.15
  ambiguous: 0.05
---

# Figwright shared 协议层

`packages/shared/src/` 是 `@figwright/mcp` 和 Figma plugin 共享的协议层。所有 transport、消息包装、心跳、RPC 调用、节点序列化都从这里出。

## 核心 7 文件

| 文件 | 职责 |
|---|---|
| `codec.ts` | msgpack 二进制编码/解码(WebSocket 传输层) |
| `envelope.ts` | RPC envelope 包装(request ID + type + payload) |
| `heartbeat.ts` | 心跳协议(leader↔plugin 持续 ping/pong) |
| `rpc.ts` | 远程过程调用抽象(leader ↔ follower / leader ↔ plugin) |
| `protocol.ts` | 消息类型定义(message kinds、payload schema) |
| `serialized-node.ts` | Figma node 序列化格式(API 树 → JSON-friendly) |
| `queries.ts` | 高层查询原语(`get_design_context`/`component_map`/`token_map` 等的共享部分) |

## 扩展文件

| 文件 | 职责 |
|---|---|
| `components.ts` | 组件序列化/反序列化(component_properties + main_component) |
| `styles.ts` | paint/effect/text style 序列化 |
| `variables.ts` | Figma variable + collection 序列化 |
| `writes.ts` | Write 操作的 schema(创建/编辑) |
| `design-context.ts` | `get_design_context` 输出结构 |
| `design-context-dedupe.ts` | design context 的 dedupe 算法(去掉重复 token/style/component) |
| `tool-budgets.ts` | 工具调用预算/限制 |
| `version.ts` | 协议版本号 + 兼容性 |

## 数据流

```
Figma plugin (Figma Plugin API)
       │ 原始 figma.* 对象
       ▼
plugin/serializer.ts → shared/serialized-node.ts
       │ 标准化 JSON
       ▼
plugin/protocol/bridge.ts ←→ shared/protocol.ts + shared/envelope.ts
       │ msgpack 编码
       ▼
shared/codec.ts ← WebSocket binary
       │
       ▼
@figwright/mcp
mcp/src/dispatch.ts ←→ shared/rpc.ts + shared/queries.ts
       │
       ▼
MCP client (Claude Code / Cursor)
```

## 关键设计观察

- **codec 统一**:全链路 msgpack 二进制(JSON 字符串 + Base64 也考虑过,msgpack 更紧凑) ^[inferred]
- **envelope 与 protocol 分离**:envelope 是 RPC 包装(请求 ID + 类型 + 负载),protocol 是消息类型定义——便于升级 message kinds 而不动 RPC 框架
- **serialized-node 抽象 Figma 原始 API**:Figma 的 `figma.*` 对象深嵌套、含循环引用、含函数 —— 不能直接 JSON.stringify;serializer.ts 把它转成平面结构
- **design-context-dedupe 与 ground 工具紧耦合**:`get_design_context` 输出的去重由 shared 层提供,工具层只负责传参
- **tool-budgets 治理 token 消耗**:防止一次 call 返回过多节点把 MCP context 撑爆

## 协议升级策略

`version.ts` 提供协议版本号 + 兼容性字段——MCP client 连接时通过 `initialize` 协商版本。这是 MCP 协议自身的标准做法,figwright 在它之上做了扩展(RPC envelope + binary transport)。

## 与 vault 已有协议知识对应

| vault 已有 | 本层对应 |
|---|---|
| [[concepts/mcp-server-protocol-quirks]] MCP 鉴权/作用域 | figwright 是 MCP 协议的应用层实例 |
| [[concepts/static-analysis-knowledge-graph]] OpenLore AST 图 | `serialized-node.ts` 是 Figma 树的结构化序列化(类似 AST) |
| [[concepts/deterministic-agent-memory]] 确定性 + 显式失败 | `design-context-dedupe.ts` 去重是确定性算法 |
| [[concepts/cordis-plugin-framework]] 三件套 Service/Event/Effect | envelope ≈ RPC envelope,protocol ≈ message kinds |

## Open Questions

- msgpack vs JSON 在 WebSocket 上的实际性能差异(token 量/延迟)
- `serialized-node` 与 Figma `node` 对象的字段对齐率(100%?还是有省略?)
- `tool-budgets` 阈值是 hard-coded 还是按 MCP client 动态协商

## 相关

- [[projects/figwright/figwright]] 项目主页
- 中继架构 [[projects/figwright/concepts/mcp-local-relay-architecture]]
- 工具速查 [[projects/figwright/references/figwright-tool-taxonomy]]