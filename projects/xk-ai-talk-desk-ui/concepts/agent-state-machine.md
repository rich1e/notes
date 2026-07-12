---

title: >-
  坐席状态机设计
category: concepts
tags: [call-center, state-management, zustand, react]
sources: [projects/xk-ai-talk-desk-ui]
summary: >-
  坐席状态分两层：agentState（业务层）与 callState（通话层），分别由 SDK 事件驱动，通话结束自动回归。
provenance:
  extracted: 0.65
  inferred: 0.3
  ambiguous: 0.05
base_confidence: 0.65
lifecycle: draft
lifecycle_changed: 2026-06-29
created: 2026-06-29
updated: 2026-06-29
relationships:
  - target: "[[projects/jrfed-zaxd-mediation-tool/jrfed-zaxd-mediation-tool]]"
    type: related_to
  - target: "[[projects/xk-ai-talk-desk-ui/xk-ai-talk-desk-ui]]"
    type: related_to
  - target: "[[entities/zustand]]"
    type: related_to
---

# 坐席状态机设计

xk-ai-talk-desk-ui 中坐席状态分两个正交维度，由 `useSoftbar` Hook 维护。

## 坐席业务状态（agentState）

```
LOGGED_OUT ──登录──→ READY ⇄ NOT_READY
                      ↓
               AFTER_CALL_WORK
```

| 状态 | 枚举值 | 触发事件 |
|------|--------|---------|
| 已登出 | `LOGGED_OUT` | `AgentLoggedOffEvt` |
| 就绪 | `READY` | `AgentReadyEvt` |
| 非就绪（小憩等） | `NOT_READY` | `AgentNotReadyEvt` + reason code |
| 话后处理 | `AFTER_CALL_WORK` | `AgentWorkingAfterCallEvt` |

reason code 持久化到 `sessionStorage(softbar_agent_state)`，断线重连后恢复签入时自动还原坐席状态。

## 通话状态（callState）

```
IDLE → DIALING → RINGING_OUT → CONNECTED → HANGUP → AFTER_CALL
           ↑
      RINGING_IN
           ↓
       CONNECTED ⇄ HOLD ⇄ CONFERENCE
           ↓
       TRANSFERRED
```

通话状态完全由 SDK 事件驱动，不允许 UI 直接修改（单向数据流）。^[inferred]

## AutoIn 模式

当 `H5Client.settings.workMode === 'AutoIn'` 时：
1. 签入后自动切换到就绪（`setAgentStateFn(0)`）
2. 来电自动接听（`answerFn()`，无需手动点击）

这是预测式外呼场景的特殊模式，普通热转场景不启用。^[inferred]

## 状态持久化策略

| 数据 | 存储 | 原因 |
|------|------|------|
| token + user | localStorage（[[entities/zustand|Zustand]] persist） | 跨 tab、跨刷新 |
| agentStateCode | sessionStorage | 断线重连恢复，tab 关闭清除 |
| businessCode | sessionStorage | 同上 |

## 防刷新保护

签入后注册 `beforeunload` 事件，提示用户刷新将导致签出，避免意外丢失通话。^[extracted]

## 相关页面

- [[xk-ai-talk-desk-ui/concepts/call-center-sdk-integration]]
- [[xk-ai-talk-desk-ui/skills/phonebar-call-flow]]

## Related

- [[projects/xk-ai-talk-desk-ui/xk-ai-talk-desk-ui]] — >-

- [[projects/jrfed-zaxd-mediation-tool/jrfed-zaxd-mediation-tool]] — >-
