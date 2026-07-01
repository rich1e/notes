---
title: Wiki Index
---

# Wiki Index

*This index is automatically maintained. Last updated: 2026-07-01T12:30:00Z*

## Concepts

- [[concepts/prompt-caching]] — LLM 提示缓存机制，KV 缓存复用原理
- [[concepts/javascript-event-loop]] — JavaScript 事件循环：调用栈、微任务、宏任务
- [[concepts/browser-process-model]] — Chrome 多进程架构，Renderer 进程与线程模型
- [[concepts/frontend-storage-cache]] — Cookie / LocalStorage / HTTP 缓存全览
- [[concepts/mobile-timer-accuracy]] — 移动端定时器精度问题与解决方案
- [[concepts/swift-fundamentals]] — Swift 5.9 类型系统、集合、闭包、可选值、协议导向编程
- [[concepts/swiftui-framework]] — SwiftUI 声明式 UI、View 协议、状态管理（@State/@Binding/@ObservedObject）
- [[concepts/arc-memory-management]] — ARC 自动引用计数、强/弱/无主引用、循环引用解决方案
- [[concepts/swift-concurrency]] — async/await、Task/TaskGroup、Actor 数据隔离、MainActor
- [[concepts/ios-app-architecture]] — iOS 架构模式对比：MVC/MVVM/VIPER/Redux 及常见反模式

## Entities

- [[entities/feather-ios-sideload]] — iOS 付费开发者签名工具 Feather
- [[entities/nds-flashcard]] — NDS 烧录卡（R4 / DSTWO）使用指南
- [[entities/neogeo-mame]] — NEOGEO / MAME 模拟器配置
- [[entities/ique-dsi]] — 神游 DSi（iQue DSi）主机，型号 TWL-001(CHN)，双摄/Wi-Fi/内置软件
- [[entities/nintendo-wansui]] — iQue DSi 内置任天狗狗虚拟宠物游戏
- [[entities/ios17-app-development-book]] — iOS 17 App Development for Beginners（书籍），Arpit Kulsreshtha 著，Swift 5.9/SwiftUI/Xcode 15

## Skills

- [[skills/claude-code-token-optimization]] — Claude Code Token 优化策略（提示缓存 + 会话管理）
- [[skills/claude-code-settings]] — Claude Code 四级配置作用域与权限系统
- [[skills/tmux]] — Tmux 快捷键速查与推荐配置
- [[skills/terminal-music]] — macOS 终端本地音乐播放（afplay + shell 函数）
- [[skills/ique-dsi-camera]] — iQue DSi趣照 11种趣味相机、相册、幻灯片、照片管理完整操作
- [[skills/ique-dsi-sound]] — iQue DSi趣音 麦克风录音、声音变换、SD卡 AAC 音乐播放
- [[skills/ique-dsi-wifi-setup]] — iQue DSi Wi-Fi 四种联网方法（AOSS/搜索/USB/手动/WPS）
- [[skills/ique-dsi-parental-control]] — iQue DSi 亲子管理设置、可限制功能、密码找回
- [[skills/pictochat]] — PictoChat 涂鸦聊天最多16人，绘图工具与键盘操作
- [[skills/ique-ds-download-play]] — iQue DS 下载游戏 1台对多台无线游戏广播
- [[skills/xcode-ide-guide]] — Xcode 15 界面布局、快捷键、模拟器、Playground、Organizer、Xcode Cloud
- [[skills/ios-data-persistence]] — UserDefaults/Plist/SQLite/Core Data/SwiftData CRUD 完整指南
- [[skills/ios-networking]] — URLSession/Alamofire REST 请求、JSON 解码、连接可达性检测
- [[skills/ios-multithreading]] — GCD 三种队列、QoS 优先级、DispatchGroup、NSOperation
- [[skills/ios-app-store-publishing]] — 证书/Identifier/Profile 创建、Archive 打包、App Store Connect 配置、TestFlight

## Projects

- [[projects/dayfold/dayfold]] — 暖色风格 iOS 日记 App（SwiftUI + Core Data/CloudKit + MapKit + WeatherKit）
- [[projects/dayfold/concepts/architecture-overview]] — 抽屉式根容器 + MVVM + 共享 CoreDataStack 单例
- [[projects/dayfold/concepts/core-data-cloudkit-fallback]] — CloudKit 134400 降级本地存储实现
- [[projects/dayfold/concepts/swiftui-context-propagation]] — sheet/cover 必须显式注入 managedObjectContext
- [[projects/dayfold/concepts/fetchrequest-vs-observedobject]] — 列表增删 vs 行内属性刷新的两套机制
- [[projects/dayfold/concepts/drawer-architecture]] — 85% 屏宽抽屉 + 0.38/0.82 弹簧贯穿全 App
- [[projects/dayfold/skills/entry-editor-image-dirty-tracking]] — imagesChanged 脏标记避免 MediaAsset 误删
- [[projects/dayfold/skills/soft-delete-with-trash]] — deletedAt 时间戳 + FetchRequest predicate 隔离
- [[projects/dayfold/skills/warm-theme-tokens]] — Color.warmPaper / Font.warmHeadline / .warmCard() 视觉 token
- [[projects/dayfold/skills/swipe-to-delete-row]] — 自定义左滑删除 + 速度阈值 + 圆角并入
- [[projects/dayfold/references/source-tree]] — 源码目录布局与各模块职责
- [[projects/xk-ai-talk-desk-ui/xk-ai-talk-desk-ui]] — AI 外呼热转坐席前端（React 19 + JsSIP + 信科 CC SDK）
- [[projects/xk-ai-talk-desk-ui/concepts/call-center-sdk-integration]] — CC SDK 集成：useSoftbar Hook 封装 LaihuAPI
- [[projects/xk-ai-talk-desk-ui/concepts/agent-state-machine]] — 坐席状态机（agentState + callState 双层设计）
- [[projects/xk-ai-talk-desk-ui/skills/phonebar-call-flow]] — PhoneBar 热转/外呼完整通话流程
- [[projects/jrfed-zaxd-mediation-tool/jrfed-zaxd-mediation-tool]] — 金融客服协谈助手 Chrome 扩展（MV3 + React + Zustand + Antd）
- [[projects/jrfed-zaxd-mediation-tool/concepts/permission-system]] — 菜单/按钮/浮窗三级权限管控，usePermission Hook
- [[projects/jrfed-zaxd-mediation-tool/concepts/chrome-extension-architecture]] — MV3 三层架构与 Content Script 双世界注入策略
- [[projects/jrfed-zaxd-mediation-tool/skills/zustand-chrome-storage]] — Zustand persist + chromeStorage 适配器（禁止 localStorage）
- [[projects/jrfed-zaxd-mediation-tool/skills/sensorsdata-dual-world]] — 神策 SDK world:MAIN 注入方案
- [[projects/jrfed-zaxd-mediation-tool/references/source-tree]] — 源码目录布局

## References

- [[references/ique-dsi-menu-software]] — iQue DSi 所有内置软件图标一览及软件位置移动方法
- [[references/ique-dsi-system-settings]] — iQue DSi 主机设置四页全部选项（软件管理/亮度/用户信息/亲子管理/互联网）
- [[references/ique-dsi-wifi-glossary]] — iQue DSi 网络术语表（SSID/WEP/WPA/AOSS/WPS等）
- [[references/ique-dsi-shop]] — iQue DSi 商店与 iQue 点数购买、充值、限制说明
- [[references/ios-design-patterns]] — GoF 23 种设计模式速查（创建/结构/行为）+ iOS 常见反模式清单

## Synthesis

## Journal

- [[journal/fire-emblem-new-mystery-prologue]] — FE 新·黑暗龙序章四部分攻略
- [[journal/nds-flashcard-memories]] — NDS 世代烧录卡横评回忆录
