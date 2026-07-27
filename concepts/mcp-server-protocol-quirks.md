---
title: MCP Server 作用域陷阱 — `claude mcp add --global` 的两层存储
category: concepts
tags:
  - mcp
  - claude-code
  - concept
summary: claude mcp add 默认是项目级，写入 projects.<path>.mcpServers；只有 --global 才落顶层 mcpServers。$HOME 目录不会被特殊处理，规则与 git config 一致。
sources:
  - https://joydig.com/notebooklm-mcp-server-claude-code/
created: 2026-07-26
updated: 2026-07-26
tier: supporting
lifecycle: draft
lifecycle_changed: "2026-07-26"
base_confidence: 0.55
provenance:
  extracted: 0.92
  inferred: 0.05
  ambiguous: 0.03
relationships:
  - target: "[[skills/claude-code-settings]]"
    type: related_to
  - target: "[[skills/notebooklm-mcp-setup]]"
    type: related_to
---

# MCP Server 作用域陷阱 — `claude mcp add --global` 的两层存储

> Claude Code 配置 `~/.claude.json` 中 MCP server 存储分两层：顶层 `mcpServers`（全局）vs `projects.<路径>.mcpServers`（项目级），**`$HOME` 不被特殊处理**，规则与 `git config` 一致。

## 两层存储结构

| 作用域 | 路径 | 生效范围 | 触发方式 |
|--------|------|----------|----------|
| **全局（global）** | `~/.claude.json` → 顶层 `mcpServers` | 所有项目、所有会话 | `claude mcp add --global` |
| **项目（project）** | `~/.claude.json` → `projects.<项目路径>.mcpServers` | 仅该目录下的会话 | `claude mcp add`（默认） |

## 陷阱 1：默认是项目级

`claude mcp add <name> -- <command>` **默认**写入当时所在目录对应的项目条目。这意味着：

```bash
cd ~/projects/aml_config
claude mcp add notebooklm-mcp -- /home/$USER/.local/bin/notebooklm-mcp
# 这条配置只对 ~/projects/aml_config 目录下启动的 Claude Code 生效
```

症状：MCP server 在某些项目里**根本不出现**，但其他项目里正常。

## 陷阱 2：`$HOME` 不是"用户级"配置

最反直觉的点——你以为在 `~` 下执行 `claude mcp add` 会写到"用户级"配置（毕竟家目录感觉很"全局"），但**不是**。

```bash
cd ~
claude mcp add notebooklm-mcp -- /home/$USER/.local/bin/notebooklm-mcp
# 实际写出 /home/$USER 这条路径对应的项目级条目
# 不影响 ~/projects/other-project 下的会话
```

**类比 git**：

```bash
git config user.email "foo@bar"          # 写入当前 repo 的 .git/config
git config --global user.email "foo@bar" # 写入 ~/.gitconfig
```

Claude Code 的 `mcp add` 遵循同样规则——**没有 `--global` 就永远是项目级，与目录无关**。

## 解决方法

**方案 A：用 `--global`（推荐）**

```bash
claude mcp add --global notebooklm-mcp -- /home/$USER/.local/bin/notebooklm-mcp
```

**方案 B：手动迁移配置**

编辑 `~/.claude.json`，把 `projects.<某路径>.mcpServers.notebooklm-mcp` 移到顶层 `mcpServers`：

```json
{
  "mcpServers": {
    "notebooklm-mcp": {
      "command": "/home/$USER/.local/bin/notebooklm-mcp"
    }
  },
  "projects": {
    "/home/$USER/projects/aml_config": {
      "mcpServers": {}   // 清空
    }
  }
}
```

**方案 C：删除项目级条目后重新加全局**

```bash
# 1. 编辑 ~/.claude.json 删除 projects.<path>.mcpServers
# 2. 重新执行
claude mcp add --global notebooklm-mcp -- /home/$USER/.local/bin/notebooklm-mcp
```

## 验证 MCP server 当前作用域

```bash
# 列出当前可用 MCP servers
claude mcp list
```

或直接看 `~/.claude.json`：

```bash
cat ~/.claude.json | python3 -c "
import json, sys
d = json.load(sys.stdin)
print('全局 mcpServers:')
for k in d.get('mcpServers', {}):
    print(f'  - {k}')
print()
print('项目级 mcpServers:')
for p, v in d.get('projects', {}).items():
    if v.get('mcpServers'):
        print(f'  {p}:')
        for k in v['mcpServers']:
            print(f'    - {k}')
"
```

## 为什么设计成项目级默认

- 大多数 MCP server 是项目专属（项目内的开发工具、项目定义的 API）
- 防止全局污染——避免装一个工具就全局生效
- 与 git config 默认项目级保持一致（降低认知负担）

代价：**理解 `--global` 的语义**成为上手 MCP 的必修课。

## 与 settings.json 的作用域层级对比

详见 [[skills/claude-code-settings]]：

| 配置 | 层级 | 触发 |
|------|------|------|
| settings.json | Managed / Local / Project / User 四级 | `--settings` 标志或编辑对应文件 |
| mcpServers | Global / Project 两级 | `--global` 标志 |
| CLAUDE.md | User / Project / Local 三级 | 文件位置 |

MCP 是**最简化的两层**——理解这点可避免 90% 的"MCP 装上不生效"问题。

## 相关页面

- [[skills/notebooklm-mcp-setup]] — NotebookLM MCP 完整安装流程
- [[skills/claude-code-settings]] — Claude Code 完整配置作用域
