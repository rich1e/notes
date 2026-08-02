---
title: Sanyue-ImgHub
category: entities
tags: [cloudflare, image-hosting, vue, f2e]
sources:
  - "https://github.com/MarSeventh/Sanyue-ImgHub"
created: 2026-07-31T06:29:00Z
updated: 2026-07-31T06:29:00Z
summary: >-
  MarSeventh/Sanyue-ImgHub：CloudFlare ImgBed 的前端仓库，Vue.js（Vue 3 + Element Plus）构建，
  可独立定制后 build 出 dist 塞回主项目。MIT 许可。
provenance:
  extracted: 0.85
  inferred: 0.12
  ambiguous: 0.03
base_confidence: 0.62
lifecycle: draft
lifecycle_changed: "2026-07-31"
tier: supporting
---

# Sanyue-ImgHub

**Sanyue-ImgHub**（仓库 `MarSeventh/Sanyue-ImgHub`）是 [[entities/cloudflare-imgbed]] 的**前端仓库**——可定制的 UI 层，与后端解耦。

## 事实

- **角色**: CloudFlare ImgBed 的前端（About 明写 "Frontend of MarSeventh/CloudFlare-ImgBed"）
- **技术栈**: Vue.js（`vue.config.js` / `babel.config.js` / `vitest.config.js`）；文档站标注为 **Vue 3 + Element Plus**
- **后端地址配置**: `.env.development` 里的 `VUE_APP_BACKEND_URL`
- **许可**: MIT

## 定制工作流

1. 本地拉起 CloudFlare-ImgBed 当后端。
2. 拉 Sanyue-ImgHub，设 `VUE_APP_BACKEND_URL` 指向后端。
3. 改代码（DIY）→ `npm run build`。
4. 把 `/dist` 内容拷进主项目根 → 部署。

> 前后端分离让「换皮」不动后端逻辑——ImgBed 主仓库里 `frontend-dist/` 就是这里 build 出来的产物。

## 相关页面

- [[entities/cloudflare-imgbed]] — 后端主项目
- [[concepts/serverless-image-hosting]] — 所属架构范式
- [[synthesis/Research: CloudFlare ImgBed]] — 研究综合页
