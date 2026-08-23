---
title: "macOS Keychain 读取 — security + base64 解码"
category: skills
tags: [macos, keychain, security-command, base64, secret-management]
sources:
  - "rich1e session (2026-08-24)"
created: 2026-08-24
updated: 2026-08-24
summary: macOS `security find-generic-password -s SERVICE -w` 返回密码值,但部分 go-keyring / chezmoi 工具链写入时用 `go-keyring-base64:` 前缀 + base64 编码;读取需先 strip 前缀再 `base64 -d` 解码。完整 pattern:`security find-generic-password -s SVC -w | sed 's|^go-keyring-base64:||' | base64 -d`。
base_confidence: 0.7
provenance:
  extracted: 0.6
  inferred: 0.4
lifecycle: draft
lifecycle_changed: 2026-08-24
tier: supporting
---

## 基础读取

```bash
security find-generic-password -s SERVICE_NAME -w
```

返回该 service 的密码值(明文)。可能弹出钥匙串访问授权对话框(Touch ID / 密码)。

## base64 前缀解码

部分工具链(go-keyring、某些 chezmoi 模板实现)写入时对密码做 base64 编码并加 `go-keyring-base64:` 前缀,使得含特殊字符的密码能无损存储。读取时需要:

```bash
security find-generic-password -s SERVICE_NAME -w \
  | sed 's|^go-keyring-base64:||' \
  | base64 -d
```

`go-keyring-base64:` 前缀存在说明该 entry 是编码后存储的(go-keyring 的事实标准);没有该前缀说明是明文直接写入。

## 常见 service 命名约定

| 工具链 | service 命名 | 例子 |
|---|---|---|
| chezmoi keyring template | `<service>-<username>` 或用户自定义 | `minimax-api-key`, `github-pat-rich1e` |
| go-keyring (Go 库) | 用户传入 | 因调用方而异 |
| 1Password CLI | N/A(走不同后端) | - |
| AWS CLI | `Amazon Web Services` | - |

## 与 chezmoi 配合

chezmoi `{{ keyring "service" "account" }}` 内部调用 `security find-generic-password`,但**它自己处理 base64 解码**(chezmoi 知道自家模板的编码格式)。若你绕过 chezmoi 直接用 `security` 命令读 chezmoi 写入的 keychain entry,记得手动 strip `go-keyring-base64:` 前缀 + base64 解码 —— 见 [[skills/statusline-template-injection-defense]] 中的 fallback 路径。

## 相关

- [[skills/chezmoi-keyring-template]] — chezmoi `{{ keyring ... }}` 模板
- [[skills/statusline-template-injection-defense]] — statusline 防御模板注入的修复
- [[concepts/unrendered-chezmoi-template-env-leak]] — 未渲染模板的 env 泄漏概念