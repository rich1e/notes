---
title: "DSTwo Plugin 系统（3 文件协议）"
category: concepts
tags:
  - retro-gaming
  - nds
  - dstwo
  - emulator
  - launcher-protocol
summary: "SuperCard DSTWO 烧录卡的 plugin 启动协议：3 个同名文件 (16bit BMP 40x42 + INI + .nds/.plg) 放 microSD /_dstwoplug/ 目录，由 DSTWO 菜单扫描显示。完整故障模式分类与文件名一致性约束。"
sources:
  - "https://wiki.gbatemp.net/wiki/DSTwo_Plugin"
created: 2026-08-12T13:15:00Z
updated: 2026-08-12T13:15:00Z
base_confidence: 0.55
lifecycle: draft
lifecycle_changed: "2026-08-12"
tier: supporting
provenance:
  extracted: 0.82
  inferred: 0.13
  ambiguous: 0.05
relationships:
  - target: "[[entities/nds-flashcard]]"
    type: extends
  - target: "[[concepts/dstwo-contact-fix]]"
    type: related_to
  - target: "[[concepts/mame-rom-to-neods-conversion]]"
    type: related_to
  - target: "[[misc/web-wiki-gbatemp-net-wiki-dstwo-plugin]]"
    type: derived_from
---

# DSTTwo Plugin 系统(3 文件协议)

## 概念

**DSTWO Plugin 协议**是 SuperCard DSTWO 烧录卡的"microSD 内嵌 launcher 协议"——烧录卡 firmware 扫描 microSD 根下一个固定目录 `/_dstwoplug/`,读里面的"3 个同名文件"(图标 + 配置 + 程序),在主菜单显示为带图标的 launcher 入口。这与 R4 内核的"扁平 .nds 扫描"(vault [[entities/nds-flashcard]])或 NeoDS 的"microSD 根 .neo 单文件"(vault [[concepts/mame-rom-to-neods-conversion]])都不同,是 DSTWO 独有的"应用市场"模式。

## 3 文件协议

每个 plugin 必须在 microSD 的 `/_dstwoplug/` 目录下放置 **3 个同名**(basename 一致,扩展名不同)文件:

| 文件 | 扩展名 | 格式约束 | 作用 |
|------|--------|---------|------|
| **图标** | `.bmp` | **16bit 色深 BMP,40×42 像素** | DSTWO 菜单显示的 launcher 入口图 |
| **配置** | `.ini` | 3 行文本(2 行实际使用) | 第 1 行 = Display Name;第 2 行 = 图标 graphic 路径声明 |
| **程序** | `.nds` 或 `.plg` | DS homebrew binary | `.nds` = 通用 DS homebrew;`.plg` = 专为 DSTWO 额外 CPU/Memory 优化的程序 |

**关键约束**:**3 文件 basename 必须完全一致**。例:

```
/_dstwoplug/
├── NeoDS.bmp          ← 图标(16bit, 40x42)
├── NeoDS.ini          ← 配置(Display Name + 图标路径)
└── NeoDS.nds          ← 程序
```

任何命名错位 → plugin 不显示或显示为 3 种已知故障之一(见下)。

## 16bit BMP 约束的硬件根因

DS 的 GBA slot 渲染管线只支持 **16bit 色深**(RGB565 = 65536 色),无法直接渲染 24bit 或 32bit BMP。这是硬件决定,不是软件偏好 ^[inferred]。所以 DSTWO 的 plugin 图标必须用 16bit BMP,否则菜单跳过/报错。

**自制 icon 工具链**(wiki 列出):
- Icon Templates for Slot-1 and Slot-2
- 16-bit converting Tool by spinal_cord

## 安装流程

1. 从 wiki 或 GBAtemp 帖 `t229551` 下载 plugin 的 `.zip`
2. 解压到临时目录,通常包含 BMP/INI/NDS 三件套(可能带额外子目录)
3. 把 BMP + INI 复制到 `/_dstwoplug/`
4. 把 NDS(或 PLG)复制到 `/_dstwoplug/`
5. **手动确保 NDS 与 INI 文件名一致**(若 zip 内 NDS 命名错误,必须重命名)
6. 部分 homebrew 需要额外文件夹(读 README.txt)
7. 重启 DSTWO 主菜单 → 新 plugin 应出现在 launcher 列表

## 3 种已知故障模式

| 故障显示 | 根因 | 修复 |
|---------|------|------|
| **No 'INI'** | ini 文件缺失 / 与 NDS 不同名 | 检查 zip 内容,确保 3 文件同名 |
| **NOT 16bit** | bmp 不是 16bit 色深 | 用 spinal_cord 的转换工具重新导出 16bit BMP |
| **No 'BMP'** | bmp 文件缺失 / 与 INI 声明的图标路径不同名 | 检查 INI 第 2 行的图标路径,与实际 bmp 文件名一致 |

## 协议对比:DSTWO vs 其他 NDS 烧录卡

| 维度 | R4 内核 | NeoDS | DSTWO Plugin |
|------|---------|-------|--------------|
| 扫描入口 | microSD 根或一层子目录 | microSD 根(只扫根) | 固定目录 `/_dstwoplug/` |
| 文件类型 | `.nds` 单文件 | `.neo` 单文件(转换后) | `.bmp + .ini + .nds/.plg` 三件套 |
| 命名一致性 | 自由 | 自由 | **3 文件 basename 必须完全一致** |
| 图标 | 无(纯文件名列表) | 无 | 16bit BMP 40x42 强制 |
| 菜单显示 | 文本列表 | 文本列表 | 图标列表(类应用市场) |
| 额外资源 | 无 | 无 | 部分 plugin 需额外文件夹/文件 |

**DSTWO 是唯一带"应用市场风格 launcher"的 NDS 烧录卡** —— 是它价格高(R4 约 ¥40,DSTWO 高于 R4 数倍,vault [[entities/nds-flashcard]] 提到的"DSTWO 体验最好")的核心功能溢价来源。

## .plg vs .nds

- **`.nds`** = 标准 NDS homebrew,在 DS 自身硬件上跑
- **`.plg`** = DSTWO 特制程序,利用 DSTWO 内置的**额外 CPU/Memory** —— 这是 DSTWO 比其他烧录卡"更高级"的工程体现

**典型 .plg 应用**:官方 GBA 模拟器、官方 SNES 模拟器、利用 DSTWO 协处理器的多媒体解码等。

## 已知 plugin 生态(2025-03-20 wiki 快照)

详见 [[misc/web-wiki-gbatemp-net-wiki-dstwo-plugin]] 主页蒸馏。100+ 个 plugin 跨 4 类(Emulators 28 / Utilities 20+ / Multimedia 25+ / Games 30+),展示 2006~2013 NDS homebrew 长尾社区。

## Open Questions

- **(O1)** DSTWO 菜单的 plugin 扫描是否限制单层目录?子目录是否支持?
- **(O2)** 16bit BMP 之外的图标格式(PNG/Icon)是否在固件升级后支持?
- **(O3)** supercard 官方域名(supercard.sc)在 2018 重组后是否还能访问?
- **(O4)** 100+ plugin 中,2026 年实测能跑的比例?硬件/firmware 兼容性?

## Related

- [[entities/nds-flashcard]] — DSTWO 是 vault 中"最高级烧录卡"的核心事实来源
- [[concepts/dstwo-contact-fix]] — DSTWO 接触不良 4 路径修复(同烧录卡不同问题)
- [[concepts/mame-rom-to-neods-conversion]] — NeoDS 是 DSTWO plugin 列表中的具体一项
- [[misc/web-gbatemp-net-threads-dstwo-not-making-proper-contact-with-my-ds-lite-634036]] — DSTWO 接触不良主贴蒸馏
- [[misc/web-wiki-gbatemp-net-wiki-dstwo-plugin]] — 本概念的事实来源(wiki 主页蒸馏)
- [[synthesis/concepts-dstwo-plugin-system × concepts-mame-rom-to-neods-conversion]] — synthesis：DSTWO plugin 路径 vs 通用 .neo 路径，在 DS 上玩 NeoGeo 的两条方案对比