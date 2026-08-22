---
title: "sysctl Hardening Table — Linux Kernel Security Parameters"
category: references
tags:
  - sysctl
  - kernel
  - hardening
  - linux
  - reference-table
summary: "Linux kernel sysctl 安全加固参数索引表：122 个 key=value 配对，按域分组（fs/kernel/net.core/net.ipv4/net.ipv6/net.* 杂项）。源文件 imthenachoman/How-To-Secure-A-Linux-Server/linux-kernel-sysctl-hardening.md。"
sources:
  - "https://github.com/imthenachoman/How-To-Secure-A-Linux-Server/blob/main/linux-kernel-sysctl-hardening.md"
source_url: "https://github.com/imthenachoman/How-To-Secure-a-Linux-Server/blob/main/linux-kernel-sysctl-hardening.md"
created: "2026-08-13T10:17:00Z"
updated: "2026-08-13T10:17:00Z"
provenance:
  extracted: 0.85
  inferred: 0.10
  ambiguous: 0.05
base_confidence: 0.6
lifecycle: draft
lifecycle_changed: "2026-08-13"
tier: peripheral
relationships:
  - target: "[[entities/imthenachoman-how-to-secure-a-linux-server]]"
    type: derived_from
  - target: "[[skills/sysctl-kernel-hardening]]"
    type: extends
---

# sysctl Hardening Table — Linux Kernel Security Parameters

> imthenachoman 合并的 Linux kernel sysctl 安全加固参数索引 — 来自5 个独立来源（cyberciti / geektnt / linoxide / cloudpro / klaver sysctl）。**122 条 key=value** 配对，全部带 Torvalds Linux Documentation 链接。

## 适用 / 警告

> "I do not know what most of these settings do. This list is being provided just as reference material. I take no responsibility for anything."
> — Disclaimer, imthenachoman

- **不要盲目应用** — 某些参数（如 `net.ipv4.ip_forward=0`）会破坏 Docker / Kubernetes
- **逐项评估** — 参考 [[skills/sysctl-kernel-hardening]] 的分类与决策点
- **来源**：原文档基于 **2.2 内核 Documentation**（已陈旧），作者未找到更新的官方文档

## 5 大域分组

### 域 1: `fs.*` — 文件系统保护

| Key | 推荐值 | 作用 |
|---|---|---|
| `fs.file-max` | 65535 | 系统级最大打开文件数 |
| `fs.protected_hardlinks` | 1 | 防 hardlink 攻击 |
| `fs.protected_symlinks` | 1 | 防 symlink 攻击 |
| `fs.suid_dumpable` | 0 | SUID 程序不生成 core dump |
| `fs.protected_fifos` | 2 | 防 FIFO 攻击 |
| `fs.protected_regular` | 2 | 防 regular file 攻击 |

### 域 2: `kernel.*` — 内核安全

| Key | 推荐值 | 作用 |
|---|---|---|
| `kernel.randomize_va_space` | 2 | 完全 ASLR |
| `kernel.kptr_restrict` | 2 | /proc/kallsyms 隐藏内核地址 |
| `kernel.dmesg_restrict` | 1 | 非 root 不可读 dmesg |
| `kernel.yama.ptrace_scope` | 3 | 仅 parent 可 ptrace |
| `kernel.unprivileged_bpf_disabled` | 1 | 非 root 禁用 BPF |
| `kernel.core_uses_pid` | 1 | core dump 文件名带 PID |
| `kernel.ctrl-alt-del` | 0 | 禁用 Ctrl-Alt-Del 重启 |
| `kernel.sysrq` | 0 | 禁用 SysRq magic key |
| `kernel.kexec_load_disabled` | 1 | 禁用 kexec 加载新内核 |
| `kernel.perf_event_paranoid` | 3 | perf 子系统严格限制 |
| `kernel.pid_max` | 65535 | 最大 PID 数 |
| `kernel.msgmax` / `kernel.msgmnb` | 65535 | System V IPC 消息限制 |
| `kernel.shmmax` / `kernel.shmall` | 268435456 | System V 共享内存限制 |

### 域 3: `net.core.*` — 网络核心

| Key | 推荐值 | 作用 |
|---|---|---|
| `net.core.somaxconn` | 32768 | listen() 队列上限 |
| `net.core.netdev_max_backlog` | 16384 | 网卡 backlog |
| `net.core.rmem_default` / `wmem_default` | 262144 | socket 缓冲默认 |
| `net.core.rmem_max` / `wmem_max` | 16777216 | socket 缓冲最大 |
| `net.core.optmem_max` | 65535 | socket opt 大小 |
| `net.core.default_qdisc` | fq | 默认队列（fq 比 pfifo 更公平）|

### 域 4: `net.ipv4.*` — IPv4 加固（最大类，约 40 项）

**反 spoofing / MITM**：

| Key | 推荐值 | 作用 |
|---|---|---|
| `net.ipv4.conf.all.rp_filter` | 1 | 反向路径过滤（防 spoofing）|
| `net.ipv4.conf.default.rp_filter` | 1 | |
| `net.ipv4.conf.all.accept_redirects` | 0 | 不接受 ICMP redirect |
| `net.ipv4.conf.default.accept_redirects` | 0 | |
| `net.ipv4.conf.all.secure_redirects` | 0 | 即使来自默认网关也不接受 |
| `net.ipv4.conf.all.send_redirects` | 0 | 不发送 ICMP redirect |
| `net.ipv4.conf.all.accept_source_route` | 0 | 禁用源路由 |
| `net.ipv4.conf.all.log_martians` | 1 | 记录 martian packets |

**转发 / ICMP**：

| Key | 推荐值 | 作用 |
|---|---|---|
| `net.ipv4.ip_forward` | 0 | **禁用 IP forwarding（容器需要 1）**|
| `net.ipv4.conf.all.forwarding` | 0 | 同上（conf 子目录）|
| `net.ipv4.icmp_echo_ignore_broadcasts` | 1 | 防 smurf 攻击 |
| `net.ipv4.icmp_echo_ignore_all` | 1 | 不响应 ping（**强硬化**，可能影响监控）|
| `net.ipv4.icmp_ignore_bogus_error_responses` | 1 | 忽略异常 ICMP error |

**TCP 抗攻击**：

| Key | 推荐值 | 作用 |
|---|---|---|
| `net.ipv4.tcp_syncookies` | 1 | 防 SYN flood |
| `net.ipv4.tcp_rfc1337` | 1 | 防 TIME_WAIT assassination |
| `net.ipv4.tcp_max_syn_backlog` | 2048 | SYN backlog 大小 |
| `net.ipv4.tcp_max_orphans` | 16384 | 最大孤儿 socket |
| `net.ipv4.tcp_max_tw_buckets` | 1440000 | TIME_WAIT socket 上限 |
| `net.ipv4.tcp_tw_recycle` | 0 | **禁用**（NAT 场景会破坏连接）|
| `net.ipv4.tcp_tw_reuse` | 1 | 允许 TIME_WAIT 重用（作为客户端时）|

**TCP 性能**：

| Key | 推荐值 | 作用 |
|---|---|---|
| `net.ipv4.tcp_rmem` | 8192 87380 16777216 | TCP 读缓冲 min/default/max |
| `net.ipv4.tcp_wmem` | 8192 65536 16777216 | TCP 写缓冲 |
| `net.ipv4.tcp_congestion_control` | htcp / bbr | 拥塞控制算法 |
| `net.ipv4.tcp_fastopen` | 3 | TFO 客户端 + 服务端 |
| `net.ipv4.tcp_ecn` | 1 | 显式拥塞通知 |
| `net.ipv4.tcp_window_scaling` | 0 | **禁用**（某些 NAT 场景会破坏）|
| `net.ipv4.tcp_sack` | 0 | 选择性确认（广域网优化）|
| `net.ipv4.tcp_timestamps` | 1 | 时间戳（保护 PAWS）|
| `net.ipv4.tcp_no_metrics_save` | 1 | 不保存 TCP metrics（节内存）|
| `net.ipv4.tcp_fin_timeout` | 15 | FIN-WAIT-2 超时缩短 |
| `net.ipv4.tcp_keepalive_time` | 1800 | keepalive 启动时间 |
| `net.ipv4.tcp_keepalive_intvl` | 15 | keepalive 间隔 |
| `net.ipv4.tcp_keepalive_probes` | 5 | keepalive 探测次数 |

### 域 5: `net.ipv6.*` — IPv6（如果不用，全部禁用）

| Key | 推荐值 | 作用 |
|---|---|---|
| `net.ipv6.conf.all.disable_ipv6` | 1 | 禁用 IPv6（**慎用**）|
| `net.ipv6.conf.default.disable_ipv6` | 1 | |
| `net.ipv6.conf.all.accept_redirects` | 0 | 同 IPv4 |
| `net.ipv6.conf.all.accept_source_route` | 0 | |
| `net.ipv6.conf.all.accept_ra` | 0 | 不接受路由器公告（**默认**应禁）|

## Per-interface 注意

`net.ipv4.conf.<iface>.*` 需要为每个网络接口显式设。原文档针对 `eth0` — 但现代是 `ens3` / `enp0s3` 等命名约定。

```bash
# 自动检测接口名并应用
INTERFACE=$(ip route | grep default | awk '{print $5}' | head -1)
sudo sysctl -w net.ipv4.conf.$INTERFACE.rp_filter=1
sudo sysctl -w net.ipv4.conf.$INTERFACE.accept_redirects=0
```

## 应用方式

```bash
# 方法 1: 直接写文件
sudo tee /etc/sysctl.d/99-hardening.conf << 'EOF'
kernel.randomize_va_space = 2
kernel.kptr_restrict = 2
net.ipv4.ip_forward = 0
net.ipv4.conf.all.rp_filter = 1
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.tcp_syncookies = 1
EOF

sudo sysctl --system

# 方法 2: 直接用本表（cp 全部参数后写入）
```

## 验证

```bash
# 验证所有配置生效
sudo sysctl -a 2>/dev/null | grep -E "(randomize_va_space|kptr_restrict|rp_filter|syncookies|accept_redirects)" | sort

# Lynis 自动审计
sudo lynis audit system

# CIS Benchmark 对照
# https://www.cisecurity.org/cis-benchmarks/
```

## 相关页面

- [[skills/sysctl-kernel-hardening]] — 5 大域分类与决策点
- [[concepts/linux-server-hardening-checklist]] — Layer 5 在整体清单
- [[entities/imthenachoman-how-to-secure-a-linux-server]] — 源仓库
- [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks/) — 工业级对照标准