---
title: "sysctl Kernel Hardening — Linux 内核参数加固"
category: skills
tags:
  - sysctl
  - kernel
  - hardening
  - linux
  - network
  - skills
summary: "Linux sysctl 内核加固操作 skill：网络栈（IPv4/IPv6 forwarding / ICMP redirect / source route）+ ASLR / 内核指针隐藏 / BPF / ptrace / 文件系统保护。完整表格见 [[references/sysctl-hardening-table]]。"
sources:
  - "https://github.com/imthenachoman/How-To-Secure-A-Linux-Server/blob/main/linux-kernel-sysctl-hardening.md"
created: "2026-08-13T10:17:00Z"
updated: "2026-08-13T10:17:00Z"
provenance:
  extracted: 0.90
  inferred: 0.08
  ambiguous: 0.02
base_confidence: 0.65
lifecycle: draft
lifecycle_changed: "2026-08-13"
tier: supporting
relationships:
  - target: "[[entities/imthenachoman-how-to-secure-a-linux-server]]"
    type: derived_from
  - target: "[[references/sysctl-hardening-table]]"
    type: related_to
---

# sysctl Kernel Hardening — Linux 内核参数加固

> 从 imthenachoman/How-To-Secure-A-Linux-Server/linux-kernel-sysctl-hardening.md（19KB 完整表格）蒸馏的 sysctl 内核加固 skill。**完整参数表见 [[references/sysctl-hardening-table]]** — 本页是分类与原理。

## 加载方式

```bash
# 立即生效（重启失效）
sudo sysctl -w net.ipv4.ip_forward=0

# 永久生效 — 写入 /etc/sysctl.d/99-hardening.conf
echo "net.ipv4.ip_forward = 0" | sudo tee /etc/sysctl.d/99-hardening.conf

# 应用所有配置
sudo sysctl --system

# 验证
sudo sysctl net.ipv4.ip_forward
```

**最佳实践**：所有 hardening 配置放 `/etc/sysctl.d/99-hardening.conf`（数字大 = 最后加载，可覆盖发行版默认）。

## 5 大加固域

### 1. 网络栈加固（`net.*`）

防 IP spoofing / 路由劫持 / 嗅探：

```ini
# === IPv4 ===
net.ipv4.ip_forward = 0                    # 禁用 IP forwarding（除非是路由器）
net.ipv4.conf.all.rp_filter = 1           # 反向路径过滤（防 spoofing）
net.ipv4.conf.default.rp_filter = 1
net.ipv4.icmp_echo_ignore_broadcasts = 1  # 防 smurf 攻击
net.ipv4.icmp_ignore_bogus_error_responses = 1
net.ipv4.conf.all.accept_redirects = 0    # 不接受 ICMP redirect（防 MITM）
net.ipv4.conf.default.accept_redirects = 0
net.ipv4.conf.all.secure_redirects = 0    # 即使来自默认网关也不接受
net.ipv4.conf.default.secure_redirects = 0
net.ipv4.conf.all.send_redirects = 0      # 不发送 redirect（除非是路由器）
net.ipv4.conf.default.send_redirects = 0
net.ipv4.conf.all.accept_source_route = 0 # 禁用源路由（防 IP spoofing）
net.ipv4.conf.default.accept_source_route = 0
net.ipv4.tcp_syncookies = 1                # 防 SYN flood
net.ipv4.tcp_rfc1337 = 1                  # 防 TIME_WAIT assassination

# === IPv6（如果不用 IPv6，全部禁用）===
net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1
net.ipv6.conf.all.accept_redirects = 0
net.ipv6.conf.default.accept_redirects = 0
net.ipv6.conf.all.accept_source_route = 0
net.ipv6.conf.default.accept_source_route = 0
```

### 2. ASLR + 内核指针隐藏（`kernel.*`）

```ini
# === ASLR（地址空间布局随机化）===
kernel.randomize_va_space = 2              # 完全 ASLR（0=关闭, 1=保守, 2=完全）

# === 内核指针隐藏（防内核地址泄漏）===
kernel.kptr_restrict = 2                   # /proc/kallsyms 显示 0 给非 root

# === dmesg 限制 ===
kernel.dmesg_restrict = 1                  # 仅 root 可读 dmesg

# === BPF JIT 限制（防 eBPF 漏洞）===
kernel.unprivileged_bpf_disabled = 1      # 非 root 禁用 BPF

# === ptrace 限制（防进程注入）===
kernel.yama.ptrace_scope = 3               # 仅 parent 可 ptrace，或 root

# === perf 子系统限制 ===
kernel.perf_event_paranoid = 3             # 完全限制 perf 到非 root

# === kexec 限制（防 kexec 注入恶意内核）===
kernel.kexec_load_disabled = 1
```

### 3. BPF / JIT hardening（`net.core.bpf_*`）

```ini
net.core.bpf_jit_harden = 2                # BPF JIT 强化模式
```

### 4. 文件系统保护（`fs.*`）

```ini
# === protected_*
fs.protected_fifos = 2                     # 防 FIFO 攻击
fs.protected_regular = 2                  # 防 symlink 攻击
fs.protected_symlinks = 1                 # 防 world-writable symlink

# === sudo 路径保护 ===
fs.protected_hardlinks = 1
```

### 5. 系统全局限制

```ini
# === core dump 限制 ===
kernel.core_pattern = |/bin/false         # 完全禁用 core dump
fs.suid_dumpable = 0

# === PID 限制 ===
kernel.pid_max = 65536                     # 默认即可

# === inotify 限制（防资源耗尽）===
fs.inotify.max_user_watches = 524288       # 默认 8192 太小，CI/CD 容易撞
```

## 关键决策点

### 「IP forwarding = 0」会破坏 Docker / K8s 吗？

**会**。Docker 默认需要 `net.ipv4.ip_forward=1`。

**解法**：用 iptables / nftables 替代 netfilter forwarding，或在容器网络命名空间内启用 forwarding（容器默认自己的 netns）。

### 「IPv6 disable」会断 IPv6-only 服务吗？

**会**。如果你的服务依赖 IPv6（IPv6-only 内网、Cilium、Istio 等），不要 disable，改只禁 `accept_ra` / `accept_redirects`。

### 「ASLR = 2」会影响性能吗？

**轻微影响**（~1%）。但防 ROP / buffer overflow 攻击的收益远大于此。

### 「BPF disabled」会影响什么？

非 root 用户的 bpf() 系统调用 — 但合法运维工具（bpftrace、systemtap）通常以 root 跑。

## 反向论证

| 误区 | 实际 |
|---|---|
| 「sysctl 改了就生效」 | `sysctl -w` 立即生效；配置文件需 `--system` |
| 「Hardening 后 Linux 性能大降」 | ASLR ~1%、BPF 0%（root 没影响）；整体 <3% |
| 「sysctl 等同于防火墙」 | sysctl 是**内核参数**；防火墙是 netfilter 规则 — 两层独立 |
| 「Docker 默认 secure」 | Docker daemon 启动时会**强制开启 ip_forward**；hardening 与容器有冲突点 |
| 「所有发行版都一样」 | 发行版默认 sysctl 不同；Debian/Ubuntu 通常较松；RHEL/CentOS 较严 |

## 验证脚本

```bash
# 检查当前所有 hardening 配置
sudo sysctl -a | grep -E "(randomize_va_space|kptr_restrict|dmesg_restrict|unprivileged_bpf|ptrace_scope|accept_redirects|accept_source_route)"

# 对比：CIS Benchmark 推荐值 vs 当前
# CIS 推荐：kernel.randomize_va_space = 2, kernel.kptr_restrict = 2, ...

# 用 Lynis 自动跑一遍
sudo lynis audit system
```

## Open Questions

1. **Cloud provider 内核**（AWS / GCP / Azure）是否有自定义 sysctl？— 可能与上述配置冲突 ^[ambiguous]
2. **Cilium / eBPF-based 网络** 在 `unprivileged_bpf_disabled=1` 下还能用吗？— Cilium 以特权身份跑，**应该能** ^[inferred]
3. **systemd 容器化进程**（systemd-nspawn）是否会继承这些限制？— 默认不会 ^[inferred]

## 相关页面

- [[references/sysctl-hardening-table]] — 19KB 完整参数表
- [[concepts/linux-server-hardening-checklist]] — Layer 5 在整体清单
- [[concepts/intrusion-detection-stack]] — 与 HIDS 联动
- [[entities/imthenachoman-how-to-secure-a-linux-server]] — 源仓库