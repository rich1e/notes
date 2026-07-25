---
title: 多台机器 dotfiles 难同步？chezmoi 模板加密、一条命令还原 | X-CMD 一键安装
source: https://cn.x-cmd.com/install/chezmoi#%E6%95%8F%E6%84%9F%E4%BF%A1%E6%81%AF%E7%AE%A1%E7%90%86-%E4%B8%8D%E6%B3%84%E9%9C%B2-secret-%E7%9A%84%E6%8F%90%E4%BA%A4
author:
  - "[[X-CMD]]"
published:
created: 2026-07-25
description: 作为裸 Git 管理 dotfiles 的替代，chezmoi 支持模板、加密与密码管理器。通过 x-cmd 一键安装，跨机器一致配置。
tags:
  - clippings
  - chezmoi
  - dotfiles
---
## chezmoi

跨多个不同的机器安全地管理您的 dotfiles

| Language | Go |
| --- | --- |
| Homepage | [https://github.com/twpayne/chezmoi](https://github.com/twpayne/chezmoi) |

```sh
x install chezmoi
```

| [x pkg](https://cn.x-cmd.com/pkg/chezmoi) | ```sh x pkg use chezmoi ``` |
| --- | --- |
| /eget | ```sh x eget use twpayne/chezmoi ``` |
| /asdf | ```sh x asdf use chezmoi ``` |
| /curl | ```sh sh -c "$(curl -fsLS get.chezmoi.io)" ``` |
| /wget | ```sh sh -c "$(wget -qO- get.chezmoi.io)" ``` |
| win/powershell | ```sh x pwsh (irm -useb https://get.chezmoi.io/ps1) \| powershell -c - ``` |
| alpine/apk | ```sh sudo apk add chezmoi ``` |
| arch/pacman | ```sh sudo pacman -S chezmoi ``` |
| nix/ | ```sh nix-env -i chezmoi ``` |
| opensuse/zypper | ```sh sudo zypper install chezmoi ``` |
| termux/pkg | ```sh sudo pkg install chezmoi ``` |
| void/xbps | ```sh sudo xbps-install -S chezmoi ``` |
| darwin/brew | ```sh brew install chezmoi ``` |
| darwin/port | ```sh sudo port selfupdate && sudo port install chezmoi ``` |
| /snap | ```sh snap install chezmoi --classic ``` |
| (win\|wsl2)/scoop | ```sh x scoop install chezmoi ``` |
| (win\|wsl2)/choco | ```sh x choco install chezmoi ``` |
| (win\|wsl2)/winget | ```sh x winget install twpayne.chezmoi ``` |
| freebsd/pkg | ```sh pkg install chezmoi ``` |
| openindiana/pkg | ```sh pkg install application/chezmoi ``` |
| /build | ```sh git clone https://github.com/twpayne/chezmoi.git \ && cd chezmoi \ && make install-from-git-working-copy ``` |

## chezmoi：跨机器管理 dotfiles 的利器

如果你有多台机器需要维护——公司的 MacBook、家里的 Linux 台式机、云服务器——配置文件的同步绝对是个头疼的问题。 `~/.gitconfig` 、 `~/.zshrc` 、 `~/.ssh/config` ，每台机器都稍有不同，纯靠手动复制粘贴容易出错，用 Git 裸仓库又难以处理机器间的差异。chezmoi 就是为解决这个问题而生的：它在 Git 版本控制的基础上，增加了模板、加密、密码管理器集成等能力，让你用一条命令就能在新机器上还原完整的开发环境。

## 核心定位：不只是 dotfiles 管理器

| 能力 | 裸 Git 仓库 | 符号链接 | chezmoi |
| --- | --- | --- | --- |
| 版本控制 | ✅ | ❌ | ✅ |
| 机器差异化配置 | ❌ | ❌ | ✅ 模板支持 |
| 敏感信息加密 | ❌ | ❌ | ✅ age/gpg/git-crypt |
| 密码管理器集成 | ❌ | ❌ | ✅ 1Password/Bitwarden 等 |
| 脚本执行 | ❌ | ❌ | ✅ 安装时/更新时运行脚本 |
| 单二进制文件 | \- | \- | ✅ 零依赖 |

chezmoi 的设计理念是「声明式管理」：你把目标状态描述清楚，它负责帮你达成。不管是文件内容需要根据不同机器变化，还是需要从密码管理器获取 API key，都可以在配置中表达，而不需要手动干预。

## 快速开始：一条命令部署新机器

如果你的 dotfiles 已经托管在 GitHub 上，chezmoi 可以让你用一条命令在新机器上完成工具安装和配置还原：

```bash
# 公开仓库
sh -c "$(curl -fsLS get.chezmoi.io)" -- init --apply $GITHUB_USERNAME

# 私有仓库（SSH 认证）
sh -c "$(curl -fsLS get.chezmoi.io)" -- init --apply git@github.com:$GITHUB_USERNAME/dotfiles.git
```

这条命令会：

1. 下载安装 chezmoi
2. 克隆你的 dotfiles 仓库
3. 应用所有配置（包括模板渲染、脚本执行）

更新配置同样简单：

```bash
chezmoi update
```

## 模板系统：一台仓库适配多台机器

这是 chezmoi 区别于其他工具的核心能力。你可以在配置文件中使用 Go 模板语法，根据机器特征动态生成内容：

```bash
# 查看当前机器的 chezmoi 变量
chezmoi data
```

典型用法—— `~/.gitconfig` 根据邮箱域名区分公司和个人的提交身份：

```toml
# 保存为 ~/.local/share/chezmoi/dot_gitconfig.tmpl
[user]
    name = Your Name
{{- if contains "company.com" .chezmoi.hostname }}
    email = your.name@company.com
{{- else }}
    email = your.personal@gmail.com
{{- end }}
```

chezmoi 会自动识别 `.tmpl` 后缀，渲染后写入目标位置。支持的变量包括主机名、操作系统、架构、自定义配置值等，足够应对大多数差异化场景。

## 敏感信息管理：不泄露 secret 的提交

把 API key、SSH 私钥直接提交到 Git 仓库是安全隐患。chezmoi 提供多种方案解决这个问题：

**加密文件（age/gpg）**

```bash
# 用 age 加密敏感文件
chezmoi add --encrypt ~/.ssh/id_rsa

# chezmoi 会在提交前自动加密，应用时自动解密
```

**密码管理器集成**

chezmoi 支持从主流密码管理器动态获取 secret，避免将敏感信息写入 Git：

```toml
# 模板中引用 1Password 的 item
[api]
    key = {{ onepasswordRead "op://Private/api-key/credential" }}
```

支持的密码管理器包括 1Password、Bitwarden、LastPass、KeePassXC、gopass、pass 等。secret 只在本地内存中短暂存在，不会写入磁盘或 Git 历史。

## 脚本执行：处理复杂初始化逻辑

有些配置无法用静态文件表达，比如需要安装特定字体、编译工具链、或者运行系统命令。chezmoi 支持在特定时机执行脚本：

```bash
# 创建运行时脚本（每次 apply 都执行）
chezmoi add --autotemplate --executable ~/.local/bin/my-setup.sh

# 创建安装时脚本（仅首次运行）
# 命名成 run_once_install-packages.sh
chezmoi add ~/.local/bin/run_once_install-packages.sh
```

脚本支持 `run_` （每次）、 `run_once_` （仅首次）、 `run_onchange_` （文件变化时）三种前缀，配合 `.tmpl` 后缀还能根据机器特征生成不同的脚本内容。

## 从现有配置迁移

如果你已经有散落的 dotfiles，可以用 chezmoi 快速接管：

```bash
# 初始化 chezmoi
chezmoi init

# 添加现有配置文件
chezmoi add ~/.zshrc
chezmoi add ~/.gitconfig
chezmoi add ~/.vimrc

# 查看 chezmoi 将要做的改动
chezmoi diff

# 确认无误后应用
chezmoi apply

# 提交到仓库
chezmoi cd
git add .
git commit -m "Initial dotfiles"
git push
```

`chezmoi add` 会把文件复制到 source directory（默认是 `~/.local/share/chezmoi` ），保留原有权限和元数据。之后原文件仍可用，chezmoi 通过应用（apply）来同步变更。

## 常用工作流

**日常编辑**

```bash
# 直接编辑源文件
chezmoi edit ~/.zshrc

# 或者编辑目标文件后同步回源
chezmoi add ~/.zshrc
```

**查看状态**

```bash
# 哪些文件将被改动
chezmoi status

# 具体改动内容
chezmoi diff
```

**跨设备同步**

```bash
# 拉取最新配置并应用
chezmoi update

# 或者分步执行
chezmoi git pull -- --rebase
chezmoi apply
```

## 架构与部署特性

chezmoi 采用单二进制静态链接设计，这是它能在各种环境中无缝运行的基础：

| 特性 | 说明 |
| --- | --- |
| 零依赖 | 单个可执行文件，无需运行时 |
| 跨平台 | Linux、macOS、Windows、FreeBSD、OpenIndiana |
| 无需 root | 用户级安装，无系统权限要求 |
| 多安装方式 | 包管理器、cURL、Winget、Homebrew、源码编译 |
| 验证机制 | 发布包用 cosign 签名，支持 SHA256 校验 |

对于安全敏感的环境，你可以下载校验文件验证二进制完整性：

```bash
curl --location --remote-name-all \
    https://github.com/twpayne/chezmoi/releases/download/v2.69.3/chezmoi_2.69.3_checksums.txt \
    https://github.com/twpayne/chezmoi/releases/download/v2.69.3/chezmoi_2.69.3_checksums.txt.sig \
    https://github.com/twpayne/chezmoi/releases/download/v2.69.3/chezmoi_cosign.pub

cosign verify-blob --key=chezmoi_cosign.pub \
    --signature=chezmoi_2.69.3_checksums.txt.sig \
    chezmoi_2.69.3_checksums.txt
```

## 适合谁用

- **多设备开发者** ：需要在公司、家里、云服务器间同步开发环境
- **基础设施工程师** ：维护大量机器的 SSH、shell、工具配置
- **安全敏感用户** ：希望用加密或密码管理器保护敏感配置
- **团队协作者** ：希望共享基础配置模板，同时保留个人定制

如果你只有一台机器，dotfiles 管理可能感觉不到明显价值。但一旦需要维护第二台、第三台机器，手动同步的痛点就会越来越明显。chezmoi 的前期投入（学习模板语法、组织仓库结构）会在后续节省大量时间，而且它的设计足够灵活，从简单到复杂的场景都能优雅处理。

**来源：**

[https://github.com/twpayne/chezmoi](https://github.com/twpayne/chezmoi)

[https://www.chezmoi.io/](https://www.chezmoi.io/)