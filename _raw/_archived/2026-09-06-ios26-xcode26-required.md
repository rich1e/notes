---
title: iOS 26 真机调试要求 Xcode 26.x —— DDI 缺失陷阱
tags: [ios, xcode, real-device, debugging, ddi]
summary: >-
  iOS 26 (含 26.6.x) 真机只能被 Xcode 26.x 识别与调试；Xcode 16.x 报 DDI 缺失，
  且 App Store 不提供 Xcode 26 主程序包更新。
project: dayfold
created: 2026-09-06
updated: 2026-09-06
sources:
  - "dayfold session (2026-09-06)"
summary: |
  在 Xcode 16.x 上对 iOS 26 真机 (iPhone 17 Pro Max / iOS 26.6.1) 进行 Debug 构建
  与 install 时，xcodebuild / devicectl 报 `kAMDMobileImageMounterPersonalizedBundleMissingVariantError`。
  根因是 Xcode 16.x 带的 iOS DDI 不含 iOS 26 variant。Xcode 26.x (Build 17F113) 才能识别。
provenance:
  extracted: 0.85
  inferred: 0.15
  ambiguous: 0.0
base_confidence: 0.9
lifecycle: draft
lifecycle_changed: 2026-09-06
---

## 现象

- 真机 iPhone 17 Pro Max (iPhone18,2) iOS 26.6.1
- 本机 Xcode 16.2 / 16.4 均报 `connected (no DDI)`
- `xcodebuild -destination id=<UDID> build` → `Unable to find a device matching`
- `xcrun devicectl device install app` → `kAMDMobileImageMounterPersonalizedBundleMissingVariantError`
- 设备 `osVersionNumber: 26.6.1`，Xcode `iPhoneOS.platform/DeviceSupport/` 最大到 `16.4`

## 根因

Apple 2025 年将 Xcode / iOS 改成按年份命名。Xcode 16.x 最高对应 iOS 18 SDK，不带 iOS 26 设备的 Developer Disk Image (DDI)。

## 解决方法

- 安装 Xcode 26.x（Apple App Store 实际只更新 Command Line Tools，主程序包需另寻渠道）
- macOS 上常见做法是双版本共存：`/Applications/Xcode.app` 与 `/Applications/Xcode-old.app`
- 用环境变量切换，不需要 sudo：

```bash
export DEVELOPER_DIR=/Applications/Xcode-old.app/Contents/Developer
xcodebuild -version   # → Xcode 26.6 Build 17F113
xcrun devicectl list devices
```

## 验证证据

切换到 Xcode 26.6 后：

- `xcrun devicectl list devices` → 设备状态从 `connected (no DDI)` 变为 `available (paired)`
- `xcrun devicectl device install app --device <UDID> <App.app>` → `App installed: bundleID: com.Yuqi.Dayfold`
- `xcrun devicectl device process launch --terminate-existing com.Yuqi.Dayfold` → `Launched application`
- `xcrun devicectl device info processes` 显示 PID 3124 在跑 `dayfold.app/dayfold`

## 副作用

- `xcode-select -p` 默认指向 `/Applications/Xcode.app/Contents/Developer`
- `sudo xcode-select -s` 需要交互密码
- 推荐在脚本 / 临时会话用 `DEVELOPER_DIR` 而非 `xcode-select`，避免全局副作用

## 相关

- [[xcode-multiple-installation]]
- [[ios-bundle-id-case-sensitivity]]