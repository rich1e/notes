---
title: iOS 模拟器安装与配置（ManicEMU / MeloNX）
category: skills
tags: [mobile, MAME, Feather]
sources:
  - "https://www.onmyodev.com/2026/05/manicemu/"
  - "https://www.onmyodev.com/2026/05/melonx/"
created: 2026-07-02
updated: 2026-08-03T05:47:33Z
summary: iOS 平台 3DS 模拟器（ManicEMU/Azahar 核心）和 Switch 模拟器（MeloNX/MeloVertex）的安装、JIT 配置与常见问题。
base_confidence: 0.83
lifecycle: reviewed
lifecycle_changed: 2026-08-03
lifecycle_reason: "auto-promoted by wiki-lint --consolidate: age>30d, confidence>0.7"
tier: peripheral
provenance:
  extracted: 0.80
  inferred: 0.15
  ambiguous: 0.05
relationships:
  - target: "[[skills/ios-sideloading-fundamentals]]"
    type: uses
  - target: "[[entities/feather-ios-sideload]]"
    type: related_to
---

# iOS 模拟器安装与配置

iOS 平台的高性能模拟器（3DS、Switch 等）依赖 **JIT** 才能达到可玩帧率，因此必须通过侧载安装，且需要调试证书。

> 参考：[[skills/ios-sideloading-fundamentals]] — 证书类型与 JIT 原理

## ManicEMU（3DS 模拟器）

### 安装要求

- **必须侧载**（App Store 版无法启用 JIT，3DS 游戏性能极差）
- 侧载后自动解锁除 iCloud 同步外的所有功能（永久会员）
- 支持 SideStore、AltStore、LiveContainer 安装；官方不推荐 LiveContainer 但实测可用

下载：[GitHub Releases](https://github.com/Manic-EMU/ManicEMU/releases)

### 核心配置步骤

1. **切换核心**：设置 → 向下滚动到“模拟器核心” → 改为 **Azahar**；默认 Citra 核心不支持 JIT
2. **带 JIT 启动**：从 StikDebug 使用 `manic.js` 启动 ManicEMU，而不是从桌面直接打开；返回设置页确认状态为绿色“JIT 可用”
3. **每个游戏单独开启 JIT**：点游戏打开菜单 → 翻到“高级设置” → 开启 `use_cpu_jit` → 保存；该设置不是全局项，每个游戏都要重复一次
4. **CPU 倍率**：`cpu_scale` 按设备实际性能逐步调整，并非越高越好；设备无法提供对应算力时，设置为 400% 也不会获得等比例性能

### 游戏格式

只支持**已解密的 ROM**，加密 ROM（安装说明含"导入 FBI 密钥"步骤）无法运行。

### Mii 问题

游戏需要 Mii 时，优先使用 **Artic Base** 从 3DS 真机向 ManicEMU 传输 NAND 数据；没有真机时，可将来源可靠的 `nand.zip` 解压后，覆盖 ManicEMU 文件夹中的 `3DS` 目录。导入真机 NAND 可能反过来使部分已解密游戏无法运行，因此应在“需要 Mii”与游戏兼容性之间取舍。

### 注意事项

- **App Store 版不能开启 JIT**：即使 StikDebug 的 Other 页面能找到并启动它，也不会为其启用 JIT；要获得 3DS 所需性能，必须安装侧载版
- **切勿依赖即时存档**：3DS 模拟尚不稳定，即时存档可能导致游戏之后无法打开。应使用游戏内置存档，并把即时存档仅视为临时状态而非可靠进度。

---

## MeloNX（Switch 模拟器）

### 设备要求

| 设备 | 最低内存 | 备注 |
|------|----------|------|
| iPhone（无 TrollStore） | 4GB+ | |
| iPad（无 TrollStore） | 8GB+ | 或付费开发者账户 |
| 有 TrollStore 的设备 | 要求较低 | 安装最容易 |

### 必要权限

**`Increased Memory Limit`** Entitlement 是 MeloNX 的硬性要求，无法绕过。

- 使用 **PlumeImpactor** 侧载（官方推荐）：可直接签出该 Entitlement
- 使用 **SideStore**：需额外通过 Get More RAM 启用该 Entitlement，然后在 SideStore 中重装一次
- 使用 **LiveContainer**：在 LiveContainer 本体上启用 Increased Memory Limit + Extended Virtual Addressing

下载：[Forgejo 托管](https://git.ryujinx.app/projects/MeloNX/releases)

### 密钥与固件

1. 下载 prod.keys + title.keys（同时勾选两个文件导入）
2. 下载固件（.zip 文件，**不要解压**，直接导入）
3. 首次启动时会提示导入，两项都显示绿色勾后点 Finish Setup

### JIT 配置

- 通过 **StikDebug** 启动 MeloNX
- iOS 26+：需配置 JIT 脚本（独立安装用 `universal.js`；LiveContainer 中需在 MeloNX 设置内导入脚本）

### 人森优化版（MeloVertex）

专为《动物森友会》优化的改版，修复闪退问题并降低内存使用。
下载：[GitHub Releases](https://github.com/VertexSelection/MeloVertex/releases)

### 常见问题

| 问题 | 解决方法 |
|------|----------|
| 模拟器闪退 | 检查 Increased Memory Limit 是否启用；内存是否足够 |
| 卡在 Waiting for JIT | 确认从 StikDebug 启动；iOS 26 检查 JIT 脚本 |
| 游戏卡 40 帧 | 关闭 Nugget/Pocket Poster 配置的动态壁纸（占用 GPU） |
| 游戏显示英文 | 设置 → System → System Language → Simplified Chinese |
| 文件导入失败 | LiveContainer 中勾选"修复文件导入" |

## 相关页面

- [[skills/ios-sideloading-fundamentals]] — JIT、证书与侧载工具原理
- [[entities/feather-ios-sideload]] — 付费证书签名工具
- [[entities/nds-flashcard]] — 实机 NDS 烧录卡对比
