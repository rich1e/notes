---
title: chezmoi：你的 dotfiles 管理神器
source: https://juejin.cn/post/7624438584691310628
author:
  - "[[ovensi]]"
published: 2026-04-03
created: 2026-07-25
description: 相信很多人和我一样，在多台机器之间工作时，最头疼的事情之一就是同步各种配置文件——.bashrc、.zshrc、.gitconfig、.vimrc……每次换电脑或者重装系统，光是恢复这些配置就要折腾大
tags:
  - clippings
  - chezmoi
  - dotfiles
---
相信很多人和我一样，在多台机器之间工作时，最头疼的事情之一就是同步各种配置文件——`.bashrc` 、`.zshrc` 、`.gitconfig` 、`.vimrc` ……每次换电脑或者重装系统，光是恢复这些配置就要折腾大半天。今天要介绍的 **chezmoi** ，就是来解决这个问题的。

## 什么是 chezmoi？

chezmoi 是一个开源的 dotfiles 管理工具，它的核心思想很简单： **把你在各台机器上个性化的配置文件（dotfiles）集中管理起来，通过 Git 进行版本控制，然后在每台机器上同步应用** 。

与普通的 `cp` 或 symlink 方案不同，chezmoi 支持：

- **模板化** ：配置文件中的敏感信息（如 API key、邮箱）可以用变量替代
- **差异化** ：可以为不同主机设置不同的配置
- **幂等性** ：多次运行结果一致，不会重复追加内容
- **跨平台** ：支持 Linux、macOS、Windows

## 安装 chezmoi

### macOS

```bash
代码解读复制代码brew install chezmoi
```

### Linux

```bash
代码解读复制代码# 使用安装脚本
curl -sfL https://get.chezmoi.io | sh

# 或使用包管理器
sudo apt install chezmoi  # Debian/Ubuntu
sudo yum install chezmoi  # CentOS/RHEL
```

### Windows

```bash
代码解读复制代码winget install chezmoi
```

安装完成后，初始化 chezmoi：

```bash
代码解读复制代码chezmoi init
```

这会在 `~/.local/share/chezmoi` （Linux/macOS）或 `%LOCALAPPDATA%\chezmoi` （Windows）创建一个 Git 仓库。

## 基本使用

### 1\. 添加配置文件

假设你有一个 `.bashrc` 想纳入管理：

```bash
代码解读复制代码# 将现有的 .bashrc 添加到 chezmoi
chezmoi add ~/.bashrc

# 或者直接在 chezmoi 目录创建文件
chezmoi cd  # 进入 chezmoi 的 Git 仓库
touch rootBashrc  # 注意：chezmoi 中文件名前缀 "root" 表示root用户，"dot" 表示当前用户
```

chezmoi 会自动把 `~/.bashrc` 复制到它的管理目录，并在文件名加 `dot_` 前缀，即 `dot_bashrc` 。

### 2\. 编辑配置文件

```bash
代码解读复制代码# 编辑 chezmoi 管理的 .bashrc
chezmoi edit ~/.bashrc

# 或者直接编辑源文件
chezmoi cd  # 进入 chezmoi 管理目录
vim dot_bashrc
```

### 3\. 查看变更

```bash
代码解读复制代码# 查看将要做的所有变更（不实际应用）
chezmoi diff
```

### 4\. 应用变更

```bash
代码解读复制代码# 应用所有变更到实际文件
chezmoi apply

# 只应用特定文件
chezmoi apply ~/.bashrc
```

### 5\. 自动拉取和推送

如果你把 chezmoi 的 Git 仓库托管到 GitHub/Gitee，可以设置自动同步：

```bash
代码解读复制代码# 添加 remote
git remote add origin git@github.com:yourusername/dotfiles.git

# 每次启动终端时自动拉取最新配置
echo 'eval "$(chezmoi init --execute)"' >> ~/.bashrc
```

## 加入 Git 管理

chezmoi 本身就在 `~/.local/share/chezmoi` 目录下初始化了一个 Git 仓库，我们只需要把它托管到 GitHub 或 Gitee 上，就能在多台机器之间同步了。 **国内推荐 Gitee** ，访问速度更快。

### 1\. 在 Gitee 创建仓库

登录 [Gitee](https://link.juejin.cn/?target=https%3A%2F%2Fgitee.com "https://gitee.com") ，新建一个仓库，命名为 `dotfiles` （也可以叫其他名字），选择 Private（私有）或 Public（公开）都可以。

### 2\. 关联远程仓库

```bash
代码解读复制代码# 进入 chezmoi 的 Git 仓库
chezmoi cd

# 添加 Gitee 远程仓库（替换为你自己的地址）
git remote add origin git@gitee.com:yourusername/dotfiles.git

# 如果已经有 GitHub 的地址，也可以同时保留两个 remote
git remote add github git@github.com:yourusername/dotfiles.git
```

### 3\. 首次推送

```bash
代码解读复制代码git add -A
git commit -m "Initial commit: manage dotfiles with chezmoi"
git push -u origin main   # Gitee 默认分支是 main
```

### 4\. 在新机器上快速恢复

以后在任意新机器上，只需要一行命令就能恢复所有配置：

```bash
代码解读复制代码# 使用 Gitee（国内推荐）
bash -c "$(curl -fsSL https://raw.githubusercontent.com/yourusername/dotfiles/main/install.sh)"

# 或使用 GitHub
chezmoi init --source=https://github.com/yourusername/dotfiles.git
```

更优雅的做法是先用 chezmoi 引导初始化：

```bash
代码解读复制代码# chezmoi 会自动 clone 远程仓库并应用配置
chezmoi init git@gitee.com:yourusername/dotfiles.git
chezmoi apply
```

### 5\. 日常更新流程

```bash
代码解读复制代码# 1. 修改配置
chezmoi edit ~/.bashrc

# 2. 查看变更
chezmoi diff

# 3. 应用到本地
chezmoi apply

# 4. 提交到本地 Git
git add -A
git commit -m "Update bashrc"

# 5. 推送到远程
git push
```

### 6\. 在多台机器间同步

假设你在公司电脑和家庭电脑都要用同一套配置：

```bash
代码解读复制代码# 公司电脑修改后
git push

# 家庭电脑使用时
git pull && chezmoi apply
```

或者设置每次打开终端自动拉取：

```bash
代码解读复制代码echo 'eval "$(chezmoi init --execute)"' >> ~/.bashrc
```

这样每次开终端就会自动从远程拉取最新配置并应用。

## 模板化配置

chezmoi 最强大的功能之一是支持 Go 模板语法，这让你可以为不同主机设置不同配置。

### 创建模板文件

```bash
代码解读复制代码chezmoi add --template ~/.gitconfig
```

这会创建一个 `.gitconfig.tmpl` 文件，内容可以这样写：

```
代码解读复制代码{{- $name := .name -}}
{{- $email := .email -}}
[user]
    name = {{ $name }}
    email = {{ $email }}
[alias]
    lg = log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit
```

### 配置主机信息

```bash
代码解读复制代码# 创建配置文件
cat > ~/.config/chezmoi/chezmoi.toml << 'EOF'
[data]
    name = "Your Name"
    email = "your.email@example.com"
EOF
```

### 使用加密敏感信息

```bash
代码解读复制代码# 用 age 加密敏感文件
chezmoi secret key # 生成本机密钥
chezmoi add --encrypt ~/.netrc
```

## 多主机管理

chezmoi 支持为不同主机设置不同配置，非常适合公司电脑和个人电脑有不同需求的场景。

### 按主机名条件判断

```
代码解读复制代码{{ if eq .chezmoi.hostname "work-pc" }}
# 公司电脑特有的配置
[user]
    email = "work@company.com"
{{ else }}
# 个人电脑的配置
[user]
    email = "personal@mail.com"
{{ end }}
```

### 使用.chezmoi.\<host>.tmpl

创建 `.chezmoi.<hostname>.tmpl` 文件，可以包含该主机特有的变量：

```bash
代码解读复制代码# 在公司电脑上
echo 'name = "Work Name"' > ~/.config/chezmoi/chezmoi.work-pc.toml
echo 'email = "work@company.com"' >> ~/.config/chezmoi/chezmoi.work-pc.toml
```

## 实用技巧

### 1\. 导入现有配置

```bash
代码解读复制代码# 一键导入多个 dotfiles
chezmoi import ~/.bashrc ~/.zshrc ~/.vimrc
```

### 2\. 干跑模式

```bash
代码解读复制代码# -n 显示将要做什么，但不实际执行
chezmoi apply -n
```

### 3\. 撤销变更

```bash
代码解读复制代码# 恢复到修改前的状态
chezmoi update
```

### 4\. 查看状态

```bash
代码解读复制代码chezmoi status
```

输出示例：

```bash
代码解读复制代码  M .bashrc          # M = 已修改
 A .zshrc           # A = 新增
 ? .viminfo         # ? = 未跟踪
```

## 我的配置结构

分享一下我目前的 chezmoi 配置结构：

```ruby
代码解读复制代码~/.local/share/chezmoi/
├── dot_bashrc          # ~/.bashrc
├── dot_zshrc           # ~/.zshrc
├── dot_gitconfig       # ~/.gitconfig
├── dot_gitconfig.tmpl  # 模板版本
├── dot_tmux.conf       # ~/.tmux.conf
├── dot_config/
│   └── nvim/           # ~/.config/nvim/
└── scripts/
    └── install.sh      # 初始化脚本
```

## 总结

chezmoi 解决的不是什么高深莫测的问题，但它把「管理 dotfiles」这件事做得很优雅。对于需要频繁在多台机器间切换的开发者来说，它能节省大量重复配置的时间。

如果你还没有尝试过 dotfiles 管理工具，chezmoi 是一个很好的起点。它比直接用 symlink 更安全，比 Ansible/Puppet 轻量，比 `rsync` 灵活。

**官网** ： [chezmoi.io](https://link.juejin.cn/?target=https%3A%2F%2Fchezmoi.io "https://chezmoi.io") **GitHub** ： [github.com/twpayne/che…](https://link.juejin.cn/?target=https%3A%2F%2Fgithub.com%2Ftwpayne%2Fchezmoi "https://github.com/twpayne/chezmoi")
