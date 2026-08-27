---
title: Herdr — AI Agent 感知终端工作区管理器
category: entities
tags:
  - tools
  - cli
  - ai-agents
  - tmux
summary: 鼠标优先、Agent 状态感知的终端复用器，后台服务器持有所有进程，专为 Claude/Codex 等编码 Agent 设计。
sources:
  - https://herdr.dev/agent-guide.md
  - https://raw.githubusercontent.com/herdrdev/herdr/master/skills/herdr/SKILL.md
created: 2026-08-24T10:40:00Z
updated: 2026-08-24T10:40:00Z
tier: supporting
lifecycle: draft
lifecycle_changed: "2026-08-24"
base_confidence: 0.75
provenance:
  extracted: 0.90
  inferred: 0.10
  ambiguous: 0.00
---

# Herdr — AI Agent 感知终端工作区管理器

Herdr 是一个终端工作区管理器，以鼠标优先、Agent 状态感知为核心，后台服务器持有所有终端进程，断开连接后 pane 持续运行。

## 核心概念层级

| 层级 | 含义 |
|---|---|
| **Session** | 后台服务器命名空间 |
| **Workspace** | 项目级容器，侧边栏实时汇总 Agent 状态 |
| **Tab** | Workspace 内的布局单元 |
| **Pane** | 真实终端，可拆分，断连后存活 |
| **Agent** | 被识别的进程，状态：`working` / `blocked` / `done` / `idle` / `unknown` |

## 安装

```bash
# macOS（推荐）
brew install herdr

# Linux/macOS 脚本安装
curl -fsSL https://herdr.dev/install.sh | sh
```

验证安装：`herdr --version`

## 第一次使用

1. `cd` 进入项目目录，运行 `herdr`（自动创建 workspace）
2. 启动 Agent（如 `claude`），侧边栏自动检测状态
3. 先用**鼠标**：点击、拖拽边框、右键菜单
4. 分割 pane：`prefix+v`（右分）/ `prefix+-`（下分）；新建 tab：`prefix+c`
5. 断开：`prefix+q` 或关终端——一切继续运行；重连执行 `herdr`
6. 完全停止：`herdr server stop`

> **重要**：若 `HERDR_ENV=1` 已设置，说明已在 Herdr pane 内，跳过第 1 步，不支持嵌套启动。

## 与 tmux 的关系

- **不可在 tmux 内嵌套运行**：两者定位相同（终端复用），`ctrl+b` 前缀键会冲突
- **不是 tmux**：不支持 tmux 命令，`.tmux.conf` 语法无效
- 取舍：Herdr 对 AI Agent 状态原生感知；tmux 生态更成熟，vault 已有大量配置经验

## 给 Claude Code 安装控制 Skill

```bash
npx skills add herdrdev/herdr --skill herdr -g
```

安装后 Claude Code 可通过 `herdr` CLI 控制终端环境：分割 pane、启动 Agent、读取输出、发送按键。

### 核心 CLI 操作

```bash
# 查看当前状态
herdr workspace list
herdr pane current --current
herdr agent list

# 分割 pane（后台不抢焦点）
herdr pane split --current --direction right --cwd "$PWD" --no-focus

# 在其他 pane 运行命令
herdr pane run <pane-id> "npm test"
herdr pane read <pane-id> --source recent-unwrapped --lines 120

# 控制另一个 Agent
herdr agent start reviewer --kind codex --pane <pane-id>
herdr agent prompt reviewer "Review this PR." --wait --timeout 120000
```

### 前置条件

Claude Code 使用 Herdr Skill 必须在 Herdr pane 内运行：

```bash
test "${HERDR_ENV:-}" = 1  # 验证是否在 Herdr 环境中
```

正确启动顺序：先运行 `herdr` → 在 Herdr pane 内启动 `claude`。

## 配置

- 位置：`~/.config/herdr/config.toml`
- 查看默认配置：`herdr --default-config`
- 热重载：`herdr server reload-config`

## 常见问题

| 问题 | 解决方法 |
|---|---|
| Agent 未被检测 | `herdr agent list` / `herdr agent explain <target> --json` |
| 快捷键无响应 | 被 OS/终端拦截；`prefix+?` 查看全部活绑定 |
| 启动/socket 问题 | `herdr status` / 检查 `~/.config/herdr/` 日志 |
| 远程使用 | `herdr --remote <host>` |

## Related

- [[skills/zellij-terminal-multiplexer]] — 同类现代化终端复用器（Rust，tmux 友好替代）
- [[entities/gpakosz-tmux]] — tmux 生态成熟配置方案
- [[skills/tmux-agent-teams-pane-workflow]] — Claude Code Agent Teams tmux 模式实战
- [[concepts/tmux-pane-split-for-agents]] — tmux split-pane 多 Agent 配置
