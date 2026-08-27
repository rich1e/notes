---
title: Tmux 快速参考
category: skills
tags:
  - tmux
  - cli
  - tools
summary: Tmux 终端复用器快捷键速查、配置要点及插件管理，适用于 Tmux 2.3+。
sources:
  - https://gist.github.com/ryerh/14b7c24dfd623ef8edc7
created: 2026-06-29
updated: 2026-08-05T03:30:00Z
tier: supporting
lifecycle: draft
lifecycle_changed: "2026-06-29"
base_confidence: 0.67
provenance:
  extracted: 0.95
  inferred: 0.04
  ambiguous: 0.01
relationships:
  - target: "[[skills/claude-code-settings]]"
    type: related_to
  - target: "[[skills/terminal-music]]"
    type: related_to
  - target: "[[skills/zellij-terminal-multiplexer]]"
    type: related_to
  - target: "[[concepts/tmux-pane-split-for-agents]]"
    type: related_to
  - target: "[[skills/tmux-join-pane-swap-pane]]"
    type: extended_by
  - target: "[[concepts/tmux-pane-layout-rearrangement]]"
    type: related_to
---

# Tmux 快速参考

> 适用于 Tmux 2.3+。前缀键默认为 `Ctrl+b`（下文简写为 `PREFIX`）。

## 基本命令

```bash
tmux [new -s 会话名 -n 窗口名]   # 新建会话
tmux at [-t 会话名]              # 恢复会话
tmux ls                          # 列出所有会话
tmux kill-session -t 会话名      # 关闭会话
```

## 关闭会话的其他方式

除了 `tmux kill-session -t 会话名` 之外，还有 4 种关闭会话的替代方式：

```bash
tmux kill-server                 # 杀掉整个 tmux server（所有 session 一起关闭）
tmux kill-session -a             # 关闭除当前 session 之外的全部
tmux kill-session -a -t 目标名   # 关闭除指定 session 之外的全部
```

**命令行模式：** 在 PREFIX 提示符下输入 `:kill-session`，等价于关闭当前 session。

**级联关闭：** 在 pane 内执行 `exit`（或按 `Ctrl+d`）退出 shell 时——若这是当前 window 的最后一个 pane，window 自动关闭；若这是当前 session 的最后一个 window，session 自动关闭。这是"清空"会话最自然的方式。

> ⚠️ 注意 `PREFIX d` 只是**脱离**（detach）—— session 在后台保持运行，并未被关闭。

## 会话操作（PREFIX 后）

```
:new<回车>   启动新会话
s            列出所有会话
$            重命名当前会话
d            退出 tmux（后台保持运行）
```

## 窗口操作

```
c   创建新窗口
w   列出所有窗口
n   下一个窗口
p   上一个窗口
f   查找窗口
,   重命名当前窗口
&   关闭当前窗口
```

调整窗口排序：
```
swap-window -s 3 -t 1   交换 3 号和 1 号窗口
move-window -t 1        移动当前窗口到 1 号
```

## 窗格操作

```
%   垂直分割
"   水平分割
o   交换窗格
x   关闭窗格
q   显示窗格编号（出现时按数字选中）
z   切换窗格最大化/最小化
{   与上一个窗格交换位置
}   与下一个窗格交换位置
空格 切换布局
```

调整尺寸：
```
PREFIX : resize-pane -D 20   当前窗格向下扩大 20 格
PREFIX : resize-pane -t 2 -L 20   编号 2 的窗格向左扩大 20 格
```

同步所有窗格输入：
```
PREFIX : setw synchronize-panes
```

## 文本复制模式

`PREFIX + [` 进入，`PREFIX + ]` 粘贴。

建议开启 Vi 模式（`.tmux.conf`）：
```
setw -g mode-keys vi
```

Vi 模式常用键：`h/j/k/l`（移动）、`w/b`（逐词）、`Space`（开始选中）、`Enter`（复制）、`q`（退出）

## 推荐配置（~/.tmux.conf）

```bash
# 修改前缀键为 Ctrl+z（与 Vim 冲突少）
set -g prefix C-z

set -g base-index         1      # 窗口从 1 开始编号
set -g display-panes-time 10000  # PREFIX-Q 显示时长（ms）
set -g mouse              on     # 开启鼠标支持
set -g pane-base-index    1      # 窗格从 1 开始编号
set -g renumber-windows   on     # 关闭窗口后重排编号

setw -g allow-rename      off    # 禁止进程修改窗口名
setw -g automatic-rename  off    # 禁止自动命名
setw -g mode-keys         vi     # 复制模式使用 Vi 键位
```

## 插件管理（TPM）

```bash
git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm
bash ~/.tmux/plugins/tpm/bin/install_plugins
```

推荐插件：

| 插件 | 功能 |
|------|------|
| `tmux-plugins/tmux-resurrect` | 持久化保存/恢复会话 |
| `tmux-plugins/tmux-sensible` | 合理默认配置 |
| `tmux-plugins/tmux-yank` | 系统剪贴板集成 |
| `tmux-plugins/tmux-pain-control` | 窗格操作快捷键增强 |
| `seebi/tmux-colors-solarized` | Solarized 配色 |

## 状态栏配置示例

```bash
set -g status-right '#{prefix_highlight} #H | %a %Y-%m-%d %H:%M'
set -g @prefix_highlight_show_copy_mode 'on'
```

## 相关页面

- [[skills/claude-code-settings]] — Tmux 与 Claude Code session 配合使用
- [[skills/terminal-music]] — 终端中优雅听歌
- [[skills/zellij-terminal-multiplexer]] — tmux 友好的现代替代：Rust 写、YAML 布局、状态栏开箱即用
