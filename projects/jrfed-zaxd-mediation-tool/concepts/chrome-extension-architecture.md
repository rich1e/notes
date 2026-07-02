---
title: >-
  Chrome 扩展 MV3 架构：三进程协作与 Content Script 注入策略
category: concepts
tags: [chrome-extension]
sources: [projects/jrfed-zaxd-mediation-tool]
summary: >-
  MV3 三层架构：Background Service Worker + SidePanel + Content Script（注入全部 frame），划词浮窗仅顶层渲染，iframe 内通过 postMessage 上传识别结果。
provenance:
  extracted: 0.88
  inferred: 0.1
  ambiguous: 0.02
base_confidence: 0.87
lifecycle: active
lifecycle_changed: 2026-07-01
created: 2026-07-01T12:00:00Z
updated: 2026-07-01T12:00:00Z
---

# Chrome 扩展 MV3 架构

## 三层架构

```
Background Service Worker
  ↕ chrome.runtime.sendMessage
SidePanel（独立 HTML，React UI）
  ↕ 共享 Chrome Storage
Content Script（注入所有页面，含 iframe）
  └── sa-main-world.ts（MAIN world，神策 SDK）
  └── main.tsx（isolated world，React UI + 划词浮窗）
```

### Background Service Worker

处理扩展生命周期事件、快捷键触发（`Ctrl+B` / `Cmd+B` 打开 SidePanel）。MV3 中 Service Worker 没有持久化生命周期，不能依赖全局变量跨请求存储状态。

### SidePanel

独立的 HTML 页面，通过 `chrome.sidePanel` API 打开。包含完整的 React 应用（登录、菜单、各功能页）。与 Content Script 共享 Chrome Storage 进行数据交换。

### Content Script 双脚本方案

两个脚本注入同一页面：

1. **`sa-main-world.ts`**（`world: "MAIN"`）：运行在页面主世界，可直接访问 `window.sensorsDataAnalytic201505`，负责初始化神策 SDK
2. **`main.tsx`**（隔离世界，默认）：React 应用主逻辑，挂载划词浮窗

两者都设置 `all_frames: true`，确保划词功能在 iframe 内（如合同预览、借款查询 iframe）也能工作。

## 划词浮窗的跨 Frame 策略

- 悬浮球和浮窗 UI **只在顶层页面**渲染（判断 `window === window.top`）
- iframe 内的 Content Script 监听 `mouseup`，识别身份证号/手机号后通过 `window.parent.postMessage` 或 `chrome.runtime.sendMessage` 传给顶层
- 跨域 iframe 无法直接访问 `contentDocument`，需要 try-catch 保护

## 样式隔离

- 所有组件使用 CSS Modules（`*.module.scss`）避免污染宿主页面
- Ant Design 组件设置 `prefixCls: 'zaxd-tool'`，避免与宿主页面的 antd 样式冲突
- Antd 弹窗等 Portal 组件需要指定 `getContainer` 挂载到扩展自己的容器节点

## 关键约束

- 不能使用 `localStorage` / `sessionStorage`（Content Script 共享宿主页面的存储，会造成污染），必须用 `chrome.storage.local` ^[inferred]
- MV3 的 Service Worker 没有 `window` 对象，不能运行 DOM 操作
- 扩展图标点击行为配置为 `_execute_action`，触发 SidePanel 开启

## 关联页面

- [[projects/jrfed-zaxd-mediation-tool/jrfed-zaxd-mediation-tool]] — 项目总览
- [[projects/jrfed-zaxd-mediation-tool/skills/sensorsdata-dual-world]] — 神策双世界注入
- [[projects/jrfed-zaxd-mediation-tool/skills/zustand-chrome-storage]] — 存储方案
