---
title: tmux join-pane & swap-pane 用法
category: skills
tags:
  - tmux
  - cli
  - tools
  - pane-management
summary: >-
  tmux join-pane（跨窗口移动 pane）与 swap-pane（交换 pane 位置）的完整用法，含 move-pane、break-pane 配合模式、marked pane 技巧，以及典型工作流场景。
sources:
  - https://man.openbsd.org/tmux
  - https://www.man7.org/linux/man-pages/man1/tmux.1.html
  - https://tmuxcheatsheet.com
created: 2026-08-27
updated: 2026-08-27T00:00:00Z
tier: supporting
lifecycle: reviewed
lifecycle_changed: "2026-08-27"
base_confidence: 0.85
provenance:
  extracted: 0.90
  inferred: 0.08
  ambiguous: 0.02
relationships:
  - target: "[[skills/tmux]]"
    type: extends
  - target: "[[concepts/tmux-pane-split-for-agents]]"
    type: related_to
  - target: "[[concepts/tmux-pane-layout-rearrangement]]"
    type: related_to
---

# tmux join-pane & swap-pane 用法

> 前缀键简写 `PREFIX` = `Ctrl+b`（默认）。

## 核心概念区分

| 命令 | 效果 | 别名 |
|---|---|---|
| `join-pane` | 把 src-pane 移入另一个窗口，拆分目标 pane 腾出空间 | `joinp` |
| `move-pane` | 与 `join-pane` 完全相同 | `movep` |
| `swap-pane` | 交换两个 pane 的**位置**（不移动跨窗口） | `swapp` |
| `break-pane` | 把 pane 拆出来成为独立 window（`join-pane` 的反向） | `breakp` |

---

## join-pane — 跨窗口 pane 移动

### 语法

```
join-pane [-bdfhv] [-l size] [-s src-pane] [-t dst-pane]
```

### 选项

| Flag | 含义 |
|---|---|
| `-s src-pane` | 源 pane（要被移走的那个） |
| `-t dst-pane` | 目标 pane（在哪里腾出空间来接收） |
| `-h` | 水平分割（源 pane 出现在目标右侧） |
| `-v` | 垂直分割（默认，源 pane 出现在目标下方） |
| `-b` | 源 pane 出现在目标的**左侧或上方**（-h/-v 的反向） |
| `-f` | 全宽/全高分割（跨越整个窗口宽度或高度） |
| `-l size` | 指定新 pane 的尺寸（行数或列数） |
| `-d` | 不切换焦点到被移入的 pane |

### 核心用法示例

```bash
# 把当前 session 的 window 2 的 pane 0 移入 window 1
tmux join-pane -s 2.0 -t 1

# 把 window 2 的 pane 0 移入 window 1，水平排列，宽度 80 列
tmux join-pane -h -l 80 -s :2.0 -t :1

# 移入后 src-pane 出现在目标上方
tmux join-pane -v -b -s :2 -t :1

# 跨 session 移动
tmux join-pane -s mysession:2.0 -t othersession:1
```

### Pane 目标语法速查

```
session:window.pane     # 完整格式: mysession:2.0
:window.pane            # 省略 session（当前 session）
window                  # 省略 pane（该 window 的活动 pane）
%N                      # pane ID（唯一 ID，终身不变，如 %3）
{last}  或  !           # 上一个活动 pane
{marked} 或  ~          # 已标记的 pane
```

### 使用 Marked Pane（标记工作流）

先标记要移走的 pane，然后省略 `-s` 参数，让 tmux 自动使用被标记的那个：

```bash
# 在要移走的 pane 上按
PREFIX m            # 标记当前 pane（绿色边框，状态栏显示 M）

# 跳到目标 window，然后：
tmux join-pane -t :1     # 省略 -s，自动用 marked pane 作为源
```

### 反转 break-pane

`join-pane` 的设计初衷就是撤销 `break-pane`：

```bash
# 把当前 pane 拆出去变成独立 window
tmux break-pane            # 当前 pane 变成新 window（比如 window 2）

# 后悔了，把 window 2 拉回 window 1
tmux join-pane -s :2 -t :1
```

---

## swap-pane — 交换 pane 位置

### 语法

```
swap-pane [-dDUZ] [-s src-pane] [-t dst-pane]
```

### 选项

| Flag | 含义 |
|---|---|
| `-U` | 目标 pane 与**上一个**（前一个编号）pane 互换，无需 `-s` |
| `-D` | 目标 pane 与**下一个**（后一个编号）pane 互换，无需 `-s` |
| `-d` | 交换后不改变活动 pane |
| `-Z` | 若窗口处于 zoom 状态，交换后保持 zoom |
| `-s src-pane` | 明确指定要交换的另一端 |
| `-t dst-pane` | 目标 pane（默认为当前 pane） |

### 快捷键

```
PREFIX {    # 当前 pane 与前一个 pane 互换（等同 swap-pane -U）
PREFIX }    # 当前 pane 与后一个 pane 互换（等同 swap-pane -D）
PREFIX C-o  # 轮转窗口内所有 pane（rotate-window）
```

### 常用示例

```bash
# 交换 pane 0 和 pane 2
tmux swap-pane -s :0 -t :2

# 当前 pane 向上挪一位
tmux swap-pane -U

# 当前 pane 向下挪一位（等同 PREFIX }）
tmux swap-pane -D

# zoom 状态下不丢失 zoom
tmux swap-pane -UZ
```

### 用 Marked Pane 跨 window 交换

```bash
# 标记 window 1 里的某个 pane
PREFIX m

# 切到 window 2，交换（省略 -s，用 marked pane）
tmux swap-pane -t :2.1
```

> **注意：** `swap-pane` 交换的是位置（布局槽），不能用于跨 window 移动 pane 的归属。跨 window 移动请用 `join-pane`。

---

## move-pane — 与 join-pane 等价

```
move-pane [-bdfhv] [-l size] [-s src-pane] [-t dst-pane]
```

`move-pane`（别名 `movep`）与 `join-pane` 行为完全相同，接受相同的所有参数。两者可互换使用；`move-pane` 在语义上更直观（"移动"而非"合并"）。

**浮动 pane 扩展：** 在支持浮动 pane 的版本中，`move-pane` 额外支持 `-D/-L/-R/-U`（相对移动）、`-X/-Y`（绝对定位）和 `-P position`（命名位置，如 `centre`、`top-right`）。

---

## 典型工作流

### 工作流 1：整理散乱 pane

```bash
# 有两个窗口，想把 window 2 的 pane 全部并入 window 1
tmux join-pane -s :2.0 -t :1
tmux join-pane -s :2.0 -t :1   # 重复直到 window 2 清空
```

### 工作流 2：用 break + join 重新布局

```bash
# 想把 pane 移到窗口另一侧（当前垂直布局改水平）
tmux break-pane -s :1.2         # 先拆出去
tmux join-pane -h -s :2 -t :1  # 再水平合入
```

### 工作流 3：临时 zoom + 归位

```bash
# 临时单独看一个 pane
tmux break-pane                 # 拆出成独立 window 全屏查看
# 查看完毕...
tmux join-pane -s :last -t :1  # 归位（{last} = 刚才的 window）
```

### 工作流 4：Agent 多 pane 重排（Claude Code 场景）

```bash
# 把 agent pane 移到主 pane 下方，保持 editor 在左侧
tmux swap-pane -s :0.1 -t :0.2   # 调整 pane 顺序
tmux join-pane -v -l 20 -s :2 -t :1.0   # 把工具 window 合并进来
```

---

## 与相关命令的对比

| 需求 | 推荐命令 |
|---|---|
| 在同一窗口内调换 pane 顺序 | `swap-pane` / `PREFIX {` / `PREFIX }` |
| 把 pane 从一个 window 搬到另一个 | `join-pane -s src -t dst` |
| 把 pane 独立成全屏 window | `break-pane` |
| 撤销 break-pane | `join-pane -s :break_window -t :orig_window` |
| 新建分割 pane（新 shell） | `split-window` |
| 移动整个 window 到另一 session | `move-window` |
