---
title: PTP 报文类型
category: concepts
tags: [ptp, ieee-1588, network-protocol, message-format]
sources: ["https://github.com/Lularible/ptp-book"]
created: 2026-07-03T09:00:00Z
updated: 2026-07-03T09:00:00Z
summary: "PTP 定义 10 种报文，分事件报文（需硬件时间戳）和通用报文，共同完成时间同步、延迟测量和网络管理"
base_confidence: 0.88
lifecycle: draft
lifecycle_changed: "2026-07-03"
tier: supporting
provenance:
  extracted: 0.88
  inferred: 0.10
  ambiguous: 0.02
relationships:
  - target: "[[concepts/ptp-ieee1588]]"
    type: related_to
  - target: "[[concepts/ptp-delay-measurement]]"
    type: related_to
  - target: "[[concepts/ptp-tlv-extension]]"
    type: related_to
---

# PTP 报文类型

[[concepts/ptp-ieee1588|PTP]] 定义了 10 种报文，分为两类：**事件报文**（Event Messages）和**通用报文**（General Messages）。

## 两类报文的本质区别

- **事件报文**：在发送和接收时需要**硬件时间戳**，精度直接影响同步精度
- **通用报文**：携带信息，不需要精确时间戳，软件处理即可

## 事件报文（4种）

| 报文 | 方向 | 用途 |
|------|------|------|
| `Sync` | 主→从 | 携带主时钟的 originTimestamp，触发从时钟记录接收时间戳 t2 |
| `Delay_Req` | 从→主（E2E） | 从时钟发起，用于测量从→主方向的延迟 |
| `Pdelay_Req` | 任意→邻居（P2P） | 点对点延迟测量，发起方记录发送时间戳 t1 |
| `Pdelay_Resp` | 邻居→发起方（P2P） | 携带接收时间戳 t2，响应方记录发送时间戳 t3 |

## 通用报文（6种）

| 报文 | 方向 | 用途 |
|------|------|------|
| `Follow_Up` | 主→从 | 两步模式下，携带 Sync 的精确发送时间戳 t1 |
| `Delay_Resp` | 主→从（E2E） | 携带主时钟收到 Delay_Req 的时间戳 t4 |
| `Pdelay_Resp_Follow_Up` | 邻居→发起方（P2P） | 两步模式下，携带 Pdelay_Resp 的精确发送时间戳 t3 |
| `Announce` | 主→所有 | 广播时钟质量属性（clockClass/clockAccuracy 等），供 [[concepts/ptp-bmca|BMCA]] 使用 |
| `Management` | 管理→设备（双向）| 查询/设置 PTP 设备的数据集，携带[[concepts/ptp-tlv-extension|TLV]] |
| `Signaling` | 任意 | 协商单播传输参数，携带 TLV |

## 报文头公共字段

所有 PTP 报文共享 34 字节的报文头：

```
transportSpecific(4b) + messageType(4b)   // 各 4 位
reserved(4b) + versionPTP(4b)
messageLength(16b)                         // 含头部的总长度
domainNumber(8b)                           // PTP 域编号（隔离不同域）
reserved(8b)
flagField(16b)                             // 标志位（twoStep、unicast 等）
correctionField(64b)                       // 透明时钟累积延迟补偿
reserved(32b)
sourcePortIdentity(80b)                    // 发送方 clockIdentity(64b) + portNumber(16b)
sequenceId(16b)                            // 报文序号，匹配请求/响应
controlField(8b)                           // 兼容 PTPv1（已弃用）
logMessageInterval(8b)                     // 报文发送间隔（log₂ 秒）
```

## 传输方式

PTP 支持多种传输层：

| 传输方式 | 特点 |
|---------|------|
| UDP/IPv4（L3）| 最常见，目标 IP 224.0.1.129（多播）或单播 |
| UDP/IPv6（L3）| IPv6 网络 |
| IEEE 802.3（L2）| 直接以太帧，目标 MAC 01:1B:19:00:00:00，延迟最低 |

[[entities/linuxptp]] 默认使用 L2 多播（精度最高），也支持 L3 UDP。
