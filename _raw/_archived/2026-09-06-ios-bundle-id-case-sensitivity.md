---
title: iOS Bundle ID 大小写与 Provisioning Profile 不匹配 —— 签名失败常见根因
tags: [ios, xcode, code-signing, provisioning-profile, bundle-id]
summary: >-
  Xcode 自动签名时，项目的 PRODUCT_BUNDLE_IDENTIFIER 与 Apple Developer 后台
  App ID 必须完全一致（含大小写），否则报"Provisioning profile doesn't include
  aps-environment / icloud-container-identifiers entitlements"或
  "has app ID X which does not match the bundle ID Y"。
project: dayfold
created: 2026-09-06
updated: 2026-09-06
sources:
  - "dayfold session (2026-09-06)"
summary: |
  dayfold 项目 PRODUCT_BUNDLE_IDENTIFIER = com.Yuqi.dayfold (d 小写)，
  但 Developer 后台注册与本地 profile 都是 com.Yuqi.Dayfold (D 大写)。
  Xcode 16.2 自动签名失败，提示 profile 不支持 iCloud / Push 能力。
  实际根因是 bundle id 大小写不匹配导致选错 profile (wildcard)。
provenance:
  extracted: 0.8
  inferred: 0.2
  ambiguous: 0.0
base_confidence: 0.95
lifecycle: draft
lifecycle_changed: 2026-09-06
---

## 现象

- 项目 `PRODUCT_BUNDLE_IDENTIFIER = com.Yuqi.dayfold` (d 小写)
- Provisioning Profile `iOS Team Provisioning Profile: com.Yuqi.Dayfold` (D 大写)
- `application-identifier` 在 profile 内为 `SG7W8L7FQK.com.Yuqi.Dayfold`
- 自动签名失败：
  ```
  Provisioning profile "iOS Team Provisioning Profile: *" doesn't support the
  iCloud and Push Notifications capability.
  ... doesn't include the aps-environment,
  com.apple.developer.icloud-container-identifiers,
  and com.apple.developer.icloud-services entitlements.
  ```

## 误导性诊断

错误信息看起来像 iCloud/Push 权限问题。但实际是 Xcode 在多个 profile 中按 bundle id 匹配失败，
回退到了 wildcard `*` profile，而 wildcard 不带 CloudKit / aps-environment。

## 修复

把项目里所有 `PRODUCT_BUNDLE_IDENTIFIER`（含 `…Tests` / `…UITests` 后缀的三个 target 的 Debug + Release 配置）改为与 profile 一致的大小写：

```
sed -i '' 's/com.Yuqi.dayfold/com.Yuqi.Dayfold/g' \
  path/to/project.xcodeproj/project.pbxproj
```

`replace_all` 一次替换即可覆盖 6 处（3 个 target × 2 个 config）。

## 验证

修复后立刻 `BUILD SUCCEEDED`，且：

- `codesign -dvv <App.app>` 显示 `Identifier=com.Yuqi.Dayfold`
- `embedded.mobileprovision` 已嵌入
- 自动选择正确 profile：`iOS Team Provisioning Profile: com.Yuqi.Dayfold (ef264a7a-…)`

## 教训

- Apple Developer 后台的 App ID 一旦注册，大小写不可变
- Bundle id 必须精确匹配（即使大小写不同）
- 错误信息若提到"不支持某 capability"且同时有多份 profile，先查 bundle id 匹配

## 相关

- [[xcode-multiple-installation]]
- [[ios26-xcode26-required]]