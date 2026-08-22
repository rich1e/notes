---

title: Dell KB — 外星人笔记本 CPU 高温排查
category: references
tags: [dell, alienware, support, thermal, tcc, kb]
relationships:
  - target: "[[entities/smokeless-umaf]]"
    type: related_to

sources:
  - https://www.dell.com/support/kbdoc/en-us/000131532
  - https://www.dell.com/support/article/en-us/sln308057
source_url: https://www.dell.com/support/kbdoc/en-us/000131532
created: 2026-08-23
updated: 2026-08-23T08:45:00Z
summary: Dell 官方支持文档：外星人笔记本（13 R3/15 R3-R7/17 R4-R5/m15/m15 R2-R3 等）CPU 100°C 是正常 TCC 工作机制；提供 AWCC 散热模式建议、BIOS/驱动更新、SupportAssist 压力测试步骤。不直接讲 ThrottleStop。
provenance:
  extracted: 0.7
  inferred: 0.2
  ambiguous: 0.1
base_confidence: 0.65
lifecycle: draft
lifecycle_changed: 2026-08-23---

# Dell KB — 外星人笔记本 CPU 高温排查

来源：https://www.dell.com/support/kbdoc/en-us/000131532

## 涵盖内容

- 总结多个旧/新外星人 SKU 的 TCC 阈值（多数 100°C，13 R3 / 15 R3-R4 / 17 R4-R5 为 97°C）
- 提供 AWCC 散热模式建议（Performance / Balance / Cool / Quiet / Full Speed）
- 建议 BIOS、驱动、Windows 更新
- SupportAssist 跑压测 + Fusion 页监控
- FAQ：idle 温度高 / 游戏时温度上升 / 100°C 是否损坏 CPU（明确：不会）

## 关键命题

- "100°C 是 TCC 激活点，不是故障"^[extracted] — Dell 把它当成规格的一部分，区别于消费 Z 系列的默认 95-105°C
- AWCC Fusion 页可监控 CPU 频率+温度，**官方**监控点
- BIOS 1.1.0+ 已把 PL1 从 115W 调到 75W ^[ambiguous]（间接证据，源未给完整 URL 引用）

## 局限

- 不讲 ThrottleStop / 降压，官方立场保守
- 不同 SKU 散热设计差异大，单一温度阈值不能一概而论
- AWCC TCC Offset 滑块功能在此 KB 中未见介绍 ^[extracted]（与 sln308057 是两篇文档）

## 相关 wiki 页面

- [[throttlestop-alienware-thermals]]
- [[alienware-bios-undervolt-unlock]]
- [[cpu-undervolting]]
- [[throttlestop-fivr-undervolting]]
- [[research-throttlestop-alienware-thermals]]

## Related

- [[entities/smokeless-umaf|Smokeless_UMAF]] — shares #alienware (entities)

