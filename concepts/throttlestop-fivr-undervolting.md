---

title: ThrottleStop 与 FIVR 降压原理
category: concept
tags: [throttlestop, fivr, msr-0x150, undervolt, intel, 降压]
relationships:
  - target: "[[references/ultrabookreview-throttlestop-guide-2026]]"
    type: related_to
  - target: "[[references/techpowerup-m16-r1-undervolt-thread]]"
    type: related_to

summary: ThrottleStop 通过 MSR 0x150 写入负向 Offset Voltage 到 Intel FIVR 的 CPU Core/Cache 通道，从而实现 CPU 降压。配合 Speed Shift EPP、BD PROCHOT 等开关控制 throttling 行为。
sources:
  - https://ultrabookreview.com/31385-the-throttlestop-guide
  - https://maketecheasier.com/reduce-cpu-temperature-undervolting/
created: 2026-08-23
updated: 2026-08-23T08:45:00Z
base_confidence: 0.9
lifecycle: draft
lifecycle_changed: 2026-08-23
provenance:
  extracted: 0.85
  inferred: 0.10
  ambiguous: 0.05

---
# ThrottleStop 与 FIVR 降压原理

## 工具身份

- **ThrottleStop** — 由 Kevin "UncleWebb" Glynn 开发的 Windows CPU 调参工具
- 主战场：笔记本 Intel CPU 的降压 / 限频 / 拒热（repel thermal throttling）
- 下载渠道：TechPowerUp（官方镜像），NotebookReview forum 维护

## FIVR 是什么

**FIVR（Fully Integrated Voltage Regulator）**：Intel 自 Haswell 起把大部分 VRM 集成进 CPU 自己的 die。FIVR 内部有 4 个独立电压轨道，ThrottleStop 可独立调节：

| 轨道 | 控制范围 | 建议 |
|---|---|---|
| **CPU Core** | 核心电压 | 主战场，offset 改这里 |
| **CPU Cache** | 末级缓存电压 | **必须与 Core 同值**（很多崩溃是 Cache 不一致导致） |
| **iGPU (Intel GPU)** | 核显电压 | 默认 0，老手可降 |
| **System Agent** | 内存控制器 / PCIe | 默认 0 |

## MSR 0x150 写入流程

1. 用户在 FIVR 窗口填 Offset（-100 mV 等）
2. ThrottleStop 拼成 MSR 0x150 的合法位结构
3. 调用 `wrmsr` 把 MSR 写到目标 CPU 核
4. **若 VBS（Memory Integrity）开启**：写入被静默丢弃，电压表显示 0.000V
5. **若 BIOS 锁住 UnderVolt Protection**：写入返回 RO 值，FIVR "Locked" 标记

## mV Boost @ 800 MHz 机制

Intel V/F 曲线按频率给出电压。offset 是减法，对全频率段统一加 -100 mV：

- **高频（turbo 4-5 GHz）**：电压仍有 1.0-1.2V，扣 100 mV 后仍稳定
- **低频（800 MHz-2 GHz）**：原电压 0.7-0.9V，扣 100 mV 后可能跌到 0.6V 触发电气不稳定

`mV Boost @ 800 MHz = +100 mV` 表示**在 800 MHz 频率点上加 100 mV 补偿**，把对应那段曲线拉回安全区。开启后整条 V/F 曲线只在高频段有完整 -100 mV 收益，低频不受影响。^[extracted][inferred]

这是 m16 R1 社区验证的"安全 -100 mV 模板"的关键。

## 其他关键 FIVR 选项

- **Unlock Adjustable Voltage**：必须勾选，否则为只读
- **CPU Cache 与 Core 同步**：单独降 Cache 而不同步 Core 几乎必崩
- **Apply** → "Save voltages immediately"：固化到 TS 持久层，关掉软件再开仍生效

## ThrottleStop 主窗口速查

| 选项 | 用途 |
|---|---|
| Turn On | 启用 TS 监控和调参 |
| FIVR | 打开电压编辑 |
| TPL (Turbo Power Limits) | PL1/PL2/PL4 限制（轻松降功率） |
| Speed Shift | EPP 调频响应（0=激进，128=保守） |
| BD PROCHOT | 关掉 dGPU→CPU 的双向热信号（谨慎） |
| C States | 控制睡眠 C-state 时钟 |
| Benchmark | TS 内置压力测试 |

## 与 AWCC TCC Offset 的协同

AWCC 的 **TCC Offset**（0-15）：

- 把 CPU 温度硬上限从 100°C 拉到 95°C（TCC=5）或 85°C（TCC=15）
- 是降压之前的零成本第一步
- **与降压正交**：TCC 是硬上限，降压是平均值；两者叠加温度更稳

## 相关 wiki 页面

- [[throttlestop-alienware-thermals]]
- [[cpu-undervolting]]
- [[alienware-bios-undervolt-unlock]]
- [[throttlestop-options]]
- [[throttlestop]]
- [[kevin-glynn]]
- [[research-throttlestop-alienware-thermals]]

## Related

- [[references/ultrabookreview-throttlestop-guide-2026|ThrottleStop Guide (UltrabookReview, 2026)]] — shares #intel/#throttlestop/#undervolt (references)
- [[references/techpowerup-m16-r1-undervolt-thread|How to unlock Alienware m16 R1 undervolt for ThrottleStop (TechPowerUp Forum)]] — shares #throttlestop/#undervolt (references)

