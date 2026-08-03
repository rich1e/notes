---
title: Trek 环境变量配置参考
category: references
tags:
  - configuration
  - docker
  - deployment
  - reference
sources:
  - "_raw/trek.txt (Gitingest export, 2026-07-02)"
created: 2026-07-02T00:00:00Z
updated: 2026-08-03T05:47:33Z
summary: Trek 通过环境变量配置，核心变量包括 ENCRYPTION_KEY、APP_URL（OIDC 必须）、SESSION_DURATION，MCP 相关变量控制速率和会话数量。
tier: peripheral
lifecycle: reviewed
lifecycle_changed: 2026-08-03
lifecycle_reason: "auto-promoted by wiki-lint --consolidate: age>30d, confidence>0.7"
base_confidence: 0.90
provenance:
  extracted: 0.95
  inferred: 0.05
  ambiguous: 0.00
relationships:
  - target: "[[projects/trek/trek]]"
    type: related_to
  - target: "[[projects/trek/concepts/auth-system]]"
    type: related_to
---

# Trek 环境变量配置参考

## 核心变量

| 变量 | 说明 | 默认值 |
|---|---|---|
| `PORT` | 服务器端口 | `3000` |
| `NODE_ENV` | 环境（`production` / `development`） | `production` |
| `ENCRYPTION_KEY` | 静态数据加密密钥（API 密钥、MFA、SMTP、OIDC）。推荐：`openssl rand -hex 32` | 自动生成 |
| `TZ` | 时区（如 `Europe/Berlin`，用于日志、提醒、定时任务） | `UTC` |
| `LOG_LEVEL` | `info`=简洁用户操作，`debug`=详细 | `info` |
| `DEFAULT_LANGUAGE` | 登录页默认语言（浏览器语言自动检测优先）。支持：de/en/es/fr/hu/nl/br/cs/pl/ru/zh/zh-TW/it/ar/id/tr/ja/ko/uk/gr | `en` |
| `ALLOWED_ORIGINS` | CORS 和邮件链接的允许来源（逗号分隔） | 同源 |

## HTTPS 与代理

| 变量 | 说明 | 默认值 |
|---|---|---|
| `FORCE_HTTPS` | `true` 时：301 重定向 HTTP→HTTPS，HSTS，CSP upgrade-insecure-requests，强制 `secure` cookie。需配合 TLS 终止反向代理使用，需要 `TRUST_PROXY`。 | `false` |
| `HSTS_INCLUDE_SUBDOMAINS` | `true` 时：HSTS 包含 `includeSubDomains`。仅在 HSTS 生效时有效。若子域有 HTTP 服务，保留 `false`。 | `false` |
| `COOKIE_SECURE` | 控制 `trek_session` cookie 的 `secure` 标志。自动派生：`NODE_ENV=production` 或 `FORCE_HTTPS=true` 时开启。紧急情况下可设 `false` 允许 HTTP cookie。 | 自动 |
| `TRUST_PROXY` | 受信任的反向代理数量，用于读取 `X-Forwarded-For` 和 `X-Forwarded-Proto`。 | 生产环境 `1` |
| `ALLOW_INTERNAL_NETWORK` | `true` 时允许访问私有/RFC-1918 IP（如局域网 Immich）。回环和链路本地始终被阻止。 | `false` |

## 会话时长

| 变量 | 说明 | 默认值 |
|---|---|---|
| `SESSION_DURATION` | 普通登录（不勾选"记住我"）的会话时长。格式：`1h`/`12h`/`7d`/`30d`/`90d`。无效值回退到默认。 | `24h` |
| `SESSION_DURATION_REMEMBER` | 勾选"记住我"的会话时长（持久化 cookie）。同上格式。 | `30d` |

## OIDC / SSO

| 变量 | 说明 | 默认值 |
|---|---|---|
| `APP_URL` | 实例公网 URL（如 `https://trek.example.com`）。**OIDC 启用时必须设置**；也用于邮件通知链接中的基础 URL。 | — |
| `OIDC_ISSUER` | OpenID Connect 提供商 URL | — |
| `OIDC_CLIENT_ID` | OIDC 客户端 ID | — |
| `OIDC_CLIENT_SECRET` | OIDC 客户端密钥 | — |
| `OIDC_DISPLAY_NAME` | SSO 登录按钮上的文字 | `SSO` |
| `OIDC_ONLY` | `true` 时：禁用密码登录和注册，首个 SSO 登录成为管理员 | `false` |
| `OIDC_ADMIN_CLAIM` | 用于识别管理员用户的 OIDC 声明字段 | — |
| `OIDC_ADMIN_VALUE` | 授予管理员角色的声明值 | — |
| `OIDC_SCOPE` | 自定义 OIDC 范围（**完全替换**默认值，始终包含 `openid email profile`） | `openid email profile` |
| `OIDC_DISCOVERY_URL` | 覆盖 OIDC 发现端点（Authentik 等非标准路径） | — |

## 初始化配置

| 变量 | 说明 | 默认值 |
|---|---|---|
| `ADMIN_EMAIL` | 首次启动时创建的管理员邮箱（须与 `ADMIN_PASSWORD` 同时设置；用户已存在时无效） | `admin@trek.local` |
| `ADMIN_PASSWORD` | 首次启动时创建的管理员密码 | 随机（输出到容器日志） |

## MCP 相关

| 变量 | 说明 | 默认值 |
|---|---|---|
| `MCP_RATE_LIMIT` | 每用户每分钟最大 MCP API 请求数 | `300` |
| `MCP_MAX_SESSION_PER_USER` | 每用户最大并发 MCP 会话数 | `20` |

## 其他

| 变量 | 说明 | 默认值 |
|---|---|---|
| `DEMO_MODE` | 启用 Demo 模式（每小时数据重置） | `false` |
| `KITINERARY_EXTRACTOR_PATH` | KDE Itinerary 提取器二进制路径（未设置时自动检测） | — |

## Docker Compose 最佳实践

```yaml
services:
  app:
    image: mauriceboe/trek:latest
    read_only: true
    security_opt:
      - no-new-privileges:true
    cap_drop: [ALL]
    cap_add: [CHOWN, SETUID, SETGID]
    tmpfs:
      - /tmp:noexec,nosuid,size=64m
    volumes:
      - ./data:/app/data
      - ./uploads:/app/uploads
    # ⚠️ 禁止挂载 /app，会隐藏应用代码导致启动失败
```

> **警告：** 只挂载 `./data:/app/data` 和 `./uploads:/app/uploads`，切勿挂载 `/app`。

## 相关页面

- [[projects/trek/trek]] — 项目概览与快速启动
- [[projects/trek/concepts/auth-system]] — 认证机制（密钥、OIDC、会话）
- [[projects/trek/concepts/mcp-server]] — MCP OAuth 配置
