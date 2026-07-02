---
title: 前端存储与缓存
category: concepts
tags:
  - browser
  - performance
  - f2e
summary: 浏览器端存储机制全览：Cookie、LocalStorage、SessionStorage 对比，HTTP 强缓存与协商缓存原理及最佳实践。
sources:
  - https://segmentfault.com/a/1190000021857936
created: 2026-06-29
updated: 2026-06-29
tier: supporting
lifecycle: draft
lifecycle_changed: "2026-06-29"
base_confidence: 0.67
provenance:
  extracted: 0.80
  inferred: 0.15
  ambiguous: 0.05
relationships:
  - target: "[[concepts/browser-process-model]]"
    type: related_to
  - target: "[[concepts/javascript-event-loop]]"
    type: related_to
---

# 前端存储与缓存

## Cookie

### 是什么
HTTP 是无状态协议，Cookie 是服务器在响应中颁发给客户端的一小段键值对文本，用于识别用户身份。浏览器后续请求会自动携带对应 Cookie。

### 主要属性

| 属性 | 说明 | 注意 |
|------|------|------|
| `NAME=VALUE` | 键值对内容 | KEY 不能与其他属性名相同 |
| `Expires` / `Max-Age` | 过期时间 | 负值=临时 Cookie（关闭浏览器即删），0=立即删除 |
| `Domain` | 生效域名 | 该域名下的请求才携带 |
| `Path` | 生效路径 | 默认 `/`（根目录下所有页面） |
| `Secure` | 仅 HTTPS 传输 | SSH 连接才回传 |
| `HttpOnly` | 禁止 JS 访问 | 防止 XSS 盗取 Cookie |
| `SameSite` | 跨站请求控制 | `Strict`/`Lax`/`None`，防止 CSRF |

### Cookie 的限制
- 大小限制约 4KB
- 每个域名 Cookie 数量有限制（通常 20 个）
- 每次 HTTP 请求都会携带（影响性能）

## Web Storage

### LocalStorage vs SessionStorage

| 特性 | LocalStorage | SessionStorage |
|------|-------------|----------------|
| 生命周期 | 永久（除非手动清除） | 标签页关闭即删除 |
| 作用域 | 同源共享 | 仅当前标签页 |
| 大小限制 | ~5MB | ~5MB |
| 随请求发送 | 否 | 否 |

```javascript
// 操作 LocalStorage
localStorage.setItem('key', 'value')
localStorage.getItem('key')
localStorage.removeItem('key')
localStorage.clear()
```

### IndexedDB
- 浏览器端结构化数据库，支持事务
- 存储容量大（通常 50MB+）
- 异步 API，适合大量结构化数据

## HTTP 缓存

### 强缓存（本地缓存）

浏览器直接使用缓存，不发请求到服务器。

**控制字段**：
- `Cache-Control: max-age=3600`（HTTP/1.1，优先）
- `Expires: Wed, 01 Jan 2026 00:00:00 GMT`（HTTP/1.0，精确到秒，受本地时间影响）

### 协商缓存（条件请求）

强缓存过期后，浏览器向服务器验证资源是否更新。

**ETag / If-None-Match**（优先）：
- 服务器返回 `ETag: "abc123"`（资源指纹）
- 浏览器再次请求时发送 `If-None-Match: "abc123"`
- 未变化：服务器返回 `304 Not Modified`

**Last-Modified / If-Modified-Since**：
- 服务器返回 `Last-Modified: ...`（最后修改时间）
- 浏览器发送 `If-Modified-Since: ...`
- 缺点：精度只到秒，且文件修改时间变化不代表内容变化

### 缓存策略最佳实践

| 资源类型 | 推荐策略 |
|---------|---------|
| HTML 入口文件 | `no-cache`（每次协商，确保最新） |
| 带 hash 的 JS/CSS | `max-age=31536000, immutable`（永久强缓存） |
| 图片/字体 | 较长 `max-age` + ETag 兜底 |
| API 响应 | 通常 `no-store` 或短 `max-age` |

## Service Worker 缓存

Service Worker 可以拦截网络请求，实现离线缓存：
- **Cache Storage API**：精细控制缓存策略
- 策略：Cache First、Network First、Stale While Revalidate

## 相关页面

- [[concepts/browser-process-model]] — 浏览器数据存储持久层的架构背景
- [[concepts/javascript-event-loop]] — 异步请求与缓存结合的执行机制
