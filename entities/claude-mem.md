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
  - "Clippings/开源 Claude Code 自动记忆管理插件 Claude-Mem 完整上手攻略.md (兔兔AGI, 2026-03-03, 二手/v9.0.5 时代)"
source_url: https://github.com/thedotmack/claude-mem
created: 2026-07-29T09:04:00Z
updated: 2026-07-31T12:10:00Z
summary: >-
  Alex Newman (thedotmack) 出品的 Claude Code 记忆插件，Apache-2.0。用生命周期 hook 把每次
  Read/Edit/Bash 压成 observation 存入本地 SQLite+Chroma，下次会话自动注入相关上下文。
provenance:
  extracted: 0.9
  inferred: 0.05
  ambiguous: 0.05
base_confidence: 0.7
lifecycle: draft
tier: supporting
lifecycle_changed: "2026-07-29"
relationships:
  - target: "[[entities/sqlite]]"
    type: uses
---

# claude-mem

**claude-mem** 是一个为 [[entities/claude-code]] 提供跨会话长期记忆的插件，作者 Alex Newman（GitHub `thedotmack`），Apache-2.0 许可。本页基于**一手来源**：本地安装的 v13.12.4 插件文件（`~/.claude/plugins/cache/thedotmack/claude-mem/`）+ 实际 `~/.claude-mem/settings.json`，并与 GitHub README 交叉验证。

## 它解决什么问题

Claude Code 每次新会话都是"失忆"的——上一次的架构决策、踩过的坑、代码库结构全部要重新解释。claude-mem 让 Claude "记住"过去的工作：把每次工具调用压缩成 observation，会话结束时总结，下次会话开始时自动把相关记忆注入 prompt。核心口号是「compress, don't re-explain」，与本 wiki 的「[[concepts/prompt-caching|compile, don't retrieve]]」哲学同源。

## 核心机制（三段）

1. **捕获（capture）** — 通过 [[concepts/claude-code-hooks-lifecycle|6 个生命周期 hook]] 拦截工具调用，把 Read/Edit/Bash 异步压成结构化 observation。
2. **压缩 + 存储** — observation 落 [[entities/sqlite|SQLite]]（`sessions`/`observations`/`summaries` 表）+ Chroma 向量库（混合语义+关键词检索），全部在 `~/.claude-mem/`。压缩用便宜模型（默认 `claude-haiku-4-5`）。
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

claude-mem 通过 `mcp-search` MCP 服务器暴露 4 个工具，配合 3 层检索工作流（search → timeline → get_observations），见 [[skills/claude-mem-memory-usage]]。第 4 个工具 `__IMPORTANT` 不返回数据——它是对 Claude 可见的**工作流文档**，指导如何高效走三层检索 ^[inferred]。也提供 `/knowledge-agent` 把 observation 编译成可对话的「知识大脑」。

## Web 查看器 + Worker HTTP API

Worker 服务（Bun 管理，SessionStart 拉起、常驻）不只是 hook 的后端，还暴露一个 **HTTP API + Web 查看器 UI**，可在浏览器里实时可视化记忆流：实时 observation 流（emoji 标重要性）、会话时间线、搜索界面、设置面板、稳定版/beta 版本切换。健康检查 `curl http://localhost:<port>/api/health`。

> **端口有版本差异** ^[ambiguous]：本地一手 `hooks.json`（v13.12.4）实证默认端口 **37702**（见 [[concepts/claude-code-hooks-lifecycle]]）；二手攻略（v9.0.5 时代）反复写 **37777** 并配 10 个搜索端点。以一手 37702 为准；旧版本或不同配置可能是 37777。端口冲突时用 `CLAUDE_MEM_WORKER_PORT` 改。UI 对基本使用非必需，但便于理解捕获了什么。

## 目录级 CLAUDE.md（文件夹上下文）

除全局记忆库外，claude-mem 还能为**被操作的项目文件夹自动生成 `CLAUDE.md`**，作为该目录的「活动时间线」补充全局库。机制：识别文件夹 → 查该目录相关 observation → 整理成时间线表（observation ID、时间、类型 emoji、标题、预估 token）→ 写入并用 `<claude-mem-context>` 标签包裹。**标签之外的用户内容在重新生成时保留**——可在生成块上下写自己的文档、目录指令、架构约定。由 `CLAUDE_MEM_FOLDER_INDEX_ENABLED` 开关控制。详见 [[concepts/claude-mem-memory-architecture]] 注入段。

## 无尽模式（Endless Mode，beta）

beta 通道提供**无尽模式**——延长单会话的仿生记忆架构：不再在约 50 次工具调用后触上下文上限，支持约 **1000 次工具使用（~20 倍）**；靠实时压缩工具输出削减约 **95% token**，把扩展复杂度从 **O(N²) 降到 O(N)**。代价：每次工具调用生成 observation 会**加 60–90 秒延迟**——跨天/周的深度会话可接受，快速连续调用时会成瓶颈。经 Web 查看器 → 设置 → 版本频道切 beta 启用。详见 [[concepts/claude-mem-memory-architecture]] 无尽模式小节。

## 依赖与要求

- Node.js ≥ 20.12（`engines` 一手确认）、Bun ≥ 1.0（缺失自动装）、uv（Python 包管理器，自动装）、SQLite3（bundled）
- 内置 20+ 语言的 tree-sitter 语法（TS/Py/Go/Rust/Swift/…）用于代码结构解析

## 隐私与云同步

**默认全部本地**——除了发给压缩 provider（Claude/OpenRouter/Gemini）的调用外，数据不出机器，`npx claude-mem uninstall` 干净清除。用 `<private>` 标签排除敏感内容。**可选**付费云同步（cmem.ai Pro）会上传 observation 叙述和完整 prompt 文本——见 [[skills/claude-mem-memory-usage]] 的云同步小节。这是一个需要显式区分的点：**本地免费 vs 上云付费**。

**双重标签系统**：`<private>`（用户控制，保护敏感内容不入库）+ `<claude-mem-context>`（系统级，标记自动生成区、防重复存储）。两者职责不同——前者是隐私边界，后者是幂等/去重标记。

## 已知问题

- **空 `CLAUDE.md`**：`v9.0.5` 已知 bug——目录级上下文会生成空 `CLAUDE.md`。临时解法：手动删已建目录、在 `.gitignore` 加模式，或等后续版本修复 ^[ambiguous]（二手来源，本地 v13.12.4 未复现）。

## 相关页面

- [[concepts/claude-mem-memory-architecture]] — 捕获/压缩/注入三段架构
- [[concepts/claude-code-hooks-lifecycle]] — 6 个 hook 事件如何驱动记忆
- [[skills/claude-mem-memory-usage]] — 安装、检索、知识 agent、调优实操
- [[entities/claude-code]] — 宿主 agent
- [[concepts/mcp-server-protocol-quirks]] — 同类安装作用域坑

## Related

- [[synthesis/Research: claude-mem 长期记忆]] — 自身综合页(入口)
