---
title: "Tmux pane maximize 跨 window 保留状态的设计"
category: concepts
tags:
  - tmux
  - pane
  - window-management
  - state
  - gpakosz
sources:
  - https://github.com/gpakosz/.tmux
  - _raw/github-gpakosz-tmux.txt (gitingest export, gpakosz/.tmux master, 2026-08-03)
created: 2026-08-03T16:05:00Z
updated: 2026-08-03T16:05:00Z
summary: gpakosz `<prefix> +` 比内置 `resize-pane -Z` 强:把 pane 升格到新 window 仍可继续 split;跨 window 切换后,被 maximize 的 pane 在新 window 里仍处 maximized 状态 —— 用 `maximized` window 名字 + `remain-on-exit` + `swap-pane` 还原实现。
tier: peripheral
lifecycle: draft
lifecycle_changed: "2026-08-03"
base_confidence: 0.82
provenance:
  extracted: 0.78
  inferred: 0.18
  ambiguous: 0.04
relationships:
  - target: "[[entities/gpakosz-tmux]]"
    type: derived_from
  - target: "[[skills/tmux]]"
    type: related_to
---

# Tmux pane maximize 跨 window 保留状态

> gpakosz 的 `<prefix> +` 设计:把当前 pane maximize 到一个**专用的、命名固定的**新 window,原 pane 实际被 swap-pane 取代;再次按 `<prefix> +` 在任一 window 触发都能还原。

## 与内置 `resize-pane -Z` 的差异

| 行为 | `resize-pane -Z`(内置) | gpakosz `<prefix> +` |
|---|---|---|
| 占用模式 | 当前 window 内"伪"放大 | **新开 window** 把 pane 整个移过去 |
| 放大后能否再 split | ❌ 整 window 锁为一个 pane | ✅ 新 window 可继续 split |
| 切到其它 window 再回来 | **仍处于放大态**(毕竟没动 window) | **仍处于放大态**(在新 window 那边) |
| 触发按键后窗口切换 | 否 | 是(`new-window`) |
| 还原 | 同一 `<prefix> z` | 同一 `<prefix> +`(在源或目标 window 都生效) |

README 第 201-206 行原文:

> "The 'Maximize any pane to a new window with `<prefix> +`' feature is different from the builtin `resize-pane -Z` command, as it allows you to further split a maximized pane. It's also more flexible by allowing you to maximize a pane to a new window, then change window, then go back and the pane is still in maximized state in its own window."

## 实现思路(`.tmux.conf` line 492-518)

```sh
_maximize_pane() {
  current_session=${1:-$(tmux display -p '#{session_name}')}
  dead_panes=$(tmux list-panes -s -t "$current_session:" -F '...' | grep -E -o '^1 %.+maximized.+$' || true)

  # 1. 找当前是否已有 maximize 出来的 window
  if [ -n "$dead_panes" ]; then
    # 还原路径:把 source pane swap 回来
    tmux swap-pane -s "$current_pane" -t "$new_pane"
  else
    # 2. 新开一个名字固定包含 'maximized' 的 window,保留原 pane 的内容
    info=$(tmux new-window -t "$current_session:" -F "#{session_name}:#{window_index}.#{pane_id}" -P "maximized... 2>/dev/null & ...")
    # remain-on-exit 让 maximized 提示进程不会因命令结束而消失
    session_window=${info%.*}

    # 3. 轮询直到新 pane 真正死亡(原 shell 已退出),再 swap-pane
    while [... pane is still alive ...]; do :; done

    # 4. 把 source pane swap 进新 window
    tmux swap-pane -s "$current_pane" -t "$new_pane"
  fi
}
```

核心三招:

1. **`maximized` window 名作为状态标记**:`list-panes -F` + grep 名字里的 `maximized` 字符串判断当前 session 是否有"被 maximize 出来"的 window。这是**用 window 名字当作可枚举状态**,无需额外 storage。
2. **`remain-on-exit on`**:在新 window 跑的"maximized..."提示命令结束时,window 不立即消失,等外部 swap 进来才退出 —— 充当"占位 + 时机窗口"。
3. **`swap-pane -s $src -t $dst`**:最后一步把原 pane 物理换到新 window 内。原位置的 window 自动获得焦点,看起来像"展开"。

## 状态机

```
         +-- <prefix> + (无现存 maximize) --> 新 window 含 'maximized'
         |                                    |
源 pane ──┤                                    | swap-pane
         |                                    ↓
         +-- <prefix> + (已存在 maximize) --> swap-pane 反向 → 还原
                                              ↑
                                              +-- 触发位置可以是源或目标 window
```

`list-panes -s`(列出"无 window 的 pane")是判断"是否已 maximize"的探针:被 maximize 的原 pane 没有所属 window,会出现在 `-s` 列表里。

## 失败的反模式(从实现反推)

- ❌ 用 `resize-pane -Z` 然后想再 split —— 单 window 单 pane,不可 split。
- ❌ 用 `link-window` 或 `join-pane` 链接 window —— 失去单 pane 独立性,源/目标 pane 状态相互污染。
- ❌ 不轮询新 pane 死亡直接 swap —— race:原 shell 还没退出,swap 后原 window 仍残留新进程。
- ❌ 状态标记用 `set-option` 或外部文件 —— 不需要,window name 即可枚举。

## 与 vault 已有页的关系

- 实现:[[entities/gpakosz-tmux]]
- 通用 tmux 速查:[[skills/tmux]]