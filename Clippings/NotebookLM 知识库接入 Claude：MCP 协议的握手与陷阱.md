---
title: NotebookLM 知识库接入 Claude：MCP 协议的握手与陷阱
source: https://joydig.com/notebooklm-mcp-server-claude-code/
author:
  - "[[Faith]]"
published: 2026-04-22
created: 2026-07-25
description: NotebookLM 擅长消化文档做问答，Claude 擅长推理和代码，但两者之间的内容搬运一直是手动操作。MCP 协议本应是桥梁，我搭了一座，发现桥面上有几处坑。 什么是 NotebookLM MCP Server？ NotebookLM 是 Google 推出的 AI
tags:
  - clippings
  - NotebookLM
  - Claude
  - MCP
---
NotebookLM 擅长消化文档做问答，Claude 擅长推理和代码，但两者之间的内容搬运一直是手动操作。MCP 协议本应是桥梁，我搭了一座，发现桥面上有几处坑。

## 什么是 NotebookLM MCP Server？

[NotebookLM](https://notebooklm.google.com/) 是 Google 推出的 AI 笔记工具，擅长对你上传的文档进行问答和总结，特别适合作为个人知识库。Claude 则在推理和代码能力上更强。两者各有所长，但以前要结合使用很麻烦——需要在两个工具之间反复切换、手动搬运内容。

[MCP（Model Context Protocol）](https://modelcontextprotocol.io/) 是 Anthropic 推出的开放协议，允许 AI 模型通过标准化接口调用外部工具和服务。 `notebooklm-mcp-server` 就是一个基于 MCP 的桥接服务，让 Claude 可以直接操作你的 NotebookLM 笔记本，包括列出笔记本、查询内容、添加资料源等。

## 安装步骤

### 第一步：安装 uv

`uv` 是一个现代 Python 工具管理器，比 `pip` 快很多，也更适合管理独立的命令行工具。

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

安装后重新加载 shell 环境，确认 `uv` 可用：

```
uv --version
```

### 第二步：安装 notebooklm-mcp-server

```
uv tool install notebooklm-mcp-server
```

安装完成后， `~/.local/bin/` 下会出现两个命令：

- `notebooklm-mcp` — MCP 服务器主程序
- `notebooklm-mcp-auth` — Google 账号认证工具

### 第三步：Google 账号认证

运行认证工具，按提示完成 Google 账号授权：

```
notebooklm-mcp-auth
```

认证成功后，凭据会保存在 `~/.notebooklm-mcp/auth.json` ，内容是你 Google 账号的 Cookie 信息。

### 第四步：将 MCP Server 添加到 Claude Code

这一步和网上大多数文章里写的 Claude Desktop 配置方法不同。我用的是 Claude Code（命令行版），配置方式如下：

```
claude mcp add --global notebooklm-mcp -- /home/your-username/.local/bin/notebooklm-mcp
```

**注意这里有两个关键点：**

1. **必须加 `--global` 参数** ，否则只对当前目录所在的项目生效（详见下面的坑）。
2. **建议使用绝对路径** ，避免因 `PATH` 环境变量差异导致 Claude Code 找不到命令。

## 踩坑记录

### 坑一：MCP Server 被配置成了项目级而非全局

按照文章操作完后，我发现 `notebooklm-mcp` 工具在某些项目的 Claude Code 会话里根本不出现。检查配置才发现，它被写到了 `aml_config` 这个特定项目的配置里，而不是全局配置。

**原因：** `claude mcp add` 命令默认是 **项目作用域** ，会把配置写入当时所在目录对应的项目条目里。我在 `aml_config` 目录下执行了这条命令，所以就只对那个项目生效了。

Claude Code 的配置作用域分两层，都存储在 `~/.claude.json` 里：

| 作用域         | 存储位置                          | 生效范围     |
| ----------- | ----------------------------- | -------- |
| 全局（global）  | 顶层 `mcpServers` 字段            | 所有项目和会话  |
| 项目（project） | `projects.<路径>.mcpServers` 字段 | 仅该目录下的会话 |

**解决方法：** 加上 `--global` 参数重新添加，或者直接编辑 `~/.claude.json` ，把配置挪到顶层 `mcpServers` 下。

### 坑二：在 $HOME 目录下操作也是项目级配置

这是一个很反直觉的地方。你可能以为在家目录 `~` 下运行 `claude mcp add` （不加 `--global` ）会写入某种"用户级"配置，毕竟家目录感觉很"全局"。

**但实际上不是。** Claude Code 对 `$HOME` 没有任何特殊处理，它就是一个普通目录。在 `~` 下执行 `claude mcp add` 不带 `--global` ，配置会被写成 `/home/your-username` 这个路径对应的项目级条目。

这和 git 的逻辑完全一样：在家目录下执行 `git config` （不加 `--global` ）是写到当前 repo 的 `.git/config` ，而不是 `~/.gitconfig` 。Claude Code 的 `mcp add` 遵循同样的规则——不加 `--global` 就永远是项目级，与目录无关。

## 验证连接

重启 Claude Code 后，在任意项目里发出指令，Claude 会自动调用 `notebook_list` 工具列出你的所有笔记本：

```
列出我 NotebookLM 里的所有笔记本
```

我的账号下共有 23 个笔记本，涵盖 Shell、Chromium 开发、Android 开发、AI 工具等方向，全部成功读取。

接下来可以直接问 Claude：

```
查询我的「Chromium Development」笔记本，总结一下里面关于渲染进程的内容
```

Claude 会调用 `notebook_query` 工具，基于笔记本里的实际资料给出回答，完全不需要手动搬运内容。

## notebooklm-mcp 支持的能力

除了最基本的读取查询，这个 MCP Server 还支持相当多的操作：

- **笔记本管理** ：创建、删除、重命名笔记本
- **资料源管理** ：添加网页 URL、YouTube 视频、Google Drive 文档、粘贴文本
- **AI 查询** ：对笔记本内容提问，支持多轮对话
- **Studio 内容生成** ：生成音频摘要、视频概览、信息图、幻灯片、报告、闪卡、测验、思维导图
- **深度研究** ：联网搜索或搜索 Google Drive，自动导入相关资料源

## 总结

整体安装过程不复杂，主要就是安装、认证、配置三步。最需要注意的就是 `claude mcp add` 的作用域问题——加 `--global` 才是真正的全局配置，在哪个目录下操作都不影响。

配置完成后，NotebookLM 作为知识存储库、Claude Code 作为分析推理引擎，两者通过 MCP 协议无缝协作，工作流的连贯性确实提升了不少。