---
title: How to unlock Alienware m16 R1 undervolt for ThrottleStop (TechPowerUp Forum)
category: references
tags: [alienware, m16-r1, throttlestop, undervolt, techpowerup, alienware-melting]
sources:
  - https://www.techpowerup.com/forums/threads/how-to-unlock-alienware-m16-r1-undervolt-for-throttlestop.319229/
source_url: https://www.techpowerup.com/forums/threads/how-to-unlock-alienware-m16-r1-undervolt-for-throttlestop.319229/
created: 2026-08-23
updated: 2026-08-23
summary: TechPowerUp forum 帖子专门讨论如何在 Alienware m16 R1 (13 代 HX) 上解锁 BIOS UnderVolt Protection 并应用 ThrottleStop 降压。核心贡献：Alienware_Melting 的 "mV Boost @ 800 = +100 mV" 模板。
provenance:
  extracted: 0.75
  inferred: 0.15
  ambiguous: 0.10
base_confidence: 0.75
lifecycle: draft
lifecycle_changed: 2026-08-23
---

# How to unlock Alienware m16 R1 undervolt for ThrottleStop

来源：https://www.techpowerup.com/forums/threads/how-to-unlock-alienware-m16-r1-undervolt-for-throttlestop.319229/

## 涵盖内容

- BIOS UnderVolt Protection 解锁步骤
- 验证可行的 ThrottleStop FIVR 配置（−100 mV Core + −100 mV Cache + mV Boost +100 mV @ 800 MHz）
- 稳定性验证流程
- CPU Core / Cache 必须同步、E-Cache 不动

## 关键命题

- "mV Boost @ 800 MHz = +100 mV"：**m16 R1 社区确认的稳定秘诀**^[extracted]
  - 纯 −100 mV 会让 idle / 唤醒跌出稳定窗口
  - 在 800 MHz 点上加 100 mV 补偿，等价于 V/F 曲线只对高频段生效
- 温度降幅 8-15°C @ 全核负载
- 部分体质好的 i9-13980HX 可达 -150 mV 稳定

## 局限

- **直接 fetch 失败**（403 / Anubis 拦截）— 内容靠 WebSearch 摘要 + 第三方 (ArchWiki/NotebookTalk) 交叉验证获取
- 仅聚焦 m16 R1；其它 Alienware SKU 需要单独测试
- 1.13.0+ BIOS 步骤未涵盖到这块具体的 "BIOS 后菜单消失" 场景的解决方案

## 相关 wiki 页面

- [[throttlestop-alienware-thermals]]
- [[alienware-bios-undervolt-unlock]]
- [[throttlestop-fivr-undervolting]]
- [[throttlestop]]
- [[kevin-glynn]]
- [[research-throttlestop-alienware-thermals]]
