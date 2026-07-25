---
title: chezmoi 使用教程
source: https://zhuanlan.zhihu.com/p/2017558515602990956
author:
  - "[[Sylearn​]]"
published:
created: 2026-07-25
description: 最近重装系统的时候希望可以将旧设备的配置文件同步到新设备上，就发现了这个非常实用的工具。 chezmoi ：一个跨平台的 dotfiles 管理工具，帮助你在多台机器间安全地同步配置文件。 核心概念源目录：~/.local/sha…
tags:
  - clippings
  - chezmoi
  - dotfiles
---
chezmoi ：一个跨平台的 dotfiles 管理工具，帮助你在多台机器间安全地同步配置文件。

## 核心概念

- **源目录** ： `~/.local/share/chezmoi/` ，存放所有配置文件的模板/副本
- **目标目录** ： `~/` （你的 home 目录），实际生效的配置文件所在位置
- **[远程仓库](https://zhida.zhihu.com/search?content_id=271646436&content_type=Article&match_order=1&q=%E8%BF%9C%E7%A8%8B%E4%BB%93%E5%BA%93&zhida_source=entity)** ：GitHub 上的 `dotfiles` 仓库，用于跨机器同步

工作流程： **编辑源目录 → 应用到目标目录 → 推送到远程仓库**

### 工作原理

chezmoi **不使用符号链接** ，而是通过 **复制** 的方式工作。源目录和目标目录是两份独立的文件， `chezmoi apply` 时用源目录的内容覆盖目标目录的文件。

```bash
chezmoi edit ~/.zshrc
  → 实际编辑 ~/.local/share/chezmoi/dot_zshrc（源目录中的副本）
​
chezmoi apply
  → 将 dot_zshrc 的内容复制到 ~/.zshrc（目标目录）
```

### 文件名映射规则

chezmoi 在源目录中使用特殊前缀来映射目标路径：

| 源目录文件名 | 对应的目标文件 |
| --- | --- |
| dot\_zshrc | ~/.zshrc |
| dot\_zprofile | ~/.zprofile |
| dot\_gitconfig | ~/.gitconfig |
| dot\_config/nvim/ [init.lua](https://zhida.zhihu.com/search?content_id=271646436&content_type=Article&match_order=1&q=init.lua&zhida_source=entity) | ~/.config/nvim/init.lua |

常用前缀说明：

| 前缀 | 作用 |
| --- | --- |
| dot\_ | 替换为.（表示隐藏文件/目录） |
| private\_ | 设置文件权限为 0600（仅所有者可读写） |
| executable\_ | 设置可执行权限 |
| exact\_ | 精确管理目录（删除目标中多余的文件） |
| readonly\_ | 设置为只读权限 |
| empty\_ | 确保空文件存在 |

前缀可以组合使用，例如： `private_dot_ssh/private_executable_dot_config`

查看文件映射关系：

```bash
# 查看某个文件在源目录中的路径
chezmoi source-path ~/.zshrc
​
# 查看所有受管理文件的映射
chezmoi managed --path-style=source-and-target
```

### 管理范围

chezmoi 能管理 home 目录（ `~/` ）下的 **任何文件** ，不限于 dotfiles：

```bash
chezmoi add ~/scripts/backup.sh       # 脚本
chezmoi add ~/Desktop/notes.md         # 普通文件
chezmoi add ~/.local/bin/my-tool       # 自定义工具
```

**适合管理的文件：**

- 配置文件（dotfiles）
- 小型脚本
- 文本类文件
- 体积小、变化少、跨机器需要保持一致的内容

**不适合管理的文件：**

- 大文件或 [二进制文件](https://zhida.zhihu.com/search?content_id=271646436&content_type=Article&match_order=1&q=%E4%BA%8C%E8%BF%9B%E5%88%B6%E6%96%87%E4%BB%B6&zhida_source=entity) （会占用 git 仓库空间，影响克隆速度）
- 频繁变化的文件（如缓存、日志、数据库）
- 敏感文件（除非使用 `--encrypt` 加密管理）

---

## 一、基础操作

### 1\. 添加文件到管理

将 home 目录下的文件纳入 chezmoi 管理：

```bash
chezmoi add ~/.zshrc
chezmoi add ~/.gitconfig
chezmoi add ~/.vimrc
```

添加整个目录：

```bash
chezmoi add ~/.config/nvim
```

添加并加密敏感文件：

```bash
chezmoi add --encrypt ~/.ssh/config
```

添加为模板（支持变量替换）：

```bash
chezmoi add --template ~/.gitconfig
```

### 2\. 编辑已管理的文件

```bash
# 编辑源目录中的副本（不会自动同步到 home 目录）
chezmoi edit ~/.zshrc
​
# 编辑并自动应用到 home 目录（推荐）
chezmoi edit --apply ~/.zshrc
```

> **注意** ： `chezmoi edit` 编辑的是源目录中的副本，不是 home 目录的原文件。 编辑后必须执行 `chezmoi apply` 才会同步到 home 目录，或使用 `--apply` 参数自动同步。

### 3\. 查看变更

```bash
# 查看源目录与 home 目录的差异
chezmoi diff
​
# 查看所有被管理的文件
chezmoi managed
​
# 查看某个文件的状态
chezmoi status
```

### 4\. 应用变更

```bash
# 将源目录的内容同步到 home 目录
chezmoi apply
​
# 只应用某个文件
chezmoi apply ~/.zshrc
​
# 预览变更（不实际执行）
chezmoi apply --dry-run
​
# 显示详细信息
chezmoi apply --verbose
```

### 5\. 移除文件

```bash
# 从 chezmoi 管理中移除（不删除 home 目录中的文件）
chezmoi forget ~/.vimrc
​
# 从管理中移除并删除目标文件
chezmoi destroy ~/.vimrc
```

---

## 二、与 GitHub 同步

### 提交并推送变更

```bash
# 方式一：进入源目录操作
chezmoi cd
git add -A
git commit -m "更新 zshrc 配置"
git push
exit
​
# 方式二：一行命令完成
git -C ~/.local/share/chezmoi add -A && \
git -C ~/.local/share/chezmoi commit -m "更新配置" && \
git -C ~/.local/share/chezmoi push
```

### 从远程拉取更新

```bash
# 拉取远程变更并查看差异（不应用）
chezmoi git pull
​
# 拉取并自动应用
chezmoi update
```

---

## 三、在新机器上恢复

### 一键初始化并应用所有配置

```bash
# 安装 chezmoi（macOS）
brew install chezmoi
​
# 从 GitHub 克隆并应用所有配置
chezmoi init --apply https://github.com/sylearn/dotfiles.git
```

### Linux 上安装

```bash
# Debian/Ubuntu
sudo apt install chezmoi
​
# 或通过官方脚本安装（适用于所有 Linux 发行版）
sh -c "$(curl -fsLS get.chezmoi.io)"
​
# 初始化并应用
chezmoi init --apply https://github.com/sylearn/dotfiles.git
```

### Windows 上安装

```powershell
# 通过 Scoop
scoop install chezmoi
​
# 或通过 Chocolatey
choco install chezmoi
​
# 初始化并应用
chezmoi init --apply https://github.com/sylearn/dotfiles.git
```

### 仅克隆不应用（先检查再决定）

```bash
# 只克隆到源目录，不应用
chezmoi init https://github.com/sylearn/dotfiles.git
​
# 查看将会发生的变更
chezmoi diff
​
# 确认无误后再应用
chezmoi apply
```

---

## 四、进阶用法

### 模板功能

不同机器可能需要不同的配置（如用户名、邮箱、路径等），chezmoi 支持 [Go 模板语法](https://zhida.zhihu.com/search?content_id=271646436&content_type=Article&match_order=1&q=Go+%E6%A8%A1%E6%9D%BF%E8%AF%AD%E6%B3%95&zhida_source=entity) ：

```bash
# 将文件转为模板管理
chezmoi add --template ~/.gitconfig
```

编辑模板时可以使用变量：

```
[user]
    name = {{ .name }}
    email = {{ .email }}
```

配置变量（编辑 `~/.config/chezmoi/chezmoi.toml` ）：

```
[data]
    name = "你的名字"
    email = "your@email.com"
```

### 内置变量

chezmoi 内置了一些有用的变量，可以在模板中直接使用：

```
{{ .chezmoi.hostname }}      # 当前主机名
{{ .chezmoi.os }}            # 操作系统（darwin, linux, windows）
{{ .chezmoi.arch }}          # CPU 架构（amd64, arm64）
{{ .chezmoi.username }}      # 当前用户名
{{ .chezmoi.homeDir }}       # home 目录路径
```

### 条件判断

根据不同系统生成不同配置：

```
{{ if eq .chezmoi.os "darwin" }}
# macOS 专用配置
export BREW_PREFIX="/opt/homebrew"
{{ else if eq .chezmoi.os "linux" }}
# Linux 专用配置
export BREW_PREFIX="/home/linuxbrew/.linuxbrew"
{{ end }}
```

### 查看可用数据

```bash
# 查看所有可用的模板数据
chezmoi data
​
# 预览模板渲染结果
chezmoi cat ~/.gitconfig
```

### 脚本功能

chezmoi 支持在 `apply` 时自动运行脚本，用于安装软件包等无法通过文件复制完成的操作：

```bash
# 在源目录中创建脚本（以 run_ 开头）
chezmoi cd
mkdir -p run_once_install-packages.sh
```

脚本前缀说明：

| 前缀 | 作用 |
| --- | --- |
| run\_ | 每次 apply 都执行 |
| run\_once\_ | 只在首次 apply 时执行 |
| run\_onchange\_ | 当脚本内容发生变化时执行 |

示例：创建一个首次运行时安装 Homebrew 包的脚本

```bash
#!/bin/bash
# run_once_install-packages.sh
brew bundle --no-lock --file=/dev/stdin <<EOF
brew "ripgrep"
brew "fd"
brew "fzf"
brew "neovim"
EOF
```

### 忽略文件

在源目录中创建 `.chezmoiignore` 文件，指定不需要应用到目标目录的文件：

```bash
chezmoi cd
cat > .chezmoiignore << 'EOF'
README.md
LICENSE
scripts/
​
# 根据操作系统忽略
{{ if ne .chezmoi.os "darwin" }}
Darwin/**
{{ end }}
{{ if ne .chezmoi.os "linux" }}
Linux/**
{{ end }}
EOF
```

### 加密敏感文件

chezmoi 支持使用 age 或 gpg 加密敏感配置，加密后的文件可以安全地提交到公开仓库：

```bash
# 安装 age
brew install age
​
# 生成密钥
age-keygen -o ~/.config/chezmoi/key.txt
```

> **重要** ：请妥善保管 `key.txt` ，它不应被提交到 git 仓库。丢失密钥将无法解密文件。

编辑 chezmoi 配置：

```bash
chezmoi edit-config
```

添加以下内容：

```
encryption = "age"
[age]
    identity = "~/.config/chezmoi/key.txt"
    recipient = "age1..."  # 替换为你的公钥（在生成密钥时输出）
```

然后添加需要加密的文件：

```bash
chezmoi add --encrypt ~/.ssh/config
chezmoi add --encrypt ~/.env
```

### 外部文件管理

chezmoi 可以从外部 URL 下载文件，适合管理第三方配置或字体：

在源目录创建 `.chezmoiexternal.toml` ：

```
# 下载单个文件
["scripts/git-prompt.sh"]
    type = "file"
    url = "https://raw.githubusercontent.com/git/git/master/contrib/completion/git-prompt.sh"
​
# 下载并解压压缩包
[".fonts/FiraCode"]
    type = "archive"
    url = "https://github.com/tonsky/FiraCode/releases/download/6.2/Fira_Code_v6.2.zip"
```

---

## 五、常用命令

| 命令 | 说明 |
| --- | --- |
| chezmoi add <文件> | 添加文件到管理 |
| chezmoi add --encrypt <文件> | 添加并加密文件 |
| chezmoi add --template <文件> | 添加为模板 |
| chezmoi edit <文件> | 编辑受管理的文件 |
| chezmoi edit --apply <文件> | 编辑并自动应用 |
| chezmoi edit-config | 编辑 chezmoi 配置文件 |
| chezmoi diff | 查看变更差异 |
| chezmoi status | 查看文件状态 |
| chezmoi apply | 应用所有变更 |
| chezmoi apply --dry-run | 预览变更（不实际执行） |
| chezmoi managed | 列出所有受管理的文件 |
| chezmoi managed --path-style=source-and-target | 查看文件映射关系 |
| chezmoi source-path <文件> | 查看文件在源目录中的路径 |
| chezmoi cat <文件> | 查看模板渲染后的内容 |
| chezmoi forget <文件> | 从管理中移除（不删除原文件） |
| chezmoi destroy <文件> | 从管理中移除并删除原文件 |
| chezmoi update | 拉取远程更新并应用 |
| chezmoi cd | 进入源目录 |
| chezmoi data | 查看模板数据 |
| chezmoi doctor | 诊断问题 |
| chezmoi init --apply <仓库URL> | 从远程仓库初始化并应用 |

---

## 六、推荐工作流

### 日常使用

```
1. 修改配置     →  chezmoi edit --apply ~/.zshrc
2. 提交推送     →  chezmoi cd && git add -A && git commit -m "描述" && git push && exit
3. 其他机器同步 →  chezmoi update
```

### 添加新文件

```
1. 添加文件     →  chezmoi add ~/.new_config
2. 确认添加成功 →  chezmoi managed
3. 提交推送     →  chezmoi cd && git add -A && git commit -m "添加 new_config" && git push && exit
```

### 新机器配置

```
1. 安装 chezmoi →  brew install chezmoi  (或其他包管理器)
2. 一键恢复     →  chezmoi init --apply https://github.com/sylearn/dotfiles.git
```
