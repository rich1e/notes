---
title: "Tmux `.local` 覆写层模式 — 主 conf 不可改,所有 customization 走变量"
category: concepts
tags:
  - tmux
  - configuration
  - upgrade-safety
  - gpakosz
  - design-pattern
sources:
  - https://github.com/gpakosz/.tmux
  - _raw/_archived/github-gpakosz-tmux.txt (gitingest export, gpakosz/.tmux master, 2026-08-03)
created: 2026-08-03T16:05:00Z
updated: 2026-08-03T16:05:00Z
summary: gpakosz 设计:`.tmux.conf`(主)不可改,`.tmux.conf.local` 是用户唯一编辑入口;主 conf 通过 source + 探测变量存在性(`_is_disabled`/`_is_true`)合并用户偏好。`#!important` 解决冲突。模式:上游可升级 + 用户可定制 + 单向注入。
tier: core
lifecycle: draft
lifecycle_changed: "2026-08-03"
base_confidence: 0.9
provenance:
  extracted: 0.88
  inferred: 0.1
  ambiguous: 0.02
relationships:
  - target: "[[entities/gpakosz-tmux]]"
    type: derived_from
  - target: "[[concepts/tmux-config-importance-override]]"
    type: uses
---

# Tmux `.local` 覆写层模式

> "🚨 You should never alter the main `.tmux.conf` or `tmux.conf` file. If you do, you're on your own. Instead, every customization should happen in your `.tmux.conf.local` or `tmux.conf.local` customization file copy."
> —— README 第 51-53 行(原句)

## 模式要点

| 角色 | 文件 | 谁能改 |
|---|---|---|
| 主配置(上游) | `.tmux.conf` | **不能改** —— `git pull` 时会被覆盖 |
| 用户覆写 | `.tmux.conf.local` | **用户唯一编辑入口**,`~/.tmux.conf.local` 持久不被覆盖 |

主 conf 用 `source-file` 引用 `.local`,后者用 `tmux_conf_*` 命名空间变量暴露所有可调点。

## 实现机制

`.tmux.conf` 通过探测变量值决定行为(简化):

```sh
# 主 conf 内
: "${tmux_conf_new_pane_retain_current_path:=true}"   # 默认值
if _is_true "$tmux_conf_new_pane_retain_current_path"; then
  # 启用新 pane 保留当前路径
fi
```

`.tmux.conf.local` 只需要覆盖变量:

```sh
tmux_conf_new_pane_retain_current_path=false   # 用户改成关闭
tmux_conf_theme_colour_4="#00afff"            # 主题色自定义
```

`_is_true` / `_is_disabled` 在 `.tmux.conf` 内定义,把 `"true"`/`"yes"`/`"1"` 之外的字符串当作"关",让"未设置"与"显式 false"语义一致。

## 为什么这么设计

1. **升级安全**:`git pull` 主 conf 不会带冲突;`.local` 单独保留,merge 仅 `.conf` 一份。
2. **合并单向性**:主 conf 永远 `source .local`,不会反过来 —— 保证上游演化不会"覆盖用户的设置"。
3. **可发现性**:用户打开 `.local` 看到一份"所有可调点的注释清单",无需 grep 主 conf。
4. **零依赖**:不需要 external tool(不像 chezmoi / dotbot);仅靠 `source-file` + shell 变量探测。

## `#!important` 冲突解决

`.local` 用 `bind` / `set` 经常被主 conf "抢走"(主 conf 在 source 之后还会执行一堆 `bind`)。README 第 127-137 行教的解法:

```sh
bind c new-window -c '#{pane_current_path}' #!important
set -g default-terminal "screen-256color"    #!important
```

`#!important` 在 `.tmux.conf` 内部被 perl 脚本(`.tmux.conf` 第 1125-1133 行附近)作为 sed 标记,在写入用户绑定的 sed 流里强制把 `new-session` 之类命令的 `bind`/`set` 提到主 conf 之前生效。

详见 [[concepts/tmux-config-importance-override]]。

## 可发现性的代价

- **复杂度高**:主 conf 内对每个 customization point 都要写一个探测分支,新增 customization point 要改主 conf,不能纯追加。
- **`#!important` 是后置补丁**:用户需要知道这个机制才能解决冲突,新手会被 `#!important` 困惑。
- **无法在 `.local` 里做条件逻辑**(变量是扁平字符串)。

但对"普通 tmux 用户 + 偶尔改键位 + 偶尔升上游"的真实场景,**收益 > 成本**。

## 反模式

| 反模式 | 后果 |
|---|---|
| 直接 fork + 改 `.tmux.conf` | 失去上游更新;一旦想升级要 cherry-pick |
| 用 chezmoi / dotbot 管理两 conf | 多一层工具,本地重装或换机器变复杂 |
| 把用户覆写写在主 conf 末尾 | `git pull` 必冲突 |
| 用 include-directive(`source -q`)而不用变量 | customization point 不集中,散落在多文件 |

## 与 vault 已有页的关系

- 实现:[[entities/gpakosz-tmux]]
- 冲突机制:[[concepts/tmux-config-importance-override]]
- 类似 dotfiles 哲学对比:[[entities/sebastienrousseau-dotfiles]] —— 后者用 chezmoi,本模式纯 tmux 内置