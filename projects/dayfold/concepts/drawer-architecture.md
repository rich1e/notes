---
title: 抽屉式导航实现
category: project
tags: [ios, swiftui, navigation, animation]
sources: [projects/dayfold]
summary: >-
  MainTabView 用 ZStack + 85% 屏宽 DrawerView 替代 TabBar；内容区用 offset + spring 动画
  横向滑动，整套 0.38/0.82 弹簧参数贯穿全 App。
provenance:
  extracted: 0.65
  inferred: 0.30
  ambiguous: 0.05
base_confidence: 0.78
lifecycle: draft
lifecycle_changed: 2026-06-29
tier: supporting
created: 2026-06-29T00:00:00Z
updated: 2026-06-29T00:00:00Z
---

# 抽屉式导航实现

文件：`dayfold/dayfold/Views/MainTabView.swift`、`SidebarView.swift`

## 为什么不用 TabBar

项目自我定位"温暖文艺"，希望避免 iOS 标准 TabBar 的工具感。采用抽屉式（占屏宽 85%）+
 内容区偏移的方式。

## 实现细节

```swift
GeometryReader { geo in
    let drawerWidth = geo.size.width * 0.85
    let offset: CGFloat = drawerOpen ? drawerWidth : 0

    ZStack(alignment: .leading) {
        DrawerView(selectedTab: $selectedTab, isOpen: $drawerOpen)
            .frame(width: drawerWidth)
            .ignoresSafeArea()

        ZStack { /* 内容区，根据 selectedTab 切换 */ }
            .offset(x: offset)
            .animation(.spring(response: 0.38, dampingFraction: 0.82), value: drawerOpen)
            .shadow(
                color: drawerOpen ? Color.black.opacity(0.4) : Color.clear,
                radius: drawerOpen ? 20 : 0, x: drawerOpen ? -6 : 0, y: 0
            )
            .ignoresSafeArea(edges: .bottom)
    }
}
```

- 抽屉**不做动画**（固定在左）；动画只施加在内容区 offset 上，避免双重缓动叠加。
- 内容区与抽屉**严格等宽**（85%），偏移量等于抽屉宽度时无缝隙。
- 抽屉打开时给内容区加阴影 `radius: 20, x: -6` 增强"浮起"层次感。

## 顶部按钮层

- 抽屉 toggle 按钮（`gearshape`）和首页模式切换按钮（`square.grid.2x2` / `list.bullet`）
  在 `MainTabView` 独立 HStack 层渲染，**与内容区一起偏移**（共享 `.offset(x: offset)`），
  保证按钮始终在内容区可见区域右上角。
- 通过 `UIApplication.shared.connectedScenes` 读真实 `topInset`，避免按钮被刘海/灵动岛
  遮挡（commit `22baee2` 修复）。

## 侧栏分组

`SidebarTab` 枚举两组：

- 组 1 "日记"：`.list` / `.photos` / `.map`
- 组 2 "更多"：`.trash` / `.stats` / `.settings`

第二组用 `Spacer()` + 顶部 `Rectangle()` 分隔线钉在底部。选中 `trash` 不替换内容区，
而是通过 `.onChange(of: selectedTab)` 触发 `showingTrash = true` 用 sheet 弹出
`TrashView`，关闭时 onDismiss 把 `selectedTab` 复位为 `.list`。

## 动画参数一致性 ^[inferred]

`response: 0.38, dampingFraction: 0.82` 是整个抽屉交互的"主键"：抽屉打开/关闭、内容区
tab 切换（`.paperDrop` transition 走 `easeOut(0.38)`）、侧栏行点击全部围绕这个值。
统一动画节奏是项目"温暖"质感的一部分——既不太快显得急促，也不太慢显得迟钝。

## 列表左滑删除与抽屉的冲突

`NotebookDetailView` 的 `SwipeToDeleteRow` 内部用 `DragGesture(minimumDistance: 10)`，
抽屉整体使用 `withAnimation(.spring(...))`；两者不冲突，因为 `NotebookDetailView` 是
`fullScreenCover` 独立呈现，抽屉本身已经处于关闭态。`MainTabView` 抽屉内若要支持
右滑关闭，可考虑用 `simultaneousGesture` 把抽屉开合手势与列表左滑手势解耦。
