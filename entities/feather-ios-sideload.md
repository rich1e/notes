---
title: Feather — iOS 签名工具
category: entities
tags:
  - ios
  - sideload
  - tools
summary: 专为付费 Apple 开发者设计的 iOS 机上签名工具，支持 AltSource 软件源、dylib 插件注入、随机包名（PPQ 保护）和本地回环安装。
sources:
  - https://www.onmyodev.com/2026/03/feather/
  - https://www.onmyodev.com/2026/05/ios-sideloading-faq/
  - "Clippings/Feather 签名工具"
created: 2026-06-29
updated: 2026-08-13
tier: supporting
lifecycle: draft
lifecycle_changed: "2026-06-29"
base_confidence: 0.55
provenance:
  extracted: 0.92
  inferred: 0.06
  ambiguous: 0.02
---

# Feather — iOS 签名工具

## 定位

专为**付费 Apple 开发者证书**设计的 iOS 机上签名工具。免费开发者账户**不可用**。

与 AltStore/SideStore 等工具不同，Feather 以付费开发者为核心用户，提供更完整的签名功能链。

## 核心功能

### 软件源
- 支持 AltSource/SideStore 格式的软件源（可直接导入 SideStore 社区源）
- 无捆绑黑灰产解锁码机制

### 插件注入
- 支持 `.dylib` / `.deb` 格式的 Substrate/ElleKit 插件注入
- 使用真实的越狱插件注入器，把插件注入待签名 App；这不同于 LiveContainer 只能借助 `TweakLoader.dylib` 加载独立 `.dylib` 的方式

### 随机包名（PPQ 保护）
苹果对付费开发者签名盗版软件零容忍。PPQ 保护在签名时于包名后附加随机字符串，绕过包名监控。
- 入口：设置 → 签名选项 → PPQ 保护

### 强制 Liquid Glass
签名选项底部可通过修改框架信息强制 App 使用 iOS 26 Liquid Glass 界面风格（适合老设备体验新系统观感）。

### 机上安装（无需外部服务器）
通过 Pairing File + 本地回环实现设备自连接安装，无需外部安装服务器：
- 入口：设置 → 安装
- 将"安装类型"从"服务器"改为 `idevice`

### 其他
- 签名时可修改图标、名称、包名、软件属性

### 强制 Liquid Glass（iOS 26 UI 风格）

签名选项底部可启用：在签名时修改框架信息强制目标软件使用 **iOS 26 Liquid Glass** 界面风格。适合老设备体验新系统观感，或反向把老 App 「假装」成新版。

## 安装流程

1. 从 [GitHub Releases](https://github.com/claration/Feather/releases) 下载 `.ipa`
2. 用已有签名工具（全能签/轻松签/Xcode）完成首次签名安装 — **不可安装在 LiveContainer 中**
3. Feather 签名安装包后用 Feather 自身或其他工具装机

## 使用流程

1. **导入证书**：需先**解压**证书压缩包（Feather 不识别 `.zip`，必须先解压看到 `.p12`/`.mobileprovision`）
2. **获取安装包**：三种方式 —
   - 通过软件源（AltSource / SideStore Community Picks）下载
   - 直接导入本地 `.ipa`
   - 输入 URL 让 Feather 帮你下载
3. **签名**：点击软件右侧"签名"按钮，可选择证书、修改属性（图标 / 名称 / 包名 / 软件属性）、启用 **PPQ 保护**、**强制 Liquid Glass**
4. **安装**：已签名软件显示剩余天数，点击即安装（Pairing File + 本地回环，**不经过外部服务器**）

## 局限

- **必须付费开发者证书**，免费 Apple ID 不可用
- 证书有效期通常 1 年（企业证书会有吊销风险）
- **无法开启 JIT**：付费证书 = 发布证书，不含 `get-task-allow` Entitlement，无法运行需要 JIT 的模拟器

## 相关页面

- [[skills/ios-sideloading-fundamentals]] — 证书类型、JIT 原理、SideStore vs LiveContainer 完整对比
- [[skills/ios-emulator-setup]] — 需要 JIT 的模拟器（ManicEMU/MeloNX）安装指南
