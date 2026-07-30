---
title: claude-mem — Claude Code 长期记忆压缩系统
category: entities
tags:
  - claude-code
  - mcp
  - memory
  - open-source
sources:
  - https://github.com/thedotmack/claude-mem
  - "本地插件: ~/.claude/plugins/cache/thedotmack/claude-mem/13.12.4"
source_url: https://github.com/thedotmack/claude-mem
created: 2026-07-29T09:04:00Z
updated: 2026-07-29T09:04:00Z
summary: >-
  Alex Newman (thedotmack) 出品的 Claude Code 记忆插件，Apache-2.0。用生命周期 hook 把每次
  Read/Edit/Bash 压成 observation 存入本地 SQLite+Chroma，下次会话自动注入相关上下文。
provenance:
  extracted: 0.9
  inferred: 0.05
  ambiguous: 0.05
base_confidence: 0.7
lifecycle: draft
lifecycle_changed: "2026-07-29"
---

# claude-mem

**claude-mem** 是一个为 [[entities/claude-code]] 提供跨会话长期记忆的插件，作者 Alex Newman（GitHub `thedotmack`），Apache-2.0 许可。本页基于**一手来源**：本地安装的 v13.12.4 插件文件（`~/.claude/plugins/cache/thedotmack/claude-mem/`）+ 实际 `~/.claude-mem/settings.json`，并与 GitHub README 交叉验证。

## 它解决什么问题

Claude Code 每次新会话都是"失忆"的——上一次的架构决策、踩过的坑、代码库结构全部要重新解释。claude-mem 让 Claude "记住"过去的工作：把每次工具调用压缩成 observation，会话结束时总结，下次会话开始时自动把相关记忆注入 prompt。核心口号是「compress, don't re-explain」，与本 wiki 的「[[concepts/prompt-caching|compile, don't retrieve]]」哲学同源。

## 核心机制（三段）

1. **捕获（capture）** — 通过 [[concepts/claude-code-hooks-lifecycle|6 个生命周期 hook]] 拦截工具调用，把 Read/Edit/Bash 异步压成结构化 observation。
2. **压缩 + 存储** — observation 落 SQLite（`sessions`/`observations`/`summaries` 表）+ Chroma 向量库（混合语义+关键词检索），全部在 `~/.claude-mem/`。压缩用便宜模型（默认 `claude-haiku-4-5`）。
3. **注入（inject）** — 第二次会话起，`SessionStart` hook 把相关记忆注入新会话开头。详见 [[concepts/claude-mem-memory-architecture]]。

## 安装（一手确认）

```bash
# 方式 A：插件市场（推荐，注册 hook）
/plugin marketplace add thedotmack/claude-mem
/plugin install claude-mem

# 方式 B：CLI 安装器
npx claude-mem install
```

⚠️ **陷阱**：`npm install -g claude-mem` **只装 SDK 库，不注册 hook**，记忆功能不生效。这与 [[concepts/mcp-server-protocol-quirks|MCP 作用域陷阱]] 是同一类「安装方式决定是否真正启用」的坑。

## 检索接口

claude-mem 通过 `mcp-search` MCP 服务器暴露 4 个工具，配合 3 层检索工作流（search → timeline → get_observations），见 [[skills/claude-mem-memory-usage]]。也提供 `/knowledge-agent` 把 observation 编译成可对话的「知识大脑」。

## 依赖与要求

- Node.js ≥ 20.12（`engines` 一手确认）、Bun ≥ 1.0（缺失自动装）、uv（Python 包管理器，自动装）、SQLite3（bundled）
- 内置 20+ 语言的 tree-sitter 语法（TS/Py/Go/Rust/Swift/…）用于代码结构解析

## 隐私与云同步

**默认全部本地**——除了发给压缩 provider（Claude/OpenRouter/Gemini）的调用外，数据不出机器，`npx claude-mem uninstall` 干净清除。用 `<private>` 标签排除敏感内容。**可选**付费云同步（cmem.ai Pro）会上传 observation 叙述和完整 prompt 文本——见 [[skills/claude-mem-memory-usage]] 的云同步小节。这是一个需要显式区分的点：**本地免费 vs 上云付费**。

## 相关页面

- [[concepts/claude-mem-memory-architecture]] — 捕获/压缩/注入三段架构
- [[concepts/claude-code-hooks-lifecycle]] — 6 个 hook 事件如何驱动记忆
- [[skills/claude-mem-memory-usage]] — 安装、检索、知识 agent、调优实操
- [[entities/claude-code]] — 宿主 agent
- [[concepts/mcp-server-protocol-quirks]] — 同类安装作用域坑
