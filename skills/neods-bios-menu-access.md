---
title: "NeoDS BIOS / Cheat 菜单访问"
category: skills
tags:
  - retro-gaming
  - nds
  - handheld
  - neogeo
  - emulator
  - keybinding
summary: "NeoDS v0.2.0 上进入 uni-bios 通用 BIOS 菜单（切地区/模式）与内置 cheat 菜单的键位组合：ROM 加载瞬间 A+B+X 触发 BIOS，游戏中 R+Start 触发 cheat，与桌面 MAME/NeoGeo 实体的 A+B+C 不同。"
sources:
  - "https://gbatemp.net/threads/help-wanted-how-to-access-the-bios-menu-of-neods-neogeo-for-ds.612585/"
created: 2026-08-12T12:55:00Z
updated: 2026-08-12T13:20:00Z
base_confidence: 0.55
lifecycle: draft
lifecycle_changed: "2026-08-12"
tier: supporting
provenance:
  extracted: 0.85
  inferred: 0.10
  ambiguous: 0.05
relationships:
  - target: "[[entities/neogeo-mame]]"
    type: extends
  - target: "[[concepts/mame-rom-to-neods-conversion]]"
    type: extends
  - target: "[[entities/nds-flashcard]]"
    type: related_to
  - target: "[[misc/web-gbatemp-net-threads-help-wanted-how-to-access-the-bios-menu-of-neods-neogeo-for-ds-612585]]"
    type: derived_from
  - target: "[[misc/web-gamebrew-org-wiki-neods]]"
    type: extends
---

# NeoDS BIOS / Cheat 菜单访问

## 前置条件

- 烧录卡上跑的 **NeoDS v0.2.0**（NDS / DS Lite / DSi 模拟器；非桌面 MAME）
- 目标游戏已用 `NeoDsConvert.exe` 转换过（含 uni-bios 嵌入）
- BIOS 是 uni-bios 系列（不是 SNK 原版 BIOS）

## 两个菜单的进入方式

| 菜单 | 时机 | 键位 | 来源 |
|------|------|------|------|
| **uni-bios 通用 BIOS 菜单** | ROM 加载瞬间（按 .nds 启动后、游戏画面出现前） | **`A + B + X` 三键同按** | GBAtemp 612585 POST 3 (DaRk_ViVi) + POST 5 (Nikokaro 验证) |
| **NeoDS 内置 cheat 菜单** | 游戏中 | **`R + Start` 同按** | GBAtemp 612585 POST 2 (Nikokaro 偶然发现) |

**注意**：`A+B+X` 是 **NDS 三键**，不是 NeoGeo 实体/桌面 MAME 用的 `A+B+C`（见下方对照表）。

## 为什么键位不一样

### NeoGeo 实体 / 桌面 MAME 的 A+B+C

NeoGeo 街机/家用机的 1P 摇杆只有 **A/B/C/D 四个动作键**（不是手柄上的 X/Y），开机瞬间按住 A+B+C（D 是记忆卡管理器）= uni-bios 菜单（vault [[entities/neogeo-mame]] 已详述）。

### NeoDS 的 A+B+X

NDS 手柄布局不同：

| NeoGeo 实体 / 桌面 MAME 键位 | NeoDS NDS 实际按键 | 备注 |
|------------------------------|--------------------|------|
| A | **NDS A** | 同 |
| B | **NDS B** | 同 |
| C | **NDS X** | NeoDS 用 X 替代 C（X 在 NDS 上位置更接近 NeoGeo C 键 ^[inferred]） |
| D | **NDS Y** | 同 |

**NeoDS 模拟器把 NeoGeo 的 C 键映射到 NDS 的 X 键**（不是 Y），所以 uni-bios 触发组合从 `A+B+C` 变成 `A+B+X`。这是 NeoDS 的输入层 remap 决策，详见 [[concepts/mame-rom-to-neods-conversion]] 的对照章节。

## 实操步骤（切地区 / 模式）

1. DS 开机 → 进 NeoDS 文件夹 → 启动 `.nds`
2. 模拟器显示游戏列表 → 选中目标游戏
3. **按住 A+B+X 三键** → 按 A 启动游戏
4. **保持按住** 直到 uni-bios 菜单出现（典型 1-2 秒）
5. 进入菜单后释放按键；用方向键 + A 选择，**按 C 退出菜单进入游戏**（C 在 NeoDS 上仍是 cheat/退出键）

### uni-bios 菜单里的关键项

- **Region Setup**：选地区（A=日 / B=美 / C=欧）
- **Mode**（如有）：A=Arcade 街机 / B=Console AES 家用机

切换后**直接生效**，无需重新转换 ROM（这是 uni-bios 优于 SNK 原版 BIOS 的点）。

## 实操步骤（启用 cheat）

1. 进游戏后任意时刻按 **`R + Start`**
2. NeoDS 内置 cheat 菜单弹出（与 uni-bios 菜单不同，是 NeoDS 自己的）
3. 选择金手指码 → 启用 / 关闭
4. 再按 **`R + Start`** 退出菜单

**注意**：vault [[concepts/mame-rom-to-neods-conversion]] 与 [[entities/nds-flashcard]] 的 [R4iSDHC](skills/r4isdhc-user-experience) 内核 cheat 菜单是**两套机制**（R4 用 B 键、NeoDS 用 R+Start）。

**R 键双功能叠加**（来自 [[misc/web-gamebrew-org-wiki-neods]] 2024-12-26 infobox Controls 表 + Nikokaro 612585 POST 2）：
- **单独按 R** = Select，新版 uni-bios 下 = **coin**（投币）
- **R + Start** = NeoDS 内置 cheat 菜单（Nikokaro 偶然发现，不在 gamebrew 官方 Controls 表）

gamebrew 2020 fork 没继承 R+Start cheat 菜单的官方文档化，说明这是社区后期发现（2022+ 时间线）。

## 与 NeoDS GameBrew 官方 Controls 表交叉验证

[[misc/web-gamebrew-org-wiki-neods]] 官方 Controls 表（2024-12-26 快照）：

| NDS 键 | NeoGeo 映射 | 备注 |
|--------|------------|------|
| D-Pad | 方向键 | |
| A/B/X/Y | A/B/C/D | |
| L | Pause | |
| R | Select（**新版 uni-bios = coin**） | **R+Start cheat 是社区叠加发现** |
| Start | Start | |
| Select | Coin | |
| Stylus | NeoDS GUI | |

**与本 skill 的差异**：gamebrew 官方只列单键，本 skill 加 R+Start / A+B+X（ROM 加载瞬间）等组合键 —— 这是社区（Nikokaro + 主教程作者）对官方键位表的补充。

## 常见踩坑

### 1. 按键时机不对

| 现象 | 原因 |
|------|------|
| 直接进游戏，没看到 BIOS 菜单 | 按 A+B+X 时机晚于游戏首帧（要在 .nds 启动后立即按住，不能等画面稳定）|
| 看到 BIOS 菜单但选完没生效 | 按键释放过早，整个加载期都要按住 |
| BIOS 菜单不出现 | ROM 是 SNK 原版 BIOS 转换（不是 uni-bios）—— 原版 BIOS 没有菜单，按键无效 |

### 2. 主机选择影响摇杆

- **DS Lite 优先**：D-pad 软硬适中，对角方向工作（格斗游戏必备）
- **DSi 摇杆太硬** + 对角失灵（vault [[misc/web-gbatemp-net-threads-help-wanted-how-to-access-the-bios-menu-of-neods-neogeo-for-ds-612585]] POST 2 Nikokaro 实测）—— 玩 KOF/MVS 类不要用 DSi

### 3. 不能跑 CPS2

NeoDS **只能跑 NeoGeo 游戏**（68000+Z80 街机/家用机），不能跑 CPS2（Capcom 街机）—— 想玩 Capcom vs SNK / Marvel vs Capcom 等需要其他模拟器（桌面 MAME 或街机 CPS2 homebrew）。

## 与桌面 MAME uni-bios 菜单的完整对照

| 功能 | 桌面 MAME | NeoDS (NDS) |
|------|-----------|-------------|
| 触发键 | `A+B+C`（NeoGeo 实体/桌面模拟器） | **`A+B+X`**（NDS 手柄 remap） |
| 时机 | splash 画面或 splash 禁用时启动瞬间 | ROM 加载瞬间（按 .nds 后到游戏首帧前）|
| 地区选择 | Region Setup → A/B/C | 同 |
| 模式选择 | A=Arcade / B=Console AES | 同 |
| 退出 | 按 C | 按 C |
| cheat 菜单 | START + A+B+C 或 START + COIN | **`R + Start`**（不同路径）|

## Open Questions

- (O1) `R + Start` cheat 菜单的 cheat 码来源 —— 是 NeoDS 内置通用码库还是读取 R4i 内核的 `usrcheat.dat`？vault 暂无资料 ^[ambiguous]
- (O2) 不同 uni-bios 版本（3.x / 4.0）的菜单键位是否完全一致？目前只看到 4.0 验证 ^[inferred]
- (O3) cheat 菜单是否每游戏都有内容？还是只对部分游戏预置 ^[ambiguous]

## Related

- [[entities/neogeo-mame]] — 桌面 MAME 端 uni-bios 菜单完整键位表（A+B+C 锚点）
- [[concepts/mame-rom-to-neods-conversion]] — NeoDS 输入层 remap 与 BIOS 嵌入机制
- [[entities/nds-flashcard]] — DS Lite / DSi 摇杆硬件差异 + R4i cheat 机制对照
- [[misc/web-gbatemp-net-threads-help-wanted-how-to-access-the-bios-menu-of-neods-neogeo-for-ds-612585]] — 本 skill 的事实来源