---
title: "inshellisense reload 兼容模式（ISTERM 守卫）"
category: concepts
tags:
  - topic/zsh
  - topic/inshellisense
  - topic/shell-wrapper
summary: "inshellisense 是 shell wrapper 模式（source → 启动 is daemon → exit），reload 需 ISTERM 守卫避免破坏 daemon 状态"
created: 2026-08-23T18:22:00Z
updated: 2026-08-23T18:22:00Z
base_confidence: 0.85
lifecycle: draft
lifecycle_changed: 2026-08-23
tier: supporting
sources:
  - "agent:claude-session zsh-extend session (2026-08-23)"
provenance:
  extracted: 0.9
  inferred: 0.1
relationships:
  - target: "[[concepts/zsh-shell-config-patterns]]"
    type: extends
---

# inshellisense reload 兼容模式（ISTERM 守卫）

## inshellisense 不是普通补全插件

大部分用户误以为 inshellisense 像 zsh-autosuggestions 那样加载即用。**实际是 shell wrapper 模式**。

`~/.local/share/inshellisense/init/zsh/init.zsh` 实际只有 7 行核心逻辑：

```bash
if [[ -z "${ISTERM}" && $- = *i* && $- != *c* && -z "${VSCODE_RESOLVING_ENVIRONMENT}" ]]; then
  if [[ -o login ]]; then
    is -s zsh --login ; exit   # 启动 is daemon + exit 当前 shell
  else
    is -s zsh ; exit            # 同上但非 login shell
  fi
fi
```

**流程**：`source init.zsh` → 启动 `is` node daemon → 当前 shell 立即 `exit` → 用户在 `is` 管理的子 shell 里工作。

`ISTERM` 环境变量是 `is` daemon 启动时设置的标志，用于告诉当前 shell"你已经被 inshellisense 接管了"。

## Reload 失败的根因

`source ~/.zshrc` 修改其他配置后，inshellisense 似乎"失效" —— 补全不响应，提示符变了，`is doctor` 报错。

**根因**：reload 时 `ISTERM=1` 已设（之前 is daemon 设置的），所以 init.zsh 的守卫条件 `[[ -z "${ISTERM}" ]]` 失败 → **不重新启动 daemon**，但当前 shell 也不是 is daemon 的子 shell。造成状态错乱：

| 阶段 | 状态 |
|------|------|
| reload 之前 | 是 daemon 管理的子 shell |
| reload 之后 | 当前 shell（is daemon 已 exit）继续运行，daemon 失联 |

官方 README 警告 "make sure the inshellisense plugin is the last command in the file" —— 不是防止 init 失败，是防止后续 source 破坏 daemon 状态。

## ISTERM 守卫方案

```bash
# 11.4 inshellisense（必须放配置最末尾）
_is_init="$HOME/.local/share/inshellisense/init/zsh/init.zsh"
[[ -z "${ISTERM}" && -f "$_is_init" ]] && source "$_is_init"
```

**逻辑**：

- `ISTERM` 未设 → 首次进入 shell → 正常 source → 启动 daemon → 接管
- `ISTERM=1` → reload 时 → 守卫跳过 → 当前 is session 不被破坏

## GitHub 上的官方答案

官方仓库（microsoft/inshellisense）**没有 reload 方案**，因为设计假设就是"exit + 重进"。社区方案就是 ISTERM 守卫（或类似 `[[ -n "${INSELLISENSE_LOADED+x}" ]] && return` 自定义守卫）。

## 修改不同部分后的生效路径

| 改了哪部分 | 怎么生效 |
|------------|---------|
| 普通 zsh 配置（zsh-extend 其他章节） | `source ~/.zshrc` 即可 |
| inshellisense 配置（`~/.inshellisenserc`） | `exit` 当前会话 + 重进终端，让 is daemon 重读 |
| inshellisense 二进制本身 | `npm update -g @microsoft/inshellisense && is reinit`，然后重进终端 |

## 相关

- [[concepts/zsh-shell-config-patterns]] — zsh 配置通用优化模式
- [[entities/inshellisense]] — 项目本体（待建）

## 替代方案

- **`fzf-tab`**：纯 zsh 实现的 Tab 补全增强，无 daemon、reload 自动生效、内存占用低。适合追求轻量的用户。
- 当前 zsh-extend 配置因 inshellisense 与 zsh-autosuggestions 在 ghost-text 场景下冲突，已临时注释 11.4 节。