---
title: "Tmux × Claude Code Agent Teams 实战 — Pane 工作流与故障排查"
category: skills
tags:
  - tmux
  - claude-code
  - agent-teams
  - workflow
  - skills
summary: Claude Code Agent Teams 选 tmux 模式后的 pane 工作流：3 个 pane 操作技巧（zoom / detach / scroll）、CLAUDE.md 共享上下文协议、Delegate 模式防抢活、5 大常见故障排查（teammateMode 未生效、终端太小、prefix 冲突、剪贴板不通、session 残留）。
sources:
  - "https://blog.csdn.net/qq_60735796/article/details/157912075"
created: "2026-08-13T01:40:00Z"
updated: "2026-08-13T01:40:00Z"
provenance:
  extracted: 0.85
  inferred: 0.12
  ambiguous: 0.03
base_confidence: 0.6
lifecycle: draft
lifecycle_changed: "2026-08-13"
tier: supporting
relationships:
  - target: "[[concepts/agent-team-display-modes]]"
    type: extends
  - target: "[[concepts/tmux-config-importance-override]]"
    type: related_to
---

# Tmux × Claude Code Agent Teams 实战 — Pane 工作流与故障排查

> Claude Code Agent Teams 选 `teammateMode: "tmux"` 后的实战 skill：pane 操作 3 件套、CLAUDE.md 共享上下文、5 大故障排查。

## 一次性的环境配置

```bash
# 1. 启用 Agent Teams 实验功能
echo 'export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1' >> ~/.zshrc
source ~/.zshrc

# 2. 配置 teammateMode 为 tmux（持久化）
# 编辑 ~/.claude/settings.json
{
  "teammateMode": "tmux"
}

# 3. 验证环境
echo $CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS   # 输出 1
tmux -V                                      # 输出 tmux 3.x
claude --version                             # Claude Code 版本
```

## 启动 Agent Teams

```bash
# 1. 启动 tmux session（推荐先 tmux 再 claude）
tmux new -s ai-dev
cd ~/your-project
claude
```

在 Claude Code 内用自然语言下达团队任务：

```
Create a team to build this project in parallel:
- "bridging-dev" to implement the Bridging layer
- "engine-dev" to build the core engine
- "utility-dev" to create utility extensions

Read CLAUDE.md for project context. Each teammate should work on their assigned files only.
```

Claude Code 自动：
1. 创建 Shared Task List（`~/.claude/tasks/`）
2. 用 `create_teammate` 工具启动独立 Claude Code 实例
3. 每个 Teammate 在新 tmux pane 中打开

## 3 个高频 Pane 操作

| 操作 | 快捷键 | 场景 |
|---|---|---|
| **Zoom** | `Ctrl+B z` | 当前 pane 放大到全屏 → 再按一次恢复 |
| **Detach / Reattach** | `Ctrl+B d` / `tmux a -t <name>` | 让 Agent 在后台持续工作（关终端也不停） |
| **Scroll 历史** | `Ctrl+B [` → `↑/↓/PgUp/PgDn` → `q` 退出 | 查看 Teammate 的完整输出 |

**配合方向键切换 Pane**：`Ctrl+B ↑/↓/←/→` 在 Lead 与各 Teammate 之间跳。

## 推荐配置（`~/.tmux.conf`）

针对 Agent Teams 优化的关键项：

```bash
# 鼠标支持（点击切换、滚轮翻页、拖拽调大小）
set -g mouse on

# 历史行数（Agent 输出很长）
set -g history-limit 50000

# 减少 Esc 延迟（默认 500ms 太慢）
set -sg escape-time 10

# 256 色
set -g default-terminal "screen-256color"

# 状态栏 — 当前 window 绿色高亮
set -g status-style 'bg=#1a1a2e fg=#888888'
set -g window-status-current-style 'fg=#4ec9b0,bold'

# Alt+方向键不用 prefix 直接切 pane（更快）
bind -n M-Left  select-pane -L
bind -n M-Right select-pane -R
bind -n M-Up    select-pane -U
bind -n M-Down  select-pane -D

# | 垂直分，- 水平分（比 %/" 更直觉）
bind | split-window -h
bind - split-window -v

# Ctrl+B r 重载配置
bind r source-file ~/.tmux.conf \; display-message "Config reloaded!"
```

**重载配置**（无需重启 tmux）：`Ctrl+B r`。

## CLAUDE.md — Teammate 的唯一上下文

**关键约束**：Teammate **不会**继承 Lead 的对话历史。启动后它们能获取的上下文只有：

1. Lead 发给它们的 Task 描述
2. 项目根目录的 `CLAUDE.md`

→ **CLAUDE.md 是项目级共享上下文的唯一来源**，务必写清楚：

```markdown
# Project: Tuck (macOS Menu Bar Manager)

## Tech Stack
- Swift + SwiftUI (70%) + AppKit (30%)
- macOS 14+ deployment target
- Xcode 15+

## Architecture
- /Sources/Bridging/ → Private API wrappers
- /Sources/Engine/ → MenuBarEngine core
- /Sources/Utils/ → Extensions

## Important Rules
- Each agent ONLY modifies files in their assigned directory
- Always run `swift build` before marking task as complete
- Use `@MainActor` for all UI-related code
- Never force unwrap optionals
```

**Teammate 文件分工**必须明确 — 不同 Teammate 写不同的文件，否则互相 git conflict。

## Delegate 模式（防 Lead 抢活）

在 Lead Agent 的 pane 中按 `Shift+Tab` 三态切换：

```
Normal Mode → [Shift+Tab] → Delegate Mode → [Shift+Tab] → Auto-Accept Mode
     ↑                                                            │
     └──────────────── [Shift+Tab] ──────────────────────────────┘
```

**Delegate 模式**：Lead 只能用协调工具（创建 Teammate、发送消息、更新任务），**不能自己写代码**。这是防止 Lead 抢活、专注协调的关键。

## 三种模式的对比与选型

| 场景 | 推荐模式 |
|---|---|
| iTerm2 用户 + 不需要后台运行 | `"iterm2"` |
| 需要后台运行 / 远程服务器使用 | `"tmux"` |
| 快速试用 / 不想配置 | `"in-process"`（默认） |

详细5模式对比见 [[concepts/agent-team-display-modes]]。

## 5 大常见故障排查

### 1. Teammate 没出现在新 pane 中
检查3件事：
- `cat ~/.claude/settings.json` 确认 `"teammateMode": "tmux"` 已设
- 是否在 tmux session 内启动（先 `tmux new` 再 `claude`）
- 环境变量是否生效：`echo $CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` 应输出 `1`

### 2. tmux session 残留（Agent 结束后 session 还在）
```bash
tmux ls                                    # 查看所有 session
tmux kill-session -t session-name          # 杀掉指定 session
tmux kill-server                            # 杀掉所有（核弹级）
```
**预防**：在 `~/.tmux.conf` 中加 `set -g remain-on-exit off`。

### 3. Pane 空间不够（终端太小，Teammate 太多）
- 全屏终端窗口（`Cmd+Ctrl+F` iTerm2 / `Ctrl+B z` 放大单 pane）
- `Ctrl+B Space` 循环切换预设布局（`main-vertical` 推荐 — 左侧 Lead 大窗口，右侧 Teammates 小窗口）
- 减少同屏 Teammate 数，让部分在不同 Window 里（`Ctrl+B c` 新建 Window）

### 4. tmux 和 macOS 剪贴板不通
两种方案：
- `brew install reattach-to-user-namespace`
- 或开启 `set -g mouse on` 后，按住 `Option(Alt)` + 鼠标选择 = 用终端原生选择，绕过 tmux

### 5. Prefix 键 `Ctrl+B` 与其他程序冲突
改成 `Ctrl+A`（screen 风格）：
```bash
# ~/.tmux.conf
unbind C-b
set -g prefix C-a
bind C-a send-prefix
```

## 远程服务器场景

```bash
# 本地 ssh 到服务器
ssh user@server

# 服务器上启动 tmux + claude
tmux new -s ai-dev
claude
# > "Create team..."

# SSH 断开（网络不好、关电脑都行）
# Agent 在服务器上继续运行！

# 重新 SSH 后
ssh user@server
tmux a -t ai-dev    # 回到工作现场
```

→ **tmux 是远程服务器跑 Agent Teams 的必需前置**（SSH 断开不杀进程）。

## 相关页面

- [[concepts/agent-team-display-modes]] — 5 种 teammateMode 全景
- [[concepts/tmux-config-importance-override]] — gpakosz tmux 配置的 `#!important` 标记
- [[concepts/tmux-pane-maximize-stateful]] — gpakosz `<prefix> +` 跨 window 保留状态
- [[concepts/tmux-installer-safety-pattern]] — install.sh 安全设计