---
title: "zsh 配置通用优化模式"
category: skills
tags:
  - topic/zsh
  - topic/shell-config
  - topic/macos
summary: "Zsh 个人配置文件的实战优化：HOMEBREW_PREFIX 缓存、setopt 兼容性、chezmoi 密钥集成、Insidell 等陷阱"
tier: supporting
related: []
extends: null
contradicts: null
superseded_by: null
capture_source: claude-session
project: zsh-extend
base_confidence: 0.8
lifecycle: draft
lifecycle_changed: 2026-08-23
provenance:
  extracted: 0.85
  inferred: 0.15
sources:
  - "zsh-extend session (2026-08-23)"
---

# zsh 配置通用优化模式

`zsh-extend.sh` 审计得出的可复用模式。所有改动都在 macOS + Homebrew + chezmoi 环境下验证过。

## HOMEBREW_PREFIX 缓存

**Problem:** 配置中多处 `$(brew --prefix)/share/xxx` 重复调用，启动期 17 次 brew 调用，慢 200-400ms。

**Root cause:** Homebrew 不会自动 export `HOMEBREW_PREFIX` 给子 shell，但用户/系统 profile.d 通常已设置。`brew --prefix` 每次都查 Cellar 状态。

**Fix:**
```bash
# 2.1 节顶部，缓存一次
if [[ -z "$HOMEBREW_PREFIX" ]] && type brew &>/dev/null; then
  HOMEBREW_PREFIX="$(brew --prefix)"
  export HOMEBREW_PREFIX
fi

# 之后统一用变量
[[ -f "$HOMEBREW_PREFIX/share/zsh-autosuggestions/zsh-autosuggestions.zsh" ]] && ...
```

**Confirmed by:** 启动时间实测下降；后续插件加载用 `${HOMEBREW_PREFIX}` 替换所有硬编码 `/opt/homebrew/...`。

## setopt NO_UNSET 与第三方插件不兼容

**Problem:** 启用 `setopt NO_UNSET` 后启动报错：
```
/opt/homebrew/etc/profile.d/autojump.sh:3: BASH: parameter not set
/opt/homebrew/share/forgit/forgit.plugin.zsh:34: BASH_VERSION: parameter not set
```

**Root cause:** autojump 和 forgit 在 BASH 模式下用 `${VAR:-}` 探测环境变量，`NO_UNSET` 下未定义变量即报错，使整个探测失败。

**Fix:**
```bash
# 注释清楚为什么不启用 NO_UNSET
setopt PIPE_FAIL              # 管道任一阶段失败即整体失败
# 注意：不启用 NO_UNSET —— autojump/forgit 等插件依赖 BASH 模式下的未设置变量判断
# 改用 ${VAR:-} 显式默认值作为防御写法
```

**Confirmed by:** 移除 NO_UNSET 后 autojump (`j`) 和 forgit (`gla`) 加载成功，无报错。

## chezmoi 密钥模板与函数重复

**Problem:** 配置里既定义了 `getBase64Key()` 函数族，又写了 `export XXX="{{ keyring "xxx" "rich1e" }}"` 模板语法，两套机制并存。

**Root cause:** 用户从 zsh-extend 切到 chezmoi 管理后，函数变成历史遗留，但 export 行改成 chezmoi 的 `{{ keyring ... }}` 模板。

**Fix:** 保留 chezmoi 模板（chezmoi 启动前渲染），删除未使用的 `getBase64Key/openai_api_key/...` 函数族：
```bash
# 1.6-1.9 chezmoi 模板（chezmoi 启动前渲染为真实值）
export GITHUB_TOKEN="{{ keyring "github-token" "rich1e" }}"
export OPENAI_API_KEY="{{ keyring "openai-api-key" "rich1e" }}"
# ...
```

**Confirmed by:** 模板保留，函数族删除，启动期密钥直接由 chezmoi 注入。

## alias 改为函数避免劫持

**Problem:** `alias ssh="ssh -X"` 和 `alias rm='trash'` 会劫持所有调用，包括 `git+ssh`、`npm scripts` 里的 `rm`。

**Root cause:** alias 替换是文本级，无条件覆盖。脚本期望 `rm` 是 GNU coreutils。

**Fix:** 用函数 + `command` 前缀：
```bash
# ssh 加保活，函数优先于 alias
ssh() { command ssh -o ServerAliveInterval=60 -o ServerAliveCountMax=3 "$@" }

# rm 包装 trash，但危险参数显式拦截
rm() {
  if [[ $# -eq 0 ]]; then echo "用法: rm <file>..." >&2; return 1; fi
  if [[ "$1" == "-rf" || "$1" == "--" ]]; then
    echo "❌ 已禁止直接调用 rm" >&2; return 1
  fi
  trash "$@"
}
```

**Confirmed by:** 函数覆盖 alias（zsh 优先级），`command rm` 仍可手动调用真实删除。

## fzf preview 公共变量提取

**Problem:** `FZF_COMPLETION_OPTS` / `FZF_DEFAULT_OPTS` / `FZF_CTRL_T_OPTS` 三个变量里 `--preview 'if [ -d {} ]; then eza ...; fi'` 重复三次。

**Fix:**
```bash
_fzf_preview_cmd='if [ -d {} ]; then eza --tree --level=2 --color=always --icons {}; else bat --style=numbers --color=always --line-range :500 {}; fi'

export FZF_COMPLETION_OPTS="
--height 80%
--layout reverse
--border
--select-1
--exit-0
--preview '$_fzf_preview_cmd'
"
```

**Confirmed by:** 三个 fzf 入口（Ctrl+T / Alt+C / 补全）共用同一 preview，行为一致。

## inshellisense 必须放配置最末尾

**Problem:** inshellisense 官方要求 source 行是文件最后一行，否则 `is` daemon 状态被破坏。

**Root cause:** inshellisense 是 shell wrapper 模式（source → 启动 is daemon → exit 接管当前 shell），任何后续 source 都会破坏 daemon。

**Fix:** 把 inshellisense 放到 zsh-extend.sh 第 11.4 节（11.x 节末尾），Starship 之后。

**Confirmed by:** 启动时 is daemon 接管成功，is doctor 无 legacy config 警告。

## Notes

- `trash` CLI 选项：`trash -l`（列出）、`trash -e`（清空）、`trash -y`（无确认）、`trash -F`（强制含 root-owned）
- zsh-extend.sh 当前 609 行，所有修改都过 `zsh -n` 语法验证