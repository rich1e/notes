---
title: chezmoi × 密码管理器：Bitwarden 模板注入与跨平台主密码保管
category: references
tags: [chezmoi, secrets, bitwarden, dotfiles, reference]
sources:
  - "https://yangzh.cn/posts/posts/chezmoi-dotfiles-secrets.html/"
created: 2026-07-25T09:00:00Z
updated: 2026-07-25T09:00:00Z
tier: peripheral
summary: >-
  把 Bitwarden 作为模板函数注入密钥，macOS 用 Keychain、Windows 用 DPAPI 加密文件免去每次手输主密码；git-filter-repo 重写历史清除已泄露密钥。多主机同步时 Windows Store Python 幽灵、`stat` 方言、Bitwarden 本地缓存等坑位的修复方案。
provenance:
  extracted: 0.85
  inferred: 0.10
  ambiguous: 0.05
base_confidence: 0.50
lifecycle: draft
lifecycle_changed: 2026-07-25
    type: related_to
relationships:
  - target: "[[concepts/chezmoi-templating]]"
    type: uses
  - target: "[[entities/chezmoi]]"
    type: related_to

---

# chezmoi × 密码管理器：Bitwarden 模板注入与跨平台主密码保管

> 来源：yangjh 《chezmoi 配置文件管理与密钥安全实践》——把 chezmoi 实战讲透了的三层结构：Bitwarden 模板注入 + 操作系统密码保管 + Git 历史重写。

## 三层密钥管理栈

| 层 | 工具 | 作用 |
|---|---|---|
| 模板 | chezmoi + Bitwarden | 渲染时拉取 secret，源文件只保留"意图声明" |
| 主密码 | macOS Keychain / Windows DPAPI | OS 级硬件/账户保护，避免明文出现 |
| 历史清理 | git-filter-repo | 修补"过去泄露"的密钥 |

## 一、Bitwarden 模板注入

### 模板写法

模板源（`dot_bashrc.tmpl`）只保留意图：

```bash
export ANTHROPIC_AUTH_TOKEN="{{ (bitwarden "item" "ANTHROPIC_AUTH_TOKEN").notes }}"
export CHERYY_API_KEY="{{ (bitwarden "item" "CHERYY_API_KEY").notes }}"
```

chezmoi apply 渲染时调用 Bitwarden CLI，把 `.notes` 字段值注入。源文件中**没有明文密钥**。

### Bitwarden 中存储结构

每个变量一个 secure note：

```bash
echo '{"type":2,"name":"MY_API_KEY","notes":"sk-xxx","secureNote":{"type":0}}' \
  | bw encode | bw create item
```

`notes` 字段放密钥值，name 字段是 chezmoi 查找键。

### 使用流程

1. `chezmoi forget --force ~/.bashrc`（把现有文件从管理中移除）
2. `chezmoi add --template ~/.bashrc`（重新加为模板）
3. 编辑源文件，把明文密钥替换为 `{{ (bitwarden ...) }}`
4. 解锁 Bitwarden 后 `chezmoi apply`

```bash
export BW_SESSION=$(bw unlock --raw)
chezmoi apply
```

## 二、跨平台 bw-unlock：免手输主密码

频繁 `bw unlock` 是个累赘。把主密码托管给操作系统的硬件保护（Keychain 走 Secure Enclave、DPAPI 走当前用户），chezmoi 模板负责按 OS 渲染不同实现。

### macOS：Keychain 路径

```bash
# 一次性存储
security add-generic-password -s "bitwarden-cli" -a "$USER" -w
```

`-w` 不带参数表示交互式输入——密码**不进命令历史**。

然后 chezmoi 模板里渲染的 `bw-unlock()`：

```bash
bw-unlock() {
    local pw
    pw=$(security find-generic-password -s "bitwarden-cli" -a "$USER" -w 2>/dev/null)
    [[ -z "$pw" ]] && { echo "Keychain 中未找到 bitwarden-cli 密码"; return 1; }
    export BW_SESSION=$(BW_PASSWORD="$pw" bw unlock --passwordenv BW_PASSWORD --raw 2>/dev/null)
    [[ -n "$BW_SESSION" ]] && echo "Bitwarden 已解锁"
}
```

主密码变更时：

```bash
security delete-generic-password -s "bitwarden-cli" -a "$USER"
security add-generic-password -s "bitwarden-cli" -a "$USER" -w
```

### Windows：DPAPI 加密文件路径

```powershell
Read-Host "输入 Bitwarden 主密码" -AsSecureString | ConvertFrom-SecureString | Set-Content "$env:USERPROFILE\.bw-cred.xml"
```

生成 `%USERPROFILE%\.bw-cred.xml`——只有当前 Windows 用户在当前机器上能解密。

Git Bash 里的 `bw-unlock()`：

```bash
bw-unlock() {
    local cred_file="$USERPROFILE/.bw-cred.xml"
    [[ ! -f "$cred_file" ]] && { echo "未找到加密凭据文件"; return 1; }
    local pw
    pw=$(powershell.exe -NoProfile -Command \
      '$ss = Get-Content "$env:USERPROFILE\.bw-cred.xml" | ConvertTo-SecureString; [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($ss))' 2>/dev/null | tr -d '\r')
    export BW_SESSION=$(BW_PASSWORD="$pw" bw unlock --passwordenv BW_PASSWORD --raw 2>/dev/null)
}
```

### chezmoi 模板按 OS 渲染

`dot_shell_common.tmpl`：

```go-template
{{- if eq .chezmoi.os "darwin" }}
# macOS: 从 Keychain 读取主密码
bw-unlock() { ... security find-generic-password ... }
{{- else }}
# Windows: 从 DPAPI 加密文件读取主密码
bw-unlock() { ... powershell.exe ... ConvertTo-SecureString ... }
{{- end }}
```

同一份源文件 → 不同平台不同实现，调用方完全无感：`bw-unlock && chezmoi apply`。

### 首次配置鸡生蛋问题

`bw-unlock` 函数定义**在模板文件里**，渲染时需要 bw 已解锁。首次引导：

```bash
# macOS
security add-generic-password -s "bitwarden-cli" -a "$USER" -w

# 手动解锁一次
export BW_SESSION=$(bw unlock --raw)

# 此时模板能正常渲染
chezmoi apply

# 之后只需
bw-unlock
```

## 三、Git 历史清除：用 git-filter-repo 抹掉地层化石

密钥泄露是**历史问题**而非状态问题——`git log -p` 一铲子就能挖出来。需要重写历史。

### 工具选择

| 工具 | 推荐度 | 说明 |
|---|---|---|
| `git-filter-repo` | 推荐 | git 官方推荐，速度快功能全 |
| BFG Repo-Cleaner | 备选 | 语法简单但需要 JRE |
| `git filter-branch` | 不推荐 | 官方已建议弃用 |

### 操作步骤

```bash
# 1. 安装
pip install git-filter-repo

# 2. 替换规则（按行格式 原文==>替换文）
cat > replacements.txt <<EOF
sk-7893ed65...完整密钥...==>***REDACTED_ANTHROPIC_AUTH_TOKEN***
sk-7YUdjC5i...完整密钥...==>***REDACTED_CHERYY_API_KEY***
EOF

# 3. 执行重写
cd $(chezmoi source-path)
git filter-repo --replace-text replacements.txt --force
```

执行后 `origin` remote 被自动移除（安全措施，防"误把历史推出去"）。

### 验证 + 强制推送

```bash
# 验证残留 = 0
git log --all -p | grep -c "sk-7893"   # 应为 0

# 重新加 remote 并强制推送
git remote add origin https://github.com/<user>/dotfiles.git
git push --force origin main
```

### 必须轮换密钥

**关键警告**：仅清除历史不能撤销已被读取的风险——锁已经被人看过的门，换锁比换门便宜。推送后建议到 GitHub Settings → Secret scanning 检查是否还有告警。

## 四、多主机同步的踩坑清单

### apply 不是 update

| 命令 | 作用 | 是否联网 |
|---|---|---|
| `chezmoi apply` | 本地源 → 目标 | 否 |
| `chezmoi init` | 重新生成配置 | 否 |
| `chezmoi update` | git pull + apply | 是 |

多台主机共用时**第一步是 `chezmoi update`**，否则本地源可能落后几十个 commit。

### Windows Store 的 Python 幽灵

`command -v python3` 在 Windows 上会返回 Windows Store 引导页路径——执行报 exit code 49。靠不住的写法 vs 靠得住的：

```bash
# 靠不住
PYTHON=$(command -v python3 || command -v python)

# 靠得住——跑一下验证
if python3 -c "0" 2>/dev/null; then
  PYTHON=python3
elif python -c "0" 2>/dev/null; then
  PYTHON=python
fi
```

### `stat` 方言问题

| OS | 命令 | 时间戳格式 |
|---|---|---|
| macOS | `stat -f %m` | 秒 |
| Linux/Git Bash | `stat -c %Y` | 秒 |

跨平台脚本：把当前平台更可能命中的语法放前面，用 `2>/dev/null` 吞掉另一种的报错。顺序反了不会出 bug，但会在 stderr 吐一屏数字。

### Bitwarden 本地缓存

`bw get item` 报"Not found"不一定是 item 不存在，可能只是本地缓存未同步。**换主机或长时间未用后，先 `bw sync` 再操作**。

### chezmoi 管配置，不管依赖

chezmoi 同步 starship.toml，但**不安装 starship**。配置文件到了但软件没到，shell 静默跳过 `if command -v` 守卫。新主机完整流程：

1. 安装依赖（starship / zoxide / python 等）
2. `chezmoi update`（拉取最新配置）
3. `chezmoi init`（生成本机配置）
4. `bw-unlock`（解锁 Bitwarden）
5. `chezmoi apply`（渲染模板并落盘）

第 4 步和第 5 步必须在同一终端——`BW_SESSION` 是环境变量，换终端即丢。

## 相关页面

- [[concepts/chezmoi-templating]] — 模板渲染机制
- [[concepts/chezmoi-workflow]] — add/edit/diff/apply 四动词 + update/init 跨机
- [[synthesis/Research: chezmoi]] — chezmoi 综合
