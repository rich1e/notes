---
title: >-
  cf-pages/Telegraph-Image — 上游图床（GitHub 仓库）
category: references
tags: [cloudflare, image-hosting, telegram, open-source]
sources:
  - "https://github.com/cf-pages/Telegraph-Image"
source_url: "https://github.com/cf-pages/Telegraph-Image"
created: 2026-07-31T06:29:00Z
updated: 2026-07-31T06:29:00Z
summary: >-
  Telegraph-Image 是 CloudFlare ImgBed 的上游：基于 Cloudflare Pages + Telegram Bot API 的免费图床，
  把图片存到 Telegram 服务器。其局限（getFile ≤20MB、速率限制、免费配额）正是催生 fork 的动因。
provenance:
  extracted: 0.9
  inferred: 0.07
  ambiguous: 0.03
base_confidence: 0.62
lifecycle: draft
lifecycle_changed: "2026-07-31"
---

# cf-pages/Telegraph-Image（上游）

- **URL**: https://github.com/cf-pages/Telegraph-Image
- **定位**: Flickr/imgur 免费替代，基于 Cloudflare Pages + Telegram Bot API
- **下游**: [[entities/cloudflare-imgbed]] 脱胎自此项目

## 这个源覆盖什么

CloudFlare ImgBed 的**上游血缘**。理解这个源，才能理解 ImgBed 为什么长成现在的样子——ImgBed 的多存储后端、管理面板、API Token 全是在补 Telegraph-Image 的局限。

## 工作原理（extracted）

- 文件经 **Telegram Bot API** 上传，存到 **Telegram 服务器**当免费图床（[[concepts/telegram-as-blob-storage]] 的原型）。
- 原本用 Telegraph API，官方关停后改为设 `TG_Bot_Token` + `TG_Chat_ID` 走 Telegram Channel。
- 部署：fork 仓库 → 连 Cloudflare Pages → 把 bot 设为频道管理员。
- 可选 R2：`STORAGE_PROVIDER=r2`。

## 催生 fork 的局限（extracted）

| 局限 | 数值 |
|---|---|
| getFile 下载端点 | 仅支持 ≤20MB 文件（Bot API 上传虽允许 ~50MB，但传上去下不回来） |
| Telegram 速率 | 每频道约 20 条消息/分钟 |
| Cloudflare 免费 tier | Functions 10 万请求/日；KV 每日 1000 写 / 10 万读 / 1000 删 / 1000 list |
| 加载速度 | 部分地区不保证 |
| 内容审查 | 旧 moderatecontent.com 停止新注册 |

> 这些局限**没被原文明说是 fork 动因**，但 ImgBed 恰好逐条解决了它们（多后端绕开单一 Telegram 限制、内置审查替代停摆的第三方）。^[inferred]

## 相关页面

- [[entities/cloudflare-imgbed]] — 下游演进项目
- [[concepts/telegram-as-blob-storage]] — 把 IM 平台当免费对象存储
- [[sources/cloudflare-imgbed-github]] — 下游仓库源
- [[synthesis/Research: CloudFlare ImgBed]] — 研究综合页
