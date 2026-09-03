---
title: White Rabbit — 亚纳秒级时间同步
category: entities
tags: [ptp, time-sync, handheld, physics, cern]
sources: ["https://github.com/Lularible/ptp-book"]
created: 2026-07-03T09:00:00Z
updated: 2026-08-03T05:47:33Z
summary: "CERN 开发的 White Rabbit 协议，在 PTP 基础上增加 DMTD 相位测量和 L1_SYNC TLV，实现亚纳秒级同步"
base_confidence: 0.85
lifecycle: reviewed
lifecycle_changed: 2026-08-03
lifecycle_reason: "auto-promoted by wiki-lint --consolidate: age>30d, confidence>0.7"
tier: peripheral
provenance:
  extracted: 0.80
  inferred: 0.18
  ambiguous: 0.02
relationships:
  - target: "[[concepts/ptp-ieee1588]]"
    type: extends
  - target: "[[concepts/ptp-tlv-extension]]"
    type: uses
  - target: "[[references/ptp-book-overview]]"
    type: related_to
  - target: "[[concepts/ptp-delay-measurement]]"
    type: extends
  - target: "[[synthesis/ptp-ieee1588 × linuxptp]]"
    type: related_to
---

# White Rabbit — 亚纳秒级时间同步

White Rabbit（WR）是 CERN（欧洲核子研究中心）开发的精密时间分发系统，基于 [[concepts/ptp-ieee1588|PTP]]（IEEE 1588）扩展，实现**亚纳秒级（<1ns）**时钟同步。

## 背景与来源

CERN 的大型强子对撞机（LHC）实验需要在整个加速器环（周长 27km）的数千个传感器之间实现皮秒级时间同步，普通 PTP 的纳秒级精度不够用。

2008 年，CERN 联合 GSI（德国重离子研究中心）、7Solutions 等机构开发了 White Rabbit，全部开源（OHWR，Open Hardware Repository）。

## White Rabbit 的精度来源

标准 PTP 的精度瓶颈：

1. **四时间戳法的量化噪声**：时间戳分辨率通常 8ns（125MHz 时钟）
2. **链路非对称性**：光纤不同方向传播时间可能差异数纳秒

WR 通过两项技术突破这些限制（见 [[concepts/ptp-delay-measurement|PTP 延迟测量]]的对称性假设局限）：

### 1. DMTD 相位测量（Digital Dual Mixer Time Difference）

WR 交换机和终端节点在硬件层面实现 DMTD 电路，直接测量两个频率接近的时钟信号之间的**相位差**，分辨率达 **10ps 量级**（比普通时间戳精度高 1000 倍）。

### 2. L1_SYNC TLV + 同步光纤

WR 使用专用光纤，通过 [[concepts/ptp-tlv-extension|L1_SYNC TLV]] 在 PTP Sync 报文中携带额外的相位校正信息，并利用 WDM（波分复用）在同一根光纤上双向传输，精确测量并消除链路非对称性。

## WR 在 IEEE 1588-2019 的影响

IEEE 1588-2019 中新增的 **High Accuracy** 选项（HA profile）就是受 WR 启发，将 WR 的部分技术标准化进入主规范，通过 TLV 扩展机制实现向后兼容。

## 应用场景

| 场景 | 精度需求 | 说明 |
|------|---------|------|
| 粒子加速器（CERN LHC）| <1ns | 最初应用场景 |
| 射电望远镜阵列（SKA）| <1ns | 基线干涉测量 |
| 引力波探测器（Virgo）| 亚纳秒 | 多站点时间关联 |
| 量子通信网络 | <100ps | 量子纠缠分发 |

## 与标准 PTP 的互操作性

WR 设备在不使用 WR 增强功能时完全兼容标准 PTP，可以与普通 PTP 设备混合组网——普通设备获得标准 PTP 精度，WR 设备之间获得亚纳秒精度。^[inferred]

## 相关

- [[synthesis/ptp-ieee1588 × linuxptp]] — PTP 协议文本规定的是协议行为的最少集合，LinuxPTP 揭示了协议必须解决的工程空白：PI 伺服、PHC 桥接、硬件时间戳三级精度分层。

## 相关页面

- [[synthesis/concepts-ptp-clock-types × entities-white-rabbit]] — synthesis
