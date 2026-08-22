---
title: MAME ROM → NeoDS 转换
category: concepts
tags:
  - retro-gaming
  - neogeo
  - nds
  - emulator
  - rom-conversion
sources:
  - "https://gbatemp.net/threads/neods-a-guide-to-using-one-of-the-greatest-ds-emulators.291225/"
  - "https://gbatemp.net/threads/neods-names-compatibility-list.102177/"
created: 2026-08-12T03:55:00Z
updated: 2026-08-12T13:20:00Z
summary: "NeoDS 模拟器把 MAME 街机 ROM 集转换为 NDS 可读的 .neo 单文件格式：原理、BIOS 嵌入机制（每个 .neo 自带 BIOS）、uni-bios 菜单键位 remap（A+B+X vs 桌面 MAME 的 A+B+C）、命名兼容性陷阱与部署目录结构 + Fork 链(0.2.0 主线 → 0.21.b 社区现行版) + DSTWO 烧录卡用户走 plugin 协议的旁路"
base_confidence: 0.50
lifecycle: draft
lifecycle_changed: "2026-08-12"
tier: supporting
provenance:
  extracted: 0.65
  inferred: 0.28
  ambiguous: 0.07
relationships:
  - target: "[[entities/neogeo-mame]]"
    type: extends
  - target: "[[entities/nds-flashcard]]"
    type: related_to
  - target: "[[misc/web-gbatemp-net-threads-neods-a-guide-to-using-one-of-the-greatest-ds-emulators-291225]]"
    type: derived_from
  - target: "[[skills/neods-bios-menu-access]]"
    type: related_to
  - target: "[[misc/web-gbatemp-net-threads-help-wanted-how-to-access-the-bios-menu-of-neods-neogeo-for-ds-612585]]"
    type: derived_from
  - target: "[[concepts/dstwo-plugin-system]]"
    type: related_to
---

# MAME ROM → NeoDS 转换

## 概念

NeoDS（v0.2.0，DS homebrew）**不直接吃 MAME ROM**——它需要先把 MAME 多文件街机 ROM 集（split/merged/non-merged）打包成 NDS 端易于单次读取的 `.neo` 单文件格式。这是 NDS 存储/带宽限制下的工程取舍，与桌面 MAME 直接跑 zip 完全不同。

## 转换原理

### 输入：MAME ROM 三种集格式

桌面 MAME 用三种格式打包 NeoGeo 游戏（vault [[entities/neogeo-mame]] 已记录）：

- **merged** —— 所有依赖文件已合并到游戏 zip，体积大但单一文件
- **split** —— 父子文件分开，最新版 MAME 默认
- **non-merged** —— 每个游戏完全独立

**NeoDS 兼容任一格式**（Nathan Drake 原帖："Any game that works with MAME will work with NeoDS after conversion"），但**实际**只接受其官方兼容性列表（[NeoDS Names Compatibility List](https://gbatemp.net/threads/neods-names-compatibility-list.102177/)）里命名的版本 ^[ambiguous]。这意味着 MAME 最新版 ROM 集可能 reject（2016 年 ArugulaZ 的核心痛点）。

### 输出：.neo 单文件

`NeoDsConvert.exe` 处理流程（推断 ^[inferred]，因源代码未公开）：
1. 解压输入 `.zip`
2. 提取 NeoGeo BIOS 必需的 P-ROM（68K 程序）和 S-ROM（字库）数据
3. 重打包成 NDS 友好格式（合并连续数据块、裁剪未用区域）
4. 输出 2 个 `.neo`：1 主游戏 + 1 副产物（用途未明，原作者也说"找不到用"）

## 必依赖：`neogeo.zip` BIOS

转换必须**自带 `neogeo.zip`**（NeoGeo BIOS 文件集），没有它无法启动转换流程。这是：
- 仓库规则禁止链接的版权文件（BIOS 著作权属 SNK）
- 与桌面 MAME 通用（[[entities/neogeo-mame]] 的 BIOS 章节）
- 不同 BIOS 版本影响地区/模式选择（日版/美版/欧版/uni-bios）

### BIOS 嵌入机制（GBAtemp 612585 Nikokaro 关键澄清）

NeoDS 与桌面 MAME 在 BIOS 处理上**根本不同**：

| 维度 | 桌面 MAME | NeoDS |
|------|-----------|-------|
| BIOS 文件位置 | `neogeo.zip` 独立放 ROM 目录 | **嵌入到每个 .neo 游戏文件**里 |
| 切换 BIOS 版本 | 替换 `neogeo.zip` 即可 | **重新转换所有 ROM** |
| 校验 BIOS | 自动读 .zip | NeoDsConvert 转换时一次写入 |
| 用户手动配置 | MAME config (`bios unibios40`) | 无（每个游戏自带）|

Nikokaro 原话：*"NG BIOS has to be inserted into the neo geo game you are interested in at the time of conversion, and the tool to do this only works on Windows. There's no other way."*

**工程后果**：没有"放个 BIOS 到 microSD 根目录"这种 NeoDS 配置；这是 NDS 端 4MB RAM + 单文件读取限制下的工程取舍。

### NeoDS 端 uni-bios 菜单触发（与桌面 MAME 键位 remap）

NeoDS 模拟器把 NeoGeo 街机的 C 键 remap 到 NDS 的 X 键，所以触发 uni-bios 通用 BIOS 菜单的组合从 `A+B+C`（NeoGeo 实体/桌面 MAME）变成 **`A+B+X`**（ROM 加载瞬间按住）。详细操作见 [[skills/neods-bios-menu-access]]。

| 菜单 | 桌面 MAME | NeoDS |
|------|-----------|-------|
| uni-bios 通用菜单 | `A+B+C` 启动瞬间 | **`A+B+X`** ROM 加载瞬间 |
| cheat 菜单 | `START+A+B+C` | `R+Start`（游戏中） |

**为什么 remap**：NeoGeo 街机的 1P 摇杆只有 4 个动作键 A/B/C/D（不是手柄 X/Y）；NDS 手柄布局为 A/B/X/Y，NeoDS 选择把 C→X（位置更接近 ^[inferred]）。

## 部署目录结构（关键陷阱）

NeoDS 与 [R4iSDHC](skills/r4isdhc-user-experience) 等普通 NDS 烧录卡（[[entities/nds-flashcard]]）的目录行为**相反**：

| 项目 | R4iSDHC 内核 | NeoDS |
|------|--------------|-------|
| 游戏 ROM | microSD 根目录或一层子目录（见 [skills/r4isdhc-user-experience](skills/r4isdhc-user-experience)） | **仅 microSD 根目录** ^[inferred 验证：Nathan Drake 原帖明确]"This emulator searches the root of the MicroSD card for ROM files. Placement anywhere else will render them undetectable" |
| 模拟器本体 | microSD 根目录 | microSD `/NeoGeo/` 文件夹 |
| 子目录扫描 | 一层递归 | 不递归游戏 |

这意味着 NeoDS 与同一 microSD 上其他模拟器（如 SNEmulDS / lolDS / jEnesisDS）共存时要小心，**根目录污染**。

## 兼容性陷阱与版本漂移

### MAME ROM 版本漂移

MAME 持续重命名/重组 ROM（"ROM rename" 是 MAME 团队的持续 PR）。NeoDS 0.2.0 发布于 2008 年 ^[inferred]，此后**未跟进 MAME 的命名变更**，导致：
- 2016 年用户 ArugulaZ 反馈所有"现代" MAME ROM 都 reject
- Smoker1 提供第三方 [NeoDS Names Compatibility List](https://gbatemp.net/threads/neods-names-compatibility-list.102177/) 作为唯一可靠参考

### 推荐策略

1. **优先用 GBAtemp 第三方命名映射表**（thread 102177）选对应 NeoDS 命名
2. **保留老版 MAME ROM 集**（如 MAME 0.106 ~ 0.120 是 NeoDS 时代主流）
3. **不要直接用最新版 MAME ROM 集** —— 大概率 rename 错过

## 与桌面 MAME 的功能差异

| 功能 | 桌面 MAME | NeoDS |
|------|-----------|-------|
| 直接读 .zip | ✓ | ✗（必须转换） |
| uni-bios 4.0 菜单 | ✓ | △（BIOS 相同，菜单键映射到 DS 按钮 ^[inferred]） |
| AES/MVS 切换 | uni-bios Region Setup | 同 BIOS，模式由 game.ini 等决定 ^[ambiguous] |
| 联网对战 | 多数 NeoGeo 游戏支持 | ✗（NDS 端无网络栈 ^[inferred]） |
| 存档位置 | per-game statename | 取决于 microSD 布局 |

## 工具链

- **NeoDsConvert.exe** —— 唯一官方转换工具（Windows）；CLI 备选见 README
- **MAME 0.106 ~ 0.120** ROM 集 —— 历史兼容窗口（具体版本需查 thread 102177 列表）
- **neogeo.zip** —— BIOS 文件（不链接，需自备）
- **DLDI patch** —— NeoDS.nds 需用 [DLDI](https://www.gamebrew.org/wiki/DLDI) 工具 patch（不是所有烧录卡都需要，但通用步骤；见 [[misc/web-gamebrew-org-wiki-neods]] Installation 段）

## NeoDS 版本与 Fork 链（gamebrew 2024-12 权威修正）

vault 之前所有 wiki 页都说"NeoDS v0.2.0（2008-06-19）"，**不准确**。GameBrew 权威 infobox 显示当前实际版本链（[[misc/web-gamebrew-org-wiki-neods]]）：

| 版本 | 作者 | 日期 | 状态 |
|------|------|------|------|
| 0.1.0 | Ben Ingram (Ingramb) | 2008-04-29 | 初始发布 |
| 0.1.1 / 0.1.1a | Ingramb | 2008-05-06 | Bug 修复 |
| **0.2.0** | Ingramb | 2008-06-19 | 主线最终版本 |
| **0.21** | nitendo | (2010+) | ROM 菜单 64→256；Left/Right = pageUp/pageDown；配置目录 `fat:/data/neoDS/`；`_NeoDs.ini` 控制独立子目录 |
| **0.21.b** | nitendo | 2020-08-26 | 当前最新；0.21b_scaled 默认 scaled 全屏 |
| **0.21 mod** | indy13 | (2010+) | 改 ROM 路径 + 法/英 readme |
| **EZ flash 3in1 版** | j03lpr86 | (2010+) | EZ Flash 3in1 卡带兼容 |
| **TWL 版** | Universal-Team | (2020+) | 整合到 Twilight Menu++ |
| **GBMacro** | xonn83 | (wip) | GameBoy Macro(NDS Lite 改 GBA 形态)用 |
| **Yardape8000 fork** | 社区 | (current) | GitHub 仓库 https://github.com/Yardape8000/NeoDS |

**关键修正**:
- **Ingramb 主线 0.2.0** 自 2008-06 未更新(这就是 vault 之前说"NeoDS v0.2.0 未跟进 MAME ROM 重命名"的真实含义)
- **nitendo fork 0.21 / 0.21.b** 持续维护到 2020-08-26,是社区**实际可用版本**
- **DLDI patch 步骤**是 gamebrew 显式列出但 GBAtemp 主帖没说
- Indy13 同时是 vault [[misc/web-gbatemp-net-threads-dstwo-not-making-proper-contact-with-my-ds-lite-634036]] DSTWO 接触不良主贴贡献者之一 —— 社区活跃 homebrew 玩家跨项目
- Indy13 0.21 mod 提供法/英 readme —— 体现 NDS homebrew 社区跨语言协作

## NeoDS 同时也是 DSTWO 烧录卡 plugin 之一

GBAtemp WikiTemp 的 DSTwo Plugin 索引页（2025-03-20 快照，[[misc/web-wiki-gbatemp-net-wiki-dstwo-plugin]]）明确把 NeoDS 列入 Emulators 分类。这意味着 **DSTWO 用户可绕开本概念页描述的"先转 .neo 单文件 → microSD 根"流程** —— 直接用 DSTWO 烧录卡的 plugin 协议（vault [[concepts/dstwo-plugin-system]]）：microSD `/_dstwoplug/` 目录放 BMP + INI + NeoDS.nds 三件套，由 DSTWO 菜单扫描显示。

**两条路径对比**：

| 路径 | DSTWO 烧录卡用户 | R4 / 普通烧录卡用户 |
|------|-----------------|---------------------|
| NeoDS 部署方式 | DSTWO plugin（3 文件协议）| .neo 单文件（microSD 根）|
| 步骤 | 解压 zip → 3 文件复制到 `/_dstwoplug/` | NeoDsConvert.exe 转 → 复制 .neo 到根 |
| 目录陷阱 | `/_dstwoplug/` 固定目录 | microSD 根（不放子目录）|
| 图标 | 16bit BMP 40x42（plugin 协议强制）| 无（纯文件名列表）|

**vault 整合点**：本概念页聚焦 .neo 单文件流程；DSTWO plugin 部署走 [[concepts/dstwo-plugin-system]] 的协议规范。

## Open Questions

- NeoDS 是否在 2026 年仍有维护？Filetrip 链接活跃但无版本号变更
- Mac/Wine 路径下 NeoDsConvert.exe 输出是否 byte-identical
- 副产物 `.neo` 文件实际用途

## 相关页面

- [[entities/neogeo-mame]] — 桌面 MAME 端 NeoGeo 配置主条目（BIOS/配置文件层级/MAMEPlus 对比）
- [[entities/nds-flashcard]] — NDS 烧录卡知识簇（R4 Wood v1.27 是 NeoDS 测试环境）
- [[misc/web-gbatemp-net-threads-neods-a-guide-to-using-one-of-the-greatest-ds-emulators-291225]] — 本概念的事实来源（Nathan Drake 主贴）

## Related

- [[entities/neogeo-mame]] — vault 中所有 NeoGeo 知识的桌面 MAME 锚点
- [NeoDS Names Compatibility List (GBAtemp thread 102177)](https://gbatemp.net/threads/neods-names-compatibility-list.102177/) — 2016 年后唯一可靠的兼容性命名映射
- [[synthesis/concepts-dstwo-plugin-system × concepts-mame-rom-to-neods-conversion]] — synthesis：DSTWO plugin 路径 vs 通用 .neo 路径，在 DS 上玩 NeoGeo 的两条方案对比