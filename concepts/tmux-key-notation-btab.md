---
title: "Tmux 键位记号 `B<Tab>` — `<prefix>` + `<key>` 的简写约定"
category: concepts
tags:
  - tmux
  - keybinding
  - documentation
  - gpakosz
sources:
  - https://github.com/gpakosz/.tmux
  - _raw/github-gpakosz-tmux.txt (gitingest export, gpakosz/.tmux master, 2026-08-03)
created: 2026-08-03T16:05:00Z
updated: 2026-08-03T16:05:00Z
summary: gpakosz README 用 `B<Tab>`、`B<C-c>`、`B<C-f>` 等记号代替 `<prefix> Tab` / `<prefix> C-c` / `<prefix> C-f` —— `B` 是 prefix 占位符(Bind/Button),配合双 prefix 设计,文档层抽象掉 `C-b` vs `C-a` 的差异。
tier: supporting
lifecycle: draft
lifecycle_changed: "2026-08-03"
base_confidence: 0.85
provenance:
  extracted: 0.95
  inferred: 0.04
  ambiguous: 0.01
relationships:
  - target: "[[entities/gpakosz-tmux]]"
    type: derived_from
  - target: "[[concepts/tmux-prefix-double-binding]]"
    type: related_to
---

# Tmux 键位记号 `B<Tab>`

## 记号约定

README 第 234 行起明确定义:

> - `<prefix>` means you have to either hit `Ctrl+a` or `Ctrl+b`
> - `<prefix> c` means you have to hit `Ctrl+a` or `Ctrl+b` followed by `c`
> - `<prefix> C-c` means ... followed by `Ctrl+c`

但**正文实际写法**采用 `B<Tab>`、`B<C-c>`、`B<C-f>` 这种紧凑记号:

| README 写法 | 实际含义 | `.tmux.conf` 行号 |
|---|---|---|
| `<prefix> BTab` | `prefix + Shift+Tab` → `switch-client -l`(回上一 active session) | line 76 `bind BTab switch-client -l` |
| `<prefix> Tab` | `prefix + Tab` → `last-window`(回上一 active window) | line 107 `bind Tab last-window` |
| `<prefix> C-c` | `prefix + Ctrl+c` → `new-session` | line 70 `bind C-c new-session` |
| `<prefix> C-f` | `prefix + Ctrl+f` → `command-prompt`(找 session) | line 73 `bind C-f command-prompt -p '(find-session)' 'switch-client -t %%'` |
| `<prefix> +` | `prefix + Shift+=` → maximize pane | line 92 `bind + run "..._maximize_pane..."` |
| `<prefix> -` | `prefix + -` → 垂直 split | — |

## `B` 字符的含义

`B` 是 prefix 的"占位符字母",**不是字面 `Ctrl+B`**。含义有几种解读:

- **Bind/Button**:tmux 配置语境下"按 prefix"是触发一组 `bind-key`,所以 `B` 表"已触发 Bind 状态"。
- **GNU Screen 致敬**:`C-a` 是 GNU Screen prefix,字母 `B` 紧邻 `A`,可记作"A 已按,等下一个键"。
- **占位习惯**:其它 README 也用类似记号(如 `<P>`、`<leader>`),本仓库统一选 `B`。

## 修饰键的字母拼写

- `C` = `Ctrl`
- `S` = `Shift`(且必须大写,代表 shift 后产生的字母)
- `M` = `Alt` / `Meta`
- 无字母 = 字面键

所以:
- `BTab` = "prefix + Shift+Tab"(`B`=prefix,`Tab` 字母大写 = Shift 修饰后的 Tab)
- `B<C-c>` = "prefix + Ctrl+c"(尖括号内大写 `C` 表示 Ctrl)
- `B+` = "prefix + Shift+="(`+` 不需要 Shift 的键位,直接写)

## 为什么不用尖括号包裹 prefix

角括号 `<prefix> Tab` 是 ASCII 友好的"完整版",`B<Tab>` 是简写版。两者在同一文档混用:

- 章节首段用 `<prefix>` 做语法定义(清楚、跨工具兼容)。
- 后续段落大量用 `B<Tab>` 节省篇幅,且视觉上能扫读。

## 反模式

- ❌ 把 `B` 误读成字面 `Ctrl+B` —— 会以为需要按 `Ctrl+B Shift+Tab`,实际只需 `Ctrl+A` 或 `Ctrl+B` + `Shift+Tab`。
- ❌ 把 `BTab` 读成"按 Tab 键两次"——`B` 是 prefix 占位符不是修饰符。

## 与 vault 已有页的关系

- 实现:[[entities/gpakosz-tmux]]
- prefix 双方案背景:[[concepts/tmux-prefix-double-binding]]