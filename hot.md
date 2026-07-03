---
title: Hot Cache
updated: 2026-07-02T01:00:00Z
---

# Hot Cache

*A ~500-word semantic snapshot of recent activity. Updated after every major write operation.*

## Recent Activity

- [2026-07-02T01:00:00Z] INGEST `_raw/zustand.txt`（Gitingest 导出，pmndrs/zustand 源码 + 文档，3.1 万行）— 创建 7 页：实体页（Zustand 定位与对比）、核心架构（createStore ~30 行实现：Object.is + 浅合并 + Set<Listener>，StoreApi 接口，双层 vanilla/react 架构）、中间件系统（StoreMutators 开放扩展类型，persist/devtools/immer/redux/subscribeWithSelector 详解）、React 集成（useSyncExternalStore 原理，useShallow 浅比较实现）、最佳实践（Slices/外部 Actions/重置/Map-Set/URL 同步）、SSR/Next.js（per-request store + Context 模式）、TypeScript（双括号语法原因、Slices 类型、中间件组合）。与 Trek 项目的 Zustand 使用已交叉链接。
- [2026-07-02T00:30:00Z] INGEST `_raw/trek.txt`（Gitingest 导出，33 万行）— Trek 自托管旅行计划器，创建 8 页：项目总览、架构概览（NestJS 模块 + React Zustand 切片 + 离线优先 PWA）、插件系统（9 个插件管理员可切换）、MCP 服务器（OAuth 2.1 + 150 工具 + 27 scope）、实时同步（WebSocket Room 模型 + MutationQueue 离线队列）、认证系统（JWT/OIDC/Passkeys/MFA/OAuth 2.1）、数据库表结构（SQLite，~40 张表）、环境变量参考。
- [2026-07-02T00:20:00Z] INGEST Clippings/（8个新文件）— 创建 6 页：**llm-speculative-decoding**（DSpark 推测解码框架，半自回归架构 + 置信度调度，DeepSeek 线上 60–85% 加速）；**ios-sideloading-fundamentals**（调试/发布证书区别、JIT 原理、SideStore/LiveContainer 机制对比，iOS 26.4 RPPairing 变化）；**ios-emulator-setup**（ManicEMU 3DS + MeloNX Switch 侧载配置，JIT 必须通过 StikDebug）；**hackintosh-mini-build**（5000 元黑苹果对标 Mac Studio + DIY MacBook Pro 2019 拆机件清单）；**mechanical-watch-mechanics**（机械表七部件能量链）；**fire-emblem-mystery-chapter1**（FE 第1章攻略）。更新 feather-ios-sideload 补充 JIT 局限说明。
- [2026-07-02T00:10:00Z] CROSS_LINK — 扫描 61 页，新增 43 个链接，修改 24 个文件；typed relations 写入 frontmatter；仅剩 1 个孤立页面（entities/feather-ios-sideload）。主要连接：ios17-app-development-book ↔ arc/concurrency/networking/multithreading/xcode/appstore；nintendo-wansui ↔ 全部 ique-dsi 技能页；ios concepts ↔ ios skills 双向关联；两个跨项目链接（jrfed ↔ xk-ai-talk-desk）。
- [2026-07-02T00:01:00Z] TAG_NORMALIZE — 规范化 76 个文件；保留 `dsi`/`DSTWO` 原样；删除占位标签 `标签1`/`标签2`；未知标签合并（`strategy`→`game`、`磁盘管理`→`macos`、`日本`→`travel` 等）；别名统一（`gcd`/`dispatchqueue`/`multithreading`→`concurrency`、`urlsession`/`alamofire`→`networking` 等）。
- [2026-07-01T12:30:00Z] WIKI_UPDATE jrfed-zaxd-mediation-tool — 首次同步，创建 6 页：项目总览（协谈工具 Chrome 扩展）、权限管控体系（usePermission Hook）、MV3 三层架构（Content Script 双世界注入）、Zustand+Chrome Storage 持久化、神策 SDK 双脚本方案、源码目录布局
- [2026-07-01T12:00:00Z] INGEST iOS 17 App Development for Beginners.epub — Arpit Kulsreshtha 著 iOS 17 开发入门书（Swift 5.9/SwiftUI/Xcode 15），蒸馏为 12 页：书籍实体、Swift 基础/SwiftUI 框架/ARC 内存/Swift 并发/iOS 架构模式（概念页）、数据持久化/网络编程/多线程/App Store 发布/Xcode IDE（技能页）、设计模式速查（参考页）
- [2026-07-01T00:00:00Z] INGEST DSiSoftware.pdf — 神游 DSi 官方操作说明书（操作篇），蒸馏为 12 页：主机实体、趣照/趣音/Wi-Fi/亲子管理/PictoChat/下载游戏技能页、商店/系统设置/菜单软件/网络术语参考页、任天狗狗实体页
- [2026-06-29T09:30:00Z] INGEST Clippings/ — 15 个网页剪藏蒸馏为 13 个 wiki 页面，覆盖 Claude Code 优化、前端核心概念、复古游戏与工具类知识

## Key New Additions

**jrfed-zaxd-mediation-tool（新建）**：金融客服协谈助手 Chrome 扩展首次同步，创建 6 页。核心架构决策：MV3 三层（Background SW + SidePanel + Content Script），双 Content Script 解决神策 SDK 主世界注入问题（`world: "MAIN"`），`chrome.storage.local` 替代 localStorage 的 `chromeStorage` 适配器接入 Zustand persist，三级权限管控（MENU_/BTN_/FW_）通过 `usePermission` Hook 驱动条件渲染。

## Active Threads

**jrfed-zaxd-mediation-tool（进行中）**：金融客服 Chrome 扩展，MV3 + React + Zustand + Antd。最近迭代聚焦权限管控：历史订单页 `BTN_EQUITY_HIST_QUERY` 缺失导致空白 bug、接口 URL 空格 404 问题均已修复。项目含提前结清/安抚金/权益计算/投诉列表/征信核身/供应商工单/原单退款共 9 个功能模块。

**dayfold（进行中）**：iOS 18+ 暖色日记 App，SwiftUI + Core Data/CloudKit 同步。核心架构：抽屉式导航（85% 屏宽）替代 TabBar，MVVM + 共享 CoreDataStack 单例，无 iCloud 自动降级本地。

**xk-ai-talk-desk-ui（进行中）**：AI 外呼热转坐席前端，`dev_1.0.0` 分支活跃开发。核心是 `useSoftbar` Hook 封装信科 LaihuAPI，事件驱动管理通话生命周期。

**Claude Code 知识集群**：已建立 `skills/claude-code-token-optimization` 和 `skills/claude-code-settings` 两个核心页面，`concepts/prompt-caching` 作为理论基础页面支撑两者。

**前端核心概念**：已建立 Event Loop → 浏览器进程模型 → 存储缓存 → 移动端定时器四页互链体系。

## Key Takeaways

- **Chrome 扩展禁用 localStorage**：Content Script 与宿主页面共享 localStorage 会造成键名冲突，必须用 `chrome.storage.local`；通过 `chromeStorage` 适配器可直接接入 Zustand persist（[[projects/jrfed-zaxd-mediation-tool/skills/zustand-chrome-storage]]）
- **神策 SDK 主世界注入**：Content Script 默认在隔离世界，无法访问 `window.sensorsData*`；用 `world: "MAIN"` 额外注入一个脚本初始化 SDK，两个脚本同一页面并存（[[projects/jrfed-zaxd-mediation-tool/skills/sensorsdata-dual-world]]）
- **权限控制无路由守卫**：侧边栏扩展没有 URL 变化，权限失效只通过 `usePermission` 隐藏 UI 元素，不做路由跳转（[[projects/jrfed-zaxd-mediation-tool/concepts/permission-system]]）
- **Core Data + CloudKit 优雅降级**：监听 `NSCocoaErrorDomain 134400` → 清空 `cloudKitContainerOptions` → 二次 `loadPersistentStores`，避免在无 iCloud 设备上刷错误日志
- **SwiftUI sheet/cover 上下文不继承**：必须显式 `.environment(\.managedObjectContext, context)`，否则子视图写入不会触发外层 `@FetchRequest` 刷新（dayfold 历史上多个 fix 都围绕这个坑）
- **EntryEditor 图片脏标记模式**：`@Published var images` 的 `didSet` + `isLoadingImages` 守卫，避免 auto-save 时把刚加载的旧图当"未改动"或"已改动"误判
- **信科 CC SDK 集成关键**：双通道签入（CC only vs CC+WebRTC），外呼号码须加 `9` 前缀；`DeliveredEvt.dialogue` 携带 AI 对话历史，是热转场景的核心数据
- Claude Code 提示缓存：**缓存热时继续聊比重开更便宜**；1M 上下文慎用（缓存失效代价极高）
- 移动端定时器不准根因：浏览器对后台页面冻结定时器；解法：visibilitychange + 服务器时间差值
- NDS 最佳烧录卡：DS Two（已停售）；GBA Slot-2：SuperCard Mini SD + SuperFW 固件

## Flagged Contradictions

*None yet.*
