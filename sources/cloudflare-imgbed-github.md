---
title: >-
  MarSeventh/CloudFlare-ImgBed — GitHub 仓库
category: references
tags: [cloudflare, image-hosting, serverless, open-source]
sources:
  - "https://github.com/MarSeventh/CloudFlare-ImgBed"
source_url: "https://github.com/MarSeventh/CloudFlare-ImgBed"
created: 2026-07-31T06:29:00Z
updated: 2026-07-31T06:29:00Z
summary: >-
  CloudFlare ImgBed 主仓库：自托管文件/图床，支持 Cloudflare Serverless + Docker 双部署，
  多存储后端（Telegram/R2/S3/Discord/HuggingFace/WebDAV），MIT 许可，脱胎自 Telegraph-Image。
provenance:
  extracted: 0.9
  inferred: 0.08
  ambiguous: 0.02
base_confidence: 0.62
lifecycle: draft
tier: supporting
lifecycle_changed: "2026-07-31"
---

# MarSeventh/CloudFlare-ImgBed（GitHub 仓库）

- **URL**: https://github.com/MarSeventh/CloudFlare-ImgBed
- **许可**: MIT
- **上游**: fork/演进自 [[sources/telegraph-image-github]]（cf-pages/Telegraph-Image）
- **前端仓库**: [[entities/sanyue-imghub]]（MarSeventh/Sanyue-ImgHub）

## 这个源覆盖什么

CloudFlare ImgBed 的权威一手仓库，实体页见 [[entities/cloudflare-imgbed]]。它是一个**自托管的文件/图床解决方案**，把多种存储后端统一到单一管理界面里，用于「个人图床、站点资产管理、轻量文件分发」。

## 关键声明（extracted）

- **双部署形态**：Cloudflare Serverless（Pages Functions / Workers）+ Docker 自托管（含 `Dockerfile` 与 `docker-compose.yml`）。
- **多存储后端**：Telegram、Discord、Cloudflare R2、S3 兼容存储、Hugging Face、WebDAV。
- **仓库结构**：`functions/`（serverless 逻辑）、`frontend-dist/`（前端产物）、`database/`、`deploy/`。
- **数据层**：Cloudflare 部署用 KV 或 D1；Docker 用本地 SQLite。^[inferred]
- **关联项目**：桌面客户端 MarSeventh/satellite；前端 MarSeventh/Sanyue-ImgHub。
- **规模**：约 6k stars、1000+ commits（计数为 WebFetch 抓取值，forks 数字反常偏高，见综合页 flag）。^[ambiguous]

## 局限

- 仓库主页信息偏概览，KV binding 名称、API 端点格式等细节需查官方文档站 [[sources/cloudflare-imgbed-docs]]。
- 免费 tier 的配额上限继承自 Cloudflare（KV 每日写/读限额）与 Telegram（getFile ≤20MB、Bot 速率限制）——见上游 [[sources/telegraph-image-github]]。

## 相关页面

- [[entities/cloudflare-imgbed]] — 主实体
- [[concepts/serverless-image-hosting]] — 无服务器图床范式
- [[concepts/telegram-as-blob-storage]] — 把 IM 平台当免费对象存储
- [[synthesis/Research: CloudFlare ImgBed]] — 研究综合页
