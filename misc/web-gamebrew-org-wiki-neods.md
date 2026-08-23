---
title: "GameBrew NeoDS 主页（2024-12-26 快照）"
category: misc
tags:
  - retro-gaming
  - nds
  - handheld
  - neogeo
  - emulator
  - wiki
sources:
  - "https://www.gamebrew.org/wiki/NeoDS"
source_url: "https://www.gamebrew.org/wiki/NeoDS"
created: 2026-08-12T13:20:00Z
updated: 2026-08-12T13:20:00Z
summary: "GameBrew Wiki NeoDS 主页(2024-12-26 Wayback 快照 oldid=186632):作者链 Ben Ingram (Ingramb) → j03lpr86/nitendo/indy13 + 当前版本 0.2.1.b (2020-08-26) + 4 个 fork + 完整 changelog(0.1.0→0.2.0) + GitHub Yardape8000/NeoDS 仓库 + DLDI patch 步骤。"
affinity: {}
promotion_status: misc
stub: false
provenance:
  extracted: 0.88
  inferred: 0.08
  ambiguous: 0.04
base_confidence: 0.62
lifecycle: draft
lifecycle_changed: "2026-08-12"
tier: peripheral
relationships:
  - target: "[[entities/neogeo-mame]]"
    type: related_to
  - target: "[[concepts/mame-rom-to-neods-conversion]]"
    type: extends
  - target: "[[skills/neods-bios-menu-access]]"
    type: extends
  - target: "[[misc/web-gbatemp-net-threads-neods-a-guide-to-using-one-of-the-greatest-ds-emulators-291225]]"
    type: related_to
  - target: "[[misc/web-gbatemp-net-threads-help-wanted-how-to-access-the-bios-menu-of-neods-neogeo-for-ds-612585]]"
    type: related_to
---

# GameBrew NeoDS 主页(2024-12-26 快照)

## 概述

GameBrew Wiki [NeoDS](https://www.gamebrew.org/wiki/NeoDS) 页面(oldid=186632,Last modified 2024-08-21)是 NeoDS homebrew 的**官方权威元数据页**(MediaWiki + Citizen skin)。原 URL 被 gamebrew 服务器 403 拦截,fallback 到 Wayback Machine 2024-12-26 快照(200 OK)蒸馏为 markdown(本地副本 `_raw/web-gamebrew-org-wiki-neods-20260812.md`,6.7KB)。

## InfoBox(权威元数据)

| 字段 | 值 |
|------|---|
| **Author** | **Ben Ingram (Ingramb)**, updated by j03lpr86, nitendo, indy13 |
| **Type** | Console(DS homebrew emulator) |
| **Version** | **0.2.1.b** |
| **License** | Mixed |
| **Last Updated** | 2020/08/26 |
| **下载** | NeoDS 0.2.0(主)+ EZ3in1 + 0.21 + 0.21.b forks |
| **Website** | Google Groups neods |
| **GitHub** | https://github.com/Yardape8000/NeoDS(社区 fork,未在 infobox 但 External Links 列) |

**关键修正**:vault [[concepts/mame-rom-to-neods-conversion]] 和 [[misc/web-gbatemp-net-threads-neods-a-guide-to-using-one-of-the-greatest-ds-emulators-291225]] 之前都说 **v0.2.0**,gamebrew 实际最新版是 **0.2.1.b**(nitendo fork,2020-08-26 更新),Ingramb 原始 0.2.0 仍是 2008 年的版本。

## 描述(主帖)

> This is a NeoGeo AES/MVS emulator for the Nintendo DS. It can run all types of NeoGeo roms with some limitations.

## Features(模拟的 NeoGeo 组件)

- **M68000 cpu** —— cyclone 引擎
- **Z80 cpu** —— DrZ80 引擎
- **所有 NeoGeo 保护/加密形式**(加密卡带处理)
- **Graphics**(图形)
- **ADPCM audio**(ADPCM 音频)
- **PSG audio**(PSG 音频)

## 未模拟(Known issues)

- **FM audio**(FM 合成音频)—— 影响 NeoGeo 标志性音效(部分 KOF 音乐)
- **Raster effects**(光栅特效)—— 部分游戏视觉
- **Multiplayer**(多人对战)—— NDS 端无网络栈(vault 之前已确认)
- **部分 timing 不精确**

## Installation(完整步骤,比 GBAtemp Nathan Drake 主帖更详细)

1. 准备兼容的 BIOS ROM(`neogeo.zip`)—— 与 GBAtemp 帖子一致
2. **对 NeoDS.nds 做 [DLDI](https://www.gamebrew.org/wiki/DLDI) patch**(不是所有烧录卡都需要,但通用步骤)
3. 转换一些 NeoGeo ROM(例:`mslug.zip`)
4. NeoDS 用与 MAME 相同的 ROM 集,**确保它们先在 MAME 上能跑**
5. 把所有想转换的 ROM + BIOS 放同一文件夹
6. 复制 `NeoDSConvert.exe` 到同文件夹
7. 运行 `NeoDSConvert` —— 自动转换该文件夹下所有 NeoGeo ROM,生成 `*.neo` 文件
8. 复制 DLDI patched 的 `NeoDS.nds` + 所有 `*.neo` ROM 到 microSD 根

## User guide(用户操作 + GUI)

### 主流程
- 运行 `NeoDS.nds` → 主菜单加载 → 显示 microSD 上所有 ROM 列表
- 方向键选择 + Start 加载游戏
- **可不带音频加载**(提速帧率),无音频游戏只能通过重载恢复
- **带 GBA slot 外部 RAM 的烧录卡**(可选)—— NeoDS 用额外 RAM 缓存数据,提升部分游戏速度,主屏会显示 "SLOT2" 字样

### NeoDS GUI 选项
- **Video** —— normal(裁剪屏)/ scaled(全屏缩放)
- **CPU Clock** —— NeoGeo CPU 可降频(实验;降频减轻模拟负担,部分游戏本身不需全速)
- **Screen Off** —— 下屏关闭(点任意处恢复)
- **Load rom** —— 加载新游戏
- **Save** —— 把当前配置 + SRAM 写到 microSD
- **Input** —— 重映射输入

### Input 重映射机制
**网格布局**:DS 按钮沿右列,NeoGeo 按钮沿顶行。每个 checkbox 把一行 NeoGeo 按钮映射到一个 DS 按钮。**多对一**(格斗游戏常用):一个 DS 按钮可触发多个 NeoGeo 按钮。

## 完整 Forks 列表(vault 之前无)

| Fork | 作者 | 基于 | 主要变更 |
|------|------|------|---------|
| **NeoDS TWL** | Universal-Team | 2.0 source | 整合到 **Twilight Menu++** |
| **NeoDS GBMacro**(wip) | xonn83 | 0.2.0 | GameBoy Macro 用(NDS Lite 改 GBA 形态) |
| **NeoDS 0.2.0 EZ flash 3in1** | j03lpr86 | 0.2.0 | EZ Flash 3in1 卡带兼容 |
| **NeoDS 0.21 + 0.21.b** | nitendo | 0.2.0 | ROM 菜单上限 64→256;Left/Right = pageUp/pageDown;配置文件目录 `fat:/data/neoDS/`;所有 ROM 可放独立子目录(由 `_NeoDs.ini` 控制);0.21b_scaled 默认 scaled 全屏 |
| **NeoDS 0.21 mod** | indy13 | 0.21 | 改 ROM 路径 + 法/英双语 readme |

**关键事实**:Indy13 同时也是 vault [[misc/web-gbatemp-net-threads-dstwo-not-making-proper-contact-with-my-ds-lite-634036]] DSTWO 接触不良主贴的贡献者之一 —— 社区活跃的 homebrew 玩家跨多个项目。

## 完整 Changelog(原帖官方历史)

| 版本 | 日期 | 关键变更 |
|------|------|---------|
| Summer 2007 | - | 项目启动 |
| **v0.1.0** | 2008-04-29 | 初始发布 |
| **v0.1.1** | 2008-05-06 | Level2 sprite cache(slot2 RAM);增大 ROM 页(修 Metal Slug 1 手雷);修中断(修 Metal Slug 2);修 tile palette update(Last Blade 2 GUI);converter 用最新 MAME 数据(修 KOF98 等);FluBBa DAA Z80 指令优化省 RAM;-bios 选项修复 |
| **v0.1.1a** | 2008-05-06 | "Forgot to include updated NeoDSConvert is last version" |
| **v0.2.0** | 2008-06-19 | Key configuration;Pause key;合盖睡眠;SRAM+config 保存;修切换 ROM 在某些烧录卡的崩溃;修 palette bank swap bug(Metal Slug 1 HUD);修 vcounter / vposition 中断(修 Samurai Showdown 3 冻结 + Blazing Star level 2 图形);修 DLDI + slot2 RAM 同一卡冲突(supercard lite);修 slot2 RAM 用久后图形损坏 |

## Credits

FinalDave / notaz / Reesy / Wintermute / chishm / MAME / Minizip / www.pocketheaven.com(hosting NeoDS forum) / FluBBa / GnGeo / FinalBurnAlpha / MVSPSP / Charles MacDonald / Alexander Stante / Brandon Long + gbadev.org forums 上回答问题的所有人。

## External Links(vault 关键发现)

- Google Groups - http://groups.google.com/group/neods
- GitHub - **https://github.com/Yardape8000/NeoDS**(社区 fork,值得进一步调查是否有现代兼容补丁)
- **vault 之前 ingest 的 GBAtemp 612585 BIOS 帖子被 gamebrew 官方列为 reference**:
  https://gbatemp.net/threads/help-wanted-how-to-access-the-bios-menu-of-neods-neogeo-for-ds.612585/post-10307753
  (Nikokaro 关于 NeoDsConvert 用法的特定 post)

## Controls(完整官方键位)

| NDS 键 | NeoGeo 映射 | 备注 |
|--------|------------|------|
| D-Pad | 方向键 | |
| A/B/X/Y | A/B/C/D | NeoGeo 街机/家用机动作键(无独立 X/Y,模拟器映射) |
| L | Pause | |
| R | Select | **新版 uni-bios = coin** |
| Start | Start | |
| Select | Coin | |
| Stylus | NeoDS GUI | |

**注意**:R 键同时是 "Select(coin in newer uni-bios)" 和 vault [[skills/neods-bios-menu-access]] 提到的 "R+Start = cheat menu" —— gamebrew 2020 fork 没提 R+Start cheat 菜单,说明 cheat 菜单是 Nikokaro 后期发现的新功能。

## vault 整合

**新信息(本帖独有)**:
- 完整作者链:Ingramb → j03lpr86 / nitendo / indy13(vaull 之前只有 Ingramb 一行)
- **0.2.1.b 是当前实际可用版本**(vault 之前只说 0.2.0)
- **DLDI patch 步骤**(GBAtemp 主帖没提)
- **完整 forks 链 + 各自用途**(TWL/Twilight Menu++ / GBMacro / EZ3in1 / 0.21b 分目录)
- **GitHub Yardape8000/NeoDS 社区 fork**(可能含现代兼容补丁)
- **GUI 选项完整列表** + **Input 重映射网格布局**(格斗游戏多对一映射)

**与 vault 已有知识交叉验证**:
- BIOS 嵌入(Nikokaro 612585)→ **确认**(gamebrew 也说必须自带 `neogeo.zip`)
- uni-bios 菜单 A+B+X(GBAtemp 612585 + 本 skill)→ **gamebrew 没列 BIOS 菜单键**(不在 controls 表),但 [[skills/neods-bios-menu-access]] 的键位知识独立于 gamebrew
- R+Start cheat 菜单(Nikokaro 612585)→ **gamebrew 没提**(2020 fork 没继承此发现)
- 版本漂移问题(GBAtemp 291225 + Nathan Drake)→ **部分修正**:Ingramb 主线 0.2.0 自 2008 不更新,但 nitendo/indy13 fork 持续到 2020-08,严格说 vault "NeoDS v0.2.0 未跟进 MAME ROM 重命名"应改为"Ingramb 主线 0.2.0 未跟进,但社区 fork 仍在更新"

## Open Questions

- **(O1)** GitHub Yardape8000/NeoDS 是只镜像 gamebrew zip 还是含独立改进?(需进一步调查)
- **(O2)** Nitendo 0.21.b 的 `_NeoDs.ini` 配置文件机制详细格式?(vault 之前没记录)
- **(O3)** Indy13 0.21 mod 的法/英 readme 翻译内容?(社区跨语言贡献)
- **(O4)** NeoDS TWL 整合到 Twilight Menu++ 的具体路径?(Universal-Team 仓库)
- **(O5)** gamebrew 提到 Google Groups neods 还有"兼容性列表在 discussion thread"—— 是 web-gbatemp-net-threads-neods-names-compatibility-list-102177 之外的第二个官方兼容列表?

## Related

- [[entities/neogeo-mame]] — 桌面 MAME 端 NeoGeo 配置(vault NeoGeo 锚点)
- [[concepts/mame-rom-to-neods-conversion]] — NeoDS 转换原理(需补 fork 链 + 0.2.1.b + GitHub)
- [[skills/neods-bios-menu-access]] — NeoDS BIOS 菜单键位(需补 R 键双功能提示)
- [[misc/web-gbatemp-net-threads-neods-a-guide-to-using-one-of-the-greatest-ds-emulators-291225]] — Nathan Drake 主教程(gamebrew 与之互证)
- [[misc/web-gbatemp-net-threads-help-wanted-how-to-access-the-bios-menu-of-neods-neogeo-for-ds-612585]] — Nikokaro BIOS 帖子(gamebrew External Links 引用)