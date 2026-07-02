---
title: >-
  权限管控体系（菜单级 + 按钮级 + 浮窗级）
category: concepts
tags: [chrome-extension, security, zustand, react]
sources: [projects/jrfed-zaxd-mediation-tool]
summary: >-
  登录后从后端获取权限资源树，存入 Zustand Store，通过 usePermission Hook 在组件中控制菜单/按钮/浮窗的显示，无需路由守卫。
provenance:
  extracted: 0.85
  inferred: 0.12
  ambiguous: 0.03
base_confidence: 0.84
lifecycle: active
lifecycle_changed: 2026-07-01
created: 2026-07-01T12:00:00Z
updated: 2026-07-01T12:00:00Z
---

# 权限管控体系

## 设计思路

权限数据在用户登录时从后端 `/complaintAgent/perm/listMyResources` 获取，以扁平字符串数组形式存入 `useMenuStore.permissionResources`，持久化到 Chrome Storage。前端通过 `usePermission` Hook 查询这个数组，决定 UI 的显示与隐藏。

**没有路由守卫**。权限失效只影响 UI 渲染，不跳转路由——因为侧边栏本身没有 URL 变化。

## 权限编码体系

| 前缀 | 类型 | 示例 |
|------|------|------|
| `MENU_` | 菜单显示/隐藏 | `MENU_PREPAY`, `MENU_EQUITY` |
| `BTN_` | 页面按钮控制 | `BTN_PREPAY_QUERY`, `BTN_EQUITY_CANCEL` |
| `FW_` / `FLOAT_` | 划词浮窗控制 | `FW_CUSTOMER_INFO`, `FLOAT_PREPAY` |

## usePermission Hook

```typescript
// src/content/hooks/usePermission.ts
const { hasPermission, hasAnyPermission, hasAllPermissions } = usePermission();
```

- `hasPermission(code)` — 检查单个权限
- `hasAnyPermission(codes[])` — 任意一个匹配即为 true
- `hasAllPermissions(codes[])` — 全部匹配才为 true

组件中直接用条件渲染控制按钮：

```tsx
{hasPermission('BTN_PREPAY_QUERY') && <Button>查询</Button>}
```

## 菜单权限

`menuContent` 组件通过 `useMemo` 过滤 `DEFAULT_ITEMS` 菜单树，只渲染有权限的菜单项。菜单权限变化时（如登出）自动重渲染。

## 权限失效处理

划词浮窗在 `permissionResources` 变化时检查 `hasAnyPermission(['FLOAT_CUSTOMER', 'FLOAT_PREPAY', 'FLOAT_SUPPLIER', 'FW_AGENT_TAG'])`，无权限则立即关闭浮窗并清空用户标签数据。

## 重要踩坑

- `BTN_EQUITY_HIST_QUERY` 缺失会导致历史订单页面空白（查询按钮被隐藏，页面不发请求）
- 接口 URL 末尾空格（`getBenefitsCalculationHistoryRecords%20`）会导致 404——URL 来自常量时注意 trim
- 权限数据通过 Chrome Storage 持久化，切换账号需要调用 `resetMenuPermissions()` 清除旧数据

## 关联页面

- [[projects/jrfed-zaxd-mediation-tool/jrfed-zaxd-mediation-tool]] — 项目总览
- [[projects/jrfed-zaxd-mediation-tool/skills/zustand-chrome-storage]] — 持久化方案
