---
title: iOS Bundle ID 大小写与 Provisioning Profile 不匹配 —— 签名失败常见根因
category: skills
tags: [ios, xcode, code-signing, provisioning-profile, bundle-id]
sources:
  - "dayfold session (2026-09-06)"
created: 2026-09-06
updated: 2026-09-06
summary: Xcode 自动签名时,项目的 `PRODUCT_BUNDLE_IDENTIFIER` 与 Apple Developer 后台 App ID 必须**完全一致(含大小写)**,否则报"profile 不支持某 capability"误导性错误,实际是匹配失败回退到 wildcard profile。
base_confidence: 0.95
lifecycle: draft
lifecycle_changed: 2026-09-06
tier: supporting
provenance:
  extracted: 0.8
  inferred: 0.2
  ambiguous: 0.0
---

# iOS Bundle ID 大小写与 Provisioning Profile 不匹配

## 现象

- 项目 `PRODUCT_BUNDLE_IDENTIFIER = com.Yuqi.dayfold`(d 小写)
- Provisioning Profile `iOS Team Provisioning Profile: com.Yuqi.Dayfold`(D 大写)
- `application-identifier` 在 profile 内为 `SG7W8L7FQK.com.Yuqi.Dayfold`
- 自动签名失败:

```
Provisioning profile "iOS Team Provisioning Profile: *" doesn't support the
iCloud and Push Notifications capability.
... doesn't include the aps-environment,
com.apple.developer.icloud-container-identifiers,
and com.apple.developer.icloud-services entitlements.
```

## 误导性诊断

错误信息看起来像 iCloud / Push 权限问题。但实际是 Xcode 在多个 profile 中按 bundle id 匹配失败,
**回退到了 wildcard `*` profile**,而 wildcard 不带 CloudKit / aps-environment。
提示里"doesn't include ... entitlements"是真,但**根因不是 entitlement 配置,而是选错了 profile**。^[inferred]

## 修复

把项目里所有 `PRODUCT_BUNDLE_IDENTIFIER`(含 `…Tests` / `…UITests` 后缀的三个 target 的 Debug + Release 配置)改为与 profile 一致的大小写:

```bash
sed -i '' 's/com.Yuqi.dayfold/com.Yuqi.Dayfold/g' \
  path/to/project.xcodeproj/project.pbxproj
```

`replace_all` 一次替换即可覆盖 6 处(3 个 target × 2 个 config)。

## 验证

修复后立刻 `BUILD SUCCEEDED`,且:

- `codesign -dvv <App.app>` 显示 `Identifier=com.Yuqi.Dayfold`
- `embedded.mobileprovision` 已嵌入
- 自动选择正确 profile:`iOS Team Provisioning Profile: com.Yuqi.Dayfold (ef264a7a-…)`

## 教训

- Apple Developer 后台的 App ID 一旦注册,**大小写不可变**(后台只接受首次注册时的大小写)
- Bundle id 必须精确匹配(即使大小写不同也不行)
- 错误信息若提到"不支持某 capability"且同时有多份 profile,**先查 bundle id 匹配**,再查 entitlement 配置
- 修复时一次性 sed 全 6 个 target/config 组合,避免漏改 Debug 后 Release 又失败

## 调试命令清单

| 命令 | 用途 |
|------|------|
| `grep -r "PRODUCT_BUNDLE_IDENTIFIER" project.pbxproj` | 列出所有 target 的 bundle id |
| `codesign -dvv <App.app>` | 查看已签名 App 的真实 Identifier |
| `security cms -D -i embedded.mobileprovision` | 查看 profile 内 `application-identifier` |
| `ls ~/Library/MobileDevice/Provisioning\ Profiles/` | 查看本机所有 profile(用 `*.mobileprovision` UUID 识别) |

## 相关

- [[skills/xcode-multiple-installation]] — 多 Xcode 切换后第一个跑通的 debug 任务,触发本问题。
- [[projects/dayfold/skills/ios26-xcode26-required]] — 同 session 的姊妹 skill:iOS 26 真机调试前置条件。
- [[projects/dayfold/dayfold]] — 项目主页(Bundle ID `com.Yuqi.dayfold`)。