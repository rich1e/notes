---
title: 2026-03-17
source: https://litearch.cn/obsidian/notes/%E6%88%91%E7%9A%84%E7%AC%94%E8%AE%B0/%E7%BC%96%E7%A8%8B/Ops/17%E3%80%81chezmoi%20%E9%83%A8%E7%BD%B2%E7%BB%B4%E6%8A%A4%E6%95%99%E7%A8%8B.html
author:
  - "[[loaden航]]"
published: 2026-07-24
created: 2026-07-25
description: 17、chezmoi 部署维护教程 | loaden航
tags:
  - clippings
  - chezmoi
  - dotfiles
---
## Chezmoi 部署与拉取教程

> dotfiles 跨机器同步方案 · chezmoi + age + GitHub  
> 三段式命令语义： `czpush` （推）/ `czpull` （拉）/ `czapply` （应用）

---

## 1\. 架构总览

```gradle
┌─────────────────┐
│  GitHub 远端    │  github.com/luduihang/dotfiles
└────────┬────────┘
         │ czpush (推)
         │ czpull (拉)
         ▼
┌──────────────────────────┐
│ ~/.local/share/chezmoi   │  ← source of truth (源)
└────────┬─────────────────┘
         │ czapply (部署)
         ▼
┌─────────────────┐
│  ~/ 真实环境    │  .bashrc .zshrc .config/* 等
└─────────────────┘
复制代码
```

**核心思想** ：

- **源** （ `~/.local/share/chezmoi` ）：唯一真相
- **远端** ：备份 + 多机同步的中转
- **真实环境** `~/` ：部署目标

---

## 2\. 三段式命令

### 2.1 czpush — 推送本地修改到远端

类似 `git push` 。把 `~/` 的改动收录到源，再 push 到 GitHub。

```bash
czpush
language-bash复制代码
```

**做了什么** ：

1. 扫描所有 chezmoi 已管理的文件
2. 把有变化的文件 `chezmoi add` 到源（跳过 SSH 私钥、.age 加密文件、bin/ 二进制）
3. `git add . && commit -m "auto sync: <时间戳>"`
4. `git push` 到 `luduihang/dotfiles`

**何时用** ：

- 你改了 `~/` 里的某个 dotfile，想同步到其他机器
- 你新写了一个配置，想纳入 chezmoi 管理

---

### 2.2 czpull — 从远端拉取最新到源

类似 `git pull` 。从 GitHub 拉取最新源到本地源目录。

```bash
czpull
language-bash复制代码
```

**做了什么** ：

1. `chezmoi git -- pull --rebase --autostash`
2. 自动 stash 未提交改动，rebase 后再 pop

**何时用** ：

- 你想看看远端有没有新配置
- 另一台机器刚 push 了新东西，你想同步过来

> **注意** ： `czpull` **不会** 自动 apply 到 `~/` ，还要跑一次 `czapply`

---

### 2.3 czapply — 把源部署到 ~/

类似 `git apply` 。把源里的内容覆盖到真实环境。

```bash
czapply
language-bash复制代码
```

**做了什么** ：

1. `chezmoi apply -v`
2. 逐个文件对比源和 `~/` ，有差异就覆盖

**何时用** ：

- 跑完 `czpull` 后，必须 `czapply` 才生效
- 你直接编辑了源文件（ `~/.local/share/chezmoi/dot_xxx` ），想让 `~/` 同步

> **注意** ：bashrc/zshrc 等需要重启 shell 才生效：
> 
> ```bash
> czapply && exec bash    # 或 exec zsh
> language-bash复制代码
> ```

---

### 2.4 完整工作流

| 你想做的事 | 命令序列 |
| --- | --- |
| 推送本地改动到远端 | `czpush` |
| 拉取远端最新到本地 | `czpull && czapply && exec bash` |
| 推送 + 部署 | `czpush && czapply` |
| 改了源文件想推送+部署 | `czpush && czapply` |

---

## 3\. 新机器首次部署

### 3.1 一步到位（推荐）

```bash
# 1. 设置代理
export all_proxy=http://162.14.77.140:7897

# 2. 安装 mihomo 代理 (国内新机器必须先做这一步)
curl -fsSL https://raw.githubusercontent.com/luduihang/dotfiles/main/proxy-setup.sh | bash

# 3. 安装 dotfiles (代理通了之后, 自动装 age/chezmoi/nvim/yazi/zoxide + 部署所有配置)
export all_proxy=http://127.0.0.1:7897
curl -fsSL https://raw.githubusercontent.com/luduihang/dotfiles/main/bootstrap.sh | bash

# 4. 重启 shell 让新 bashrc 生效
exec bash
language-bash复制代码
```

---

### 3.2 bootstrap.sh 做了什么

1. **环境准备** ： `ensure_base` 装 curl/unzip/sudo（精简 Linux 镜像需要）
2. **搭代理** ： `install_mihomo` + `copy_mihomo_config` + `start_mihomo` + `check_proxy`
3. **装工具** （在线，走代理）：
	- `install_age` — 加密工具
		- `install_chezmoi` — dotfiles 管理器
		- `install_nvim` — 文本编辑器
		- `install_yazi` — 终端文件管理器
		- `install_zoxide` — 智能目录跳转
4. **配置密钥** ： `setup_age_key` 提示输入 `AGE-SECRET-KEY` 私钥
5. **应用配置** ： `apply_dotfiles` 调 `chezmoi init` + `chezmoi apply`

---

### 3.3 AGE-SECRET-KEY 私钥来源

新机器需要你的 age 私钥来解密 SSH 私钥、API key 等加密文件。

**获取方式** （从已有机器）：

```bash
# 在已部署的机器上运行
cat ~/.config/age/key.txt
language-bash复制代码
```

**输出示例** ：

```
AGE-SECRET-KEY-1xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
复制代码
```

**新机器上** ： `bootstrap.sh` 跑到最后会提示输入这串密钥，粘贴回车即可。

> **安全注意** ：
> 
> - 私钥绝不提交到任何 git 仓库
> - 不要通过不安全的渠道传输（推荐 GPG 加密邮件 / 临时 SSH / 加密网盘）
> - 建议本地保留多份备份

---

## 4\. 已有机器同步配置

### 4.1 第一次拉取（已有 chezmoi 但未拉过远端）

```bash
cd ~/.local/share/chezmoi
czpull       # 拉取远端
czapply      # 部署到 ~/
exec bash
language-bash复制代码
```

---

### 4.2 日常同步

```bash
# 场景 A: 另一台机器推了新东西, 拉过来
czpull && czapply && exec bash

# 场景 B: 本机改了 ~/ 配置, 推给其他机器
czpush
language-bash复制代码
```

---

### 4.3 改了源文件（高级）

```bash
# 直接编辑源 (vim/nvim)
nvim ~/.local/share/chezmoi/dot_bashrc

# 推送到远端 + 部署到 ~/
czpush && czapply
language-bash复制代码
```

---

## 5\. 常见问题

### Q1: czpush 后远端没收到？

检查网络和 SSH key：

```bash
ssh -T git@github.com   # 测 SSH 连通性
chezmoi git -- status   # 看本地源状态
language-bash复制代码
```

---

### Q2: 改了 ~/ 里的.bashrc 但 czpush 没推上去？

确认 `chezmoi managed` 列表里有这个文件：

```bash
chezmoi managed | grep bashrc
language-bash复制代码
```

不在列表里说明这个文件没纳入 chezmoi 管理，需要先 `chezmoi add ~/.bashrc` 。

---

### Q3: czapply 后 bashrc 没生效？

bashrc 是登录时加载的，需要重启 shell：

```bash
czapply && exec bash
language-bash复制代码
```

---

### Q4: 冲突了（rebase 失败）？

czpull 用 `autostash` 自动处理大多数冲突。如果失败：

```bash
cd ~/.local/share/chezmoi
chezmoi git -- status              # 看冲突文件
chezmoi git -- checkout -- <file>  # 放弃本地改动用远端版本

# 或手动编辑冲突文件后:
chezmoi git -- add .
chezmoi git -- rebase --continue
language-bash复制代码
```

---

### Q5: 想放弃本地 ~/ 改动，让源覆盖回来？

```bash
czapply   # 直接覆盖 ~/
language-bash复制代码
```

chezmoi apply 默认就是用源覆盖 `~/` （不会合并）。

---

### Q6: AGE 私钥在哪存？丢了怎么办？

- 私钥在 `~/.config/age/key.txt` （chezmoi 默认位置）
- 模板配置在 `~/.config/chezmoi/chezmoi.toml` 或 `dot_chezmoi.toml.tmpl`
- 丢了 = 没法解密 `*.age` 文件 = **重新部署新机器时所有加密配置失效**
- **强烈建议** ：把 `key.txt` 多处备份（密码管理器 + 加密 U 盘 + 打印一份纸质）

---

## 6\. 配置文件位置速查

| 路径 | 作用 |
| --- | --- |
| `~/.local/share/chezmoi/` | 源目录（source of truth） |
| `~/.local/share/chezmoi/.git/` | 源的 git 仓库 |
| `~/.config/chezmoi/chezmoi.toml` | chezmoi 全局配置 |
| `~/.config/age/key.txt` | age 私钥 |
| `~/` | 真实环境（czapply 部署目标） |
| `github.com/luduihang/dotfiles` | 远端 GitHub 仓库 |

---

## 7\. 相关命令速查

| chezmoi | 说明 |
| --- | --- |
| `chezmoi managed` | 列出所有 chezmoi 管理的文件 |
| `chezmoi diff` | 对比源和 `~/` 的差异 |
| `chezmoi cd` | 跳到源目录 |
| `chezmoi init luduihang/dotfiles` | 从远端初始化（bootstrap 用） |
| `chezmoi apply -v` | 部署到 `~/` （带 -v 看详情） |
| `chezmoi add <file>` | 把文件纳入管理 |
| `chezmoi git -- <cmd>` | 在源目录里跑 git 命令 |
| `czpush` | 自定义：推送本地修改到远端 |
| `czpull` | 自定义：从远端拉取到源 |
| `czapply` | 自定义：部署源到 `~/` |

---

## 8\. 心法总结

**三段式哲学** （对应 git）：

```
本机改了什么？ → czpush   (类似 git push)
远端变了什么？ → czpull   (类似 git pull)
源怎么生效？   → czapply  (类似 git apply)
复制代码
```

**和 git 的对应** ：

| git | chezmoi | 方向 |
| --- | --- | --- |
| `git push` | `czpush` | 本地 → 远端 |
| `git pull` | `czpull` | 远端 → 本地源 |
| `git apply` | `czapply` | 源 → 真实环境 |

**职责清晰** ：

- `czpush` = 推送，不拉取不部署
- `czpull` = 拉取，不推送不部署
- `czapply` = 部署，不拉取不推送

按需组合，覆盖所有维护场景。

---

## 9\. 踩坑清单

### 9.1 部署前：环境检查

| 检查项 | 命令 | 期望结果 |
| --- | --- | --- |
| 代理连通 | `curl -s --max-time 5 -o /dev/null -w "%{http_code}\n" --proxy http://127.0.0.1:7897 http://www.google.com` | `200/301/302` |
| age 私钥存在 | `ls -la ~/.config/age/key.txt` | 文件存在 + 600 权限 |
| age 私钥内容 | `cat ~/.config/age/key.txt` | `AGE-SECRET-KEY-1...` |
| chezmoi 模板 | `ls ~/.local/share/chezmoi/.chezmoi.toml.tmpl` | 文件存在 |
| chezmoi 配置 | `ls ~/.config/chezmoi/chezmoi.toml` | 必须存在（否则 age 解密失败） |

---

### 9.2 部署流程中（按顺序）

```bash
# 第 1 步: 安装 mihomo 代理
curl -fsSL https://raw.githubusercontent.com/luduihang/dotfiles/main/proxy-setup.sh | bash

# 第 2 步: 验证代理 (重要!)
export all_proxy=http://127.0.0.1:7897
curl -s --max-time 5 -o /dev/null -w "%{http_code}\n" --proxy http://127.0.0.1:7897 http://www.google.com

# 第 3 步: bootstrap.sh (核心)
curl -fsSL https://raw.githubusercontent.com/luduihang/dotfiles/main/bootstrap.sh | bash
language-bash复制代码
```

**bootstrap 跑完后必须验证** ：

```bash
ls ~/.config/chezmoi/chezmoi.toml        # 必须存在
cat ~/.config/chezmoi/chezmoi.toml       # 应该有 [age] 段
ls ~/.config/age/key.txt                 # 必须存在
cat ~/.config/age/key.txt                # 应该有 AGE-SECRET-KEY
language-bash复制代码
```

**如果 chezmoi.toml 不存在（最容易踩的坑）** ：

```bash
chezmoi init --force       # 强制从模板重新生成
language-bash复制代码
```

---

### 9.3 部署后：手动补全 SSH

chezmoi 不会自动创建 `~/.ssh` 目录——你必须手动：

```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
chezmoi apply -v
chmod 600 ~/.ssh/id_ed25519 ~/.ssh/config
chmod 644 ~/.ssh/id_ed25519.pub
language-bash复制代码
```

---

### 9.4 GitHub raw CDN 缓存陷阱

**症状** ：明明已经 push 了新代码，但 `curl https://raw.githubusercontent.com/.../bootstrap.sh | bash` 跑的还是旧版。

**原因** ：raw.githubusercontent.com 用 CloudFront CDN，URL 相同时缓存命中，TTL 5 分钟。`?nocache=...` query string 不起作用（raw 不解析 query）。

**绕过方法——用 commit SHA** ：

```bash
# 先拿到当前 main 的 SHA (从 GitHub API)
SHA=$(curl -fsSL "https://api.github.com/repos/luduihang/dotfiles/commits/main" | grep '"sha"' | head -1 | cut -d'"' -f4)

# 用 SHA 拿 (100% 最新, bypass CDN)
curl -fsSL "https://raw.githubusercontent.com/luduihang/dotfiles/${SHA}/bootstrap.sh" | bash
language-bash复制代码
```

---

### 9.5 SSH key 部署（避免 identity\_sign 报错）

**症状** ： `identity_sign: private key ~/.ssh/id_ed25519 contents do not match public`

**原因** ：agent 缓存了旧 key，或磁盘上 key 真的不配对。

**修复方法** ：

```bash
eval "$(ssh-agent -s)"
ssh-add -D                                # 清缓存
ssh-add ~/.ssh/id_ed25519                # 加载新 key

# 强制 SSH 用指定 key (绕开 agent 缓存)
cat >> ~/.ssh/config << 'EOF'
Host github.com
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
EOF
chmod 600 ~/.ssh/config
language-bash复制代码
```

---

### 9.6 推送前的本地验证（4 步必跑）

```bash
# 1. 语法检查
bash -n bootstrap.sh
bash -n dot_bashrc
zsh -n dot_zshrc

# 2. 关键函数都在
grep -c "^install_zoxide" bootstrap.sh    # 应该 >= 1
grep "function y\|zoxide init" dot_bashrc # 应该 2 行
grep "function y\|zoxide init" dot_zshrc  # 应该 2 行

# 3. 关键 URL 都对
grep "zoxide-0.9.9" bootstrap.sh          # 应该带 -0.9.9- 段

# 4. 推送 + 验证
git push origin main
curl -fsSL "https://raw.githubusercontent.com/luduihang/dotfiles/$(git rev-parse HEAD)/bootstrap.sh" | head -50
language-bash复制代码
```

---

### 9.7 速记表

| 问题 | 一行修法 |
| --- | --- |
| chezmoi.toml: No such file | `chezmoi init --force` |
| encryption not configured | `chezmoi init --force` |
| install\_zoxide: command not found | 重拉 bootstrap.sh（用 commit SHA） |
| y/czpull not found | `exec bash` 重启 shell |
| ~/.ssh/config missing | `mkdir -p ~/.ssh && chmod 700 && chezmoi apply -v && chmod 600 ~/.ssh/*` |
| identity\_sign: contents do not match | `ssh-add -D && ssh-add ~/.ssh/id_ed25519` |
| Connection refused 7897 | `nohup ~/.local/bin/mihomo -f ~/.config/mihomo/config.yaml &` |
| GitHub raw 是旧版 | 用 commit SHA URL 绕过 CDN |
| bashrc/y()/zoxide init 反复消失 | 检查 czsync/coredump，别加 `chezmoi add ~/.bashrc` |

---

### 9.8 核心心法

1. `.chezmoi.toml` 是 age 解密的开关——不在就全部.age 文件解不开
2. `chezmoi apply` 不会创建 `~/.ssh` ——手动 mkdir
3. `czpush` / `czpull` / `czapply` 三段式——别再让 czsync 自动 add rc
4. GitHub raw 会缓存——SHA 绕过
5. 每次改完源 push 前先本地 grep 验证—— `grep -c "^install_xxx"`

---

## 附录 A：版本信息

- chezmoi ≥ 2.0
- 最后更新：2026-06-21

---

转载请注明来源，欢迎对文章中的引用来源进行考证，欢迎指出任何有错误或不够清晰的表达。可以在下面评论区评论，也可以邮件至 kipleyarch@gmail.com