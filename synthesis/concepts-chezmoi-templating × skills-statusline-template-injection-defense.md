---
title: "密钥注入 dotfile 的耦合陷阱 — chezmoi template × statusline env-first"
category: synthesis
tags: [chezmoi, templating, secrets, statusline, env-injection, macos-keychain, synthesis]
sources:
  - "[[concepts/chezmoi-templating]]"
  - "[[concepts/unrendered-chezmoi-template-env-leak]]"
  - "[[skills/statusline-template-injection-defense]]"
  - "[[skills/chezmoi-keyring-template]]"
  - "[[skills/macos-keychain-getBase64Key]]"
created: 2026-08-24
updated: 2026-08-24
summary: chezmoi `{{ keyring ... }}` 模板注入密钥到 dotfile → env 是当前 macOS 上最流行的密钥管理 pattern，但与 env-first + keychain-fallback 消费者（statusline / API 客户端）的耦合产生静默注入漏洞：未渲染时字面模板字符串当 Bearer token 发出。修复必须在消费者侧（启发式守卫），不在供给侧（chezmoi apply 有用户操作滞后）。
base_confidence: 0.90
provenance:
  extracted: 0.55
  inferred: 0.40
  ambiguous: 0.05
lifecycle: draft
lifecycle_changed: 2026-08-24
tier: core
relationships:
  - target: "[[concepts/chezmoi-templating]]"
    type: extends
  - target: "[[concepts/unrendered-chezmoi-template-env-leak]]"
    type: derived_from
  - target: "[[skills/statusline-template-injection-defense]]"
    type: related_to
---

# 密钥注入 dotfile 的耦合陷阱

## 现象

`~/.zsh-extend.sh`(或同族 dotfile)用 chezmoi 模板注入密钥：

```bash
export MINIMAX_API_KEY="{{ keyring "minimax-api-key" "rich1e" }}"
```

`chezmoi apply` 渲染时，从 macOS keychain 读真密钥替换进文件 → shell 启动时 env 已有真密钥 → 下游消费者（statusline / API 客户端）读 env-first, 一切正常。

**但当 `chezmoi apply` 漏跑**（新机首启 / dotfile 改后 / 模板语法错）,env 中实际值是字面 ~22 字节的 `{{ keyring ... }}` 模板字符串。下游消费者把它当密钥发到上游 API（如 `https://www.minimaxi.com/v1/token_plan/remains`），上游返回：

```json
{"base_resp": {"status_code": 1004, "status_msg": "login fail: Please carry the API secret key"}}
```

HTTP 200 + `status_code != 0` 让常规 `curl --fail` 检测不到；statusline 的缓存分支接管, 静默显示 `unavailable`。

## 修复 pattern（消费者侧）

```bash
# ~/.claude/statusline.sh
minimax_api_key_value="${MINIMAX_API_KEY:-}"
if [ -n "$minimax_api_key_value" ] \
  && printf '%s' "$minimax_api_key_value" | grep -q "{{"; then
  minimax_api_key_value=""
fi
if [ -z "$minimax_api_key_value" ]; then
  minimax_api_key_value="$(security find-generic-password -s MINIMAX_API_KEY -w | sed 's|^go-keyring-base64:||' | base64 -d)"
fi
```

`grep -q "{{"` 只匹配字面双花括号, 真实 API token 含 `{{` 概率几乎为 0。

## 为什么 fix 必须在消费者侧

`chezmoi apply` 是干净的长期方案，但**门槛是用户主动跑该命令**。statusline 必须在用户忘记跑 / 新机器首启 / dotfile 改完未 apply 的窗口里也能工作。Defense-in-depth 属于消费者侧, 不在供给侧 —— 供给侧修复有滞后, 消费者必须能自我保护。

## 一般化

任何 env-first + keychain-fallback 模式都易感:

| 消费者 | 例子 | 风险 |
|---|---|---|
| 编辑器 status bar | VSCode / Cursor / Zed 的 status bar API | 显示错位 / API 调用失败 |
| CLI 工具认证 | `gh auth`, `aws sso` | 401 / 服务不可用 |
| CI runner 注入 | CI 注入明文, 本地走 keychain | 本地开发时静默失败 |
| 本地脚本 | `~/.zshrc` / `~/.zsh-extend.sh` 启动脚本 | shell 启动失败 / 后续 API 失败 |

共同修复 pattern: env 值含 `{{` / 长度异常 / 已知错误前缀 → fail-closed 到下一个数据源。**不要 fail-open**。

## 跨域判断

**(J1)** **Supply-side vs demand-side 的责任划分**：env-first 是"信任供给侧已正确渲染"的乐观假设；chezmoi apply 是供给侧的 happy path，但现实中有漏跑窗口。demand-side 必须假设供给可能错,即 defense-in-depth 是常态。

**(J2)** **HTTP 200 + status_code 嵌套错误是 silent failure 教科书案例**: curl 看 HTTP, status line 看 status_code, 两层都看似"通过"但实际 fail。设计 API 时应让 401/403 触发 HTTP 错误状态码,而不是把错误编码在 200 body 里。

**(J3)** **vault/金库知识架构**: 此模式(消费者启发式 + keychain 回退)与 [[concepts/atomic-state-recovery]] 同哲学 —— 两层防御, 上一层失败时下一层兜底。`grep -q "{{"` 是 **检测注入信号** 的 deterministic check, 不需要预先知道所有 chezmoi 模板语法。

## 相关

- [[concepts/chezmoi-templating]] — chezmoi 模板语法
- [[concepts/unrendered-chezmoi-template-env-leak]] — 概念抽象 (渲染态 × env 耦合)
- [[skills/statusline-template-injection-defense]] — 修复 pattern (bash 守卫代码)
- [[skills/chezmoi-keyring-template]] — `{{ keyring ... }}` 模板用法
- [[skills/macos-keychain-getBase64Key]] — `security` 命令 + base64 解码
- [[skills/claude-code-statusline]] — Claude Code statusline 基础
- [[concepts/chezmoi-workflow]] — chezmoi 四动词 + apply 渲染桥梁