---
title: Trek MCP 服务器 — AI 集成接口
category: concepts
tags:
  - mcp
  - ai-integration
  - oauth
  - api-design
sources:
  - "_raw/trek.txt (Gitingest export, 2026-07-02)"
created: 2026-07-02T00:00:00Z
updated: 2026-08-03T05:47:33Z
summary: Trek 内置 MCP 服务器，通过 OAuth 2.1 为 AI 客户端（Claude Desktop、Cursor 等）提供 150+ 工具和 30 个资源，支持完整行程自动化。
tier: supporting
lifecycle: reviewed
lifecycle_changed: 2026-08-03
lifecycle_reason: "auto-promoted by wiki-lint --consolidate: age>30d, confidence>0.7"
base_confidence: 0.85
provenance:
  extracted: 0.90
  inferred: 0.10
  ambiguous: 0.00
relationships:
  - target: "[[projects/trek/trek]]"
    type: related_to
  - target: "[[projects/trek/concepts/auth-system]]"
    type: uses
  - target: "[[projects/trek/concepts/addon-system]]"
    type: uses
  - target: "[[synthesis/trek-auth-system × trek-mcp-server]]"
    type: related_to
---

# Trek MCP 服务器 — AI 集成接口

Trek 内置了一个 **Model Context Protocol (MCP)** 服务器，让 AI 助手（Claude Desktop、Cursor 或任意 MCP 兼容客户端）通过结构化 API 读取和修改旅行数据。

> **注意：** MCP 是一个插件（addon），需要 Trek 管理员先在管理面板中启用。

## 认证机制

Trek MCP 支持三种认证方式：

| 方式 | Token 前缀 | 访问级别 | TTL | 备注 |
|---|---|---|---|---|
| **OAuth 2.1** | `trekoa_` | 按 scope 限定 | 1 小时 | 推荐。通过 30 天滚动刷新 token（`trekrf_`）自动续期。重放检测：被重放的 token 会级联吊销整个链。 |
| **静态 API Token** | `trek_` | 完全访问 | 无过期 | **已废弃**。会在 AI 客户端触发废弃警告，未来版本将移除。 |
| **Web Session JWT** | — | 完全访问 | 基于会话 | 供 Trek Web UI 内部使用，不面向外部客户端。 |

## OAuth 2.1 自动化流程

```
1. 客户端获取 /.well-known/oauth-protected-resource (RFC 9728)
   → 发现授权服务器，绑定 /mcp 端点
2. 客户端获取 /.well-known/oauth-authorization-server
   → 获取完整 AS 元数据
3. 动态客户端注册 (RFC 7591)
4. 浏览器打开 Trek 授权同意页，用户选择授权哪些 scope
5. 客户端收到短期访问 token（受众绑定到 /mcp，RFC 8707）和滚动刷新 token
```

**前提条件：** 必须设置 `APP_URL` 环境变量，指向 Trek 实例的公网 URL，OAuth 发现才能正常工作。

### 配置示例 (Claude Desktop)

```json
{
  "mcpServers": {
    "trek": {
      "command": "npx",
      "args": ["mcp-remote", "https://your-trek-instance.com/mcp"]
    }
  }
}
```

## OAuth Scope 设计

Trek 定义了 **27 个 OAuth scope**，分为 13 个权限组：

| Scope | 权限 | 组 |
|---|---|---|
| `trips:read/write/delete/share` | 行程访问 | Trips |
| `places:read/write` | 地点/地图数据 | Places |
| `atlas:read/write` | Atlas（已访问国家） | Atlas |
| `packing:read/write` | 行李清单 | Packing |
| `todos:read/write` | 待办事项 | To-dos |
| `budget:read/write` | 预算 | Budget |
| `reservations:read/write` | 预订 | Reservations |
| `collab:read/write` | 协作（聊天/笔记/投票） | Collaboration |
| `notifications:read/write` | 通知 | Notifications |
| `vacay:read/write` | 假期计划 | Vacation |
| `geo:read` | 地图与地理编码 | Geo |
| `weather:read` | 天气预报 | Weather |
| `journey:read/write/share` | 旅行日志 | Journey |

**Scope 规则：**
- `:write` 隐含 `:read`（例如 `budget:write` 自动授予预算读取权限）
- `list_trips` 和 `get_trip_summary` **始终可用**，不受 scope 限制（导航工具）
- 插件门控工具（Atlas、Collab、Vacay、Journey）需要对应 scope **且**插件已启用

## 工具体系

Trek MCP 提供 **150+ 工具**，按功能区分：

### 核心工具
- `get_trip_summary` — 行程完整快照（元数据、成员、每日行程、住宿、预算、行李、预订、协作笔记、待办），用作上下文加载器
- `list_trips`、`create_trip`、`update_trip`、`delete_trip`

### 复合工具（原子事务）

复合工具将常见多步骤操作合并为单次原子调用，若第二步失败则回滚第一步：

| 工具 | 包含操作 | 说明 |
|---|---|---|
| `create_and_assign_place` | `create_place` + `assign_place_to_day` | 创建地点并立即分配到特定日程 |
| `create_place_accommodation` | `create_place` + `create_accommodation` | 创建地点并预订为住宿，同时自动创建酒店预订 |
| `create_budget_item_with_members` | `create_budget_item` + `set_budget_item_members` | 创建预算项并设置分摊成员 |

### 资源（只读）

| 资源 URI | 说明 |
|---|---|
| `trek://trips` | 你拥有或参与的所有行程 |
| `trek://trips/{tripId}` | 单个行程元数据 |
| `trek://trips/{tripId}/days` | 行程的每日安排 |
| `trek://trips/{tripId}/budget` | 预算和费用项 |
| `trek://trips/{tripId}/budget/settlement` | 建议的结算交易（谁欠谁多少） |
| `trek://visited-countries` | Atlas 中已访问的国家 |
| `trek://notifications/in-app` | 最近 50 条应用内通知 |

### 内置提示词

- `trip-summary` — 行程摘要
- `packing-list` — 行李清单建议
- `budget-overview` — 预算概览

## 限制与注意事项

| 限制 | 详情 |
|---|---|
| 管理员需启用 | MCP 插件必须由管理员先启用 |
| 用户级 scope | 每个 MCP 会话限定到已认证用户，只能访问自己的行程 |
| 无图片上传 | 封面图片不能通过 MCP 设置 |
| 预订初始为 pending | AI 创建的预订需手动确认 |
| 速率限制 | 每用户每分钟 300 请求（可配置 `MCP_RATE_LIMIT`） |
| 会话限制 | 每用户最多 20 个并发 MCP 会话（空闲 1 小时后过期） |
| Token 限制 | 每用户最多 10 个静态 token，10 个 OAuth 客户端 |
| 插件切换失效 | 管理员启用/禁用插件后，所有活跃 MCP 会话失效，需重新建立 |
| 实时推送 | MCP 的变更也会通过 WebSocket 广播到所有连接客户端 |
| Demo 模式 | Demo 模式下所有 MCP 写操作被阻止 |

## 相关页面

- [[projects/trek/trek]] — 项目概览
- [[projects/trek/concepts/addon-system]] — 插件系统（MCP 是插件之一）
- [[projects/trek/concepts/auth-system]] — 认证系统详解
