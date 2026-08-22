---
title: "Linux Intrusion Detection Stack — 入侵检测工具全景"
category: concepts
tags:
  - ids
  - security
  - linux
  - audit
  - stack
  - concept
summary: "Linux 入侵检测工具全景：网络层（PSAD/Fail2Ban/CrowdSec）+ 主机层（AIDE/ClamAV/rkhunter/chrootkit/Lynis/OSSEC）+ 日志层（logwatch/ss）。每层定位、覆盖范围、选型。"
sources:
  - "https://github.com/imthenachoman/How-To-Secure-A-Linux-Server#the-auditing"
created: "2026-08-13T10:17:00Z"
updated: "2026-08-13T10:17:00Z"
provenance:
  extracted: 0.82
  inferred: 0.13
  ambiguous: 0.05
base_confidence: 0.6
lifecycle: draft
lifecycle_changed: "2026-08-13"
tier: supporting
relationships:
  - target: "[[entities/imthenachoman-how-to-secure-a-linux-server]]"
    type: derived_from
  - target: "[[concepts/linux-server-hardening-checklist]]"
    type: extends
  - target: "[[concepts/fail2ban-vs-crowdsec]]"
    type: related_to
---

# Linux Intrusion Detection Stack — 入侵检测工具全景

> imthenachoman/How-To-Secure-A-Linux-Server 把 Linux IDS 分为 **网络层 + 主机层 + 日志层**。每层工具职责不同，组合使用才能覆盖完整攻击面。

## 3 层架构

```
[Internet / Network]
        ↓
   ┌────────────────┐
   │ Network 层 IDS │  ← 攻击到达边界时拦截
   └────────────────┘
        ↓
   ┌────────────────┐
   │ Host 层 IDS    │  ← 攻击已上机时检测
   └────────────────┘
        ↓
   ┌────────────────┐
   │ Log 层 IDS     │  ← 攻击后续 + 长期趋势
   └────────────────┘
```

## Network 层 — 攻击到达边界时拦截

| 工具 | 类型 | 触发源 | 响应 | 适用 |
|---|---|---|---|---|
| **UFW / iptables** | 防火墙（静态规则）| 配置 | drop / accept | 基础 — 所有服务器 |
| **PSAD** | iptables 日志分析 | iptables log | 主动 ban | 已有 iptables 时叠加 |
| **Fail2Ban** | 日志正则匹配 | auth.log / app log | iptables ban | SSH brute-force / app 攻击 |
| **CrowdSec** | 社区共享 + 日志 | 多种 log | 多 bouncer | 现代 / 多机 / 容器 |

### Network 层选型决策

```
单台 + 极简  →  UFW + Fail2Ban (传统组合)
多台 + 现代  →  CrowdSec (社区 + 跨机同步)
已有 iptables →  UFW + PSAD + Fail2Ban (三件套)
容器化       →  CrowdSec sidecar + firewalld-bouncer
```

→ 详细对比见 [[concepts/fail2ban-vs-crowdsec]] 与 [[skills/fail2ban-setup]]

## Host 层 — 攻击已上机时检测

| 工具 | 类型 | 检测对象 | 状态 | 输出 |
|---|---|---|---|---|
| **AIDE** | 文件完整性 | 文件/目录哈希变化 | WIP（imthenachoman 标 WIP）| 文件级 diff |
| **ClamAV** | 反病毒 | 病毒签名 + 启发式 | WIP | 病毒检测报告 |
| **rkhunter** | rootkit 检测 | rootkit 签名 + 异常检查 | WIP | rootkit 警告 |
| **chrootkit** | rootkit 检测 | 类似 rkhunter | WIP | rootkit 警告 |
| **Lynis** | 全系统安全审计 | CIS / NIST 控制项 | 成熟 | 审计建议 |
| **OSSEC** | HIDS（主机入侵检测）| 日志 + 文件 + 完整性 | 成熟 | 中央 alert |

### AIDE — 文件完整性监控（重点推荐）

```bash
# 安装
sudo apt install aide

# 初始化数据库（**在确认系统是干净状态时**）
sudo aideinit  # 或 sudo aide --init

# 比较
sudo aide --check

# 自动检查（cron）
echo "0 5 * * * /usr/bin/aide --check | mail -s 'AIDE report' admin@yourdomain.com" | sudo tee /etc/cron.d/aide
```

**关键**：AIDE 数据库**必须**在系统干净时初始化；之后任何文件变更都被标记。

### rkhunter / chrootkit — rootkit 检测

```bash
# 安装
sudo apt install rkhunter chkrootkit

# 扫描
sudo rkhunter --check --sk          # 跳过 keypress
sudo chkrootkit

# 定期 cron
echo "0 6 * * 0 /usr/bin/rkhunter --check --sk --cronjob" | sudo tee /etc/cron.d/rkhunter
```

### Lynis — 全系统审计

```bash
# 安装
sudo apt install lynis

# 审计
sudo lynis audit system

# 关键输出
# - Warnings (高优先级)
# - Suggestions (低优先级建议)
# - Hardening index (0-100)
```

### OSSEC — 完整 HIDS

```bash
# 安装（OSSEC 官方源）
wget https://updates.atomicorp.com/installers/atomic-release.deb
sudo dpkg -i atomic-release.deb
sudo apt update
sudo apt install ossec-hids ossec-hids-agent

# 配置 agent + server（agent 端）
sudo /var/ossec/bin/ossec-control start
```

**OSSEC 特色**：完整 HIDS = 日志监控 + 文件完整性 + rootkit 检测 + 主动响应 — **一站式替代 AIDE+rkhunter+logwatch**。

## Log 层 — 攻击后续 + 长期趋势

| 工具 | 类型 | 用途 |
|---|---|---|
| **logwatch** | 日志摘要 + 邮件 | 每日 / 每周邮件报告 |
| **ss** | 网络状态查询 | 实时监听端口查看 |
| **journalctl** | systemd 日志 | systemd 服务日志 |
| **logrotate** | 日志轮转 | 防 disk 满 |

### logwatch 配置

```bash
# 安装
sudo apt install logwatch

# 每日 cron 默认启用
# 配置 /etc/logwatch/conf/logwatch.conf
MailTo = admin@yourdomain.com
Detail = Med
Range = yesterday
```

### ss 查看监听端口

```bash
# 所有监听 TCP/UDP 端口
ss -tulnp

# 仅 TCP
ss -tlnp

# 已建立的连接
ss -tnp state established
```

## 实测推荐栈 (^[inferred])

| 场景 | 推荐栈 | 备注 |
|---|---|---|
| **家用 Linux server** | UFW + Fail2Ban + AIDE + logwatch | 经典四件套，资源友好 |
| **小型业务服务器** | UFW + CrowdSec + AIDE + Lynis + logwatch | CrowdSec 加社区共享 |
| **多机微服务** | CrowdSec sidecar + OSSEC + 中央 ELK | 中央化运维 |
| **合规驱动（PCI-DSS / SOC2）** | OSSEC + AIDE + ClamAV + rkhunter + logwatch + auditd | 完整审计 + 入侵检测 |

## WIP 状态警告

imthenachoman 把以下章节标 (WIP)：

- **AIDE** — 主章节有 setup 但章节标记 WIP
- **ClamAV** — WIP
- **rkhunter** — WIP
- **chrootkit** — WIP

→ **实战参考前需自行查官方文档** 补充 ^[ambiguous]

## 与 vault 已有页面的呼应

- [[concepts/chezmoi-templating]] — chezmoi 用于 dotfile 管理；IDS 配置（jail.local / fail2ban filter）也是 dotfile — **可纳入 chezmoi 追踪**
- [[skills/chezmoi-bitwarden-secrets]] — IDS 邮件告警的 SMTP 凭证应放在 Bitwarden
- [[concepts/dotfile-manager]] — 把整套 IDS 配置纳入 dotfile = 让加固 stack 可跨机器复现

## 反向论证

| 误区 | 实际 |
|---|---|
| 「IDS 防住所有攻击」 | IDS 检测 + 响应；不防已知漏洞（补丁是基础）|
| 「OSSEC 太重，小机不必」 | agent 端约 30MB RSS，可装 |
| 「AIDE 配置一次就够" | 应用更新会改文件 → 需 update AIDE db |
| 「rkhunter/chrootkit 是 rootkit 万灵药」 | 新 rootkit 可能无签名 → 行为检测必要 |
| 「logwatch 看一周日志够」 | 实时日志需 journal + alerting |

## Open Questions

1. **OSSEC vs Wazuh** — Wazuh 是 OSSEC fork，更活跃；imthenachoman 仍用 OSSEC ^?[ambiguous]
2. **ClamAV 在 Linux server 上 false positive 率** — 比 Windows 场景低，但需要 manual exclude ^[inferred]
3. **Lynis vs OpenSCAP** — 都是审计工具，前者更轻量，后者更系统化 ^[ambiguous]

## 相关页面

- [[concepts/linux-server-hardening-checklist]] — Layer 3-4 在整体清单
- [[skills/fail2ban-setup]] — Network 层操作 skill
- [[concepts/fail2ban-vs-crowdsec]] — Network 层选型
- [[entities/imthenachoman-how-to-secure-a-linux-server]] — 源仓库
- [OSSEC / Wazuh 文档](https://wazuh.com/)