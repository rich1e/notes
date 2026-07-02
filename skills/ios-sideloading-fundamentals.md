---
title: iOS 侧载基础：证书、JIT、SideStore 与 LiveContainer
category: skills
tags: [ios, sideload, security]
sources:
  - "https://www.onmyodev.com/2026/05/ios-sideloading-faq/"
created: 2026-07-02
updated: 2026-07-02
summary: iOS 侧载完整机制：调试/发布证书区别、Entitlements 权限体系、描述文件有效期、SideStore 与 LiveContainer 的原理与适用场景、JIT 开启条件。
base_confidence: 0.83
lifecycle: draft
lifecycle_changed: "2026-07-02"
tier: supporting
provenance:
  extracted: 0.85
  inferred: 0.12
  ambiguous: 0.03
relationships:
  - target: "[[entities/feather-ios-sideload]]"
    type: related_to
---

# iOS 侧载基础：证书、JIT、SideStore 与 LiveContainer

## 证书类型

### 调试证书 vs 发布证书

| 项目 | 调试证书 | 发布证书（企业证书）|
|------|----------|---------------------|
| `get-task-allow` | ✅ 含（允许调试器附加） | ❌ 无 |
| JIT 支持 | ✅ | ❌ |
| 数量限制 | 每开发者 2 张 | 较多 |
| 免费开发者 | ✅ 可申请 | ❌ 仅付费 |
| 网购"个人开发者证书" | 本质是发布证书，无 JIT | — |

**关键结论**：购买的证书 = 发布证书，无法开启 JIT，与用了什么签名工具无关。

### Entitlements（特殊权限）

不同于普通弹窗权限（照片/定位等），Entitlements 由 iOS 自动处理：

| Entitlement | 可用性 |
|-------------|--------|
| `Increased Memory Limit` | 任何人（模拟器必需） |
| `Extended Virtual Addressing` | 任何人（大内存 App） |
| `get-task-allow` | 调试证书专有 → 允许 JIT |
| `Personal VPN` | 付费开发者 + 向苹果申请 |

### 描述文件有效期

- **证书本身**有效期 1 年（含免费开发者）
- **免费开发者产生的描述文件有效期 7 天**（不是证书有效期短，是描述文件有效期短）
- 续签 = 用同一张证书重新生成新的描述文件（再得 7 天）

描述文件有效的三个条件同时满足：
1. 证书在有效期内
2. 描述文件在有效期内
3. 描述文件记载的 Entitlements 与 App 实际使用的一致

## SideStore 原理

传统侧载工具，直接将 App 安装到系统，受证书体系全部限制。

关键组件：
- **minimuxer**：在 iOS 沙盒内实现 usbmuxd，使设备能自连接（模拟通过 Wi-Fi 连接的电脑）
- **Anisette 服务器**：远程模拟 Xcode 签名服务，生成描述文件（这是账户里出现陌生 Mac 的原因）
- **StosVPN/LocalDevVPN**：通过回环隧道模拟电脑正在监听 iOS 设备

**为何需要 Wi-Fi**：iOS 的 iTunes Wi-Fi Sync 机制只在联网时激活，SideStore 借用这个通道。

**iOS 26.4 的影响**：苹果将配对格式从 Lockdown 改为 RPPairing，旧方法（飞行模式欺骗 + 中途关隧道）不再有效，需要全程保持 StikDebug 开启和 Wi-Fi 连接。

## LiveContainer 原理

**不将 App 安装到系统**，而是解压 App 到自身数据文件夹，通过 LiveProcess 在运行时绕过主程序执行 App 代码。

| 特性 | SideStore | LiveContainer |
|------|-----------|---------------|
| 占用 App ID | ✅ 是 | ❌ 否 |
| 描述文件限制 | ✅ 受限 | ❌ 绕过 |
| 桌面图标 | ✅ 有 | ❌ 无（需手动创建） |
| `.dylib` 注入支持 | ❌ 差 | ✅ 好 |
| App 与 LiveContainer 共享 Entitlements | — | ✅（在 LiveContainer 上统一配置） |

LiveContainer 中所有 App 共享 LiveContainer 的 Entitlements，修改 Increased Memory Limit 需在 **LiveContainer 本体**上操作，不在 App 内操作。

续签时也只给 **LiveContainer 本体**续签。

## JIT 开启原理

JIT（Just-in-time Compilation）允许运行时动态写入可执行内存，iOS 默认仅授权 WebKit。

**开启条件**：App 必须拥有 `get-task-allow` Entitlement（调试证书专属），且连接调试器。

- **StikDebug**：模拟一台运行调试器的电脑，让 iOS 认为 App 正在被调试，自动允许 JIT
- iOS 26+ 要求：全程保持 StikDebug 开启 + Wi-Fi 连接，否则 iOS 判定调试器断开 → App 闪退

**iOS 18.4 前的旧方法**：直接利用 `get-task-allow` 抓进程开启 JIT；18.4 已堵漏。

## 工具选型

| 需求 | 推荐工具 |
|------|----------|
| 需要 JIT（模拟器、虚拟机） | SideStore / LiveContainer |
| 需要 Personal VPN / iCloud 同步等 Entitlements | Feather（付费证书）|
| 注入 `.dylib` 插件 | LiveContainer / Feather |
| 不想频繁续签 | Feather（付费证书，1 年有效）|

## 相关页面

- [[entities/feather-ios-sideload]] — 付费证书签名工具 Feather
- [[skills/ios-app-store-publishing]] — 官方证书与发布流程对比
