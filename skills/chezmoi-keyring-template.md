---
title: "chezmoi Keyring 模板 — `{{ keyring ... }}` 用法"
category: skills
tags: [chezmoi, keyring, template, macos-keychain, secret-management]
sources:
  - "rich1e session (2026-08-24)"
created: 2026-08-24
updated: 2026-08-24
summary: chezmoi `{{ keyring "service" "account" }}` 模板在渲染时从 OS keychain(macOS Security / Linux secret-service / Windows Credential Manager)读取密码替换进文件。用于把密钥/Token 注入 dotfile 而不入 git。坑:dotfile 未 `chezmoi apply` 时,字面模板字符串会进入 env —— 见 [[concepts/unrendered-chezmoi-template-env-leak]]。
base_confidence: 0.6
provenance:
  extracted: 0.5
  inferred: 0.5
lifecycle: draft
lifecycle_changed: 2026-08-24
tier: supporting
---

## 用法

```bash
# 在 dot_zsh-extend.sh.tmpl 中:
export MINIMAX_API_KEY="{{ keyring "minimax-api-key" "rich1e" }}"
```

`chezmoi apply` 渲染时,chezmoi 会调用 OS keychain API(macOS `security find-generic-password` 等)读取 service=`minimax-api-key` account=`rich1e` 的密码,替换进文件。文件落地后是明文密钥 + `export`,shell 启动时自动注入 env。

## 适用场景

- dotfile 仓库要公开/多端同步,但含个人 API key(Anthropic / OpenAI / GitHub PAT / 各种 SaaS)
- 不想用 1Password CLI / Bitwarden CLI 之类的额外依赖(虽然它们各有自己的模板函数)
- macOS / Linux / Windows 都有原生 keychain,chezmoi 统一抽象

## 坑:未渲染状态

详见 [[concepts/unrendered-chezmoi-template-env-leak]]。核心:**dotfile 未 `chezmoi apply` 时,模板字符串原样进入 env**。修复在消费者侧,见 [[skills/statusline-template-injection-defense]]。

## 相关

- [[concepts/chezmoi-templating]] — chezmoi 模板语法全景
- [[concepts/chezmoi-workflow]] — chezmoi 工作流(`apply` 是渲染桥梁)
- [[skills/macos-keychain-getBase64Key]] — macOS keychain 读取细节(base64 解码)
- [[concepts/unrendered-chezmoi-template-env-leak]] — 未渲染模板的 env 泄漏概念