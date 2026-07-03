---
title: Trek — 自托管实时协同旅行计划器
category: projects
tags:
  - self-hosted
  - travel-app
  - nestjs
  - react
  - pwa
sources:
  - "_raw/trek.txt (Gitingest export, 2026-07-02)"
created: 2026-07-02T00:00:00Z
updated: 2026-07-02T00:00:00Z
summary: Trek 是一个自托管、实时协同旅行计划器，支持地图、预算、行李清单、日志和 AI MCP 接口，采用 NestJS + React + SQLite 技术栈。
tier: core
lifecycle: draft
lifecycle_changed: "2026-07-02"
base_confidence: 0.83
provenance:
  extracted: 0.85
  inferred: 0.15
  ambiguous: 0.00
relationships:
  - target: "[[projects/trek/concepts/architecture-overview]]"
    type: related_to
  - target: "[[projects/trek/concepts/mcp-server]]"
    type: related_to
  - target: "[[projects/trek/concepts/addon-system]]"
    type: related_to
  - target: "[[projects/trek/concepts/realtime-sync]]"
    type: related_to
---

# Trek — 自托管实时协同旅行计划器

**Trek** 是一个开源、自托管的实时协同旅行计划器。用户可以在自己的服务器上运行它，与团队成员实时协作管理旅行行程，支持地图、预算、行李清单、旅行日志和 AI 自动化（通过 MCP）。

- GitHub: `mauriceboe/TREK`
- 许可证: AGPL v3
- Demo: `demo.liketrek.com`
- Docker Hub: `mauriceboe/trek`

## 核心功能

### 行程规划
- **拖放式日程规划器** — 将地点组织成按天的计划，支持跨天移动
- **交互式地图** — Leaflet 或 Mapbox GL，支持 3D 建筑、地形、照片标记、聚类、路线可视化
- **地点搜索** — Google Places（照片、评分、营业时间）或 OpenStreetMap（免费）
- **地点导入** — 共享的 Google Maps / Naver Maps 列表，以及 GPX、KML/KMZ/GeoJSON 文件
- **路线优化** — 自动排序地点并导出到 Google Maps
- **天气预报** — 16 天预报（Open-Meteo，无需 key）+ 历史气候备选

### 旅行管理
- **预订管理** — 航班、住宿、餐厅，含状态、确认号、文件；支持从预订确认邮件和 PDF 导入（KDE Itinerary）
- **费用管理** — 追踪并分摊行程开销（类 Splitwise）：人均/每日明细、结算、多货币
- **行李清单** — 分类、模板、用户分配、进度跟踪
- **文档管理** — 将文档、票据、PDF 附加到行程/地点/预订（每个最大 50 MB）
- **PDF 导出** — 生成含封面页、图片、笔记的完整行程 PDF

### 协作
- **实时同步** — WebSocket，更改即时出现在所有连接用户
- **多用户行程** — 基于角色的访问控制邀请成员
- **SSO (OIDC)** — 支持 Google、Apple、Authentik、Keycloak 或任意 OIDC 提供商
- **2FA** — TOTP + 备份码
- **Passkeys** — 无密码 WebAuthn 登录（指纹/面部/PIN/安全密钥），管理员可切换
- **协作套件** — 群聊、共享笔记、投票、每日打卡

### 移动端 & PWA
- **可安装** — iOS 和 Android，直接从浏览器安装，无需 App Store
- **离线支持** — Service Worker 通过 Workbox 缓存瓦片、API、上传
- **触控优化** — 移动端专用布局，含安全区域处理

## 技术栈

| 层 | 技术 |
|---|---|
| 运行时 | Node.js 22 |
| 后端框架 | NestJS 11 |
| 数据库 | SQLite (better-sqlite3) |
| 前端框架 | React 19 |
| 构建工具 | Vite |
| 语言 | TypeScript |
| 样式 | Tailwind CSS |
| 地图 | Leaflet + Mapbox GL |
| 状态管理 | Zustand |
| 实时通信 | WebSocket (ws) |
| 认证 | JWT + OAuth 2.1 + OIDC + Passkeys (WebAuthn) + TOTP MFA |
| 天气 | Open-Meteo（无需 key） |
| 容器化 | Docker / Helm |

## 快速启动

```bash
ENCRYPTION_KEY=$(openssl rand -hex 32) docker run -d -p 3000:3000 \
  -e ENCRYPTION_KEY=$ENCRYPTION_KEY \
  -v ./data:/app/data -v ./uploads:/app/uploads mauriceboe/trek
```

首次启动后，访问 `http://localhost:3000`，Trek 会自动创建管理员账户（凭据输出到容器日志）。

## 数据存储

- **数据库** — `./data/travel.db`（SQLite）
- **上传文件** — `./uploads/`
- **日志** — `./data/logs/trek.log`（自动轮转）
- **备份** — 通过管理面板创建和恢复

## 相关页面

- [[projects/trek/concepts/architecture-overview]] — 整体架构设计
- [[projects/trek/concepts/addon-system]] — 插件系统设计
- [[projects/trek/concepts/mcp-server]] — AI/MCP 集成
- [[projects/trek/concepts/realtime-sync]] — 实时同步机制
- [[projects/trek/concepts/auth-system]] — 认证与安全
- [[projects/trek/references/database-schema]] — 数据库表结构
- [[projects/trek/references/environment-variables]] — 环境变量配置参考
