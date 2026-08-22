---
title: loopback 安全与 Host/Origin 头
category: concept
tags: [security, dns-rebinding, cors, host-header, origin-header, mcp, figwright]
sources:
  - https://github.com/awdr74100/figwright
created: 2026-08-14T08:00:00Z
updated: 2026-08-14T08:00:00Z
summary: 本地 MCP relay 的安全边界:loopback 不够,需 Host 头(防 DNS rebinding)+ Origin 头(CORS)+ CORS preflight-only 媒体类型三层组合
base_confidence: 0.55
lifecycle: draft
lifecycle_changed: 2026-08-14
tier: supporting
provenance:
  extracted: 0.80
  inferred: 0.15
  ambiguous: 0.05
---

# loopback 安全与 Host/Origin 头

Figwright 解决"loopback ≠ 安全边界"问题的三层防御方案。

## 核心论点(README 原话)

> Loopback is not on its own a boundary — a web page you visit can still reach a local port — so the relay gates every request on two headers a page cannot forge

**背景**:本地 127.0.0.1:3055 端口,浏览器访问的恶意网页仍可通过 `fetch('http://127.0.0.1:3055/...')` 触达。loopback 不是访问控制。

## 三层防御

### 第 1 层:`Host` 头校验(防 DNS rebinding)

- 攻击向量:恶意 DNS `evil.com` → DNS rebinding 指向 `127.0.0.1`
- 防护:HTTP/WebSocket 升级请求的 `Host` 头必须解析为 loopback
- 这是 **DNS rebinding 的标准解**:浏览器强制 `Host` 头不能被 JS 控制

### 第 2 层:`Origin` 头校验(CORS)

- 攻击向量:浏览器中已加载的恶意 JS 直接发请求
- 防护:`Origin` 头必须为插件的 sandboxed 来源;**拒绝一切浏览器来源**
- 这等同于把 plugin 作为唯一受信源(白名单)

### 第 3 层:CORS preflight-only 媒体类型

- leader 的 HTTP 端点(`/rpc)要求一种 **无法不经过 CORS preflight 就发送** 的媒体类型
- 简单请求(`text/plain`/`application/x-www-form-urlencoded`/`multipart/form-data`)绕过 preflight → 不可用
- 非简单请求(`application/json` 等)强制浏览器发 OPTIONS preflight → CORS 策略生效 → 即便被攻击者控制也走不到真实请求

## 拓扑回顾

```
浏览器恶意页面 ──HTTP──→ @figwright/mcp :3055
                          │
                          ├─ Host 头 ≠ loopback → 拒
                          ├─ Origin ≠ plugin sandbox → 拒
                          └─ Content-Type 是 simple CORS → 拒(preflight 才能过)
                          
Figma plugin (iframe) ───WebSocket──→ @figwright/mcp :3055/ws
                          ✓ Host=loopback ✓ Origin=plugin ✓ binary ws upgrade
```

## 为什么图 W3C 标准攻击面

| 攻击 | 攻击向量 | Figwright 防护 |
|---|---|---|
| DNS rebinding | `evil.com → 127.0.0.1` | `Host` 头必须 = `127.0.0.1` 或 `localhost` |
| CSRF from 浏览器 | 恶意页面 fetch | `Origin` 头必须 ∈ plugin 白名单 |
| 简单 CORS 绕过 | `text/plain` POST | `/rpc` 强制 application/json(需 preflight) |
| WebSocket 跨源 | 恶意 JS new WebSocket | WebSocket 升级也走 HTTP `Host`/`Origin` 校验 |

## 与 vault 已有安全知识对应

| vault 已有 | 本方案对应 |
|---|---|
| [[skills/ssh-server-hardening]] SSH 服务端硬化 | 同样思想:每个边界都要独立验证 |
| [[concepts/cdp-cookie-extraction]] Chrome DevTools Protocol 本地桥 | 同样的"本地端口暴露"问题——CDP 用独立 profile + 远调试封锁 |
| [[skills/fail2ban-setup]] 应用层 IDS | 攻击面不同但都在"如何处理边界外的请求"层 |
| [[concepts/auth-status-semantics]] 5-state auth 健康词典 | `unverified` 类似——某些本地连接无法 100% 验证身份 |

## 与官方 MCP 安全最佳实践的关系

README 引用 [MCP Security Best Practices](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices)——这是 Anthropic 官方文档对本地 MCP server 的推荐做法。Figwright 是该推荐的实际实现样本。

## Open Questions

- `Host` 头允许的具体值集:`127.0.0.1` / `localhost` / IPv6 `[::1]`?是否支持自定义 host?
- plugin sandbox 的 Origin 字符串具体是什么格式?
- preflight-only 媒体类型:实际用 `application/json` 还是更严苛的自定义类型?
- 当用户运行 `figma.com` (browser-based)而非 desktop 时,Origin 是否相同?

## 相关

- [[projects/figwright/figwright]] 项目主页
- 中继架构 [[projects/figwright/concepts/mcp-local-relay-architecture]]
- 参考 [[references/sysctl-hardening-table]] / [[concepts/linux-server-hardening-checklist]]