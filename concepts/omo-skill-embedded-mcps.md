---
title: "omo Skill-Embedded MCPs（skill 自带 MCP）"
category: concepts
tags:
  - omo
  - mcp
  - skill
  - token-optimization
  - concept
sources:
  - "https://github.com/code-yeongyu/oh-my-openagent"
created: "2026-08-05T07:30:00Z"
updated: "2026-08-05T07:30:00Z"
provenance:
  extracted: 0.82
  inferred: 0.12
  ambiguous: 0.06
base_confidence: 0.60
lifecycle: draft
lifecycle_changed: "2026-08-05"
tier: supporting
relationships:
  - target: "[[skills/claude-code-token-optimization]]"
    type: related_to
  - target: "[[concepts/mcp-server-protocol-quirks]]"
    type: related_to
  - target: "[[entities/oh-my-openagent]]"
    type: related_to
summary: "omo 的 MCP context 优化策略：MCP servers 随 skill 按需 spin up 而非常驻主 context，避免 tools/schemas 占满 context window，任务结束自动 spin down。"
---

# omo Skill-Embedded MCPs（skill 自带 MCP）

> omo 的 **Skill-Embedded MCPs** 解决"MCP servers 吃 context budget"问题——MCPs 不在主 session 里常驻，**随 skill 按需 spin up**、任务结束 spin down。Context window 保持清洁。

## 问题

> "MCP servers eat your context budget. We fixed that."

MCP servers（web 搜索 / docs 检索 / GitHub 代码搜索等）每个都暴露 N 个 tools + schemas。一次性全加载 → 主 context window 被塞满，**留给实际任务的 token 反而少了**。

## 解决方案

> "Skills bring their own MCP servers. They spin up on demand, scoped to the task, and go away when done. The context window stays clean."

**MCPs 嵌入到 skills 里**——不是 session 全局：

1. **Skill 启动** → 关联 MCPs spin up
2. **Skill 工作中** → MCPs 在 skill context 里
3. **Skill 完成** → MCPs spin down

每个 skill 自带自己需要的 MCP server。**不像全局 MCP 注册**那样 always-on。

## 与 vault 已有概念的关系

| vault 已有 | 在 Skill-Embedded MCPs 中的体现 |
|---|---|
| [[skills/claude-code-token-optimization]] | 直接落地"token 节流"的工程方案 |
| [[concepts/mcp-server-protocol-quirks]] | 反转 vault MCP 默认全局注册的策略——按 skill scope |
| [[entities/claude-code-agent-teams-feature]] | 推测 Team Mode 每个 member 自己 spin up MCPs [[inferred]] |
| [[concepts/ai-tool-specialization]] | MCP 跟着 skill 而非跟着 session——专业化更细 |

## Light Edition 的对应实现

omo Light Edition（Codex CLI）有 **5 个 plugin-scoped MCPs**：

| MCP | 用途 |
|---|---|
| `grep_app` | GitHub 代码搜索 |
| `context7` | 官方文档 |
| `codegraph` | 代码图 |
| `git_bash` | Git 操作 |
| `lsp` | LSP（diagnostics / navigation） |

**Light Edition 也是 plugin-scoped**——MCPs 跟 plugin（≈ skill）走，不在主 session 常驻。

## 与"全局 MCP"的对比

| 维度 | 全局 MCP（默认） | Skill-Embedded MCP（omo） |
|---|---|---|
| 加载时机 | session 启动时全加载 | skill 启动时按需加载 |
| context 占用 | 持续占 | 临时占 |
| 适用 | 频繁使用的 MCP | 偶尔使用的 MCP |
| 配置 | `.mcp.json` 全局 | skill 内置 |

## Open Questions

- Skill-Embedded MCPs 的**生命周期管理**——是 skill exit 自动 spin down，还是有显式 close？[[ambiguous]]
- 与 [[concepts/agent-team-display-modes]] 的"deferred schemas"关系——Claude Code 的 `alwaysLoad: false` 似乎与 skill-embedded 同思路，但机制不同
- 跨 skill **共享 MCP** 的机制——例如 Exa 同时给 search 和 analyze skill 用，是 spin up 两次还是 share？[[ambiguous]]

## Related

- [[entities/oh-my-openagent]] — 框架本体
- [[skills/claude-code-token-optimization]] — 直接落地 vault token 优化哲学
- [[concepts/mcp-server-protocol-quirks]] — MCP 注册策略反转
- [[concepts/omo-editions-ultimate-vs-light]] — Light Edition 也有 plugin-scoped MCPs