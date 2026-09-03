---
title: >-
  chezmoi + nix-darwin：macOS 一键复刻开发环境的组合拳
category: references
tags: [chezmoi, nix-darwin, dotfiles, macOS, reference]
sources:
  - "https://juejin.cn/post/7589477341766352942"
created: 2026-07-25T09:00:00Z
updated: 2026-07-25T10:00:00Z
tier: peripheral
summary: >-
  chezmoi 管用户级配置（点文件、模板、加密），nix-darwin 管系统级（包、macOS defaults、Homebrew、Dock/Finder），通过 run_* 钩子钩成单条命令；.chezmoidata.yaml shared/work/private profile 区分机器差异，Justfile 收敛日常维护。
provenance:
  extracted: 0.82
  inferred: 0.13
  ambiguous: 0.05
base_confidence: 0.50
lifecycle: draft
lifecycle_changed: 2026-07-25
relationships:
  - target: "[[concepts/dotfile-manager]]"
    type: related_to
  - target: "[[entities/chezmoi]]"
    type: related_to
---

# chezmoi + nix-darwin：macOS 一键复刻开发环境的组合拳

> 来源：LuYixian dotfiles（github.com/LuYixian/dotfiles）——一份公开的 chezmoi + nix-darwin 双工具组合实现，可一键复刻完整 macOS 开发环境。

## 组合的动机

传统 dotfiles 只管 `~/.zshrc`、`.gitconfig` 这类用户级配置。但开发者换机的真实痛点还包括：

- 重装哪些 CLI 工具
- macOS 系统默认值（Dock、Finder、Trackpad）
- Homebrew formula/cask 的图形应用
- 包版本是否一致

单靠 chezmoi 解决不了"装软件"——它只放配置文件。引入 nix-darwin（macOS 上的 NixOS 派生项目），把系统配置也声明化。

## 职责分工

| 职责 | 工具 | 典型内容 |
|---|---|---|
| 用户级配置 | chezmoi | `.zshrc`、`gitconfig`、`~/.config/*` |
| 系统包 & defaults | nix-darwin | CLI 包、`defaults write`、launchd |
| GUI 应用 | Homebrew（由 nix-darwin 生成 Brewfile） | VS Code、Raycast、Slack |
| 私密信息 | chezmoi + age | token、私钥、加密配置 |
| Mac App Store | `mas`（由 nix-darwin 管理） | 必须走 MAS 的 App |

## 上机流程

```bash
sh -c "$(curl -fsLS get.chezmoi.io)" -- init --apply LuYixian
cd ~/.local/share/chezmoi
just darwin
```

`init --apply` 完成后，跑 `just darwin` 触发 darwin-rebuild 把系统配置完整应用到 macOS。期间通过 chezmoi 的 `.chezmoiscripts/` 钩子分阶段执行：

```
.chezmoiscripts/
├── run_once_before_01_install-nix.sh        # 确保 Nix 已装
├── run_onchange_after_02_init.sh.tmpl       # 渲染并写点文件
├── run_onchange_after_03_install-paperlib.sh.tmpl
├── run_after_04_set_profiles.sh.tmpl        # 按机器 profile 装包
└── run_after_05_update_homebrew_packages.sh.tmpl
```

## 数据驱动差异化：.chezmoidata.yaml

luyixian 方案的核心创新是用 YAML 数据文件描述"差异"，而不是用一堆 `{{ if eq .chezmoi.hostname "x" }}`：

```yaml
homebrew:
  casks:
    shared:  [visual-studio-code, ghostty]
    work:    [slack]
    private: [discord]

homepkgs:
  shared:  [ripgrep, bat, fzf]
  work:    [google-cloud-sdk, awscli2]
  private: [mas]
```

模板里用 `{{- if .work }}` 渲染 work-only 配置。共享一份仓库，profile 在 init 时选择。

## 10 个值得复用的设计

| # | 设计 | 解决的问题 |
|---|---|---|
| 1 | 现代 CLI 替换（eza/bat/ripgrep/fd/dust/zoxide/tldr） | 默认更快/更友好 |
| 2 | shell 启动"只在命令存在时初始化" | 慢启动 + 脆弱依赖 |
| 3 | 工作流函数（dev/fgc/fkill/port/backup_dev_env） | 减少"我记得有个命令"的脑力消耗 |
| 4 | profile 分层（shared/work/private） | 工作机 vs 私人机差异"写在代码里" |
| 5 | CI + Renovate | pre-commit 统一格式、Renovate 自动更新 Nix 依赖 |
| 6 | mise 统一语言运行时（Node/Python/Go/Rust/Terraform） | 避免 nvm/pyenv/asdf 互打 |
| 7 | AI 集成（aicommit + Claude Code） | 让 AI 用在"重复但需要上下文"的地方 |
| 8 | 统一主题（Dracula） | 降低长期使用疲劳感 |
| 9 | Nix + Homebrew + MAS 分层 | 不强迫"一切都用 Nix" |
| 10 | Justfile 维护命令 | just darwin / up / full-upgrade / gc |

## 现代 CLI 工具链对照

| 传统 | 现代替代 | 选择理由 |
|---|---|---|
| `ls` | `eza` | Git 集成、图标、树形视图 |
| `cat` | `bat` | 语法高亮、分页、Git diff 提示 |
| `grep` | `ripgrep` | 极快、尊重 `.gitignore` |
| `find` | `fd` | 语法更直觉 |
| `du` | `dust` | 可视化 |
| `cd` | `zoxide` | 记忆习惯跳转 |
| `man` | `tldr` | "我现在要怎么用"导向 |

## Justfile 收敛维护命令

```makefile
# 重建并切换系统配置
just darwin

# 更新 flake inputs
just up

# 完整升级
just full-upgrade

# 清理旧版本释放空间
just gc
```

高层意图的"just do it"命令，隐藏 darwin-rebuild / nix flake update / nix-collect-garbage 等细节。

## Nix-darwin 在 macOS 的真正价值

| 维度 | 命令式（brew） | 声明式（nix-darwin） |
|---|---|---|
| 可复现性 | 不可——你装的版本会被 brew 仓库演化 | 锁版本（flake lock） |
| 原子更新 | 不可能 | 是——要么整套切过去要么不动 |
| 可回滚 | 不可 | 是（system generations） |
| 系统设置 | 散落在 defaults write 与在线博客 | 写在 Nix 配置里 |
| Homebrew 编排 | 手动 install | nix-darwin 生成 Brewfile |

> 注意：nix-darwin 与 Determinate Systems 安装的 Nix 的 daemon 管理方式可能冲突，本仓库已做适配。

## 为什么不用纯 Nix home-manager

home-manager 也能管 `~/` 下文件，但：

- 它属于 NixOS 生态，引入门槛更高
- 用户级配置量大时模板/加密/钩子需求复杂，chezmoi 的命名约定更可读
- nix-darwin 的 `defaults write` 与 homebrew 编排能力与 home-manager 是替代而非互补关系

**chezmoi + nix-darwin 是实践中被验证最稳的双工具组合**——chezmoi 处理声明/模板/加密，nix-darwin 处理包与系统。

## 起步路径

按这个顺序逐步搭建（避免一上来就搞 Nix 吓退自己）：

1. **先 chezmoi**：单文件 `chezmoi add ~/.zshrc` → git 托管 → `chezmoi init --apply`
2. **加数据分层**：`.chezmoidata.yaml` 做 shared/work/private
3. **转模板**：把易变配置 `.tmpl` 化
4. **加 age 加密**：敏感文件
5. **加脚本钩子**：`.chezmoiscripts/` 把安装步骤封装
6. **最后引入 nix-darwin**：逐步把包与系统设置声明式化

## 相关页面

- [[concepts/dotfile-manager]] — dotfile 管理五大流派对比
- [[concepts/chezmoi-workflow]] — chezmoi 四动词 + update/init
- [[concepts/chezmoi-templating]] — 模板差异化机制
- [[synthesis/Research: chezmoi]] — chezmoi 综合研究
