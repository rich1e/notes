---
title: >-
  CloudFlare ImgBed 官方文档站（cfbed.sanyue.de）
category: references
tags: [cloudflare, image-hosting, serverless, documentation]
sources:
  - "https://cfbed.sanyue.de/guide/introduction.html"
source_url: "https://cfbed.sanyue.de/"
created: 2026-07-31T06:29:00Z
updated: 2026-07-31T06:29:00Z
summary: >-
  CloudFlare ImgBed 官方文档站：给出完整能力清单与技术架构——Vue 3 + Element Plus 前端、
  Pages Functions/Workers/Hono 后端、KV 或 D1 数据层、PBKDF2 + HttpOnly Cookie 鉴权。
provenance:
  extracted: 0.92
  inferred: 0.05
  ambiguous: 0.03
base_confidence: 0.62
lifecycle: draft
lifecycle_changed: "2026-07-31"
---

# CloudFlare ImgBed 官方文档站

- **URL**: https://cfbed.sanyue.de/ （introduction 页：`/guide/introduction.html`）

## 这个源覆盖什么

官方文档站的 introduction 页，给出 [[entities/cloudflare-imgbed]] 最权威的**能力清单 + 技术架构**——比仓库主页更完整。

## 技术架构（extracted）

| 层 | 实现 |
|---|---|
| 前端 | **Vue 3 + Element Plus** |
| 后端 | Cloudflare Pages Functions/Workers（Serverless）；Docker 用 **Node.js + Hono** |
| 图像处理 | Pages 用同域 URL 转换；Workers 用 Images binding；Docker 用 **Sharp** |
| 数据层 | Cloudflare 部署用 **KV 或 D1**；Docker 用本地 **SQLite** |
| 许可 | MIT |

## 核心能力（extracted）

- **多存储后端**：Telegram / R2 / S3 / Discord / Hugging Face / WebDAV，统一管理。
- **鉴权**：**PBKDF2 密码哈希 + HttpOnly Cookie 会话管理**。
- **管理面板**：响应式仪表盘、用户管理、系统设置、暗色模式、中英切换。
- **API Token**：细粒度权限、过期时间、自动删除。
- **内容审查**（moderation）。
- **文件夹上传**：递归文件夹上传、批量操作、过滤。
- **随机图 API** + 完整的上传/读取/删除/列举/Token 管理 API + WebDAV 服务。
- **图像处理**：URL 参数做缩放/裁剪/拉伸。
- **负载均衡**：多通道均衡、容量限制、故障转移、大文件分块上传。

## 局限

- introduction 页不含具体 KV binding 名称、环境变量、部署命令——需查 quick-start / 配置说明子页。
- 文档站首页（landing）是营销页，正文在 `/guide/*` 子页。

## 相关页面

- [[entities/cloudflare-imgbed]] — 主实体
- [[sources/cloudflare-imgbed-github]] — 仓库源
- [[concepts/serverless-image-hosting]] — 无服务器图床范式
- [[synthesis/Research: CloudFlare ImgBed]] — 研究综合页
