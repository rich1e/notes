---
title: iOS 侧载基础：证书、JIT、SideStore 与 LiveContainer
category: skills
tags: [ios, sideload, security]
sources:
  - "https://www.onmyodev.com/2026/05/ios-sideloading-faq/"
  - "[[Clippings/Feather 签名工具.md]]"
created: 2026-07-02
updated: 2026-08-13T01:40:00Z
summary: iOS 侧载完整机制：调试/发布证书区别、Entitlements 权限体系、描述文件有效期、SideStore 与 LiveContainer 的原理与适用场景、JIT 开启条件。
base_confidence: 0.83
lifecycle: reviewed
lifecycle_changed: 2026-08-03
lifecycle_reason: "auto-promoted by wiki-lint --consolidate: age>30d, confidence>0.7"
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

关键组件形成“设备自连 + 远程签名”链路：
- **minimuxer**：电脑端 `usbmuxd` 的 iOS 精简实现，可在沙盒内工作，使设备通过系统已有的 Wi‑Fi 设备管理通道连接自身
- **Anisette 服务器**：在远程服务器模拟 Xcode 的签名服务并向苹果请求描述文件；使用后 Apple 账户里出现陌生 MacBook/iMac，通常源于该模拟环境
- **StosVPN/LocalDevVPN**：把发往指定地址的数据包交换源与目标后回送设备自身，建立本地回环隧道；配合 minimuxer，让 iOS 认为有电脑正在监听连接

**为何需要 Wi-Fi**：iOS 的 iTunes Wi-Fi Sync 机制只在联网时激活，SideStore 借用这个通道。

**iOS 26.4 的影响**：苹果废弃旧的 Lockdown 配对格式，改用 RPPairing。配对文件仍然需要，但飞行模式欺骗和连接后中途关闭回环隧道不再可用；SideStore 续签以及 StikDebug 启用 JIT 时需按工具要求保持 Wi‑Fi 和隧道连接。

> 真实案例：[[misc/web-github-com-livecontainer-issues-1456]] — LiveContainer 3.7.14 Nightly + iPadOS 26.3 下 SideStore Refresh All 报 "Unable to manage profiles on the device"，维护者 hugeBlack 确认根因即 RPPairing 文件缺失或格式错误，建议用 `idevice_pair` (jkcoxson, v0.1.14+) 自行生成。

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

### JIT 工具分类

| 类型 | 代表工具 / 场景 | 原理与限制 |
|------|-----------------|------------|
| 机上调试器模拟 | StikDebug | 借助配对文件、回环隧道与脚本模拟电脑调试器；iOS 26+ 通常要持续保持 Wi‑Fi、LocalDevVPN 与调试连接 |
| 电脑端调试附加 | AltJIT 等 | 由真实电脑连接并附加目标进程，适用于部分旧系统与工具链 |
| 容器内 JIT | LiveContainer | 容器以 JIT 运行内部 App，可绕过内部程序的代码签名，但仍取决于 LiveContainer 本体及系统版本支持 |
| 越狱环境 | 越狱工具链 | 系统级放宽或移除 Code Signing 限制，能力最强，但设备和系统版本受限 |

- **StikDebug**：模拟一台运行调试器的电脑，让 iOS 认为 App 正在被调试，自动允许 JIT
- iOS 26+ 要求：全程保持 StikDebug 开启 + Wi-Fi 连接，否则 iOS 判定调试器断开 → App 闪退

**iOS 18.4 前的旧方法**：直接利用 `get-task-allow` 抓进程开启 JIT；18.4 已堵漏。

## 签名工具选择决策表

| 首要需求 | 推荐方案 | 选择依据 |
|----------|----------|----------|
| 模拟器、虚拟机等需要 JIT | **SideStore**（配合 StikDebug 等 JIT 工具） | 免费开发者调试证书包含 `get-task-allow`；购买的发布证书不能替代 |
| 需要更多签名选项、改包信息、插件注入或特定 Entitlement | **全能签 / Feather** | 面向付费发布证书，签名与注入功能更完整；能否使用某项 Entitlement 仍由证书和描述文件决定 |
| 想减少 App ID 占用、集中运行多个 App | **LiveContainer** | 内部 App 不单独占用 App ID，共享容器本体的 Entitlements 和有效期 |

> 选择顺序应先看 **JIT 与 Entitlement**，再看界面和便利性：JIT 需求优先 SideStore；功能、注入和 Entitlement 需求优先全能签或 [[entities/feather-ios-sideload|Feather]]。两类方案通常不能互换。

## 工具选型

| 需求 | 推荐工具 |
|------|----------|
| 需要 JIT（模拟器、虚拟机） | SideStore / LiveContainer |
| 需要 Personal VPN / iCloud 同步等 Entitlements | Feather（付费证书）|
| 注入 `.dylib` 插件 | LiveContainer / Feather |
| 不想频繁续签 | Feather（付费证书，1 年有效）|
| 老设备体验 iOS 26 Liquid Glass UI 风格 | Feather（强制 Liquid Glass 选项）|

## Feather 的几个易踩坑细节

- **导入证书需先解压**：Feather 不识别 `.zip`/`.7z` 压缩包，必须先解压出 `.p12`/`.mobileprovision` 再导入。
- **不可安装在 LiveContainer 中**：Feather 自身签名时要装在「真实环境」，不能装在 LiveContainer 的沙盒里，否则签名工具链失败。
- **机上安装走本地回环**：通过 Pairing File + StosVPN/LocalDevVPN 实现「设备自连接自己」，安装过程不经过外部服务器（更隐私 + 不依赖中央服务存活）。
- **强制 Liquid Glass**：在签名选项底部可启用 — 修改框架信息让目标软件使用 iOS 26 Liquid Glass 界面风格，适合老设备体验新观感或反向把老 App「假装」成新版。
- **PPQ 保护**：苹果对付费开发者签名盗版软件零容忍（包名撞库付费 App → 证书拉黑）。PPQ 在包名后加随机字符串绕过此检测。

## 相关页面

- [[entities/feather-ios-sideload]] — 付费证书签名工具 Feather
- [[skills/ios-app-store-publishing]] — 官方证书与发布流程对比
- [[misc/web-github-com-livecontainer-issues-1456]] — LiveContainer #1456 案例：iPadOS 26.3 + RPPairing 缺失导致 SideStore Refresh All 失败
