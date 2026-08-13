---
title: "R4iSDHC 用户体验教训 — 内核设计缺陷与即时存档破解"
category: skills
tags:
  - nds
  - flashcard
  - retro-gaming
  - user-experience
  - skills
summary: R4iSDHC 内核 UX 教训：菜单只扫一层目录、4 槽 RTS 仅 2 槽可用（SAVE C/D 灰禁），通过 HxD 把 SD:/R4iMenu/R4i.sav 中 `23 23` 附近的 `23` 改成 `AB` 可强制开启 4 槽。以及「为什么还是 DSTwo 香」结论。
sources:
  - "https://jixun.uk/posts/2016/r4isdhc-simple-review/"
created: "2026-08-13T01:40:00Z"
updated: "2026-08-13T01:40:00Z"
provenance:
  extracted: 0.92
  inferred: 0.06
  ambiguous: 0.02
base_confidence: 0.55
lifecycle: draft
lifecycle_changed: "2026-08-13"
tier: supporting
relationships:
  - target: "[[concepts/dstwo-plugin-system]]"
    type: related_to
---

# R4iSDHC 用户体验教训 — 内核设计缺陷与即时存档破解

> 2016 年的 R4iSDHC 烧录卡实测：内核 UX 槽点 + 4 槽 RTS 强制开启方法。

## 内核 UX 的三大槽点

### 1. 菜单只扫一层目录
- 游戏列表只列**根目录 + 一层子目录**的 `.nds` 文件
- 再下一层子目录**直接被无视** — 想分门别类整理两层目录的用户会撞墙
- 反例：**Wood 内核**支持多层目录浏览（用户评价「别用 R4i 的破文件浏览器，用 Wood 吧」）

### 2. 单个游戏 Rom 设置的输入反人类
- 通过 `X` 和 `B` 键**上下切换**游戏 Rom 设定（不是单 Rom 多选项）
- 选择体验与 Wood 内核的「点选 + 多选项」差距明显

### 3. 无法模拟 NDS 主机语言
- 兼容性不错（《游戏王 GX：灵魂召唤者》汉化版在两个 Wood 内核 R4 山寨卡上白屏，**R4iSDHC 能跑**）
- 但**无法模拟 NDS 主机语言** — 欧版 3DS 上汉化版出英文，无法切日语系统显示汉化内容
- 启动游戏慢，初次启动会建立存档（半分钟左右）

## 即时存档（RTS）的两槽困境

R4iSDHC 菜单画 4 个存档位（SAVE A/B/C/D），**实际上只能用 A/B 两槽**：

| 存档位 | 状态 |
|---|---|
| `SAVE A` | ✅ 可读写 |
| `SAVE B` | ✅ 可读写 |
| `SAVE C` | ❌ **灰禁**（开不开）|
| `SAVE D` | ❌ **灰禁**（开不开）|

更糟的是：**A/B 操作一次后，再次按下 RTS 快捷键就会死机**。等于「即时」存档根本不可用。

### 强制开启 4 槽的破解方法

用 HxD 或其它 Hex 编辑器打开 `SD:/R4iMenu/R4i.sav`，**搜索 `23 23`**，把附近的 `23` 全部替换成 `AB`。这个值一般在卡带 ID 后面。

→ 改完后 C/D 槽被解锁可用。但**仍然不能修复 A/B 操作后的死机问题**（属于内核 bug，不在存档格式层）。

## 与 DSTwo 的对比

> 「想要即时存档和超强的 Rom 兼容性，还是用 DsTwo 吧，别想省钱。」

| 维度 | R4iSDHC | DS Two（DSTwo） |
|---|---|---|
| 即时存档 | 2 槽可用 + 死机 | 完整 4 槽稳定 |
| GBA 模拟 | — | **TempGBA**（有缓存，兼容性高）|
| 内核 UX | 抄来抄去 + 文件结构乱 | 成熟稳定 |
| 价格 | 便宜（¥40-80）| 二手 ¥200+ |
| 兼容性 | OK，但 NDS 主机语言切换不支持 | 几乎全兼容 |

## 结论与教训

- **R4iSDHC 的内核是「抄来抄去最后抄出了个四不像」** — 用户原话
- 文件结构混乱、设计逻辑不一致（菜单只扫一层 + Rom 切换上下 + 4 槽变 2 槽）
- 实在要用，套个 **Wood 内核** + 修复游戏兼容性，比 R4iSDHC 原生内核体验好

## 相关页面

- [[concepts/dstwo-plugin-system]] — DSTWO 的 plugin 协议（烧录卡 firmware 启动协议的代表）
- [[journal/nds-flashcard-memories]] — NDS 烧录卡横向对比