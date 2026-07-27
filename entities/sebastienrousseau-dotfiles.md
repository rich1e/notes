---
title: "sebastienrousseau/dotfiles — Trusted Shell Platform"
category: entities
tags: [dotfiles, shell, chezmoi, zsh, tools]
sources:
  - "https://github.com/sebastienrousseau/dotfiles.github.io"
  - "https://dotfiles.io"
created: 2026-07-27T06:20:00Z
updated: 2026-07-27T06:20:00Z
summary: "Sebastien Rousseau 的跨平台 shell 分发版，基于 chezmoi 管理，集成 Zsh/Neovim/tmux，提供 53 条 dot CLI 命令和 1250+ 别名。"
provenance:
  extracted: 0.90
  inferred: 0.08
  ambiguous: 0.02
base_confidence: 0.72
lifecycle: draft
lifecycle_changed: 2026-07-27
tier: supporting
relationships:
  - target: "[[entities/chezmoi]]"
    type: uses
  - target: "[[concepts/dotfile-manager]]"
    type: implements
  - target: "[[entities/trusted-shell-platform]]"
    type: related_to
---

# sebastienrousseau/dotfiles — Trusted Shell Platform

- **官网**: https://dotfiles.io
- **文档仓库**: https://github.com/sebastienrousseau/dotfiles.github.io
- **主仓库**: https://github.com/sebastienrousseau/dotfiles
- **作者**: Sebastien Rousseau（伦敦）
- **版本**: v0.2.495
- **许可证**: MIT

## 定位

面向开发者的"开箱即用" shell 分发版，核心理念是：

> "Your Shell, Everywhere" — 一套配置，所有设备保持同步

以 [[entities/chezmoi]] 为底层状态管理，提供 **幂等安装**（运行一次或一百次结果相同）。

## 技术栈

| 组件 | 工具 |
|------|------|
| Shell | Zsh |
| 编辑器配置 | Neovim |
| 终端复用 | tmux / [[entities/zellij]] |
| 文件管理 | Yazi |
| 历史管理 | Atuin |
| 终端模拟器 | Ghostty |
| 配置管理 | [[entities/chezmoi]] |

所有工具组件均为 Rust 生态工具（Atuin、Yazi、Zellij、Ghostty），重视现代化替代品。^[inferred]

## dot CLI

提供 53 条统一命令，分 8 大类管理 dotfiles 生命周期。详见 [[references/dot-cli-commands]]。

核心分类：Core（11）、Diagnostics（14）、Appearance（4）、Security（7）、Secrets（5）、AI（3+）、Tools（5）、Meta（3）。

## 别名体系

1,250+ shell 别名，覆盖 48 个分类。详见 [[concepts/shell-alias-taxonomy]]。

类别包括：AI、Docker、Git、Kubernetes、Terraform、tmux、Python、Rust、Go、macOS 等。

## 支持平台

- macOS
- Linux
- WSL（Windows Subsystem for Linux）

## 文档站

文档站 [dotfiles.io](https://dotfiles.io) 以 VitePress 构建，支持 **22 种语言**。详见 [[skills/vitepress-multilingual-docs]]。

## 安全特性

- SSH 原生签名（Git commit signing via SSH key）
- XDG 基础目录规范合规
- 无私有依赖
- `dot encrypt-check`、`dot firewall`、`dot dns-doh` 等安全命令
