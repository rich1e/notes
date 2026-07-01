---
title: Hot Cache
updated: 2026-06-29T11:00:00Z
---

# Hot Cache

*A ~500-word semantic snapshot of recent activity. Updated after every major write operation.*

## Recent Activity

- [2026-06-29T11:00:00Z] WIKI_UPDATE dayfold — 首次同步，创建 11 页：项目总览、架构概览、CloudKit 降级、SwiftUI context 注入、FetchRequest vs ObservedObject、抽屉导航、EntryEditor 图片脏标记、软删除回收箱、暖色主题 token、左滑删除容器、源码目录布局
- [2026-06-29T10:00:00Z] WIKI_UPDATE xk-ai-talk-desk-ui — 首次同步，创建 4 页：项目总览、CC SDK 集成（useSoftbar）、坐席状态机、PhoneBar 通话流程
- [2026-06-29T09:30:00Z] INGEST Clippings/ — 15 个网页剪藏蒸馏为 13 个 wiki 页面，覆盖 Claude Code 优化、前端核心概念、复古游戏与工具类知识

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
