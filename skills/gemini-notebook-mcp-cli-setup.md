---
title: "安装 gemini-notebook-mcp-cli — install + nlm setup add + nlm login"
category: skills
tags:
  - mcp
  - claude-code
  - notebooklm
  - install
  - google
summary: 安装 gemini-notebook-mcp-cli,通过 `nlm setup add` 为任意 AI 工具配置 MCP,再通过 CDP 驱动的浏览器登录完成认证。
sources:
  - https://github.com/jacob-bd/gemini-notebook-mcp-cli
  - https://github.com/jacob-bd/gemini-notebook-mcp-cli/blob/main/docs/GETTING_STARTED.md
  - https://github.com/jacob-bd/gemini-notebook-mcp-cli/blob/main/docs/AUTHENTICATION.md
  - https://github.com/jacob-bd/gemini-notebook-mcp-cli/blob/main/docs/CLI_GUIDE.md
created: 2026-08-06
updated: 2026-08-06
tier: core
lifecycle: reviewed
lifecycle_changed: "2026-08-06"
base_confidence: 0.85
provenance:
  extracted: 0.80
  inferred: 0.15
  ambiguous: 0.05
relationships:
  - target: "[[entities/gemini-notebook-mcp-cli]]"
    type: related_to
  - target: "[[concepts/cdp-cookie-extraction]]"
    type: uses
  - target: "[[concepts/mcp-multi-tool-installer]]"
    type: uses
  - target: "[[concepts/multi-profile-google-auth]]"
    type: uses
  - target: "[[concepts/auth-status-semantics]]"
    type: related_to
  - target: "[[concepts/mcp-server-protocol-quirks]]"
    type: related_to
  - target: "[[references/gemini-notebook-mcp-cli-known-issues]]"
    type: related_to
  - target: "[[references/gemini-notebook-mcp-cli-tools]]"
    type: related_to
  - target: "[[skills/notebooklm-mcp-setup]]"
    type: replaces
---

# 安装 gemini-notebook-mcp-cli

> **取代**旧版 [[skills/notebooklm-mcp-setup]] 方案。如果你之前安装的是老版本的 `notebooklm-mcp-server`,请按本页底部的迁移说明操作。

## 5 分钟安装

```bash
# 1. 安装(推荐用 uv;pip 和 pipx 也可以)
uv tool install notebooklm-mcp-cli

# 2. 验证
nlm --version                  # → notebooklm-mcp-cli 0.9.x
which notebooklm-mcp            # → ~/.local/bin/notebooklm-mcp

# 3. 为你的 AI 工具自动配置 MCP(不需要手动编辑 JSON)
nlm setup add claude-code      # 或者: claude-desktop, gemini, cursor, windsurf,
                                # github-copilot, cline, antigravity, opencode
nlm setup list                  # 验证

# 4. 认证(会启动一个受管理的浏览器会话)
nlm login

# 5. 重启你的 AI 工具,然后问它:
#    "列出我所有的 Gemini Notebook 笔记本"
```

就这样——5 条命令,不需要手动编辑 JSON,也不需要粘贴 cookie(CDP 浏览器流程会处理认证)。

## 认证实际是怎么工作的

`nlm login` **不**使用 OAuth(Google 没有为 NotebookLM 提供 OAuth)。它会通过 Chrome DevTools Protocol 启动一个专用的 Chromium 浏览器 profile(`~/.notebooklm-mcp-cli/chrome-profiles/default/`),你在里面登录一次 Google 账号,随后 cookie + CSRF token + session ID 会被提取出来并缓存到 `~/.notebooklm-mcp-cli/profiles/default/auth.json`。后续登录会复用已保存的浏览器 profile——只是重新提取新鲜的 cookie,不需要人工介入。

```
┌────────────────────┐   CDP launch    ┌──────────────────────────┐
│  nlm login         │ ──────────────→ │  Managed Chrome profile   │
│  (CLI / standalone)│                 │  (~/.notebooklm-mcp-cli/ │
└────────────────────┘                 │   chrome-profiles/default)│
                                       └──────────┬───────────────┘
                                                  │ user logs in to Google
                                                  ↓
                                       ┌──────────────────────────┐
                                       │  profiles/default/       │
                                       │   auth.json (cookies +   │
                                       │   CSRF + session + email)│
                                       └──────────────────────────┘
```

v0.1.9+ 版本中,认证生命周期已完全自动化:
- cookie 每次请求都会轮换 → 针对已保存的 profile 通过 CDP 自动刷新
- CSRF token 数分钟后过期 → 在 MCP 启动时自动提取
- session ID 每个会话都会轮换 → 在 MCP 启动时自动提取
- Build label(`bl` 参数) → 在登录/CSRF 刷新期间自动提取

如果你想查看认证状态:

```bash
nlm login --check                 # 实时状态(绕过缓存)
nlm doctor                        # 一站式诊断
```

MCP server 还暴露了 `server_info`,会报告 5 种认证状态中的一种——参见 [[concepts/auth-status-semantics]]。

## `nlm setup add <client>` — 多工具安装器

这是杀手级功能。不需要为 7 个不同的 AI 工具手动编辑 7 个不同的 JSON 配置文件,每个工具只需一条命令:

```bash
nlm setup add claude-code         # 通过 `claude mcp add` 写入 ~/.claude.json
nlm setup add claude-desktop      # 自动检测 regular + Relay AI/3P 两套 profile
nlm setup add gemini              # 写入 ~/.gemini/settings.json
nlm setup add cursor              # 写入 ~/.cursor/mcp.json
nlm setup add windsurf            # 写入 ~/.codeium/windsurf/mcp_config.json
nlm setup add github-copilot      # 写入 .vscode/mcp.json
nlm setup add cline
nlm setup add antigravity
nlm setup add opencode
nlm setup add json                # 面向其他任意工具的交互式向导
```

对于 Claude Desktop,该 CLI 具有 profile 感知能力:
- 自动检测 `regular` 和 `Relay AI / 3P` 两套 profile
- Claude 正在运行时拒绝写入(Claude 会在退出时重写配置,从而覆盖掉这次改动)
- 从不为不存在的 profile 创建新配置;只修改已检测到的 profile
- 移除操作只会列出包含 `gemini-notebook-mcp` 或某个已识别旧条目的 profile——不相关的 MCP 不会被触碰

`nlm setup add json` 模式是一个向导:它会依次询问 uvx 还是 binary、完整路径还是名称、是否带 `mcpServers` 外层包装,然后打印出 JSON 片段供你复制粘贴。

这个模式是可以泛化的——参见 [[concepts/mcp-multi-tool-installer]]。

## 多账号支持

同时使用工作和个人 Google 账号:

```bash
nlm login --profile work         # 打开浏览器 —— 用工作账号登录
nlm login --profile personal     # 打开浏览器 —— 用个人账号登录
nlm login profile list           # → work: jane@corp.com, personal: jane@gmail.com

nlm login switch personal        # 切换 MCP server 的默认账号
nlm notebook list --profile work # 一次性覆盖

# 重命名 / 删除
nlm login profile rename work company
nlm login profile delete old
```

每个 profile 都是完全隔离的:各自独立的 `profiles/<name>/auth.json`、各自独立的 Chromium profile 目录、各自独立采集到的邮箱。你可以同时登录多个 Google 账号,不需要在浏览器层面做任何会话倒腾。

MCP server 始终使用当前的默认 profile,因此 `nlm login switch <name>` 能让运行中的 MCP 立刻改指向另一个 Google 账号——参见 [[concepts/multi-profile-google-auth]]。

## 为非 MCP 工具安装 skill

某些 AI 工具(Cline、Antigravity、OpenClaw、Codex、OpenCode、Claude Code、Gemini CLI、Alef Agent)可以从一份 SKILL.md 中受益,它能教会 agent 如何使用这个 MCP。为你的工具安装它:

```bash
nlm skill install claude-code    # 用户级(需要先检测到该工具)
nlm skill install claude-code --level project   # 项目本地级
nlm skill install codex
nlm skill install gemini-cli
nlm skill install agents         # 通用的 .agents/skills/ 目标
nlm skill install alef-agent     # 单独的 ~/.alef-agent/workspace/skills/ 目标
nlm skill list                   # 显示所有目标的状态
nlm skill update                 # 刷新已安装的 skill
```

## 按需暴露工具(上下文窗口控制)

该 MCP 默认暴露 **43 个工具**——这会占用相当多的上下文。可以用分组或按名称的过滤器:

```bash
# 只读设置:隐藏会修改数据的分组
export NOTEBOOKLM_DISABLED_GROUPS="notebooks_manage,sources_manage,studio,research,sharing,notes"

# 隐藏某一个额外工具,但保留 studio_status 可见
export NOTEBOOKLM_DISABLED_TOOLS="tag"
export NOTEBOOKLM_ENABLED_TOOLS="studio_status"

# 解析顺序: DISABLED_GROUPS → DISABLED_TOOLS → ENABLED_TOOLS
```

可用分组:`notebooks_read`、`notebooks_manage`、`sources_read`、`sources_manage`、`chat`、`query_multi`、`organization`、`automation`、`notes`、`auth`、`server`、`sharing`、`research`、`studio`。未知分组会被忽略;改动在 server 重启后生效。更广泛的上下文窗口控制模式参见 [[concepts/mcp-server-protocol-quirks]]。

## 验证

安装 + 认证完成后,标准的冒烟测试是:

```bash
nlm notebook list --json         # CLI:返回笔记本的 JSON 数组
```

在你的 AI 助手中,等价的自然语言测试是:

> "列出我所有的 Gemini Notebook 笔记本"

如果 `notebook_list` 返回了你真实的笔记本,说明配置已经打通。如果遇到认证错误,参见 [[references/gemini-notebook-mcp-cli-known-issues]]。

## 从旧版 `notebooklm-mcp-server` 迁移

如果你之前安装的是**独立**的 `notebooklm-cli` + `notebooklm-mcp-server` 两个包(joydig 时代的方案,记录在 [[skills/notebooklm-mcp-setup]] 中):

```bash
# 1. 检查已安装的内容
uv tool list | grep notebooklm
# 留意: notebooklm-cli(旧)和/或 notebooklm-mcp-server(旧)

# 2. 移除旧包
uv tool uninstall notebooklm-cli
uv tool uninstall notebooklm-mcp-server

# 3. 重新安装统一包(--force 可修复 uv 的符号链接竞争问题)
uv tool install --force notebooklm-mcp-cli

# 4. 重新认证(cookie 通常还能用,但要验证一下)
nlm login --check
nlm login     # 只有在 --check 报告已失效时才需要

# 5. 如果你之前用另一个名字(例如 "notebooklm")注册过其他基于浏览器自动化的
#    NotebookLM MCP,请在添加新的之前先把它移除。
#    像 Hermes 这样的 agent 在两个 server 暴露了重叠的工具名
#    (notebook_create、source_add、notebook_query)时会感到困惑。
nlm setup add claude-code   # 注册为 "gemini-notebook-mcp"
```

迁移完成后,重启你的 AI 工具,让它加载新的 MCP 注册信息。

## 卸载

```bash
uv tool uninstall notebooklm-mcp-cli    # 移除二进制文件
rm -rf ~/.notebooklm-mcp-cli            # 移除缓存的状态(可选)

# 从每个 AI 工具中移除:
nlm setup remove claude-code
nlm setup remove cursor
# ...
```
