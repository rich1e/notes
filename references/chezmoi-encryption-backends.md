---
title: >-
  chezmoi 加密后端 — GPG / Gnome Keyring / KeePassXC
category: references
tags:
  - chezmoi
  - encryption
  - gpg
  - dotfiles
  - security
sources:
  - "https://axionl.me/p/%E5%BD%92%E6%A1%A3-%E7%94%A8-chezmoi-%E7%AE%A1%E7%90%86%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6/#gnome-keyring"
source_url: "https://axionl.me/p/%E5%BD%92%E6%A1%A3-%E7%94%A8-chezmoi-%E7%AE%A1%E7%90%86%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6/#gnome-keyring"
created: 2026-07-25T08:30:00Z
updated: 2026-07-25T08:30:00Z
summary: >-
  chezmoi 通过 `chezmoi secret` 抽象包装多种加密后端。GPG（非对称/对称）、gnome-keyring（Linux 原生 + macOS Keychain）、KeePassXC（数据库化）。模板函数形式消费。
provenance:
  extracted: 0.85
  inferred: 0.10
  ambiguous: 0.05
base_confidence: 0.66
lifecycle: draft
lifecycle_changed: 2026-07-25
tier: supporting
---

# chezmoi 加密后端 — GPG / Gnome Keyring / KeePassXC

- **URL**: https://axionl.me/p/归档-用-chezmoi-管理配置文件/#gnome-keyring
- **角色**: 三种加密后端的实操命令 + 配置文件 + 模板消费方式

## 通用入口：`chezmoi secret`

所有加密后端通过 `chezmoi secret <backend> <verb>` 调用（不是独立命令），例如 `chezmoi secret keyring set/get`、`chezmoi secret gpg ...`、`chezmoi secret keepassxc ...`。

`chezmoi doctor` 会扫描本机上已安装的 secret 后端并报告缺失项。

## GPG（公钥/对称两种模式）

### 非对称加密（推荐）

```toml
# ~/.config/chezmoi/chezmoi.toml
[gpg]
    recipient = "ArielAxionL"   # gpg --list-public-keys 中的 uid
```

```sh
# 列出可用 recipient（支持 Tab 补全）
gpg --list-public-keys

# 加密并加入 chezmoi（默认用 --armor，可读文本）
chezmoi add --encrypt test.toml
```

模板消费 GPG 解密内容的方式：先解密为文件再读 chezmoi 由 GPG 后端决定（与 age 不同，GPG 通常直接解密为最终文本文件）。

### 对称加密

```toml
[gpg]
    symmetric = true
```

提示输入口令而非指定 recipient —— 适合个人单机。

## Gnome Keyring（Linux 原生 + macOS Keychain）

底层依赖 [zalando/go-keyring](https://github.com/zalando/go-keyring)。Linux 上目前**只支持 gnome-keyring**（社区希望补 kwallet），macOS 自动落到 Keychain。

```sh
chezmoi secret keyring set --service=github --user=<github-user>
Password: <github-token>

chezmoi secret keyring get --service=github --user=<github-user>
```

可用 [Seahorse](https://wiki.gnome.org/Apps/Seahorse) GUI 管理条目。

模板消费：

```go-text-template
{{ keyring "github" .github.user }}
```

通常配合：

```toml
# ~/.config/chezmoi/chezmoi.toml
[gpg]   # 若用 GPG 存文件，配置项
[github]
    user = "axionl"
```

keyring 在用户登录时自动解锁，模板渲染即可拿到 token。

## KeePassXC（数据库化）

配置文件：

```toml
# ~/.config/chezmoi/chezmoi.toml
[keepassxc]
    args = ["--key-file", "/path/to/your/key"]
    database = "/path/to/your/kdbx"
```

模板函数：

```go-text-template
{{ (keepassxc "<YourEntry>").Password }}     # 默认字段：Notes/Password/URL/Username
{{ keepassxcAttribute "VPS Keyring" "public-key" }}   # 自定义字段
```

适用场景：把密钥集中在一个 KeePassXC 数据库中，chezmoi 直接读取，避免密钥在不同工具间重复维护。

## 其余后端

官方还支持 1Password、Bitwarden、Vault、pass、LastPass 等；实际选型取决于操作系统、团队习惯、是否已经购买了密码管理器订阅。

## 与 [[concepts/chezmoi-templating]] 的关系

加密后端都是"模板函数形式的运行时数据源"，不是加密原语本身：

- GPG/age（加密原语）→ 加密文件存仓库，chezmoi apply 时解密
- Keyring/KeePassXC/1Password（密码管理器）→ chezmoi 模板渲染时实时查询

这两类的安全模型不同：GPG/age 依赖私钥保护，Keyring/PM 依赖密码管理器的主密码 + 系统解锁。

## 相关链接

- [[entities/chezmoi]]
- [[concepts/chezmoi-templating]]
- [[concepts/chezmoi-attribute-prefixes]]
- [[references/chezmoi-templating-guide]]
- [[references/chezmoi-official-site]]
## 相关页面

- [[references/chezmoi-patterns-recipes.md]]
- [[concepts/chezmoi-workflow.md]]
- [[skills/chezmoi-bitwarden-secrets]] — Bitwarden 运行时注入与跨平台解锁实践
