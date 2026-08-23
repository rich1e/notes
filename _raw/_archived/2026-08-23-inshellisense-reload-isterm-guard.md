---
title: "inshellisense reload 兼容模式（ISTERM 守卫）"
category: skills
tags:
  - topic/zsh
  - topic/inshellisense
  - topic/shell-wrapper
summary: "inshellisense 是 shell wrapper 模式（source → 启动 is daemon → exit），reload 需 ISTERM 守卫避免破坏 daemon"
tier: supporting
related: []
extends: null
contradicts: null
superseded_by: null
capture_source: claude-session
project: zsh-extend
base_confidence: 0.85
lifecycle: draft
lifecycle_changed: 2026-08-23
provenance:
  extracted: 0.9
  inferred: 0.1
sources:
  - "zsh-extend session (2026-08-23)"
---

# inshellisense reload 兼容模式（ISTERM 守卫）

## inshellisense 不是普通补全插件

**Behavior:** 大多数人误以为 inshellisense 像 zsh-autosuggestions 那样加载即用。实际是 shell wrapper 模式：source init.zsh → 启动 `is` node daemon → 当前 shell 立即 `exit` → 用户在 `is` 管理的子 shell 里工作。

**Explanation:** init.zsh 实际只有 7 行核心逻辑：
```bash
if [[ -z "${ISTERM}" && $- = *i* && $- != *c* && -z "${VSCODE_RESOLVING_ENVIRONMENT}" ]]; then
  if [[ -o login ]]; then
    is -s zsh --login ; exit
  else
    is -s zsh ; exit
  fi
fi
```
`ISTERM` 环境变量是 `is` daemon 启动时设置的标志，用于告诉当前 shell"你已经被 inshellisense 接管了"。

## Reload 失败的根因

**Behavior:** `source ~/.zshrc` 修改其他配置后，inshellisense 似乎"失效"了 —— 补全不响应，提示符变了，`is doctor` 报错。

**Explanation:** reload 时 `ISTERM=1` 已设（之前 is daemon 设置的），所以 init.zsh 的守卫条件 `[[ -z "${ISTERM}" ]]` 失败 → **不重新启动 daemon**，但当前 shell 也不是 is daemon 的子 shell。这造成状态错乱：
- reload 之前：是 daemon 管理的子 shell
- reload 之后：当前 shell（is daemon 已 exit）继续运行，daemon 失联

官方 README 警告 "make sure the inshellisense plugin is the last command in the file" —— 不是防止 init 失败，是防止后续 source 破坏 daemon 状态。

## ISTERM 守卫方案

**Fix:**
```bash
# 11.4 inshellisense（必须放配置最末尾）
# reload 守卫：isterm 设了 → 当前已在 is daemon 中 → 不重新 source

_is_init="$HOME/.local/share/inshellisense/init/zsh/init.zsh"
[[ -z "${ISTERM}" && -f "$_is_init" ]] && source "$_is_init"
```

**Confirmed by:** 模拟测试 `ISTERM=1 source zsh-extend.sh` → 守卫生效，不重复 source。

## GitHub 上的官方答案

官方仓库（microsoft/inshellisense）**没有 reload 方案**，因为设计假设就是"exit + 重进"。社区方案就是 ISTERM 守卫（或类似 `[[ -n "${INSELLISENSE_LOADED+x}" ]] && return` 自定义守卫）。

**Confirmed by:** GitHub search "inshellisense zsh reload" 无相关 issue/讨论。

## 修改配置后的处理流程

| 改了哪部分 | 怎么生效 |
|------------|---------|
| 普通 zsh 配置（zsh-extend 其他章节） | `source ~/.zshrc` 即可 |
| inshellisense 配置（`~/.inshellisenserc`） | `exit` 当前会话 + 重进终端，让 is daemon 重读 |
| inshellisense 二进制本身 | `npm update -g @microsoft/inshellisense && is reinit`，然后重进终端 |

## Notes

- inshellisense 与 zsh-autosuggestions 在某些 ghost-text 场景下冲突 —— 当前配置已临时注释 inshellisense（11.4 节），等社区方案稳定
- 替代方案：`fzf-tab`（纯 zsh，reload 自动生效，无 daemon），适合追求轻量的用户