---
title: >-
  PhoneBar 通话流程与操作指南
category: skills
tags: [react, call-center, webrtc, design-system]
sources: [projects/xk-ai-talk-desk-ui]
summary: >-
  热转来电与手动外呼的完整操作路径，PhoneBar 各子组件在通话生命周期中的切换逻辑。
provenance:
  extracted: 0.7
  inferred: 0.25
  ambiguous: 0.05
base_confidence: 0.7
lifecycle: draft
lifecycle_changed: 2026-06-29
created: 2026-06-29
updated: 2026-06-29
---

# PhoneBar 通话流程与操作指南

PhoneBar（`src/components/PhoneBar/index.tsx`）是坐席工作台的核心 UI 入口，基于 `useSoftbar` Hook 驱动。

## 热转来电流程

```
AI 外呼结束
    ↓
DeliveredEvt（含 dialogue AI 对话）
    ↓
IncomingBar 振铃 + CallSessionModal 弹出
（展示 AI 对话记录、客户信息）
    ↓
坐席点击接听 → answerFn()
    ↓
ActiveCallBar（通话中：静音/保持/转接/DTMF/挂断）
    + AgentAnnotation（标注：意向/标签/小结）
    ↓
挂断 → ConnectionClearedEvt → AFTER_CALL
    ↓
提交标注（/api/call/summary/save）
```

## 手动外呼流程

```
坐席输入号码 → makeCallFn(phone)
    ↓
OutgoingBar（拨号等待接通）
    ↓
EstablishedEvt → 接通
    ↓
ActiveCallBar + AgentAnnotation
    ↓
挂断 → 提交标注（/api/callRecord/summary）
```

## 子组件职责

| 组件 | 显示条件 | 职责 |
|------|---------|------|
| `IncomingBar` | `callState = RINGING_IN` | 来电接听/拒接 |
| `OutgoingBar` | `callState = DIALING/RINGING_OUT` | 外呼等待中 |
| `ActiveCallBar` | `callState = CONNECTED` | 通话中全套操作 |
| `HoldCallBar` | `callState = HOLD` | 保持中恢复/挂断 |
| `TransferPanel` | 点击咨询/单转按钮 | 输入转接号码 |
| `Dialpad` | 点击 DTMF | 按键发送 |
| `AgentAnnotation` | 通话建立后 | 标注意向/标签/小结 |
| `CallSessionModal` | 来电或通话中 | 统一弹窗容器（支持最小化） |
| `PendingAnnotationDropdown` | 最小化后 | 悬浮气泡，恢复弹窗 |

## 并发通话处理

`callSessions` 数组支持多路并发通话（如咨询时主通话 + 咨询通话同时存在）。`currentCallId` 跟踪当前活跃的通话 ID，事件回调通过 `currentCallIdRef`（Ref 版本）避免闭包问题。

## API 接口

| 时机 | 接口 | 说明 |
|------|------|------|
| 来电振铃 | `POST /api/call/init` | 初始化热转通话记录 |
| 外呼发起 | `POST /api/callRecord/init` | 初始化手动通话记录 |
| 标注提交（热转） | `POST /api/call/summary/save` | 保存意向+标签+小结 |
| 标注提交（手动） | `POST /api/callRecord/summary` | 同上 |
| 配置获取 | `GET /api/config/value` | 意向/标签选项 |

## 相关页面

- projects/xk-ai-talk-desk-ui/xk-ai-talk-desk-ui
- [[projects/xk-ai-talk-desk-ui/concepts/call-center-sdk-integration]]
- [[projects/xk-ai-talk-desk-ui/concepts/agent-state-machine]]
- [[projects/xk-ai-talk-desk-ui/xk-ai-talk-desk-ui]]
