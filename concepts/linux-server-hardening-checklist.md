---
title: Linux Server Hardening Checklist
category: concepts
tags:
  - linux
  - security
  - hardening
  - checklist
  - concept
summary: "从 imthenachoman/How-To-Secure-A-Linux-Server 蒸馏的 Linux server 加固全栈清单：威胁建模 → SSH → 基础（sudo/su/sandbox/自动更新）→ 网络（防火墙/入侵检测）→ 审计（完整性/rootkit/反病毒）→ 内核（sysctl）→ 日志/告警。"
sources:
  - "https://github.com/imthenachoman/How-To-Secure-A-Linux-Server"
created: "2026-08-13T10:17:00Z"
updated: "2026-08-13T10:17:00Z"
provenance:
  extracted: 0.82
  inferred: 0.13
  ambiguous: 0.05
base_confidence: 0.65
lifecycle: draft
lifecycle_changed: "2026-08-13"
tier: supporting
relationships:
  - target: "[[entities/imthenachoman-how-to-secure-a-linux-server]]"
    type: derived_from
---

# Linux Server Hardening Checklist

> 从 imthenachoman/How-To-Secure-A-Linux-Server 蒸馏的全栈 Linux server 加固清单。**不是完整指南** — 蒸馏核心节点，详细步骤见各 skill 页。

## 7 层加固栈

### Layer 0 — Threat Modeling（前置）

不先建模 = 在黑暗中加固。问自己：

| 问题 | 选项 |
|---|---|
| 为什么加固？ | 防止数据泄露 / DDoS 节点 / 勒索软件 / 监管合规 |
| 物理访问是攻击向量吗？ | 是 → disk encryption + BIOS 密码 + GRUB 密码 |
| 端口暴露？ | 是 → 仅暴露 22 + reverse proxy |
| 文件共享？ | 是 → Samba / NFS 上 SMB signing + 强认证 |
| **锁回自己怎么办？** | **永远先准备恢复路径**：Live USB + 物理访问 + 救援模式 |

> "If you don't know the answer to that question, I advise you research it first."
> — Why Secure Your Server, imthenachoman

### Layer 1 — SSH 加固（公网入口）

SSH 是**最常见的攻击面** — bot 一秒钟扫描一次 22 端口。加固顺序：

1. **SSH 公私钥** — 禁用密码登录（`PasswordAuthentication no`）
2. **创建 ssh-users 组 + `AllowGroups`** — 只允许特定 Unix 组登录
3. **`/etc/ssh/sshd_config` 关键配置** — 见 [[skills/ssh-server-hardening]]
4. **删除弱 Diffie-Hellman 密钥** — `ssh-keygen -G /tmp/moduli -b 4096` 替换
5. **2FA/MFA for SSH** — Google Authenticator PAM 模块

### Layer 2 — 基础用户/进程加固

- **限制 sudo** — 仅 wheel 组 / NOPASSWD 仅限服务账号
- **限制 su** — 仅 wheel 组可 `su`
- **FireJail 沙箱** — 限制应用可见文件系统/网络
- **NTP 客户端** — 时间一致是日志关联基础
- **`/proc` 加固** — 隐藏进程 PID、禁用 kcore
- **强密码策略** — `pwquality` + `libpam-cracklib`
- **自动安全更新** — `unattended-upgrades` + 邮件告警
- **诱饵密码** — Panic / Secondary / Fake 密码登录后触发 IP 封锁

### Layer 3 — 网络防火墙 + 入侵检测

| 工具 | 角色 | 适用 |
|---|---|---|
| **UFW** | 用户态防火墙（iptables 前端）| 入门 — Debian/Ubuntu 友好 |
| **iptables** | 内核 netfilter 前端 | 高级 — 规则最细 |
| **PSAD** | iptables 日志分析 + 主动封锁 | 已有 iptables 规则时叠加 |
| **Fail2Ban** | 日志正则匹配 → iptables ban | 应用层 brute-force |
| **CrowdSec** | 社区共享 IP 黑名单 + 本地 ban | Fail2Ban 现代替代，跨机器共享情报 |

→ 详细对比见 [[concepts/fail2ban-vs-crowdsec]]

### Layer 4 — 审计 / 入侵检测

| 工具 | 角色 | 状态 |
|---|---|---|
| **AIDE** | 文件/目录完整性监控 | WIP |
| **ClamAV** | 反病毒扫描 | WIP |
| **rkhunter** | rootkit 检测 | WIP |
| **chrootkit** | rootkit 检测（另一实现）| WIP |
| **Lynis** | 全系统安全审计 | 成熟 |
| **OSSEC** | 主机入侵检测（HIDS）| 成熟 |
| **logwatch** | 日志摘要 + 邮件告警 | 成熟 |
| **ss** | 监听端口查看 | 工具 |

→ 完整栈分析见 [[concepts/intrusion-detection-stack]]

### Layer 5 — 内核加固（sysctl）

19KB 完整表格见 [[references/sysctl-hardening-table]]。核心维度：

- 网络栈加固：`net.ipv4.*` / `net.ipv6.*` / `net.core.*`
- ASLR / 内核指针限制：`kernel.randomize_va_space` / `kernel.kptr_restrict`
- BPF / ptrace 限制：`kernel.unprivileged_bpf_disabled` / `kernel.yama.ptrace_scope`
- 文件系统保护：`fs.protected_*`

→ 详细 skill 见 [[skills/sysctl-kernel-hardening]]

### Layer 6 — 日志与告警

- **logwatch** — 每日 / 每周日志摘要邮件
- **`/var/log/auth.log`** — 登录尝试（已合 SSH / sudo / 失败）
- **`/var/log/ufw.log`** 或独立 iptables log file — 防火墙拦截
- **`/var/log/fail2ban.log`** — 入侵检测动作
- 关键是：**日志不会自己产生价值** — 必须配邮件/Slack/PagerDuty 告警才有用

### Layer 7 — 应用层（nginx 子模块）

[[entities/imthenachoman-how-to-secure-a-linux-server]] 自带 nginx.md（1.4KB）— 应用层加固是单独议题。

## 加固顺序原则

> "organized in an order that makes logical sense — i.e. securing SSH before installing a firewall."
> — About This Guide

- **SSH 先于防火墙** — 否则可能被锁出
- **防火墙先于审计** — 不必要的端口不应出现在审计结果里
- **基础（Layer 2）先于网络（Layer 3）** — 用户/进程加固是底层
- **内核（Layer 5）可在 Layer 1 之前或之后** — 视风险偏好

## 与 vault 已有页面的呼应

- [[concepts/chezmoi-templating]] — chezmoi 用于管理 `~/.ssh/config`、`/etc/ssh/sshd_config` 的分发与版本化 — **直接对接 Layer 1**
- [[skills/chezmoi-bitwarden-secrets]] — SSH 私钥加密存储在 Bitwarden + chezmoi 注入 — **直接对接 Layer 1.1**
- [[concepts/dotfile-manager]] — 整个加固栈的「基础设施」 — dotfile-as-code 让加固可跨机器复现

## 反向论证（^[inferred]）

| 误区 | 实际 |
|---|---|
| 「家用 Linux 不需要加固」 | 一旦暴露公网 = 与企业服务器同等攻击面（bot 不知道你是谁）|
| 「装个防火墙就够了」 | 防火墙只是 Layer 3；Layer 0-2 + 5 才是基础 |
| 「自动更新就够了」 | 自动更新只补已知 CVE；0day 需要 Layer 4 审计 |
| 「SSH 密码够长就安全」 | 16 字符密码 vs 私钥，**私钥** 才是工业级 |
| 「审计是事后动作」 | AIDE 主动监控 → 入侵后 5 分钟内知道；不审计 = 入侵可能潜伏数月 |

## Open Questions

1. **SELinux / AppArmor** — TODO 列表中，未来是否完成 ^[ambiguous]
2. **disk encryption** — TODO 列表中 ^[ambiguous]
3. **CIS-CAT 自动化合规检查** — TODO 列表中 ^[ambiguous]
4. **debsums（Debian 包校验）** — TODO 列表中 ^[ambiguous]
5. **Ansible Playbooks 同步状态** — 配套 moltenbit 仓库是否保持与本文档同步 ^[ambiguous]

## 相关页面

- [[entities/imthenachoman-how-to-secure-a-linux-server]] — 源仓库
- [[skills/ssh-server-hardening]] — Layer 1 操作 skill
- [[skills/fail2ban-setup]] — Layer 3 操作 skill
- [[skills/sysctl-kernel-hardening]] — Layer 5 操作 skill
- [[references/sysctl-hardening-table]] — sysctl 完整表格
- [[concepts/fail2ban-vs-crowdsec]] — Fail2Ban vs CrowdSec
- [[concepts/intrusion-detection-stack]] — Linux IDS 工具全景
- [[concepts/dotfile-manager]] — 加固基础设施
- [[concepts/chezmoi-templating]] — SSH 配置分发

## Related

- [[synthesis/concepts-linux-server-hardening-checklist × entities-imthenachoman-how-to-secure-a-linux-server]] — synthesis
