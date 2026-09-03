---
title: SwiftUI 富文本 layout 深度解析 — MarkdownView / MarkdownText / RichText 演进史
category: references
tags:
  - swiftui
  - text-rendering
  - layout-protocol
  - text-selection
  - inline-attachment
  - richtext
  - markdownview
  - fatbobman
  - liyanan
  - iOS-26
sources:
  - https://fatbobman.com/zh/posts/a-deep-dive-into-swiftui-rich-text-layout/
  - https://github.com/LiYanan2004/MarkdownView
  - https://github.com/LiYanan2004/RichText
source_url: https://fatbobman.com/zh/posts/a-deep-dive-into-swiftui-rich-text-layout/
created: 2026-09-03T04:10:00Z
updated: 2026-09-03T04:10:00Z
summary: LiYanan (X/Grok + Hugging Face Chat 的 MarkdownView / RichText 作者) 撰文:SwiftUI 富文本混排 3 代方案演进史 — Layout 协议 + FlowLayout → MarkdownText 失败(TextRenderer vs textSelection 互斥) → 最终用 NSTextView + View overlay + Mirror View.id 状态保留。
provenance:
  extracted: 0.85
  inferred: 0.10
  ambiguous: 0.05
base_confidence: 0.82
lifecycle: draft
lifecycle_changed: 2026-09-03
tier: supporting
---

# SwiftUI 富文本 layout 深度解析 — MarkdownView / MarkdownText / RichText 演进史

## Source

- URL: <https://fatbobman.com/zh/posts/a-deep-dive-into-swiftui-rich-text-layout/>
- 作者邀请嘉宾:LiYanan ([GitHub](https://github.com/LiYanan2004))
- Published: 2025(原文未明示具体日期, 但视频 demo 为 2025-11-29)
- 作者:MarkdownView 与 RichText 作者(被 X/Grok + Hugging Face Chat 采用)

## 3 代方案演进

### 第 1 代:MarkdownView (2022-07 起)

**问题**: markdown 需要**实时预览 + 完整支持**(图、表、引用、代码块),且需要**文本可选择/可复制**。

**方案**:
- 用 [swift-markdown](https://github.com/swiftlang/swift-markdown) 解析 markdown 节点树
- 每个节点递归生成对应小 View
- 用 Layout 协议自定义 `FlowLayout` 把 views 一行行排列

**关键洞察**:**相邻的 Text 拼接 = 文本连续显示**:
- 给每个 view 打 tag
- 如果相邻 view 都是 Text → 合并显示
- 如果不是 → 用 FlowLayout 排列

**失败尝试**:
- 按字符拆:西文场景失败
- 用 Natural Language Framework 拆成词:能解决但性能差

**SVG + 数学公式**:
- SVG: WebKit 内嵌成网页(js 查询 svg 大小)
- LaTeX: 集成 [colinc86/LaTeXSwiftUI](https://github.com/colinc86/LaTeXSwiftUI)

**文本选择的妥协**:
- 多个连续 Text 支持连续选中 ✅
- 跨段落用 `\n` 分隔,可跨段落选中 ✅
- 图片异步加载 → 不参与文本选中 ❌
- 块内容(引用/代码块)不参与跨元素选中 ❌

### 第 2 代:MarkdownText 失败案例

**思路**:用 `TextRenderer` + `.textSelection(.enabled)` 看起来完美。
- TextRenderer: 自定义 Text 渲染方式 + 自由组合 Text
- `.textSelection(.enabled)`:iOS 18+ 的文本选择

**踩坑**:**一旦开启 `.textSelection(.enabled)`,所有 TextRenderer 都失效**(回看 Apple 文档只字未提)。

→ **TextRenderer 和 textSelection 相互排斥**,Apple 文档没说明。这是 iOS 18 的已知 trade-off。

### 第 3 代:RichText (2025)

**思路**:彻底放弃 SwiftUI Text,使用 `NSTextView` / `UITextView` + View overlay:

```swift
// Platform Text View: 整体布局 + 显示文本
// View overlay: 拿到 Text Layout 后位置信息后显示
// → overlay 坐标系与 Platform Text View 保持一致,完美贴合
```

**关键能力**:
- ✅ 嵌入任意 SwiftUI.View(支持交互)
- ✅ 跨元素文本选择(iOS 上 SwiftUI `.textSelection` 只支持全选, macOS 支持区域)
- ✅ 等价文本替换(嵌入 View 在复制时被替换为对应文本)

## 4 个关键技术挑战

### 1. Font 转换:SwiftUI.Font → PlatformFont

底层是 `NSTextView` / `UITextView`,**不能识别 SwiftUI.Font**。

**新 API (OS 26+)**:
```swift
@Environment(\.fontResolutionContext) var fontResolutionContext
@Environment(\.font) var font
let platformFont = (font ?? .body).resolve(in: fontResolutionContext).ctFont as PlatformFont
```

**旧版本 fallback**:`RichText` 提供 `.font(_ font: PlatformFont?)` modifier,直接传 UIFont/NSFont。

⚠️ `Font.Resolved` 仅 OS 26+,`Font.Context` iOS 15+ / macOS 12+ — Apple 自己的可用性差异。

### 2. View ID 提取(状态保留)

**问题**: 每次内容变化都重建视图 → 状态丢失(滚动位置、TextField 输入)。

**方案**:通过 Mirror 反射找到 `SwiftUI.IDView.id`:

```swift
private static func descend(mirror: Mirror) -> AnyHashable? {
    let typeName = String(reflecting: mirror.subjectType)
    if typeName.starts(with: "SwiftUI.TupleView") {
        return nil  // VStack wraps a TupleView — id 不可访问
    }
    if typeName.starts(with: "SwiftUI.IDView"),
       let id = mirror.descendant("id") as? AnyHashable {
        return id
    }
    for child in mirror.children {
        guard let view = child.value as? (any SwiftUI.View) else { continue }
        if let found = explicit(view) { return found }
    }
    return nil
}
```

**限制**:`VStack { Text("a").id("a"); Text("b").id("b") }` — VStack wraps TupleView,**id 不可访问**(返回 nil)。只有顶层 View 的 id 才能提取。

参考 [OpenSwiftUI](https://github.com/OpenSwiftUIProject/OpenSwiftUI) 的 `SwiftUI.View.id(_:)` 实现。

### 3. InlineTextAttachment 存储 View

每个传入的 View 最终被转换为 `InlineTextAttachment`,里面存:
- 对应的 SwiftUI View
- 通过 id 与前一个 attachment 匹配,继承状态

### 4. 等价文本替换(复制行为)

View 嵌入后在复制时**会消失**。通过 `InlineView` 关联一个文本别名,拷贝时替换为该文本。

## 与 vault 既有研究的关系

| 维度 | vault 研究 [[synthesis/Research: SwiftUI 图文混排]] | LiYanan 的 RichText |
|---|---|---|
| **目标场景** | 图文混排(general) | Markdown 渲染 + 选中文本选择 |
| **底层** | UIViewRepresentable + UITextView (推荐) | NSTextView / UITextView + View overlay |
| **iOS 版本** | iOS 13+ | iOS 13+ (Font 转换需要 iOS 26+) |
| **Image 渲染** | NSTextAttachment | InlineTextAttachment + SwiftUI.View |
| **文本选择** | UIKit 默认 | 支持跨元素 + 区域选择 |
| **作者** | 业界共识 | LiYanan (X/Grok + Hugging Face Chat) |

**互相补充**:vault 既有研究提供"业界共识 + 多种方案",本文提供"实战落地 + 4 个具体技术坑 + iOS 18 TextRenderer 失败案例"。

## Key Takeaways

- **Layout 协议 + 相邻 Text 合并** 是 SwiftUI 富文本可行的第一代方案
- **TextRenderer 在 iOS 18 与 textSelection 互斥** — Apple 文档未提及
- **Platform Text View + SwiftUI overlay** 是真正能任意 View 混排的方案,需 Mirror 提取 View.id
- **Font 转换 API 是 OS 26 才完善**(`Font.Resolved`),旧版本需自定义 modifier
- 业界 consensus + LiYanan 实战 = 两层互补的 SwiftUI 富文本知识

## Related

- [[entities/markdownview]] — LiYanan 自己的 SwiftUI markdown 渲染(本仓库的 description 是 1.0 早期,现在 production 验证)
- [[entities/swift-markdown]] — 解析后端 (LiYanan 的 MarkdownView 1.0 核心依赖)
- [[synthesis/Research: SwiftUI 图文混排]] — vault 既有研究综述
- [[concepts/swiftui-rich-text-rendering-comparison]] — 全方案矩阵
- [[skills/uiviewrepresentable-uitextview-rich-text]] — UIViewRepresentable 模板
- [[references/uikit-nstextattachment-vs-appkit]] — UIKit vs AppKit API 差异
- [[misc/web-fatbobman-com-mixing-text-and-graphics-with-text-in-swiftui]] — Fatbobman 早期文章 (4 种方案)

## Verification

- Defuddle 提取 453 行 markdown,核心 3 代方案 + 4 个技术坑完整
- 与 vault 既有 fatbobman URL 互相补充(早期文章 vs 演进深度)
- 代码示例可执行(`InlineTextAttachment` + `Mirror.descend` + `Font.resolve`)
- iOS 18 TextRenderer vs textSelection 矛盾 — 文档级验证的 Apple Bug
- LiYanan 库 MarkdownView + RichText 在 X/Grok + Hugging Face Chat 实战验证