---
title: "Fail2Ban / CrowdSec Setup — 应用层入侵检测"
category: skills
tags:
  - fail2ban
  - crowdsec
  - ssh-hardening
  - ids
  - skills
summary: "Fail2Ban 与 CrowdSec 设置 skill：日志正则匹配 + iptables ban（Fail2Ban 范式），或社区共享 IP 黑名单（CrowdSec 现代替代）。包含 jail 模板 / email 告警 / 持久化 ban。"
sources:
  - "https://github.com/imthenachoman/How-To-Secure-A-Linux-Server#firewall-with-ufw-uncomplicated-firewall"
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
relationships:
  - target: "[[entities/imthenachoman-how-to-secure-a-linux-server]]"
    type: derived_from
  - target: "[[concepts/linux-server-hardening-checklist]]"
    type: extends
  - target: "[[concepts/fail2ban-vs-crowdsec]]"
    type: related_to
---

# Fail2Ban / CrowdSec Setup — 应用层入侵检测

> 从 imthenachoman/How-To-Secure-A-Linux-Server 蒸馏的应用层 IDS skill。覆盖 Fail2Ban 经典配置 + CrowdSec 现代替代 + jail 模板。

## Fail2Ban 安装与基础配置

### 安装

```bash
# Debian/Ubuntu
sudo apt install fail2ban

# 启动 + 开机启动
sudo systemctl enable --now fail2ban
```

### `/etc/fail2ban/jail.local`（推荐覆盖默认）

```ini
[DEFAULT]
# 5 分钟内失败 3 次则 ban 1 小时
findtime = 300
maxretry = 3
bantime = 3600

# 忽略本机
ignoreip = 127.0.0.1/8 ::1  10.0.0.0/8  192.168.0.0/16

# 邮件告警
destemail = admin@yourdomain.com
sender = fail2ban@yourdomain.com
mta = sendmail
action = %(action_mwl)s  # mw = mail + whois, l = log

# 持久化 ban（重启后保留）
dbfile = /var/lib/fail2ban/fail2ban.sqlite3
dbpurgeage = 86400

# === 内置 SSH jail ===
[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
mode = aggressive  # aggressive 模式 1 次失败就 ban；normal 模式 maxretry 次

# === 自定义 jail 示例 ===
[nginx-http-auth]
enabled = true
filter = nginx-http-auth
port = http,https
logpath = /var/log/nginx/error.log

[nginx-botsearch]
enabled = true
filter = nginx-botsearch
port = http,https
logpath = /var/log/nginx/access.log
```

### 验证

```bash
# 检查 jail 状态
sudo fail2ban-client status
sudo fail2ban-client status sshd

# 解 ban IP
sudo fail2ban-client set sshd unbanip 1.2.3.4

# 手动 ban IP
sudo fail2ban-client set sshd banip 1.2.3.4

# 测试 jail 触发（用 ssh 多输错几次密码）
ssh wronguser@server   # 故意输错密码 3 次
sudo fail2ban-client status sshd
```

### 自定义 jail（filter 规则）

filter 文件位于 `/etc/fail2ban/filter.d/<name>.conf`：

```ini
[Definition]
failregex = ^.* authentication failed for .* from <HOST>.*$
ignoreregex =
```

`<HOST>` 是 Fail2Ban 保留字，自动匹配 IP。

## CrowdSec 安装与基础配置（现代范式）

### 为什么考虑 CrowdSec

- **社区共享 IP 黑名单** — 一个机器 ban 的 IP，全社区受益（防 brute-force bot）
- **容器化、API 驱动** — 比 Fail2Ban 更现代的架构
- **可视化 dashboard** — 中央控制台查看攻击图
- **跨机器 ban 同步** — 多台服务器共享 ban 列表

### 安装

```bash
# 安装脚本
curl -s https://packagecloud.io/install/repositories/crowdsec/crowdsec/script.deb.sh | sudo bash
sudo apt install crowdsec

# 查看 hub（社区共享规则）
sudo cscli hub list
sudo cscli scenarios install crowdsecurity/sshd-bf
```

### 启用 SSH brute-force 检测

```bash
sudo cscli parsers install crowdsecurity/sshd
sudo cscli scenarios install crowdsecurity/sshd-bf
sudo systemctl reload crowdsec
```

### 验证

```bash
# 检查本地 alerts
sudo cscli alerts list

# 注册 console（可选 — 中央 dashboard）
sudo cscli console enroll <your-token>
```

## Fail2Ban vs CrowdSec 选型

| 维度 | Fail2Ban | CrowdSec |
|---|---|---|
| **成熟度** | 20+ 年 | 5+ 年 |
| **学习曲线** | 简单（配置文件 + 正则）| 中（API + scenarios + hub）|
| **社区共享** | ❌ 无 | ✅ 全球 ban 列表 |
| **Dashboard** | ❌ 无 | ✅ 可选 console |
| **多机器同步** | 需自建 | ✅ 内置 |
| **资源占用** | 极低 | 中（Go runtime + hub sync）|
| **容器友好** | 一般 | ✅ 一等公民 |
| **WAF / API 保护** | 需手动配 | ✅ 内置 HTTP scenarios |

→ 详细对比见 [[concepts/fail2ban-vs-crowdsec]]

## 与防火墙联动

### Fail2Ban + UFW

Fail2Ban 默认用 iptables。**如果你用 UFW**，Fail2Ban action 需要切到 UFW：

```ini
# /etc/fail2ban/action.d/ufw.conf
[Definition]
actionban = ufw insert 1 deny from <ip> to any
actionunban = ufw delete deny from <ip> to any
```

```ini
# /etc/fail2ban/jail.local
[sshd]
action = ufw
```

### CrowdSec + UFW/NFTables

CrowdSec 自动检测已有防火墙并注册 bouncer：

```bash
# 安装 firewall bouncer
sudo apt install crowdsec-firewall-bouncer-iptables
sudo systemctl enable --now crowdsec-firewall-bouncer

# 或 NFTables 版本
sudo apt install crowdsec-firewall-bouncer-nftables
```

## 告警与告警去噪

### 避免「告警疲劳」

- **不要每个 jail 都开 mail 告警** — 只对关键 jail 告警
- **bantime 渐进** — 首次 ban 5min，二次 1h，三次 24h（fail2ban `recidive` jail）
- **whitelist 内部 IP** — 防止自己锁自己

### recidive jail（重复犯罪 IP 长期 ban）

```ini
[recidive]
enabled = true
filter = recidive
logpath = /var/log/fail2ban.log
bantime = 604800  ; 7 days
findtime = 86400  ; 1 day
maxretry = 5
```

## 反向论证

| 误区 | 实际 |
|---|---|
| 「Fail2Ban 装上就安全」 | 默认配置不 ban，需要 jail.local 启用 sshd 等关键 jail |
| 「CrowdSec 替代防火墙」 | **不是替代** — 是防火墙的补充层（封禁已知恶意 IP）|
| 「ban IP 后攻击者不会再来」 | bot net 有数百万 IP，单 IP ban 无意义 |
| 「Fail2Ban 防 DDoS」 | 抗不住大流量 DDoS，需要 CDN + WAF + 流量清洗 |
| 「CrowdSec 中央控制台是免费的」 | community edition 免费；enterprise 收费 |

## 相关页面

- [[concepts/linux-server-hardening-checklist]] — Layer 3 在整体清单
- [[skills/ssh-server-hardening]] — SSH hardening（Fail2Ban 的主要对象）
- [[concepts/fail2ban-vs-crowdsec]] — 详细对比
- [[concepts/intrusion-detection-stack]] — Linux IDS 工具全景
- [[entities/imthenachoman-how-to-secure-a-linux-server]] — 源仓库