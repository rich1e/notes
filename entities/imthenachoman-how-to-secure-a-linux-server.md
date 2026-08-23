---
title: "imthenachoman/How-To-Secure-A-Linux-Server — Linux Server Hardening Guide"
category: entities
tags:
  - linux
  - security
  - hardening
  - github-repo
  - reference-guide
  - entity
summary: "GitHub 仓库 imthenachoman/How-To-Secure-A-Linux-Server：CC-BY-SA 4.0 的 Linux server hardening 实用指南，覆盖 SSH/防火墙/审计/入侵检测/sysctl 内核加固全栈 + 自带 nginx 子模块。"
sources:
  - "https://github.com/imthenachoman/How-To-Secure-A-Linux-Server"
source_url: "https://github.com/imthenachoman/How-To-Secure-A-Linux-Server"
created: "2026-08-13T10:17:00Z"
updated: "2026-08-13T10:17:00Z"
provenance:
  extracted: 0.85
  inferred: 0.10
  ambiguous: 0.05
base_confidence: 0.65
lifecycle: draft
lifecycle_changed: "2026-08-13"
tier: supporting
---

# imthenachoman/How-To-Secure-A-Linux-Server — Linux Server Hardening Guide

> 一份**不断演进的 Linux 服务器安全加固实战指南**，作者 [imthenachoman](https://github.com/imthenachoman)，CC-BY-SA 4.0 开源。配套有 [moltenbit](https://github.com/moltenbit) 的 [Ansible Playbooks 实现](https://github.com/moltenbit/How-To-Secure-A-Linux-Server-With-Ansible)。

## 仓库规模

| 文件 | 用途 | 字节数 |
|---|---|---|
| `README.md` | 主指南（SSH / 网络 / 审计 / 杂项 / 危险区） | 171 KB |
| `linux-kernel-sysctl-hardening.md` | sysctl 内核加固完整表格 | 19 KB |
| `nginx.md` | Nginx 加固子模块 | 1.4 KB |
| `LICENSE.txt` | CC-BY-SA 4.0 | 20 KB |

## 内容架构（按 TOC）

```
Introduction
├── Guide Objective
├── Why Secure Your Server
├── Why Yet Another Guide
└── Other Guides

Before You Start
├── Identify Your Principles
├── Picking A Linux Distribution
├── Pre/Post Installation Requirements
└── Using Ansible playbooks

The SSH Server
├── SSH Public/Private Keys
├── Create SSH Group For AllowGroups
├── Secure /etc/ssh/sshd_config
├── Remove Short Diffie-Hellman Keys
└── 2FA/MFA for SSH

The Basics
├── Limit sudo / su
├── FireJail sandbox
├── NTP Client
├── Securing /proc
├── Force Secure Passwords
├── Automatic Security Updates
└── Panic/Secondary/Fake password

The Network
├── Firewall With UFW
├── iptables + PSAD
├── Fail2Ban
└── CrowdSec

The Auditing
├── AIDE / ClamAV / Rkhunter / chrootkit
├── logwatch
├── ss / Lynis
└── OSSEC

The Danger Zone
The Miscellaneous
└── MSMTP / Gmail / Exim4 / iptables log split

To Do: SELinux / AppArmor / disk encryption / CIS-CAT / debsums
```

## 适用范围

> "**is** focused on **at-home** Linux servers. All of the concepts/recommendations here apply to larger/professional environments but those use-cases call for more advanced and specialized configurations that are out-of-scope for this guide."
> — About This Guide

- **面向家庭 Linux server**：桌面级电脑、单网卡、消费级路由器、动态 ISP WAN IP、需要从外部 SSH
- **distribution-agnostic**：不绑定特定发行版
- **不教 Linux 基础**：默认读者已会用 Linux
- **不在范围内**：物理安全、程序/工具深入用法、生产级加固

## 设计哲学

> "**aims** to make it easy by providing code you can copy-and-paste. You might need to modify the commands before you paste..."

- **可复制粘贴的代码片段**：所有改动都有 `echo` / `sed` / `awk` / `grep` 片段
- **改前必备份**：每条改动都先备份原文件
- **顺序合理**：SSH 优先于防火墙，防火墙优先于审计 — 后置章节依赖前置章节
- **WIP 标记**：rkhunter / chrootkit / ClamAV / AIDE 仍标 (WIP)，说明作者在迭代
- **TODO 未完成**：SELinux / AppArmor / disk encryption / CIS-CAT / debsums 等待贡献

## 关键工具集（作者推荐栈）

| 类别 | 工具 | 章节 |
|---|---|---|
| **防火墙** | UFW（Uncomplicated Firewall） | The Network |
| **入侵检测** | Fail2Ban + CrowdSec | The Network |
| **入侵检测（iptables 层）** | PSAD | The Network |
| **审计** | AIDE + ClamAV + rkhunter + chrootkit + Lynis + OSSEC | The Auditing |
| **日志** | logwatch | The Auditing |
| **SSH 加固** | sshd_config + 2FA + Diffie-Hellman 移除 | The SSH Server |
| **沙箱** | FireJail | The Basics |
| **密码** | pwquality + libpam-cracklib | The Basics |
| **更新** | unattended-upgrades + 邮件告警 | The Basics |
| **内核** | sysctl（独立子模块，19KB 完整表格） | linux-kernel-sysctl-hardening.md |

## 评估

| 维度 | 评分 | 说明 |
|---|---|---|
| **覆盖度** | ★★★★☆ | 覆盖 SSH/网络/审计全栈，但 SELinux/AppArmor/disk encryption 待补 |
| **可执行性** | ★★★★★ | 每步都有可粘贴的代码片段 |
| **原理深度** | ★★☆☆☆ | "doesn't delve into nook and crannies" — 偏操作手册 |
| **可移植性** | ★★★★★ | distribution-agnostic |
| **持续维护** | ★★★☆☆ | 仍在迭代，但频率未知 |
| **许可** | CC-BY-SA 4.0 | 可自由使用 + 衍生，但需同许可 + 署名 |

## 相关页面

- [[concepts/linux-server-hardening-checklist]] — 从本指南蒸馏的核心清单
- [[skills/ssh-server-hardening]] — SSH 章节蒸馏为可复用 skill
- [[skills/fail2ban-setup]] — Fail2Ban / CrowdSec 设置
- [[skills/sysctl-kernel-hardening]] — sysctl 子模块蒸馏
- [[references/sysctl-hardening-table]] — sysctl 完整加固表格
- [[concepts/fail2ban-vs-crowdsec]] — 两套入侵检测的对比
- [[concepts/intrusion-detection-stack]] — Linux 入侵检测工具栈全景
- moltenbit-ansible-playbooks — 配套 Ansible Playbooks

## Open Questions

1. **本指南的最新 commit 时间** — 没有直接的 last-updated 指示，需查 GitHub commits 页面
2. **WIP 章节何时完成** — rkhunter / chrootkit / ClamAV / AIDE 标记 (WIP) 状态 ^[ambiguous]
3. **作者是否维护 Debian/Ubuntu/CentOS 发行版专章** — 指南说 distribution-agnostic 但实际可能有偏向 ^[ambiguous]