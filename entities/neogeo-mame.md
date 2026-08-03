---
title: NEOGEO / MAME 模拟器配置
category: entities
tags:
  - game
  - retro-gaming
summary: MAME 模拟器中运行 NEOGEO 街机及 AES 家用机游戏的配置要点，包括 BIOS、ROM 管理、uni-bios 菜单按键组合、地区与模式选择以及配置文件层级。
sources:
  - https://jjui.readthedocs.io/mame/mame_configure/neogeo.html
created: 2026-06-29
updated: 2026-07-25
lifecycle_changed: "2026-07-25"
tier: peripheral
lifecycle: draft
base_confidence: 0.50
provenance:
  extracted: 0.85
  inferred: 0.10
  ambiguous: 0.05
relationships:
  - target: "[[entities/nds-flashcard]]"
  - target: "[[journal/nds-flashcard-memories]]"
    type: related_to
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

### 地区与模式选择（uni-bios 4.0 菜单）

启动画面（splash screen）显示时，或 splash 禁用时启动瞬间按住组合键，玩家 1 的 1up 控制器：

| 组合键 | 功能 |
|--------|------|
| **A + B + C** | UNIVERSE BIOS 菜单 |
| **A + B + C + D** | 记忆卡管理器（Memory Card Manager） |
| **B + C + D** | 测试模式（仅 MVS 街机） / 硬件测试（仅 AES 家用机） |

> 注：B+C+D 在街机和家用机表现不同——街机为 Test Mode，家用机为 Hardware Test。

玩家 2（2up 控制器）：
- **A + B + C + D** → 控制器测试（仅 AES）

进入 uni-bios 4.0 菜单后选 **Region Setup**（地区设置），下一层：
- **Region 地区**：A = 日 / B = 美 / C = 欧
- **Mode 模式**：A = Arcade 街机 / B = Console AES 家用机

选完后回到主菜单，按 **C** 退出菜单进入游戏。

### 游戏内菜单按键

游戏中（如未在 bios 常规设置中禁用）：

| 组合键 | 功能 |
|--------|------|
| **START + SELECT** | 游戏内菜单 |
| **START + COIN** | 游戏内菜单 |
| **START + A + B + C** | 游戏内菜单 |

进入后按 **C** 退出菜单。菜单第一项是**作弊功能**（与 MAME 自带作弊码可对比）。

### 不同 BIOS 的体验差异

- **日版 bios**：游戏中日语元素更多（侍魂、月华剑士等），适合懂日语的玩家；日语中常用汉字，汉字元素多的游戏即便不懂日语也赏心悦目
- **美版 bios**：kof97 街机默认 bios 不方便一开始就在玩家 2 方向玩；用美版 bios kof97 玩家 2 单独投币可一开始就在玩家 2 方向玩
- **街机 vs AES bios 选择数量**：街机可选 bios 版本多一些；家用机 AES 可选 bios 少一些

## uni-bios 来源与使用

- 官方说明：[http://unibios.free.fr/](http://unibios.free.fr/) 和 [http://unibios.free.fr/howitworks.html](http://unibios.free.fr/howitworks.html)
- UNIVERSE BIOS 是原始 SNK BIOS 的修补版本（patched），多数代码与原 BIOS 相同，只是把新代码嵌入进去

## 配置文件层级（kof97.ini / neogeo.ini / mame.ini）

**不要把 BIOS 等选项设置到全局配置文件 mame.ini**，因为不同游戏的最优值可能不同。

查询可用 BIOS 名称：
```bash
mame.exe kof97 -listbios      # 推荐（新版支持）
mame.exe kof97 -listxml       # 内容太多
```

配置层级（**优先级从高到低**，越具体覆盖越通用）：

| 配置文件 | 作用域 | 用途 |
|----------|--------|------|
| `<game>.ini`（如 `kof97.ini`） | 单个游戏 | 最具体，单独游戏覆盖 |
| `neogeo.ini` | 同 BIOS 类型的所有游戏 | 按 BIOS 类型聚合 |
| `mame.ini` | 全局 | 默认值兜底 |

**实践要点**：
- 配置文件中 `bios` 项默认未设置
- 在 `kof97.ini` 中设置示例：`bios unibios40`
- 注意：**仅保留与上层不同的选项**。比如 `neogeo.ini` 中只设了 `bios`，其它 `mame.ini` 同名选项全删，仅保留此项

### MamePlus vs 官方原版 MAME

- **官方原版 MAME**：没有家用机 bios（家用机 AES 需单独 `aes.zip`，并用 uni-bios 切换到 AES）
- **MamePlus**：bios 中既有 uni-bios 也有家用机 bios
  - 早期 MamePlus：家用机 bios 无 bug，两个都能用
  - 后期 MamePlus：家用机 bios 有 bug（**游戏没有声音**），遇到此 bug 改用 uni-bios 切换到 AES

## ROM 管理

MAME 使用 merged/split/non-merged 三种 ROM 集格式，NEOGEO 游戏通常依赖 `neogeo.zip` 作为父集。

## 存档注意事项

家用机游戏若使用模拟器存档功能，需设置独立存档位置，否则同一机型所有游戏共用同一存档槽——容易互相覆盖。查看 MAME 说明文件中的 `statename` 选项进行配置。

## 相关页面

- [[entities/nds-flashcard]] — NDS 烧录卡，同为复古游戏主题

## Related

- [[journal/nds-flashcard-memories]] — NDS 世代烧录卡回忆录
