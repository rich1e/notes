---
title: QSLSの站
source: https://blog.qingshanls.icu/2026/04/05/chezmoi/
author:
  - "[[青山蓝山]]"
published:
created: 2026-07-25
description: Hexo Theme Keep
tags:
  - clippings
  - chezmoi
  - dotfiles
---
## 用 chezmoi 优雅管理你的跨设备 Dotfiles

## 快速开始

### 1\. 安装 chezmoi

chezmoi 是一个独立的静态二进制文件，无任何依赖，无需 root 权限。你可以选择以下方式之一安装：

**方式一：使用 Curl（推荐用于快速上手）**

```bash
sh -c "$(curl -fsLS https://get.chezmoi.io)" -- init --apply $GITHUB_USERNAME
```

这条命令会直接从你的 GitHub 用户仓库 (`$GITHUB_USERNAME`) 拉取 dotfiles 并立即应用。

**方式二：使用包管理器** chezmoi 支持所有主流操作系统包管理器

```bash
# macOS (Homebrew)
brew install chezmoi

# Ubuntu/Debian
sudo apt install chezmoi

# Arch Linux
sudo pacman -S chezmoi

# Windows (Winget)
winget install chezmoi.chezmoi
```

更多安装方式请查阅 [官方安装指南](https://www.chezmoi.io/install/) 。

### 2\. 使用

1. `chezmoi init`: 该命令会在 `~/.local/share/chezmoi` 下初始化一个 Git 仓库。
2. `chezmoi add ~/.zshrc`: 将 `~/.zshrc` 纳入 chezmoi 的管理。其在 `~/.local/share/chezmoi` 下对应的文件是 `dot_bashrc`, 下文统一称为源文件。
3. `chezmoi edit ~/.zshrc`: 编辑源文件。
4. `chezmoi diff`: 查看源文件和实际家目录下的对应文件的差异。
5. `chezmoi -v apply`: 将源文件应用到家目录。其中 `-v` 选项会显示对实际文件所做的更改，建议添加。
6. `chezmoi cd`: 进入 `~/.local/share/chezmoi`.
7. `git add .`然后 `git commit`: 提交更改。
8. 在 GitHub 下新建一个仓库(建议命令为 `dotfiles` ，这样在新机器的安装的时候可以使用 `sh -c "$(curl -fsLS get.chezmoi.io)" -- init --apply $GITHUB_USERNAME` 一键应用配置)，然后:

```bash
git remote add origin git@github.com:$GITHUB_USERNAME/dotfiles.git
git branch -M main
git push -u origin main
```

### 3\. 在新机器上部署

拿到新机器后，只需三步：

1. 安装 chezmoi（如上）。
2. 运行 `chezmoi init $GITHUB_USERNAME` 克隆你的 dotfiles 仓库。
3. 运行 `chezmoi apply` 应用配置。

就这么简单！你的 Shell、Git、编辑器等配置瞬间就绪。

## 进阶功能示例

### 1\. 处理机器差异（模板）

假设你的工作电脑和笔记本使用不同的 Git 用户名，可以在 `~/.local/share/chezmoi/home/.gitconfig.tmpl` 中这样写：

```
[user]
    name = {{ if eq .chezmoi.hostname "work-laptop" }}工作姓名{{ else }}个人姓名{{ end }}
    email = {{ if eq .chezmoi.hostname "work-laptop" }}work@email.com{{ else }}personal@email.com{{ end }}
```

chezmoi 会根据当前主机名自动渲染正确的值。

### 2\. 加密敏感文件

使用 `chezmoi add --encrypt ~/.secrets/api-key` 即可加密文件。chezmoi 会询问你使用哪种加密方式（推荐 `age` ），加密后的文件（如 `api-key.age` ）可以安全地提交到公开仓库，只有拥有私钥的你才能解密使用。

> 注意：本文基于 chezmoi 官网信息整理，具体命令和功能请以 [官方文档](https://www.chezmoi.io/) 和你的实际版本为准。