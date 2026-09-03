---
title: UIViewRepresentable 桥接 UITextView 富文本编辑器
category: skills
tags:
  - swiftui
  - uikit
  - uiviewrepresentable
  - uitextview
  - rich-text
  - coordinator
sources:
  - "[[references/apple-developer-nstextattachment-docs]]"
  - "[[projects/dayfold/skills/nstextattachment-bounds-overflow]]"
  - "[[projects/dayfold/skills/uitextview-intrinsic-width-overflow]]"
  - "[[projects/dayfold/skills/auto-expanding-texteditor-scroll]]"
  - "[[projects/dayfold/skills/swiftui-editor-scrollview-vs-attachment]]"
created: 2026-09-03T03:30:00Z
updated: 2026-09-03T03:30:00Z
summary: 2024-2026 仍是 SwiftUI 富文本(尤其 attachment)唯一可行方案:UIViewRepresentable 包装 UITextView,Coordinator 处理 delegate。Apple TextEditor 至今不支持 attachment。
provenance:
  extracted: 0.55
  inferred: 0.40
  ambiguous: 0.05
base_confidence: 0.78
lifecycle: draft
lifecycle_changed: 2026-09-03
tier: supporting
---

# UIViewRepresentable 桥接 UITextView 富文本编辑器

## Context

当 SwiftUI 需要 inline 图片(markdown 渲染、笔记富文本、富文本编辑),Apple 原生 `TextEditor` 和 `Text(AttributedString)` 都**不够**。业界共识是**用 UIViewRepresentable 包装 UITextView** — 这是 dayfold、Notes、Mail 等 app 都遵循的标准方案。

## Architecture

```swift
struct RichTextEditor: UIViewRepresentable {
    @Binding var text: NSAttributedString
    let isScrollEnabled: Bool
    let onHeightChange: (CGFloat) -> Void

    func makeCoordinator() -> Coordinator { Coordinator(self) }

    func makeUIView(context: Context) -> UITextView {
        let tv = UITextView()
        tv.delegate = context.coordinator
        tv.isScrollEnabled = isScrollEnabled
        tv.attributedText = text
        tv.allowsEditingTextAttributes = true
        return tv
    }

    func updateUIView(_ tv: UITextView, context: Context) {
        if tv.attributedText != text {
            tv.attributedText = text
        }
    }

    class Coordinator: NSObject, UITextViewDelegate {
        var parent: RichTextEditor
        init(_ parent: RichTextEditor) { self.parent = parent }

        func textViewDidChange(_ tv: UITextView) {
            parent.text = tv.attributedText
            // 计算实高传给 SwiftUI
            let size = tv.sizeThatFits(CGSize(width: tv.bounds.width,
                                              height: .greatestFiniteMagnitude))
            parent.onHeightChange(size.height)
        }
    }
}
```

## 决策点

### 1. `isScrollEnabled` 控制

- `true` — UITextView 自身滚动,适合长文输入
- `false` — UITextView 报告实高给 SwiftUI,外层 ScrollView 统一滚动

dayfold 选择 `false` + 外层 ScrollView 是因为**图文混排 + 大图**需要统一滚动而非分段滚动。

### 2. Attachment image bounds

参考 [[projects/dayfold/skills/nstextattachment-bounds-overflow]]: 用 `textContainer.size.width - padding*2` 作 attachment.bounds.width(iOS 14-)。

**iOS 15+ 警示**: 直接设 `attachment.bounds` 不可靠 — 必须改用 `containerSize` 或 override `attachmentBounds(for:...)`。

### 4. intrinsicContentSize

参考 [[projects/dayfold/skills/uitextview-intrinsic-width-overflow]]:`isScrollEnabled=false` 的 UITextView 会把被超宽 attachment 撑大的 `contentSize.width` 报成 `intrinsicContentSize.width`,撑爆 SwiftUI 父层。**必须** override `intrinsicContentSize` 横向返回 `noIntrinsicMetric`。

### 5. ScrollViewReader 反行为

参考 [[projects/dayfold/skills/swiftui-editor-scrollview-vs-attachment]]:图文混排下外层 `ScrollViewReader.scrollTo(anchor: .bottom)` 会把所有元素推出屏幕顶部。**改由 UITextView 自管 caret 可见性**即可。

## TextEditor vs UIViewRepresentable 对比

| 特性 | SwiftUI `TextEditor` | `UIViewRepresentable + UITextView` |
|---|---|---|
| Inline 图片 attachment | ❌ 不支持 | ✅ 完整支持 |
| 富文本格式(bold/color/font) | 受限 | ✅ 全控 |
| 图片 copy/paste | ❌ | ✅ |
| 自定义菜单 | ❌ | ✅ |
| 与 SwiftUI 集成 | ✅ 简单 | ⚠️ 需 bridge |
| Dynamic Type | ✅ 自动 | ⚠️ 手动 |

(数据来源:WebSearch 2024 多源共识 — Apple 至今 iOS 18 仍未给 TextEditor 加 attachment)

## Related

- [[projects/dayfold/skills/auto-expanding-texteditor-scroll]]
- [[projects/dayfold/skills/nstextattachment-bounds-overflow]]
- [[projects/dayfold/skills/uitextview-intrinsic-width-overflow]]
- [[projects/dayfold/skills/swiftui-editor-scrollview-vs-attachment]]
- [[references/apple-developer-nstextattachment-docs]]
- [[references/uikit-nstextattachment-vs-appkit]]
- [[synthesis/Research: SwiftUI 图文混排]]