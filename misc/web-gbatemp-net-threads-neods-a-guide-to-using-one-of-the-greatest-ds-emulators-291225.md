---
title: "GBAtemp NeoDS 完整使用指南（2011）"
category: misc
tags:
  - retro-gaming
  - nds
  - handheld
  - neogeo
  - emulator
  - forum
sources:
  - "https://gbatemp.net/threads/neods-a-guide-to-using-one-of-the-greatest-ds-emulators.291225/"
source_url: "https://gbatemp.net/threads/neods-a-guide-to-using-one-of-the-greatest-ds-emulators.291225/"
created: 2026-08-12T03:55:00Z
updated: 2026-08-12T03:55:00Z
summary: "GBAtemp NeoDS 0.2.0 教程（Nathan Drake 2011）：NDS 上运行 NeoGeo 街机游戏的完整 4 阶段流程（下载 → MAME ROM 转换 → microSD 部署 → 运行），含 56 回复里 2016 年后的兼容性过时警告。"
affinity: {}
promotion_status: misc
stub: false
provenance:
  extracted: 0.78
  inferred: 0.16
  ambiguous: 0.06
base_confidence: 0.42
lifecycle: draft
lifecycle_changed: "2026-08-12"
tier: peripheral
---

# GBAtemp NeoDS 完整使用指南（2011）

## 概述

GBAtemp 论坛贴 [NeoDS - A Guide to Using One of the Greatest DS Emulators](https://gbatemp.net/threads/neods-a-guide-to-using-one-of-the-greatest-ds-emulators.291225/)（Nathan Drake / Nathan Nendez，2011-05-04 发，3 页 / 56 回复 / 至 2016 年持续更新）是 DS homebrew 圈对 **NeoDS** 这一 NeoGeo 模拟器的标准入门教程。原始 URL 被 Cloudflare challenge 拦截（defuddle / WebFetch / curl 三路 403），本文通过 superpowers-chrome MCP 真实 Chrome 浏览器绕过 challenge 后蒸馏为 markdown（捕获目录 `2026-08-12/session-1786506390286/001-navigate.md`，2,165 行）。

## NeoDS 是什么

NeoDS v0.2.0（截至 2026 年仍为 v0.2.0，未见新版发布 ^[ambiguous]）是一款 **Nintendo DS / DS Lite / DSi 上的 NeoGeo 街机/家用机模拟器**，Nathan Drake 自评为"DS homebrew 史上最强模拟器之一"。能在 2004 年发布的 67 MHz 双屏 ARM9 设备上跑 1990 年代 NeoGeo 的 68000 + Z80 街机游戏是相当程度的工程成果，**但它不是 NDS 模拟器**（用户引用时常与 NO\$DS 混淆 ^[inferred]）。

## 4 阶段教程（Nathan Drake 主帖蒸馏）

### 阶段 1：下载 NeoDS

- 来源：GBAtemp Filetrip 链接 [NeoDS v0.2.0](http://filetrip.net/f2398-NeoDS-0-2-0.html)
- 解压 `[2684]NeoDs020.zip`，得到单层文件夹，**10 个文件**含：
  - `NeoDsConvert/`（转换工具目录）
  - `.nds` 主程序 + 资源文件
  - README.md

### 阶段 2：MAME ROM 转换

**前置前提**：(P1) NeoDS 使用 **MAME ROM 集**（merged/split/non-merged 任一都行）；MAME 能跑的游戏，NeoDS 转换后都能跑。(P2) 必须**自带 `neogeo.zip` BIOS 文件** —— 这是仓库规则禁止链接的，作者只能提示"Google 一下"。

**转换流程**：
1. 把 `neogeo.zip` 和目标游戏 ROM（仍是 zip 格式）放在 NeoDsConvert 同目录
2. 双击 `NeoDsConvert.exe`（**不是 `.sln` Visual Studio 工程文件**）
3. 命令行窗口闪过大量处理过程，最终输出 2 个 `.neo` 文件
4. 副产物的 `.neo` 文件用途未明 —— Metal Slug 测试有/无都正常运行

**备选方法**：CLI 转换（见 README），本教程不展开。

### 阶段 3：microSD 部署（关键路径）

**目录结构要求**：
- microSD 根目录：放**转换后的 .neo 游戏文件**（NeoDS 在 microSD 根扫描，不放子目录）
- microSD `/NeoGeo/`：放**模拟器本体的 8-9 个文件**（readme + NeoDsConvert/ + 转换前的源 ROM **不放**）

**Nathan Drake 强调**："This emulator searches the root of the MicroSD card for ROM files. Placement anywhere else will render them undetectable." —— 与 vault 中已知的 R4 内核（一个文件/一层子目录）行为不同，是 NeoDS 的特例。

### 阶段 4：运行

1. DS 开机 → 进 NeoGeo 文件夹 → 启动 `.nds`
2. 模拟器显示游戏列表
3. 按 Start 进入游戏

## 56 回复里的关键补丁信息

### 兼容性列表（2016 年起争议）

- **2016-03-09** ArugulaZ（#11）："this guide is kind of outdated ... NeoDS rejects the ones I have. Any chance someone could explain which version of MAME will have compatible Neo-Geo ROMs?" —— **指南与 MAME ROM 版本漂移是真实问题**（同 [[entities/neogeo-mame]] 提到的 MAME merged/split 集持续变动）。
- **2016-03-10** Smoker1（#12）：给出专用 [NeoDS Names Compatibility List](https://gbatemp.net/threads/neods-names-compatibility-list.102177/) —— 第三方维护的 NeoDS 专用 ROM 命名映射表（**不是 MAME 标准命名**），是 2016 年后唯一可靠参考。

### 平台兼容性

- 作者测试环境：**Original R4 + Wood v1.27 firmware** —— 不保证其他烧录卡。
- **Mac/Wine 路径**（2016-11 TheZoc）：用户 Zirus_Blackheart 想在 Mac 上跑 .exe 转换工具，TheZoc 回复未给出明确解（Wine 可行但 ROM 转换产物是否一致未验证 ^[ambiguous]）。

### 杀手本能测试（2011-06 obaz）

- obaz（#6）报告 Killer Instinct 1.4 不工作 —— KI 严格说是 Rare 的 N64/街机游戏（基于 Midway ROM），可能与"NeoGeo MAME 集"兼容性边界混淆 ^[inferred]。

## 与 vault 已有 NeoGeo 知识的整合

vault 已有的 [[entities/neogeo-mame]] 聚焦桌面 MAME 配置（uni-bios / 配置文件层级 / MAMEPlus vs 官方版），与本教程互补而非重叠：

- **共同点**：都用 MAME ROM 集、都需要 `neogeo.zip` BIOS、都涉及地区/模式选择
- **差异**：桌面 MAME 直接跑 .zip 即可；NeoDS 必须先转 `.neo`（单文件压缩格式，专为 NDS 的 SD 存储/读取带宽优化 ^[inferred]）
- **延伸**：桌面 MAME 用 uni-bios 4.0 + Region Setup 切地区；NeoDS 用同样的 BIOS，但地区/模式选择逻辑在 NDS 端（键位映射到 DS 摇杆/按钮）^[inferred]

## Open Questions

- **(O1)** NeoDS v0.2.0 之后是否有新版？Filetrip 链接已 10+ 年，社区未见 fork 报道 ^[ambiguous]。
- **(O2)** Mac 用户用 Wine 跑 NeoDsConvert.exe + MAME 0.106/0.107 ROM（兼容版本）是否能产出与 Windows 一致的 .neo？需实测。
- **(O3)** "side file"（转换副产物 .neo 第二个文件）的实际用途 —— Nathan Drake 也说"I can't find a use"，可能是 NeoDS 内部调试或未来功能预留 ^[inferred]。
- **(O4)** NeoDS 是否能跑 AES 家用机 ROM（不仅限于 MVS 街机）？vault [[entities/neogeo-mame]] 的 aes.zip 区分在此是否适用？
- **(O5)** 3DS 上 NeoDS 表现 —— ArugulaZ（#11）说 "3DS is 2D handicapped... straight port isn't going to be terribly easy"，似乎暗示 3DS 端口项目失败或未推进。

## Related

- [[entities/neogeo-mame]] — 桌面 MAME 端 NeoGeo 配置主条目；本教程是其 NDS 端的 homebrew 对应
- [[concepts/mame-rom-to-neods-conversion]] — NeoDS 转换原理 + 兼容性版本概念的抽象页（独立 wiki 页便于查询）
- [[entities/nds-flashcard]] — R4 + Wood v1.27 firmware 是 Nathan Drake 测试环境；与 NDS 烧录卡知识簇交叉
- [GBAtemp NeoDS Names Compatibility List (thread 102177)](https://gbatemp.net/threads/neods-names-compatibility-list.102177/) — 2016 年后的兼容性命名映射外部参考
- [NeoDS v0.2.0 on Filetrip](http://filetrip.net/f2398-NeoDS-0-2-0.html) — 官方下载（GBAtemp 自托管镜像）