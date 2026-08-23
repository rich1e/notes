---
title: "Claude Code Statusline 配置基础"
category: skills
tags: [claude-code, statusline, shell, configuration]
sources:
  - "rich1e session (2026-08-24)"
created: 2026-08-24
updated: 2026-08-24
summary: Claude Code statusline 是 shell 脚本(默认 ~/.claude/statusline.sh),每次 turn 结束时 Claude Code 把 JSON 通过 stdin 喂给脚本,stdout 第一行作为 status bar 显示。常见模式:读 env 密钥(env-first),空了读 macOS keychain(keychain-fallback),把模型剩余额度/仓库分支/时间等渲染成单行。
base_confidence: 0.6
provenance:
  extracted: 0.4
  inferred: 0.6
lifecycle: draft
lifecycle_changed: 2026-08-24
tier: supporting
---

## 概述

Claude Code statusline 是一个用户可配置的 shell 脚本,在每次 turn 结束时被调用:

- **stdin**: 一段 JSON,含 `cwd` / `model` / `cost` / `duration_ms` / `session_id` 等字段
- **stdout 第一行**: 作为 IDE / terminal 的 status bar 渲染

默认脚本在 `~/.claude/statusline.sh`,用户可通过 `~/.claude/settings.json` 的 `statusLine` 字段覆盖。

## 典型 pattern:env-first + keychain-fallback

```bash
key="${ENV_VAR:-}"
if [ -z "$key" ]; then
  key="$(security find-generic-password -s ENV_VAR -w | sed 's|^go-keyring-base64:||' | base64 -d)"
fi
```

**为什么这个 pattern 易感**:见 [[concepts/unrendered-chezmoi-template-env-leak]] —— 当 env 由 chezmoi 模板注入且未渲染时,env 值是字面模板字符串而非密钥,后续所有调用都会失败。

## 防御

见 [[skills/statusline-template-injection-defense]] —— 在 env 读到值之后、用于 Bearer token 之前,加 `grep -q "{{"` 启发式守卫,模板字符串清空让 keychain 回退接管。

## 相关

- [[skills/claude-code-settings]] — settings.json 整体结构
- [[skills/statusline-template-injection-defense]] — 未渲染模板注入的修复 pattern
- [[concepts/unrendered-chezmoi-template-env-leak]] — 概念抽象