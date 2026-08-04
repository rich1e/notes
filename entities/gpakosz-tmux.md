---
title: "gpakosz/.tmux — Oh my tmux! 配置仓库"
category: entities
tags:
  - tmux
  - dotfiles
  - terminal
  - multiplexer
  - configuration
  - gpakosz
sources:
  - https://github.com/gpakosz/.tmux
  - _raw/_archived/github-gpakosz-tmux.txt (gitingest export, gpakosz/.tmux master, 2026-08-03)
created: 2026-08-03T16:05:00Z
updated: 2026-08-03T16:05:00Z
summary: gpakosz 自 2012 年维护的"自洽、美观、多用"tmux 配置:Powerline 视觉主题、双 prefix (`C-b`/`C-a`)、`<prefix> +` 跨 window 保留状态的 pane maximize、可热重载的 `.tmux.conf.local` 覆写层、WTFPLv2 + MIT 双协议。
tier: supporting
lifecycle: draft
lifecycle_changed: "2026-08-03"
base_confidence: 0.9
provenance:
  extracted: 0.9
  inferred: 0.08
  ambiguous: 0.02
relationships:
  - target: "[[concepts/tmux-prefix-double-binding]]"
    type: derived_from
  - target: "[[concepts/tmux-local-override-pattern]]"
    type: uses
  - target: "[[concepts/tmux-key-notation-btab]]"
    type: related_to
  - target: "[[concepts/tmux-pane-maximize-stateful]]"
    type: uses
  - target: "[[concepts/tmux-config-importance-override]]"
    type: uses
  - target: "[[concepts/tmux-installer-safety-pattern]]"
    type: derived_from
  - target: "[[skills/tmux-gpakos-config]]"
    type: related_to
  - target: "[[skills/tmux]]"
    type: extends
---

# gpakosz/.tmux — Oh my tmux!

> Gregory Pakosz(@gpakosz)自 2012 年起维护的"自洽、美观、多用"tmux 配置仓库,标语 _"made with ❤️"_。仓库极简(8 文件,~150KB),但提供了 Powerline 视觉主题、双 prefix、跨 window 保留的 pane maximize、可热重载覆写层等大量工程化设计。

## 仓库结构

```
gpakosz/.tmux/
├── .tmux.conf           # 主配置 —— 用户不该改
├── .tmux.conf.local     # 用户覆写层 —— 所有定制在这里
├── install.sh           # 安全安装脚本(dry-run + 备份 + anti-piping)
├── README.md
├── LICENSE.MIT
├── LICENSE.WTFPLv2      # 双协议
└── .github/funding.yml
```

单一可执行文件 + 双 conf 文件,把所有"配置"集中在两个文件里,而**强约束用户只能改 `.local`**(README 有🚨标记反复提醒)。

## 核心设计

| 设计 | 一句话 | 详见 |
|---|---|---|
| **双 prefix** | `C-b`(默认)+ `C-a`(GNU Screen 兼容)同时可用 | [[concepts/tmux-prefix-double-binding]] |
| **`.local` 覆写层** | 主 conf 不可改,所有 customization 走 `tmux_conf_*` 变量 | [[concepts/tmux-local-override-pattern]] |
| **键位记号约定** | `B<Tab>` = `<prefix> Tab`,`B<C-c>` = `<prefix> C-c` | [[concepts/tmux-key-notation-btab]] |
| **`<prefix> +` maximize pane** | 比内置 `resize-pane -Z` 更强:maximize 到新 window 后还能继续 split,跨 window 保留状态 | [[concepts/tmux-pane-maximize-stateful]] |
| **`#!important` 覆写** | 在 `.local` 用 `#!important` 强制覆写被主 conf 抢走的 bind/set | [[concepts/tmux-config-importance-override]] |
| **install.sh 安全设计** | dry-run / 备份现 config / 拒绝 root / 拦截 stdin piping | [[concepts/tmux-installer-safety-pattern]] |

## Features 速览(README 列出)

- `C-a` secondary prefix,`C-b` 默认 prefix 同时生效
- Powerline 风格视觉主题
- `<prefix> +` maximize pane 到新 window
- `<prefix> m` 切换 mouse mode(自动切 copy-mode 选文本)
- 状态栏:电池百分比/横条、uptime、SSH/Mosh 感知 hostname、wttr.in 天气(用 `sleep 900` 节流)
- 可选高亮 focused pane
- SSH/Mosh 感知 pane 分割(自动重连远程)
- 剪贴板集成(`xsel`/`xclip`/`wl-copy` on Linux)
- Unicode `\uXXXX` / `\UXXXXXXXX` 转义支持
- PathPicker / Urlscan / Urlview 集成(若可用)
- TPM 插件管理(`<prefix> I` 安装 / `<prefix> M-u` 卸载 / `<prefix> u` 更新)

## 安装

**自动:**
```sh
curl -fsSL "https://github.com/gpakosz/.tmux/raw/refs/heads/master/install.sh#$(date +%s)" | bash
```
(脚本会拦截 stdin piping,要求在 TTY 下确认)

**手动:**
```sh
git clone --single-branch https://github.com/gpakosz/.tmux.git
ln -s -f .tmux/.tmux.conf ~/.tmux.conf       # 或 XDG 路径
cp .tmux/.tmux.conf.local ~/.tmux.conf.local
```

## 版本历史(README 与 install.sh 时间戳佐证)

- **2012** —— Gregory Pakosz 起始,Copyright 2012—
- 至今持续维护,master 分支活跃

## 协议

**WTFPLv2 + MIT dual license**,原作者声明无任何保证(见两个 LICENSE 文件)。

## 与 vault 已有页的关系

- 扩展 [[skills/tmux]] —— 后者是通用速查,本页是 gpakosz 这套具体配置
- 互补 [[skills/zellij-terminal-multiplexer]] —— 同类(终端复用器)但 Rust/YAML 实现
- [[concepts/terminal-music]] / [[skills/claude-code-settings]] —— 上层"tmux 在哪个工作流里用"

## 相关

- 仓库:[github.com/gpakosz/.tmux](https://github.com/gpakosz/.tmux)
- 自述:[README.md](https://github.com/gpakosz/.tmux/blob/master/README.md)
- 配套 vim 配置:[github.com/gpakosz/.vim](https://github.com/gpakosz/.vim.git)