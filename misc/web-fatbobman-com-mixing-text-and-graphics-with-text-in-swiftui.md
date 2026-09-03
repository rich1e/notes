---
title: SwiftUI 中用 Text 实现图文混排的 4 种方案 — Fatbobman
category: misc
tags:
  - swiftui
  - text
  - inline-graphic
  - dynamic-type
  - textrenderer
  - fatbobman
  - article
  - iOS-18
sources:
  - https://fatbobman.com/zh/posts/mixing_text_and_graphics_with_text_in_swiftui/
source_url: https://fatbobman.com/zh/posts/mixing_text_and_graphics_with_text_in_swiftui/
created: 2026-09-03T03:50:00Z
updated: 2026-09-03T03:50:00Z
summary: Fatbobman 2022 + 2024-06 增补:SwiftUI Text 图文混排 4 种思路(预制图缩放 / overlay占位 / ImageRenderer / TextRenderer 协议),核心目标是"Text 中嵌入带圆角背景的标签"。
provenance:
  extracted: 0.85
  inferred: 0.12
  ambiguous: 0.03
base_confidence: 0.78
lifecycle: draft
lifecycle_changed: 2026-09-03
tier: peripheral
---

# SwiftUI 中用 Text 实现图文混排的 4 种方案 — Fatbobman

## Source

- URL: <https://fatbobman.com/zh/posts/mixing_text_and_graphics_with_text_in_swiftui/>
- Author: Fatbobman (东坡肘子, SwiftUI 核心博主)
- Published: 2022-08,2024-06 增补 TextRenderer 章节

## 问题域

用户问"SwiftUI 能否实现 tag (圆角背景)+ 商品介绍的版式",Fatbobman 答"能但不容易"。

**约束**:
- 标签带圆角背景 — 排除 AttributedString 纯文本方案
- 标签内容动态可变 — 排除 SF Symbols 静态方案
- 必须支持 Dynamic Type(动态类型)— 不能预生成所有尺寸图片
- 需要避免预制位图

## 4 种解决思路

### 方案一:Text 中直接使用图片(预制 + 动态缩放)

**思路**:
- 准备标签 SVG/高分辨率位图
- 当 Dynamic Type 变化时,用 `UIGraphicsImageRenderer` 等比缩放到当前 fontSize 对应的大小
- 通过 `baselineOffset` 调整基线对齐

**关键代码**:
```swift
@Sendable
func resizeImage() async {
    if var image = UIImage(named: tagName) {
        let aspectRatio = image.size.width / image.size.height
        let newSize = CGSize(width: aspectRatio * fontSize, height: fontSize)
        image = image.resized(to: newSize)
        tagImage = Image(uiImage: image)
    }
}

.task(id: fontSize, resizeImage)
```

**优缺点**:
- ✅ 方案简单,实现容易
- ✅ Dynamic Type 友好(`@ScaledMetric` 自动同步)
- ❌ 需要预制图片(标签种类多/常变的场景不适用)
- ❌ 非矢量图需提供高分辨率原图,系统负担大

### 方案二:Text + Overlay 覆盖视图(占位图法)

**思路**:
- 不预制图,用 SwiftUI 视图创建标签
- 根据标签视图尺寸创建空白占位图,插入 Text
- 用 `overlay 将`标签视图定位在占位图上(leadingTop)

**关键代码**:
```swift
extension UIImage {
    @Sendable
    static func solidImageGenerator(_ color: UIColor, size: CGSize) async -> UIImage {
        // 生成纯色占位图
    }
}

@Sendable
func createPlaceHolder() async {
    let size = CGSize(width: tagSize.width, height: 1)
    let uiImage = await UIImage.solidImageGenerator(.clear, size: size)
    let image = Image(uiImage: uiImage)
    placeHolder = Text(image)
}
```

**优缺点**:
- ✅ 无需预制
- ✅ 标签内容/复杂度自由
- ❌ 仅适用标签在左上角的特殊案例
- ❌ 改变位置时对齐困难

### 方案三:SwiftUI ImageRenderer 视图转图(iOS 16+)

**思路**:
- 同样不用预制,SwiftUI 视图创建标签
- 用 `ImageRenderer` 把视图转成 `UIImage`
- 插入 Text 中(不限位置)

**关键代码**:
```swift
@Sendable
func createImage() async {
    let tagView = TagView(tag: tag, textStyle: textStyle, fontSize: fontSize - 6)
    tagView.generateSnapshot(snapshot: $tagImage)
}

func generateSnapshot(snapshot: Binding<Image>) {
    Task {
        let renderer = await ImageRenderer(content: self)
        await MainActor.run {
            renderer.scale = UIScreen.main.scale
        }
        if let image = await renderer.uiImage {
            snapshot.wrappedValue = Image(uiImage: image)
        }
    }
}
```

**优缺点**:
- ✅ 无需预制
- ✅ 标签内容/复杂度/位置都自由
- ❌ 仅支持 iOS 16+(ImageRenderer)
- ⚠️ iOS 16 以下需用 UIHostingController 包裹(主线程压力大)

### 方案四:TextRenderer 协议(WWDC 2024,iOS 18+)

**思路**:
- 实现 `TextRenderer` 协议的 `draw(layout:in:)` 方法
- 找出含 `TagAttribute` 的 run,绘制圆角矩形背景
- 通过 `.customAttribute(TagAttribute())` 给 run 加 attribute

**关键代码**:
```swift
struct TagAttribute: TextAttribute {}

struct TagEffect: TextRenderer {
    let tagBackgroundColor: Color
    func draw(layout: Text.Layout, in context: inout GraphicsContext) {
        for run in layout.flattenedRuns {
            if run[TagAttribute.self] != nil {
                let rect = run.typographicBounds.rect
                let copy = context
                let shape = RoundedRectangle(cornerRadius: 5).path(in: rect)
                copy.fill(shape, with: .color(tagBackgroundColor))
            }
            context.draw(run)
        }
    }
}

// 使用
Text("\(tagPlaceHolderText) \(title)")
    .font(.system(size: fontSize))
    .textRenderer(TagEffect(tagBackgroundColor: tagBackgroundColor))
```

**优缺点**:
- ✅ 最高灵活性 + 优异性能
- ✅ 标签与正文排版一致(文本基线自然)
- ❌ 仅 iOS 18+(作者期待未来兼容 iOS 17)

## Cross-cutting Insight

**这 4 种方案本质上解决的是 3 个不同层次的问题**:

1. **方案一(预制图)**:把"图文混排"当作**位图合成**问题 — 图片就是图片,Text 只是渲染位图
2. **方案二/三(视图合成图)**:把"图文混排"当作**布局工程**问题 — 用 SwiftUI 视图表达标签,把视图渲染为位图塞回 Text
3. **方案四(TextRenderer)**:把"图文混排"当作**渲染协议**问题 — SwiftUI 终于给开发者 hook 进 Text 的 layout/draw pipeline

**演进趋势**:从"黑盒位图" → "白盒视图" → "可控渲染"。每代都把更多控制权交还给开发者,iOS 18 的 TextRenderer 是 Apple 终于承认"图文混排需求真实存在"的"标志。

## 与 dayfold session (2026-09-02) 的对比

dayfold 的"图文混排"问题域不同:
- **fatbobman**:在 Text 内嵌入**带圆角背景的小标签**(装饰元素)
- **dayfold**:在 UITextView 内嵌入**大尺寸照片作为**(实内容)

但**共享技术底座**:UIKit 的 `NSTextAttachment` + `UIViewRepresentable`。Fatbobman 的方案一/二/三本质上是"用 SwiftUI Image 当 attachment",而 dayfold 用 UITextView 的 attachment 处理真实照片。

参考 [[synthesis/Research: SwiftUI 图文混排]] 的对比矩阵,本文的方案一/二/三对应"只读显示"或"弱编辑"场景,方案四(TextRenderer)是未来 iOS 18+ 的方向。

## Author's Conclusion

> "在读完本文后,或许你的第一感受是 SwiftUI 好笨呀,竟然需要如此多的操作才能完成这种简单的需求。但能用现有的方法来解决这类实际问题,何尝又不是一种挑战和乐趣?"

**工程现实主义**:SwiftUI 抽象不完美,真问题经常需要 drop 到 UIKit 或协议层解决。

## Related

- [[synthesis/Research: SwiftUI 图文混排]] — vault 既有研究综述
- [[concepts/swiftui-rich-text-rendering-comparison]] — 全方案矩阵
- [[skills/uiviewrepresentable-uitextview-rich-text]] — 可编辑图文混排方案
- [[references/uikit-nstextattachment-vs-appkit]] — UIKit 与 AppKit 的 imageBounds API 差异
- [[projects/dayfold/skills/nstextattachment-bounds-overflow]] — dayfold 的 photo attachment bounds 修复
- https://fatbobman.com/zh/posts/creating-stunning-dynamic-text-effects-with-textrender/ — 作者 TextRenderer 详解

## Verification

- Defuddle 提取 26 KB markdown,核心 4 个方案 + 2024-06 增补完整
- 与 vault 既有 dayfold session 主题不同(装饰元素 vs 实内容)
- 4 个方案 trade-off 描述清晰,各有 pros/cons
- TextRenderer (方案四) 给出 iOS 18 适配预期