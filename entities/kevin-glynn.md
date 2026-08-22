---

title: Kevin Glynn (UncleWebb)
category: entity
tags: [people, throttlestop, unclewebb, kevin-glynn, intel, fivr]
relationships:
  - target: "[[references/techpowerup-m16-r1-undervolt-thread]]"
    type: related_to

summary: ThrottleStop 作者 Kevin "UncleWebb" Glynn，活跃于 TechPowerUp 与 NotebookReview 论坛，独立维护 Windows 笔记本 Intel CPU 调参工具 16+ 年（自 2009 起）。是 FIVR / TPL / Speed Shift 调参生态最关键的第一手资料源。
sources:
  - https://www.techpowerup.com/forums/members/unclewebb.html
  - https://www.techpowerup.com/forums/threads/throttlestop-official-thread.255311/
  - https://ultrabookreview.com/31385-the-throttlestop-guide
  - https://throttlestop.en.lo4d.com/windows
created: 2026-08-23
updated: 2026-08-23T08:45:00Z
base_confidence: 0.6
lifecycle: draft
lifecycle_changed: 2026-08-23
provenance:
  extracted: 0.45
  inferred: 0.35
  ambiguous: 0.20---

# Kevin Glynn (UncleWebb)

## 身份

- **真名**：Kevin Glynn ^[extracted]（多源一致引用软件作者为 "Kevin Glynn"）
- **化名**：UncleWebb
- **活跃场域**：
  - TechPowerUp Forums：账户自 2010 注册，累积数千帖 ^[extracted]
  - NotebookReview Forums：长期参与热门 ThrottleStop 串
  - UltrabookReview：作为撰稿人发表过 ThrottleStop 教程
- **角色**：ThrottleStop 唯一活跃维护者（独立开发者）

## 影响

### 工程层

- 自 2009 年起持续维护 ThrottleStop，至今已 16+ 年 ^[extracted]（lo4d 列出"Initial Release"为 2009 年）
- 在多代 Intel 平台（Skylake 6 代到 Arrow Lake）的电压行为分析里是最关键的第一手来源
- 在 m16 R1 / m15 R7 等热门 Alienware 型号讨论里亲自提示"CPU Core / Cache 必须同步"、"E-Cache 别动"、"mV Boost @ 800 MHz"等关键稳定化思路 ^[extracted from UltrabookReview guide]
- 与 Dell XPS 15 系列 BIOS 长期适配（9550/9560 默认关闭 Speed Shift EPP，是 unclewebb 报告的）

### 生态位

- "Intel XTU 限制的非官方破冰者"：Intel XTU 在很多 OEM 修改过的 SKU 上读不到 MSR 0x150，ThrottleStop 绕开这些限制 ^[inferred]
- 通过 TechPowerUp 官方线程直接答疑，跨 OEM 平台（Clevo / Dell / HP / Lenovo）的特殊情况都是 unclewebb 一手判读
- Notebookcheck 2017 首发 ThrottleStop 指南的撰稿人之一 ^[ambiguous]（原指南由"Unwinder"= David Lee 出面；unclewebb 提供技术输入但署名关系未独立确认）

### 历史事件

- **TechPowerUp 官方线程**：ThrottleStop 主要分发渠道，公告新版本与 bug fix
- **NotebookReview 长篇支持串**：600+ 页历史累积 ^[inferred]（社区报告规模）
- **WinRing0 / AV 误报事件**：Avast / Norton / Kaspersky 等安全软件曾把 ThrottleStop 配套的 WinRing0.sys 标记为可疑（基于驱动行为的启发式）；事件已缓和，主流 AV 已加白 ^[ambiguous — 部分来源仍报告 2024-2025 偶发误报]
- **CVE-2025-7771**：Kaspersky 报告过 ThrottleStop.sys 的一个漏洞，被 MedusaLocker 勒索软件团伙在巴西的攻击中利用作 Living-off-the-Land 工具 ^[extracted — 来源见 kaspersky.co.uk 公告] 详细 patch 状态需查 TechPowerUp 官方 ^[ambiguous]

## 风格与社区声誉

- 长期在公开论坛高强度技术作答，被社区标注为"笔记本降压最高产的独立专家"
- 工具闭源但二进制可重现 ^\[inferred]（无 checksum 公开比较）
- 与硬件 OEM 关系：直接与 ASUS / Dell / HP 工程组邮件协作，部分 BIOS 解锁路径反过来影响 OEM ^[ambiguous]

## 局限 / 未解问题

- **职业背景不明**：多源引用为独立开发者，无雇主信息 ^[ambiguous]
- **地理位置不明**：TechPowerUp 个人资料未公开
- **维护活跃度**：最近一次 README / 论坛帖时间 ^[ambiguous — 需直接登陆检查]
- **源代码状态**：完全闭源，社区无审计；CVE-2025-7771 是首个公开记录的安全问题，但也意味着"之前没有 ≠ 没有问题"

## 相关 wiki 页面

- [[throttlestop]]
- [[throttlestop-options]]
- [[throttlestop-fivr-undervolting]]
- [[cpu-undervolting]]
- [[throttlestop-alienware-thermals]]
- [[ultrabookreview-throttlestop-guide-2026]]
- [[research-throttlestop-alienware-thermals]]

## Related

- [[references/techpowerup-m16-r1-undervolt-thread|Techpowerup M16 R1 Undervolt Thread]] — shares #throttlestop (references)

