---
title: >-
  chezmoi — Official Site
category: references
tags: [chezmoi, dotfiles, tools]
sources:
  - "https://chezmoi.io/"
source_url: "https://chezmoi.io/"
created: 2026-07-25T02:27:13Z
updated: 2026-07-25T02:27:13Z
summary: >-
  chezmoi.io 官网首页。覆盖核心理念、单命令引导、五大特性（模板/密码管理器/导入归档/加密/脚本）。
provenance:
  extracted: 0.85
  inferred: 0.10
  ambiguous: 0.05
base_confidence: 0.67
lifecycle: draft
lifecycle_changed: 2026-07-25
---

# chezmoi — Official Site

- **URL**: https://chezmoi.io/
- **角色**: 项目官方门户，定位为 "manage your dotfiles across multiple diverse machines, securely"
- **发音**: /ʃeɪ mwa/ (shay-mwa)

## 项目标识

- **维护者**: Tom Payne（twpayne），版权 2018 起
- **仓库**: github.com/twpayne/chezmoi（MIT）
- **当前版本**: 2.71.1
- **文档站**: MkDocs Material 构建，文档位于 chezmoi.io
- **支持平台**: Linux / macOS / Windows / 容器与虚拟机

## 五大核心特性（首页明示）

1. **Templates** — 处理机器间小差异
2. **Password manager support** — 把密钥安全存储在外部
3. **Importing files from archives** — 适合 shell 和编辑器的插件
4. **Full file encryption** — 支持 age / gpg / git-crypt / transcrypt
5. **Running scripts** — 处理模板与加密覆盖不到的部分

## 单命令引导（one-liner）

```sh
sh -c "$(curl -fsLS https://chezmoi.io/get)" -- init --apply $GITHUB_USERNAME
```

- 把"安装 chezmoi + 拉取 GitHub dotfiles 仓库 + 应用"打包为一次调用
- 跨机器同步的入口：`chezmoi update`

## 命名约定（首页导航揭示的特殊文件/目录）

- 特殊文件：`.chezmoi.<format>.tmpl`、`.chezmoidata.<format>`、`.chezmoiexternal.<format>`、`.chezmoiignore`、`.chezmoiremove`、`.chezmoiroot`、`.chezmoiversion`
- 特殊目录：`.chezmoidata/`、`.chezmoiexternals/`、`.chezmoiscripts/`、`.chezmoitemplates/`

## 关键信息（明确陈述）

- 单一二进制分发，statically-linked，无依赖，不需要 root
- 包含 Homebrew / apt / dnf / scoop / winget / Nix 等多包管理器安装路径（页面有指向但未详述）
- 文档类型包括：User Guide、Reference、Developer Guide（含 Architecture）

## 局限性

- 仅显示首页与导航；详细工作流需进入子页面
- 不包含明确架构图
- 不显示源码层级（internal/、cmd/、pkg/ 等 Go 包布局）

## 相关链接

- [[entities/chezmoi]]
- [[concepts/dotfile-manager]]
- [[concepts/chezmoi-three-state-model]]
- [[concepts/chezmoi-templating]]
- [[concepts/chezmoi-attribute-prefixes]]