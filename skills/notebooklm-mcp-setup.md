---
title: NotebookLM MCP Server — 让 Claude 直接查 Google NotebookLM
category: skills
tags:
  - mcp
  - claude-code
  - notebooklm
  - llm
  - deprecated
summary: ⚠ DEPRECATED — superseded by [[entities/gemini-notebook-mcp-cli]] (unified CLI + 43-tool MCP). Use [[skills/gemini-notebook-mcp-cli-setup]] instead. This page kept only for users still on the legacy `notebooklm-mcp-server`.
sources:
  - https://joydig.com/notebooklm-mcp-server-claude-code/
created: 2026-07-26
updated: 2026-08-06
tier: peripheral
lifecycle: archived
lifecycle_changed: "2026-08-06"
lifecycle_reason: "Superseded by [[skills/gemini-notebook-mcp-cli-setup]] — the unified package ships both nlm CLI and notebooklm-mcp, supports 43 tools, and replaces the 4-step legacy install. See [[entities/gemini-notebook-mcp-cli]] for full migration context."
base_confidence: 0.55
provenance:
  extracted: 0.75
  inferred: 0.15
  ambiguous: 0.10
relationships:
  - target: "[[skills/claude-code-settings]]"
    type: related_to
  - target: "[[concepts/mcp-server-protocol-quirks]]"
    type: related_to
  - target: "[[skills/gemini-notebook-mcp-cli-setup]]"
    type: related_to
  - target: "[[entities/gemini-notebook-mcp-cli]]"
    type: related_to
---

# NotebookLM MCP Server — DEPRECATED ⚠

> **This skill describes the legacy `notebooklm-mcp-server` package. It has been superseded by the unified [[entities/gemini-notebook-mcp-cli]] package (single wheel ships both `nlm` CLI and `notebooklm-mcp` MCP server).**
>
> **Use [[skills/gemini-notebook-mcp-cli-setup]] instead.** That page covers `nlm login` (CDP-driven browser auth), `nlm setup add <client>` (auto-configures 9+ AI tools), named profiles, the 43-tool surface, and the multi-probe `auth_status` health checks.
>
> The 4-step recipe below is kept for users who have not yet migrated. If you're new to this, go to the new page; if you're troubleshooting an old install, the steps below still work but expect to upgrade soon.

## Why deprecate

The legacy `notebooklm-mcp-server`:

- Exposes only **2 tools** (`notebook_list`, `notebook_query`) — no source management, no Studio artifacts, no sharing, no research, no batch
- Requires **manual cookie paste** into `notebooklm-mcp-auth` — hostile UX
- Has no multi-account support
- Has no setup wizard — you hand-edit `~/.claude.json` paths

[[entities/gemini-notebook-mcp-cli]] v0.9.7 ships all of this and is the de facto standard. The migration path is in [[skills/gemini-notebook-mcp-cli-setup#migrating-from-legacy-notebooklm-mcp-server]].

---

# Legacy 4-step install (kept for migration only)

## 什么是 NotebookLM MCP Server

> NotebookLM 擅长"消化文档做问答"，Claude 擅长"推理和代码"。MCP 桥接后两者无缝协作。

## 什么是 NotebookLM MCP Server

[NotebookLM](https://notebooklm.google.com/) 是 Google 推出的 AI 笔记工具，专门针对用户上传的文档做问答和总结。

[notebooklm-mcp-server](https://modelcontextprotocol.io/) 是基于 [MCP（Model Context Protocol）](https://modelcontextprotocol.io/) 的开源桥接服务，让 Claude 通过标准化接口直接操作 NotebookLM 笔记本。

**典型场景**：把团队的技术文档导入 NotebookLM，用 Claude 协助分析、检索、生成；NotebookLM 当作"知识存储库"，Claude Code 当作"分析推理引擎"。

## 安装步骤

### 1. 安装 uv（Python 工具管理器）

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv --version
```

### 2. 安装 notebooklm-mcp-server

```bash
uv tool install notebooklm-mcp-server
```

安装后 `~/.local/bin/` 会出现两个命令：

- `notebooklm-mcp` — MCP 服务器主程序
- `notebooklm-mcp-auth` — Google 账号认证工具

### 3. Google 账号认证

```bash
notebooklm-mcp-auth
```

认证成功后凭据保存在 `~/.notebooklm-mcp/auth.json`（Google 账号 Cookie 信息）。

### 4. 添加到 Claude Code（推荐使用 `--global`）

```bash
claude mcp add --global notebooklm-mcp -- /home/$USER/.local/bin/notebooklm-mcp
```

**两个关键点**：

1. **必须加 `--global`**：否则只对当前目录对应的项目生效
2. **建议使用绝对路径**：避免 `PATH` 环境变量差异导致找不到命令

详见 [[concepts/mcp-server-protocol-quirks]] —— `claude mcp add` 默认是项目作用域，`$HOME` 目录也不会被特殊处理。

## 验证连接

重启 Claude Code 后：

```
列出我 NotebookLM 里的所有笔记本
```

Claude 调用 `notebook_list` 工具返回所有笔记本（典型数量 20+）。

```
查询我的「Chromium Development」笔记本，总结一下里面关于渲染进程的内容
```

Claude 调用 `notebook_query` 工具，基于笔记本实际资料给出回答。

## 支持的功能

| 类别 | 能力 |
|------|------|
| 笔记本管理 | 创建、删除、重命名 |
| 资料源管理 | 添加网页 URL、YouTube 视频、Google Drive 文档、粘贴文本 |
| AI 查询 | 笔记本内容问答、多轮对话 |
| Studio 内容生成 | 音频摘要、视频概览、信息图、幻灯片、报告、闪卡、测验、思维导图 |
| 深度研究 | 联网搜索 / Google Drive 搜索，自动导入相关资料源 |

## 典型工作流

```
┌─────────────────┐   add_source    ┌──────────────┐
│  文档/网页/视频 │ ──────────────→ │  NotebookLM  │
└─────────────────┘                 └──────┬───────┘
                                           │ query
                                           ↓
                                    ┌──────────────┐
                                    │ Claude Code  │
                                    │  (推理+代码) │
                                    └──────────────┘
```

1. **存**：把文档/网页/视频导入 NotebookLM（自带 RAG）
2. **问**：让 Claude 通过 MCP 查询 NotebookLM 笔记本
3. **做**：Claude 基于检索结果做推理、生成代码或分析报告

## 故障排查

| 现象 | 原因 | 解决 |
|------|------|------|
| 工具在某些项目不出现 | MCP 配置是项目级，没 `--global` | 重新 `claude mcp add --global`，或挪到 `~/.claude.json` 顶层 `mcpServers` |
| 找不到 `notebooklm-mcp` 命令 | PATH 没含 `~/.local/bin` | 用绝对路径 |
| 认证失败 | Cookie 过期 | 重新跑 `notebooklm-mcp-auth` |
| 笔记本列表为空 | 账号没笔记本 | 先在 NotebookLM Web 创建至少一个笔记本 |

## 相关页面

- [[concepts/mcp-server-protocol-quirks]] — `claude mcp add --global` 的作用域陷阱详解
- [[skills/claude-code-settings]] — Claude Code 完整配置作用域体系
- [[skills/claude-code-token-optimization]] — 复杂工作流下的会话管理
