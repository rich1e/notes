---
title: "Claude Code"
category: entities
tags: [anthropic, ai-coding-agent, mcp, claude-code, entity]
sources:
  - "https://medium.com/devsecops-ai/how-google-stitch-claude-codes-mcp-integration-changed-the-way-i-build-products-63ecb8ed7f5a"
  - "https://baoyu.io/blog/2026-04-06/claude-code-token-optimization"
  - "https://joydig.com/notebooklm-mcp-server-claude-code/"
source_url: "https://www.claude.com/product/claude-code"
created: "2026-07-28T00:00:00Z"
updated: "2026-07-28T00:00:00Z"
summary: "Anthropic 出品的终端式 AI 编码 agent。承担项目中逻辑、组件架构、代码生成的职责；通过 MCP 接外部服务（设计工具、文档、CI 等），通过提示缓存与上下文管理控制 token。"
tier: core
lifecycle: draft
lifecycle_changed: "2026-07-28"
base_confidence: 0.62
provenance:
  extracted: 0.85
  inferred: 0.10
  ambiguous: 0.05
relationships:
  - target: "[[entities/google-stitch]]"
    type: related_to
  - target: "[[concepts/mcp-server-protocol-quirks]]"
    type: derived_from
  - target: "[[skills/claude-code-mcp-auth-patterns]]"
    type: derived_from
  - target: "[[skills/claude-code-token-optimization]]"
    type: related_to
  - target: "[[skills/claude-code-settings]]"
    type: related_to
---

# Claude Code

> Anthropic 的终端式 AI 编码 agent。设计感不强，逻辑/接线强。

## 是什么

Claude Code 是 Anthropic 出品的基于终端的编码 agent。它不是 IDE 插件，不是聊天机器人——它是命令行里的协作编码伙伴。典型用法：在仓库根目录 `claude` 启动，进入对话式编码会话，agent 通过工具调用读文件、改文件、跑命令。

## 核心特征

- **CLAUDE.md 项目规则**：仓库根的 markdown 文件承载项目级指令，每次请求都作为缓存前缀的一部分加载。
- **MCP 接入外部服务**：通过 Model Context Protocol 连接外部工具（设计工具、文档、数据库、CI）。MCP 是 Claude Code 区别于普通 chat agent 的关键能力。
- **提示缓存友好**：见 [[skills/claude-code-token-optimization]]——固定基础设施（系统提示、工具定义、CLAUDE.md）以 1/10 价复用。频繁 `/clear` 反而把缓存优势烧光。

## 在多 agent 工作流中的角色

Sachin Sharma 在 Google Stitch + Claude Code 一文中的定位很清晰：

- **Stitch 拥有视觉层**（设计、间距、配色、字体）
- **Claude Code 拥有逻辑层**（数据流、状态管理、组件架构、构建配置）
- **MCP 层做翻译**（无需人工搬运设计决策）

这套分工避免 Claude Code 在不擅长的设计决策上耗 token，也避免 Stitch 越界去生成业务逻辑。

## MCP 相关配置要点

- **`claude mcp add` 默认项目级**——见 [[concepts/mcp-server-protocol-quirks]]。
- **`-s user` / `--global` 写到顶层 `mcpServers`**——一次配置跨项目生效。
- **不要把 `.claude.json` 提交**——里面可能含 API key 等明文凭证。

## 主要配置页面

- [[skills/claude-code-settings]] — settings.json 四级作用域、CLAUDE.md 三层、MCP 两层的完整层级
- [[skills/claude-code-token-optimization]] — 提示缓存与会话生命周期策略
- [[skills/claude-code-mcp-auth-patterns]] — 接外部 MCP server 的两种鉴权范式
- [[concepts/mcp-server-protocol-quirks]] — `claude mcp add` 的作用域陷阱
- [[skills/notebooklm-mcp-setup]] — 接 NotebookLM 的具体流程

## Related

- [[synthesis/concepts-agent-operating-system × entities-claude-code]] — synthesis:AOS 五层记忆里宿主原生只兜底两层
- [[synthesis/concepts-claude-mem-memory-architecture × skills-claude-code-settings]] — synthesis:可扩展性两支柱与共享的作用域陷阱