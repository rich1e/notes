---
title: NDS 世代烧录卡回忆录
category: journal
tags:
  - game
  - retro-gaming
  - nds
  - personal
summary: 错过 NDS 世代后补票的烧录卡折腾经历：DS Two、R4 COM 卡、SuperCard Mini SD、ChisFlash 的横向对比与使用体验。
sources:
  - https://www.omega.im/866/
  - "[[Clippings/电波的电玩记忆-NDS世代 – 电波万事屋.md]]"
  - "[[Clippings/nds折腾.md]]"
created: 2026-06-29
updated: 2026-08-13
tier: peripheral
lifecycle: draft
lifecycle_changed: "2026-06-29"
base_confidence: 0.55
provenance:
  extracted: 0.87
  inferred: 0.10
  ambiguous: 0.03
relationships:
  - target: "[[entities/nds-flashcard]]"
  - target: "[[entities/neogeo-mame]]"
    type: related_to
    type: related_to
---

# NDS 世代烧录卡回忆录

> 整个 NDS 世代完全错过，3DS 发售后才入手 NDSL，以折腾烧录卡为主要乐趣。

## NDS 烧录卡横评

NDSL 具备 Slot-1（NDS 插槽）和 Slot-2（GBA 插槽），折腾价值丰富。

### DS Two（SuperCard 出品）— 公认第一

- 自带缓存，**模拟 GBA 不卡**（其他烧录卡做不到）
- 即时存档功能远超 R4 COM 卡
- TempGBA 模拟器兼容性优于 GBA Runner 2
- 已停售，二手价 ¥200+

### R4 COM 卡（山寨）— 普及度最高

- 3DS 附赠标配，知名度最高
- 实为 DSTTi 山寨 + 时间炸弹（图标炸弹人 = 有倒计时，到期要刷固件）
- 原版 R4 团队早已跑路，市面现存全为山寨

### R4 系列分裂史 — HK / COM / CN 区别

> 整个 R4 名号的来源：2013 年经销与开发团队内部分裂，一部分人另起门户成立 HK 版本。

- **r4.com**（原版）→ 13 年分裂 →
- **r4isdhc.com HK 版** — 海绵宝宝图标，内核最优秀，可刷 bl2ck 内核，兼容性最佳，但 2017-18 年停产 → 现在市面 HK 卡基本是假的（价格 ¥40+）
- **r4isdhc.com COM 版** — 炸弹人图标，兼容性比 HK 略差但量大便宜，可用第三方内核破解倒计时
- **r4isdhc.com.cn** — 山寨卡 + Wood 内核，淘宝俗称「新 HK 卡」，兼容性还行但功能略差、**不支持即时存档**
- **DSOne** — 另一公司产品，家族关系简单

**结论**（横向排序）：`r4hk > dsone > r4com > r4cn`（已记忆，可能有误）。

### DS One / R4 HK 银卡 — 第二梯队

- 运行 TT/Wood/YS 内核
- 功能与 DS Two 接近，无 TempGBA
- 体验差距不大

### Hyper-R4i — 收藏品

- 号称原版 R4 团队参与开发
- 即时存档功能不好用
- 疑为 AceKard 或 EZ-Flash Vi 山寨（PCB 未拆验证）

## GBA 烧录卡（Slot-2）

### SuperCard Mini SD + SuperFW 固件

- 远古产品，David GF 开源固件使其焕发新生
- 除时钟功能需模拟外基本无短板
- 标准 GBA 卡带尺寸，插在 NDSL 凸出，适合 GBA SP
- 2025-05 市场现状：网上能买到的大多数都是抄板山寨版（贴纸模糊、号称 Mini SD 实则用 TF 卡），但能用

### ChisFlash（开源）

- 近年流行，**开源硬件**，二手制卡大佬有售
- PCB 画工精良
- 带时钟，适合重温宝可梦绿宝石

## 印象最深的 NDS 游戏

- **极限脱出999**（玩完善人死亡线再体验完整剧情）
- **苍月十字架**（魔封阵设计令人印象深刻）
- 语言障碍下以汉化版为主，收藏卡带但通常不直接玩

## 相关页面

- [[entities/nds-flashcard]] — NDS 烧录卡技术详情与使用指南

## Related

- [[entities/neogeo-mame]] — NEOGEO / MAME 模拟器配置
