---
title: EntryEditor 图片脏标记
category: project
tags: [ios, swiftui, core-data, media, app-architecture]
relationships:
  - target: "[[concepts/swiftui-framework]]"
    type: uses
sources: [projects/dayfold]
summary: >-
  用 @Published var images 的 didSet 维护 imagesChanged 布尔，保存时仅在
  true 时全量重建 MediaAsset 并删旧文件；编辑但未动图片时跳过，避免破坏
  loadExistingImages 的并发覆盖逻辑。
provenance:
  extracted: 0.80
  inferred: 0.18
  ambiguous: 0.02
base_confidence: 0.85
lifecycle: draft
lifecycle_changed: 2026-06-29
tier: supporting
created: 2026-06-29T00:00:00Z
updated: 2026-06-29T00:00:00Z
---

# EntryEditor 图片脏标记

文件：`dayfold/dayfold/ViewModels/EntryEditorViewModel.swift`

## 问题

`EntryEditorView` 编辑已有日记时：

1. `loadExistingImages` 异步读盘 → 拿到后写回 `self.images`。
2. 2 秒 auto-save 触发 `save()` → 若直接用当前 `images` 全量重建 `MediaAsset`，
   会把"刚加载还没编辑"的旧图全删了重建一遍（每次 auto-save 一次，磁盘抖动）。

## 解法：脏标记

```swift
@Published var images: [UIImage] = [] {
    didSet {
        if !isLoadingImages { imagesChanged = true }
    }
}
private var isLoadingImages = false
private var imagesChanged = false
```

- `loadExistingImages` 把 `isLoadingImages` 置 true 期间，`didSet` 不会把
  `imagesChanged` 置 true；赋值完后再置 false。
- 用户**手动**增删图片时 `didSet` 触发，`imagesChanged = true`。
- `save()` 中：

  ```swift
  if imagesChanged {
      // 1. 删旧 MediaAsset 与磁盘文件
      for asset in entryToSave.mediaAssetsArray {
          let filename = asset.wrappedFilename
          viewContext.delete(asset)
          Task { await MediaService.shared.deleteImage(filename: filename) }
      }
      // 2. 按当前 images 顺序重建
      for (index, image) in images.enumerated() {
          if let result = await MediaService.shared.saveImage(image) {
              let asset = MediaAsset.create(type: .photo,
                  filename: result.filename, in: viewContext)
              asset.thumbnailData = result.thumbnail
              asset.order = Int32(index)
              asset.entry = entryToSave
          }
      }
      imagesChanged = false
  }
  ```

- 跳过 `imagesChanged == false` 分支，**整段 IO 与重建都不执行**，仅写其他字段。
- 加载竞态保护：`loadExistingImages` 完成时若 `imagesChanged` 已被用户操作置 true，
  不覆盖用户操作结果（`guard !self.imagesChanged else { return }`）。

## 为什么不用更"现代"的方案 ^[inferred]

- 增量 diff（`[MediaAsset.filename]` 对比 `images`）也能做，但 `UIImage` 不可哈希，
  难以直接比对"内容是否变化"，且图片重编码不可逆（jpeg 0.8 → 解码 → 编码 → 0.8），
  即使是同一张图字节也不同。
- 现状："用户没动图片 → 跳过；动了图片 → 全量重建"在 UX 上完全够用，且逻辑直白可读。

## 关键细节

- `MediaService.saveImage` 返回 `(filename, thumbnail)`，文件名用 `UUID().uuidString` 避免
  冲突；写入后立刻生成 100pt 缩略图存到 `MediaAsset.thumbnailData`（避免列表回显时
  再读盘解码）。
- 旧文件删除是 fire-and-forget `Task { await MediaService.shared.deleteImage(...) }`，
  不阻塞保存主流程；极端情况下面板会留下孤儿 jpg，由后续清理任务回收（目前未实现）。
- `imagesChanged = false` **在 await 之后**才清，保证 await 期间用户改图也会被下一次
  save 感知。

## 相关

- [[concepts/swiftui-framework]] — SwiftUI 声明式 UI 框架核心：View 协议、ViewBuilder tuple 组合、`some View` 不透明类型、布局容器、状态管理、修饰符
