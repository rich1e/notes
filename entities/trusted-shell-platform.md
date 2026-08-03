---
title: "Trusted Shell Platform"
category: entities
tags: [dotfiles, shell, tools, zsh]
sources:
  - "https://github.com/sebastienrousseau/dotfiles.github.io"
  - "https://dotfiles.io"
created: 2026-07-27T06:20:00Z
updated: 2026-07-27T06:20:00Z
summary: "sebastienrousseau/dotfiles 项目的品牌名称，一个声明式、幂等的跨平台 shell 环境分发版，以 chezmoi 为核心。"
provenance:
  extracted: 0.85
  inferred: 0.12
  ambiguous: 0.03
base_confidence: 0.62
lifecycle: draft
lifecycle_changed: 2026-07-27
tier: peripheral
relationships:
  - target: "[[entities/sebastienrousseau-dotfiles]]"
    type: related_to
  - target: "[[entities/chezmoi]]"
    type: uses
  - target: "[[concepts/dotfile-manager]]"
    type: implements
---

# Trusted Shell Platform

**Trusted Shell Platform** 是 [[entities/sebastienrousseau-dotfiles]] 项目使用的官方品牌名。

## 核心设计原则

1. **幂等性**：安装脚本无论执行多少次，结果一致
2. **声明式状态**：目标环境通过配置声明，而非命令序列描述
3. **单一配置源**：一套配置驱动 macOS、Linux、WSL 三平台
4. **零投机策略（Zero Speculation）**：文档内容严格镜像源代码，不记录不存在的参数^[extracted]

## 架构层次

```
Trusted Shell Platform
├── chezmoi（状态管理层）
│   ├── 模板引擎
│   ├── 加密集成
│   └── 脚本钩子
├── dot CLI（用户接口层）
│   └── 53 条命令
├── Shell 环境层
│   ├── Zsh 配置
│   ├── 1250+ 别名
│   └── Shell 函数
└── 工具集成层
    ├── Neovim
    ├── tmux / Zellij
    ├── Atuin（历史）
    └── Yazi（文件浏览）
```

## 与竞品对比

| 特性 | Trusted Shell Platform | 纯 chezmoi | GNU Stow |
|------|----------------------|------------|----------|
| CLI 管理命令 | 53 条 dot 命令 | chezmoi 子命令 | 无 |
| 别名预设 | 1250+ | 无 | 无 |
| AI 集成 | 内建 | 无 | 无 |
| 诊断工具 | 14 条命令 | 有限 | 无 |

^[inferred] 对比数据基于各工具文档推断。

## 相关链接

- [[entities/chezmoi]] — 底层配置管理工具
- [[references/dot-cli-commands]] — 完整 CLI 命令参考
- [[concepts/shell-alias-taxonomy]] — 别名分类体系
- [[concepts/dotfile-manager]] — Dotfile 管理工具设计空间
