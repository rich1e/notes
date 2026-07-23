---
title: PTP 端口状态机
category: concepts
tags: [ptp, ieee-1588, state-management, protocol-design]
sources: ["https://github.com/Lularible/ptp-book"]
created: 2026-07-03T09:00:00Z
updated: 2026-07-03T09:00:00Z
summary: "PTP 端口有 9 种状态，由 BMCA 结果和链路事件驱动转换，决定端口的主/从/被动/禁用角色"
base_confidence: 0.88
lifecycle: draft
lifecycle_changed: "2026-07-03"
tier: supporting
provenance:
  extracted: 0.88
  inferred: 0.10
  ambiguous: 0.02
relationships:
  - target: "[[concepts/ptp-bmca]]"
    type: related_to
  - target: "[[concepts/ptp-ieee1588]]"
    type: related_to
  - target: "[[entities/linuxptp]]"
    type: related_to
  - target: "[[synthesis/ptp-ieee1588 × linuxptp]]"
    type: related_to
  - target: "[[references/ptp-book-overview]]"
    type: derived_from
---

# PTP 端口状态机

[[concepts/ptp-ieee1588|PTP]] 每个端口都有独立的状态机，状态由 [[concepts/ptp-bmca|BMCA]] 结果和链路事件驱动转换。

## 9 种端口状态

| 状态 | 说明 |
|------|------|
| `INITIALIZING` | 初始化中，配置端口参数，不收发任何 PTP 报文 |
| `FAULTY` | 故障状态，端口出现硬件/通信错误 |
| `DISABLED` | 管理员手动禁用，不参与 PTP |
| `LISTENING` | 监听 Announce 报文，等待足够信息运行 BMCA |
| `PRE_MASTER` | 准主状态，即将成为主时钟（qualificationTimeout 过渡期）|
| `MASTER` | 主状态，发送 Sync/Follow_Up/Announce |
| `PASSIVE` | 被动状态，不发送时间，但监听（BC 上非最优端口）|
| `UNCALIBRATED` | 已选择主时钟但尚未完成同步校准 |
| `SLAVE` | 从状态，向主时钟同步，发送 Delay_Req |

## 状态转换要点

### 启动流程

```
INITIALIZING → LISTENING（端口初始化完成）
LISTENING → PRE_MASTER（BMCA 选出自己为主）
PRE_MASTER → MASTER（qualificationTimeout 超时）
LISTENING → UNCALIBRATED（BMCA 选出其他设备为主，开始同步）
UNCALIBRATED → SLAVE（收到足够 Sync 报文，完成初始校准）
```

`PRE_MASTER` 过渡期的意义：避免刚上线的设备立即成为主时钟，让网络有时间收到它的 Announce 报文并更新 BMCA 结果。

### 故障与恢复

```
任何状态 → FAULTY（检测到端口故障）
FAULTY → INITIALIZING（故障恢复后重新初始化）
```

### BC 的被动端口

边界时钟（BC）有多个端口，BMCA 会为每个端口独立决策：

- 连接上游最优主时钟的端口 → `SLAVE`
- 向下游分发时间的端口 → `MASTER`
- 连接到比自己更优时钟但不是最优路径的端口 → `PASSIVE`（避免环路）

## LinuxPTP 实现

[[entities/linuxptp]] 中，端口状态机实现在 `port.c`，核心状态转换逻辑约 200 行代码，处理了所有 9 种状态之间的合法转换路径。

每个端口的当前状态可以通过 pmc 工具查询：

```bash
pmc -u -b 0 'GET PORT_DATA_SET'
# 输出包含 portState 字段
```

## 相关

- [[synthesis/ptp-ieee1588 × linuxptp]] — PTP 协议文本规定的是协议行为的最少集合，LinuxPTP 揭示了协议必须解决的工程空白：PI 伺服、PHC 桥接、硬件时间戳三级精度分层。
- [[references/ptp-book-overview]] — Lularible 的开源 PTP 技术书，41节从时间本质到 LinuxPTP 源码再到手写 ptp-lite 实现
