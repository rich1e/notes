---
title: "The Last Generation of Fully Upgradeable PCs Is Being Built Right Now — XDA"
category: misc
tags:
  - pc-hardware
  - sodimm-vs-lpddr
  - right-to-repair
  - ai-pc-trend
  - misc
sources:
  - "https://www.xda-developers.com/the-last-generation-of-fully-upgradeable-pcs-is-being-built-right-now/"
source_url: "https://www.xda-developers.com/the-last-generation-of-fully-upgradeable-pcs-is-being-built-right-now/"
created: "2026-08-13T01:53:00Z"
updated: "2026-08-13T01:53:00Z"
summary: "XDA 2026 评论：soldered RAM + LPDDR 扩散到桌面是 AI 工作负载驱动，可升级 DIY PC 可能正成为最后一代。涵盖 Framework Desktop 妥协、Framework Laptop 仍半模块化、Intel Lunar Lake/Apple M-series/Qualcomm Snapdragon X 已全面板载。"
affinity: {}
promotion_status: misc
stub: false
provenance:
  extracted: 0.78
  inferred: 0.18
  ambiguous: 0.04
base_confidence: 0.45
lifecycle: draft
lifecycle_changed: "2026-08-13"
tier: peripheral
---

# The Last Generation of Fully Upgradeable PCs Is Being Built Right Now — XDA

> XDA Developers 2026 评论长文。原作者 2013 年买的 PC 跨越十年换了 3 张 GPU + 2 个 CPU + 1 块主板，"从未真正完工"，亲历者立场。核心论点：**soldered RAM 的扩散 + AI 加速器对内存带宽的硬性要求 = 桌面 PC 即将步入与笔电同一条不可升级路**。

## Overview

- **Soldered RAM + 集成芯片**：更薄、更快、更低功耗，但代价是用户再也换不了内存。
- **桌面跟着笔电走**：LPDDR + AI 需求把焊死内存推向塔式机型；Framework Desktop 是已发生的标志性案例。
- **云游戏 + 封闭设计**：把 PC 变成"家电"，DIY 升级时代的范围持续缩小。
- **个人观点**：升级性 PC 不会明天消失，但行业方向 "从未如此清晰" — **这一代很可能是最后的真正可升级 PC**。

## Key Points

### 1. 升级是 PC 的灵魂（情怀与历史）

- 作者自己的 PC：2013 入手 → 2023 换，10 年间 3 张 GPU / 2 个 CPU / 1 块主板。"从未真正完工"，像共同成长的兄弟姐妹。
- 几十年来即使是普通用户也会换 HDD→SSD、加 RAM、换 Wi-Fi 卡 — **每一次升级都在推迟整机的换新**。
- 当代趋势："day one 选什么硬件，就用什么硬件到机器退役那天"。

### 2. Soldered RAM 不是纯粹的"反派"（物理在驱动）

AI 工作负载要求越来越快的内存 → OEM 把内存焊到芯片组上。**好处是真实的**：

- 电路路径更短 → 延迟更低
- 功耗更低
- 散热更好
- 笔记本/AI PC 续航才有今天的数字

**代价是真实的**：再也不能换/扩 RAM。

**全面板载的代表**：
- Intel Lunar Lake
- Apple M-series
- Qualcomm Snapdragon X

> 物理不关心怀旧 — 每一代在更小空间里挤更多性能，「无限可升级」越来越难以工程实现。

### 3. 桌面不会永远免疫

- **Mini PC + All-in-One** 已经拥抱焊死的 LPDDR（低功耗 + 短信号路径 → 现代集成 GPU 和 AI 加速器所需带宽）。
- **Framework Desktop 的标志性妥协** — 即使以"可维修 / 可升级"立身的 Framework 也在第一代 Desktop 上**焊了 LPDDR5X**。原因：模组方案**达不到 Ryzen AI Max 设计的 256GB/s 内存带宽**。Framework 自陈花了好几个月寻找替代方案后接受妥协。
- 桌面处理器越来越追 AI 性能 + 越来越强的集成显卡 — **笔记本的工程权衡迟早侵蚀桌面**。
- **数十年来首次：upgradability 不再是默认保证**。

### 4. PC 正在变成"家电"

- 手机 / 平板 / 笔电已稳定地用模块化换更薄/更高效的设计。
- **云游戏**（Xbox Cloud Gaming / Nvidia GeForce Now）证明**即使高端游戏也不一定需要 $2000 主机** — 当硬件变成可流式的内容，单组件升级就开始显得不必要。
- 即使作者本人也表态："传统 PC 明天不会死" + "你不能把我的硬件从我冰冷僵硬的手里夺走" + "爱好者永远会攒机" — **但方向从未如此清晰**。

## Concepts

> vault 暂无 PC 硬件架构的 concept 页（vault 强项是 AI agent / software 工程）。本节列出本文章可以蒸馏出的概念，留待未来有兴趣时建。

- **[[concepts/on-package-memory-trend]]** (建议) — Intel Lunar Lake / Apple M-series / Snapdragon X 把内存推到处理器封装上/里，物理层动机（带宽/功耗/散热）vs 用户层的代价（不可升级）。
- **[[concepts/lpddr-vs-sodimm-bandwidth-tradeoff]]** (建议) — LPDDR5X 在带宽/功耗/物理尺寸的全面优势 vs SO-DIMM 在可维修性/成本/扩展性的优势；Framework Desktop 是标志性妥协案例。
- **[[concepts/right-to-repair-pc-hardware]]** (建议) — PC 硬件维修权的范围持续缩小，与欧盟维修权立法形成张力。
- **[[concepts/cloud-gaming-as-appliance-shift]]** (建议) — GeForce Now / Xbox Cloud Gaming 把 PC 硬件价值从"你拥有的东西"重新定义为"你订阅的通道"。
- **[[concepts/diy-pc-final-generation-thesis]]** (建议) — 2026 这一代可能真的是最后一代"完整可升级"桌面 PC 的论点（待 5-10 年后验证 ^[ambiguous]）。

## Entities

- **[[entities/framework-computer]]** (建议) — Framework Desktop 是本故事最关键的实体（标志性的"妥协"事件）。Framework Laptop 仍保留模块化设计。
- **[[entities/intel-lunar-lake]]** (建议) — Intel Lunar Lake 是首批把内存推到封装内的 x86 处理器之一。
- **[[entities/apple-m-series]]** (建议) — Apple M-series 从 M1 起就走统一内存架构（UMA）。
- **[[entities/qualcomm-snapdragon-x]]** (建议) — Qualcomm Snapdragon X 是 Windows-on-ARM AI PC 的代表，全面板载内存。
- **[[entities/nvidia-geforce-now]]** (建议) — 云游戏代表之一。
- **[[entities/xbox-cloud-gaming]]** (建议) — 微软云游戏代表。

## Open Questions

1. **Framework Desktop 的焊死方案是否会扩展到 Framework Laptop 16 等旗舰？** 文章只提到 Desktop；Laptop 16 用的是 AMD Ryzen 7040HS / 7045HX 系列，仍是 SO-DIMM。
2. **欧盟维修权立法（2025 年起）**）能否逆转桌面不可升级趋势？— 文中未提，但这是最大的反作用力 ^[inferred]。
3. **集成显卡 + AI 加速器的"内存墙"**最终会否让"加内存"也变无用？— 因为 CPU/GPU 内存访问模式不变，只是封装内集成而已，应用层需求不变 ^[ambiguous]。
4. **云游戏的延迟瓶颈**（30-60ms 输入滞后）是否能被 5G/Wi-Fi 7 + 边缘节点完全消除？— 文章没提，但这是云游戏能否替代本地硬件的关键 ^[ambiguous]。
5. **DIY 文化会否迁移到 SFF / 工控 / 工业 PC 细分市场**？— 普通消费市场不可升级，但小众市场仍可能保留升级性 ^[inferred]。

## Related

- (暂无直接相关 — vault 暂无 PC 硬件架构主题的页面)

---

## Provenance

- **extracted**: 0.78 — 大部分内容是 XDA 文章的直接陈述（Framework Desktop 案例 / Intel/Apple/Qualcomm 板载事实 / 云游戏事实）
- **inferred**: 0.18 — 5 条 Open Questions 中的 #1/#5 和 Repair-Right 张力是文中未说但合逻辑的推论
- **ambiguous**: 0.04 — "DIY PC 是不是最后一代"的核心论断需要 5-10 年才能验证，且受到立法 / 市场需求反向因素影响
- **base_confidence**: 0.45 — 单一来源（XDA 博客 + 评论文）+ 关键论断（"最后一代"）属作者主观判断

---

> **Source**: https://www.xda-developers.com/the-last-generation-of-fully-upgradeable-pcs-is-being-built-right-now/
> **Ingested at**: 2026-08-13T01:53:00Z
> **Mode**: misc（vault 即 obsidian-wiki repo, no project context）
> **Affinity**: {}（无已索引项目连接 — 等待未来 cross-linker 评估）