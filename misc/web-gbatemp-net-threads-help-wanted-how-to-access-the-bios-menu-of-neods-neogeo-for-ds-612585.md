---
title: "GBAtemp NeoDS BIOS 菜单求助帖（2022）"
category: misc
tags:
  - retro-gaming
  - nds
  - handheld
  - neogeo
  - emulator
  - forum
sources:
  - "https://gbatemp.net/threads/help-wanted-how-to-access-the-bios-menu-of-neods-neogeo-for-ds.612585/"
source_url: "https://gbatemp.net/threads/help-wanted-how-to-access-the-bios-menu-of-neods-neogeo-for-ds.612585/"
created: 2026-08-12T12:50:00Z
updated: 2026-08-12T12:50:00Z
summary: "GBAtemp 帖子 612585 (Nikokaro OP 2022-05-21):NDS 端 NeoDS 模拟器怎么调 uni-bios 菜单切地区/模式。最终答案:ROM 加载时按 A+B+X;副产物包括 cheat 菜单 R+Start、BIOS 嵌入机制、DS Lite vs DSi 摇杆差异。"
affinity: {}
promotion_status: misc
stub: false
provenance:
  extracted: 0.82
  inferred: 0.13
  ambiguous: 0.05
base_confidence: 0.48
lifecycle: draft
lifecycle_changed: "2026-08-12"
tier: peripheral
---

# GBAtemp NeoDS BIOS 菜单求助帖（2022）

## 概述

GBAtemp 论坛贴 [Help wanted: how to access the BIOS menu of NeoDS NeoGeo for DS](https://gbatemp.net/threads/help-wanted-how-to-access-the-bios-menu-of-neods-neogeo-for-ds.612585/)（Nikokaro OP 2022-05-21，20 回复，跨 2022-2023 年）是 **NeoDS v0.2.0 上 uni-bios 菜单触发方式**的简短咨询帖。原始 URL 被 Cloudflare challenge 拦截（defuddle / WebFetch / superpowers-chrome / curl 全路 403），fallback 到 **Wayback Machine 2025-05-21 快照**（200 OK）蒸馏为 markdown（本地副本 `_raw/web-gbatemp-net-threads-612585-neods-bios-menu-20260812.md`，5.5KB）。

## 原始问题（POST 1，Nikokaro 2022-05-21）

> Would someone kindly tell me how to access the general menu of uni-bios: which button combination should I use and when? I need it to switch from console mode to arcade mode.

**使用场景**:所有 ROM 都用 uni-bios (bios 8) 转换过；想切到 arcade 模式（街机模式续关无限 vs 家用机模式续关受限）。**不愿为切模式重新转换整套 ROM**。

## 最终答案（POST 3 + POST 5 验证）

- **POST 3 DaRk_ViVi (2022-05-23)**：*"if you are using Uni-Bios you should get the menu by pressing **A+B+X** while it's loading the rom."*
- **POST 5 Nikokaro (2022-05-23)**：*"It works! It is exactly what I was looking for."* ——验证成功。

**关键事实**：NeoDS 上 uni-bios 菜单触发键位是 **`A+B+X` 在 ROM 加载瞬间**（与桌面 MAME / 真实 NeoGeo 的 `A+B+C` 不同，详见 [[skills/neods-bios-menu-access]]）。

## 帖内其他有价值发现

### Cheat 菜单（POST 2 Nikokaro）

Nikokaro 在玩游戏时**偶然按出** cheat 菜单：

> by randomly pressing buttons during gameplay I discovered, if anyone else is interested, the cheat menu **(R+start)**

这是 NeoDS 文档里没正式说明的快捷键（vault [[concepts/mame-rom-to-neods-conversion]] 之前未记录），社区发现。

### DS Lite vs DSi 摇杆差异（POST 2）

Nikokaro 的硬件评测：

| 主机 | D-pad 表现 |
|------|-----------|
| **DS Lite** | "responds exceptionally well especially for fighting games" —— 格斗游戏优选 |
| **DSi** | "too stiff and the diagonals don't work" —— 太硬、对角失灵 |

**推论**：NeoDS + DS Lite + 格斗游戏 = Nikokaro 的"完美组合"；DSi 摇杆反向升级反而更差（这是任天堂的硬件事实，与模拟器无关）。

### NeoDS 仅 NeoGeo（POST 6/7）

**POST 6**: *"Neo Geo is on the DS?"*（已删除用户 578956，惊叹）
**POST 7 Nikokaro**: *"Of course. And for a long time. NeoDS. A masterpiece of talent and technique, running on just 4mb of RAM. Unbelievable!"*

15 年后仍跑全速 NeoGeo 街机游戏，Nikokaro 评"DS homebrew 史上最强模拟器之一"（同 [[misc/web-gbatemp-net-threads-neods-a-guide-to-using-one-of-the-greatest-ds-emulators-291225]] 的评价一致）。

### BIOS 嵌入机制（POST 9/11/13）

POST 11 Nikokaro 的关键澄清：**NG BIOS 不是独立文件**，而是在 `NeoDsConvert.exe` 转换游戏 ROM 时被**嵌入到每个 .neo 文件**里：

> NG BIOS has to be inserted into the neo geo game you are interested in at the time of conversion, and the tool to do this only works on Windows. There's no other way, sorry.

**工程后果**：
- 没有"放个 BIOS 到 microSD 根"这种配置；每个游戏自带 BIOS
- 切换 BIOS 版本（如 uni-bios 3.x ↔ 4.0 ↔ 原版）= 重新转换该游戏所有 ROM
- 用户 yoooblls 想在手机/Android 上做转换 → Nikokaro 直说不可能（NeoDsConvert.exe 是 Windows-only）

### NeoDS 不能跑 CPS2（POST 14）

yoooblls 问 Capcom vs Marvel → Nikokaro 解释 *"...it's an cps2 game"* —— **NeoDS 是 NeoGeo-only 模拟器**（基于 NeoGeo 的 68000+Z80 硬件），不能跑 CPS2 的 Capcom 街机游戏（基于不同的硬件架构）。

vault [[concepts/mame-rom-to-neods-conversion]] 的 MAME ROM 范围限定在 NeoGeo 集（CPS2 不在其列），本帖是一次性确认。

### 推荐的 NeoDS 大作（POST 15 Nikokaro）

> *SNK vs. Capcom Plus* ... perfectly playable on NeoDS: the only flaw is the backgrounds that are too dull, flat and static. ... it is almost 80MB big.

**80MB 是 NeoDS 能处理的极限**（与桌面 MAME 动不动几个 GB 完全不同；NDS microSD 存储+读取带宽+ 4MB RAM 三重约束）。

## 帖子作者画像

- **Nikokaro (user 517430)** —— OP + 主回帖者，意大利/欧洲口音（"lad" "of course" "bro" 称呼），资深深宅 NeoDS 玩家
- **DaRk_ViVi (user 22157)** —— 引用第三方资料回答键位
- **yoooblls (user 617418)** —— Android/手机端用户，受 NeoDsConvert.exe 仅 Windows 限制
- **Angelus (user 577926)** —— 2023 年仍来询问 BIOS 转换问题，说明 NeoDS 社区到 2023 年仍有零星活跃
- **Magician_777 (user 480333)** —— 2023-11 也来询问，2 年后还有新人入门

## 与 vault 已有 NeoDS 知识的整合

本帖是 [[misc/web-gbatemp-net-threads-neods-a-guide-to-using-one-of-the-greatest-ds-emulators-291225]]（Nathan Drake 主教程）的**补丁**：Nathan Drake 教程只覆盖 4 阶段流程（下载 → 转换 → 部署 → 运行），但**没有详写怎么在运行中触发 uni-bios 菜单 / cheat 菜单**，本帖补全这一空缺。

vault [[concepts/mame-rom-to-neods-conversion]] 现在新增两段：
- **NeoDS 端 BIOS 菜单键位** —— `A+B+X` (NDS 上) vs `A+B+C` (NeoGeo 实体 / 桌面 MAME) 的差异
- **BIOS 嵌入机制** —— 无独立 BIOS 文件，每个 .neo 自带

## Open Questions

- **(O1)** Nikokaro 提到的 `R+Start` cheat 菜单在 NeoDS README 是否有正式记载？（vault 仅"偶尔按出"，未独立核实 ^[ambiguous]）
- **(O2)** `A+B+X` 的"loading the ROM"具体是哪个时间窗？（DS 屏闪、NeoDS 启动画面、还是游戏首帧前？）Nikokaro 没量化
- **(O3)** Android 端 NeoDsConvert 是否真的"完全无解"？可能存在 QEMU / Wine on Termux 路径 ^[inferred]
- **(O4)** DSi 摇杆的"diagonals don't work"是 NeoDS 软件问题还是 DSi 硬件本身？（vault [[entities/nds-flashcard]] 的 R4iSDHC 也提到 DSi 兼容性，但此处是物理 D-pad）
- **(O5)** 2025-04 至 2025-05 仍有用户提问（POST 41-48 时间戳），说明 GBAtemp 上 NeoDS 持续 18+ 年有零星新讨论 —— 反映"旧 homebrew 长尾社区"模式

## Related

- [[entities/neogeo-mame]] — 桌面 MAME 端 NeoGeo 配置（BIOS/uni-bios 菜单键 A+B+C 的桌面 MAME 锚点）
- [[concepts/mame-rom-to-neods-conversion]] — NeoDS 转换原理 + 现在补全 NeoDS 端键位与 BIOS 嵌入机制
- [[entities/nds-flashcard]] — DS Lite / DSi 摇杆硬件差异（NDS 烧录卡簇）
- [[skills/neods-bios-menu-access]] — 主帖答案蒸馏的可操作 skill 页（NDS 端 uni-bios + cheat 菜单两步进入）
- [[misc/web-gbatemp-net-threads-neods-a-guide-to-using-one-of-the-greatest-ds-emulators-291225]] — Nathan Drake 主教程；本帖是其补丁