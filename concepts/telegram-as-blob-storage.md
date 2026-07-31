---
title: 把 IM 平台当免费对象存储（Telegram as Blob Storage）
category: concepts
tags: [telegram, image-hosting, storage]
sources:
  - "https://github.com/cf-pages/Telegraph-Image"
  - "https://github.com/MarSeventh/CloudFlare-ImgBed"
created: 2026-07-31T06:29:00Z
updated: 2026-07-31T06:29:00Z
summary: >-
  用 Telegram/Discord Bot API 把即时通讯平台当免费无限对象存储的模式：上传即发消息、读取即 getFile。
  零成本但受制于速率、单文件大小与平台政策，是「白嫖」范式的典型。
provenance:
  extracted: 0.78
  inferred: 0.17
  ambiguous: 0.05
base_confidence: 0.55
lifecycle: draft
lifecycle_changed: "2026-07-31"
tier: supporting
---

# 把 IM 平台当免费对象存储（Telegram as Blob Storage）

一种「白嫖」存储模式：把 **Telegram / Discord 等 IM 平台**当免费、近乎无限的对象存储——**上传 = 给频道发一条消息**，**读取 = 调 getFile 拿回文件**。[[sources/telegraph-image-github]]（Telegraph-Image）是原型，[[entities/cloudflare-imgbed]] 把它列为多后端之一。

## 机制

1. 建一个 Bot，拿 `TG_Bot_Token`；建一个频道，拿 `TG_Chat_ID`，把 Bot 设为频道管理员。
2. 上传：图床后端把文件通过 Bot API 发到频道，记下返回的 `file_id`。
3. 读取：拿 `file_id` 调 `getFile` → 得到 Telegram CDN 的临时 URL → 代理回给用户。
4. 索引：`file_id` 与访问路径的映射存在图床自己的元数据层（KV/D1/SQLite）。

## 代价与风险

| 维度 | 限制 |
|---|---|
| 单文件大小 | getFile 下载端点 ≤20MB（上传虽可 ~50MB，但大于 20MB 下不回来） |
| 速率 | 每频道约 20 条消息/分钟 |
| 政策风险 | 平台可随时改规则或封号；Telegraph API 已被官方关停 |
| 合规 | 内容审查责任仍在图床方，需自建 moderation |

## 为什么仍被采用

- **零存储成本**：对个人图床/小站极有吸引力。
- **多后端兜底**：ImgBed 把 Telegram 当「负载均衡通道之一」，同时支持 R2/S3，用可控存储对冲政策风险——这是「白嫖」升级为「工程可用」的关键。^[inferred]

## 相关页面

- [[concepts/serverless-image-hosting]] — 上层图床范式
- [[entities/cloudflare-imgbed]] — 把此模式列为多后端之一
- [[sources/telegraph-image-github]] — 该模式的原型实现
- [[synthesis/Research: CloudFlare ImgBed]] — 研究综合页
