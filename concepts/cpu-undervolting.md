---
title: CPU 降压（Undervolting）
category: concept
tags: [undervolting, fivr, msr, intel, throttlestop, 降压, 散热]
summary: 通过降低 CPU 工作电压（Vcore）在保持频率的同时降低功耗与发热。原理 P=C×V²×f。Intel CPU 通过 FIVR/Offset Voltage 实现，AMD 通过 PBO Curve Optimizer。
sources:
  - https://ultrabookreview.com/31385-the-throttlestop-guide
  - https://www.dell.com/support/article/en-us/sln308057
created: 2026-08-23
updated: 2026-08-23
base_confidence: 0.85
lifecycle: draft
lifecycle_changed: 2026-08-23
provenance:
  extracted: 0.75
  inferred: 0.15
  ambiguous: 0.10
---

# CPU 降压（Undervolting）

## 物理动机

CPU 动态功耗近似满足：$P = C \times V^2 \times f$，其中 C 是开关电容、V 是电压、f 是频率。

把 Vcore 从 1.2V 降到 1.1V（约 −100mV），理论功耗下降到 $(1.1/1.2)^2 \approx 84\%$，即约 16% 节省，对应温度也相应下降。这是笔记本降压的物理基础。^[extracted]

## Intel 实现路径

Intel 把 CPU 电压调节集成进芯片，叫 **FIVR（Fully Integrated Voltage Regulator）**。开发者通过特定 MSR（Model Specific Register）写入 offset：

- **MSR 0x150 (Voltage / Current Misc)**：写入 negative offset 即降压
- **Offset 模式**：
  - **Adaptive**：根据 SKU 的 V/F 曲线表动态减电压（推荐笔记本用）
  - **Override**：强制写死电压（一般用于极端 debug，笔记本慎用）

## AMD 实现路径

AMD 不开放同一套 MSR。降压走：

- **Ryzen Controller** / **Curve Optimizer**：在 PBO（Precision Boost Overdrive）里给每核一个 negative value（magnitude），通过 V/F 曲线整体下移
- Ryzen 不支持 FIVR Offset 概念，但目标效果一样

## 支持世代与封锁

- **Skylake（6 代）~ Comet Lake（10 代）**：完整 FIVR offset 支持，老平台最稳
- **Alder Lake（12 代）开始的 K/KF**：Intel 收回了 offset，多数电压写入 MSR 0x150 时返回值被忽略^[ambiguous] — 多个社区来源称 H/KF SKU 锁死
- **12 代非-K H/HX**：部分 OEM 通过 BIOS setup 变量控制；Alienware HX 平台可以经 Smokeless UMAF 改写该 setup 变量恢复降压能力^[extracted]
- **AMD Ryzen 全系**：FIVR offset 不适用，走 Curve Optimizer 路径

## 风险与稳定化方法

降压过度会出现：

- 蓝屏 / 死机 — 抬升 5 mV
- WHEA Logger 事件 ID 19 — 抬升 10-15 mV
- 黑屏唤醒 / 低负载崩溃 — 抬升 mV Boost（mV Boost @ 800 MHz 机制）

## 与 Overclocking 的区别

降压反向于超频：

| 操作 | 电压 | 频率 | 功耗 | 性能 |
|---|---|---|---|---|
| 降压（undervolt） | ↓ | 不变（多数负载） | ↓ | 不降反升（因为不 thermal throttle） |
| 超频（overclock） | ↑ 或不变 | ↑ | ↑ | ↑（前提散热够） |
| 降频（underclock） | ↓ | ↓ | ↓ | ↓ |

降压的优秀副产品：**CPU 不撞 thermal throttle 时甚至性能略升**，因为持续 turbo 时间更长。

## 工具栈

- **Intel**：ThrottleStop（首选，绕过 XTU 限制）、Intel XTU（Intel 官方但功能受限）
- **AMD**：Ryzen Controller、AMD Ryzen Master
- **OEM 自有**：Alienware Command Center TCC Offset（与降压正交，温度天花板）
- **监控**：HWInfo64（看 CPU Package Temp / Power / Clock）、HWiNFO

## 相关 wiki 页面

- [[throttlestop-alienware-thermals]] — 实践层：Alienware + ThrottleStop 完整流程
- [[throttlestop-fivr-undervolting]] — 工具层：ThrottleStop 怎么实现 offset 写入
- [[alienware-bios-undervolt-unlock]] — Alienware HX 的 BIOS setup 变量解锁
- [[throttlestop]]
- [[research-throttlestop-alienware-thermals]]
