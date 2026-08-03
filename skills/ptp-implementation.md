---
title: PTP 轻量实现 — ptp-lite 要点
category: skills
tags: [ptp, c-language, implementation, networking]
sources: ["https://github.com/Lularible/ptp-book"]
created: 2026-07-03T09:00:00Z
updated: 2026-08-03T05:47:33Z
summary: "约 1000 行 C 实现的 ptp-lite，涵盖 PTP 报文编解码、主时钟发布和从时钟偏移计算的核心流程"
base_confidence: 0.85
lifecycle: reviewed
lifecycle_changed: 2026-08-03
lifecycle_reason: "auto-promoted by wiki-lint --consolidate: age>30d, confidence>0.7"
tier: peripheral
provenance:
  extracted: 0.85
  inferred: 0.13
  ambiguous: 0.02
relationships:
  - target: "[[concepts/ptp-ieee1588]]"
    type: implements
  - target: "[[concepts/ptp-delay-measurement]]"
    type: implements
  - target: "[[entities/linuxptp]]"
    type: related_to
---

# PTP 轻量实现 — ptp-lite 要点

ptp-lite 是《[[references/ptp-book-overview|PTP技术书]]》第四章的动手实现，约 1000 行 C 代码，帮助理解 [[concepts/ptp-ieee1588|PTP]] 协议的核心机制，可以在两台 Linux 机器上实际运行。

## 快速开始

```bash
git clone https://github.com/Lularible/ptp-book.git
cd ptp-book/ptp_lite
make

# 主时钟（终端 A）
sudo ./ptp_master eth0

# 从时钟（终端 B，同一局域网）
sudo ./ptp_slave eth0
```

## 报文结构与编码

PTP 报文使用网络字节序（大端）。报文头 34 字节，关键字段用位域定义：

```c
struct ptp_header {
    uint8_t  message_type;      // 低4位：报文类型
    uint8_t  version_ptp;       // PTP 版本，应为 2
    uint16_t message_length;    // 含头部的总长度（网络字节序）
    uint8_t  domain_number;     // PTP 域（通常 0）
    uint8_t  reserved1;
    uint16_t flags;             // twoStep=0x0200 等标志位
    int64_t  correction_field;  // 透明时钟累积补偿（Q6.58 定点数）
    uint32_t reserved2;
    uint8_t  source_port_id[10]; // clockIdentity(8) + portNumber(2)
    uint16_t sequence_id;
    uint8_t  control;           // 兼容 PTPv1
    int8_t   log_message_interval;
} __attribute__((packed));
```

时间戳格式：

```c
struct ptp_timestamp {
    uint16_t seconds_msb;   // 高 16 位秒
    uint32_t seconds_lsb;   // 低 32 位秒
    uint32_t nanoseconds;   // 纳秒部分（0-999,999,999）
} __attribute__((packed));
```

## 主时钟实现核心流程

```
初始化：创建 L2 raw socket，绑定到目标网卡
循环（每秒）：
  1. 构造 Sync 报文，记录发送时间戳 t1
  2. 发送 Sync（目标 MAC: 01:1B:19:00:00:00）
  3. 构造 Follow_Up，携带精确 t1
  4. 发送 Follow_Up
  5. 每 8 秒发送一次 Announce（携带 clockClass/clockAccuracy 等）
  6. 监听 Delay_Req，收到后记录 t4，回复 Delay_Resp（携带 t4）
```

## 从时钟实现核心流程

```
初始化：创建 L2 raw socket，绑定到网卡
监听循环：
  1. 收到 Sync → 记录接收时间戳 t2
  2. 收到 Follow_Up → 得到精确 t1
  3. 发送 Delay_Req，记录发送时间戳 t3
  4. 收到 Delay_Resp → 得到 t4
  5. 计算并应用时钟调整：
     delay  = ((t2 - t1) + (t4 - t3)) / 2
     offset = (t2 - t1) - delay
     调用 clock_adjtime / adjtimex 调整系统时钟
```

## 时钟调整

Linux 提供两种时钟调整接口：

| 接口 | 用途 |
|------|------|
| `clock_settime(CLOCK_REALTIME)` | 直接跳变时钟（跳变量大时使用）|
| `adjtimex()` / `clock_adjtime()` | 平滑调频（offset 小时使用，避免时间跳变）|

ptp-lite 的简化实现直接用 `clock_settime` 设置时间，生产级实现（如 [[entities/linuxptp]]）使用 PI 伺服控制器配合 `adjtimex` 实现平滑调整。

## 与 LinuxPTP 的对比

| 特性 | ptp-lite | LinuxPTP ptp4l |
|------|---------|----------------|
| 代码量 | ~1000 行 | ~15000 行 |
| 伺服控制器 | 无（直接 settime）| PI 控制器 |
| 状态机 | 简化（仅 Master/Slave）| 完整 9 状态 |
| BMCA | 无 | 完整实现 |
| 传输层 | L2 多播 | L2/UDP/单播 |
| 用途 | 学习理解 | 生产部署 |

## 常见问题排查

```bash
# 检查网卡是否支持硬件时间戳（ptp-lite 使用软件时间戳）
ethtool -T eth0

# 确认网卡已启用混杂模式或加入 PTP 多播组
ip link show eth0

# 检查防火墙是否阻断 L2 多播
# PTP 使用以太帧，不走 IP 层，iptables 不生效，需检查 ebtables

# 查看同步效果（offset 应逐渐收敛到 0）
# ptp-lite 输出格式示例：
# [+000.100] offset: +1234 ns, delay: 5678 ns
```
