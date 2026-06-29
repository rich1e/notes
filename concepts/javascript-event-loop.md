---
title: JavaScript 事件循环（Event Loop）
category: concepts
tags:
  - javascript
  - event-loop
  - async
  - browser
summary: JavaScript 单线程执行模型与事件循环机制：调用栈、任务队列、微任务与宏任务的执行顺序。
sources:
  - https://www.zhoulujun.cn/html/webfront/ECMAScript/js6/2015_1110_345.html
created: 2026-06-29
updated: 2026-06-29
tier: supporting
lifecycle: draft
lifecycle_changed: "2026-06-29"
base_confidence: 0.67
provenance:
  extracted: 0.75
  inferred: 0.20
  ambiguous: 0.05
relationships:
  - target: "[[concepts/browser-process-model]]"
    type: related_to
  - target: "[[concepts/frontend-storage-cache]]"
    type: related_to
---

# JavaScript 事件循环（Event Loop）

## 单线程的根本原因

JavaScript 从诞生起就是单线程语言，设计初衷是避免多线程共享资源导致的复杂性（对网页脚本而言过于复杂）。

> Worker API 可以实现多线程，但 JavaScript 本身始终是单线程的。

单线程的问题：一旦遇到耗时任务，网页会"假死"，无法响应用户操作。

## 浏览器常驻线程

- **GUI 渲染线程**：渲染页面，与 JS 引擎线程互斥
- **JavaScript 引擎线程**：执行 JS 代码（同一时间只有一个在运行）
- **定时触发器线程**：处理 `setTimeout` / `setInterval`
- **事件触发线程**：控制事件循环，管理待处理队列
- **异步 HTTP 请求线程**：处理 XMLHttpRequest / fetch

**关键**：事件触发线程归属于浏览器，而非 JS 引擎。JS 引擎只负责执行，浏览器另开线程辅助管理事件队列。

## Event Loop 执行模型

```
         ┌─────────────────┐
         │    调用栈         │  ← 同步任务在这里执行
         │  (Call Stack)   │
         └────────┬────────┘
                  │ 空了之后
                  ↓
    ┌─────────────────────────┐
    │   先清空微任务队列        │  ← Promise.then, MutationObserver
    │   (Microtask Queue)    │
    └────────────┬────────────┘
                 │ 清空后
                 ↓
    ┌─────────────────────────┐
    │   取一个宏任务执行         │  ← setTimeout, setInterval, I/O
    │   (Macrotask Queue)    │
    └─────────────────────────┘
         ↑ 循环
```

## 宏任务 vs 微任务

| 类型 | 典型来源 |
|------|---------|
| **宏任务（Macrotask）** | `setTimeout`、`setInterval`、I/O、UI 渲染、`MessageChannel` |
| **微任务（Microtask）** | `Promise.then`、`MutationObserver`、`queueMicrotask`、`async/await` |

**执行顺序**：同步代码 → 清空所有微任务 → 取一个宏任务 → 清空所有微任务 → 下一个宏任务 …

## setTimeout 不准时的原因

`setTimeout` 推入事件队列时，主线程可能仍在忙碌。等主线程空闲时才会从队列取出执行，所以实际延迟 ≥ 指定时间。

## 异步实现的本质

Event Loop 是实现 JavaScript 异步的核心机制：
- 主线程负责运行同步任务
- 事件循环线程负责监视异步任务完成，将回调推入队列
- 主线程空闲时从队列取任务执行

## 相关页面

- [[concepts/browser-process-model]] — 浏览器多进程架构，JS 线程所在的 Renderer 进程
- [[concepts/frontend-storage-cache]] — 浏览器存储与缓存，与异步请求密切相关
