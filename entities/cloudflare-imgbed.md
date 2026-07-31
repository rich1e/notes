---
title: CloudFlare ImgBed
category: entities
tags: [cloudflare, image-hosting, serverless, open-source]
sources:
  - "https://github.com/MarSeventh/CloudFlare-ImgBed"
  - "https://cfbed.sanyue.de/guide/introduction.html"
created: 2026-07-31T06:29:00Z
updated: 2026-07-31T06:29:00Z
summary: >-
  MarSeventh 开发的开源自托管文件/图床：Cloudflare Serverless + Docker 双部署，多存储后端
  （Telegram/R2/S3/Discord/HuggingFace/WebDAV），Vue 3 前端，MIT 许可，脱胎自 Telegraph-Image。
provenance:
  extracted: 0.88
  inferred: 0.09
  ambiguous: 0.03
base_confidence: 0.62
lifecycle: draft
lifecycle_changed: "2026-07-31"
tier: core
---

# CloudFlare ImgBed

**CloudFlare ImgBed**（仓库 `MarSeventh/CloudFlare-ImgBed`）是一个**开源、自托管的文件/图床解决方案**，把多种存储后端统一到单一管理界面，用于个人图床、站点资产管理和轻量文件分发。它是 [[concepts/serverless-image-hosting]] 范式的代表实现。

## 事实

- **作者/组织**: MarSeventh
- **许可**: MIT
- **上游**: 脱胎自 [[sources/telegraph-image-github]]（cf-pages/Telegraph-Image）
- **前端**: [[entities/sanyue-imghub]]（Vue 3 + Element Plus）
- **桌面客户端**: MarSeventh/satellite

## 部署形态

- **Cloudflare Serverless**：Pages Functions / Workers，数据层用 KV 或 D1。
- **Docker 自托管**：Node.js + Hono 后端 + Sharp 图像处理 + 本地 SQLite。

## 核心能力

- 多存储后端：**Telegram / Discord / Cloudflare R2 / S3 / Hugging Face / WebDAV**，多通道负载均衡 + 故障转移。
- 鉴权：PBKDF2 密码哈希 + HttpOnly Cookie 会话。
- API Token：细粒度权限 + 过期 + 自动删除。
- 管理面板：仪表盘、用户管理、暗色模式、中英切换。
- 内容审查、递归文件夹上传、随机图 API、URL 参数图像处理、大文件分块上传。
- 完整 REST API + WebDAV 服务。

## 相对上游的演进 ^[inferred]

Telegraph-Image 只把图存到 Telegram、受制于单一后端与免费配额；ImgBed 逐条补足：**多后端**（绕开 Telegram 20MB/速率限制）、**内置审查**（替代停摆的 moderatecontent.com）、**管理面板 + API Token**（从「能存」到「可运营」）。

## 相关页面

- [[concepts/serverless-image-hosting]] — 所属架构范式
- [[concepts/telegram-as-blob-storage]] — 其存储后端之一的模式
- [[entities/sanyue-imghub]] — 前端项目
- [[sources/cloudflare-imgbed-github]] / [[sources/cloudflare-imgbed-docs]] — 一手源
- [[sources/telegraph-image-github]] — 上游
- [[synthesis/Research: CloudFlare ImgBed]] — 研究综合页

## 关联关系

```yaml
extends:
  - "[[sources/telegraph-image-github]]"      # 脱胎并补足上游局限
uses:
  - "[[concepts/telegram-as-blob-storage]]"   # 多后端之一
  - "[[entities/sanyue-imghub]]"              # 前端
related_to:
  - "[[concepts/serverless-image-hosting]]"   # 所属范式
```
