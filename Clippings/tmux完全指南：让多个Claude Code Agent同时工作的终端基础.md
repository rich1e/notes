---
title: "tmux完全指南：让多个Claude Code Agent同时工作的终端基础"
source: "https://blog.csdn.net/qq_60735796/article/details/157912075"
author:
  - "[[qq_60735796]]"
published: 2026-02-09
created: 2026-08-05
description: "文章浏览阅读1.2w次，点赞36次，收藏38次。tmux完全指南：让多个Claude Code Agent同时工作的终端基础_claude code tmux"
tags:
  - "clippings"
---
## 1、前言

如果你已经了解了 Claude Code 的 **Agent Teams** 功能（多个 Claude 实例并行协作开发），那你一定会遇到一个非常实际的问题：

> **这些 Agent 在终端里到底怎么显示？我怎么同时看到它们各自在做什么？**

答案就是 **tmux** 。

Claude Code Agent Teams 有三种 Teammate 显示模式：

- **in-process** ：所有 Teammate 在同一个终端窗口内，用 `Shift+Up/Down` 切换查看（默认）
- **tmux** ：每个 Teammate 占据独立的 tmux pane，一目了然
- **iterm2** ：利用 iTerm2 的原生标签页（仅限 iTerm2 用户）

其中 **tmux 模式** 是最推荐的方案——它不依赖特定终端软件，任何 macOS/Linux 终端都能用，而且可以 **detach 后台运行** ，Agent 们会在你关掉终端后继续工作。

本文是一篇 **从零到实战** 的完整指南，目标是让你读完就能用 tmux 驾驭 Agent Teams。

## 2、tmux 是什么

### 2.1 一句话定义

tmux（ **T** erminal **MU** ltiple **X** er）是一个终端复用器，它允许你在一个终端窗口中运行多个终端会话，并且在断开连接后，会话依然保持运行。

### 2.2 为什么 Agent Teams 需要它

不用 tmux 的情况下，你启动 Agent Teams 后只能通过 `Shift+Up/Down` 在一个窗口内切换查看不同 Teammate 的状态，一次只能看一个。这就像看监控只有一个屏幕，要一个个切画面。

用了 tmux 之后：

```
┌─────────────────────┬──────────────────────┐
│  Team Lead          │  bridging-dev        │
│  (you talk here)    │  Creating files...   │
│                     │  ████████░░░ 80%     │
│  > engine-dev done  ├──────────────────────┤
│  > assigning test   │  engine-dev          │
│                     │  Task completed ✓    │
│                     ├──────────────────────┤
│                     │  utility-dev         │
│                     │  Writing tests...    │
└─────────────────────┴──────────────────────┘
```

每个 Agent 有自己独立的 pane，你可以 **同时看到所有 Agent 的工作状态** 。

### 2.3 tmux 的三大核心优势

| 优势 | 说明 |
| --- | --- |
| **多面板显示** | 一个屏幕同时看到 Lead + 所有 Teammates |
| **后台持久运行** | 关掉终端窗口 / SSH 断开，Agent 们继续工作 |
| **随时恢复** | `tmux a` 一条命令，立即回到之前的工作现场 |

## 3、macOS 从零安装

![[assets/804ebc19dfce48c88a6325d357a70ae1.png|在这里插入图片描述]]

### 3.1 安装 Homebrew（如果还没有）

Homebrew 是 macOS 的包管理器。打开 Terminal 运行：

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

安装完后验证：

```bash
brew --version
# Homebrew 4.x.x
```

> 如果你的 Mac 是 Apple Silicon（M1/M2/M3/M4），Homebrew 安装在 `/opt/homebrew` 。安装脚本会自动提示你添加 PATH， **务必按照提示操作** 。

### 3.2 安装 tmux

```bash
brew install tmux
```

验证：

```bash
tmux -V
# tmux 3.5a (or similar)
```

### 3.3 安装 Claude Code（如果还没有）

```bash
# 确保有 Node.js 18+
node -v

# 如果没有 Node.js
brew install node

# 安装 Claude Code
npm install -g @anthropic-ai/claude-code
```

验证：

```bash
claude --version
```

### 3.4 一键验证全部就绪

```bash
echo "=== Environment Check ===" && \
tmux -V && \
node -v && \
claude --version && \
echo "=== All Good! ==="
```

看到类似输出就说明一切就绪：

```asciidoc
=== Environment Check ===
tmux 3.5a
v22.13.0
1.0.33 (Claude Code)
=== All Good! ===
```

## 4、tmux 核心概念

这是理解 tmux 最重要的一节。tmux 的层级结构是：

```
Server
  └── Session（会话）
        └── Window（窗口）
              └── Pane（面板）
```

![[assets/b227bb7b5ee54eb5932a599a860c63df.png|在这里插入图片描述]]

### 4.1 Session（会话）

**Session 是 tmux 的最外层容器。**

- 一个 Session 可以包含多个 Window
- Session 可以被 detach（分离）—— 你关掉终端，Session 仍在后台运行
- 你可以随时 reattach（重新连接）到任何 Session

类比：Session 就像一个"工作空间"。你可以有一个叫 `tuck-dev` 的 Session 用于开发 Tuck 应用，另一个叫 `blog` 的 Session 用于写博客。

```bash
# 创建一个叫 tuck-dev 的 session
tmux new -s tuck-dev

# 列出所有 session
tmux ls

# 分离当前 session（session 继续运行）
# 快捷键：Ctrl+B d

# 重新连接到 tuck-dev
tmux a -t tuck-dev
```

### 4.2 Window（窗口）

**Window 是 Session 内的标签页。**

- 一个 Session 可以有多个 Window
- 底部状态栏显示所有 Window，带星号（\*）的是当前 Window
- 每个 Window 可以有自己的多个 Pane

类比：就像浏览器的标签页。你可以在一个标签页写代码，另一个标签页看日志。

### 4.3 Pane（面板）

**Pane 是 Window 内的分屏区域。**

- 一个 Window 可以水平/垂直分割为多个 Pane
- 每个 Pane 是一个独立的终端
- **Claude Code Agent Teams 的每个 Teammate 就运行在独立的 Pane 中**

这是和 Agent Teams 最直接相关的概念——当你启用 tmux 模式后，Claude Code 会自动为每个 Teammate 创建一个 Pane。

### 4.4 前缀键（Prefix Key）

tmux 的所有快捷键都需要先按 **前缀键** ，默认是 `Ctrl+B` 。

操作方式：

1. 按下 `Ctrl+B` （同时按住 Ctrl 和 B）
2. **松开**
3. 再按功能键

例如，要分屏：先按 `Ctrl+B` ，松开，再按 `"` （双引号）。

> 这和 Vim 的 leader key 概念类似。后文中的"Prefix"均指 `Ctrl+B` 。

## 5、tmux 动手实操

### 5.1 第一个 tmux Session

```bash
# 创建一个新 session（自动命名为 0）
tmux

# 或者，创建带名字的 session（推荐）
tmux new -s my-first
```

你会进入一个看起来和普通终端几乎一样的环境，唯一区别是底部多了一条 **绿色状态栏** 。

### 5.2 分屏操作

这是 tmux 最常用的功能：

```
# 水平分割（上下两半）
Ctrl+B "

# 垂直分割（左右两半）
Ctrl+B %
```

分割后的效果：

```
水平分割 (Ctrl+B "):        垂直分割 (Ctrl+B %):
┌──────────────────┐         ┌─────────┬─────────┐
│  Pane 0          │         │ Pane 0  │ Pane 1  │
├──────────────────┤         │         │         │
│  Pane 1          │         │         │         │
└──────────────────┘         └─────────┴─────────┘
```

### 5.3 在 Pane 之间切换

```
Ctrl+B ↑    # 切换到上方 pane
Ctrl+B ↓    # 切换到下方 pane
Ctrl+B ←    # 切换到左侧 pane
Ctrl+B →    # 切换到右侧 pane
```

当前活动的 Pane 的边框会高亮显示。

### 5.4 放大/缩小单个 Pane（Zoom）

当 Pane 太多导致每个都很小时：

```
Ctrl+B z    # 将当前 pane 放大到全屏
Ctrl+B z    # 再按一次，恢复原始布局
```

**这在 Agent Teams 中极其有用** ——你可以先通过方向键切换到某个 Teammate 的 Pane，然后 `Ctrl+B z` 放大查看它的详细输出，看完后再 `Ctrl+B z` 缩回去。

### 5.5 滚动查看历史输出

tmux 的 Pane 默认不能用鼠标滚轮滚动。要查看历史输出：

```
Ctrl+B [    # 进入滚动模式（Copy Mode）
```

进入后：

- 用 `↑/↓` 或 `PgUp/PgDn` 翻页
- 按 `q` 或 `Esc` 退出滚动模式

> 后面的配置章节会教你如何开启鼠标滚轮支持。

### 5.6 Detach 和 Reattach（核心技能）

这是 tmux 的杀手级特性：

```bash
# 分离（Detach）：当前 session 进入后台
Ctrl+B d

# 此时你回到了普通终端，但 tmux session 还在运行！

# 查看有哪些 session 在后台
tmux ls
# my-first: 1 windows (created Mon Feb  9 10:00:00 2026)

# 重新连接（Reattach）
tmux a -t my-first
# 一切回到你离开时的样子
```

**Agent Teams 场景** ：你启动了 3 个 Teammate 在干活， `Ctrl+B d` 分离后去喝杯咖啡。回来后 `tmux a` 重新连接，发现 Teammate 们已经写完了所有代码。

### 5.7 关闭和清理

```bash
# 关闭当前 pane
Ctrl+B x   # 会提示确认 y/n

# 关闭当前 window
Ctrl+B &   # 会提示确认

# 杀掉指定 session
tmux kill-session -t my-first

# 杀掉 tmux 服务（关闭所有 session）—— 谨慎使用
tmux kill-server
```

## 6、快捷键速查表

![[assets/925e35ad7ede47c5992df98bd7c40896.png|在这里插入图片描述]]

最高频使用的快捷键（建议背下来）：

| 快捷键 | 功能 | 使用场景 |
| --- | --- | --- |
| `Ctrl+B d` | Detach（分离） | 让 Agent 们在后台继续工作 |
| `Ctrl+B ↑↓←→` | 切换 Pane | 在 Lead 和 Teammates 之间切换 |
| `Ctrl+B z` | Zoom Pane | 放大查看某个 Teammate 的输出 |
| `Ctrl+B [` | 滚动模式 | 查看 Teammate 的历史输出 |
| `Ctrl+B "` | 水平分屏 | 手动创建新 Pane |
| `Ctrl+B %` | 垂直分屏 | 手动创建新 Pane |
| `Ctrl+B c` | 新建 Window | 创建新标签页（如监控用） |
| `Ctrl+B n/p` | 切换 Window | 在标签页间切换 |
| `Ctrl+B x` | 关闭 Pane | 清理不需要的 Pane |

> 记忆技巧： `d` =detach, `z` =zoom, `[`\=看(scroll), `"` =横线(水平分), `%` =竖线(垂直分)

## 7、tmux 配置优化

默认的 tmux 配置可以用，但不够好用。下面的配置专门为 Claude Code Agent Teams 场景优化。

### 7.1 创建配置文件

```bash
touch ~/.tmux.conf
```

### 7.2 推荐配置

将以下内容写入 `~/.tmux.conf` ：

```bash
# ============================================
# tmux config optimized for Claude Code Agent Teams
# ============================================

# --- 基础设置 ---
# 开启鼠标支持（可以用鼠标点击切换 pane、拖拽调整大小、滚轮翻页）
set -g mouse on

# 提高历史记录行数（Agent 输出可能很长）
set -g history-limit 50000

# 减少 Esc 键延迟（默认 500ms，太慢了）
set -sg escape-time 10

# 开启 256 色支持
set -g default-terminal "screen-256color"

# --- 状态栏美化 ---
# 状态栏位置
set -g status-position bottom

# 状态栏颜色
set -g status-style 'bg=#1a1a2e fg=#888888'

# 左侧：session 名称
set -g status-left '#[fg=#4ec9b0,bold] [#S] '
set -g status-left-length 20

# 右侧：时间
set -g status-right '#[fg=#666666] %H:%M '

# 当前 window 高亮
set -g window-status-current-style 'fg=#4ec9b0,bold'

# --- Pane 边框 ---
# 非活动 pane 边框颜色
set -g pane-border-style 'fg=#333333'
# 活动 pane 边框颜色（绿色高亮，方便识别当前 pane）
set -g pane-active-border-style 'fg=#4ec9b0'

# --- 便捷键绑定 ---
# Ctrl+B r 重新加载配置（修改配置后不用重启 tmux）
bind r source-file ~/.tmux.conf \; display-message "Config reloaded!"

# Ctrl+B | 垂直分屏（比 % 更直觉）
bind | split-window -h
# Ctrl+B - 水平分屏（比 " 更直觉）
bind - split-window -v

# Alt+Arrow 不用 prefix 直接切换 pane（更快）
bind -n M-Left select-pane -L
bind -n M-Right select-pane -R
bind -n M-Up select-pane -U
bind -n M-Down select-pane -D
```

### 7.3 让配置生效

```bash
# 方法一：如果你在 tmux 中
# 按 Ctrl+B 然后按 : 进入命令模式，输入：
source-file ~/.tmux.conf

# 方法二：如果你已经配置了 bind r（上面的配置里有）
# 直接 Ctrl+B r

# 方法三：重启 tmux（退出所有 session 后重新打开）
tmux kill-server
tmux new -s dev
```

### 7.4 配置后的效果

配置后的改善：

- **鼠标可以直接用了** ：点击切换 Pane，滚轮翻页，拖拽边框调整大小
- **Alt+方向键快速切换** ：不需要先按 Prefix，直接 `Alt+←→↑↓` 在 Pane 间跳转
- **`|` 和 `-` 更直觉的分屏** ：竖线 = 垂直分，横线 = 水平分
- **历史记录更长** ：5万行，足够查看 Agent 的完整输出
- **更好看的状态栏** ：暗色调配色，当前 pane 绿色高亮

## 8、Claude Code Agent Teams + tmux 实战

这是本文的核心章节。我们来完整走一遍 **从启用到看到 Agent 们在 tmux 中并行工作** 的全流程。

![[assets/2ab8b30fe3be4b24b4ec132d45997083.png|在这里插入图片描述]]

### 8.1 一次性配置（只需做一次）

#### 8.1.1 启用 Agent Teams 实验功能

```bash
# 添加到 ~/.zshrc（macOS 默认 shell）
echo 'export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1' >> ~/.zshrc
source ~/.zshrc
```

#### 8.1.2 配置 teammateMode 为 tmux

Claude Code 的设置文件在 `~/.claude/settings.json` 。如果文件不存在就创建：

```bash
# 查看是否已有配置
cat ~/.claude/settings.json 2>/dev/null || echo "文件不存在，需要创建"
```

编辑（或创建）这个文件，确保包含：

```json
{
  "teammateMode": "tmux"
}
```

> 如果你已经有其他配置项，只需要在 JSON 对象里添加 `"teammateMode": "tmux"` 即可。

#### 8.1.3 验证环境

```bash
# 确认环境变量已设置
echo $CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS
# 应该输出 1

# 确认 tmux 已安装
tmux -V

# 确认 Claude Code 可用
claude --version
```

### 8.2 启动 Agent Teams

#### 8.2.1 进入项目目录并启动 Claude Code

```bash
cd ~/your-project
claude
```

#### 8.2.2 用自然语言描述团队任务

启动 Claude Code 后，直接用自然语言告诉它你需要一个团队：

```
I need a team to build this project in parallel. Please create teammates:
- "bridging-dev" to implement the Bridging layer (PrivateAPIs.swift, BridgingHelpers.swift)
- "engine-dev" to build the MenuBarEngine core (ControlItemManager.swift)
- "utility-dev" to create utility extensions (NSScreen+Extensions.swift)

Read CLAUDE.md for project context. Each teammate should work on their assigned files only.
```

或者用中文也完全可以：

```
帮我创建一个开发团队来并行开发这个项目。需要3个teammate：
- "bridging-dev" 负责 Bridging 层代码
- "engine-dev" 负责引擎核心代码
- "utility-dev" 负责工具类扩展

请阅读 CLAUDE.md 了解项目上下文。每个 teammate 只修改自己负责的文件。
```

#### 8.2.3 Claude 开始创建团队

Claude Code（Lead Agent）收到你的请求后，会自动：

1. 创建 Shared Task List（ `~/.claude/tasks/` ）
2. 使用 `create_teammate` 工具为每个 Teammate 启动独立的 Claude Code 实例
3. 因为你配置了 `"teammateMode": "tmux"` ，每个 Teammate 会自动在新的 tmux pane 中打开

**此时你的终端会自动变成这样：**

```
┌───────────────────────────┬───────────────────────────┐
│ [Team Lead]               │ [bridging-dev]            │
│                           │                           │
│ Created team with 3       │ Reading CLAUDE.md...      │
│ teammates.                │ Starting on Bridging      │
│                           │ layer...                  │
│ Task #1 → bridging-dev    │                           │
│ Task #2 → engine-dev      │ Creating PrivateAPIs.swift│
│ Task #3 → utility-dev     │ ████████░░░░ 65%          │
│                           ├───────────────────────────┤
│ Waiting for teammates...  │ [engine-dev]              │
│                           │                           │
│                           │ Building ControlItem      │
│                           │ Manager.swift...          │
│                           │ ████░░░░░░░░ 30%          │
│                           ├───────────────────────────┤
│                           │ [utility-dev]             │
│                           │                           │
│                           │ Creating NSScreen+        │
│                           │ Extensions.swift...       │
│                           │ ██░░░░░░░░░░ 15%          │
│  You: _                   │                           │
└───────────────────────────┴───────────────────────────┘
```

**就是这么自动** ——你不需要手动分屏，Claude Code 会通过 tmux API 自动创建 Pane。

### 8.3 在 tmux 中观察和操作 Teammates

#### 8.3.1 切换到 Teammate 的 Pane

```
Ctrl+B →    # 切换到右侧 Teammate
Ctrl+B ↓    # 切换到下方 Teammate
Ctrl+B ←    # 切换回 Lead
```

如果你配置了 `Alt+方向键` （见第7章配置），可以直接：

```
Alt+→       # 更快地切换到右侧
Alt+↓       # 更快地切换到下方
```

#### 8.3.2 Zoom 查看某个 Teammate 的详细输出

```
# 1. 先切换到目标 Teammate 的 pane
Ctrl+B →

# 2. 放大该 pane 到全屏
Ctrl+B z

# 3. 查看完毕后，恢复原始布局
Ctrl+B z
```

#### 8.3.3 滚动查看 Teammate 的历史输出

```
# 1. 切换到目标 pane
# 2. 进入滚动模式
Ctrl+B [

# 3. 用 PgUp/PgDn 或方向键翻页
# 4. 按 q 退出滚动模式
```

#### 8.3.4 Detach 让所有 Agent 后台运行

这是 tmux 最强大的功能之一：

```
Ctrl+B d    # Detach
```

此时：

- 你回到了普通终端
- **但所有 Agent（Lead + Teammates）都还在运行！**
- 你可以关掉终端、合上笔记本，Agent 们继续工作

当你想回来查看进度时：

```bash
tmux a      # 重新连接到最近的 session
# 或者
tmux a -t session-name    # 连接到指定 session
```

### 8.4 Delegate 模式（让 Lead 专注协调）

在 Lead Agent 的 Pane 中，你可以按 `Shift+Tab` 进入 Delegate 模式：

```
Normal Mode → [Shift+Tab] → Delegate Mode → [Shift+Tab] → Auto-Accept Mode
     ↑                                                            │
     └──────────────────── [Shift+Tab] ───────────────────────────┘
```

**Delegate 模式下的 Lead 只能使用协调工具** （创建 Teammate、发送消息、更新任务），不能自己写代码。这可以防止 Lead “抢活”，确保它专注于分配和协调。

### 8.5 CLAUDE.md：Agent 间的共享上下文

**极其重要** ：Teammate 不会继承 Lead 的对话历史。它们启动后唯一的上下文来源是：

1. Lead 发给它们的 Task 描述
2. 项目根目录的 `CLAUDE.md` 文件

所以你必须在 `CLAUDE.md` 中写清楚项目的关键信息：

```markdown
# Project: Tuck (macOS Menu Bar Manager)

## Tech Stack
- Swift + SwiftUI (70%) + AppKit (30%)
- macOS 14+ deployment target
- Xcode 15+

## Architecture
- /Sources/Bridging/ → Private API wrappers (CGS, SkyLight)
- /Sources/Engine/ → MenuBarEngine core (ControlItemManager)
- /Sources/Utils/ → Extensions (NSScreen, NSStatusItem)

## Important Rules
- Each agent ONLY modifies files in their assigned directory
- Always run \`swift build\` before marking task as complete
- Use \`@MainActor\` for all UI-related code
- Never force unwrap optionals
```

Teammate 启动后会自动读取这个文件，获取项目上下文。

## 9、iTerm2 用户的额外选择

如果你使用 iTerm2（macOS 上最流行的第三方终端），有两个额外选项。

### 9.1 方案一：tmux - CC 控制模式

iTerm2 有一个独特的功能——可以将 tmux 的 Pane 映射为 iTerm2 的原生标签页和分屏：

```bash
tmux -CC
```

这会启动 tmux 的"控制模式"，iTerm2 会接管 tmux 的显示，把 tmux pane 变成 iTerm2 的原生 pane。好处是可以用 iTerm2 的鼠标操作和快捷键。

### 9.2 方案二：直接用 iterm2 模式

如果你不想折腾 tmux，可以直接在 `~/.claude/settings.json` 中设置：

```json
{
  "teammateMode": "iterm2"
}
```

这样 Claude Code 会直接在 iTerm2 中为每个 Teammate 创建新的标签页/分屏，完全不需要 tmux。

### 9.3 三种模式对比

| 特性 | in-process | tmux | iterm2 |
| --- | --- | --- | --- |
| 终端要求 | 任意 | 任意 + tmux | 仅 iTerm2 |
| 显示方式 | 同一窗口切换 | 独立 Pane | 原生标签页 |
| 同时看到所有 Agent | 不能 | 能 | 能 |
| 后台运行 | 不支持 | **支持** | 不支持 |
| SSH 远程场景 | 不支持 | **支持** | 不支持 |
| 配置复杂度 | 零 | 低 | 零 |

**推荐** ：

- 如果你是 **iTerm2 用户** 且不需要后台运行 → 选 `iterm2`
- 如果你需要 **后台运行** 或在 **远程服务器** 上使用 → 选 `tmux`
- 如果你只是想 **快速试试** → 用默认的 `in-process`

## 10、实战场景与高级技巧

### 10.1 场景一：启动 Agent Teams 后去吃饭

```bash
# 1. 启动 Claude Code，描述团队任务
cd ~/tuck-app
claude
# > "Create a team of 3 to implement Phase 1..."

# 2. 看到 Agent 们开始工作后
Ctrl+B d    # Detach

# 3. 去吃饭 🍜（Agent 们继续工作）

# 4. 回来后
tmux a      # 重新连接
# 所有 Agent 的输出都保留着，可以回滚查看
```

### 10.2 场景二：在远程服务器上运行 Agent Teams

```bash
# 本地 SSH 到远程服务器
ssh user@server

# 在服务器上启动 tmux
tmux new -s ai-dev

# 启动 Claude Code + Agent Teams
claude
# > "Create team..."

# SSH 断开后（网络不好、关电脑等）
# Agent 们在服务器上继续运行！

# 重新 SSH 后
ssh user@server
tmux a -t ai-dev
# 回到工作现场
```

### 10.3 场景三：用额外的 Window 做监控

```bash
# Agent Teams 在 Window 0 工作
# 你可以创建一个新 Window 来监控

Ctrl+B c    # 创建 Window 1

# 在 Window 1 中运行监控命令
watch -n 5 'git log --oneline -10'     # 监控 git 提交
# 或者
tail -f ~/project/build.log             # 监控构建日志

# 在两个 Window 间切换
Ctrl+B 0    # 回到 Agent Teams（Window 0）
Ctrl+B 1    # 看监控（Window 1）
```

### 10.4 技巧：调整 Pane 布局

当 Agent Teams 自动创建的布局不满意时：

```bash
# 在 tmux 中循环切换预设布局
Ctrl+B Space

# 预设布局包括：
# even-horizontal: 所有 pane 等宽水平排列
# even-vertical:   所有 pane 等高垂直排列
# main-horizontal: 一个大 pane 在上，其余在下
# main-vertical:   一个大 pane 在左，其余在右
# tiled:           网格排列
```

推荐 `main-vertical` ——左边大窗口给 Lead，右边小窗口给 Teammates。

### 10.5 技巧：给 Pane 命名（方便识别）

```bash
# 在 tmux 命令模式下（Ctrl+B :）
select-pane -T "bridging-dev"
```

或者在配置中启用 Pane 标题显示：

```bash
# 添加到 ~/.tmux.conf
set -g pane-border-status top
set -g pane-border-format " #{pane_title} "
```

这样每个 Pane 顶部会显示名字，一目了然。

## 11、常见问题排障

### 11.1 tmux session 残留（Agent 结束后 session 还在）

```bash
# 查看所有残留 session
tmux ls

# 杀掉不需要的 session
tmux kill-session -t session-name

# 杀掉所有（核弹级操作）
tmux kill-server
```

**预防** ：在 `~/.tmux.conf` 中添加：

```bash
# 当窗口内最后一个 pane 关闭时，自动关闭窗口
set -g remain-on-exit off
```

### 11.2 Teammate 没有出现在新的 Pane 中

可能的原因：

1. **`teammateMode` 没设对**
	```bash
	cat ~/.claude/settings.json
	# 确认有 "teammateMode": "tmux"
	```
2. **不在 tmux 环境内启动的 Claude Code**
	```bash
	# 错误：直接在普通终端启动
	claude
	# 正确：先进入 tmux，再启动 claude
	tmux new -s dev
	claude
	```
	> 注意：如果你已经设置了 `teammateMode: "tmux"` ，Claude Code 即使在普通终端启动，也会尝试调用 tmux 来创建 Pane。但为了最佳体验，建议先进入 tmux Session。
3. **环境变量没有生效**
	```bash
	echo $CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS
	# 如果为空，重新 source
	source ~/.zshrc
	```

### 11.3 Pane 空间不够（终端太小）

当 Teammate 多了，每个 Pane 都很小，看不清内容：

- **方法一** ：放大终端窗口（全屏）
- **方法二** ：用 `Ctrl+B z` Zoom 到需要看的 Pane
- **方法三** ： `Ctrl+B Space` 切换到更合适的布局
- **方法四** ：减少同时显示的 Pane 数，让部分 Teammate 在不同 Window 中

### 11.4 tmux 和 macOS 剪贴板不通

在 tmux 中复制内容时可能粘贴不到外面。解决方案：

```bash
# 安装 reattach-to-user-namespace（如果需要）
brew install reattach-to-user-namespace

# 或者，更简单的方案——开启鼠标支持后
# 按住 Option(Alt) 键 + 鼠标选择 = 使用终端原生选择（绕过 tmux）
# 然后 Cmd+C 复制
```

### 11.5 Prefix 键 Ctrl+B 和其他程序冲突

如果你习惯 Vim/Emacs 等工具， `Ctrl+B` 可能有冲突。可以改成 `Ctrl+A` ：

```bash
# 添加到 ~/.tmux.conf
unbind C-b
set -g prefix C-a
bind C-a send-prefix
```

> 改完后所有 “Ctrl+B” 操作变成 “Ctrl+A”。

## 12、总结

tmux 是使用 Claude Code Agent Teams 的 **最佳拍档** 。让我们回顾核心要点：

**安装 3 步走：**

```bash
brew install tmux                           # 安装
echo 'export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1' >> ~/.zshrc  # 启用
# 在 ~/.claude/settings.json 中添加 "teammateMode": "tmux"        # 配置
```

**日常使用 5 个快捷键：**

| 快捷键 | 你要做的事 |
| --- | --- |
| `Ctrl+B d` | “我先去忙别的，你们继续” |
| `tmux a` | “我回来了，让我看看进度” |
| `Ctrl+B ↑↓←→` | “让我看看这个 Teammate 在干嘛” |
| `Ctrl+B z` | “放大看看它写的代码” |
| `Ctrl+B [` | “往上翻翻它之前的输出” |

**核心认知：**

- tmux 的 Detach/Reattach 是 Agent Teams 后台运行的基础
- `CLAUDE.md` 是所有 Teammate 的共享上下文，务必写好
- 每个 Teammate 应该负责 **不同的文件** ，避免冲突
- Delegate 模式（ `Shift+Tab` ）让 Lead 专注协调，不"抢活"

如果你还没有用过 tmux，不要被快捷键吓到——实际上你日常只需要上面那 5 个。用两天就会变成肌肉 记忆 。

tmux + Claude Code Agent Teams，让你的终端变成一个 **并行 AI 开发工厂** 。