---
title: PTP 延迟测量 — E2E 与 P2P 四时间戳法
category: concepts
tags: [ptp, ieee-1588, algorithm, network-protocol]
sources: ["https://github.com/Lularible/ptp-book"]
created: 2026-07-03T09:00:00Z
updated: 2026-08-03T05:47:33Z
summary: "PTP 用四个时间戳消除单程网络延迟：E2E 测量端到端路径，P2P 逐链路测量并由透明时钟补偿"
base_confidence: 0.92
lifecycle: reviewed
lifecycle_changed: 2026-08-03
lifecycle_reason: "auto-promoted by wiki-lint --consolidate: age>30d, confidence>0.7"
tier: core
provenance:
  extracted: 0.92
  inferred: 0.06
  ambiguous: 0.02
relationships:
  - target: "[[concepts/ptp-ieee1588]]"
    type: related_to
  - target: "[[concepts/ptp-clock-types]]"
    type: related_to
  - target: "[[concepts/ptp-message-types]]"
    type: uses
  - target: "[[concepts/ptp-tlv-extension]]"
    type: related_to
  - target: "[[synthesis/ptp-ieee1588 × linuxptp]]"
    type: related_to
  - target: "[[references/ptp-book-overview]]"
    type: derived_from
---

# PTP 延迟测量 — E2E 与 P2P 四时间戳法

[[concepts/ptp-ieee1588|PTP]] 必须精确知道**单程网络延迟**，才能从"传输时差"中分离出"时钟偏移"。

## 核心数学

```
主时钟                          从时钟
  │ t1: 发送 Sync               │
  │ ──────────────────────────► │ t2: 收到 Sync
  │                             │
  │ t3: 收到 Delay_Req          │ (t3内部): 发送 Delay_Req
  │ ◄────────────────────────── │
  │                             │ t4: 收到 Delay_Resp
  │ ──Delay_Resp(t3)──────────► │
```

设主→从单程延迟为 `d₁`，从→主单程延迟为 `d₂`：

```
t2 - t1 = offset + d₁
t4 - t3 = -offset + d₂

联立（假设链路对称，d₁ = d₂ = delay）：
delay  = [(t2 - t1) + (t4 - t3)] / 2
offset = (t2 - t1) - delay
       = [(t2 - t1) - (t4 - t3)] / 2
```

**对称性假设**是 PTP 精度的关键限制。非对称链路（光纤上下行不同、不同方向走不同路由）会引入系统性误差。

## E2E 延迟测量机制

### 流程

```
主时钟                          从时钟
  │ Sync（t1）                   │
  │ ──────────────────────────► │ t2 记录
  │ Follow_Up（携带 t1 精确值）  │
  │ ──────────────────────────► │ 得到精确 t1
  │                             │ 发送 Delay_Req（t3）
  │ ◄────────────────────────── │
  │ 记录 t4                     │
  │ Delay_Resp（携带 t4）        │
  │ ──────────────────────────► │ 得到 t4
  │                             │ 计算 offset 和 delay
```

### Follow_Up 报文的意义

硬件时间戳在报文发出后才能读取，无法提前写入 Sync 报文。因此：

- **单步模式（One-step）**：硬件在报文传输时实时修改 [[concepts/ptp-message-types|Sync]] 的 `originTimestamp` 字段，无需 Follow_Up
- **两步模式（Two-step）**：先发 Sync（时间戳为 0），硬件记录精确发出时间，随后软件发送 Follow_Up 携带该时间

两步模式对硬件要求低，更常见。

### E2E 的局限

中间经过的普通交换机（非 TC）会引入不确定的排队延迟，导致测量的 delay 包含交换机延迟，误差增大。

## P2P 延迟测量机制（Pdelay）

### 核心思想

不测量端到端路径，而是**逐段链路独立测量**，每个 TC 设备负责测量相邻链路的延迟并补偿。

### 流程（每对相邻节点之间）

```
节点 A                         节点 B
  │ Pdelay_Req（t1）            │
  │ ─────────────────────────► │ t2 记录
  │                             │ Pdelay_Resp（t3, 携带 t2）
  │ ◄───────────────────────── │
  │ t4 记录                    │
  │ Pdelay_Resp_Follow_Up（携带 t3）
  │ ◄───────────────────────── │
  │ 计算链路延迟                 │

链路延迟 = [(t4 - t1) - (t3 - t2)] / 2
```

### TC 补偿机制

每个 P2P TC 设备：

1. 持续测量与上游端口的链路延迟（`peerDelay`）
2. 当转发 Sync 报文时，将 `peerDelay + 驻留时间` 累加到 `correctionField`

```
correctionField（最终）= 
    链路1延迟 + TC₁驻留时间 
  + 链路2延迟 + TC₂驻留时间 
  + ...
```

从时钟收到 Sync 时，`correctionField` 已包含了全路径的网络延迟，直接得到偏移量。

### E2E vs P2P 对比

| 特性 | E2E | P2P |
|------|-----|-----|
| 测量范围 | 从主时钟到从时钟的全路径 | 逐链路独立测量 |
| 依赖 TC | E2E TC（可选） | P2P TC（必须） |
| 精度 | 受中间设备排队延迟影响大 | 逐链路补偿，精度更高 |
| 网络报文量 | 较少 | 每对相邻节点都要交换 Pdelay 报文 |
| 典型应用 | 简单网络、电信场景 | 高精度工业网络、PROFINET |

## 硬件时间戳的必要性

软件时间戳（在操作系统层获取）受 CPU 调度、中断延迟影响，误差 100μs~1ms。

硬件时间戳在网卡物理层或 MAC 层打戳，精度达纳秒级。

Linux 通过 `SO_TIMESTAMPING` socket 选项启用硬件时间戳，详见 [[entities/linuxptp]]。

## 相关

- [[synthesis/ptp-ieee1588 × linuxptp]] — PTP 协议文本规定的是协议行为的最少集合，LinuxPTP 揭示了协议必须解决的工程空白：PI 伺服、PHC 桥接、硬件时间戳三级精度分层。
- [[references/ptp-book-overview]] — Lularible 的开源 PTP 技术书，41节从时间本质到 LinuxPTP 源码再到手写 ptp-lite 实现
