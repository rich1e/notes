---
title: "使用 gpakosz/.tmux — 安装、定制、热重载、卸载"
category: skills
tags:
  - tmux
  - gpakosz
  - dotfiles
  - terminal
  - how-to
sources:
  - https://github.com/gpakosz/.tmux
  - _raw/_archived/github-gpakosz-tmux.txt (gitingest export, gpakosz/.tmux master, 2026-08-03)
created: 2026-08-03T16:05:00Z
updated: 2026-08-03T16:05:00Z
summary: gpakosz/.tmux 实战用法:三步安装(自动/手动/manual)、改 `.tmux.conf.local` 走 `tmux_conf_*` 变量、`<prefix> r` 热重载、按 Powerline 字形换主题色、TMUX_CONF_LOCAL env 标记 active session、卸载只需 `rm` symlink + 备份。
tier: peripheral
lifecycle: draft
lifecycle_changed: "2026-08-03"
base_confidence: 0.85
provenance:
  extracted: 0.85
  inferred: 0.12
  ambiguous: 0.03
relationships:
  - target: "[[entities/gpakosz-tmux]]"
    type: extends
  - target: "[[concepts/tmux-local-override-pattern]]"
    type: uses
  - target: "[[concepts/tmux-installer-safety-pattern]]"
    type: uses
  - target: "[[skills/tmux]]"
    type: related_to
---

# 使用 gpakosz/.tmux

> "Manage your tmux like a pro, with sane defaults and one file to edit."
> —— 本页是 gpakosz 配置的"上手 + 定制 + 维护"实战。

## 1. 安装(三选一)

### 自动(推荐先演练)

```sh
# 演练:不写盘,只看会发生什么
DRY_RUN=1 curl -fsSL \
  "https://github.com/gpakosz/.tmux/raw/refs/heads/master/install.sh#$(date +%s)" \
  | PERMISSIVE=1 bash

# 正式
curl -fsSL \
  "https://github.com/gpakosz/.tmux/raw/refs/heads/master/install.sh#$(date +%s)" \
  | bash
```

脚本会发现 stdin 是 pipe,在 TTY 下弹出 [Yes/No/Cancel] review(见 [[concepts/tmux-installer-safety-pattern]])。

### 手动(完全可控)

```sh
cd ~
git clone --single-branch https://github.com/gpakosz/.tmux.git
ln -s -f .tmux/.tmux.conf           # 或 XDG 路径
cp .tmux/.tmux.conf.local ~/.tmux.conf.local
```

### XDG 路径

```sh
mkdir -p ~/.config/tmux
git clone --single-branch https://github.com/gpakosz/.tmux.git ~/.local/share/tmux/oh-my-tmux
ln -s ~/.local/share/tmux/oh-my-tmux/.tmux.conf ~/.config/tmux/tmux.conf
cp ~/.local/share/tmux/oh-my-tmux/.tmux.conf.local ~/.config/tmux/tmux.conf.local
```

> ⚠️ XDG 路径下,conf 文件名不带前导 `.`。

## 2. 热重载

```sh
<prefix> r
```

会 `source-file ~/.tmux.conf` —— 主 conf 重新 source → `.local` 重新 source。无需重连 session。

## 3. 编辑定制

永远改 `~/.tmux.conf.local`,不要改 `.tmux.conf`(主 conf 在仓库里,`git pull` 会覆盖)。

打开方式:

```sh
<prefix> e    # 用 $VISUAL / $EDITOR 编辑 ~/.tmux.conf.local
              # 默认 vim,见 README line 240
```

## 4. 关键 customization 点

| 变量 | 默认 | 作用 |
|---|---|---|
| `tmux_conf_preserve_stock_bindings` | `false` | 设为 `true` 保留 tmux 原生 bind |
| `tmux_conf_new_session_prompt` | `false` | `true` 时创建 session 弹 prompt 让命名 |
| `tmux_conf_new_session_retain_current_path` | `false` | 新 session 沿用当前路径 |
| `tmux_conf_new_window_retain_current_path` | `false` | 新 window 沿用当前路径 |
| `tmux_conf_new_pane_retain_current_path` | `true` | 新 pane 沿用当前路径 |
| `tmux_conf_new_pane_reconnect_ssh` | `false` | 远程 pane 自动重连 |
| `tmux_conf_theme_colour_1` … `colour_17` | 默认调色板 | 状态栏/Powerline 配色 |
| `tmux_conf_theme_highlight_focused_pane` | `false` | `true` 高亮当前 pane |
| `tmux_conf_theme_status_left` / `_right` | 见样本 | 状态栏自定义内容 |
| `tmux_conf_theme_left_separator_main` 等 | `''` 等 | Powerline 字形 |

> 完整列表见 `~/.tmux.conf.local` 里的注释样本,共约 30+ 变量。

## 5. 启用 Powerline 视觉

需要三步:

1. **字体**:装 `Source Code Pro`(自带 Powerline 字形)或用 [powerline/fonts](https://github.com/powerline/fonts) 给已有字体打补丁。
2. **设变量**(在 `.local`):
   ```sh
   tmux_conf_theme_left_separator_main=''
   tmux_conf_theme_left_separator_sub=''
   tmux_conf_theme_right_separator_main=''
   tmux_conf_theme_right_separator_sub=''
   ```
   (这些其实是默认值,问题通常是终端用错了字体导致字形变 □。)
3. `<prefix> r` 热重载。

## 6. 加 TPM 插件

`.local` 末尾:

```sh
set -g @plugin 'tmux-plugins/tpm'
set -g @plugin 'tmux-plugins/tmux-sensible'
set -g @plugin 'tmux-plugins/tmux-resurrect'
```

⚠️ **不要**写 `set -g @plugin 'tmux-plugins/tpm'`(README line 435 警告)也不要写 `run '~/.tmux/plugins/tpm/tpm'` —— gpakosz 主 conf 已自带这两块。

按键安装/卸载/更新:

| 操作 | 按键 |
|---|---|
| 安装 | `<prefix> I` |
| 卸载 | `<prefix> M-u` |
| 更新 | `<prefix> u` |

## 7. 状态栏加 wttr.in 天气

```sh
tmux_conf_theme_status_right='#{prefix}#{pairing}#{synchronized} #(curl -m 1 wttr.in?format=3 2>/dev/null; sleep 900) , %R , %d %b | #{username}#{root} | #{hostname} '
```

`#()` 是 tmux 调外部命令的语法。`sleep 900` 让网络请求最多每 15 分钟一次,无论 `status-interval` 多短。

## 8. 在已有 session 内重装

```sh
PERMISSIVE=1 curl ... | bash
```

不退出当前 server。⚠️ 主 conf 警告:已存在 session 里的 `TMUX_CONF`/`TMUX_CONF_LOCAL`/`TMUX_PROGRAM`/`TMUX_SOCKET` 环境变量已过时,新会话用新值,老会话可能不一致。

## 9. 卸载

```sh
rm ~/.tmux.conf ~/.tmux.conf.local
rm -rf ~/.local/share/tmux/oh-my-tmux    # XDG 路径
```

备份文件 `~/.tmux.conf.YYYYMMDDHHMMSS.PID` 不会被自动删,可手动清理。

## 10. `#!important` 解决冲突

```sh
# 用户在 .local 末尾
bind c new-window -c '#{pane_current_path}' #!important
```

主 conf 末尾 perl 阶段会把"含 `#!important` 的行"原样保留,不重写。详见 [[concepts/tmux-config-importance-override]]。

## 常见坑

| 症状 | 原因 | 解法 |
|---|---|---|
| `<prefix> +` maximize 还原失败 | `list-panes -s` 检测失败(用户改过 window name 模板) | 保留 `maximized` 子串在 window name 模板里 |
| 状态栏字体显示 □ | 终端字体不含 Powerline 字形 | 换字体或装 `powerline/fonts` |
| `<prefix> e` 打开空文件 | `$EDITOR` 未设置,fallback 失败 | `export EDITOR=vim` 或 `export VISUAL=nvim` |
| 改动 `.local` 不生效 | 忘了 `<prefix> r` 热重载 | `<prefix> r` 重新 source |
| `<prefix> BTab` 报 "no previous session" | 第一次运行只有 1 个 session | 创建第二个 session 再试 |
| Powerline 字形变 □ 但 vim 显示正常 | 终端"Use Unicode version 9" 选项冲突 | 关闭 iTerm2 该选项(gpakosz 故意避开 U9 变宽字符) |

## 相关页面

- 仓库本体:[[entities/gpakosz-tmux]]
- 双 prefix:[[concepts/tmux-prefix-double-binding]]
- `.local` 覆写模式:[[concepts/tmux-local-override-pattern]]
- 安装安全闸:[[concepts/tmux-installer-safety-pattern]]
- 键位记号 `B<Tab>`:[[concepts/tmux-key-notation-btab]]
- pane maximize 跨 window:[[concepts/tmux-pane-maximize-stateful]]
- 通用 tmux 速查:[[skills/tmux]]