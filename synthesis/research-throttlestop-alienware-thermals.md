---

title: "Research: Alienware 笔记本 ThrottleStop 降压降温"
category: synthesis
tags: [research, throttlestop, alienware, undervolt, fivr, 散热, 降压]
relationships:
  - target: "[[skills/throttlestop-alienware-thermals]]"
    type: related_to

sources:
  - https://ultrabookreview.com/31385-the-throttlestop-guide
  - https://maketecheasier.com/reduce-cpu-temperature-undervolting/
  - https://www.dell.com/support/kbdoc/en-us/000131532
  - https://www.dell.com/support/article/en-us/sln308057
  - https://notebooktalk.net/topic/2310-m16r1m18r1-smokeless-umaf-bios-options
  - https://www.techpowerup.com/forums/threads/how-to-unlock-alienware-m16-r1-undervolt-for-throttlestop.319229/
  - https://wiki.archlinux.org/index.php/User:0xMrRobot/Alienware_m16_R1
created: 2026-08-23
updated: 2026-08-23T08:45:00Z
summary: 对 Dell Alienware 笔记本 Intel H/HX 平台利用 ThrottleStop 降压降温的 3 轮研究综合。覆盖原理（FIVR / MSR 0x150 / P=C×V²×f）、Alienware BIOS 解锁路径（Smokeless UMAF / UnderVolt Protection）、mV Boost 关键技巧、安全边界、温度降幅预期（8-15°C @ 全核负载）。
provenance:
  extracted: 0.7
  inferred: 0.2
  ambiguous: 0.1
base_confidence: 0.75
lifecycle: draft
lifecycle_changed: 2026-08-23---

# Research: Alienware 笔记本 ThrottleStop 降压降温

## Overview

Dell Alienware 笔记本 Intel H/HX 平台出厂默认电压偏保守，长时负载容易撞到 100°C 触发 TCC thermal throttle。ThrottleStop 通过写入 MSR 0x150 negative Offset Voltage 到 FIVR 的 CPU Core / Cache 轨道，可以在保持频率的前提下把 CPU Package 温度压低 8-15°C。Alienware HX 平台需要先通过 Smokeless UMAF 解锁 BIOS 里隐藏的 "UnderVolt Protection" 开关，1.13.0+ BIOS 需要走 grubx64 + setup_var 替代路径。核心稳定化技巧是 `mV Boost @ 800 MHz = +100 mV`，避免 idle / 唤醒阶段的电压跌破稳定窗口。整条路径为无损可逆：CPU 体质决定落地 offset（-80 ~ -150 mV），验证用 Cinebench R23 + Prime95 + WHEA Logger 19。

## Key Findings

- **降压是温度控制而非性能控制**：频率不变但同频功耗按 P=C×V²×f 下降，撞 thermal throttle 减少后持续 turbo 反而能维持更久，等价性能不降反升 ^[extracted from [[ultrabookreview-throttlestop-guide-2026]]]
- **Alienware HX 平台默认锁了 MSR 0x150**：即使 ThrottleStop 启动，FIVR 显示 "Locked"，offset 控件灰显。需用 Smokeless_UMAF 改 UnderVolt Protection = Disabled ^[extracted from [[techpowerup-m16-r1-undervolt-thread]]]
- **`mV Boost @ 800 MHz = +100 mV` 是 m16 R1 社区验证的关键技巧**：纯 -100 mV 在 idle / 唤醒时电压跌破稳定窗口；800 MHz 点上加 100 mV 补偿，等价 V/F 曲线只对高频段生效 ^[extracted from [[techpowerup-m16-r1-undervolt-thread]] + [[ultrabookreview-throttlestop-guide-2026]]]
- **VBS / Memory Integrity 屏蔽写入**：若启用，offset 写不进去，右侧电压表显示 0.000V。是社区报告中最常见的"我设了但没生效"原因 ^[extracted from [[techpowerup-m16-r1-undervolt-thread]]]
- **不建议禁用 BD PROCHOT**：Dell 让 dGPU 过热时反向触发 CPU 降频，关掉后会丢失跨设备保护 ^[inferred from [[ultrabookreview-throttlestop-guide-2026]]]
- **推荐起点：-100 mV（Core + Cache 同步）+ mV Boost +100 mV @ 800**：i9-13980HX 好体质可推到 -150 mV；起步不必激进 ^[extracted from [[techpowerup-m16-r1-undervolt-thread]]]
- **典型温度降幅**：8-15°C @ 全核负载（m16 R1 / m15 R7 一致范围）^[extracted from [[techpowerup-m16-r1-undervolt-thread]]]
- **AWCC TCC Offset 与 ThrottleStop 降压正交**：TCC 控制硬上限（默认 100°C），降压控制平均；两者叠加温度更稳 ^[inferred from [[dell-kb-alienware-high-cpu-temp]]]

## Core Concepts

- [[cpu-undervolting]] — 降压物理动机（P=C×V²×f）和跨平台（Intel FIVR vs AMD PBO）差异
- [[throttlestop-fivr-undervolting]] — ThrottleStop 写 MSR 0x150 进入 FIVR 的详细路径
- [[alienware-bios-undervolt-unlock]] — Smokeless_UMAF 解锁 UnderVolt Protection 的流程
- [[throttlestop-options]] — FIVR / TPL / Speed Shift / BD PROCHOT 等按钮速查

## Entities & Tools

- [[throttlestop]] — 工具本体，作者 UncleWebb，主战场 Windows Intel
- [[kevin-glynn]] — ThrottleStop 作者
- [[smokeless-umaf]] — BIOS setup var 编辑器

## Contradictions & Open Questions

- **"12 代 K 系列被锁 vs Alienware HX 仍然能降压"**：未矛盾，但需要边界条件。Intel 收回对 12 代 K/KF SKU 的 FIVR offset 支持，但 HX 平台（包括非-K）的 MSR 0x150 在 BIOS 层面默认 enable prot bit，需要 OEM setup var 才能 enable ^[inferred]
- **m16 R1 1.13.0+ BIOS**：UnderVolt Protection 选项从菜单消失，社区报告 grubx64 + setup_var 可恢复，但操作文档化不完整 ^[ambiguous — 仅为社区传言，未在权威 guide 中确认]
- **稳定化温度降幅数据**：只有 m16 R1 / m15 R7 社区报告的 8-15°C 范围，无单点权威基准（如 AnandTech 风格的完整 before/after 表）^[ambiguous — 期望有权威 review 但未找到]

## Sources Consulted

- [[ultrabookreview-throttlestop-guide-2026]] — ThrottleStop 全选项教科书级指南（2026 更新）
- [[techpowerup-m16-r1-undervolt-thread]] — m16 R1 专属解锁+稳定化方案，"mV Boost @ 800" 来源
- [[dell-kb-alienware-high-cpu-temp]] — Dell 官方对 Alienware CPU 高温的立场（100°C 是 TCC 不是故障）
- [[dell-kb-alienware-high-cpu-temp]] 注：另一篇 sln308057 是 AWCC undervolt 灰色问题，**fetch 失败未验证**
- [[ultrabookreview-throttlestop-guide-2026]] — 2026 版的可选项、风险与 OEM 特性

## 进一步研究方向

- 跨 SKU 验证：M18 R1 / X17 R2 是否同样适用 mV Boost 模板
- 温度降幅的正式基准（HWiNFO + Log 数小时 CPU Package Temp 曲线对比）
- 非 Intel 路径：AMD R9 6900HX / 7040H 系列走 Ryzen Controller / Curve Optimizer 是否收益相同

## Related

- [[skills/throttlestop-alienware-thermals|Throttlestop Alienware Thermals]] — shares #alienware/#throttlestop/#undervolt (skills)

