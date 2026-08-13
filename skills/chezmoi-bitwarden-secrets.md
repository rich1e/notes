---
title: chezmoi Bitwarden 密钥注入与跨平台解锁
category: skills
tags: [chezmoi, security, cli, automation]
sources:
  - "https://yangzh.cn/posts/posts/chezmoi-dotfiles-secrets.html"
  - "https://cn.x-cmd.com/install/chezmoi"
created: 2026-07-25
updated: 2026-07-25
summary: 使用 chezmoi 模板从 Bitwarden 等密码管理器运行时注入 secret，并用 macOS Keychain 或 Windows DPAPI 自动解锁 Bitwarden CLI；同时说明首次 bootstrap、历史泄露清理与多机安全边界。
provenance:
  extracted: 0.88
  inferred: 0.09
  ambiguous: 0.03
base_confidence: 0.67
lifecycle: draft
lifecycle_changed: 2026-07-25
tier: peripheral
---

# chezmoi Bitwarden 密钥注入与跨平台解锁

## 目标

不要把 API token、密码或主密码写进 dotfiles 源文件。将 secret 放入 Bitwarden 安全笔记，chezmoi 在 `apply` 渲染模板时查询并写入目标文件；Git 中只保留模板表达式。

```gotemplate
export ANTHROPIC_AUTH_TOKEN="{{ (bitwarden "item" "ANTHROPIC_AUTH_TOKEN").notes }}"
```

模板渲染前必须已有 `BW_SESSION`。Bitwarden CLI 支持多种后端集成方案，类似模式也适用于 1Password、LastPass、KeePassXC、gopass 和 pass。

## 首次 bootstrap

模板本身不能在 Bitwarden 尚未解锁时调用 Bitwarden，因此首次配置要打破循环依赖：

1. 在 macOS Keychain 或 Windows DPAPI 中保存 Bitwarden 主密码。
2. 手动执行一次 `export BW_SESSION=$(bw unlock --raw)`。
3. 执行 `chezmoi apply`，让模板生成包含 `bw-unlock` 的 shell 配置。
4. 后续新终端只需运行 `bw-unlock && chezmoi apply`。

`BW_SESSION` 只存在于当前终端环境，关闭终端后自然失效；不要把主密码写进 `.zshrc` 或长期环境变量。

## macOS Keychain

```bash
security add-generic-password -s "bitwarden-cli" -a "$USER" -w

bw-unlock() {
    local pw
    pw=$(security find-generic-password -s "bitwarden-cli" -a "$USER" -w 2>/dev/null) || return 1
    export BW_SESSION=$(BW_PASSWORD="$pw" bw unlock --passwordenv BW_PASSWORD --raw 2>/dev/null)
}
```

主密码变更时删除并重新写入 generic password。

## Windows DPAPI

PowerShell 的 `ConvertFrom-SecureString` 使用当前用户和机器的 DPAPI 保护凭据文件：

```powershell
Read-Host "输入 Bitwarden 主密码" -AsSecureString |
  ConvertFrom-SecureString |
  Set-Content "$env:USERPROFILE\.bw-cred.xml"
```

Git Bash 中可通过 `powershell.exe` 读取并转成临时 `BW_PASSWORD`，再运行 `bw unlock --passwordenv BW_PASSWORD --raw`。chezmoi 模板用 `.chezmoi.os` 选择 Keychain 或 DPAPI 实现，让调用者始终只记住 `bw-unlock`。

## Bitwarden 缓存与更新顺序

换机器或长时间未使用后，`bw get item` 报 Not found 可能只是本地缓存过期，先运行 `bw sync`。多机更新时区分：`chezmoi update` 才会联网拉取并应用，`chezmoi apply` 只处理本地源态。

## 泄露后的处理

当前文件已删除并不代表 secret 从 Git 历史消失。使用 `git-filter-repo --replace-text` 重写历史，验证 `git log --all -p` 不再出现旧 token，重新添加 remote 后强制推送，并立即轮换已泄露的密钥。历史重写清除的是可见痕迹，不会撤销已经被读取的 token。

## 相关链接

- [[concepts/chezmoi-templating]]
- [[concepts/chezmoi-workflow]]
- [[entities/chezmoi]]
- [[concepts/chezmoi-attribute-prefixes]]
- [[references/chezmoi-encryption-backends]] — GPG / Keyring / KeePassXC 加密后端对比
