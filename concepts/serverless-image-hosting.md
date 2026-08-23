---
title: 无服务器图床（Serverless Image Hosting）
category: concepts
tags: [serverless, image-hosting, cloudflare]
sources:
  - "https://github.com/MarSeventh/CloudFlare-ImgBed"
  - "https://cfbed.sanyue.de/guide/introduction.html"
created: 2026-07-31T06:29:00Z
updated: 2026-07-31T06:29:00Z
summary: >-
  无服务器图床范式：用边缘函数（Cloudflare Pages Functions/Workers）做上传/读取路由，
  存储外包给对象存储或第三方（R2/S3/Telegram），无需常驻服务器，靠免费/低价 tier 运行。
provenance:
  extracted: 0.75
  inferred: 0.2
  ambiguous: 0.05
base_confidence: 0.55
lifecycle: draft
lifecycle_changed: "2026-07-31"
tier: supporting
---

# 无服务器图床（Serverless Image Hosting）

一种**图床架构范式**：不租常驻服务器，而是把上传/读取逻辑放进**边缘 serverless 函数**，把实际字节外包给对象存储或第三方平台。[[entities/cloudflare-imgbed]] 是这一范式的代表实现。

## 三个组成部分

1. **边缘计算层** — Cloudflare Pages Functions 或 Workers 承接上传/读取/删除/鉴权路由。无冷服务器，按请求计费，免费 tier 常够个人用。
2. **存储层（可换）** — 字节落到 Cloudflare R2、S3 兼容存储，或「借」第三方平台（[[concepts/telegram-as-blob-storage]]）。存储与计算解耦，可多后端负载均衡。
3. **元数据层** — Cloudflare KV / D1（或 Docker 下的 SQLite）存文件索引、目录、Token、配置。

## 为什么这样设计

- **成本趋零**：边缘函数 + 对象存储的免费额度可覆盖个人/小站，无固定月费。
- **免运维**：无服务器可打补丁/扩容，Cloudflare 托管边缘 + CDN + 安全。
- **可移植**：ImgBed 同时提供 Docker 形态（Node.js + Hono + Sharp + SQLite），说明「serverless」是部署选项而非架构锁定。

## 局限

- 受制于平台免费 tier 的硬配额（请求数、KV 读写次数、单文件大小）。
- 边缘函数执行时间/内存受限，大文件需分块上传。
- 「借」第三方存储（Telegram）有政策与速率风险——见 [[concepts/telegram-as-blob-storage]]。

## 相关页面

- [[entities/cloudflare-imgbed]] — 代表实现
- [[concepts/telegram-as-blob-storage]] — 存储层的一种「白嫖」变体
- cloudflare-imgbed-github / cloudflare-imgbed-docs — 一手源
- [[synthesis/Research: CloudFlare ImgBed]] — 研究综合页
