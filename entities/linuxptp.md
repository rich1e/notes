---
title: LinuxPTP
category: entities
tags: [ptp, linux, open-source, tool]
sources: ["https://github.com/Lularible/ptp-book"]
created: 2026-07-03T09:00:00Z
updated: 2026-07-03T09:00:00Z
summary: "Linux 平台的工业级 PTP 实现，包含 ptp4l（协议）、phc2sys（时钟同步）和 pmc（管理）工具"
base_confidence: 0.88
lifecycle: draft
lifecycle_changed: "2026-07-03"
tier: core
provenance:
  extracted: 0.88
  inferred: 0.10
  ambiguous: 0.02
relationships:
  - target: "[[concepts/ptp-ieee1588]]"
    type: implements
  - target: "[[concepts/ptp-bmca]]"
    type: implements
  - target: "[[skills/ptp-implementation]]"
    type: related_to
  - target: "[[synthesis/ptp-ieee1588 × linuxptp]]"
    type: related_to
---

# LinuxPTP

LinuxPTP 是 Linux 平台上最成熟的开源 [[concepts/ptp-ieee1588|PTP]] 实现，Richard Cochran 主导开发，广泛用于 5G 基站、电信设备、工业自动化。

## 核心组件

### ptp4l — PTP 协议引擎

运行完整的 PTP 协议栈，包括 [[concepts/ptp-bmca|BMCA]] 选举、[[concepts/ptp-port-state-machine|端口状态机]]、[[concepts/ptp-delay-measurement|延迟测量]]。

```bash
# 以硬件时间戳模式运行，L2 多播，E2E 机制
ptp4l -i eth0 -m

# 从时钟模式（slaveOnly）
ptp4l -i eth0 -m -s

# 使用配置文件
ptp4l -f /etc/ptp4l.conf
```

### phc2sys — PHC 与系统时钟同步

将 PTP Hardware Clock（PHC，网卡硬件时钟）同步到系统时钟（CLOCK_REALTIME），或反向。

```bash
# 将系统时钟同步到 PHC（ptp4l 已将 PHC 同步到 PTP 网络后）
phc2sys -s /dev/ptp0 -c CLOCK_REALTIME -w

# 也可以直接读取 ptp4l 的 UNIX domain socket
phc2sys -a -r
```

### pmc — 管理命令行工具

通过 PTP 管理协议查询和设置 ptp4l 的运行状态，对应书中 2.14 章的管理协议。

```bash
# 查询当前数据集
pmc -u -b 0 'GET CURRENT_DATA_SET'
pmc -u -b 0 'GET PARENT_DATA_SET'
pmc -u -b 0 'GET TIME_PROPERTIES_DATA_SET'

# 查询端口状态
pmc -u -b 0 'GET PORT_DATA_SET'

# 设置 UTC 偏移
pmc -u -b 0 'SET GRANDMASTER_SETTINGS_NP utcOffset 37'
```

## 关键源码模块

| 文件 | 功能 |
|------|------|
| `bmc.c` | BMCA 算法实现（约 150 行，六属性比较） |
| `port.c` | 端口状态机（约 2000 行，驾驭 9 种状态） |
| `servo.c` | PI 伺服控制器（让时钟频率追上主时钟） |
| `clock.c` | 数据集管理和核心协调 |
| `phc.c` | PHC 操作（通过 PHC_SETTIME/ADJTIME ioctl）|
| `transport.c` | 传输层抽象（UDP/L2 多播/单播）|
| `tlv.c` | TLV 处理（扩展信息解析/序列化）|
| `raw.c` | L2 原始以太帧传输 |

## PI 伺服控制器

PTP 同步不仅是相位对齐，还需要频率同步——否则时钟会不断漂移回来。

LinuxPTP 使用 PI（比例-积分）控制器：

```
offset_error = slave_time - master_time
freq_adj = Kp × offset_error + Ki × ∫offset_error dt

# 调用 adjtimex(2) 调整本地时钟频率
```

默认参数：Kp=0.7, Ki=0.3（可在配置文件中调整）。

## 硬件时间戳支持

通过 `SO_TIMESTAMPING` socket 选项启用，支持三种级别：

| 级别 | 精度 | 说明 |
|------|------|------|
| 软件时间戳 | 100μs~1ms | 操作系统层，不建议用于 PTP |
| 驱动时间戳 | 10μs | 驱动程序层 |
| 硬件时间戳 | <10ns | 网卡 MAC 层，PTP 推荐使用 |

检查网卡是否支持硬件时间戳：

```bash
ethtool -T eth0
# 查找 hardware-transmit hardware-receive hardware-raw-clock
```

## 典型配置示例

```ini
# /etc/ptp4l.conf（从时钟配置）
[global]
slaveOnly 1
logMinDelayReqInterval -4    # 每秒 16 次 Delay_Req
logSyncInterval -4           # 每秒 16 次 Sync
clockServoPKP 0.7            # 伺服控制器 Kp
clockServoI   0.3            # 伺服控制器 Ki
tx_timestamp_timeout 10
time_stamping hardware

[eth0]
```
