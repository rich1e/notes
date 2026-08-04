---
title: >-
  chezmoi — Entity
category: entities
tags: [chezmoi, dotfiles, tools, entity]
sources:
  - "https://chezmoi.io/"
  - "https://github.com/twpayne/chezmoi"
  - "https://yangzh.cn/posts/posts/chezmoi-dotfiles-secrets.html"
  - "https://cn.x-cmd.com/install/chezmoi"
  - "https://juejin.cn/post/7589477341766352942"
  - "https://github.com/sebastienrousseau/dotfiles.github.io"
created: 2026-07-25T02:27:13Z
updated: 2026-07-27T06:20:00Z
summary: >-
  chezmoi：twpayne 维护的跨平台 dotfile 管理工具，单 Go 二进制分发，三态模型 + 模板 + 加密 + 脚本。
provenance:
  extracted: 0.85
  inferred: 0.10
  ambiguous: 0.05
base_confidence: 0.67
lifecycle: draft
tier: core
lifecycle_changed: 2026-07-25
---

# chezmoi — Entity

- **官网**: https://chezmoi.io/
- **仓库**: https://github.com/twpayne/chezmoi
- **维护者**: Tom Payne (twpayne)
- **首发**: 2018
- **当前版本**: 2.71.1（截至 2026-07）
- **许可**: MIT
- **实现语言**: Go（单二进制静态链接，无依赖）
- **发音**: /ʃeɪ mwa/ (shay-mwa)

## 定位

"Manage your dotfiles across multiple diverse machines, securely."

相比裸 git + symlink（最低门槛）与 Nix home-manager（最高门槛），chezmoi 占据**中段**：

- 不绑定 OS
- 提供声明式状态机
- 单二进制分发，无需运行时

## 关键设计

- **三态模型**：源态 / 目标态 / 实际态（[[concepts/chezmoi-three-state-model]]）
- **命名作元数据**：17 个属性前缀嵌入文件名（[[concepts/chezmoi-attribute-prefixes]]）
- **Go 模板 + sprig**：差异化机器配置（[[concepts/chezmoi-templating]]）
- **四动词工作流**：`add` / `edit` / `diff` / `apply`（[[concepts/chezmoi-workflow]]）

## 支持平台

- Linux（含各发行版包管理器）
- macOS（Homebrew）
- Windows（scoop、winget）
- FreeBSD / OpenBSD（ports / packages）
- 容器与虚拟机（独立二进制）

## 加密与集成能力

- age（默认推荐）、GPG、git-crypt / transcrypt、SOPS。
- 外部密码管理器（1Password / Bitwarden / Vault / pass）作为模板数据源，而非文件加密；Bitwarden 实践见 [[skills/chezmoi-bitwarden-secrets]]。
- macOS 可与 nix-darwin 分层协作，由 chezmoi 管用户级配置、nix-darwin 管系统包与 defaults，见 [[references/chezmoi-nix-darwin-integration]]。
- 可用 bootstrap 脚本安装 chezmoi、age 和常用 CLI，再执行 `init --apply` 完成新机恢复。

## 知名使用案例

- [[entities/sebastienrousseau-dotfiles]] — Trusted Shell Platform，以 chezmoi 为核心状态管理层，叠加 dot CLI（53 条命令）和 1,250+ 别名，面向跨平台开发者分发

## 相关链接

- [[concepts/dotfile-manager]]
- [[concepts/chezmoi-three-state-model]]
- [[concepts/chezmoi-attribute-prefixes]]
- [[concepts/chezmoi-templating]]
- [[concepts/chezmoi-workflow]]
- [[references/chezmoi-official-site]]
- [[references/chezmoi-templating-guide]]
- [[references/chezmoi-source-state-attributes]]
- [[references/chezmoi-workflow-discussion]]
- [[references/chezmoi-patterns-recipes]]
- [[synthesis/Research: chezmoi]]
- [[skills/chezmoi-bitwarden-secrets]]
- [[references/chezmoi-nix-darwin-integration]]

## 相关页面

- [[synthesis/concepts-dotfile-manager × entities-chezmoi]] — synthesis
- [[synthesis/concepts-chezmoi-templating × concepts-chezmoi-attribute-prefixes]] — synthesis
