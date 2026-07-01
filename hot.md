---
title: Hot Cache
updated: 2026-07-01T12:00:00Z
---

# Hot Cache

*A ~500-word semantic snapshot of recent activity. Updated after every major write operation.*

## Recent Activity

- [2026-07-01T12:00:00Z] INGEST iOS 17 App Development for Beginners.epub — Arpit Kulsreshtha 著 iOS 17 开发入门书（Swift 5.9/SwiftUI/Xcode 15），蒸馏为 12 页：书籍实体、Swift 基础/SwiftUI 框架/ARC 内存/Swift 并发/iOS 架构模式（概念页）、数据持久化/网络编程/多线程/App Store 发布/Xcode IDE（技能页）、设计模式速查（参考页）
- [2026-07-01T00:00:00Z] INGEST DSiSoftware.pdf — 神游 DSi 官方操作说明书（操作篇），蒸馏为 12 页：主机实体、趣照/趣音/Wi-Fi/亲子管理/PictoChat/下载游戏技能页、商店/系统设置/菜单软件/网络术语参考页、任天狗狗实体页
- [2026-06-29T11:00:00Z] WIKI_UPDATE dayfold — 首次同步，创建 11 页：项目总览、架构概览、CloudKit 降级、SwiftUI context 注入、FetchRequest vs ObservedObject、抽屉导航、EntryEditor 图片脏标记、软删除回收箱、暖色主题 token、左滑删除容器、源码目录布局
- [2026-06-29T09:30:00Z] INGEST Clippings/ — 15 个网页剪藏蒸馏为 13 个 wiki 页面，覆盖 Claude Code 优化、前端核心概念、复古游戏与工具类知识

## Key New Additions

**iOS 17 知识集群（新建）**：已建立覆盖 iOS 开发全栈的 12 页互链体系。核心概念：Swift 5.9 类型系统+闭包+可选值（`concepts/swift-fundamentals`）、SwiftUI 声明式 UI+状态管理+已知 sheet 陷阱（`concepts/swiftui-framework`）、ARC 强/弱/无主引用+循环引用（`concepts/arc-memory-management`）、async/await+Task+Actor+MainActor（`concepts/swift-concurrency`）、MVC/MVVM/VIPER/Redux 对比（`concepts/ios-app-architecture`）。技能页：Core Data/SwiftData CRUD（与 dayfold 深度互链）、URLSession/Alamofire 网络、GCD/DispatchGroup 多线程、App Store 发布流程（证书→Archive→TestFlight）、Xcode 15 IDE 速查。参考页：GoF 23 种设计模式 + iOS 反模式清单。

## Active Threads

**dayfold（进行中）**：iOS 18+ 暖色日记 App，SwiftUI + Core Data/CloudKit 同步。核心架构：抽屉式导航（85% 屏宽）替代 TabBar，MVVM + 共享 CoreDataStack 单例，无 iCloud 自动降级本地。最近 30 个 commit 集中在 UI 打磨（列表样式/左滑删除/回收箱/地图页面），架构层面稳定。

**xk-ai-talk-desk-ui（进行中）**：AI 外呼热转坐席前端，`dev_1.0.0` 分支活跃开发。核心是 `useSoftbar` Hook 封装信科 LaihuAPI，事件驱动管理通话生命周期。当前迭代聚焦：热转/手动详情字段调整、电话条样式优化、日期组件优化。

**Claude Code 知识集群**：已建立 `skills/claude-code-token-optimization` 和 `skills/claude-code-settings` 两个核心页面，`concepts/prompt-caching` 作为理论基础页面支撑两者。

**前端核心概念**：已建立 Event Loop → 浏览器进程模型 → 存储缓存 → 移动端定时器四页互链体系。

## Key Takeaways

- **Core Data + CloudKit 优雅降级**：监听 `NSCocoaErrorDomain 134400` → 清空 `cloudKitContainerOptions` → 二次 `loadPersistentStores`，避免在无 iCloud 设备上刷错误日志
- **SwiftUI sheet/cover 上下文不继承**：必须显式 `.environment(\.managedObjectContext, context)`，否则子视图写入不会触发外层 `@FetchRequest` 刷新（dayfold 历史上多个 fix 都围绕这个坑）
- **EntryEditor 图片脏标记模式**：`@Published var images` 的 `didSet` + `isLoadingImages` 守卫，避免 auto-save 时把刚加载的旧图当"未改动"或"已改动"误判
- **信科 CC SDK 集成关键**：双通道签入（CC only vs CC+WebRTC），外呼号码须加 `9` 前缀；`DeliveredEvt.dialogue` 携带 AI 对话历史，是热转场景的核心数据
- Claude Code 提示缓存：**缓存热时继续聊比重开更便宜**；1M 上下文慎用（缓存失效代价极高）
- 移动端定时器不准根因：浏览器对后台页面冻结定时器；解法：visibilitychange + 服务器时间差值
- NDS 最佳烧录卡：DS Two（已停售）；GBA Slot-2：SuperCard Mini SD + SuperFW 固件

## Flagged Contradictions

*None yet.*
