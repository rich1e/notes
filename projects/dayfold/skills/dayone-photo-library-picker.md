---
title: Day One 风格照片库多选与预热加载
category: project
tags: [mobile, swiftui, photos, phasset, performance, app-architecture]
relationships:
  - target: "[[projects/dayfold/skills/entry-editor-image-dirty-tracking]]"
    type: related_to
  - target: "[[projects/dayfold/concepts/architecture-overview]]"
    type: uses
sources: [projects/dayfold]
summary: >-
  自研 Photos 框架深色多选选择器：PHCachingImageManager 组级视口预热、
  .opportunistic 二次回调、≤2048px 选择器内统一降采样回传，配合照片
  EXIF 时间/坐标锚点采纳与代际校验反向地理编码。
provenance:
  extracted: 0.85
  inferred: 0.13
  ambiguous: 0.02
base_confidence: 0.90
lifecycle: reviewed
lifecycle_changed: 2026-09-02
created: 2026-08-05T10:00:00Z
updated: 2026-08-05T10:00:00Z
---

# Day One 风格照片库多选与预热加载

## Context
系统提供的 `PHPickerViewController` 在需要复杂自定义展示（如深色主题、按日分组带时间区间、序号角标连续多选）时受限于系统 UI 且大图加载响应较慢。使用 `Photos` 框架自建图片库选择器，需要在滚动流畅度、内存占用、异步加载时序以及照片元数据与日记条目时间的联动上做精细控制。

## Architecture & Implementation

### 1. 视口预热与轻量模型解耦
- **轻量模型持有**：UI 层与列表仅持有包含 `PHAsset` 的轻量结构体 `LibraryPhoto`，不直接在模型层常驻位图。
- **分组与区间计算**：按 `Calendar.current.startOfDay(for: creationDate)` 归类为 `PhotoDayGroup`，组内倒序；提取该组最早与最晚拍摄时间拼接为「HH:mm–HH:mm」或单张「HH:mm」。
- **组级视口预热**：在 `LazyVStack` 的 `Section.header` 挂载 `.onAppear` 与 `.onDisappear`，调用 `PHCachingImageManager.startCachingImages` 与 `stopCachingImages`，按当前单元格点阵尺寸（`side × UIScreen.main.scale`）批量预热。

### 2. Opportunistic 缩略图请求与生命周期管理
- **请求策略**：使用 `.opportunistic` 交付模式配合 `isNetworkAccessAllowed = false`。
- **二次回调处理**：同一 `requestID` 会先快速返回本地低清/缓存位图，随后返回高清位图；View 层的 `@State image` 直接接收回调即可实现平滑的从模糊到清晰过渡。
- **滚动取消**：单元格 `.onDisappear` 触发 `cancelImageRequest(requestID)`，快速滑动时及时释放无效渲染算力。

### 3. 选择器内统一解码（降采样 ≤2048px）
- **避免原图内存爆炸**：用户点击「完成」后，在选择器内部异步调用 `requestImage(for:targetSize:contentMode:options:)`，指定长边上限为 2048px（`aspectRatio .fit`，允许 iCloud 下载），转为 `UIImage` 后再通过 `onDone` 回传。
- **单次脏标记更新**：编辑器 ViewModel 收到回调后执行单次 `images.append(contentsOf:)`，仅触发一次 `imagesChanged` 脏标记更新（配合 [[projects/dayfold/skills/entry-editor-image-dirty-tracking]]），避免多次增量触发 Core Data 观察与视图重排。

### 4. 附件拍摄时间与位置采纳
- **Anchor 选择**：多选照片中取带拍摄时间且时间最早的照片作为 `anchor`。
- **合并策略**：连续多批选图时与已有 `pendingMetadata` 比较，仅当新批次包含更早时间时才更新 anchor 时间，旧有已解析或解析中的坐标/地名保留。
- **代际作废机制（Generation Check）**：反向地理编码 `CLGeocoder.reverseGeocodeLocation` 为异步操作，维护 `placeResolveGeneration: Int`。当用户取消选图、重新选图或放弃采纳时递增代际，在途网络回调到达后校验代际，防止失效地名覆盖最新状态。
- **Alert 时序保护**：SwiftUI 中弹窗关闭时会先触发绑定值的 `set(false)` 再执行按钮 action。使用 `metadataConfirmConsumed` 状态标志位，确保点击「是，使用」时不会被关闭流程的默认 `decline` 逻辑覆盖。

### 5. 权限分级与降级兜底
- `.authorized` / `.limited`：展示自定义深色分组网格；`.limited` 状态顶部追加横条引导「选择更多照片」，调用系统 `PHPickerViewController`（可免额外权限访问全部照片）补选。
- `.denied` / `.restricted`：展示深色引导页，提供「前往设置」跳转 URL 与「从系统相册选择」（PHPicker 兜底）双入口。

## Key Code Reference

```swift
// PhotoLibraryService.swift - 预热与缩略图获取
func requestThumbnail(_ photo: LibraryPhoto, cellSize: CGSize, completion: @escaping (UIImage?) -> Void) -> PHImageRequestID {
    let options = PHImageRequestOptions()
    options.deliveryMode = .opportunistic
    options.isNetworkAccessAllowed = false
    options.resizeMode = .fast
    let scale = UIScreen.main.scale
    let targetSize = CGSize(width: cellSize.width * scale, height: cellSize.height * scale)
    return imageManager.requestImage(for: photo.asset, targetSize: targetSize, contentMode: .aspectFill, options: options) { image, _ in
        DispatchQueue.main.async { completion(image) }
    }
}
```

## Related
- [[projects/dayfold/skills/entry-editor-image-dirty-tracking]] — 图片保存脏标记与延迟删除机制
- [[projects/dayfold/concepts/architecture-overview]] — Dayfold 架构概览与状态流转
- [[projects/dayfold/dayfold]] — Dayfold 项目主索引
