---
title: "Tmux `#!important` 覆写标记 — 解决 `.local` bind/set 被主 conf 抢走的冲突"
category: concepts
tags:
  - tmux
  - configuration
  - override
  - gpakosz
sources:
  - https://github.com/gpakosz/.tmux
  - _raw/_archived/github-gpakosz-tmux.txt (gitingest export, gpakosz/.tmux master, 2026-08-03)
created: 2026-08-03T16:05:00Z
updated: 2026-08-03T16:05:00Z
summary: gpakosz 设计:`.local` 里写 `bind c new-window -c '#{pane_current_path}' #!important`,主 conf 用 perl sed 在 `bind`/`set` 行尾追加 `#!important` 后,会在 source 阶段被改写成"提前插入"到主 conf 之前,达到用户绑定"赢"的目的。
tier: supporting
lifecycle: draft
lifecycle_changed: "2026-08-03"
base_confidence: 0.78
provenance:
  extracted: 0.6
  inferred: 0.32
  ambiguous: 0.08
relationships:
  - target: "[[entities/gpakosz-tmux]]"
    type: derived_from
  - target: "[[concepts/tmux-local-override-pattern]]"
    type: extends
---

# Tmux `#!important` 覆写标记

> README Troubleshooting 第 127-137 行教用户的招式:在 `.local` 末尾加 `#!important`,让被主 conf 抢走的 `set` / `bind` 反过来赢。

## 用户视角的写法

```sh
# 在 ~/.tmux.conf.local 里
bind c new-window -c '#{pane_current_path}' #!important
set -g default-terminal "screen-256color"    #!important
```

不加 `#!important` 时,主 conf 后执行的同名 `bind c new-window` 会覆盖用户配置 —— 用户以为生效实际没生效。加 `#!important`,用户的版本"赢"。

## 主 conf 内部如何吃这个标记

`.tmux.conf` 第 1050-1133 行,有一个**生成最终 tmux 配置**的 perl 流:

```sh
tmux list-keys | awk '!/TMUX_CONF_LOCAL/ && /new-window|split[-_]window|new-session|copy-selection|copy-pipe/' > "$cfg"
```

然后是一连串 `perl -p -i -e '...'` 对 `$cfg`(生成的最终配置)做 sed 替换:

```perl
# 大致意图(简化)
perl -p -i -e "s/\\bcommand-prompt -p new-session \"new-session -s '%%'\"/new-session/g" "$cfg"
```

这一阶段会**重写**用户的 `new-session` 等命令。在用户的 `.local` 里加 `#!important`,本质是给 perl sed 一个"跳过这条重写"的锚点 —— 让用户原文进最终 cfg。

## 推断的关键细节(^[inferred])

README 没给 perl 流程图,代码也没把 `#!important` 处理写得像下面这样干净,但从脚本命名/上下文反推:

- `#!important` 后缀被识别为"原文保留、不被 perl sed 改写"
- `#!important` 紧跟命令最后一个参数之后,作为 tmux 的合法注释(tmux 会忽略 `#` 后内容)
- 主 conf 内部通过正则把"含 `#!important` 的行"提前到对应 `bind c` / `set -g default-terminal` 之前(或者只是不重写)

> 具体 perl regex 实现见 `.tmux.conf` 第 1050-1133 行附近,本笔记不深入到 sed 层面,因 README 的"用户文档"语义已清楚。

## 为什么需要这个机制

问题:`.local` 是 `source-file` 引入的,source 在主 conf 的 `bind c new-window ...` **之后**。tmux 的 bind 后写覆盖前写,用户的 `.local` `bind c new-window` 永远输给主 conf。

解决有 3 个候选:

| 方案 | 代价 | gpakosz 选哪个 |
|---|---|---|
| 把用户的 `.local` 在主 conf 头部 `source` | 需要重排 source 顺序,改动主 conf 结构 | ❌ |
| 在主 conf `bind` 之前加 `if -F` 检查 `.local` 是否设置过同名变量 | 复杂,需要把 bind 包成 shell 命令 | ❌ |
| 用标记符 `#!important` 让 perl sed 阶段把用户原行直接 patch 到 cfg | 用户只需在末尾加一个 magic suffix | ✅ |

## 反模式

- ❌ 在 `.local` 用 `bind -n`(无 prefix)试图绕过 —— 无 prefix 的 bind 优先级不同,问题不在这层。
- ❌ 把主 conf 的同名 `bind` 行删掉(主 conf 不能改)。
- ❌ 写 `set -g ... #!important` 但忘了空格 —— `#!important` 必须是同一行末尾的最后一个 token,前面要有空格分隔。
- ❌ 期望 `#!important` 能"加新 bind"——它只解决"覆写冲突",新 bind 直接写就行,无需标记。

## 与 vault 已有页的关系

- 上一层模式:[[concepts/tmux-local-override-pattern]]
- 实现:[[entities/gpakosz-tmux]]