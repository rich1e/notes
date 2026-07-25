---
title: >-
  GNU Stow — Entity
category: entities
tags: [stow, dotfiles, tools, entity]
sources:
  - "https://chezmoi.io/"
  - "https://github.com/twpayne/chezmoi/discussions/2673"
  - "https://farseerfc.me/using-gnu-stow-to-manage-your-dotfiles.html"
  - "https://axionl.me/p/%E5%BD%92%E6%A1%A3-%E7%94%A8-chezmoi-%E7%AE%A1%E7%90%86%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6/"
created: 2026-07-25T02:27:13Z
updated: 2026-07-25T08:30:00Z
summary: >-
  GNU Stow：symlink 农场式 dotfile 管理器。把镜像目录结构用符号链接投到 home。简单、可审计，无模板与加密。
provenance:
  extracted: 0.7
  inferred: 0.25
  ambiguous: 0.05
base_confidence: 0.55
lifecycle: draft
lifecycle_changed: 2026-07-25
---

# GNU Stow — Entity

- **官网**: https://www.gnu.org/software/stow/
- **实现语言**: Perl
- **许可**: GPL-3
- **范式**: 符号链接农场（symlink farm）

## 核心模型

```
~/dotfiles/zsh/.zshrc     →     ~/.zshrc
~/dotfiles/nvim/init.vim  →     ~/.config/nvim/init.vim
```

- 源目录结构**镜像**目标 home 结构
- 一个工具负责在镜像与 home 之间建立符号链接
- 撤掉 stow 链接即恢复原状

## 与 chezmoi 的关键差异

| 维度 | GNU Stow | chezmoi |
|---|---|---|
| 源/目标关系 | 镜像 + 符号链接 | 独立源态 + 渲染后复制 |
| 编辑目标 → 自动持久化 | 是（写目标 = 改源） | 否（必须用 `chezmoi edit`） |
| 模板化 | 无 | Go 模板 + sprig |
| 加密 | 无 | age / GPG / SOPS |
| 脚本 | 无 | `run_*` 脚本 |
| 跨平台分支 | 手工换 git 分支 | 模板内 if 分支 |
| 学习曲线 | 平缓 | 较陡 |
| 调试 | 普通文件 diff | `chezmoi diff` 渲染后对比 |

## 适用场景

- 单平台（macOS 或单一 Linux 发行版）
- 不需要区分工作机/家庭机
- 没有机密配置文件
- 偏好"普通文件 + 符号链接"的最小心智模型

## 局限

- 表达力差：无法表达"按 hostname 切换"
- 加密缺失：要么把机密文件单独管理，要么放弃仓库公开
- 跨平台靠 git 分支而非声明式分支，长期维护成本高

## 与 [[concepts/dotfile-manager]] 的关系

Stow 是流派 2（目录镜像 + 符号链接）的代表；chezmoi 是流派 3（模板化 + 加密 + 脚本）的代表。两者构成"从简到繁"的连续谱。

## 历史背景与对国内中文社区的影响

[Farseerfc 的中文化译文](https://farseerfc.me/using-gnu-stow-to-manage-your-dotfiles.html)（"【译】使用 GNU stow 管理你的点文件"）是中文 dotfiles 圈最早普及 Stow 的入门文章，由 axionl 在 2021 年的一篇归档文章中作为 Stow 的代表入门文章引用——这也正是 axionl 后来从 Stow 转向 chezmoi 的起点。

Stow 的"极简"心智模型（直接建镜像目录 + `stow <pkg>` 一键出 symlink）是其最大优势，也是其在表达力上的瓶颈：无法表达"按 hostname 切换"、"加密"、"模板变量替换"，这些场景必须让位给 chezmoi 或 Nix home-manager。

## 相关链接

- [[concepts/dotfile-manager]]
- [[entities/chezmoi]]
- [[synthesis/Research: chezmoi]]