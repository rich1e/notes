---
title: "GBAtemp Wiki DSTwo Plugin 索引页（2025-03-20 快照）"
category: misc
tags:
  - retro-gaming
  - nds
  - handheld
  - dstwo
  - emulator
  - wiki
sources:
  - "https://wiki.gbatemp.net/wiki/DSTwo_Plugin"
source_url: "https://wiki.gbatemp.net/wiki/DSTwo_Plugin"
created: 2026-08-12T13:10:00Z
updated: 2026-08-12T13:10:00Z
summary: "GBAtemp WikiTemp 的 DSTwo Plugin 索引(2025-03-20 Wayback 快照):SuperCard DSTwo 烧录卡的 3 文件 plugin 协议(`/_dstwoplug/` 目录 + BMP 16bit 40x42 + INI + .nds/.plg 同名约束),含 4 类别(Emulators/Utilities/Multimedia/Games)100+ 插件清单。"
affinity: {}
promotion_status: misc
stub: false
provenance:
  extracted: 0.80
  inferred: 0.15
  ambiguous: 0.05
base_confidence: 0.55
lifecycle: draft
lifecycle_changed: "2026-08-12"
tier: peripheral
relationships:
  - target: "[[entities/nds-flashcard]]"
    type: related_to
  - target: "[[concepts/dstwo-plugin-system]]"
    type: derived_from
  - target: "[[concepts/dstwo-contact-fix]]"
    type: related_to
  - target: "[[concepts/mame-rom-to-neods-conversion]]"
    type: related_to
  - target: "[[misc/web-gbatemp-net-threads-dstwo-not-making-proper-contact-with-my-ds-lite-634036]]"
    type: related_to
---

# GBAtemp Wiki DSTwo Plugin 索引页(2025-03-20 快照)

## 概述

GBAtemp WikiTemp 页面 [DSTwo Plugin](https://wiki.gbatemp.net/wiki/DSTwo_Plugin) 是 SuperCard DSTWO 烧录卡插件生态的**官方索引页**(oldid=75005)。原 URL Cloudflare 拦截 403,fallback 到 Wayback Machine 2025-03-20 快照(200 OK)蒸馏为 markdown(本地副本 `_raw/web-wiki-gbatemp-net-wiki-dstwo-plugin-20260812.md`,15KB)。

## DSTwo Plugin 是什么

A DSTwo 'Plugin' consists of **3 files** stored in the **`/_dstwoplug/`** folder on the DSTwo flashcard:

| 文件 | 格式 | 约束 |
|------|------|------|
| **图标** | 16bit BMP,40×42 像素 | 必须是 16bit 色深,否则菜单不显示(故障模式 "NOT 16bit")|
| **INI** | 文本,3 行 | 2 行用于 Display Name 与图标 graphic 路径声明 |
| **程序** | `*.nds` 或 `*.plg` | `.nds` = 通用 DS homebrew;`.plg` = 专门利用 DSTwo 额外 CPU/Memory 的程序 |

**核心协议**:3 个文件 **必须同名**(NDS 与 INI 同名,BMP 与 INI 声明的路径同名)。任何一文件缺失或错名 = 故障。完整协议见 [[concepts/dstwo-plugin-system]]。

## 安装步骤

1. 点击页面上的 'Plugin' 链接下载插件文件
2. 解压 → 复制 BMP 图标 + INI 文件到 `/_dstwoplug/`
3. 点击 'Program' 链接下载程序文件
4. 解压 → 复制 NDS 到 `/_dstwoplug/`
5. **确保 NDS 文件名与 INI 文件名一致**;若不同 → 重命名

部分 homebrew 需要额外文件夹/文件,需读 README.txt。

## 常见 3 种 Plugin 故障

| 故障模式 | 原因 |
|---------|------|
| **No 'INI'** | ini 缺失 或 与 nds 文件名不同 |
| **NOT 16bit** | bmp 不是 16bit 色深 |
| **No 'BMP'** | bmp 缺失 或 与 ini 声明的图标路径不同名 |

## 4 类插件清单(蒸馏自 2025-03-20 快照)

### Emulators(28 个)
- **AemioDA** - Arcade Emulator
- **ApprenticeminusDS** - GameGear/MasterSystem
- **ColecoDS** - Colecovision
- **DSboy** - Gameboy
- **DSmasterplus** - MasterSystem
- **DualSwan** - Wonderswan(**只能跑 <4MB ROM,低 FPS,自 2006-10 起未更新** ^[ambiguous])
- **FrodoDS** - C64(NDS 已含在 Plugin 内)
- **GameYob** - GB/GBC([原 GBAtemp 主题 343407](http://gbatemp.net/threads/gameyob-a-gameboy-emulator-for-ds.343407/))
- **JenesisDS / jEnesisDS** - Sega Genesis(两个分支)
- **Lameboy** - GB/GBC(3 个变体:2 备选图标)
- **MarcaDS** - Arcade
- **Mini-Vmac DS** - Mac 68k
- **NDSGBA** - GBA(官方 SD2 GBA 模拟器备选图标)
- **NeoDS** - Neo Geo(!!! **vault [[concepts/mame-rom-to-neods-conversion]] 的同款**)
- **NesDS / NesterDS** - NES
- **NitroGrafx** - PC Engine / TurboGrafx-16
- **PicodriveDS** - Sega Genesis
- **S8DS** - Game Gear / Master System
- **ScummVM** - LucasArts(3 个变体:2 备选图标)
- **SnemulDS / NDSSFC / SnesDS** - SNES
- **SpeccyDS / ZXDS / ZXDS alt.** - Sinclair ZX Spectrum
- **StellaDS / StyxDS** - Atari
- **WabbitDS** - TI-83+

### Utilities(20+ 个)
- **Beup live** - MSN Client(2 个变体)
- **Bunjalloo** - Web browser
- **ClockDS** - Alarm clock
- **DiagnoSe** - DS function tester
- **Dissonance** - WiFi Radio
- **DS battery timer / DSftp / DSorganize** - 文件/系统工具
- **DSCovered** - Homebrew launcher(**"Unable to actually launch anything - needs loader made for it"** ^[ambiguous])
- **DSkiosk / dstwo_game / DS2tools** - 启动器/EOS
- **DSTwitter** - Social Network App(2010s 时代遗物)
- **Ifile / iMenu / Xenofile** - 文件管理
- **NDS backup tool FTPd / Savbackup / Savsender** - 存档管理
- **PokesavDS** - Pokémon 存档编辑器
- **svsip / WiFi Chat** - VOIP
- **USRCheatUp** - 金手指更新器
- **ZogNC** - Calculator

### Multimedia(25+ 个)
- **音频**:Axe / cellDS / DS Drum machine (TR-909) / DScratch / DStepV2 / DuckSlinger / glitchDS / GrooveStep / Innocence / lmp-ng (MP3) / Mario paint composer / Nitrotracker / Online Jukebox / ProteinDS / repeaterDS / Sniff Jazzbox / ToneSynthDS
- **视频**:DSVideo / Mpeg4 Player / Spinal Movie Player / Tuna-viDS (Xvid) / Tuna-viDS (备选图标)
- **阅读**:Comic-book DS / DSBible / DSlibris / DSreader / DScritor / iReader / TextDS2 / Visual Novel DS
- **绘图**:Animanatee / Colors (Drawing, 3 个变体) / Flickbook / UAPaint

### Games(30+ 个)
- **1942 / 1943 / Green beret** - 街机 ports(需要原 ROM)
- **AmplituDS / Arsenal / AppleAssault / Bloxavoid** - 独立游戏
- **DeflektorDS / DSCraft / DSdoom** - 复杂游戏(DSdoom 需要 WAD shareware 文件)
- **Duke3DS** - 需要原版/共享版资源
- **EpicCaveman / Every Extend / LemmingsDS** - 经典复刻
- **Lone Wolf** 系列(Book 1-5) - 文字冒险
- **Maelstrom / Mahjong / MazeD / Maziacs / Meteora** - 杂项
- **Minecraft2D**(Crafting 版 / Mobs 版 - 需注意选择)
- **Multiview / NetHack / Nightfox Colors / PlantsVsZombies / Rick Dangerous** - 经典
- **Shmup / ShootingWatch / Smash bros crash / SSb clash** - 动作
- **Virus DS**(需重命名文件)+ **Warcraft:Tower Defence / Warhawk / World of Sand**

## 历史状态

Wiki 内明确记录几项状态:

- **官方 alidsl Full download pack** —— *UPDATE 10/29/13 : Link is invalid on filetrip and on the official supercard forums!*(2013-10-29 后失效)
- **替代 icon pack by VatoLoco** - 仍可用
- **Icon Templates for Slot-1 and Slot-2 + 16-bit converting Tool** - 自制图标工具链
- **官方 DSTWO 插件** —— http://eng.supercard.sc/manual/dstwo/plugin.htm
- **插件添加/反馈 thread** —— http://gbatemp.net/t229551-supercard-dstwo-plug-ins

## Credits(wiki 贡献者)

alidsl(GBAtemp 原帖) / CannonFoddr(wiki 创始人)/ tj_cool(wiki 模板)/ Traitor(psd 模板)/ spinal_cord(bmp 转换工具)/ VatoLoco(帮助)/ ron975(plugins 备份)/ SuperCard Team。

## vault 整合

- **核心抽象**:[[concepts/dstwo-plugin-system]] —— 把 3 文件协议 + `/_dstwoplug/` 目录规范 + 3 种故障模式 + 16bit BMP 约束蒸馏为可复用概念页
- **DSTWO 知识簇**:
  - [[entities/nds-flashcard]] —— DSTWO 是 vault 中"最高级烧录卡"判断的事实来源之一
  - [[concepts/dstwo-contact-fix]] —— 4 路径修复框架
  - [[misc/web-gbatemp-net-threads-dstwo-not-making-proper-contact-with-my-ds-lite-634036]] —— 接触不良主贴蒸馏
- **跨 homebrew 簇**:
  - [[concepts/mame-rom-to-neods-conversion]] —— NeoDS 也是 DSTWO plugin 之一(本页 Emulators 列表明确列出)
  - [[concepts/japanese-retro-gaming]](潜在)—— NDS homebrew 长尾社区的真实案例

## Open Questions

- **(O1)** supercard.sc 官方域名是否仍存活?(wiki 链接 http 协议,无 https,且 supercard 在 2018 前后已重组)
- **(O2)** alidsl pack 替代下载点是否仍可用?(wiki 链接已失效)
- **(O3)** 100+ 插件中,多少能跑在 2026 年的烧录卡?(DSTWO 自身硬件 2026 年仍可买,但 microSD 容量/兼容性?)
- **(O4)** 16bit BMP 约束的硬件根因 —— DS GBA slot 渲染管线只支持 16bit color depth?(vault 缺 DS 渲染管线文档 ^[inferred])
- **(O5)** DualSwan 自 2006-10 不更新 —— 是 developer 失联还是程序已完成?vault [[concepts/japanese-retro-gaming]] 应展开类似长尾案例

## Related

- [[entities/nds-flashcard]] — DSTWO 烧录卡全景(R4 / DSTWO 价格对比 + 4 卡版本对比 + R4 FAQ)
- [[concepts/dstwo-plugin-system]] — 本 wiki 页的事实 → 可复用概念抽象
- [[concepts/dstwo-contact-fix]] — DSTWO 接触不良 4 路径修复(同烧录卡不同问题)
- [[misc/web-gbatemp-net-threads-dstwo-not-making-proper-contact-with-my-ds-lite-634036]] — 接触不良主贴
- [[concepts/mame-rom-to-neods-conversion]] — NeoDS 也是本页列出的 DSTWO plugin 之一
- [[misc/web-wiki-gbatemp-net-wiki-dstwo-plugin]] — 本主页(本蒸馏副本)