---
title: PTP（精确时间协议，IEEE 1588）
category: concepts
tags: [ptp, ieee-1588, network-protocol, time-sync]
sources: ["https://github.com/Lularible/ptp-book"]
created: 2026-07-03T09:00:00Z
updated: 2026-07-03T09:00:00Z
summary: "IEEE 1588 精确时间协议，通过四时间戳测量网络延迟，实现纳秒级分布式时钟同步"
base_confidence: 0.9
lifecycle: draft
lifecycle_changed: "2026-07-03"
tier: core
provenance:
  extracted: 0.90
  inferred: 0.08
  ambiguous: 0.02
relationships:
  - target: "[[concepts/ptp-bmca]]"
    type: related_to
  - target: "[[concepts/ptp-delay-measurement]]"
    type: related_to
  - target: "[[entities/linuxptp]]"
    type: related_to
  - target: "[[references/ptp-book-overview]]"
    type: derived_from
  - target: "[[synthesis/ptp-ieee1588 × linuxptp]]"
    type: synthesized_in
---

# PTP（精确时间协议，IEEE 1588）

PTP（Precision Time Protocol）是 IEEE 1588 定义的网络时间同步协议，目标是在局域网内实现**纳秒级**的分布式时钟同步。

## 核心问题

分布式系统中每个节点都有独立晶振，晶振存在：

- **初始偏差**：出厂就不完全一致
- **频率漂移**：温度、电压变化导致走时速度不同
- **累积误差**：长时间运行后差异越来越大

NTP 可以实现毫秒级同步，不够用于 5G 基站（需要 ±1.5μs）、工业自动化（需要 ±1μs）、金融交易（需要纳秒级时间戳）。

## 协议版本

| 版本 | 标准 | 关键变化 |
|------|------|---------|
| PTPv1 | IEEE 1588-2002 | 首个版本 |
| PTPv2 | IEEE 1588-2008 | 重大重写，增加透明时钟、单播等 |
| PTPv2.1 | IEEE 1588-2019 | 增加安全机制、高精度选项，通过 [[concepts/ptp-tlv-extension\|TLV]] 扩展 |

## 基本原理：四时间戳法

PTP 用四个时间戳消除**单程网络延迟**的影响：

```
主时钟                          从时钟
  │ t1: 发送 Sync               │
  │ ──────────────────────────► │ t2: 收到 Sync
  │                             │
  │          t3: 发送 Delay_Req │
  │ ◄────────────────────────── │
  │ t4: 收到 Delay_Req          │
```

**计算**：

```
单程延迟 delay = [(t2 - t1) + (t4 - t3)] / 2
从时钟偏移 offset = (t2 - t1) - delay
                  = [(t2 - t1) - (t4 - t3)] / 2
```

假设链路是对称的（去程延迟 = 回程延迟）。详见 [[concepts/ptp-delay-measurement]]。

## 网络角色

详见 [[concepts/ptp-clock-types]]：

- **Grandmaster (GM)**：最顶层时钟，连接 GPS 或原子钟
- **边界时钟 (BC)**：同时有主端口和从端口，转发并重新生成时间
- **透明时钟 (TC)**：修正报文在设备内的驻留时间
- **普通时钟 (OC)**：终端设备，只有一个 PTP 端口

## 主时钟选举

[[concepts/ptp-bmca|BMCA]]（Best Master Clock Algorithm）是 PTP 的分布式选举机制，比较：

1. `priority1`（人工权重，0-255，越小越优先）
2. `clockClass`（时钟等级，6=直连 GPS/原子钟，255=仅从时钟）
3. `clockAccuracy`（精度枚举，0x20=≤25ns 电信级）
4. `offsetScaledLogVariance`（Allan 方差，稳定性）
5. `priority2`（第二人工权重）
6. `clockIdentity`（MAC 地址衍生，决胜）

## 报文类型

[[concepts/ptp-message-types]] 中定义 10 种报文，分两类：

- **事件报文**（需硬件时间戳）：Sync、Delay_Req、Pdelay_Req、Pdelay_Resp
- **通用报文**（不需时间戳）：Follow_Up、Delay_Resp、Announce、Management、Signaling、Pdelay_Resp_Follow_Up

## 典型应用场景

| 场景 | 精度需求 | PTP Profile |
|------|---------|-------------|
| 5G 基站 | ±1.5μs（相位） | ITU-T G.8275.1 |
| 电力系统 | ±1μs | IEC 61850 / C37.238 |
| 工业自动化 | ±1μs | IEC 61158（PROFINET） |
| 金融交易 | 100ns 时间戳 | FINRA CAT |
| 科学实验 | 亚纳秒 | [[entities/white-rabbit\|White Rabbit]] |

## 与 NTP 的对比

| 特性 | NTP | PTP |
|------|-----|-----|
| 精度 | 1-100ms（互联网），<1ms（局域网）| 纳秒级 |
| 硬件支持 | 不需要 | 需要硬件时间戳支持 |
| 网络范围 | 全球互联网 | 局域网 |
| 复杂度 | 低 | 高 |
| 典型用途 | 服务器时间同步 | 工业/电信/科学 |
