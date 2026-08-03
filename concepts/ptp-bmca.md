---
title: PTP BMCA — 最佳主时钟选举算法
category: concepts
tags: [ptp, ieee-1588, distributed-systems, algorithm]
sources: ["https://github.com/Lularible/ptp-book"]
created: 2026-07-03T09:00:00Z
updated: 2026-08-03T05:47:33Z
summary: "BMCA 是 PTP 的分布式主时钟选举算法，通过比较 clockClass/Accuracy/priority 决定谁当 Grandmaster"
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
  - target: "[[concepts/ptp-port-state-machine]]"
    type: related_to
  - target: "[[entities/linuxptp]]"
    type: related_to
  - target: "[[concepts/ptp-message-types]]"
    type: related_to
  - target: "[[synthesis/ptp-ieee1588 × linuxptp]]"
    type: related_to
  - target: "[[references/ptp-book-overview]]"
    type: derived_from
---

# PTP BMCA — 最佳主时钟选举算法

BMCA（Best Master Clock Algorithm）是 [[concepts/ptp-ieee1588|PTP]] 协议中用于自动选举 Grandmaster 的分布式算法。每个设备独立运行，不需要中央控制器，相同输入必然产生相同输出（确定性）。

## 选举流程

所有设备定期广播 **[[concepts/ptp-message-types|Announce 报文]]**，携带自己的"时钟简历"。每个设备收集所有 Announce 报文后，独立运行 BMCA，得出相同的结论：谁是最好的时钟。

```
设备 A 发送 Announce（priority1=10, clockClass=6）
设备 B 发送 Announce（priority1=128, clockClass=248）
设备 C 发送 Announce（priority1=128, clockClass=248）

每台设备独立比较：A 最优 → A 成为 Grandmaster
```

## 比较属性（优先级由高到低）

### 1. priority1（第一优先级）

- 类型：UInteger8（0-255），**越小越优先**
- 管理员手动设置，用于强制指定主时钟

**推荐配置**：

| 角色 | 建议值 |
|------|--------|
| 核心主时钟（高精度 GPS+铷钟） | 10-50 |
| 一级备份 | 51-100 |
| 二级备份 | 101-150 |
| 普通设备（默认） | 128 |
| 仅从时钟 | 200-255 |

### 2. clockClass（时钟等级）

越小越优先，标识时钟的精度和状态：

| 值 | 含义 |
|----|------|
| **6** | 直连 GPS/原子钟，PTP 时间尺度，永不成为从时钟 |
| **7** | 原 class 6，失去 GPS 但原子钟保持，仍高精度 |
| **13** | 应用特定时间源，ARB 时间尺度 |
| **52** | class 7 降级，保持超时，不应再当主时钟 |
| **187** | 失去同步，可以成为从时钟 |
| **248** | 默认值（大多数普通设备） |
| **255** | 仅从时钟，永远不成为主时钟 |

**关键规则**：clockClass < 128 的设备不应成为从时钟；clockClass ≥ 128 的设备可以做从时钟。

### 3. clockAccuracy（时钟精度）

越小越精确：

| 值（十六进制） | 精度 | 典型设备 |
|--------------|------|---------|
| 0x20 | ≤ 25ns | 电信级主时钟（GPS+铷钟） |
| 0x22 | ≤ 250ns | 工业级主时钟 |
| 0x23 | ≤ 1μs | 普通 GPS 时钟 |
| 0x27 | ≤ 100μs | 低端晶振 |
| 0x2C | > 10ms | 未知精度 |

### 4. offsetScaledLogVariance（稳定性）

基于 Allan 方差，越小越稳定。反映时钟频率的长期稳定性。

### 5. priority2（第二优先级）

同 priority1，用于在前四项相同时进一步区分。默认值 128。

### 6. clockIdentity（唯一标识）

通常由 MAC 地址衍生的 64 位 EUI-64 标识符。前五项完全相同时，值较小的胜出（最终决胜）。

## 故障案例：12 个主时钟的混战

某电信运营商 5G 网络，12 个核心交换机都接了 GPS，priority1 全是默认值 128，clockClass 全是 6。BMCA 到 clockIdentity 才能决胜，结果网络中每次选举结果微小差异，导致反复切换，基站时钟跳变。^[extracted]

**根因**：缺少人工 priority1 层级设计，12 台设备处于同等竞争地位。

**修复**：明确指定主用时钟 priority1=10，备用 priority1=20，其余 priority1=128。

## Announce 报文超时

如果设备在 `announceReceiptTimeout × announceInterval` 时间内收不到 Announce 报文，认为主时钟失效，重新触发 BMCA 选举新主时钟——这是 PTP 的自愈机制。

## LinuxPTP 实现

[[entities/linuxptp]] 中 BMCA 实现在 `bmc.c` 文件，核心函数约 150 行，实现了完整的六属性比较逻辑。

## 相关

- [[synthesis/ptp-ieee1588 × linuxptp]] — PTP 协议文本规定的是协议行为的最少集合，LinuxPTP 揭示了协议必须解决的工程空白：PI 伺服、PHC 桥接、硬件时间戳三级精度分层。
- [[references/ptp-book-overview]] — Lularible 的开源 PTP 技术书，41节从时间本质到 LinuxPTP 源码再到手写 ptp-lite 实现
