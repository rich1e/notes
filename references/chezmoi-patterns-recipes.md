---
title: >-
  chezmoi 实用模式集：跨平台初始化、模板变量、加密与脚本钩子
category: references
tags: [chezmoi, dotfiles, templates, cross-platform, reference]
sources:
  - "https://zhuanlan.zhihu.com/p/2017558515602990956"
  - "https://juejin.cn/post/7624438584691310628"
  - "https://recca0120.github.io/2026/04/13/chezmoi-dotfiles-management/"
  - "https://blog.qingshanls.icu/2026/04/05/chezmoi/"
  - "https://cn.x-cmd.com/install/chezmoi"
created: 2026-07-25T09:00:00Z
updated: 2026-07-25T09:00:00Z
summary: >-
  社区积累的 chezmoi 实用模式:安装速查、文件名前缀解码、跨平台模板变量、age/gpg/git-crypt/SOPS 加密矩阵、run_once_/run_onchange_ 脚本钩子时序、.chezmoiroot 与 .chezmoiignore 协作、外部文件下载与维护命令。
provenance:
  extracted: 0.82
  inferred: 0.13
  ambiguous: 0.05
base_confidence: 0.50
lifecycle: draft
lifecycle_changed: 2026-07-25
    type: uses
relationships:
  - target: "[[concepts/chezmoi-templating]]"
    type: uses
  - target: "[[entities/chezmoi]]"
    type: related_to

---

# chezmoi 实用模式集：跨平台初始化、模板变量、加密与脚本钩子

> 来源：Sylearn（zhihu）、ovensi（juejin）、recca0120（recca0120.github.io）、青山蓝山（QSLS）、X-CMD 五个独立教程的实战片段汇总。

## 一、安装方式速查矩阵

| OS / 包管理器 | 命令 |
|---|---|
| macOS Homebrew | `brew install chezmoi` |
| Debian/Ubuntu | `sudo apt install chezmoi` |
| Arch Linux | `sudo pacman -S chezmoi` |
| CentOS/RHEL | `sudo yum install chezmoi` |
| Alpine | `sudo apk add chezmoi` |
| Windows Scoop | `scoop install chezmoi` |
| Windows Chocolatey | `choco install chezmoi` |
| Windows Winget | `winget install twpayne.chezmoi` |
| macOS MacPorts | `sudo port selfupdate && sudo port install chezmoi` |
| FreeBSD | `pkg install chezmoi` |
| 通用脚本 | `sh -c "$(curl -fsLS get.chezmoi.io)"` |
| 通用脚本（Wget） | `sh -c "$(wget -qO- get.chezmoi.io)"` |
| 通用脚本（PowerShell） | `iwr -useb https://get.chezmoi.io/ps1 \| iex` |
| Termux (Android) | `sudo pkg install chezmoi` |
| Snap | `snap install chezmoi --classic` |
| X-CMD 通用 | `x install chezmoi` |

## 二、文件名前缀解码

通过**前缀嵌入元数据**是 chezmoi 的核心设计——一个文件名同时承载路径映射 + 权限 + 类型 + 行为。

| 前缀 | 含义 | 例子 |
|---|---|---|
| `dot_` | 替换为 `.` 开头（隐藏文件） | `dot_zshrc` → `~/.zshrc` |
| `private_` | 仅所有者读写（0600） | `private_dot_ssh/id_ed25519` |
| `executable_` | 添加可执行权限（0755） | `executable_bin_foo` |
| `encrypted_` | age/gpg 加密后存储 | `encrypted_dot_env.age` |
| `symlink_` | 创建符号链接 | `symlink_dot_bashrc` |
| `readonly_` | 移除写权限（0444） | `readonly_dot_config.toml` |
| `exact_` | 严格镜像（删掉目录中其他内容） | `exact_dot_config/nvim` |
| `create_` | 缺失则创建（空目录） | |
| `remove_` | 若存在则删除 | |
| `modify_` | 内容是补丁脚本 | `modify_dot_config.toml` |
| `empty_` | 即便空也保留 | |
| `external_` | 子条目忽略属性 | |
| `literal_` | 停止属性解析 | |
| 文件后缀 `.tmpl` | 套用 Go template 引擎 | `dot_gitconfig.tmpl` |

**前缀可叠加**，如 `private_executable_dot_php-cs-fixer.dist.php` → `~/.php-cs-fixer.dist.php`（0700）。

## 三、跨平台模板变量

chezmoi 内置变量在模板中可直接引用：

```gotmpl
{{ .chezmoi.os }}              # "darwin" | "linux" | "windows"
{{ .chezmoi.arch }}            # "amd64" | "arm64"
{{ .chezmoi.hostname }}        # 机器名
{{ .chezmoi.username }}        # 当前登录账户
{{ .chezmoi.homeDir }}         # home 目录路径
{{ .chezmoi.kernel.osrelease }}# 内核版本
{{ .chezmoi.git }}             # 若源目录是 git 仓库则有
```

**实战案例（recca0120 三 OS dotfiles）**：

```gotmpl
[user]
    name = {{ .name | quote }}
    email = {{ .email | quote }}

[http]
    sslBackend = openssl
{{ if eq .chezmoi.os "windows" -}}
    sslCAInfo = {{- .chezmoi.homeDir | replace "\\" "/" -}}/scoop/apps/git/current/mingw64/ssl/certs/ca-bundle.crt
{{ end }}
```

`windows` 路径里的反斜杠走 `replace` 转斜杠——stdio 跨平台 trick。

**调试模板**：

```bash
chezmoi execute-template < dot_gitconfig.tmpl
# 或查看所有可用数据
chezmoi data
```

## 四、加密矩阵

| 方式 | 配置位置 | 适用场景 |
|---|---|---|
| **age**（默认推荐） | `~/.config/chezmoi/chezmoi.toml` 配 `[age]` 段 | 公钥派生对称加密，密钥管理简单 |
| **GPG** | `[gpg]` 段 | 已有 GPG 密钥环，传统方式 |
| **git-crypt** | git 钩子层加密 | 与其他 git 流程兼容 |
| **transcrypt** | 同上 | 体验更好的 git-crypt 替代 |
| **SOPS** | `[sops]` 段 | 结构化密钥（YAML/JSON） |
| **1Password / Bitwarden / Vault / pass** | 模板数据函数 | 不加密文件，只在模板查询时取值 |

加密文件的实际落盘文件示例：`private_dot_ssh/encrypted_private_id_ed25519.age`——`.age` 后缀表明是加密源，apply 时用 `~/key.txt` 解密后写到目标位置。

**绝对不能进仓库的东西**：`key.txt` 自身。推荐 GPG 加密后放密码管理器。

## 五、4 种 run_* 钩子时序

recca0120 的核心贡献：把脚本钩子的命名规则讲透。

| 前缀 | 触发时机 | 用途 |
|---|---|---|
| `run_` | 每次 `chezmoi apply` 都执行 | 钩子 |
| `run_once_` | 首次 apply 执行一次（同内容一生命周期只一次） | 系统级一次性配置 |
| `run_onchange_` | 内容 hash 变化时才执行 | 包安装（清单没变就不重装） |
| `run_onchange_before_` | 套文件**之前** | 装包管理器 |
| `run_onchange_after_` | 套文件**之后** | 启用 zsh 插件 |

**实战**：`.chezmoiscripts/darwin/run_onchange_00_install-packages.sh.tmpl`：

```bash
{{ if eq .chezmoi.os "darwin" -}}
#!/bin/bash
brew install mas
brew install asdf
asdf plugin add nodejs
asdf install nodejs latest
asdf set nodejs latest
{{ end -}}
```

文件名前面的数字（`00_`、`01_`）控制执行顺序。

## 六、`.chezmoiroot` 与 `.chezmoiignore`

### `.chezmoiroot`

让 repo 根目录放 README/install script 等项目文件，chezmoi 只看 `home/` 子目录：

```
dotfiles/
├── .chezmoiroot        # 内容只有 "home"
├── Readme.md
├── install.sh
├── install.ps1
└── home/
    ├── dot_zshrc.tmpl
    ├── dot_gitconfig.tmpl
    └── .chezmoiscripts/
```

适合把 dotfiles repo 当正常 GitHub 项目维护。

### `.chezmoiignore`

跟 `.gitignore` 语法类似，但**支持模板**：

```fallback
README.md
LICENSE
{{ if ne .chezmoi.os "darwin" }}
.aerospace.toml
Library/
{{ end }}
```

注意：`.chezmoiignore` 默认语义是**正逻辑排除**，社区多次反映需要"仅在 X 时忽略"的负逻辑（反直觉），官方尚未修正。

## 七、外部文件：.chezmoiexternal.toml

第三方配置或字体等大文件，不入仓但按需下载：

```toml
# 单文件下载
["scripts/git-prompt.sh"]
    type = "file"
    url = "https://raw.githubusercontent.com/git/git/master/contrib/completion/git-prompt.sh"

# 下载并解压
[".fonts/FiraCode"]
    type = "archive"
    url = "https://github.com/tonsky/FiraCode/releases/download/6.2/Fira_Code_v6.2.zip"
```

## 八、chezmoi doctor 与发行版校验

```bash
chezmoi doctor      # 检查 secret 后端、template 引擎、git 等
```

发布包用 **cosign 签名校验**：

```bash
curl --location --remote-name-all \
    https://github.com/twpayne/chezmoi/releases/download/v2.69.3/chezmoi_2.69.3_checksums.txt \
    https://github.com/twpayne/chezmoi/releases/download/v2.69.3/chezmoi_2.69.3_checksums.txt.sig \
    https://github.com/twpayne/chezmoi/releases/download/v2.69.3/chezmoi_cosign.pub

cosign verify-blob --key=chezmoi_cosign.pub \
    --signature=chezmoi_2.69.3_checksums.txt.sig \
    chezmoi_2.69.3_checksums.txt
```

## 九、每日工作流模板

```
# 1. 改了 ~/ 下某个 dotfile
chezmoi add ~/.new_config

# 2. 改了 ~/.zshrc
chezmoi edit --apply ~/.zshrc

# 3. 提交推送
chezmoi cd && git add -A && git commit -m "..." && git push

# 4. 其他机器同步
chezmoi update
```

## 十、常见坑位与修复

| 坑 | 修复 |
|---|---|
| 改了 `~/` 配置 czpush 没推上去 | `chezmoi managed \| grep` 确认已纳入 |
| 初始化失败：chezmoi.toml 缺失 | `chezmoi init --force` |
| bashrc 没生效 | `czapply && exec bash` |
| rebase 冲突 | `chezmoi git -- checkout -- <file>` 放弃本地或 `git add . && rebase --continue` |
| age 私钥丢失 | **丢失 = 全部 .age 文件不可恢复**；务必多处备份（密码管理器 + 加密 U 盘 + 纸质） |
| 首次 apply 覆盖手改 | 先 `chezmoi diff` 确认 |

## 相关页面

- [[concepts/chezmoi-workflow.md]]
- [[references/chezmoi-encryption-backends.md]]
- [[concepts/chezmoi-templating]] — 模板机制
- [[concepts/chezmoi-attribute-prefixes]] — 命名作元数据
- [[concepts/chezmoi-workflow]] — 四动词 + update/init
- [[references/chezmoi-bitwarden-keychain]] — 密码管理器集成
- [[references/chezmoi-nix-darwin-integration]] — 与 nix-darwin 组合
- [[synthesis/Research: chezmoi]] — 综合研究
