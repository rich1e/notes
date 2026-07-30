---
title: >-
  Research: 在 Claude 中用 claude-mem 管理长期记忆
category: synthesis
tags:
  - memory
  - claude-code
  - mcp
  - research
sources:
  - https://github.com/thedotmack/claude-mem
  - "本地插件 v13.12.4: ~/.claude/plugins/cache/thedotmack/claude-mem/"
  - "~/.claude-mem/settings.json（实机配置）"
created: 2026-07-29T09:04:00Z
updated: 2026-07-29T09:04:00Z
summary: >-
  claude-mem 研究综合：hook 驱动的 capture→compress→inject 记忆流水线，本地 SQLite+Chroma，
  第二次会话起自动注入，3 层检索省 10× token，本地免费/上云付费。
provenance:
  extracted: 0.88
  inferred: 0.08
  ambiguous: 0.04
base_confidence: 0.7
lifecycle: draft
lifecycle_changed: "2026-07-29"
---

# Research: 在 Claude 中用 claude-mem 管理长期记忆

## Overview

本次研究的一手来源极强：**目标插件 claude-mem v13.12.4 就装在本机**，可直接读源文件（hooks.json、.mcp.json、skills/、实机 settings.json），再与 GitHub README 交叉验证。结论：claude-mem 用 Claude Code 的 hook 系统实现「跨会话长期记忆」——把工具调用压成 observation 存本地 SQLite+Chroma，第二次会话起自动注入相关记忆，查询走「先筛后取」3 层工作流省 token。

## Key Findings

- **F1 — 三段流水线**：capture（hook 拦截工具调用）→ compress（haiku 压成结构化 observation 存 SQLite+Chroma）→ inject（SessionStart 注入）。见 [[concepts/claude-mem-memory-architecture]]。
- **F2 — 全靠 hook，不改本体**：6 个挂载点（Setup/SessionStart/UserPromptSubmit/PostToolUse/PreToolUse/Stop），捕获与总结类都是 `async` 旁路，不拖慢交互。见 [[concepts/claude-code-hooks-lifecycle]]。
- **F3 — 记忆从第二次会话起注入**：第一次播种，之后每次 SessionStart 注入默认 50 条 observation + 10 个会话摘要。
- **F4 — 3 层检索省 10× token**：`search`(索引)→`timeline`(上下文)→`get_observations`(全文)，永远先筛后取。见 [[skills/claude-mem-memory-usage]]。
- **F5 — 安装方式决定是否生效**：`npm install -g` 只装 SDK 不注册 hook；必须用插件市场或 `npx claude-mem install`。这是与 [[concepts/mcp-server-protocol-quirks]] 同构的「安装作用域坑」。
- **F6 — knowledge-agent = 可对话知识大脑**：`build_corpus`→`prime_corpus`→`query_corpus` 把 observation 编译成综合回答，而非原始记录。
- **F7 — 双库设计**：SQLite 做结构化查询（sessions/observations/summaries），Chroma 做混合语义+关键词检索。
- **F8 — 便宜模型 + tier routing**：默认 `claude-haiku-4-5` 压缩，复杂总结可路由 sonnet——记忆系统自己也在做 token 优化，呼应 [[skills/claude-code-token-optimization]]。

## Core Concepts

- [[concepts/claude-mem-memory-architecture]] — capture/compress/inject 三段
- [[concepts/claude-code-hooks-lifecycle]] — 6 个 hook 挂载点
- [[concepts/prompt-caching]] — 同属「上下文复用」哲学（KV 缓存 vs 跨会话记忆）

## Entities & Tools

- [[entities/claude-mem]] — 插件本体（thedotmack，Apache-2.0）
- [[entities/claude-code]] — 宿主 agent

## Contradictions & Open Questions

- **C1 — hook 数量口径**：how-it-works skill 说「5 lifecycle hooks」，README 说「6 hook 脚本」，本地 hooks.json 实配 6 个事件。属**表述口径差异**（是否把 Setup/PreToolUse 计入 lifecycle），非事实冲突。以 hooks.json 为准。
- **C2 — 「数据不出机器」vs 云同步**：how-it-works 强调 nothing leaves your machine，但 cloud-sync skill 描述付费上云会上传 observation 叙述 + 完整 prompt。二者不矛盾——**本地默认免费、上云是可选付费**，但宣传语需并列读。
- **OQ — 实机尚未积累数据**：本机 `~/.claude-mem/` 目前只有 logs + settings，无 SQLite——说明数据库在首次实质会话后才生成，本研究的存储层结论来自 README + 代码，未在本机实测查询。

## Sources Consulted

- [[entities/claude-mem]]（含一手文件清单）
- GitHub: https://github.com/thedotmack/claude-mem
- 本地：`hooks/hooks.json` / `.mcp.json` / `skills/*` / `~/.claude-mem/settings.json`
