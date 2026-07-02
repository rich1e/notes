---
title: NEOGEO / MAME 模拟器配置
category: entities
tags:
  - game
  - retro-gaming
summary: MAME 模拟器中运行 NEOGEO 街机及 AES 家用机游戏的配置要点，包括 BIOS、ROM 管理与存档设置。
sources:
  - https://jjui.readthedocs.io/mame/mame_configure/neogeo.html
created: 2026-06-29
updated: 2026-06-29
tier: supporting
lifecycle: draft
lifecycle_changed: "2026-06-29"
base_confidence: 0.50
provenance:
  extracted: 0.85
  inferred: 0.10
  ambiguous: 0.05
relationships:
  - target: "[[entities/nds-flashcard]]"
    type: related_to
---

# NEOGEO / MAME 模拟器配置

## NEOGEO 平台概览

NEOGEO 是 SNK 开发的街机/家用游戏平台，代表作：
- 拳皇系列（KOF）
- 合金弹头系列（Metal Slug）
- 侍魂系列（Samurai Shodown）
- 月华剑士系列
- 双截龙格斗

在 MAME 0.260 中，这类游戏源码分类为 `neogeo/neogeo.cpp`。

## MAME 中的 NEOGEO 类型

### 街机版（neogeo）
标准街机 ROM，需要 `neogeo.zip`（BIOS）。

### AES 家用机版
- 额外需要 `aes.zip`
- 与街机版大量 ROM 重复，几乎不需要单独下载
- 部分游戏有差异（AES 版往往有额外模式）：
  - KOF97：VS 对战模式更方便
  - KOF98：有练习模式

在 MAME 游戏列表中找到 `Neo-Geo AES (NTSC)`（缩写 `aes`），进入子游戏列表即可选择具体游戏。

## BIOS 版本

NEOGEO 通常有多个 BIOS 版本：
- 欧版、美版、亚洲版、日版
- **uni-bios 加强版**：第三方增强版，功能最丰富（推荐）

## ROM 管理

MAME 使用 merged/split/non-merged 三种 ROM 集格式，NEOGEO 游戏通常依赖 `neogeo.zip` 作为父集。

## 存档注意事项

家用机游戏若使用模拟器存档功能，需设置独立存档位置，否则同一机型所有游戏共用同一存档槽——容易互相覆盖。查看 MAME 说明文件中的 `statename` 选项进行配置。

## 相关页面

- [[entities/nds-flashcard]] — NDS 烧录卡，同为复古游戏主题
