---
title: "MCP Multi-Tool Installer — `nlm setup add <client>` 模式"
category: concepts
tags:
  - mcp
  - cli
  - dx
  - pattern
summary: 通过每个工具一条 CLI 命令,把 MCP server 配置分发到 7 个以上的 AI 工具,而不必让用户手动编辑 7 个不同路径下的 JSON 配置文件。
sources:
  - https://github.com/jacob-bd/gemini-notebook-mcp-cli/blob/main/docs/CLI_GUIDE.md
created: 2026-08-06
updated: 2026-08-06
tier: supporting
lifecycle: reviewed
lifecycle_changed: "2026-08-06"
base_confidence: 0.85
provenance:
  extracted: 0.80
  inferred: 0.15
  ambiguous: 0.05
relationships:
  - target: "[[entities/gemini-notebook-mcp-cli]]"
    type: uses
  - target: "[[concepts/mcp-server-protocol-quirks]]"
    type: related_to
  - target: "[[concepts/auth-status-semantics]]"
    type: related_to
  - target: "[[references/gemini-notebook-mcp-cli-tools]]"
    type: related_to
---

# MCP Multi-Tool Installer — `nlm setup add <client>` 模式

> 当你的 MCP server 需要同时被 Claude Code、Claude Desktop、Gemini CLI、Cursor、Windsurf、GitHub Copilot、Cline、Antigravity、OpenCode、OpenClaw 等等工具访问时,不应该让用户去手动编辑 7 个不同路径下的 JSON 配置文件。每个工具一条 CLI 命令即可:`nlm setup add <client>`。

## 为什么这件事并不简单

每个 AI 工具都把 MCP server 配置存在不同的位置,而且 JSON 结构也各不相同:

| 工具 | 路径 | 顶层 key | 子 key | "servers" 是数组吗? |
|------|------|--------------|---------|------------------|
| Claude Code | `~/.claude.json` | `mcpServers` | `command` + `args` | dict |
| Claude Desktop(macOS 现行版) | `~/Library/Application Support/Claude-3p/claude_desktop_config.json` | `mcpServers` | `command` | dict |
| Claude Desktop(macOS 旧版) | `~/Library/Application Support/Claude/claude_desktop_config.json` | `mcpServers` | `command` | dict |
| Claude Desktop(Windows) | `%APPDATA%\Claude\claude_desktop_config.json` | `mcpServers` | `command` | dict |
| Claude Desktop(Linux) | `~/.config/Claude/claude_desktop_config.json` | `mcpServers` | `command` | dict |
| Gemini CLI | `~/.gemini/settings.json` | `mcpServers` | `command` + `args` | dict |
| Cursor | `~/.cursor/mcp.json` | `mcpServers` | `command` | dict |
| Windsurf | `~/.codeium/windsurf/mcp_config.json` | `mcpServers` | `command` | dict |
| GitHub Copilot | `.vscode/mcp.json` | `servers` ⚠️ | `command` + `args` | dict |
| Cline | `~/.cline/mcp.json` | `mcpServers` | `command` + `args` | dict |
| Antigravity | 各不相同 | 各不相同 | | |

这还没算上 Relay AI / 3P 变体,就已经是 9 个路径 × 9 种 schema。**在这种规模下手动编辑非常容易出错**——路径写错、key 写错、漏掉 `mcpServers` 外层包装、忘记重启工具。

## `nlm setup add <client>` 接口

```bash
nlm setup add claude-code       # 每个工具一条命令
nlm setup add claude-desktop
nlm setup add gemini
nlm setup add cursor
nlm setup add windsurf
nlm setup add github-copilot
nlm setup add cline
nlm setup add antigravity
nlm setup add opencode
nlm setup add json              # 面向其他工具的向导

nlm setup list                  # 显示所有已检测到工具的状态
nlm setup remove claude-desktop --profile regular
```

对于不受支持的工具,`nlm setup add json` 是一个**交互式向导**:它会依次询问 uvx 还是 binary、完整路径还是名称、是否带 `mcpServers` 外层包装,然后把 JSON 片段打印出来并复制到剪贴板。

## 一些微妙但重要的行为

1. **只做路径检测,不做创建。** 如果配置路径本身不存在,该 CLI 会拒绝写入。它不会为某个工具引导创建一份全新的配置;它只修改已检测到的配置。(这一点很重要:它避免了 CLI 为用户尚未安装的工具创建半成品配置。)
2. **对 Claude Desktop 的多 profile 有感知。** Claude Desktop 同时存在两套并行 profile——`regular` 和 `Relay AI / 3P`。该 CLI 会自动检测两者并询问要面向哪一个(脚本场景下也可传入 `--profile regular|3p|both`)。
3. **对"进程正在运行"有感知。** Claude(以及其他一些工具)会在退出时重写自己的配置文件。如果 CLI 检测到 Claude 实例正在运行,它会**拒绝写入**,并要求用户先退出。否则改动会被覆盖掉。
4. **移除操作是有范围限定的。** 移除操作只会列出那些包含你的 server 名字或某个已识别的旧版条目的 profile/配置。同一配置文件中其他不相关的 MCP 不会被触碰。
5. **是 JSON 合并,不是整体覆盖。** CLI 使用字典更新(dict-update)语义合并进现有配置文件——已有的 MCP 条目会被保留,只新增这一个。

## 两条命令即完成安装

结合 `nlm login`,整个上手流程就是两条命令:

```bash
uv tool install notebooklm-mcp-cli   # 第 1 步:拿到二进制文件
nlm setup add claude-code            # 第 2a 步:接入 Claude Code
nlm login                           # 第 2b 步:认证
```

对比一下旧版 [[skills/notebooklm-mcp-setup]] 方案所需的步骤:

1. `uv tool install` ✓
2. `claude mcp add --global ...`,需要用对名称和 scope ← 容易出错
3. 如果第 2 步出问题,还要手动编辑 `~/.claude.json` ← 容易出错
4. 重启 Claude Code
5. `notebooklm-mcp-auth` 并粘贴 cookie ← 体验很差

`nlm setup add` 去掉了这五步中的三步。

## 这个模式可以泛化成什么

任何需要把自己安装进多个第三方工具的 CLI,都可以采用同样的模式:

- **N 个目标工具** × **M 种 schema 差异** × **K 种 profile 变体** → 每个目标一条 CLI 命令
- **先检测,后创建**(不要为未安装的工具引导创建配置)
- **目标进程运行时拒绝写入**(否则改动会被覆盖)
- **交互式 JSON 向导**作为不受支持工具的应急通道

`nlm setup add json` 这个向导尤其值得直接借鉴——它和 `gh auth login` 是同一种用户体验,能避免"把你工具的配置文件发给我看看"这种支持负担。

## 相关

- [[concepts/mcp-server-protocol-quirks]] — 这个模式所依托的底层 scope/JSON 差异问题
- [[entities/gemini-notebook-mcp-cli]] — 生产环境实现
- [[concepts/auth-status-semantics]] — 与之配套的 `nlm doctor`
- [[references/gemini-notebook-mcp-cli-tools]] — 同一个 CLI 的 43 工具参考卡
