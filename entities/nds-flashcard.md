---
title: NDS 烧录卡（R4 / DSTWO）
category: entities
tags:
  - game
  - retro-gaming
  - nds
  - handheld
summary: Nintendo DS/NDSL 烧录卡使用指南：R4iSDHC 内核下载、TF 卡格式化、ROM 管理及多媒体功能。
sources:
  - https://www.cnblogs.com/mcxw/p/16347794.html
  - https://segmentfault.com/a/1190000021857936
created: 2026-06-29
updated: 2026-06-29
tier: supporting
lifecycle: draft
lifecycle_changed: "2026-06-29"
base_confidence: 0.50
provenance:
  extracted: 0.80
  inferred: 0.15
  ambiguous: 0.05
relationships:
  - target: "[[entities/neogeo-mame]]"
  - target: "[[journal/nds-flashcard-memories]]"
    type: related_to
    type: related_to
---

# NDS 烧录卡（R4 / DSTWO）

## 所需材料

- NDS/NDSL/3DS 掌机
- R4iSDHC 烧录卡（金手指处印有官网地址）
- TF（MicroSD）内存卡 + 读卡器
- 内核固件

## 内核下载与安装

1. 访问 [http://cn.r4isdhc.com](http://cn.r4isdhc.com) 下载对应版本内核
2. 解压内核文件，将所有文件转移到 TF 卡根目录

**TF 卡格式化**：
- 容量 ≤32GB：FAT32 格式（直接用系统格式化）
- 容量 >64GB：使用 DiskGenius 等专业工具格式化为 FAT32

## ROM 文件管理

- 游戏 ROM 放在 TF 卡根目录或一级子文件夹中
- **注意**：不能嵌套两层以上文件夹，否则内核检测不到游戏
- 进入游戏：选中 ROM → 按 A 键或点击图标

## 操作快捷键（内核界面）

| 按键 | 功能 |
|------|------|
| A | 打开文件夹 / 启动游戏 / 播放媒体 |
| B | 退出 / 返回上一级 |
| L | 调节屏幕亮度 |
| R | 退出到内核界面 |
| Select | 浏览近期打开的文件 |
| Start | 打开设置菜单（记事本、系统设置、壁纸等） |

## 金手指与存档

进入游戏后按 B 键可以：
- 选择金手指（Cheat Code）
- 管理存档
- 开启即时存档功能

## 多媒体功能（moonmemo 播放器）

播放器支持：MP3 音乐、DPG 格式视频、图片浏览、TXT 文本阅读、记事本

使用方式：
- 打开播放器 → 选中对应格式文件 → 按 A

## R4iSDHC 用户体验

R4iSDHC 是较主流的 R4 烧录卡品牌，相比早期 R4：
- 支持更大容量 TF 卡
- 内核更新较活跃
- 兼容性覆盖 DS/NDSL/DSi/3DS 多个平台（需对应固件版本）

## 相关页面

- [[entities/neogeo-mame]] — NEOGEO 街机模拟，同为复古游戏主题

## Related

- [[journal/nds-flashcard-memories]] — NDS 世代烧录卡回忆录
