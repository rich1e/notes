---
title: "Statusline 防御未渲染 chezmoi 模板注入 — env 启发式 + keychain 回退"
category: skills
tags: [Claude, statusline, chezmoi, macos-keychain, gotcha, defense-in-depth]
sources:
  - "rich1e session (2026-08-24)"
created: 2026-08-24
updated: 2026-08-24
summary: statusline 用 env-first + keychain-fallback 读密钥时,若 ~/.zsh-extend.sh 通过 chezmoi `{{ keyring ... }}` 模板注入密钥但未被 `chezmoi apply` 渲染,字面模板字符串会成为 Bearer token;修复靠 env 启发式 (`grep -q "{{"`) 重置并让 keychain 回退接管。
base_confidence: 0.85
provenance:
  extracted: 0.9
  inferred: 0.1
lifecycle: draft
lifecycle_changed: 2026-08-24
tier: supporting
relationships:
  - target: "[[concepts/unrendered-chezmoi-template-env-leak]]"
    type: derived_from
  - target: "[[concepts/chezmoi-workflow]]"
    type: uses
  - target: "[[skills/claude-code-settings]]"
    type: related_to
---

## 问题

Claude Code statusline 用 env-first + keychain-fallback 读密钥(典型模式见 `~/.claude/statusline.sh`):

```bash
minimax_api_key_value="${MINIMAX_API_KEY:-}"
if [ -z "$minimax_api_key_value" ]; then
  minimax_api_key_value="$(security find-generic-password -s MINIMAX_API_KEY -w | sed 's|^go-keyring-base64:||' | base64 -d)"
fi
```

当 `~/.zsh-extend.sh`(或同族 dotfile)通过 chezmoi 模板注入密钥时:

```bash
export MINIMAX_API_KEY="{{ keyring "minimax-api-key" "rich1e" }}"
```

**若该 dotfile 未被 `chezmoi apply` 渲染**,env 中实际值是字面 126 字节的 `{{ keyring ... }}` 模板字符串,而非真正密钥。该字符串被当成 Bearer token 发到上游 API(如 `https://www.minimaxi.com/v1/token_plan/remains`),返回:

```json
{"base_resp": {"status_code": 1004, "status_msg": "login fail: Please carry the API secret key"}}
```

由于 HTTP 200 但 `status_code != 0`,statusline 的 `if status_code == 0` 缓存判断失败,`model_remains` 为空,面板显示 `MINIMAX │ unavailable`。**调试时这是双重陷阱**:HTTP 200 让 curl 看不出问题,`status_code: 1004` 让所有"API 调用成功"的检查全部跳过。

## 关键诊断信号

| 维度 | 未渲染模板(env 路径) | keychain 回退(base64 解码后) |
|---|---|---|
| 实际 "key" 长度 | ~22 字节(模板片段) | 完整真实密钥 |
| 上游 `base_resp.status_code` | **1004** login fail | **0** success |

"模板 vs 解码后" 的字节长度不对称是 smoking gun。Statusline 信任 env 优先于 keychain,所以只要未渲染模板在 env 中,bug 就是静默的。

## 修复(已落地于 `~/.claude/statusline.sh`)

在 env 读到值之后、用于 Bearer token 之前,加一层启发式守卫:值像未渲染 chezmoi 模板时,清空让 keychain 回退接管。

```bash
# If MINIMAX_API_KEY was injected by sourcing zsh-extend.sh but the file
# wasn't rendered by chezmoi, the literal `{{ keyring ... }}` template
# ends up in env. Treat it as missing and fall through to keychain.
if [ -n "$minimax_api_key_value" ] \
  && printf '%s' "$minimax_api_key_value" | grep -q "{{"; then
  minimax_api_key_value=""
fi
```

`grep -q "{{"` 只匹配字面双花括号,所以真实密钥里偶然出现 `{{` 也不会误触发(API token 含双花括号的概率极低)。

## 为什么修复必须在 statusline,不在 chezmoi

"渲染 chezmoi" 是干净的长期方案,但**门槛是用户主动跑 `chezmoi apply`**。statusline 必须在用户忘记跑/新机器首启/dotfile 改完未 apply 的窗口里也能工作。Defense-in-depth 属于消费者侧(statusline),不在供给侧(chezmoi) —— 因为供给侧的修复路径有滞后,消费者必须能在滞后窗口内自我保护。

## 一般化:任何 env-first + keychain-fallback 模式都易感

同一模式可破坏任何"先读 env,空了就读 keychain"的脚本:

- **编辑器插件**(VSCode / Cursor / Zed 的 status bar API 调用)
- **CLI 工具的认证模块**(`gh auth`, `aws sso`, 各种 API 客户端)
- **CI runner 注入密钥到 env,然后脚本读 env**
- **CI / 本地两用脚本**(CI 注入明文,本地走 keychain)

共同修复模式:env 值含 `{{` / 长度明显异常 / 含已知错误前缀(如 `go-keyring-base64:` 未解码) → 视为缺失 → fail-closed 到下一个数据源。**不要 fail-open**:宁可多走一次 keychain 查询,不要把明显非密钥的字符串发到上游。

## 相关

- [[concepts/unrendered-chezmoi-template-env-leak]] — 概念化:chezmoi 渲染态 × env 注入的耦合
- [[concepts/chezmoi-workflow]] — chezmoi 工作流:四个动词 + 一次更新(渲染在 `apply` 阶段)
- [[skills/claude-code-statusline]] — Claude Code statusline 配置基础
- [[skills/chezmoi-keyring-template]] — chezmoi `{{ keyring ... }}` 模板用法
- [[skills/macos-keychain-getBase64Key]] — macOS keychain `security` 命令 + base64 解码细节
- [[skills/claude-code-settings]] — Claude Code settings.json 作用域与权限