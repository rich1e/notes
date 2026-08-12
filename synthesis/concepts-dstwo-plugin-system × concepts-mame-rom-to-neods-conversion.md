---
title: dstwo-plugin-system × mame-rom-to-neods-conversion
category: synthesis
tags:
  - retro-gaming
  - nds
  - dstwo
  - neogeo
  - emulator
  - launcher-protocol
sources:
  - "[[concepts/dstwo-plugin-system]]"
  - "[[concepts/mame-rom-to-neods-conversion]]"
  - "[[entities/nds-flashcard]]"
  - "[[entities/neogeo-mame]]"
  - "[[skills/neods-bios-menu-access]]"
created: 2026-08-12T05:49:00Z
updated: 2026-08-12T05:49:00Z
summary: "在 DS 上玩 NeoGeo 有两条路径：通用路径（.neo 单文件 → microSD 根）和 DSTWO 专属路径（NeoDS.nds 做 plugin → /_dstwoplug/ 协议）—— 目标相同，部署架构完全不同。"
provenance:
  extracted: 0.30
  inferred: 0.60
  ambiguous: 0.10
base_confidence: 0.50
lifecycle: draft
lifecycle_changed: "2026-08-12"
---

# DSTWO Plugin 系统 × MAME ROM → NeoDS 转换

## 关联

这两个概念同时出现在：

- `entities/nds-flashcard`（DSTWO 同时涉及 plugin 协议和 NeoGeo 玩法）
- `concepts/mame-rom-to-neods-conversion`（明确提到"DSTWO 烧录卡用户走 plugin 旁路"）
- `misc/web-wiki-gbatemp-net-wiki-dstwo-plugin`（wiki 页列出 NeoDS 为 DSTWO 的 Emulators 分类 plugin）

## 跨框架洞见

**在 DS 上玩 NeoGeo 有两条路径，烧录卡型号决定你走哪条。** ^[inferred]

### 通用路径（适合所有烧录卡）

`概念/mame-rom-to-neods-conversion` 描述的路径：

```
MAME ROM(.zip) → NeoDsConvert.exe → .neo 单文件 → microSD 根目录 → NeoDS.nds 扫描读取
```

- **部署单位**：`.neo` 单文件（每个游戏独立，BIOS 内嵌）
- **目录结构**：严格要求 `.neo` 文件放在 microSD **根目录**（不支持子目录）
- **启动流程**：烧录卡菜单 → 运行 `NeoDS.nds` → 在 NeoDS 内部界面选游戏
- **适用**：R4、R4iSDHC、Cyclo DS 等所有支持 `.nds` 的标准烧录卡

### DSTWO 专属路径

`概念/dstwo-plugin-system` 描述的路径：

```
NeoDS.nds 改名 + BMP(16bit) + INI → /_dstwoplug/ 目录 → DSTWO firmware 菜单直接显示
```

- **部署单位**：3 文件 plugin 包（图标 + 配置 + 程序主体）
- **目录结构**：plugin 放 `/_dstwoplug/`，`.neo` 游戏文件**仍需在 microSD 根**
- **启动流程**：DSTWO 主菜单直接显示 NeoDS 图标（无需先进入 NeoDS 再选游戏）
- **适用**：仅限 SuperCard DSTWO 及其衍生型号

### 关键差异

| 维度 | 通用路径 | DSTWO plugin 路径 |
|---|---|---|
| 菜单层级 | 烧录卡菜单 → NeoDS 主界面 | 烧录卡主菜单直接显示（少一层） |
| plugin 维护 | 无需额外文件 | 需维护 BMP + INI + .nds 三件套 |
| `.neo` 文件位置 | microSD 根 | microSD 根（同，DSTWO 没有改变这一要求） |
| 烧录卡要求 | 通用 | DSTWO 专属 |
| 安装复杂度 | 只需 `NeoDsConvert.exe` 转换 | 额外需制作 16bit BMP（40×42px）+ INI |

**第二个洞见：DSTWO plugin 路径并不能绕开 `.neo` 转换步骤。** ^[extracted]

两条路径的共同前提都是：先把 MAME ROM 转换为 `.neo` 单文件，然后放在 microSD 根目录。DSTWO plugin 路径只改变了"如何启动 NeoDS.nds"（直接从主菜单还是先进入文件浏览器），而不改变 ROM 转换和存放位置。这一点在 `concepts/mame-rom-to-neods-conversion` 的"vault 整合点"注中明确说明，但容易被误解为"用 plugin 就不需要转换"。

## 张力与权衡

- **维护成本**：DSTWO plugin 路径需要制作 16bit 限制的 BMP 图标，工具链比通用路径多一步，且 16bit BMP 的约束来自 DS 硬件的 GBA slot 渲染管线，不可绕过 ^[extracted]。
- **迁移成本**：如果已经按通用路径把 `.neo` 文件放好，切换到 plugin 路径只需要额外放 3 个文件，`.neo` 不用动 —— 两条路径可以共存。
- **DSTWO 接触不良干扰**：`concepts/dstwo-contact-fix` 记录了 DSTWO 金手指接触问题。如果烧录卡本身不能稳定识别，plugin 路径比通用路径更脆弱（更多依赖 DSTWO 固件的正常运行，而通用路径只需要 `.nds` 可执行）。

## 最强质疑

**DSTWO plugin 路径真的有实质优势，还是只是"能做"而非"值得做"？** 质疑：唯一的用户体验差异是"少一个菜单层级"——从 DSTWO 主菜单直接点 NeoDS 图标 vs 先进 NeoDS.nds 文件再选。而为此需要制作 16bit BMP 图标、维护 INI 配置文件，且 `.neo` 游戏文件仍然要放在根目录。实际操作中，玩 NeoGeo 游戏的频率可能不足以让"少一层菜单"成为显著优化。

> **test：** 找一个 DSTWO 用户，用计时器测两条路径"从开机到进入第一局游戏"的耗时差异。如果 plugin 路径不能节省超过 5 秒，则证明优化价值有限。

## 未解问题

1. DSTWO plugin 协议是否支持把 `.neo` 文件放在 plugin 目录内（`/_dstwoplug/`），而不是 microSD 根？还是说 NeoDS 本身的扫描逻辑硬编码只读根目录？
2. 社区 fork（nitendo 的 0.2.1.b）是否修改了目录扫描逻辑，支持子目录？
3. `Yardape8000/NeoDS` GitHub fork 与 DSTWO plugin 协议的兼容性如何？

## Related

- [[concepts/dstwo-plugin-system]] — DSTWO 3 文件 plugin 协议详解
- [[concepts/mame-rom-to-neods-conversion]] — 通用路径详解（转换原理 + 命名兼容性 + Fork 链）
- [[entities/nds-flashcard]] — 两条路径的硬件背景（DSTWO vs R4）
- [[entities/neogeo-mame]] — 桌面 MAME 端 NeoGeo 配置，与 NeoDS 移植端对照
- [[skills/neods-bios-menu-access]] — 两条路径都需要的 uni-bios 键位技巧
- [[concepts/dstwo-contact-fix]] — DSTWO 接触不良修复（前提：DSTWO 必须先稳定工作）
