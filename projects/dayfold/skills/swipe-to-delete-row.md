---
title: 自定义左滑删除容器
category: project
tags: [mobile, swiftui, animation, design-system, app-architecture]
relationships:
  - target: "[[concepts/swiftui-framework]]"
    type: uses
sources: [projects/dayfold]
summary: >-
  SwipeToDeleteRow 用 DragGesture + 速度阈值判断，半开显示固定 72pt 红色按钮，
  超阈值自动触发删除并动画滑出屏外；圆角在 offset<0 时与首尾圆角并入。
provenance:
  extracted: 0.80
  inferred: 0.15
  ambiguous: 0.05
base_confidence: 0.82
lifecycle: reviewed
lifecycle_changed: 2026-08-03
lifecycle_reason: "auto-promoted by wiki-lint --consolidate: age>30d, confidence>0.7"
tier: peripheral
created: 2026-06-29T00:00:00Z
updated: 2026-08-03T05:47:33Z
---

# 自定义左滑删除容器

文件：`dayfold/dayfold/Views/NotebookDetailView.swift`（文件内私有 `SwipeToDeleteRow`）

## 用 SwiftUI 自带 swipeActions 行不行

`.swipeActions` 在 iOS 16+ 表现可用，但和项目里"首尾圆角卡片"的视觉对不上：系统
swipeActions 是从屏幕最右滑出整片红底，而项目要求红按钮是固定 72pt、20px 间距、
圆角与首行/末行卡片圆角一致。只能手写。

## 实现要点

```swift
private struct SwipeToDeleteRow<Content: View>: View {
    let content: Content
    let onDelete: () -> Void
    let corners: UIRectCorner

    @State private var offset: CGFloat = 0
    private let deleteWidth: CGFloat = 92
    private let threshold: CGFloat = 50

    private var activeCorners: UIRectCorner {
        var c = corners
        if offset < 0 { c.formUnion([.topRight, .bottomRight]) }
        return c
    }

    var body: some View {
        content
            .background(activeCorners == []
                ? AnyView(Color(hex: "32323A"))
                : AnyView(Color(hex: "32323A").cornerRadius(12, corners: activeCorners)))
            .overlay(alignment: .trailing) {
                Button { triggerDelete() } label: { /* 红色 72pt 按钮 */ }
                    .offset(x: deleteWidth)  // 初始在右边缘外
            }
            .offset(x: offset)
            .clipped()
            .contentShape(Rectangle())
            .simultaneousGesture(
                DragGesture(minimumDistance: 10, coordinateSpace: .local)
                    .onChanged { value in
                        guard value.translation.width < 0 else { ... }
                        // 阻尼：超过 deleteWidth 后只移动 20% 距离
                        if -value.translation.width > deleteWidth {
                            offset = -(deleteWidth + (-value.translation.width - deleteWidth) * 0.2)
                        } else {
                            offset = value.translation.width
                        }
                    }
                    .onEnded { value in
                        let velocity = value.predictedEndTranslation.width - value.translation.width
                        if -offset > threshold || velocity < -200 {
                            // 强滑直接触发删除
                            if -offset > deleteWidth * 1.6 || velocity < -400 {
                                triggerDelete()
                            } else {
                                withAnimation(.spring(response: 0.3, dampingFraction: 0.8)) {
                                    offset = -deleteWidth
                                }
                            }
                        } else {
                            withAnimation(.spring(response: 0.3, dampingFraction: 0.8)) {
                                offset = 0
                            }
                        }
                    }
            )
    }

    private func triggerDelete() {
        withAnimation(.spring(response: 0.25, dampingFraction: 0.85)) {
            offset = -UIScreen.main.bounds.width
        }
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.25) {
            onDelete()  // 实际是 entry.moveToTrash() + context.save()
        }
    }
}
```

## 设计要点

- **初始状态**：`offset = 0`，按钮放在 `content` 右侧 `x: deleteWidth`（完全在屏外）。
- **半开**：`offset = -deleteWidth`（-92pt），按钮露出。
- **强滑**：`offset < -deleteWidth * 1.6` 或 `velocity < -400` 立即触发 `triggerDelete`。
- **删除动画**：把 `offset` 推到 `-UIScreen.main.bounds.width`，250ms 后调用 `onDelete`。
- **圆角合并**：`activeCorners = 首行圆角 ∪ 末行圆角 ∪ (offset<0 ? 右侧两角 : ∅)`，
  保证滑动展开时右侧两角也有圆角，不会露出直角的"卡片裂口"。

## 与 List 自带 .onDelete 的取舍 ^[inferred]

- 自带 `List { ForEach { ... }.onDelete }` 行为类似但视觉控制粒度更粗，且在 iOS 18 上
  swipeActions 触发需要明确的 edge 配置。
- 手写容器**不依赖** `List`，可放在 `LazyVStack` 里——和项目按月分组的滚动布局兼容。

## 已知边界

- 不支持右滑展开（项目用不上）。
- 同一行只支持一个删除动作；项目内 `TrashView` 用系统 `swipeActions` 实现"左滑恢复 +
  右滑删除"两个动作，不复用本容器。

## 相关

- [[concepts/swiftui-framework]] — SwiftUI 声明式 UI 框架核心：View 协议、ViewBuilder tuple 组合、`some View` 不透明类型、布局容器、状态管理、修饰符
