---
title: ThrottleStop Guide (UltrabookReview, 2026)
category: references
tags: [throttlestop, undervolt, intel, reference, ultrabookreview]
sources:
  - https://ultrabookreview.com/31385-the-throttlestop-guide
source_url: https://ultrabookreview.com/31385-the-throttlestop-guide
created: 2026-08-23
updated: 2026-08-23
summary: UltrabookReview 2026 的 ThrottleStop 长篇指南，由 David Lee（Unwinder）维护，承接 2017 Notebookcheck 原始版。覆盖 9.7 + 9.7.3 beta、FIVR、Speed Shift、BD PROCHOT 等全部选项，并按 Dell/Surface 列出 OEM 特有注意事项。
provenance:
  extracted: 0.85
  inferred: 0.10
  ambiguous: 0.05
base_confidence: 0.82
lifecycle: draft
lifecycle_changed: 2026-08-23
---

# ThrottleStop Guide (UltrabookReview, 2026)

来源：https://ultrabookreview.com/31385-the-throttlestop-guide

## 涵盖内容

- ThrottleStop 全选项详解（FIVR、TPL、Speed Shift、BD PROCHOT、C States、TS Bench）
- Step-by-step 降压流程：起点 -80 mV，5 mV 步进
- 平台支持矩阵：Skylake → Comet Lake 完美支持；Alder Lake 起 K 系列被 Intel 收回；HX 部分保留
- 稳定性测试流程：TS Bench + 系统级压力 + 睡眠唤醒
- Dell 特有：XPS 15 9550/9560 默认关 Speed Shift；BD PROCHOT 在 Dell 上常见

## 关键命题

- "ThrottleStop requires access to MSR 0x150..." — 这条报错说明 BIOS 已经把 MSR 设为 RO，多出现在 12 代 K/KF ^[extracted]
- 起始 offset -80 mV 是保守起点；常见落地 -100 ~ -150 mV
- FIVR Unlock Adjustable Voltage 必须勾选，否则写不进去

## 局限

- 主战场 Intel；AMD 用户需另寻 Ryzen Controller
- 9.7 版本在某些移动 SKU（i5-14500HX）界面灰显，作者承认 ^[ambiguous]
- 在 m16 R1 上 -100 mV 起步是 Alienware_Melting + unclewebb 在 TechPowerUp 讨论中共同探索出来的稳定值，本指南提及但未具体步骤化

## 相关 wiki 页面

- [[throttlestop-alienware-thermals]]
- [[throttlestop-fivr-undervolting]]
- [[throttlestop-options]]
- [[cpu-undervolting]]
- [[throttlestop]]
- [[kevin-glynn]]
- [[research-throttlestop-alienware-thermals]]
