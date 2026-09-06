---
title: mcp-server-protocol-quirks × google-stitch
category: synthesis
tags:
  - synthesis
  - mcp
  - google-stitch
  - claude-code
  - auth-pattern
sources:
  - "[[concepts/mcp-server-protocol-quirks]]"
  - "[[entities/google-stitch]]"
created: 2026-08-03T13:40:00Z
updated: 2026-08-03T13:40:00Z
summary: Stitch 是 MCP 协议的"复杂鉴权用户"——同时跑 API key header + OAuth proxy + auto refresh,把 MCP 的鉴权 layer 从"git config 类比"推到"OAuth 2.0 + proxy 链"实战级。
tier: core
lifecycle: reviewed
lifecycle_reason: "auto-promoted by wiki-lint --consolidate: age>30d, confidence>0.78"
lifecycle_changed: 2026-08-03
base_confidence: 0.78
provenance:
  extracted: 0.25
  inferred: 0.65
  ambiguous: 0.1
relationships:
  - target: "[[concepts/mcp-server-protocol-quirks]]"
    type: related_to
  - target: "[[entities/google-stitch]]"
    type: related_to
  - target: "[[skills/claude-code-mcp-auth-patterns]]"
    type: related_to
---

# mcp-server-protocol-quirks × google-stitch

## The Connection

[[concepts/mcp-server-protocol-quirks]] 给出 MCP 在 Claude Code 的"git config 类比"心智模型:`claude mcp add` 默认项目级,`-s user` ≡ `--global`,`$HOME` 不被特殊处理。这是**入门门槛低**的解释。

[[entities/google-stitch]] 是这个心智模型的**压力测试对象**:Google Labs 的 OAuth 鉴权 + 自动 refresh 需求 + `X-Goog-Api-Key` header 路径,把 MCP 的"简单两作用域 + 路径决定"推到必须用 proxy 进程 + gcloud credentials + auto refresh 才能搞定的复杂度。

二者交集揭示:**MCP 协议的协议层不复杂,协议之上的鉴权链才是真实复杂度来源**。^[inferred]

## Where They Co-occur

- [[skills/claude-code-mcp-auth-patterns]] 直接处理 Stitch + Claude Code 的两种鉴权路径(Path 1 = API key header 5 分钟;Path 2 = gcloud OAuth + proxy 自动 refresh)
- Stitch docs 是触发用户踩 MCP 作用域坑的常见入口(因为它用 `-s user` 等价形式,且需要 OAuth)
- `claude mcp add` 的命令语法在 Stitch 文档里出现时,`-s user` 与 `--global` 等价关系被首次文档化

## Cross-cutting Insight

**MCP 鉴权分三层** ^[inferred],每层有独立失败模式:

| 层 | 谁负责 | 失败模式 | Stitch 的选择 |
|---|---|---|---|
| 协议层 (transport) | Claude Code | stdio 阻塞 / JSON-RPC parse | 用 stdio (默认) |
| 鉴权层 (credentials) | 用户 / env / OAuth | 401, 过期, 路径错 | 选 Path 1 或 Path 2 |
| 执行层 (proxy refresh) | proxy 进程 | 进程崩, token 过期, 重启循环 | Path 2 用 `@_davideast/stitch-mcp proxy` |

**OAuth proxy 链对 `.env` 敏感**:运行 `stitch-mcp proxy` 前必须挪开项目根的 `.env`,否则报 cryptic 'invalid character d'。这是协议外的工程坑,不是 MCP 协议本身的问题,但暴露在 MCP 用户最常用的鉴权路径上。

## Tensions and Trade-offs

| 决策 | 短 | 长 |
|---|---|---|
| 5 分钟上手(Path 1) | 不需 proxy,API key header | 60 天过期手动换 |
| 长期重度(Path 2) | auto refresh 永远在 | proxy 进程崩了无人知;首次配置 20+ 分钟 |
| MCP 默认 stdio | 简单 | 跨机器 / 远程调试不便 |
| 项目级 `-s user` | 自动发现 | 路径稍变就找错 |

**未解**: `claude mcp add` 什么时候支持**真正的远程 MCP server**(HTTP transport)?目前都是 stdio + 本地进程。

## Strongest Objection

> **MCP 的协议层抽象泄漏**:为简化使用引入的协议,把鉴权复杂度的锅甩给了上层应用(Stitch / NotebookLM / n8n-mcp),每个应用都要重新解决"API key vs OAuth vs project vs global"。这不是 MCP 协议的胜利,是 MCP 协议的失败。

反驳路径: 协议层**故意**保持简单(只关心 stdio + JSON-RPC),让上层可以**独立演进**鉴权策略。如果 MCP 自己加 OAuth,会变成协议锁死某一厂商。代价:用户得**自己了解每个 server 的鉴权模式**。

**Test**: 在 [skills/notebooklm-mcp-setup] + Stitch + czlonkowski/n8n-mcp 三个 server 上,跑同一鉴权脚本(API key header),看谁需要改源码。MCP 协议保持简洁的代价落在用户身上。

## Open Questions

- 是否有"MCP server registry"可以公开声明 server 需要的鉴权模式?(类比 OAuth 2.0 dynamic client registration)
- Claude Code 是否会原生支持 OAuth 自动 refresh 而不需外部 proxy?
- 多 project 共用一个 MCP server 的全局 OAuth token 时,token 吊销是不是全局同步?

## Related

- [[concepts/mcp-server-protocol-quirks]] — MCP 在 Claude Code 的作用域 / `-s user` 等价
- [[entities/google-stitch]] — 复杂鉴权用户案例
- [[skills/claude-code-mcp-auth-patterns]] — 两条鉴权路径实操
- [[skills/notebooklm-mcp-setup]] — 另一 OAuth 用户案例
- [[concepts/design-system-as-ai-context]] — Stitch 输出的 DESIGN.md 是 AI 硬约束输入