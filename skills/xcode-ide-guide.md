---
title: Xcode IDE 入门
category: skills
tags: [xcode, ios, ide, simulator, playground, xcode-cloud]
sources: ["buckets/books/iOS 17 App Development for Beginners.epub"]
created: 2026-07-01T00:00:00Z
updated: 2026-07-01T00:00:00Z
summary: Xcode 15 核心功能：界面导航区/编辑区/调试区、项目配置、iOS 模拟器使用、Swift Playground、Organizer 管理、Xcode Cloud CI/CD 基础。
base_confidence: 0.86
lifecycle: draft
lifecycle_changed: "2026-07-01"
tier: supporting
provenance:
  extracted: 0.90
  inferred: 0.10
  ambiguous: 0.00
---

# Xcode IDE 入门

Xcode 15 是 Apple 官方 IDE，支持 Swift 5.9、iOS 17、macOS Sonoma SDK。

## 下载安装

从 Mac App Store 搜索 "Xcode" 下载，版本 15.x，大小约 15GB。  
首次启动会安装额外组件（可选 watchOS/tvOS SDK）。

**系统要求**：macOS 13 Ventura 或更高。

## 界面布局

```
┌────────────────────────────────────────────────────┐
│  Toolbar（工具栏）：运行/停止/设备选择/状态          │
├──────────┬─────────────────────────────┬────────────┤
│ Navigator │         Editor Area         │ Inspector  │
│ 导航区    │         编辑区              │ 检查器     │
│           │                             │            │
│           ├─────────────────────────────┤            │
│           │       Debug Area            │            │
│           │    变量区  |  控制台         │            │
└──────────┴─────────────────────────────┴────────────┘
```

| 区域 | 快捷键 | 功能 |
|---|---|---|
| Navigator（导航区） | `Cmd+0`~`Cmd+8` | 文件树/搜索/符号/问题/测试/调试/断点/报告 |
| Editor Area（编辑区） | — | 代码/Storyboard/plist/Asset Catalog 编辑 |
| Inspector（检查器） | `Cmd+Opt+0~5` | 属性/文件/历史/快速帮助 |
| Debug Area（调试区） | `Cmd+Shift+Y` | 变量监视 + 控制台输出 |
| Object Library | `Cmd+Shift+L` | 拖拽 UI 组件到 Storyboard |

### 快捷键速查

| 操作 | 快捷键 |
|---|---|
| 全局搜索 | `Cmd+Shift+F` |
| 跳转到定义 | `Cmd+Click` |
| 快速打开文件 | `Cmd+Shift+O` |
| 运行 App | `Cmd+R` |
| 停止 App | `Cmd+.` |
| 构建 | `Cmd+B` |
| 清理构建 | `Cmd+Shift+K` |
| 文档注释 | `Cmd+Alt+/` |
| 格式化代码 | `Cmd+Ctrl+I` |

## 创建 iOS 项目

1. **File → New → Project → iOS → App**
2. 填写：
   - **Product Name**：App 名称
   - **Team**：Apple Developer Account（发布时必须）
   - **Bundle Identifier**：`com.organization.appname`
   - **Interface**：SwiftUI 或 Storyboard
   - **Language**：Swift
3. 选择保存路径，勾选 Git 仓库（推荐）

### 默认生成文件

| 文件 | 用途 |
|---|---|
| `AppDelegate.swift` | App 生命周期（UIKit），通常无需修改 |
| `SceneDelegate.swift` | 窗口/Scene 管理（iOS 13+） |
| `ContentView.swift` | SwiftUI 入口视图 |
| `Assets.xcassets` | 图片/颜色资源管理 |
| `Info.plist` | App 权限声明（相机/位置/通知等） |

## 模拟器

```
Xcode Toolbar → 设备下拉菜单 → 选择 iPhone 15 / 其他机型
Cmd+R → 启动模拟器运行 App
```

**常用模拟器操作**：

| 操作 | 方法 |
|---|---|
| 旋转屏幕 | `Cmd+←` / `Cmd+→` |
| 截图 | `Cmd+S` |
| 模拟位置 | Debug → Simulate Location |
| 模拟摇晃 | Device → Shake |
| 清除 App 数据 | Device → Erase All Content |

## Swift Playground

用于快速原型验证，无需完整 App 项目：

```
File → New → Playground → Blank
```

支持实时预览（`PlaygroundPage.current.liveView`）。适合算法练习、API 探索、UI 原型。

## Xcode Organizer

管理 Archives（归档包）和设备崩溃日志：

```
Window → Organizer（Cmd+Opt+Shift+O）
```

- **Archives**：所有 Archive 版本，可直接上传 App Store 或导出 IPA
- **Crashes**：用户设备上传的崩溃报告（需 App Store 分发）

## Xcode Cloud（CI/CD）

Apple 官方 CI/CD 服务，与 Xcode 深度集成：

1. **Product → Xcode Cloud → Create Workflow**
2. 配置触发条件（Push to main / PR / 定时）
3. 配置构建、测试、分发步骤（TestFlight/App Store）
4. 连接 GitHub/GitLab/Bitbucket 仓库

免费额度：25 计算小时/月（2024 年数据）。超出按需付费。

## 调试技巧

```swift
// LLDB 常用命令（在 Debug 控制台输入）
po variableName        // 打印对象描述
p variableName         // 打印变量值
bt                     // 打印调用栈
thread list            // 列出所有线程
```

**Memory Graph**：Debug → Memory Graph Debugger，可视化对象引用关系，排查循环引用。

## 关联页面

- [[concepts/swift-fundamentals]] — Swift 语言基础
- [[concepts/swiftui-framework]] — SwiftUI 开发
- [[skills/ios-app-store-publishing]] — Xcode Archive 与发布
- [[entities/ios17-app-development-book]] — 来源书籍
