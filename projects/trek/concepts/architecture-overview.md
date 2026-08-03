---

title: Trek 架构概览
category: concepts
tags:
  - system-architecture
  - nestjs
  - monorepo
  - full-stack
sources:
  - "_raw/trek.txt (Gitingest export, 2026-07-02)"
created: 2026-07-02T00:00:00Z
updated: 2026-08-03T05:47:33Z
summary: Trek 采用前后端分离的 monorepo 架构，NestJS 模块化后端 + React SPA 前端，通过构建脚本将 client/dist 复制到 server/public 实现单容器部署。
tier: core
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
  - target: "[[projects/trek/concepts/addon-system]]"
    type: related_to
  - target: "[[projects/trek/concepts/realtime-sync]]"
    type: related_to
  - target: "[[projects/trek/references/database-schema]]"
    type: related_to
  - target: "[[entities/zustand]]"
    type: related_to
---

# Trek 架构概览

## Monorepo 布局

Trek 是一个 **前后端共置的 monorepo**，包含两个独立的 npm 包：

```
trek/
├── client/          # React 19 前端（Vite 构建）
├── server/          # NestJS 11 后端
├── shared/          # 共享类型（@trek/shared）
└── charts/          # Helm 图表
```

构建时，`build-from-sources` 脚本将 `client/dist/` 复制到 `server/public/`，NestJS 通过 SPA fallback filter 提供静态文件，从而实现**单容器部署**。

## 服务端架构：分层 NestJS

### 入口引导

`server/src/index.ts` → `bootstrap.ts` → `buildApp()` 组合整个 NestJS 应用，然后挂载 WebSocket 服务器。

```
http.Server
├── NestJS App (Express adapter)
│   ├── 全局中间件 pipeline
│   ├── /api/* (所有领域路由)
│   ├── /uploads/* (静态文件)
│   ├── /mcp (MCP OAuth 服务器)
│   ├── /.well-known/* (OAuth 发现元数据)
│   └── SPA catch-all (React 前端)
└── WebSocket Server (/ws)
```

### NestJS 模块结构

后端采用标准 **NestJS Controller-Service-Module** 三层模式，每个领域有独立模块：

| 领域 | 模块 | 说明 |
|---|---|---|
| auth | `auth.module` | JWT + OIDC + Passkey + 速率限制 |
| trips | `trips.module` | 行程 CRUD |
| days | `days.module` | 每日行程 + 日记 |
| places | `places.module` | POI 管理 |
| budget | `budget.module` | 费用跟踪 |
| packing | `packing.module` | 行李清单 |
| reservations | `reservations.module` | 预订（航班/住宿/餐厅） |
| collab | `collab.module` | 群聊/笔记/投票 |
| journey | `journey.module` | 旅行日志 |
| atlas | `atlas.module` | 已访问国家地图 |
| vacay | `vacay.module` | 假期规划 |
| mcp | MCP 服务器 | AI 接口（OAuth 2.1） |
| oauth | `oauth.module` | OAuth 2.1 授权服务器 |
| oidc | `oidc.module` | OIDC 提供商集成 |
| files | `files.module` | 文件上传管理 |
| memories | `memories.module` | Immich / Synology 照片集成 |
| maps | `maps.module` | 地图/地理编码代理 |
| weather | `weather.module` | 天气预报 |
| backup | `backup.module` | 数据库备份/恢复 |
| notifications | `notifications.module` | 邮件/Webhook/ntfy/应用内通知 |
| admin | `admin.module` | 管理面板 API |

### 中间件 Pipeline

```
请求
  ↓ globalMiddleware (CORS, CSP, HSTS, 日志)
  ↓ auth.guard (JWT 验证 / Cookie / OIDC)
  ↓ mfaPolicy.guard (MFA 执行)
  ↓ tripAccess.guard (行程权限验证)
  ↓ idempotency.interceptor (幂等性键去重)
  ↓ validate.pipe (Zod schema 验证)
  ↓ Controller
  ↓ Service（业务逻辑）
  ↓ better-sqlite3（同步 SQLite）
```

### 遗留服务层

`server/src/services/` 包含迁移到 NestJS 前的旧版服务，NestJS 模块通过依赖注入调用它们。这是从 Express 向 NestJS 迁移过程中的"绞杀榕"模式残留。^[inferred]

## 客户端架构：React + [[entities/zustand|Zustand]]

### 前端分层

```
pages/          # 路由级页面（每个页面含独立的 useXxx hook）
components/     # 领域功能组件（Admin/Budget/Collab/Journey/...）
store/          # Zustand 状态管理（tripStore / authStore / ...）
repo/           # API 调用层 + 离线降级（withOfflineFallback）
sync/           # 离线同步引擎（mutationQueue/tripSyncManager）
hooks/          # 跨组件共享 hooks
i18n/           # 国际化（20 种语言）
db/             # Dexie IndexedDB（离线存储）
```

### 状态管理模式

每个领域使用**切片（slice）模式**：

```
tripStore
├── daysSlice       (Zustand slice)
├── placesSlice
├── budgetSlice
├── packingSlice
├── reservationsSlice
├── assignmentsSlice
├── filesSlice
├── todoSlice
├── dayNotesSlice
└── remoteEventHandler   # 处理 WebSocket 推送事件，更新本地 store
```

`remoteEventHandler.ts` 是关键的**实时同步桥接层**：监听 WebSocket 事件，将服务端推送的变更反映到本地 Zustand store。

### 页面模式

每个页面遵循固定模式（见 `client/src/pages/PATTERN.md`）：

```
XxxPage.tsx          # 视图层（纯渲染）
useXxx.ts            # 逻辑层（状态、副作用）
xxxModel.ts          # 数据模型（类型定义、计算属性）
```

## 离线支持架构

Trek 的 PWA 离线支持分三层：

1. **Service Worker (Workbox)** — 缓存静态资源、地图瓦片、API 响应
2. **IndexedDB (Dexie)** — 本地数据库，存储离线操作队列
3. **MutationQueue** — 离线时的写操作队列，联网后自动同步

`withOfflineFallback.ts` 包装所有 repo 层调用，在网络不可用时透明地切换到本地数据。

## 构建与部署

```
build-from-sources
├── client: npm ci && npm run build → client/dist/
├── server: npm ci
└── 复制 client/dist/ → server/public/
```

单一 Docker 镜像，NestJS 同时服务 API 和 SPA 静态文件。

## 相关页面

- [[projects/trek/trek]] — 项目概览
- [[projects/trek/concepts/addon-system]] — 插件系统
- [[projects/trek/concepts/realtime-sync]] — WebSocket 实时同步详解
- [[projects/trek/concepts/auth-system]] — 认证系统
- [[projects/trek/references/database-schema]] — SQLite 数据库表结构
