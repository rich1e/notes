---

title: >-
  jrfed-zaxd-mediation-tool — 金融客服协谈助手 Chrome 扩展
category: projects
tags:
  - chrome-extension
  - react
  - typescript
  - zustand
  - fintech
sources: [projects/jrfed-zaxd-mediation-tool]
summary: >-
  金融客服协谈助手：基于 Chrome Extension MV3 的侧边栏工具，为金融客服提供提前结清试算、权益计算、安抚金申请、投诉列表等一站式功能，含划词识别填充与完整权限管控。
provenance:
  extracted: 0.9
  inferred: 0.08
  ambiguous: 0.02
base_confidence: 0.88
lifecycle: reviewed
tier: supporting
lifecycle_changed: 2026-08-03
lifecycle_reason: "auto-promoted by wiki-lint --consolidate: age>30d, confidence>0.7"
created: 2026-07-01T12:00:00Z
updated: 2026-08-03T05:47:33Z
relationships:
  - target: "[[projects/xk-ai-talk-desk-ui/concepts/agent-state-machine]]"
    type: related_to
  - target: "[[entities/zustand]]"
    type: uses
---

# jrfed-zaxd-mediation-tool — 金融客服协谈助手

## 项目定位

**客服助手（协谈工具）**是一款基于 Chrome Extension Manifest V3 开发的浏览器扩展，专为金融客服（协谈）团队设计。通过侧边栏集成多个业务功能模块，实现客户信息查询、试算、申请等一站式操作。

- 快捷键 `Cmd+B`（Mac）/ `Ctrl+B`（Windows）唤起侧边栏
- 支持划词浮窗：划选文本后自动识别身份证号、手机号并填充查询表单
- 查询条件和结果通过 [[entities/zustand|Zustand]] + Chrome Storage 持久化，刷新不丢失
- 当前版本：`1.1.5`

## 技术栈

| 层次 | 技术 | 备注 |
|------|------|------|
| 框架 | React 18.3 + TypeScript 5.8 | 全函数组件，strict: false |
| 构建 | Vite 7.0 + CRXJS 2.0 | Chrome 扩展专用构建 |
| UI | Ant Design 5.x + Pro-Components 2.x | prefixCls: zaxd-tool 隔离 |
| 状态 | Zustand 5.0 | 持久化层走 Chrome Storage |
| HTTP | Axios 1.13 封装 | Bearer Token 自动注入 |
| 样式 | SCSS Modules + SCSS Variables | 全局变量通过 additionalData 注入 |
| 埋点 | 神策（Sensors）SDK | 主世界注入脚本方案 |

## 功能模块

| 分组 | 功能 | route key |
|------|------|-----------|
| 试算工具 | 提前结清 | earlyRepayment |
| 试算工具 | 安抚金试算 | soothe |
| 试算工具 | 优惠券 | coupon |
| 试算工具 | 权益计算（现行） | rights |
| 试算工具 | 权益计算（历史订单） | rightsHistory |
| 投诉列表 | 外网投诉列表 | orderList |
| 征信核身 | 征信核身 | identityVerification |
| 供应商工单 | 供应商工单 | supplierTicket |
| 原单退款 | 原单退款 | amcRefund |

## 关键架构决策

### Chrome Storage 替代 localStorage

Content Script 禁止使用 `localStorage` / `sessionStorage`。项目通过 `src/content/utils/storage.ts` 封装 `chrome.storage.local` 的异步操作，并集成为 Zustand 的 `chromeStorage` 适配器。

### 神策埋点的双脚本方案

神策 SDK 需要在页面主世界（MAIN world）中运行，但 React UI 在隔离世界（isolated world）中。解决方案：

- `sa-main-world.ts`：`world: "MAIN"` 注入，在页面 `window` 上初始化神策实例
- `main.tsx`：隔离世界主逻辑，通过 `postMessage` 或 `window.sensorsDataAnalytic201505` 触发埋点

### 权限管控体系

登录后从后端获取权限资源树，写入 `useMenuStore.permissionResources`（字符串数组），通过 [[projects/jrfed-zaxd-mediation-tool/concepts/permission-system]] 控制菜单显示和按钮渲染。

### 划词浮窗的跨 frame 注入

扩展将 content script 注入到所有 frame（`all_frames: true`），但划词浮窗 UI 只在顶层页面渲染。iframe 内的 content script 监听 `mouseup` 事件、识别选中文本并通过 `postMessage` 传给顶层页面处理。

## 项目核心文件

- `manifest.config.ts` — MV3 配置，权限声明
- `src/content/main.tsx` — Content Script 入口
- `src/content/config/routes.ts` — 前端路由配置
- `src/content/hooks/usePermission.ts` — 权限检查 Hook
- `src/content/stores/menuStore.ts` — 菜单状态 + 权限数据
- `src/content/utils/request.ts` — Axios 封装（Token 注入 + 错误处理）
- `src/content/utils/storage.ts` — Chrome Storage 异步封装

## 相关页面

- [[projects/jrfed-zaxd-mediation-tool/concepts/permission-system]] — 权限管控体系
- [[projects/jrfed-zaxd-mediation-tool/concepts/chrome-extension-architecture]] — Chrome 扩展架构
- [[projects/jrfed-zaxd-mediation-tool/skills/zustand-chrome-storage]] — Zustand + Chrome Storage 持久化
- [[projects/jrfed-zaxd-mediation-tool/skills/sensorsdata-dual-world]] — 神策 SDK 双脚本注入方案
- [[projects/jrfed-zaxd-mediation-tool/references/source-tree]] — 源码目录布局

## Related

- [[projects/xk-ai-talk-desk-ui/concepts/agent-state-machine]] — >-
