---
title: Wiki Index
---

# Wiki Index

*This index is automatically maintained. Last updated: 2026-07-26T03:00:00Z*

## Concepts

- [[concepts/ptp-ieee1588]] — IEEE 1588 精确时间协议，四时间戳法实现纳秒级分布式时钟同步
- [[concepts/ptp-bmca]] — BMCA 最佳主时钟选举算法，基于 clockClass/Accuracy/priority 分布式选举
- [[concepts/ptp-clock-types]] — PTP 四种时钟角色：GM 提供时间源，BC 转发，TC 补偿驻留延迟，OC 终端
- [[concepts/ptp-delay-measurement]] — E2E 与 P2P 四时间戳延迟测量机制
- [[concepts/ptp-tlv-extension]] — PTP TLV 插件系统，支撑 IEEE 1588-2019 向后兼容扩展
- [[concepts/ptp-message-types]] — PTP 10 种报文：事件报文（需硬件时间戳）和通用报文
- [[concepts/ptp-port-state-machine]] — PTP 端口 9 种状态，由 BMCA 结果和链路事件驱动转换
- [[concepts/llm-speculative-decoding]] — 推测解码加速 LLM 推理：草稿模型 + 并行验证，DSpark 半自回归架构
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
- [[concepts/zustand-core-architecture]] — Zustand createStore 约 30 行核心：闭包 + Set`<Listener>` + 浅合并，StoreApi 接口设计
- [[concepts/zustand-middleware-system]] — Zustand 中间件系统：StoreMutators 类型扩展、persist/devtools/immer/redux/subscribeWithSelector
- [[concepts/zustand-react-integration]] — Zustand React 层：useSyncExternalStore + 选择器 + useShallow 浅比较防多余重渲染
- [[concepts/macos-window-switcher]] — macOS 窗口切换器：替代 Cmd+Tab 的 app→window 粒度扩展，含 Space 过滤/标签下钻/快速动作
- [[concepts/asciidoc-markup]] — AsciiDoc 标记语言：表格/脚注/交叉引用/属性/条件内容内置，docs-as-code 友好
- [[concepts/animation-easing-functions]] — 缓动函数：Penner 缓动 + Apple 参数化运动学 + 卷积滤波 + PD/PID 反馈控制四条路线
- [[concepts/programming-pattern-categories]] — 编程模式五大分类（数据结构/并发/系统/内存/行为），按运行时职责切分，与 GoF 互补
- [[concepts/fabric-patterns]] — Fabric Patterns：290+ 可复用 AI Prompt 单元，覆盖分析/提取/创作/安全等场景
- [[concepts/mixture-of-experts]] — MoE 混合专家架构：稀疏激活降低每 token 算力，内存与算力的核心权衡
- [[concepts/kimi-delta-attention]] — Kimi Delta Attention：Moonshot 提出的长上下文 KV 缓存优化，100 万 token 下最高 6.3× 加速
- [[concepts/dotfile-manager]] — Dotfile 管理工具五大流派（裸 git/Stow/chezmoi/Nix/云同步）的设计空间与权衡
- [[concepts/chezmoi-three-state-model]] — chezmoi 三态模型：源态/目标态/实际态，`apply` 是协调三个状态的过程
- [[concepts/chezmoi-attribute-prefixes]] — chezmoi 17 个属性前缀（dot_/private_/encrypted_/modify_ 等），命名即元数据
- [[concepts/chezmoi-templating]] — chezmoi 模板系统：Go text/template + sprig 扩展，按机器差异化
- [[concepts/chezmoi-workflow]] — chezmoi 四动词工作流（add/edit/diff/apply）+ update/init + czpush/czpull/czapply 三段式别名
- [[concepts/fourier-series]] — 傅里叶分析：单位圆 + Euler 公式串联复正弦、本轮链与傅里叶级数展开

## Entities

- [[entities/feather-ios-sideload]] — iOS 付费开发者签名工具 Feather
- [[entities/nds-flashcard]] — NDS 烧录卡（R4 / DSTWO）使用指南
- [[entities/neogeo-mame]] — NEOGEO / MAME 模拟器配置
- [[entities/ique-dsi]] — 神游 DSi（iQue DSi）主机，型号 TWL-001(CHN)，双摄/Wi-Fi/内置软件
- [[entities/nintendo-wansui]] — iQue DSi 内置任天狗狗虚拟宠物游戏
- [[entities/ios17-app-development-book]] — iOS 17 App Development for Beginners（书籍），Arpit Kulsreshtha 著，Swift 5.9/SwiftUI/Xcode 15
- [[entities/zustand]] — Zustand：pmndrs 出品的轻量 React 状态管理库，无 Provider，Hook 驱动，~1KB
- [[entities/linuxptp]] — Linux 平台工业级 PTP 实现，包含 ptp4l/phc2sys/pmc 工具
- [[entities/white-rabbit]] — CERN 开发的亚纳秒级时间同步协议，PTP 扩展 + DMTD 相位测量
- [[entities/alttab]] — AltTab：lwouis 出品的开源 macOS 窗口切换器，悬停顶层预览 + 21 语言
- [[entities/bettercmdtab]] — BetterCmdTab：rokartur 出品的永久免费开源 Cmd+Tab 替代，macOS 13+
- [[entities/contexts]] — Contexts：边栏式 macOS 窗口切换器，触控板边缘下滑手势 + 多显示器独立边栏
- [[entities/witch]] — Witch：Many Tricks 出品的付费窗口切换器，多粒度切换器并存
- [[entities/battle-tested-patterns]] — Totoro-jam 出品的开源 46 模式目录项目（React/Linux/Go/PostgreSQL 等代码级编程模式，行号精确引用）
- [[entities/fabric-ai]] — Fabric：danielmiessler 出品的开源 AI 增强框架，290+ Patterns，20+ AI 提供商，Go 编写
- [[entities/kimi-k3]] — Kimi K3：全球首个 3T 级开权重 LLM（2.8T 参数，MoE），代码评测第一，2026-07-27 发布
- [[entities/moonshot-ai]] — Moonshot AI（月之暗面）：Kimi 品牌开发商，K 系列超大规模模型，架构创新应对算力限制
- [[entities/chezmoi]] — chezmoi：twpayne 维护的跨平台 dotfile 管理工具，单 Go 二进制，三态模型 + 模板 + 加密
- [[entities/gnu-stow]] — GNU Stow：symlink 农场式 dotfile 管理器，最简镜像流派代表

## Skills

- [[skills/claude-code-token-optimization]] — Claude Code Token 优化策略（提示缓存 + 会话管理）
- [[skills/claude-code-settings]] — Claude Code 四级配置作用域与权限系统
- [[skills/ios-sideloading-fundamentals]] — iOS 证书类型、JIT 原理、SideStore/LiveContainer 机制完整解析
- [[skills/ios-emulator-setup]] — iOS 上的 3DS（ManicEMU）与 Switch（MeloNX）模拟器安装与 JIT 配置
- [[skills/hackintosh-mini-build]] — 5000 元黑苹果小机箱（对标 Mac Studio），程序员装机指南
- [[skills/tmux]] — Tmux 快捷键速查、推荐配置、关闭会话的 4 种替代方式（kill-server / kill-session -a / :kill-session / exit 级联）
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
- [[skills/zustand-patterns]] — Zustand 最佳实践：Slices、Flux 模式、外部 actions、重置状态、Map/Set、URL 同步
- [[skills/zustand-ssr-nextjs]] — Zustand Next.js SSR：per-request store 工厂函数 + Context Provider 模式
- [[skills/zustand-typescript]] — Zustand TypeScript：双括号语法原因、Slices 类型、中间件组合类型
- [[skills/ptp-implementation]] — ptp-lite 约 1000 行 C 实现：报文编解码、主时钟发布、从时钟偏移计算
- [[skills/ptp-troubleshooting]] — PTP 故障排查：pmc 诊断工具、日志解读、常见问题处理
- [[skills/pattern-study-method]] — 用 battle-tested-patterns 系统学习 46 模式：4 阶段路径 + 配套练习 + AI 编程助手技能（adopt-pattern/audit-pattern）
- [[skills/fabric-usage-patterns]] — Fabric CLI 高频用法：YouTube 分析、Shell 别名、REST API、Obsidian 集成
- [[skills/chezmoi-bitwarden-secrets]] — chezmoi Bitwarden 密钥注入 + 跨平台 Keychain/DPAPI 自动解锁 + git-filter-repo 历史清理

## Synthesis

- [[synthesis/Research: chezmoi]] — chezmoi 3 轮研究综合：三态模型 + 17 前缀 + Go 模板 + age/GPG + 四动词工作流

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
- [[projects/trek/trek]] — Trek 自托管实时协同旅行计划器（NestJS + React + SQLite + MCP）
- [[projects/trek/concepts/architecture-overview]] — Monorepo 架构，NestJS 模块化后端 + React SPA + 单容器部署
- [[projects/trek/concepts/addon-system]] — 管理员可切换的插件系统（Lists/Costs/Collab/Atlas/Journey/MCP 等）
- [[projects/trek/concepts/mcp-server]] — 内置 MCP 服务器，OAuth 2.1，150+ 工具，27 个 scope
- [[projects/trek/concepts/realtime-sync]] — WebSocket Room 模型广播 + MutationQueue 离线同步
- [[projects/trek/concepts/auth-system]] — JWT + OIDC + WebAuthn Passkeys + TOTP MFA + OAuth 2.1
- [[projects/trek/references/database-schema]] — SQLite 表结构（users/trips/days/places/addons 等）
- [[projects/trek/references/environment-variables]] — 全量环境变量配置参考

## References

- [[references/mechanical-watch-mechanics]] — 机械表七大部件与能量链原理速查
- [[references/ique-dsi-menu-software]] — iQue DSi 所有内置软件图标一览及软件位置移动方法
- [[references/ique-dsi-system-settings]] — iQue DSi 主机设置四页全部选项（软件管理/亮度/用户信息/亲子管理/互联网）
- [[references/ique-dsi-wifi-glossary]] — iQue DSi 网络术语表（SSID/WEP/WPA/AOSS/WPS等）
- [[references/ique-dsi-shop]] — iQue DSi 商店与 iQue 点数购买、充值、限制说明
- [[references/ios-design-patterns]] — GoF 23 种设计模式速查（创建/结构/行为）+ iOS 常见反模式清单
- [[references/ptp-book-overview]] — PTP技术书（Lularible），41节从思想实验到 LinuxPTP 源码到 ptp-lite 实现
- [[references/macos-window-switchers]] — macOS 窗口切换器对比速查：AltTab / BetterCmdTab / Contexts / Witch 在许可证/macOS 兼容/布局/触发方式上的差异
- [[references/pattern-catalog-battle-tested-patterns]] — battle-tested-patterns 46 模式完整目录（数据结构/并发/系统/内存/行为），每条带"Proven In"精确行号链接
- [[references/cs193p-spring-2025]] — Stanford CS193P Spring 2025 课程参考：Paul Hegarty 主讲，6周叙事式 + 5次作业 + 3周自选项目，SwiftUI 核心课
- [[references/chezmoi-official-site]] — chezmoi.io 官方首页：五大特性 + 单命令引导 + 当前版本
- [[references/chezmoi-templating-guide]] — 官方模板权威说明：Go text/template + sprig + 内置/数据/config 变量来源优先级
- [[references/chezmoi-source-state-attributes]] — 17 个属性前缀 + 2 个后缀的完整参考
- [[references/chezmoi-workflow-discussion]] — GitHub Discussions #2673：v3 方向 + 一周上手 + 七大常见坑
- [[references/chezmoi-encryption-backends]] — chezmoi 加密三后端实操：GPG（非对称/对称）、Gnome Keyring（Linux+macOS Keychain）、KeePassXC（数据库化）
- [[references/chezmoi-bitwarden-keychain]] — Bitwarden 模板注入密钥 + macOS Keychain / Windows DPAPI 免手输主密码 + git-filter-repo 历史清理
- [[references/chezmoi-nix-darwin-integration]] — chezmoi + nix-darwin 分层组合：用户级配置 + 系统级声明，.chezmoidata.yaml profile + Justfile 维护命令
- [[references/chezmoi-patterns-recipes]] — chezmoi 社区实战模式集：安装矩阵、文件名前缀、跨平台变量、加密矩阵、4 种 run_* 钩子、.chezmoiroot/.chezmoiignore 协作
- [[references/kimi-k3-technical-overview]] — Kimi K3 技术深度分析：2.8T MoE、Delta Attention、QAT、基准、定价
- [[references/kimi-k3-geopolitical-context]] — Kimi K3 地缘政治与市场背景：HBM 限制、算力绕过策略、DeepSeek 类比
- [[references/kimi-k3-video-review-lingdu]] — 零度解说实测视频：DeepSWE/LiveBench 基准、虚拟机 Agent 演示、3D 生成、越狱
- [[references/kimi-k3-video-analysis-reportify]] — 哈佛老徐深度分析：Kimi 官方原文、Anthropic Fable-5 禁令、国产芯片全球化路径
- [[references/kimi-k3-official-blog]] — Kimi K3 官方发布博客：代码案例（MiniTriton/芯片设计）、知识工作、Stable LatentMoE 组件、完整基准表

## Synthesis

- [[synthesis/ptp-ieee1588 × linuxptp]] — PTP 协议理论 × LinuxPTP 工业实现：协议 vs 实现的工程空白（PI 伺服、PHC 桥接、硬件时间戳三级精度）
- [[synthesis/trek-auth-system × trek-mcp-server]] — Trek 认证 × MCP 服务器：AI 客户端的认证特化（受众绑定、scope 切分、级联吊销、插件边界）
- [[synthesis/zustand-core-architecture × zustand]] — Zustand 内部架构 × 库品牌：30 行不是省略，是有意暴露（vanilla 闭包 vs React 包装）
- [[synthesis/arc-memory-management × swift-concurrency]] — ARC × Swift Concurrency：同一引用类型的两种正交安全机制（生命周期 vs 访问安全）
- [[synthesis/macos-window-switcher × macos-window-switchers]] — macOS 窗口切换器 概念 × 对比：4 款独立工具为何解决同一问题（结构性局限）
- [[synthesis/consolidation-2026-07-07]] — 2026-07-07 自动合并报告（wiki-lint --consolidate）：PTP 反斜杠修复、chapter1 孤儿拯救
- [[synthesis/Research: Fabric AI Framework]] — Fabric AI 框架研究综合：Patterns 设计哲学、290+ Pattern 分类、多提供商架构、REST API
- [[synthesis/consolidation-2026-07-23]] — 2026-07-23 自动合并报告（wiki-lint --consolidate）：21 个破损链接修复、6 个孤儿救援、4 个 Fabric lifecycle 修复、8 个 tag 规范化
- [[synthesis/swift-fundamentals × swiftui-framework]] — Swift 类型系统是 SwiftUI 的运行时：函数式/POP 范式如何构成 SwiftUI DSL 的基础
- [[synthesis/programming-pattern-categories × ios-app-architecture]] — 代码级五分类 × iOS 架构模式：横切面 vs 纵切面，三层模式语言覆盖不同粒度
- [[synthesis/battle-tested-patterns × ios-design-patterns]] — GoF 对象模式 × battle-tested 代码模式：两套语言的坐标轴，组合使用才能覆盖两个维度
- [[synthesis/ios17-app-development-book × cs193p-spring-2025]] — 书（地图）× 课（罗盘）：两条 iOS/SwiftUI 学习路径的互补结构
- [[synthesis/fabric-patterns × claude-code-settings]] — Fabric Patterns × Claude Code 配置：AI Unix 管道哲学在 Prompt 层与工具层的平行实践
- [[synthesis/Research: Kimi K3]] — Kimi K3 研究综合：3T 级 MoE、Delta Attention、代码第一、整体接近 Fable 5，2026-07-27 权重发布

## Misc

- [[misc/web-github-com-livecontainer-issues-1456]] — SideStore 内置 Refresh All 触发 Unable to manage profiles on the device（LiveContainer 3.7.14 Nightly + iPadOS 26.3）；维护者结论：iOS 26+ 必须用 RPPairing 替代旧 Lockdown 配对文件

## Journal

- [[journal/fire-emblem-new-mystery-prologue]] — FE 新·黑暗龙序章四部分攻略
- [[journal/fire-emblem-mystery-chapter1]] — FE 新·黑暗龙第1章攻略：マルスの旅立ち
- [[journal/nds-flashcard-memories]] — NDS 世代烧录卡横评回忆录
