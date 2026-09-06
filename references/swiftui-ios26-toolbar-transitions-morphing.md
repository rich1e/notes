---
title: "iOS 26 Native Toolbar Transitions & Morphing —— SwiftUI 26 的工具栏变形"
category: references
tags:
  - swiftui
  - ios-26
  - xcode
  - toolbar
  - navigation
  - liquid-glass
  - wwdc-2025
sources:
  - "https://hasanalidev.medium.com/ios-26-swiftui-toolbar-transitions-morphing-in-toolbar-0bd69fd803bf"
source_url: "https://hasanalidev.medium.com/ios-26-swiftui-toolbar-transitions-morphing-in-toolbar-0bd69fd803bf"
created: "2026-09-06T15:15:00Z"
updated: "2026-09-06T15:15:00Z"
summary: "iOS 26 SwiftUI 引入 4 个 native Toolbar APIs 实现屏幕间工具栏变形（DefaultToolbarItem / ToolbarSpacer / toolbar(id:) / view-attached .toolbar）；模仿 Apple Mail / Notes / Safari 的工具栏随导航变形效果。"
affinity:
  ios: 1.0
  swiftui: 1.0
promotion_status: project
provenance:
  extracted: 0.85
  inferred: 0.10
  ambiguous: 0.05
base_confidence: 0.72
lifecycle: draft
lifecycle_changed: "2026-09-06"
tier: supporting
---

# iOS 26 Native Toolbar Transitions & Morphing

来源：[Hasan Ali Siseci on Medium](https://hasanalidev.medium.com/ios-26-swiftui-toolbar-transitions-morphing-in-toolbar-0bd69fd803bf)（2025-12-15，7 分钟阅读；通过 Freedium.mhtml 镜像访问）
本地副本：`/Users/rich1e/Downloads/iOS 26 — SwiftUI Toolbar Transitions — Morphing in Toolbar - Freedium.mhtml`

## 主题区分

本文档主题是**屏幕间工具栏变形**（navigation-driven toolbar morphing），与 vault 现有的键盘工具栏主题不同：

| 主题 | 关注点 | 文档 |
|------|--------|------|
| 键盘工具栏跟随键盘 | `safeAreaInset` vs ZStack + offset | [[concepts/swiftui-keyboard-toolbar-safeareainset-pattern]] |
| 可展开工具栏菜单 | `Animatable` 自建组件 | [[references/kavsoft-swiftui-custom-keyboard-toolbar]] |
| 屏幕间工具栏变形（本页） | 4 个 native iOS 26 APIs | 本页 |

## 核心命题

> **iOS 26 之前**：SwiftUI 工具栏是静态 UI 元素，跨屏幕导航时直接消失重绘。
> **iOS 26**：SwiftUI 提供 native APIs，让工具栏**作为导航的自然参与者**——随屏幕切换平滑变形（morph）。

Apple Mail（搜索栏 → 操作按钮）、Safari、App Store、Photos 早已实现此效果；iOS 26 让 SwiftUI 也能做出同等效果。

## 4 个核心 APIs

### 1. `DefaultToolbarItem(kind: .search, placement: .bottomBar)`

把**系统组件**（如搜索框）直接嵌入工具栏，让搜索栏成为工具栏的自然成员，而非顶部独立的导航区域。

```swift
.toolbar {
    DefaultToolbarItem(kind: .search, placement: .bottomBar)

    ToolbarSpacer(.fixed, placement: .bottomBar)

    ToolbarItem(placement: .bottomBar) {
        Button { } label: {
            Image(systemName: "gobackward")
        }
    }
}
```

**关键问题解决**：之前 `searchable(text:)` 把搜索框放在导航顶部，与 `.bottomBar` 工具栏分离，无法达到 Apple Notes 那种"工具栏 + 搜索合二为一"的统一感。

### 2. `ToolbarSpacer(.fixed | .flexible, placement: .bottomBar)`

**视觉分隔同 placement 的工具栏项**。

| Spacer 类型 | 用途 |
|------------|------|
| `.fixed` | 固定间距，把按钮"推开"避免视觉粘连 |
| `.flexible` | 弹性填充，把右侧按钮推到屏幕最右 |

**iOS 26 尤为重要**：Liquid Glass 设计语言让按钮形态更立体（`.buttonStyle(.glass)`），没有 spacer 按钮会显得"物理粘在一起"，造成错误 UX。

### 3. `toolbar(id: "STABLE_ID")` —— 让指定按钮"稳定不跳"

变形动画中某些按钮（如"恢复"按钮）会有轻微跳跃。如要避免，把该按钮用 `toolbar(id:)` modifier 单独挂在两个屏幕**同 ID**上：

```swift
// 主屏
.toolbar(id: "UPDATEACTION") {
    ToolbarItem(id: "update", placement: .bottomBar) {
        Button { } label: {
            Image(systemName: "gobackward")
        }
    }
}

// 详情屏（同一个 ID）
.toolbar(id: "UPDATEACTION") {
    ToolbarItem(id: "update", placement: .bottomBar) {
        Button { } label: {
            Image(systemName: "gobackward")
        }
    }
}
```

**Apple 官方描述**：`toolbar(id:)` "Populates the toolbar or navigation bar with the specified items, allowing for user customization."

`toolbar(id:)` 同时是**用户可自定义性**的入口——用户能在系统设置中重排/隐藏这种已声明 ID 的工具栏项。

### 4. `.toolbar` 挂在 NavigationStack 内的 root view 上（而非 NavigationStack 自身）

这是**核心技巧**，触发变形：

```swift
NavigationStack {
    List {
        NavigationLink { MailDetailView() } label: { /* ... */ }
    }
    .toolbar {  // ⚠️ 挂在内层 root view，不是 NavigationStack
        // 主屏工具栏
    }
}
```

主屏和详情屏都这样挂，**iOS 26 自动 morph**——详情屏的工具栏会替换主屏的，按钮间有平滑过渡动画。

## 完整示例：Mail app 风格

```swift
struct MailView: View {
    @State private var searchText: String = ""
    var body: some View {
        NavigationStack {
            List {
                NavigationLink {
                    MailDetailView()
                } label: {
                    HStack(spacing: 10) {
                        RoundedRectangle(cornerRadius: 10).fill(.fill).frame(width: 50, height: 50)
                        VStack(alignment: .leading, spacing: 6) {
                            Text("Medium").fontWeight(.semibold)
                            Text("Your article published").font(.caption)
                        }
                    }
                }
            }
            .navigationTitle("Mail")
            .navigationSubtitle(Text("Updated 2 days ago"))
            .toolbar(id: "WRITEACTION") {
                ToolbarItem(id: "WRITE", placement: .bottomBar) {
                    Button { } label: {
                        Image(systemName: "square.and.pencil")
                    }
                }
            }
            .toolbar {
                ToolbarItem(placement: .bottomBar) {
                    Button { } label: {
                        Image(systemName: "line.3.horizontal.decrease")
                    }
                }
                ToolbarSpacer(.fixed, placement: .bottomBar)
                DefaultToolbarItem(kind: .search, placement: .bottomBar)
                ToolbarSpacer(.fixed, placement: .bottomBar)
            }
            .searchable(text: $searchText)
        }
    }
}

struct MailDetailView: View {
    var body: some View {
        VStack { }
            .navigationTitle("Medium")
            .toolbar(id: "WRITEACTION") {
                ToolbarItem(id: "WRITE", placement: .bottomBar) {
                    Button { } label: {
                        Image(systemName: "square.and.pencil")
                    }
                }
            }
            .toolbar {
                ToolbarItem(placement: .bottomBar) {
                    HStack(spacing: 12) {
                        Button { } label: {
                            Image(systemName: "trash").padding(.horizontal, 5)
                        }
                        Button { } label: {
                            Image(systemName: "folder").padding(.horizontal, 5)
                        }
                        Button { } label: {
                            Image(systemName: "arrowshape.turn.up.forward.fill").padding(.horizontal, 5)
                        }
                    }
                    .padding(.horizontal, 5)
                    .buttonStyle(.plain)
                }
                ToolbarSpacer(.flexible, placement: .bottomBar)
            }
    }
}
```

**关键观察**：`WRITEACTION` ID 在主屏和详情屏复用——`square.and.pencil` 按钮不会 morph，保持稳定；其他按钮（搜索/排序/详情操作）会 morph。

## 何时用 vs 不用

| 场景 | 适用 |
|------|------|
| 多层级 navigation（Mail/Notes/Safari 风格）| ✅ 强烈推荐 |
| 单屏 App（无深层导航）| ❌ 没必要 |
| 工具栏按钮形态跨屏不同 | ✅ 用 morphing |
| 工具栏按钮跨屏相同且需稳定 | ❌ 用 `toolbar(id:)` 锁定 |
| 想让用户能重排/隐藏某些按钮 | ✅ 用 `toolbar(id:)` 声明 |
| 工具栏里要放搜索框 | ✅ 必须用 `DefaultToolbarItem(kind: .search, ...)` |

## 与 Apple 设计语言一致性

- **Liquid Glass 按钮**（`.buttonStyle(.glass)`）+ **ToolbarSpacer** 是 iOS 26 视觉一致性的关键组合
- 4 个 API 都来自 iOS 26 / WWDC 2025 SwiftUI 更新
- 与 Kavsoft 教程中的 `.buttonStyle(.glass)` + `.buttonBorderShape(.circle)` 是同一设计语言

## Open Questions

1. `toolbar(id:)` 是否支持用户自定义的所有 extent（重排 / 隐藏 / 替换）？Apple 文档描述模糊。^[ambiguous]
2. `DefaultToolbarItem` 仅支持 `.search`？还是有 `.share`、`.camera` 等其他系统 kind？需 Apple 文档核对。^[ambiguous]
3. morph 动画的具体曲线是什么？是否可调？^[ambiguous]

## 相关页面

- [[concepts/swiftui-keyboard-toolbar-safeareainset-pattern]] — **主题区分**：键盘工具栏 vs 屏幕间工具栏是不同问题
- [[references/kavsoft-swiftui-custom-keyboard-toolbar]] — 同 iOS 26 主题（Liquid Glass 按钮 + Animatable 组件），是同代 API 的姊妹资源
- [[references/volcengine-swiftui-keyboard-toolbar-zstack-offset]] — 键盘工具栏主题，与本页不同主题
- [[projects/dayfold/dayfold]] — dayfold 项目（笔记编辑器），可应用本模式做详情页/编辑页工具栏变形
- [[concepts/swiftui-animatablemodifier-pattern]] — vault AnimatableModifier 协议抽象，4 个 native toolbar API 配合使用时也涉及 Animatable
- [[concepts/swiftui-toolbaritem-placement-semantic-vs-positional]] — Apple ToolbarItemPlacement 双层体系，本页 `DefaultToolbarItem(kind: .search, placement: .bottomBar)` 用的是 positional 路径
- [[synthesis/Research: SwiftUI Custom Animation Toolbar in iOS 26]] — 3 轮研究综合 master synthesis