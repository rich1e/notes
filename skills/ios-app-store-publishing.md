---
title: 发布到 App Store
category: skills
tags: [ios, app-store, xcode, security]
sources: ["buckets/books/iOS 17 App Development for Beginners.epub"]
created: 2026-07-01T00:00:00Z
updated: 2026-08-03T05:47:33Z
summary: iOS App 发布完整流程：Apple Developer 证书/Identifier/Profile 创建、Xcode Archive 打包、App Store Connect 配置、TestFlight 内测、版本更新与审核拒绝处理。
base_confidence: 0.86
lifecycle: reviewed
lifecycle_changed: 2026-08-03
lifecycle_reason: "auto-promoted by wiki-lint --consolidate: age>30d, confidence>0.7"
tier: peripheral
provenance:
  extracted: 0.92
  inferred: 0.08
  ambiguous: 0.00
---

# 发布到 App Store

## 前置要求

- **Apple Developer Program**：年费 $99，在 [developer.apple.com](https://developer.apple.com) 注册
- **Xcode 15**：macOS 13 Ventura 或更高
- **App 已适配**：Launch Screen、App Icons 全尺寸、适配 iPhone/iPad

## 步骤一：准备 App

### Launch Screen

使用 `LaunchScreen.storyboard`，配置品牌 Logo / 名称。在 Target → General → App Icons and Launch Screen 中指定。

### App Icons

所需尺寸：20pt、29pt、40pt、60pt、76pt、83.5pt（iPad）、1024pt（App Store）。  
推荐工具：[Prepo](https://apps.apple.com/app/prepo/id476533227)（Mac App Store 免费）批量生成。

## 步骤二：创建证书（Certificate）

1. 打开 **Keychain Access → Certificate Assistant → Request a Certificate From a Certificate Authority**
2. 填写邮箱与名称，选择"Save to Disk"，生成 `.certSigningRequest` 文件
3. 在 [developer.apple.com/account](https://developer.apple.com/account) → Certificates → 新建 **App Store Distribution** 证书
4. 上传 `.certSigningRequest` 文件，下载 `.cer` 并双击安装到 Keychain

## 步骤三：创建 App Identifier

在 **Identifiers** 页面 → 新建 **App ID**：

- **Description**：App 描述（不含 `@`, `&`, `*` 等特殊字符）
- **Bundle ID**：反域名格式，如 `com.yourcompany.appname`（不含 `*`）
- **Capabilities**：勾选需要的服务（Push Notifications、iCloud 等）

## 步骤四：创建 Distribution Profile

在 **Profiles** 页面 → 新建 **App Store** 类型的 Provisioning Profile：

1. 选择 App ID（步骤三创建的）
2. 选择 Distribution Certificate（步骤二创建的）
3. 命名后下载 `.mobileprovision`，双击安装

## 步骤五：Xcode 构建与 Archive

```
Target → Signing & Capabilities：
- Bundle Identifier 与 App ID 一致
- Provisioning Profile 选择刚安装的 Distribution Profile
- Signing Certificate 自动选择

设备选择 → "Any iOS Device (arm64)"
Product → Archive → 等待构建完成
```

Archive 完成后，Xcode 自动打开 **Organizer**：

- **Upload to App Store**：直接上传到 App Store Connect
- **Export**：导出 IPA，再用 **Transporter** 上传

## 步骤六：App Store Connect 配置

在 [appstoreconnect.apple.com](https://appstoreconnect.apple.com) → My Apps → 新建 App：

| 字段 | 说明 |
|---|---|
| Platform | iOS |
| Bundle ID | 与 Identifier 一致 |
| SKU | 内部唯一标识，不显示给用户 |
| User Access | 通常选 Full Access |

**产品页**（最多 40 种语言）：
- 名称（30字符）、副标题（30字符）
- 关键词（100字符，影响搜索排名）
- 描述（4000字符）
- 截图：最多 10 张（5.5"、6.5" iPhone 必须）

**隐私政策 URL**：必须提供。

## TestFlight（内测）

1. 上传 Build 后，在 App Store Connect → TestFlight 找到对应 Build
2. **内部测试**：最多 100 名 Apple Developer 账号成员，无需审核
3. **外部测试**：最多 10,000 名，需 TestFlight 审核（通常 1 天）
4. 测试期 90 天，可手动邀请或通过公开链接

## 提交审核

填写完所有信息后点击 **Submit for Review**。状态流转：

```
Waiting for Review → In Review → Approved/Rejected
```

审核周期通常 1-3 天；节假日可能更长。

## 常见拒绝原因及应对

| 拒绝理由 | 解决方法 |
|---|---|
| 功能缺失/崩溃 | 修复后重新提交；附说明截图 |
| 隐私政策缺失 | 添加真实可访问的隐私政策 URL |
| 登录凭据缺失 | 在 Notes 提供测试账号密码 |
| ATS 配置豁免 | 补充理由说明（如访问第三方旧 API） |
| 误导性截图 | 使用真实 App 截图，不得添加设备外框以外的内容 |
| 付费功能未说明 | 在描述和截图中清晰标注付费内容 |

## 更新版本

1. App Store Connect → 选择 App → iOS App → `+` 新版本
2. 修改 **What's New**（更新说明）
3. 在 Xcode 中更新 `CFBundleShortVersionString`（版本号）和 `CFBundleVersion`（构建号）
4. Archive → 上传 → 在 App Store Connect 选择新 Build → 提交审核

## 关联页面

- [[skills/xcode-ide-guide]] — Xcode 15 Archive 操作
- [[entities/ios17-app-development-book]] — 来源书籍
