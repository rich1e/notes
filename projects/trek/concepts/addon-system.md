---
title: Trek 插件系统（Addon System）
category: concepts
tags:
  - addon
  - extensibility
  - feature-flags
  - system-architecture
sources:
  - "_raw/trek.txt (Gitingest export, 2026-07-02)"
created: 2026-07-02T00:00:00Z
updated: 2026-08-03T05:47:33Z
summary: Trek 的插件系统允许管理员按需启用/禁用功能模块，每个插件有独立的数据库表、API 路由和前端组件，通过 addons 表中的 enabled 标志控制。
tier: supporting
lifecycle: reviewed
lifecycle_changed: 2026-08-03
lifecycle_reason: "auto-promoted by wiki-lint --consolidate: age>30d, confidence>0.7"
base_confidence: 0.80
provenance:
  extracted: 0.80
  inferred: 0.20
  ambiguous: 0.00
relationships:
  - target: "[[projects/trek/trek]]"
    type: related_to
  - target: "[[projects/trek/concepts/architecture-overview]]"
    type: related_to
  - target: "[[projects/trek/concepts/mcp-server]]"
    type: related_to
---

# Trek 插件系统（Addon System）

Trek 采用**插件（Addon）架构**将可选功能模块化。管理员可在管理面板的 **Admin > Addons** 页面按需启用或禁用插件。

## 内置插件列表

| 插件 | 功能 | 类型 |
|---|---|---|
| **Lists** | 行李清单 + 待办事项（含模板、成员分配、可选行李追踪） | global |
| **Costs** | 费用追踪，含分摊和结算（谁欠谁）、多货币 | global |
| **Documents** | 行程/地点/预订的文件附件 | global |
| **Collab** | 群聊、笔记、投票、每日出行确认 | global |
| **Vacay** | 个人假期规划，含日历、100+ 国家假日、结转追踪 | global |
| **Atlas** | 已访问国家世界地图、愿望清单、旅行统计、连续追踪、液态玻璃 UI | global |
| **Journey** | 杂志风格旅行日志，含条目、照片（Immich/Synology）、地图、心情 | global |
| **AirTrail** | 连接自托管 AirTrail 实例，将航班导入并同步到预订 | global |
| **MCP** | 通过 OAuth 2.1 将 Trek 暴露给 AI 助手（150+ 工具，30 个资源） | global |

## 数据库实现

插件配置存储在 `addons` 表：

```sql
CREATE TABLE addons (
  id TEXT PRIMARY KEY,          -- 如 'mcp', 'atlas', 'collab'
  name TEXT NOT NULL,
  description TEXT,
  type TEXT NOT NULL DEFAULT 'global',
  icon TEXT DEFAULT 'Puzzle',
  enabled INTEGER DEFAULT 0,    -- 0=禁用, 1=启用
  config TEXT DEFAULT '{}',     -- JSON 配置
  sort_order INTEGER DEFAULT 0
);
```

插件的数据库表（如 `vacay_plans`、`collab_notes`、`collab_polls` 等）在 schema 初始化时始终创建，但只有插件启用后才能通过 API 访问。^[inferred]

## Guard 模式

后端通过专用 Guard 实施插件门控：

- `journey-addon.guard.ts` — Journey 插件门控
- `airtrail-addon.guard.ts` — AirTrail 插件门控

Guard 在请求到达 Controller 之前检查 `addons` 表的 `enabled` 状态，插件未启用时返回 `404` 或 `403`。

## MCP 插件感知

MCP 服务器是插件感知的：当插件被启用/禁用时：
1. 所有活跃 MCP 会话失效
2. 用户需重新建立 MCP 连接
3. 新会话只注册当前已启用插件对应的工具

## 前端插件感知

前端通过 `addonStore.ts` 管理插件状态，组件在渲染前检查插件是否启用。Navbar、设置页等 UI 元素会根据插件状态动态显示/隐藏相应入口。

## 相关页面

- [[projects/trek/trek]] — 项目概览（功能列表）
- [[projects/trek/concepts/architecture-overview]] — 整体架构
- [[projects/trek/concepts/mcp-server]] — MCP 插件详解
