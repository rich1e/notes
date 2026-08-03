---
title: "Tmux install.sh 安全设计 — dry-run、备份、拒绝 root、anti-piping"
category: concepts
tags:
  - tmux
  - installer
  - safety
  - dry-run
  - backup
  - gpakosz
  - design-pattern
sources:
  - https://github.com/gpakosz/.tmux
  - _raw/github-gpakosz-tmux.txt (gitingest export, gpakosz/.tmux master, 2026-08-03)
created: 2026-08-03T16:05:00Z
updated: 2026-08-03T16:05:00Z
summary: install.sh 通过 5 道闸保证用户资产安全:`EUID == 0` 直接退出、`$BASH_VERSION` 必须非空、`PERMISSIVE=1` 允许在 tmux 内运行、`DRY_RUN=1` 演练、`is_true()` 三态语义,以及发现 stdin 被 pipe 时主动请用户在 TTY 下复核脚本 —— 对抗 curl|bash 钓鱼。
tier: supporting
lifecycle: draft
lifecycle_changed: "2026-08-03"
base_confidence: 0.9
provenance:
  extracted: 0.85
  inferred: 0.12
  ambiguous: 0.03
relationships:
  - target: "[[entities/gpakosz-tmux]]"
    type: derived_from
  - target: "[[concepts/safe-destroy-by-default]]"
    type: related_to
---

# Tmux install.sh 安全设计

> `install.sh` 不是一段无害的 `cp + ln -s`。它在用户家目录里做备份、覆盖、克隆、symlink —— 任何一个失误都可能抹掉用户 `.tmux.conf`。gpakosz 的脚本通过 5 道闸把"想当然地执行"挡在外面。

## 5 道闸

### 闸 1:拒绝 root

```sh
if [ ${EUID:-$(id -u)} -eq 0 ]; then
  printf '❌ Do not execute this script as root!\n' >&2 && exit 1
fi
```

- root 下会改 `/root/...` 或全局文件,影响整个系统。
- 强调"用户态运行"才能尊重 `$HOME` 与 dotfiles 的所有权。

### 闸 2:必须 bash

```sh
if [ -z "$BASH_VERSION" ]; then
  printf '❌ This installation script requires bash\n' >&2 && exit 1
fi
```

- 后续用到 `${BASH_VERSION}`、`declare -f`、bash 数组语法等 bashism,POSIX sh / dash 不行。
- 错误信息明确,不假定用户知道当前 shell。

### 闸 3:必须已装 tmux

```sh
if ! tmux -V >/dev/null 2>&1; then
  printf '❌ tmux is not installed\n' >&2 && exit 1
fi
```

- 安装本身要修改 tmux 运行时配置(末尾 `tmux source "$TMUX_CONF"`),无 tmux 安装了也没用。
- 提前失败比留半截状态好。

### 闸 4:`PERMISSIVE` 跳过 tmux-in-tmux 拦截

```sh
if ! is_true "$PERMISSIVE" && [ -n "$TMUX" ]; then
  printf '❌ tmux is currently running, please terminate the server\n' >&2 && exit 1
fi
```

- `$TMUX` 非空说明**已在 tmux 内** —— 此时改 conf 文件再 `source`,旧 session 看到的是新 conf 行为,而新开 session 又是另一份,容易迷惑。
- 但允许"我就要在 tmux 内热加载"的高级用法通过 `PERMISSIVE=1 curl ... | bash` 绕过。
- **三态语义**:`is_true` 接受 `"true"` / `"yes"` / `"1"` 为真,其它为假 —— 字符串"未设置"和"显式关闭"等价,降低误配置概率。

### 闸 5:`DRY_RUN` 演练

```sh
if ! is_true "$DRY_RUN" && ! mv "$dir" "$dir.$now"; then
  printf '❌ %s directory exists, failed to back up → %s\n' ...
fi
```

- `DRY_RUN=1` 时**所有写盘操作都跳过**,只打印"将要做"信息。
- 配合 `$now="$(date +'%Y%m%d%H%M%S').$$"` 时间戳后缀,真实运行也用 `$dir.$now` 备份现有目录/文件,**不覆盖**用户资产。
- 用户可先 `DRY_RUN=1 curl ... | PERMISSIVE=1 bash` 演练,看到具体路径再正式跑。

## 备份策略

每次进入 `install()`,对以下 4 个潜在目标各做一次冲突检测:

```
$XDG_CONFIG_HOME/tmux/  ~/.tmux/           ← 目录
~/.tmux.conf             ~/.tmux.conf.local  ← conf 文件
$XDG_CONFIG_HOME/tmux/tmux.conf   .../tmux.conf.local
```

- **已存在 → 自动备份为 `$name.$timestamp`(不用覆盖)**。
- **是 symlink → 删**(因为 symlink 一定指向旧仓库,删后装新的会更安全)。
- 备份名包含 `YYYYMMDDHHMMSS.PID` —— 同一秒重复跑也不冲突(`$$` 提供 PID 后缀)。

## Anti-piping:拦截 `curl | bash`

脚本里有一段非常有趣的"自我审视"流程(line 618-676):

```sh
if [ -p /dev/stdin ]; then
  printf '✋ STOP\n' >&2
  printf '   🤨 It looks like you are piping commands from the internet to your shell!\n' >&2
  if ! : 2>/dev/null < /dev/tty; then
    # 没有 TTY 可用(纯管道)
    printf '   ⛔️ No terminal available to review the script...\n' >&2
    exit 1
  else
    # 有 TTY:启动一个交互子 shell 让用户 review
    (
      self() { ... 把自己打印出来 ... }
      while :; do
        printf '   Do you want to review the content? [Yes/No/Cancel] > ' >&2
        read -r answer
        case $answer in
          y|yes) self | (bat || vim || less) ; break ;;
          n|no)  break ;;
          c|cancel) exit 1 ;;
        esac
      done
    ) < /dev/tty || exit 1
fi
```

行为:

1. 检测 `/dev/stdin` 是否是 pipe(`[ -p ]`)。
2. 如果是且没有 `/dev/tty` → 直接退出,拒绝纯管道安装。
3. 如果有 `/dev/tty` → 用 subshell + `< /dev/tty` 重定向,把脚本内容**用 `bat`/`vim`/`less` 渲染**给用户看,等 Yes/No/Cancel 选择。
4. 用户 Yes 后才继续安装。

这是 GitHub 上少见的 `curl|bash` **主动反钓鱼**设计。绝大多数 dotfiles 安装器要么不拦截、要么粗暴 `exit 1`,这里给了"看清楚再装"的合理 UX。

## 安装结果路径

```sh
OH_MY_TMUX_CLONE_PATH="${XDG_DATA_HOME:-$HOME/.local/share}/tmux/oh-my-tmux"
TMUX_CONF="${XDG_CONFIG_HOME:-$HOME/.config}/tmux/tmux.conf"  # 或 ~/.tmux.conf
TMUX_CONF_LOCAL="$TMUX_CONF.local"
```

- 仓库落到 `~/.local/share/tmux/oh-my-tmux/`(XDG)或 `~/.tmux/`(旧路径)。
- `TMUX_CONF` 是 symlink → 仓库里的 `.tmux.conf`。
- `TMUX_CONF_LOCAL` 是 **真实复制** 的样本,用户从此改这份。

## 反模式(同类安装器常见陷阱)

- ❌ 直接 `cp` 不备份 —— 用户原有 conf 永久丢失。
- ❌ 用 `git pull` 同步已存在的克隆 —— 强制覆盖用户的本地修改。
- ❌ 在脚本顶部 `set -e` 后不区分 dry-run —— 演练模式下也会因 `mkdir` 之类失败提前退出。
- ❌ 不拦截 stdin pipe —— 让 `curl ... | bash` 的"盲目信任"成为常态。
- ❌ 拦截 stdin pipe 时直接 `exit 1` —— 没有给用户在 TTY 下 review 的机会。

## 与 vault 已有页的关系

- 实现:[[entities/gpakosz-tmux]]
- 同类"风险 opt-in"模式:[[concepts/safe-destroy-by-default]](treehouse 概念)
- 类似 chezmoi/dotbot 的多工具对比:[[entities/sebastienrousseau-dotfiles]]