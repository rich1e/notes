---

title: >-
  xk-ai-talk-desk-ui
category: projects
tags:
  - react
  - typescript
  - webrtc
  - call-center
  - zustand
sources: [projects/xk-ai-talk-desk-ui]
summary: >-
  AI 外呼热转坐席前端，基于 React 19 + JsSIP + 信科 CC SDK，承接 AI 智能客服转人工通话。
provenance:
  extracted: 0.75
  inferred: 0.2
  ambiguous: 0.05
base_confidence: 0.73
lifecycle: reviewed
lifecycle_changed: 2026-08-03
lifecycle_reason: "auto-promoted by wiki-lint --consolidate: age>30d, confidence>0.7"
created: 2026-06-29
updated: 2026-08-03T05:47:33Z
relationships:
  - target: "[[projects/jrfed-zaxd-mediation-tool/concepts/permission-system]]"
    type: related_to
  - target: "[[entities/zustand]]"
    type: uses
---

# xk-ai-talk-desk-ui

AI 外呼热转坐席工作台前端。核心场景：AI 智能客服与客户通话后，将通话转给人工坐席继续处理；人工坐席也可手动拨打外呼。

## 技术栈

| 层次 | 技术 |
|------|------|
| 框架 | React 19 + TypeScript 6.0 |
| 构建 | Vite 8，端口 5566 |
| UI | Ant Design 6 + Pro Components + Tailwind CSS 4 |
| 状态 | [[entities/zustand|Zustand]] 5（persist 持久化到 localStorage） |
| 路由 | React Router 7 |
| 电话 SDK | JsSIP 3 + 信科 LaihuAPI（WebRTC + CC 双通道） |
| HTTP | Axios，`/api` 代理到后端 |

## 核心模块

- **[[projects/xk-ai-talk-desk-ui/concepts/call-center-sdk-integration|CC SDK 集成]]** — `useSoftbar` Hook 封装信科 LaihuAPI，管理所有通话事件与状态机
- **[[projects/xk-ai-talk-desk-ui/concepts/agent-state-machine|坐席状态机]]** — Offline → Online ⇄ Rest，通话时自动切 Busy
- **PhoneBar** — 电话条，所有通话操作的唯一入口（签入/签出、外呼、接听、挂断、转接、会议）
- **CallSessionModal** — 通话弹窗，展示 AI 对话记录 + 坐席标注
- **Dashboard** — 今日数据概览（接听数/拨打数/接起率等）
- **TransferRecords** — 热转通话记录，带筛选和回拨
- **ManualCallRecords** — 手动拨打记录，带筛选和回拨

## 路由结构

```
/login            → Login（无需鉴权）
/                 → Dashboard（AuthGuard 保护）
/records/transfer → TransferRecords
/records/manual   → ManualCallRecords
*                 → 重定向到 /
```

## 状态管理设计

两个 Zustand Store：
- `useAuthStore` — token + user，`persist` 持久化，key 为 `AI_TALK_DESK`
- `useAgentStore` — `makeCall` 函数 + `canMakeCall` 标志，供跨组件触发外呼

登录接口 `/api/auth/login` 返回 token，写入 store 后自动持久化。

## 代理配置

- **开发**：`/api` → `process.env.AITALK_API` 或 `http://xk-ai-talk-desk.test.xinke.biz`
- **生产**：`server/app.js`（Express + http-proxy-middleware），通过 `DEPLOY_BIZ_ENV` 或 `SERVICE_URL` 切换目标

## 相关页面

- [[projects/xk-ai-talk-desk-ui/concepts/call-center-sdk-integration]]
- [[projects/xk-ai-talk-desk-ui/concepts/agent-state-machine]]
- [[projects/xk-ai-talk-desk-ui/skills/phonebar-call-flow]]

## Related

- [[projects/jrfed-zaxd-mediation-tool/concepts/permission-system]] — >-
