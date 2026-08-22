---
title: "SSH Server Hardening — sshd_config 关键配置 + 2FA"
category: skills
tags:
  - ssh
  - security
  - hardening
  - sshd
  - 2fa
  - skills
summary: "SSH 服务端硬化操作 skill：`/etc/ssh/sshd_config` 关键指令（PermitRootLogin/PasswordAuthentication/AllowGroups/MaxAuthTries）+ Diffie-Hellman 弱密钥剔除 + Google Authenticator PAM 2FA + ssh-keysign 失能。Pre-flight 警告：改 SSH 配置前必须留 console fallback 物理访问。"
sources:
  - "https://github.com/imthenachoman/How-To-Secure-A-Linux-Server#the-ssh-server"
created: "2026-08-13T10:17:00Z"
updated: "2026-08-13T10:17:00Z"
provenance:
  extracted: 0.92
  inferred: 0.06
  ambiguous: 0.02
base_confidence: 0.65
lifecycle: draft
lifecycle_changed: "2026-08-13"
tier: supporting
relationships:
  - target: "[[entities/imthenachoman-how-to-secure-a-linux-server]]"
    type: derived_from
  - target: "[[concepts/linux-server-hardening-checklist]]"
    type: extends
---

# SSH Server Hardening — sshd_config 关键配置 + 2FA

> 从 imthenachoman/How-To-Secure-A-Linux-Server 蒸馏的 SSH 服务端硬化 skill。**改 SSH 配置前必读** — 锁出自己是真实风险。

## ⚠️ Pre-flight 警告

> "Make sure you have access to the server console (physical access or VM console) before you make any SSH changes."

**永远先准备**：

1. **Console 物理访问**（KVM / IPMI / VM console / 物理显示器键盘）
2. **第二个 SSH session 不关** — 当前 session 用于测试新配置
3. **回滚计划** — `cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak`
4. **`sshd -t`** 验证配置语法

## Step 1: 公私钥登录

```bash
# 客户端生成密钥（已有可跳过）
ssh-keygen -t ed25519 -C "your@email"

# 推送公钥到服务器
ssh-copy-id -i ~/.ssh/id_ed25519.pub user@server

# 验证可密钥登录后再禁用密码
```

**ed25519 优于 RSA**（更短、更快、同样安全）。

## Step 2: 创建 ssh-users 组 + AllowGroups

```bash
# 创建 ssh-users 组
sudo groupadd ssh-users
sudo usermod -aG ssh-users your_user

# 把允许 SSH 的用户加入此组（按需）
sudo usermod -aG ssh-users deploy_user
```

## Step 3: `sshd_config` 关键指令

```bash
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak
sudo vi /etc/ssh/sshd_config
```

**最小硬化配置**：

```sshd_config
# 端口（非必须，但减少 80% 自动化扫描）
Port 2222

# 协议版本（v2 是现代默认，老系统显式禁用 v1）
Protocol 2

# 登录横幅
Banner /etc/issue.net

# 鉴权
PermitRootLogin no                    # 禁用 root 直登
PubkeyAuthentication yes              # 启用公钥
PasswordAuthentication no             # 禁用密码登录（**最后开**）
PermitEmptyPasswords no
ChallengeResponseAuthentication no    # 除非用 2FA，否则禁用

# 限制
AllowGroups ssh-users                 # 仅 ssh-users 组可登录
MaxAuthTries 3                        # 每次连接最多 3 次密码尝试
MaxSessions 5                         # 每个连接最多 5 个 session
LoginGraceTime 30                      # 30 秒内未登录则断开

# 显示 / 转发
X11Forwarding no
AllowTcpForwarding no                 # 除非需要
PermitUserEnvironment no
```

**验证 + 重启**：

```bash
sudo sshd -t                           # 语法检查
sudo systemctl reload sshd             # 重新加载配置（不中断现有连接）
```

**测试**：开新 session 登录，确认能进再关旧 session。

## Step 4: 删除弱 Diffie-Hellman 密钥

SSH 的 DH 密钥交换用 `/etc/ssh/moduli`。弱密钥（< 2048 位）应剔除：

```bash
# 备份
sudo cp /etc/ssh/moduli /etc/ssh/moduli.bak

# 查看弱密钥
sudo awk '$5 < 2048' /etc/ssh/moduli

# 删除弱密钥
sudo awk '$5 >= 2048' /etc/ssh/moduli > /tmp/moduli.new
sudo mv /tmp/moduli.new /etc/ssh/moduli
```

或重新生成：

```bash
sudo ssh-keygen -G /tmp/moduli-sieve -b 4096
sudo ssh-keygen -T /tmp/moduli-test -f /tmp/moduli-sieve
sudo cp /tmp/moduli-test /etc/ssh/moduli
```

## Step 5: 2FA/MFA for SSH

用 Google Authenticator PAM 模块：

```bash
# 安装（Debian/Ubuntu）
sudo apt install libpam-google-authenticator

# 每个用户运行（生成 TOTP secret + 二维码）
google-authenticator

# 配置 PAM
echo "auth required pam_google_authenticator.so" | sudo tee -a /etc/pam.d/sshd

# sshd_config 添加
sudo tee -a /etc/ssh/sshd_config << 'EOF'
ChallengeResponseAuthentication yes
AuthenticationMethods publickey,keyboard-interactive
UsePAM yes
EOF

sudo systemctl reload sshd
```

**第一次登录**：公钥 + 6 位 TOTP code（手机 Google Authenticator / Authy）。

**丢失手机怎么办**：

- **预先生成 emergency scratch codes**（`google-authenticator` 命令会输出 5 个）
- **保留 console fallback** — 这是为什么 pre-flight 警告重要

## Step 6: ssh-keysign 失能（可选）

`ssh-keysign` 用于 host-based authentication（几乎不用）：

```sshd_config
HostbasedAuthentication no
EnableSSHKeysign no
```

## 加固后验证清单

```bash
# 1. SSH 协议版本（必须 2.x）
ssh -v user@server 2>&1 | grep "protocol"

# 2. 密码登录已禁用（应失败）
ssh -o PreferredAuthentications=password user@server

# 3. 弱算法已被禁（nmap 检查）
nmap --script ssh2-enum-algos -p 22 server

# 4. Diffie-Hellman 强度（应该都是 2048+）
sudo ssh -vvv user@server 2>&1 | grep -i "kex:"
```

## 反向论证

| 误区 | 实际 |
|---|---|
| 「非标准端口就安全」 | 仅减少自动化扫描，**不是安全措施** |
| 「公钥 + 密码双重认证最安全」 | 2FA 更强；密码可暴力 |
| 「禁用密码后一切安全」 | **没有 2FA = 一旦私钥泄露 = 直接 root** |
| 「改了 sshd_config 就生效」 | 必须 `sshd -t` + `reload`，旧 session 不受影响 |
| 「防火墙挡 SSH 就行」 | 防火墙挡外网，挡不住已侵入的内网横向移动 |

## 相关页面

- [[concepts/linux-server-hardening-checklist]] — Layer 1 在整体清单中的位置
- [[skills/fail2ban-setup]] — Layer 3 入侵检测（封禁 SSH brute-force）
- [[concepts/chezmoi-templating]] — `~/.ssh/config` 跨机器同步
- [[skills/chezmoi-bitwarden-secrets]] — SSH 私钥加密存储
- [[entities/imthenachoman-how-to-secure-a-linux-server]] — 源仓库