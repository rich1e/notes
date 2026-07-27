---
title: PTP 时钟角色 — GM、BC、TC、OC
category: concepts
tags: [ptp, ieee-1588, network-protocol]
sources: ["https://github.com/Lularible/ptp-book"]
created: 2026-07-03T09:00:00Z
updated: 2026-07-03T09:00:00Z
summary: "PTP 网络中四种时钟角色：Grandmaster 提供时间源，BC 转发，TC 补偿驻留延迟，OC 是终端"
base_confidence: 0.90
lifecycle: draft
lifecycle_changed: "2026-07-03"
tier: supporting
provenance:
  extracted: 0.90
  inferred: 0.08
  ambiguous: 0.02
relationships:
  - target: "[[concepts/ptp-ieee1588]]"
    type: related_to
  - target: "[[concepts/ptp-bmca]]"
    type: related_to
  - target: "[[concepts/ptp-delay-measurement]]"
    type: related_to
  - target: "[[concepts/ptp-port-state-machine]]"
    type: related_to
  - target: "[[entities/linuxptp]]"
    type: related_to
  - target: "[[synthesis/ptp-ieee1588 × linuxptp]]"
    type: related_to
  - target: "[[references/ptp-book-overview]]"
    type: derived_from
---

# PTP 时钟角色 — GM、BC、TC、OC

[[concepts/ptp-ieee1588|PTP]] 网络中定义了四种时钟角色，每种角色在时间同步链路中承担不同职责。

## 1. Grandmaster Clock（GM，主参考时钟）

网络中时间的最终来源，连接外部高精度时间源：

- GPS 接收机（PPS 信号 + ToD）
- 铷原子钟 / 铯原子钟
- 氢脉泽（科研场景）

GM 通过 [[concepts/ptp-bmca|BMCA]] 自动选举产生，或通过 priority1=1 强制指定。

clockClass=6 表示直连 GPS/原子钟，不会降格为从时钟。

## 2. Boundary Clock（BC，边界时钟）

同时具有**一个从端口**（上游同步）和**一个或多个主端口**（下游分发）的设备。

```
上游 GM
   │ Sync（含硬件时间戳）
   ▼
BC 从端口（同步到上游）
BC 主端口（重新生成 Sync，用自己的本地时间戳）
   │
   ▼
下游从时钟
```

**关键特性**：BC 对每个端口独立运行 PTP，消除上游累积的延迟误差。大型网络中，BC 形成时间分发层级树。

**典型设备**：支持 PTP 的二层交换机、路由器。

## 3. Transparent Clock（TC，透明时钟）

不参与主从选举，只做**驻留时间补偿**。

### 问题背景

普通交换机在转发 Sync 报文时会产生**不确定的队列延迟**（数微秒到数毫秒），导致时间同步误差。

### TC 的解决方案

TC 测量 [[concepts/ptp-message-types|Sync 报文]]在自身内部的驻留时间（ingress 时间戳 → egress 时间戳），将该时间累加到报文的 `correctionField` 字段，补偿掉这段延迟。详见 [[concepts/ptp-delay-measurement]]。

```
从时钟收到 Sync 时：
实际单程延迟 = 网络传输延迟 + 各 TC 的驻留时间总和（已补偿到 correctionField）
```

### TC 的两种类型

| 类型 | 特点 |
|------|------|
| E2E TC | 配合 E2E 延迟测量机制，补偿 Sync 和 Delay_Req 的驻留时间 |
| P2P TC | 配合 P2P 延迟测量机制，在每段链路独立测量并补偿 |

**优势**：相比 BC，TC 部署更简单（不参与选举），适合网络规模大、设备层级多的场景。

## 4. Ordinary Clock（OC，普通时钟）

只有一个 PTP 端口的终端设备，只做主时钟或从时钟之一：

- **主模式（Master OC）**：提供时间，但不向上同步（通常是 GM 本身）
- **从模式（Slave OC）**：向主时钟同步，不再向下分发

**典型设备**：5G 基站、服务器网卡（需 PTP 硬件时间戳支持）、工业控制器。参见 [[entities/linuxptp]] 中如何配置 OC 从时钟。

## 时间分发链路示例

```
GPS/铷钟
   │
   ▼
GM（OC，clockClass=6）
   │ Announce/Sync/Follow_Up
   ▼
BC（汇聚层交换机）—— 隔离上下游延迟误差
   │
   ├── TC（接入层交换机）—— 补偿交换机驻留延迟
   │      │
   │      ▼
   │   Slave OC（5G 基站）
   │
   └── TC（另一台接入层交换机）
          │
          ▼
       Slave OC（服务器）
```

精度衰减：每经过一级 BC，引入约 10-100ns 误差；TC 可以将交换机引入的误差降至接近 0。

## 相关

- [[synthesis/ptp-ieee1588 × linuxptp]] — PTP 协议文本规定的是协议行为的最少集合，LinuxPTP 揭示了协议必须解决的工程空白：PI 伺服、PHC 桥接、硬件时间戳三级精度分层。
- [[references/ptp-book-overview]] — Lularible 的开源 PTP 技术书，41节从时间本质到 LinuxPTP 源码再到手写 ptp-lite 实现

## 相关页面

- [[synthesis/concepts-ptp-clock-types × entities-white-rabbit]] — synthesis
