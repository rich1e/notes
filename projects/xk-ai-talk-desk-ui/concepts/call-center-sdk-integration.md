---
title: >-
  CC SDK 集成：useSoftbar Hook
category: concepts
tags: [react, webrtc, call-center]
sources: [projects/xk-ai-talk-desk-ui]
summary: >-
  useSoftbar 封装信科 LaihuAPI，通过事件驱动模式管理通话生命周期，CC 与 WebRTC 双通道签入。
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

# CC SDK 集成：useSoftbar Hook

`useSoftbar`（`src/sdk/hooks/useSoftbar.ts`）是整个电话功能的核心 Hook，封装了信科 LaihuAPI，将通话事件转译为 React 状态。

## 架构决策

**为什么用一个大 Hook 而不是多个小 Hook？**
LaihuAPI 的所有操作依赖同一个 `laihuObj` 实例（Ref 持有），事件监听只能初始化一次（`initCalledRef` guard），拆小 Hook 会导致 Ref 传递复杂性剧增。大 Hook 通过 `useCallback` 防止不必要重渲染，权衡是合理的。^[inferred]

## 核心对象

```
LaihuAPI
├── session
│   ├── station   ← 坐席/通话状态（calls, agent）
│   ├── event     ← 事件总线（EventEmitter 风格）
│   └── reasons   ← 坐席状态原因列表
└── laihuUA       ← JsSIP WebRTC UA
```

初始化在 `useEffect(() => {...}, [])` 中执行，`initCalledRef` 保证只初始化一次（严格模式 double-invoke 安全）。

## 双通道签入

| 模式 | `data.type` | 特性 |
|------|-------------|------|
| 仅 CC | `cc` | 无 WebRTC，不需要麦克风权限 |
| CC + WebRTC | `ccandwebrtc` | JsSIP UA 接管音频，需 ICE Server、WebRTC Server |

WebRTC 模式下，来电振铃通过 JsSIP `incomingCall` 回调处理；CC 模式通过 `DeliveredEvt` 事件处理。两路信令最终汇聚到同一套 `callState` 状态。^[inferred]

## 关键事件 → 状态映射

| SDK 事件 | 触发时机 | 状态变化 |
|---------|---------|---------|
| `DeliveredEvt` | 来电振铃 | `callState = RINGING_IN`，解析 `dialogue` 字段为 AI 对话 |
| `OriginatedEvt` | 外呼发起 | `callState = DIALING`，调用 `initCallRecord` 创建记录 |
| `EstablishedEvt` | 通话接通 | `callState = CONNECTED` |
| `HeldEvt` | 保持中 | `callState = HOLD` |
| `RetrievedEvt` | 恢复通话 | `callState = CONNECTED` 或 `CONFERENCE` |
| `ConnectionClearedEvt` | 挂断 | `callState = HANGUP → AFTER_CALL` |
| `TransferredEvt` | 转接完成 | `callState = TRANSFERRED` 或 `CONNECTED` |
| `AgentReadyEvt` | 就绪 | `agentState = READY` |
| `AgentLoggedOffEvt` | 签出 | 清空所有状态 |

## AI 对话记录解析

`DeliveredEvt` 的 `dialogue` 字段（JSON 字符串）包含 AI 与客户的对话历史：

```ts
// e.dialogue: '[{"side": "AI", "content": "..."}, ...]'
messages = raw.map(item => ({
  role: item.side === 'AI' ? 'ai' : 'customer',
  content: item.content,
  time: timestamp,
}));
```

解析后存入对应 `CallSession.aiConversation`，供 `CallSessionModal` 渲染对话气泡。

## 外呼号码前缀规则

```ts
const withPrefix = phone.startsWith('9') ? phone : `9${phone}`;
```

外呼时自动添加 `9` 前缀（非 `9` 开头的号码），这是信科 CC 系统的外线拨出约定。^[extracted]

## 通话会话管理

`callSessions: CallSession[]` 数组跟踪并发通话：
- `addCallSession` — 新增（inbound/outbound）
- `updateCallSessionState` — 更新状态（incoming/active/hold/hungup）
- `updateCallSessionDuration` — 计算持续时长（从 `callStartTimeRef` 算差值）
- `removeCallSession` — 清除（CallSessionModal 关闭时）

## 相关页面

- projects/xk-ai-talk-desk-ui/xk-ai-talk-desk-ui
- [[projects/xk-ai-talk-desk-ui/concepts/agent-state-machine]]
- [[projects/xk-ai-talk-desk-ui/skills/phonebar-call-flow]]
- [[projects/xk-ai-talk-desk-ui/xk-ai-talk-desk-ui]]
