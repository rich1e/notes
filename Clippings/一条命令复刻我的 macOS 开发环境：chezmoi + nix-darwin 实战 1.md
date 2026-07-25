---
title: 一条命令复刻我的 macOS 开发环境：chezmoi + nix-darwin 实战
source: https://juejin.cn/post/7589477341766352942
author:
  - "[[乞讨者]]"
published: 2025-12-31
created: 2026-07-25
description: "## 前言 作为开发者，你是否经历过这些痛苦？ - 换新 Mac，花一整天重新安装配置各种工具 - 公司电脑和个人电脑的配置不同步，经常忘记某个好用的 alias - `.zshrc` 越改越乱，不敢"
tags:
  - clippings
  - chezmoi
  - dotfiles
---
> 这套配置完整开源在： [github.com/LuYixian/do…](https://link.juejin.cn/?target=https%3A%2F%2Fgithub.com%2FLuYixian%2Fdotfiles "https://github.com/LuYixian/dotfiles")  
> 如果这篇文章对你有帮助，欢迎 Star / Fork；问题与改进建议也欢迎直接提 Issue。

### 前言：我为什么要做这套配置？

作为开发者，你是否经历过这些痛苦？

- 换新 Mac，花一整天重新安装、配置各种工具
- 公司电脑和个人电脑配置不同步，经常忘记某个好用的 alias / function
- `.zshrc` 越改越乱，不敢轻易动，怕改坏了
- 想把配置分享给同事，却发现根本跑不起来（“我这里没问题”）

我也深受其苦。后来我给自己定了几个硬指标：

1. **可复刻** ：在另一台 Mac 上，环境应该“完全一样”，而不是“差不多”。
2. **可变体** ：同一个仓库同时服务工作机 / 私人机，并且差异要显式、可审计。
3. **可恢复** ：升级失败或改坏配置，能快速回滚到上一版。
4. **可分享** ：仓库可以公开，但敏感信息必须安全。
5. **可维护** ：日常更新要有标准流程，不靠记忆和手工清单。

最终我选了 **chezmoi + nix-darwin** 作为组合：用户级配置交给 chezmoi，系统级（包、macOS 设置、Homebrew）交给 nix-darwin。现在我可以用一条命令在新 Mac 上拉起完整环境：

```bash
代码解读复制代码sh -c "$(curl -fsLS get.chezmoi.io)" -- init --apply LuYixian
```

你也可以直接打开仓库看完整实现（配置、脚本、CI、更新策略都在里面）：  
[github.com/LuYixian/do…](https://link.juejin.cn/?target=https%3A%2F%2Fgithub.com%2FLuYixian%2Fdotfiles "https://github.com/LuYixian/dotfiles")

下面我会按“为什么、怎么做、有哪些特性”讲清楚，并结合仓库里的真实结构给你可复用的思路。

---

### 这套方案解决什么问题？

一句话总结： **把“装软件 + 配系统 + 配 dotfiles”从手工操作，变成可版本化、可回滚、可分层的代码** 。

| 目标 | 对应机制 |
| --- | --- |
| 多机器一致 | flake lock + 声明式包清单 + 模板渲染 |
| 多 profile 差异 | shared/work/private 数据分层 |
| 不泄露私密信息 | chezmoi + age 加密 |
| 不怕升级翻车 | nix-darwin 原子切换 + 可回滚 |
| 维护成本低 | 脚本钩子 + `Justfile` 标准化命令 |

这些不是“概念图”，而是已经落在代码里。你可以把仓库当成一个可运行的参考实现：  
[github.com/LuYixian/do…](https://link.juejin.cn/?target=https%3A%2F%2Fgithub.com%2FLuYixian%2Fdotfiles "https://github.com/LuYixian/dotfiles")

---

### 什么是 chezmoi？

[chezmoi](https://link.juejin.cn/?target=https%3A%2F%2Fwww.chezmoi.io%2F "https://www.chezmoi.io/") 是一个用 Go 编写的 dotfiles 管理工具。它的核心不是 symlink，而是：

```bash
代码解读复制代码源文件（git 仓库） → 渲染/处理 → 写入目标位置（~/.zshrc 等）
```

#### 传统 dotfiles 管理的几个硬伤

很多人的流程是：把配置塞进 git 仓库，再 symlink 回家目录。这个做法很快会撞墙：

- **不支持多机器差异** ：公司机/私人机要装不同软件、不同账号怎么办？
- **不支持模板** ：想根据机器名/系统架构/是否 headless 生成不同配置？
- **敏感信息难处理** ：API key 要不要提交？不提交不完整，提交不安全。
- **symlink 脆弱** ：路径变动、误删、权限差异都可能炸。

#### chezmoi 的关键能力（也是我选择它的理由）

##### 1) 模板：把“差异”变成显式逻辑

仓库里大量文件用 `.tmpl` 结尾，代表它们会在 `apply` 时按当前机器数据渲染，例如 `dot_gitconfig.tmpl` ：

```
代码解读复制代码[user]
    name = {{ .gitUsername }}
    email = {{ .gitEmail }}
{{- if .work }}
    # work-only config…
{{- end }}
```

这意味着“差异”不是靠手改，而是靠数据驱动。

##### 2) 数据分层：一套仓库，多种 profile

我把“包和应用列表”写在 `.chezmoidata.yaml` ，按 shared/work/private 分层。初始化时通过 prompt 或数据开关选择 profile，渲染出不同的最终配置。

```yaml
代码解读复制代码homebrew:
 casks:
   shared:
     - visual-studio-code
     - ghostty
   work:
     - slack
   private:
     - discord
```

你得到的不是“两个仓库”，而是“一个仓库 + 两个可追踪变体”。

##### 3) 加密：仓库公开也能放心

我用 age 做对称/非对称加密，敏感文件可以加密后提交。关键点是： **公开仓库不等于公开秘密** 。

##### 4) 脚本钩子：把安装流程自动化

`chezmoi` 支持脚本生命周期钩子，我把“装 Nix / 触发 darwin-rebuild / 可选安装 app”全部放进 `.chezmoiscripts/` ：

```
代码解读复制代码.chezmoiscripts/
├── run_once_before_01_install-nix.sh
├── run_onchange_after_02_init.sh.tmpl
├── run_onchange_after_03_install-paperlib.sh.tmpl
├── run_after_04_set_profiles.sh.tmpl
└── run_after_05_update_homebrew_packages.sh.tmpl
```

这让“拿到新机器”变成一条流水线，而不是一堆手工步骤。

如果你想快速理解这套仓库怎么组织的，建议从这几个目录开始看（都在 repo 里）：

```bash
代码解读复制代码.
├── .chezmoiscripts/      # 安装/激活钩子
├── nix-config/           # nix-darwin flake 与模块
├── dot_custom/           # shell 逻辑（eval/alias/functions）
└── private_dot_config/   # 各工具配置（如 sheldon/atuin/mise 等）
```

---

### 什么是 nix-darwin？

[nix-darwin](https://link.juejin.cn/?target=https%3A%2F%2Fgithub.com%2FLnL7%2Fnix-darwin "https://github.com/LnL7/nix-darwin") 是把 NixOS 的“声明式系统配置”理念带到 macOS 的项目。它最关键的价值是： **把系统配置当作代码** 。

#### 声明式 vs 命令式（为什么我不想只靠 brew）

命令式（常见做法）：

```bash
代码解读复制代码brew install ripgrep bat fd
# 过半年换电脑：你还记得装了哪些吗？版本是否一致？顺序是否影响？
```

声明式（nix-darwin）：

```nix
代码解读复制代码environment.systemPackages = with pkgs; [
  ripgrep
  bat
  fd
];
```

你只需要维护一份清单；系统状态由工具计算并应用。

#### nix-darwin 在 macOS 上真正好用的点

1. **可复现** ：flake + lock file 把依赖版本锁死，避免“今天装和下周装不一样”。
2. **原子更新** ：要么整套系统切过去，要么不动；不会出现“更新一半坏了”的状态。
3. **可回滚** ：升级翻车、配置误改，回滚到上一代即可恢复工作环境。
4. **系统设置可管理** ：Dock、Finder、Trackpad、LoginWindow 等都能写进配置。
5. **Homebrew 也能纳入编排** ：GUI 应用（cask）和少量更适配 macOS 的公式（brew）统一进系统激活流程。

> 备注：如果你使用 Determinate Systems 安装的 Nix，它会有自己的 daemon 管理方式，可能与 nix-darwin 的 Nix 管理冲突。本仓库已按该组合进行适配（避免双重管理）。

---

### chezmoi + nix-darwin：为什么是“组合拳”？

它们并不是互相替代，而是职责清晰：

| 职责 | 工具 | 典型内容 |
| --- | --- | --- |
| 用户级配置 | chezmoi | `.zshrc` 、 `gitconfig` 、各类 `~/.config/*` |
| 系统包 & defaults | nix-darwin | CLI 包、系统设置、launchd 配置 |
| GUI 应用 | Homebrew（由 nix-darwin 生成 Brewfile 并安装） | VS Code、Ghostty、Raycast… |
| 私密信息 | chezmoi + age | token、私钥、仅自己可解密的配置 |

这套仓库的“上机流程”基本是：

```csharp
代码解读复制代码chezmoi init --apply
  ↓
1) 拉取 dotfiles
2) 装/检查 Nix（run_once_before）
3) 渲染并写入 dotfiles
4) 触发 darwin-rebuild（run_onchange_after）
  ↓
系统包 + Homebrew + macOS defaults 一次性到位
```

---

### 我的 dotfiles 做了哪些“值得复用”的设计？

#### 1) 现代 CLI 工具链：把体验拉满

我尽量用更快、更友好、默认更好的现代替代：

| 传统命令 | 现代替代 | 我在乎的点 |
| --- | --- | --- |
| `ls` | `eza` | Git 集成、图标、树形视图 |
| `cat` | `bat` | 语法高亮、分页、Git 变更提示 |
| `grep` | `ripgrep` | 极快、尊重 `.gitignore` |
| `find` | `fd` | 语法更直觉，默认更合理 |
| `du` | `dust` | 直观可视化 |
| `cd` | `zoxide` | 记住你的习惯，跳转更快 |
| `man` | `tldr` | 更贴近“我现在要怎么用” |

#### 2) Shell 环境：启动快、信息密度高

核心思路是“只在命令存在时初始化”，避免慢启动和脆弱依赖：

- Starship：prompt 统一且性能好
- Sheldon：zsh 插件管理（比传统框架更轻量）
- Atuin：历史记录进 SQLite，模糊搜索能力强
- direnv：目录级环境变量自动加载
- fzf：模糊搜索一切

（这些初始化逻辑集中在 `dot_custom/eval.sh` ，便于维护。）

#### 3) 常用工作流函数：把高频操作变成“肌肉记忆”

除了 alias，我还写了不少函数把工作流串起来（在 `dot_custom/functions.sh` ）：

- `dev` ：结合 ghq + fzf 快速跳转项目
- `fgc/fgl/fga` ：模糊选择分支、提交、文件（带预览）
- `fkill/port` ：系统工具（安全杀进程、查端口占用）
- `backup_dev_env` ：导出 Brewfile、VS Code 扩展、mise 工具清单，方便迁移/备份

这些东西的目标很简单： **减少上下文切换，减少“我记得有个命令”这种脑力消耗。**

#### 4) 多 profile：工作机和私人机差异“写在代码里”

我把“共享/工作/私人”三类配置拆开，让差异清晰可读、可审计，也更容易给同事复用 shared 部分：

```yaml
代码解读复制代码homepkgs:
 shared:  [ripgrep, bat, fzf]
 work:    [google-cloud-sdk, awscli2]
 private: [mas]
```

#### 5) 工程化保障：CI + 自动更新

除了“能跑”，我更想要“长期稳定可维护”：

- GitHub Actions：跑 `pre-commit` ，把格式化、lint 统一在一处
- Renovate：自动更新 Nix 相关依赖与 lock maintenance，减少手动跟进成本

#### 6) 开发工具：让“环境”支撑工作流

我更在乎的是“整条链路的顺滑”，而不仅是把工具装上去：

- mise：统一管理多语言运行时（Node/Python/Go/Rust/Terraform…），避免 nvm/pyenv/asdf 互相打架
- lazygit：把复杂 git 操作（rebase、cherry-pick、resolve）变成可视化流程
- yazi：终端文件管理器，配合预览把“找文件”变快
- tmux：把一个工作区拆成可复用会话，搭配快捷键减少窗口切换
- gh + ghq：项目收纳 + 快速跳转，配合 `dev` 函数基本等于“终端里的项目启动器”

#### 7) AI 集成：把重复劳动变成自动化

我更愿意把 AI 用在“重复但需要上下文”的地方：

- `aicommit` ：读取 staged diff，生成更像人写的 commit message（减少机械劳动）
- Claude Code：集成到日常终端工作流里，用来做重构、写测试、解释陌生代码

这些能力的设计目标不是“炫技”，而是让你把注意力留给真正难的部分。

#### 8) 统一主题：减少视觉噪音

我把常用工具的主题尽量统一（例如 Dracula），原因很简单： **一致的配色能降低长期使用的疲劳感** 。

#### 9) 包管理分层：该用 Nix 就用 Nix，该用 Homebrew 就用 Homebrew

在 macOS 上我不会强迫“一切都用 Nix”：

- Nix：适合大部分 CLI 工具（可复现、可回滚）
- Homebrew：适合 GUI 应用和部分 macOS 生态更顺的工具（通过 nix-darwin 统一编排）
- Mac App Store：少量必须走 MAS 的应用（用 `mas` 声明式管理）

#### 10) 维护命令：把维护“写进命令”

我把高频维护操作收敛成 `Justfile` ：

```bash
代码解读复制代码just darwin        # 重建并切换系统配置
just up            # 更新 flake inputs
just full-upgrade  # 一条命令做完整升级
just gc            # 清理旧版本释放空间
```

---

### 如何开始？

#### 使用我的配置（推荐）

```bash
代码解读复制代码# 1) 安装 Nix（Determinate Systems installer）
curl --proto '=https' --tlsv1.2 -sSf -L https://install.determinate.systems/nix | sh -s -- install

# 2) 一键部署
sh -c "$(curl -fsLS get.chezmoi.io)" -- init --apply LuYixian

# 3) 构建 nix-darwin
cd ~/.local/share/chezmoi
just darwin
```

提示：我把 `chezmoi` 做成了 `dot` alias，所以你也可以用：

```bash
代码解读复制代码dot diff
dot apply
```

#### 从零搭建自己的仓库（思路复用）

```bash
代码解读复制代码sh -c "$(curl -fsLS get.chezmoi.io)"
chezmoi init
chezmoi add ~/.zshrc
chezmoi apply

chezmoi cd
git add -A && git commit -m "Initial commit"
git remote add origin git@github.com:你的用户名/dotfiles.git
git push -u origin main
```

想把它做成“真正好用”，建议按这个顺序升级：

1. 引入 `.chezmoidata.yaml` 做 shared/work/private 分层
2. 把易变配置改成 `.tmpl` ，用模板表达差异
3. 用 age 加密敏感文件
4. 把安装步骤搬进 `.chezmoiscripts/` ，做到一键初始化
5. 最后再引入 nix-darwin，逐步把包和系统设置声明式化

---

### 总结

**chezmoi + nix-darwin** 对我来说不是“又学一套新东西”，而是一次性解决这些老问题：

- 换电脑：从“手工清单”变成“一条命令”
- 多机器差异：从“记忆和手改”变成“数据分层 + 模板渲染”
- 配置事故：从“修半天”变成“原子切换 + 可回滚”
- 分享复用：从“不可复现”变成“仓库即环境（且可公开）”

如果你想直接复用这套方案，最省心的路线是：

1. 先从仓库的 README 跑通一键安装与 `just darwin`
2. 再按你的需求改 `.chezmoidata.yaml` 的包清单与 profile
3. 最后再逐步把你自己的配置迁移进来（模板化/加密/脚本化）

仓库地址： [github.com/LuYixian/do…](https://link.juejin.cn/?target=https%3A%2F%2Fgithub.com%2FLuYixian%2Fdotfiles "https://github.com/LuYixian/dotfiles")  