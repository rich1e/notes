---

title: Trek 实时同步机制
category: concepts
tags:
  - websocket
  - realtime
  - offline-first
  - pwa
sources:
  - "_raw/trek.txt (Gitingest export, 2026-07-02)"
created: 2026-07-02T00:00:00Z
updated: 2026-07-02T00:00:00Z
summary: Trek 通过 WebSocket 实现实时协同，采用 Room 模型（per-trip）广播变更；离线时用 MutationQueue + IndexedDB 缓存写操作，联网后自动回放。
tier: supporting
lifecycle: draft
lifecycle_changed: "2026-07-02"
base_confidence: 0.82
provenance:
  extracted: 0.82
  inferred: 0.18
  ambiguous: 0.00
relationships:
  - target: "[[projects/trek/concepts/architecture-overview]]"
    type: related_to
  - target: "[[projects/trek/trek]]"
    type: related_to
  - target: "[[entities/zustand]]"
    type: related_to
---

# Trek 实时同步机制

## WebSocket 服务端设计

Trek 使用原生 `ws` 库实现 WebSocket 服务器，挂载在 `/ws` 路径。核心数据结构：

```typescript
// Room 管理：tripId → Set<WebSocket>
const rooms = new Map<number, Set<NomadWebSocket>>();
// 反向索引：socket → Set<tripId>
const socketRooms = new WeakMap<NomadWebSocket, Set<number>>();
// 用户信息：socket → User
const socketUser = new WeakMap<NomadWebSocket, User>();
// socket ID：socket → number
const socketId = new WeakMap<NomadWebSocket, number>();
```

### 连接认证流程

WebSocket 不使用 HTTP cookie 或 Authorization header，而是通过 **一次性临时 token（Ephemeral Token）** 认证：

```
1. 客户端向 REST API 请求临时 token（类型: 'ws'）
2. 使用 token 建立 WebSocket 连接: ws://host/ws?token=<ephemeral_token>
3. 服务端消费 token（单次使用，消费后失效）
4. 验证 password_version 防止密码变更后的旧 token 重用
5. 检查 MFA 策略
6. 发送 welcome 消息：{ type: 'welcome', socketId: <id> }
```

### Room 模型

每个行程是一个独立的"Room"。客户端通过消息加入/离开：

```json
// 加入 Room
{ "type": "join", "tripId": 123 }
// 服务端验证权限后响应
{ "type": "joined", "tripId": 123 }

// 离开 Room
{ "type": "leave", "tripId": 123 }
```

### 广播机制

服务端的所有写操作（CRUD）完成后调用 `broadcast()`：

```typescript
// 广播到 Room 内所有用户，可排除触发者
broadcast(tripId, 'places:updated', { place: {...} }, excludeSid)

// 广播到特定用户（如行程邀请通知）
broadcastToUser(userId, { type: 'trip:invited', ... })
```

### 心跳机制

每 30 秒 ping 一次所有客户端，未响应的连接被终止（`terminate()`）。

### 速率限制

每连接 10 秒窗口内最多 30 条消息，超出返回错误并丢弃消息。

## 客户端实时同步

### 连接管理 (`useTripWebSocket.ts`)

```
组件挂载
  → 获取临时 token
  → 建立 WebSocket 连接
  → 发送 join: tripId
  → 监听服务端推送事件
  → 路由到 remoteEventHandler
```

### remoteEventHandler — 事件派发器

`client/src/store/slices/remoteEventHandler.ts` 是客户端实时同步的核心。它监听所有 WebSocket 事件类型，并将变更分派到对应的 [[entities/zustand|Zustand]] slice：

```
WebSocket 事件
  ├── 'places:updated'   → placesSlice.updatePlace()
  ├── 'places:created'   → placesSlice.addPlace()
  ├── 'days:updated'     → daysSlice.updateDay()
  ├── 'budget:updated'   → budgetSlice.updateItem()
  ├── 'assignments:...'  → assignmentsSlice
  └── ...（每个领域有对应的 handler）
```

## 离线支持架构

Trek 实现了**完整的离线优先（Offline-First）**策略：

### Layer 1：Service Worker (Workbox)
- 缓存静态资源、应用 shell
- 缓存地图瓦片（`tilePrefetcher.ts` 预取当前行程区域）
- 缓存 API 响应（只读路由）

### Layer 2：IndexedDB (Dexie)
`client/src/db/offlineDb.ts` 定义离线数据库结构，存储：
- 本地缓存的行程数据
- 待同步的变更队列（MutationQueue）

### Layer 3：MutationQueue
`client/src/sync/mutationQueue.ts` 管理离线写操作：

```
用户操作
  ↓ 检查网络状态 (connectivity.ts)
  ↓ 在线：直接 API 调用
  ↓ 离线：写入 MutationQueue（IndexedDB）
         联网后：依序回放队列 → API 调用
```

### withOfflineFallback
`client/src/repo/withOfflineFallback.ts` 透明地包装所有 repo 层调用，在网络不可用时返回本地缓存数据，提供无缝降级体验。

### syncTriggers
`client/src/sync/syncTriggers.ts` 监听网络状态变化（online/offline 事件），在恢复连接时触发 MutationQueue 回放和全量数据同步。

## 数据一致性策略

Trek 采用**服务端权威**模式：

- 客户端本地操作立即更新 UI（乐观更新）
- 服务端响应确认后，广播给其他用户
- 冲突时以服务端响应为准，客户端回滚^[inferred]

## 相关页面

- [[projects/trek/concepts/architecture-overview]] — 整体架构
- [[projects/trek/concepts/auth-system]] — 临时 token 认证
- [[projects/trek/trek]] — 项目概览
