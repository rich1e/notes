---
title: >-
  神策 SDK 双世界注入方案：MAIN world + isolated world 分离
category: skills
tags: [chrome-extension, analytics]
sources: [projects/jrfed-zaxd-mediation-tool]
summary: >-
  神策 SDK 需要访问 window 对象，但 Content Script 默认运行在隔离世界。解决方案：用 world: MAIN 注入主世界脚本初始化 SDK，隔离世界通过 tracker.ts 工具函数触发上报。
provenance:
  extracted: 0.8
  inferred: 0.18
  ambiguous: 0.02
base_confidence: 0.79
lifecycle: active
lifecycle_changed: 2026-07-01
created: 2026-07-01T12:00:00Z
updated: 2026-07-01T12:00:00Z
relationships:
  - target: "[[projects/jrfed-zaxd-mediation-tool/concepts/permission-system]]"
    type: related_to

---

# 神策 SDK 双世界注入方案

## 问题背景

Chrome Extension Content Script 默认运行在隔离世界（isolated world），与页面 JavaScript 共享 DOM 但不共享 `window` 上的变量。神策（Sensors Data）分析 SDK 需要挂载在 `window.sensorsDataAnalytic201505` 上，在隔离世界中直接调用会找不到这个对象。

## 解决方案

在 `manifest.config.ts` 中声明两个 content script：

```typescript
content_scripts: [
  {
    // 主世界：SDK 初始化
    js: ['src/content/sa-main-world.ts'],
    matches: ['https://*/*', 'http://*/*', 'file://*/*'],
    run_at: "document_start",
    world: "MAIN",           // 关键：运行在页面主世界
    all_frames: true
  },
  {
    // 隔离世界：React UI 主逻辑
    js: ['src/content/main.tsx'],
    matches: ['https://*/*', 'http://*/*', 'file://*/*'],
    run_at: "document_end",
    all_frames: true         // world 默认 ISOLATED
  }
],
```

- `sa-main-world.ts`（MAIN world）：加载神策 SDK、调用 `init()` 初始化、监听埋点事件
- `main.tsx`（isolated world）：React UI，通过 `window.sensorsDataAnalytic201505` 调用 SDK，或通过 `saTrackInMainWorld` 工具函数封装

## tracker.ts 埋点工具

`src/content/utils/tracker.ts` 封装了两种上报接口：

- `trackFloatExposure(params)` — 浮窗曝光（使用 `$pageview` 事件）
- `trackButtonClick(params)` — 功能按钮点击（使用 `$WebClick` 事件）

页面来源通过 URL 关键词识别（ARK 通话页 / 工单详情页 / 其他）。

## 公共参数

```typescript
interface BaseTrackParams {
  user_id: string;          // 坐席 ID
  operators_type: string;   // 坐席角色
  $element_content: string; // 划词内容
  thirdUserNo: string;      // 三方用户 ID
  timestamp: number;
  page_source: string;      // 页面来源
}
```

## 关联页面

- [[projects/jrfed-zaxd-mediation-tool/concepts/chrome-extension-architecture]] — 架构概述
- [[projects/jrfed-zaxd-mediation-tool/jrfed-zaxd-mediation-tool]] — 项目总览

## Related

- [[projects/jrfed-zaxd-mediation-tool/concepts/permission-system]] — >-
