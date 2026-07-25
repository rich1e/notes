---
title: chezmoi 配置文件管理与密钥安全实践
source: https://yangzh.cn/posts/posts/chezmoi-dotfiles-secrets.html/
author:
  - "[[yangjh]]"
published: 2026-02-08
created: 2026-07-25
description: 用 chezmoi 管理散落各处的 dotfiles，以 Bitwarden 模板注入密钥，用 macOS Keychain 免去手动输入主密码的折磨，再从 git 历史中挖出并掩埋那些不该留下的痕迹。更新：多主机同步时踩过的坑，每一条都曾让人在终端前沉默过几秒。
tags:
  - clippings
  - chezmoi
  - dotfiles
---
chezmoi，法语"chez moi"，意为"在我家"。这个名字取得坦荡。配置文件散落在硬盘各处，像《水经注》里那些被记录又被遗忘的支流，每一条都通往某个你曾经驻留过的环境。chezmoi 做的事情，不过是把这些散佚的篇章收拢成册，用 git 装订，用模板去抹平不同水土之间的差异。

本文记录使用 chezmoi 管理 bash、WezTerm、Claude Code 配置的完整实践，重点是如何结合 Bitwarden 安全处理密钥——那些不该被看见的字符串。

## 核心工作流

### 常用命令

| 命令 | 用途 |
| --- | --- |
| `chezmoi add <path>` | 将文件纳入 chezmoi 管理 |
| `chezmoi add --template <path>` | 以模板方式添加（生成 `.tmpl` 文件） |
| `chezmoi re-add <path>` | 编辑目标文件后同步回源 |
| `chezmoi apply <path>` | 将源文件渲染并应用到目标 |
| `chezmoi diff` | 查看源与目标的差异 |
| `chezmoi status` | 查看哪些文件有变更 |
| `chezmoi forget --force <path>` | 从管理中移除文件 |
| `chezmoi git add .` | 通过 chezmoi 执行 git 操作 |
| `chezmoi git -- commit -m "msg"` | 通过 chezmoi 提交 |
| `chezmoi git push` | 通过 chezmoi 推送 |

所有 git 操作必须通过 `chezmoi git` 执行，不要直接 `cd` 到源目录操作 git。这是规矩。规矩看起来多余，直到你在错误的目录里 `git push` 了错误的东西。

### 注意事项

- `chezmoi forget` 等交互式命令在非交互终端中会卡住，需加 `--force` 参数
- chezmoi 配置了 `autoCommit` 和 `autoPush` 后， `chezmoi add` / `chezmoi re-add` 会自动提交并推送

## Bitwarden 密钥注入

`.bashrc` 和 `.bash_profile` 中写着 API Key 的明文。把密钥写进配置文件再提交到 git，这件事的荒诞程度大约相当于在城墙上刻下暗道的位置。你知道不该这样，但赶时间的时候什么都干得出来。

解决方案并不复杂：将配置文件转为 chezmoi 模板，用 Bitwarden 模板函数在渲染时注入密钥。明文从此只存在于 Bitwarden 的加密 vault 中，源文件里只剩下一行意图声明：

```bash
# 模板文件中（源）
export ANTHROPIC_AUTH_TOKEN="{{ (bitwarden "item" "ANTHROPIC_AUTH_TOKEN").notes }}"
export CHERYY_API_KEY="{{ (bitwarden "item" "CHERYY_API_KEY").notes }}"
```

渲染后目标文件会被替换为 Bitwarden vault 中存储的实际密钥值。

### 操作步骤

1. 在 Bitwarden 中创建安全笔记，name 为变量名，notes 存放密钥值：
```bash
echo '{"type":2,"name":"MY_API_KEY","notes":"sk-xxx","secureNote":{"type":0}}' \
  | bw encode | bw create item
```
2. 将配置文件从普通文件转为模板：
```bash
chezmoi forget --force ~/.bashrc
chezmoi add --template ~/.bashrc
```
3. 编辑模板源文件，将明文密钥替换为 Bitwarden 模板语法
4. 使用前需解锁 Bitwarden 并设置 `BW_SESSION` 环境变量：
```bash
export BW_SESSION=$(bw unlock --raw)
chezmoi apply
```

### 免去手动输入主密码：bw-unlock 自动解锁

每次 `bw unlock` 都要手动输入主密码，这件事做三次还算仪式感，做三十次就是折磨。密码不该写进环境变量——同用户的所有进程都能读到它，npm scripts、VS Code 扩展、任何你没留意的子进程都能顺手牵走。更不能写进 `.zshrc` ，那等于明文上了 git 仓库。

解决思路：利用操作系统自带的加密存储机制保管主密码，需要时取出并自动传递给 `bw unlock` 。密码不落盘为明文、不进 git、不持久化到 shell 环境。chezmoi 的模板条件判断让同一份源文件在不同 OS 上渲染出对应的实现。

#### macOS：Keychain

macOS Keychain 由系统登录密码 + Secure Enclave 保护。用 `security` 命令存取。

**存储密码（一次性操作）：**

```bash
security add-generic-password -s "bitwarden-cli" -a "$USER" -w
```

执行后提示输入密码， `-w` 不带参数表示交互式输入，不会出现在命令历史中。

**bw-unlock 函数（chezmoi 模板渲染后）：**

```bash
bw-unlock() {
    local pw
    pw=$(security find-generic-password -s "bitwarden-cli" -a "$USER" -w 2>/dev/null)
    if [[ -z "$pw" ]]; then
        echo "Keychain 中未找到 bitwarden-cli 密码，请先执行："
        echo "  security add-generic-password -s \"bitwarden-cli\" -a \"\$USER\" -w"
        return 1
    fi
    export BW_SESSION=$(BW_PASSWORD="$pw" bw unlock --passwordenv BW_PASSWORD --raw 2>/dev/null)
    if [[ -n "$BW_SESSION" ]]; then
        echo "Bitwarden 已解锁"
    else
        echo "解锁失败，请检查密码是否正确"
        return 1
    fi
}
```

**主密码变更时更新：**

```bash
security delete-generic-password -s "bitwarden-cli" -a "$USER"
security add-generic-password -s "bitwarden-cli" -a "$USER" -w
```

#### Windows：DPAPI 加密文件

Windows 没有 Keychain，但 PowerShell 的 `ConvertFrom-SecureString` 基于 DPAPI（Data Protection API）加密，只有当前 Windows 用户在当前机器上能解密。安全级别与 Keychain 相当，且不需要安装第三方模块。

**存储密码（PowerShell 中执行一次）：**

```powershell
Read-Host "输入 Bitwarden 主密码" -AsSecureString | ConvertFrom-SecureString | Set-Content "$env:USERPROFILE\.bw-cred.xml"
```

这会在 `%USERPROFILE%\.bw-cred.xml` 生成一个 DPAPI 加密文件，明文看不到密码，只有当前用户能解密。

**bw-unlock 函数（chezmoi 模板渲染后，用于 Git Bash）：**

```bash
bw-unlock() {
    local cred_file="$USERPROFILE/.bw-cred.xml"
    local pw
    if [[ ! -f "$cred_file" ]]; then
        echo "未找到加密凭据文件，请先在 PowerShell 中执行："
        echo '  Read-Host "输入 Bitwarden 主密码" -AsSecureString | ConvertFrom-SecureString | Set-Content "$env:USERPROFILE\.bw-cred.xml"'
        return 1
    fi
    pw=$(powershell.exe -NoProfile -Command \
        '$ss = Get-Content "$env:USERPROFILE\.bw-cred.xml" | ConvertTo-SecureString; [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($ss))' 2>/dev/null | tr -d '\r')
    if [[ -z "$pw" ]]; then
        echo "解密失败，请重新生成凭据文件"
        return 1
    fi
    export BW_SESSION=$(BW_PASSWORD="$pw" bw unlock --passwordenv BW_PASSWORD --raw 2>/dev/null)
    if [[ -n "$BW_SESSION" ]]; then
        echo "Bitwarden 已解锁"
    else
        echo "解锁失败，请检查密码是否正确"
        return 1
    fi
}
```

**主密码变更时，重新生成加密文件即可：**

```powershell
Read-Host "输入新的 Bitwarden 主密码" -AsSecureString | ConvertFrom-SecureString | Set-Content "$env:USERPROFILE\.bw-cred.xml"
```

#### chezmoi 模板中的跨平台实现

在 `dot_shell_common.tmpl` 中用 chezmoi 条件判断，同一份源文件在不同 OS 上渲染出不同的 `bw-unlock` 实现：

```go-template
{{- if eq .chezmoi.os "darwin" }}
# macOS: 从 Keychain 读取主密码
bw-unlock() { ... security find-generic-password ... }
{{- else }}
# Windows: 从 DPAPI 加密文件读取主密码
bw-unlock() { ... powershell.exe ... ConvertTo-SecureString ... }
{{- end }}
```

两边的调用方式完全一致： `bw-unlock` ，一行命令，不用记平台差异。

#### 日常使用

```bash
bw-unlock          # 一键解锁，macOS 从 Keychain / Windows 从 DPAPI 文件取密码
chezmoi apply      # 此时 BW_SESSION 已设置，模板正常渲染
```

关掉终端， `BW_SESSION` 自动失效。下次开终端再跑一次 `bw-unlock` 。

#### 首次配置的鸡生蛋问题

chezmoi 模板中调用了 `bitwarden` 函数，而 `chezmoi apply` 渲染模板时需要 bw 已解锁。但 `bw-unlock` 函数本身就在模板渲染后的文件里——经典的循环依赖。首次配置时需要手动 bootstrap：

```bash
# macOS
security add-generic-password -s "bitwarden-cli" -a "$USER" -w
# Windows（PowerShell）
# Read-Host "密码" -AsSecureString | ConvertFrom-SecureString | Set-Content "$env:USERPROFILE\.bw-cred.xml"

# 手动解锁一次
export BW_SESSION=$(bw unlock --raw)

# 此时 bw 已解锁，apply 可正常渲染模板
chezmoi apply

# 之后只需 bw-unlock 即可
source ~/.shell_common   # macOS: ~/.zshrc  Windows: ~/.bashrc
bw-unlock
```

## 跨主机差异化配置

不同主机上路径不同。你在这台机器上的家，和另一台机器上的家，门牌号总是对不上。

### hostname 自动映射

与其每次手动输入，不如让 chezmoi 自己认出来。在 `.chezmoi.toml.tmpl` 中建一张 hostname 到短名的映射表：

```go-template
{{- if eq .chezmoi.hostname "yangjhyeahnetdeMac-mini" }}
    machine = "Mini-M4-2T"
{{- else if eq .chezmoi.hostname "DESKTOP-byHome" }}
    machine = "BY-PC"
{{- else }}
    machine = {{ promptStringOnce . "machine" "未识别主机，请输入短名" | quote }}
{{- end }}
```

新增主机时，运行 `hostname` 获取值，加一行 `else if eq` 即可。未知主机走 `promptStringOnce` 兜底，不会让 `chezmoi init` 卡住。

### promptStringOnce

路径之类的值用 `promptStringOnce` 处理：

```toml
[data]
    obsidian_vault = {{ promptStringOnce . "obsidian_vault" "Obsidian vault 路径" | quote }}
```

模板中使用 `{{ .obsidian_vault }}` 引用。每台新机器只需在初始化时回答一次，此后路径便安静地待在 `chezmoi.toml` 里，不再过问。

注意这个"Once"是字面意义上的一次：值写入 `chezmoi.toml` 后，后续 `chezmoi init` 不会重复询问。想强制重新触发，需要先删配置文件再 init。

### 新机器部署

```bash
chezmoi init <github-user>/dotfiles
# 按提示输入机器特定的值（如 vault 路径）
chezmoi apply
```

三行命令，一台新机器便有了旧日的全部记忆。

## 从 Git 历史中彻底清除泄露的密钥

即使当下的文件已经干净，旧的 commit 里仍然躺着明文密钥，像地层中的化石， `git log -p` 一铲子就能挖出来。密钥泄露不是一个当前状态的问题，而是一个历史问题。历史需要重写。

### 工具选择

| 工具 | 推荐度 | 说明 |
| --- | --- | --- |
| `git-filter-repo` | 推荐 | Python 工具，速度快，功能全，git 官方推荐 |
| BFG Repo-Cleaner | 备选 | Java 工具，语法简单，但需要 JRE |
| `git filter-branch` | 不推荐 | 内置但极慢，官方已建议弃用 |

### 操作步骤

#### 1\. 安装 git-filter-repo

```bash
pip install git-filter-repo
```

#### 2\. 创建替换规则文件

创建一个文本文件（如 `replacements.txt` ），每行格式为 `原文==>替换文`:

```
sk-7893ed65...完整密钥...==>***REDACTED_ANTHROPIC_AUTH_TOKEN***
sk-7YUdjC5i...完整密钥...==>***REDACTED_CHERYY_API_KEY***
```

#### 3\. 执行历史重写

```bash
cd $(chezmoi source-path)
git filter-repo --replace-text replacements.txt --force
```

`git-filter-repo` 会遍历所有 commit，将匹配的字符串替换为占位符。执行后 `origin` remote 会被自动移除——这是一种安全措施，防止你在尚未确认结果时就把重写后的历史推了出去。

#### 4\. 验证清除结果

```bash
# 搜索历史中是否还有密钥残留，结果应为 0
git log --all -p | grep -c "sk-7893"
git log --all -p | grep -c "sk-Cupq7Y"
```

#### 5\. 重新添加 remote 并强制推送

```bash
git remote add origin https://github.com/<user>/dotfiles.git
git push --force origin main
```

#### 6\. 清理临时文件

```bash
rm replacements.txt
```

### 注意事项

- 强制推送会覆盖远程历史，如果有其他人 clone 过该仓库，他们需要重新 clone
- 推送后建议到 GitHub Settings → Secret scanning 检查是否还有告警
- 如果密钥已泄露， **必须轮换密钥** ——仅清除历史不能撤销已被读取的风险。锁已经被人看过的门，换锁比换门便宜

## 多主机同步：那些等着你踩的坑

把配置文件推到 git 仓库只是故事的前半段。当你在第二台、第三台机器上拉取这些配置时，后半段才真正开始。以下是实际部署中遇到的问题，每一条都曾让人在终端前沉默过几秒。

### apply 不是 update

`chezmoi apply` 只读本地源目录，不联网。你以为执行了 apply 就是最新的，其实本地源目录可能落后远程几十个 commit。多台主机共用时，第一步应该是 `chezmoi update` （= git pull + apply），而不是 `chezmoi apply` 。

| 命令 | 作用 | 是否联网 |
| --- | --- | --- |
| `chezmoi apply` | 本地源 → 目标目录 | 否 |
| `chezmoi init` | 重新生成配置文件 | 否 |
| `chezmoi update` | git pull + apply | 是 |

### Windows Store 的 Python 幽灵

Windows 上 `command -v python3` 会返回一个路径，看起来 Python 已就位。但执行时报 exit code 49，那是 Windows Store 的引导页，不是真正的 Python 解释器。脚本里检测命令是否可用，不能只靠 `command -v` ，要实际运行一次验证：

```bash
# 靠不住的写法
PYTHON=$(command -v python3 || command -v python)

# 靠得住的写法
if python3 -c "0" 2>/dev/null; then
  PYTHON=python3
elif python -c "0" 2>/dev/null; then
  PYTHON=python
fi
```

### stat 的方言问题

macOS 的 `stat -f %m` 和 Linux/Git Bash 的 `stat -c %Y` 是两种方言，互不兼容。跨平台脚本中把当前平台更可能命中的语法放前面，用 `2>/dev/null` 吞掉另一种的报错。顺序放错了，不会出 bug，但会在 stderr 里吐出一屏你看不懂的数字。

### Bitwarden 的本地缓存

`bw get item` 报"Not found"不一定是 item 不存在，可能只是本地缓存没同步。换主机或长时间未用后，先 `bw sync` 再操作。这个错误信息有误导性，会让你以为自己从没创建过那个条目。

### chezmoi 管配置，不管依赖

chezmoi 同步了 starship 的配置文件（ `starship.toml` ），同步了 zoxide 的初始化代码（`.shell_common` 里的 `eval "$(zoxide init bash)"` ），但它不会帮你安装 starship 和 zoxide。配置文件到了，软件没到，shell 就静默跳过了那些 `if command -v` 守卫，你甚至不会收到报错。新主机的完整流程：

1. 安装依赖软件（starship、zoxide、python 等）
2. `chezmoi update` （拉取最新配置）
3. `chezmoi init` （生成本机配置）
4. `bw-unlock` （解锁 Bitwarden）
5. `chezmoi apply` （应用到目标目录）

顺序不能乱。第 4 步和第 5 步必须在同一个终端里完成，因为 `BW_SESSION` 是环境变量，换个终端就没了。

## 本次管理的文件

| 文件 | 类型 | 说明 |
| --- | --- | --- |
| `.bashrc` | 模板 | 代理函数、ZenMux 配置、TOKEN 从 Bitwarden 注入 |
| `.bash_profile` | 模板 | API Key 从 Bitwarden 注入 |
| `.config/wezterm/wezterm.lua` | 普通文件 | WezTerm 配置含 resurrect 插件 |
| `.claude/settings.json` | 普通文件 | Claude Code 全局设置 |
| `.claude/skills/chezmoi/SKILL.md` | 普通文件 | chezmoi 管理 skill |
| `.claude/skills/obsidian/SKILL.md` | 模板 | Obsidian 笔记 skill，vault 路径通过模板注入 |
| `AppData/.../WindowsTerminal/settings.json` | 普通文件 | Windows Terminal 配置 |