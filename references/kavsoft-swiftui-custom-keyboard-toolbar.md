---
title: "SwiftUI iOS 26 自定义键盘工具栏：safeAreaInset + 可展开 glass menu"
category: references
tags:
  - swiftui
  - ios-26
  - xcode
  - kavsoft
  - ui
  - animation
  - tutorial
sources:
  - "https://www.youtube.com/watch?v=W30FV6QBTok"
source_url: "https://www.youtube.com/watch?v=W30FV6QBTok"
created: "2026-09-06T14:35:00Z"
updated: "2026-09-06T14:35:00Z"
summary: "Kavsoft 教程：iOS 26 自定义可展开键盘工具栏（仿 Apple Notes 风格），核心是 safeAreaInset 与键盘同步、可复用的 ExpandableGlassMenu<Content, Label>: View, Animatable 组件。"
affinity:
  ios: 1.0
  swiftui: 1.0
promotion_status: project
provenance:
  extracted: 0.82
  inferred: 0.15
  ambiguous: 0.03
base_confidence: 0.62
lifecycle: draft
lifecycle_changed: "2026-09-06"
tier: supporting
---

# SwiftUI iOS 26 自定义键盘工具栏

Kavsoft 7 分钟 SwiftUI 教程：用 `safeAreaInset` + 自建 `ExpandableGlassMenu` 通用组件，重现 Apple Notes 风格的"展开/收起"键盘工具栏。技术核心是**让自定义底部栏跟随键盘显隐同步**，避免默认 toolbar 与键盘脱钩的"消失过渡不连贯"问题。

> **来源**：Kavsoft 视频 [W30FV6QBTok](https://www.youtube.com/watch?v=W30FV6QBTok)（4 个月前发布，3522 次观看，SwiftUI 7.0 Tutorials | WWDC 2025 系列）
> **字幕**：YouTube 无官方字幕轨（fabric/yt-dlp 均抓不到 VTT）；视频内嵌英语字幕在画面中（文字冒泡）→ 蒸馏通过视频帧抽帧完成。

## 核心问题

iOS 17 之前 SwiftUI 没有"键盘工具栏"的一等 API。常见替代是 `.toolbar` + `ToolbarItem(placement: .keyboard)`，但 Apple 自身不鼓励把键盘栏做太花（Apple Notes 是为数不多的例外）。本教程绕开限制用 `safeAreaInset` 重做。

视频开头引述的官方说明（从画面字幕转写）：

> The default keyboard toolbar only appears when the keyboard is active, and the standard bottom bar doesn't automatically move above the keyboard—even if you toggle it using the isKeyboardActive property. This leads to subpar animation behavior, especially because the keyboard and bottom bar aren't properly synchronized. The mismatch becomes noticeable during dismissal, where the transition feels inconsistent.

> A better approach is to build a custom bottom bar using the safeAreaInset modifier. It behaves like a regular bottom bar, but importantly, it adjusts its position along with the keyboard, resulting in much smoother animations.

## 起点：标准 toolbar

视频先用 Apple Notes 风格的标准 SwiftUI 写法做起点（演示位于 1:00 帧）：

```swift
struct ContentView: View {
    var body: some View {
        NavigationStack {
            TextEditor(text: $text)
                .scrollContentBackground(.hidden)
                .safeAreaPadding(15)
                .navigationTitle("Notes")
                .toolbarTitleDisplayMode(.inlineLarge)
                .toolbar {
                    ToolbarItem(placement: .topBarTrailing) {
                        Button("Share", systemImage: "square.and.arrow.up") { }
                    }
                    ToolbarItem(placement: .topBarTrailing) {
                        Button("Options", systemImage: "ellipsis") { }
                    }
                    ToolbarSpacer(.fixed, placement: .topBarTrailing)
                    ToolbarItem(placement: .topBarTrailing) {
                        Button("Done", systemImage: "checkmark") { }
                    }
                }
        }
    }
}
```

此写法的问题：custom bottom bar 与 keyboard active 状态不同步。

## 解决：safeAreaInset 替代底部

`safeAreaInset(edge: .bottom)` 是 iOS 15+ 的 modifier，行为类似普通 `.bottom` 锚定，但**会自动随键盘显隐调整位置**——这正是教程的核心 insight。配合 `@FocusState` 检测键盘状态即可驱动工具栏的"折叠/展开"动画。

## 复用核心：ExpandableGlassMenu 组件

视频自建了一个**通用的可展开菜单组件**，签名（来自 4:10 帧代码）：

```swift
struct ExpandableGlassMenu<Content: View, Label: View>: View, Animatable {
    var alignment: Alignment
    var progress: CGFloat                       // 0 = 收起, 1 = 展开
    var labelSize: CGSize = .init(width: 55, height: 55)
    var cornerRadius: CGFloat = 30
    @ViewBuilder var content: Content           // 展开后的多个按钮
    @ViewBuilder var label: Label               // 折叠态的圆形触发器

    @State private var contentSize: CGSize = .zero
    var animatableData: CGFloat { ... }         // 关键：自定义 Animatable
}
```

**设计要点**：

- `Animatable` 协议 + `animatableData: CGFloat` —— SwiftUI 动画管线能直接驱动 `progress` 数值，进而驱动形状/尺寸插值，**比 boolean 切换过渡顺滑得多**
- 双 `@ViewBuilder` 槽位：`label`（折叠态触发器）+ `content`（展开态内容），调用方完全自定义
- `contentSize` 状态由 `GeometryReader`/PreferenceKey 测量，用于扩展时撑开容器
- `cornerRadius: 30` + `labelSize: 55x55` —— 折叠态是一个正圆，展开时通过 progress 数值过渡成圆角矩形容器
- `.buttonStyle(.glass)` —— iOS 26 新的 glass 效果（与 iOS 26 Liquid Glass 设计语言一致）

## 完整 ContentView 关键段

来自 6:00 帧的最终代码片段：

```swift
} label: {
    HStack(spacing: 20) {
        BaseActions()                            // 展开态的内嵌内容
    }
    .font(.title3)
    .foregroundStyle(Color.primary)
}
.frame(height: 45)
.zIndex(1)

Button {
    // 切换菜单可见性
} label: {
    Image(systemName: "square.and.pencil")
        .font(.title3)
        .frame(width: 25, height: 35)
}
.buttonStyle(.glass)
.buttonBorderShape(.circle)
.opacity(isKeyboardActive ? 0 : 1)             // 键盘激活时整体淡出
.blur(radius: isKeyboardActive ? 5 : 0)        // 配合 blur 软退出
.scaleEffect(isKeyboardActive ? 0.5 : 1)
.padding(.horizontal, 15)
.animation(.interactiveSpring(response: 0.6, dampingFraction: 0.75),
           value: isKeyboardActive)
```

## 关键技术点

| 技术 | 说明 |
|------|------|
| `safeAreaInset(edge: .bottom)` | 替代 `.bottom` 锚定，自动跟随键盘位置（**核心创新点**） |
| `@FocusState` | 检测 keyboard active 状态，驱动动画 trigger |
| `View, Animatable` + `animatableData: CGFloat` | 让进度数值 0→1 由 SwiftUI 动画管线自动插值 |
| `.buttonStyle(.glass)` | iOS 26 新 API（与 Liquid Glass 设计语言同步） |
| `.buttonBorderShape(.circle)` | glass style 配套，圆形触发器 |
| `interactiveSpring(response: 0.6, dampingFraction: 0.75)` | 软弹性，跟手效果好 |
| `opacity + blur + scaleEffect` 三联 | 键盘激活时 `.square.and.pencil` 触发器优雅淡出 |

## 演示效果

视频缩略图（封面）与 6:00 帧的 simulator 截图都展示了两种状态：

- **折叠态**：键盘未激活，底部仅显示一个圆形 `.square.and.pencil` 触发器（居中按钮）
- **展开态**：键盘激活时，触发器淡出 + 圆角矩形容器从底部滑入，内含 5-6 个格式按钮（粗体/斜体/字号等）

两种状态通过 `interactiveSpring` 软切换，过渡曲线与键盘显隐一致。

## 复用场景

- **笔记 App**：Apple Notes 风格编辑器的工具栏（与 dayfold 项目直接相关）
- **聊天 App**：输入框上方的 quick-action（emoji / 相册 / 语音）
- **表单填写**：键盘激活时弹出常用快速项
- **可定制 IME 替代品**：第三方键盘 App 的核心组件

## 视频元数据

- **作者**：Kavsoft（[YouTube 频道](https://www.youtube.com/@Kavsoft)，5.59 万订阅）
- **系列**：SwiftUI 7.0 Tutorials | WWDC 2025（102 个视频）
- **时长**：7:20
- **演示项目**：CustomTFT（Source Code 需 Patreon 订阅获取）
- **技术栈**：SwiftUI / iOS 26 / Xcode 26
- **相关视频**：[Custom Liquid Morphing Menu Effect](https://www.youtube.com/watch?v=Qutp-v-g2Iw)（同作者的姊妹教程）

## 蒸馏过程注记

- 本视频**无 YouTube 自动字幕**（yt-dlp / fabric 都失败），字幕轨道实际为画面内嵌的英语字幕气泡
- 用 chrome 浏览器通过 `video.currentTime = N` 跳帧 + screenshot 抓取 5 个关键时间点（0:00 / 1:00 / 2:00 / 4:10 / 6:00）覆盖：封面 → 标准 toolbar 起点 → 问题陈述 → 组件实现 → 最终 ContentView
- 代码片段由视觉转录，可能有微小字面差异（Swift 标识符、参数名按上下文补全）

## 相关页面

- [[concepts/swiftui-keyboard-toolbar-safeareainset-pattern]] — **核心概念**:`safeAreaInset(edge: .bottom)` 模式的完整抽象(避免 ZStack 浮层 + padding 的反模式),与本教程蒸馏互为表里
- [[concepts/swiftui-context-propagation]] — SwiftUI 状态注入的通用模式
- [[skills/ios-app-store-publishing]] — Xcode 项目配置基础
- [[projects/dayfold/dayfold]] — 含 [[projects/dayfold/skills/entry-editor-image-dirty-tracking]] 等笔记编辑器相关 skill，本教程的"键盘工具栏 + 自定义格式按钮"模式可迁移到 dayfold 的 [[projects/dayfold/skills/swiftui-editor-scrollview-vs-attachment]] 编辑器场景
- [[references/swiftui-ios26-toolbar-transitions-morphing]] — **iOS 26 同代姊妹资源**：屏幕间工具栏变形（DefaultToolbarItem + ToolbarSpacer + toolbar(id:)），与本键盘工具栏主题互补
- [[concepts/swiftui-animatablemodifier-pattern]] — `ExpandableGlassMenu: View, Animatable` 的协议抽象提炼（vault 总结）
- [[synthesis/Research: SwiftUI Custom Animation Toolbar in iOS 26]] — 3 轮研究综合 master synthesis，含 vault iOS 26 toolbar 10 页 + 1 master 矩阵