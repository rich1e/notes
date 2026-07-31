---
title: Claude Code 生命周期 Hook — claude-mem 的 6 个挂载点
category: concepts
tags:
  - claude-code
  - memory
  - concept
sources:
  - "本地插件: ~/.claude/plugins/cache/thedotmack/claude-mem/13.12.4/hooks/hooks.json"
  - https://github.com/thedotmack/claude-mem
created: 2026-07-29T09:04:00Z
updated: 2026-07-29T09:04:00Z
summary: >-
  claude-mem 靠 Claude Code 的 hook 系统运转：Setup 校验版本、SessionStart 注入记忆、
  UserPromptSubmit 初始化、PostToolUse 捕获、PreToolUse(Read) 补上下文、Stop 总结。
provenance:
  extracted: 0.95
  inferred: 0.03
  ambiguous: 0.02
base_confidence: 0.72
lifecycle: draft
tier: supporting
lifecycle_changed: "2026-07-29"
---

# Claude Code 生命周期 Hook（claude-mem 实证）

Claude Code 的 hook 系统允许插件在会话生命周期的特定节点执行命令。[[entities/claude-mem]] 完全靠 hook 驱动——不改 Claude 本体，只在事件点挂脚本。以下 6 个挂载点来自**一手** `hooks.json`，是理解「记忆何时捕获、何时注入」的关键。

## 6 个挂载点

| Hook 事件 | matcher | 作用 | 关键属性 |
|---|---|---|---|
| **Setup** | `*` | 跑 `version-check.js` 校验插件版本一致 | timeout 300s |
| **SessionStart** | `startup\|clear\|compact` | ①启动 worker 服务 ②把相关记忆注入新会话 | 两个子 hook 串行 |
| **UserPromptSubmit** | （全部） | `session-init`——每次提交 prompt 时初始化会话记忆 | timeout 60s |
| **PostToolUse** | `*` | `observation`——捕获工具调用压成 observation | **async: true** |
| **PreToolUse** | `Read` | `file-context`——读文件前补充上下文 | **async: true** |
| **Stop** | （全部） | `summarize`——会话结束时汇总本次 observation | **async: true** |

> README 另称有 `SessionEnd`（共 6 hook 脚本）；本地 `hooks.json` 实际配置的是上述 6 个事件（其中 Setup + PreToolUse 是 SessionEnd 之外的补充）。捕获/总结类 hook 都是 `async`，不阻塞 Claude 主流程——这是关键设计：**记忆是旁路，不拖慢交互**。

## 为什么这样切分

- **SessionStart 注入 vs UserPromptSubmit 初始化分离**：会话级上下文只需注入一次（SessionStart），而每条 prompt 可能需要刷新会话记忆句柄（UserPromptSubmit）。
- **PostToolUse 全量捕获 + skip 名单**：用 matcher `*` 兜底所有工具，再靠 `CLAUDE_MEM_SKIP_TOOLS` 过滤噪音，比逐个 matcher 更稳。
- **worker 常驻**：SessionStart 先拉起 `worker-service.cjs`（默认端口 37702），后续 hook 都通过 HTTP 与之通信——避免每个 hook 重启进程。

## 与 wiki 已有 hook 知识的关系

本 vault 已有 [[skills/claude-code-settings]]（四级配置作用域）、[[concepts/mcp-server-protocol-quirks]]（MCP 作用域）。hook 是第三条「Claude Code 可扩展性」支柱——**配置管作用域、MCP 管外部工具、hook 管生命周期事件**。三者共同构成「用好 Claude Code 要知道的底层机制」。

## 相关页面

- [[entities/claude-mem]] / [[concepts/claude-mem-memory-architecture]] — hook 驱动的记忆系统
- [[skills/claude-code-settings]] — 配置作用域
- [[concepts/mcp-server-protocol-quirks]] — MCP 服务器作用域

## Related

- [[synthesis/Research: claude-mem 长期记忆]] — 综合页:6 个 hook 装在 claude-mem 上的具体效果
