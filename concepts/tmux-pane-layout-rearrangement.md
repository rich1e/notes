---
title: tmux Pane 布局重排模型
category: concepts
tags:
  - tmux
  - pane-management
  - cli
summary: >-
  tmux 中 pane 的三类重排操作：交换位置（swap-pane）、跨 window 移动（join-pane）、拆分独立（break-pane），以及 marked pane 机制如何统一这三者的工作流。
sources:
  - https://man.openbsd.org/tmux
  - https://www.man7.org/linux/man-pages/man1/tmux.1.html
created: 2026-08-27
updated: 2026-08-27T00:00:00Z
tier: supporting
lifecycle: reviewed
lifecycle_changed: "2026-08-27"
base_confidence: 0.83
provenance:
  extracted: 0.85
  inferred: 0.12
  ambiguous: 0.03
relationships:
  - target: "[[skills/tmux-join-pane-swap-pane]]"
    type: derived_from
  - target: "[[skills/tmux]]"
    type: related_to
  - target: "[[concepts/tmux-pane-split-for-agents]]"
    type: related_to
  - target: "[[concepts/tmux-pane-maximize-stateful]]"
    type: related_to
---

# tmux Pane 布局重排模型

tmux 把「pane 重排」拆成三个正交操作，理解这个分层是熟练使用的前提。

## 三层操作模型

```
Layer 1 — 同 window 内调序
  swap-pane (-U/-D / PREFIX { / PREFIX })
  └─ 只调换"槽位"，不改变 pane 归属 window

Layer 2 — 跨 window 搬移
  join-pane / move-pane (-s src -t dst)
  └─ 把 pane 从源 window "拉入"目标 window 的新分割槽
  └─ 与 break-pane 互为逆操作

Layer 3 — 独立/归位
  break-pane  →  pane 变成全屏独立 window
  join-pane   ←  把独立 window 并回某个 window（撤销 break）
```

## Marked Pane 机制

tmux 全局只允许同时存在**一个** marked pane（`PREFIX m` 标记，`PREFIX M` 清除）。  
标记后，凡是需要 `-s` 的命令（`join-pane`、`swap-pane`、`swap-window`）都可以**省略 `-s`**，自动使用 marked pane 作为源。

```
[window A, pane 2] → PREFIX m   # 标记
[window B, pane 0] → join-pane -t :B   # 把 A.pane2 移入 window B
```

这个机制让"标记 → 导航 → 操作"成为跨 window pane 移动的标准流程，无需记住复杂的 `session:window.pane` 路径。

## Pane 编号 vs Pane ID

| 属性 | 编号（index） | ID（`%N`） |
|---|---|---|
| 稳定性 | 随 swap/join 改变 | 终身不变 |
| 引用格式 | `:window.0` | `%3` |
| 适用场景 | 交互式快捷键 | 脚本和自动化 |
| 获取方式 | `PREFIX q` 显示 | `tmux list-panes -F '#{pane_id}'` |

> swap-pane 交换的是**槽位**，两个 pane 的编号也会随之互换，但 `%ID` 保持不变。

## 布局与 pane 移动的交互

pane 移动后，tmux 会尝试维持当前布局（even-horizontal / even-vertical / main-horizontal 等）。  
如果自动布局不理想：

```bash
PREFIX Space         # 循环切换预设布局
PREFIX Alt+1~5      # 跳到具体布局
```

## 与 split-window 的区别

| | `split-window` | `join-pane` |
|---|---|---|
| 创建新 shell | ✅ | ❌（移动已有 pane） |
| 改变 pane 数量 | +1 | 0（在 src window -1，dst window +1） |
| 跨 window 操作 | ❌ | ✅ |
