---
title: Trek 认证与安全系统
category: concepts
tags:
  - auth
  - security
  - jwt
  - oauth
  - passkey
  - mfa
sources:
  - "_raw/trek.txt (Gitingest export, 2026-07-02)"
created: 2026-07-02T00:00:00Z
updated: 2026-07-02T00:00:00Z
summary: Trek 支持 JWT + Cookie、OAuth 2.1、OIDC、WebAuthn Passkeys 和 TOTP MFA 五种认证机制，加密密钥与 JWT 密钥分离设计，支持独立轮转。
tier: supporting
lifecycle: draft
lifecycle_changed: "2026-07-02"
base_confidence: 0.83
provenance:
  extracted: 0.83
  inferred: 0.17
  ambiguous: 0.00
relationships:
  - target: "[[projects/trek/trek]]"
    type: related_to
  - target: "[[projects/trek/concepts/architecture-overview]]"
    type: related_to
  - target: "[[projects/trek/concepts/mcp-server]]"
    type: uses
---

# Trek 认证与安全系统

## 认证方式总览

Trek 支持五种认证机制，可同时存在：

| 机制 | 说明 | Token 类型 |
|---|---|---|
| **JWT + Cookie** | 标准会话，`trek_session` cookie | HS256 JWT |
| **OIDC / SSO** | Google、Apple、Authentik、Keycloak 等 | OIDC ID Token → 内部 JWT |
| **WebAuthn Passkeys** | 无密码，指纹/面部/PIN/安全密钥 | WebAuthn Credential |
| **TOTP MFA** | 两步验证 + 备份码 | 短期 MFA 挑战 token |
| **OAuth 2.1** | MCP 客户端授权 | `trekoa_` Access Token + `trekrf_` Refresh Token |

## 密钥架构

Trek 将**加密密钥**和 **JWT 密钥**分离，支持独立轮转：

### ENCRYPTION_KEY（静态数据加密）
用于加密存储的敏感数据：API 密钥、MFA TOTP 密钥、SMTP 密码、OIDC 客户端密钥等。

解析优先级：
1. `ENCRYPTION_KEY` 环境变量（最高优先级）
2. `data/.encryption_key` 文件
3. `data/.jwt_secret`（一次性迁移路径，旧版本升级时）
4. 自动生成（全新安装）

### JWT_SECRET（会话令牌签名）
自动生成并持久化到 `data/.jwt_secret`。可通过管理面板轮转，不建议通过环境变量设置（会覆盖轮转后的值）。

**轮转时的动态更新：** `updateJwtSecret(newSecret)` 函数更新进程内绑定，所有现有会话立即失效。

## 会话管理

### 会话时长配置

| 场景 | 环境变量 | 默认值 |
|---|---|---|
| 普通登录（不勾选"记住我"） | `SESSION_DURATION` | 24h |
| 勾选"记住我" | `SESSION_DURATION_REMEMBER` | 30d |

- 不勾选"记住我"：使用浏览器会话 cookie（关闭浏览器后自动清除）
- 勾选"记住我"：使用持久化 cookie，浏览器重启后依然有效

### password_version 机制

`users` 表有 `password_version` 字段，每次密码变更时递增。

- JWT token 携带 `pv` 声明（密码版本号）
- 服务端验证 JWT 时比对 `pv` 与当前 `password_version`
- 不匹配则拒绝（防止密码变更后旧 token 继续有效）
- WebSocket 临时 token 也受此保护

## WebAuthn Passkeys

存储在 `webauthn_credentials` 表：
- `credential_id` — UNIQUE
- `public_key` — BLOB
- `counter` — 防重放计数器
- `backed_up` — 是否备份（跨设备同步的凭据）
- `aaguid` — 认证器类型标识

挑战（challenge）存储在 `webauthn_challenges` 表，有过期时间，防止重放攻击。

## OIDC 集成

环境变量配置：

```bash
OIDC_ISSUER=https://auth.example.com
OIDC_CLIENT_ID=trek
OIDC_CLIENT_SECRET=supersecret
OIDC_DISPLAY_NAME=SSO          # 登录按钮文字
OIDC_ONLY=false               # 纯 SSO 模式（禁用密码登录）
OIDC_ADMIN_CLAIM=groups        # 判断管理员的声明字段
OIDC_ADMIN_VALUE=app-trek-admins
APP_URL=https://trek.example.com  # OIDC redirect_uri 基础 URL（必须）
```

Authentik 非标准路径示例：
```bash
OIDC_DISCOVERY_URL=https://auth.example.com/application/o/trek/.well-known/openid-configuration
```

## OAuth 2.1（MCP 用）

Trek 同时扮演 **OAuth 授权服务器**角色（供 MCP 客户端使用）。

关键端点：
- `/.well-known/oauth-protected-resource` — RFC 9728 资源服务器元数据
- `/.well-known/oauth-authorization-server` — RFC 8414 授权服务器元数据
- `/oauth/register` — RFC 7591 动态客户端注册
- `/oauth/authorize` — 授权端点（用户同意页面）
- `/oauth/token` — Token 端点

Token 轮转策略：
- Access Token：1 小时有效期，受众绑定到 `/mcp`
- Refresh Token：30 天滚动有效期，前缀 `trekrf_`
- **重放检测**：一旦检测到刷新 token 被重用，级联吊销整个 token 链

## MFA 策略

- 管理员可设置全局"要求 MFA"策略（`app_settings` 表中 `require_mfa` 键）
- 设置后，未启用 MFA 的用户被拒绝访问（包括 WebSocket 连接）
- 支持 TOTP + 备份码（备份码存储加密后的 hash）

## SSRF 防护

`server/src/utils/ssrfGuard.ts` 防止服务端请求伪造：
- 默认阻止所有出站请求到私有/RFC-1918 IP 段
- `ALLOW_INTERNAL_NETWORK=true` 可允许局域网访问（用于 Immich 等本地服务）
- 回环地址和链路本地地址始终被阻止

## 安全相关 HTTP 头

通过 `globalMiddleware.ts` 配置：
- **HSTS**：`FORCE_HTTPS=true` 时启用，`HSTS_INCLUDE_SUBDOMAINS=false` 可选是否包含子域
- **CSP**：内容安全策略
- **CORS**：通过 `ALLOWED_ORIGINS` 配置允许的来源
- **幂等性**：`idempotency.interceptor.ts` 防止重复提交

## 相关页面

- [[projects/trek/concepts/architecture-overview]] — 整体架构（中间件 pipeline）
- [[projects/trek/concepts/mcp-server]] — MCP OAuth 2.1 详解
- [[projects/trek/concepts/realtime-sync]] — WebSocket 临时 token 认证
- [[projects/trek/references/environment-variables]] — 环境变量配置参考
