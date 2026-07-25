---
title: JavaScript 事件循环（Event Loop）
category: concepts
tags:
  - javascript
  - browser
summary: JavaScript 单线程执行模型与事件循环机制：调用栈、任务队列、微任务与宏任务的执行顺序；附 Win32 消息循环历史背景与 Java 定时器对比。
sources:
  - https://www.zhoulujun.cn/html/webfront/ECMAScript/js6/2015_1110_345.html
created: 2026-06-29
updated: 2026-07-25
tier: supporting
lifecycle: draft
lifecycle_changed: "2026-07-25"
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

## 历史背景：从 Win32 消息循环说起

Event Loop 并不是 JavaScript 独创——它继承了图形界面系统的"消息驱动"传统。

**DOS 的过程驱动 vs Windows 的事件驱动**：
- DOS 程序顺序执行，有明确的开始/过程/结束，程序直接控制事件顺序
- Windows 是事件驱动：不知道用户先点哪个按钮，所有事件无序到达；程序员只能针对"消息的产生与处理"编写代码

**Windows 消息循环骨架**（几乎所有 Win32 程序都长这样）：

```c
MSG msg;
while (GetMessage(&msg, NULL, 0, 0))
{
    TranslateMessage(&msg);
    DispatchMessage(&msg);
}
```

要点：
- `PostMessage()` 把消息放入队列立即返回；`SendMessage()` 同步等待处理完才返回
- UI 线程就是消息循环所在线程；耗时操作如果也跑在 UI 线程上，消息循环就"卡着"，程序假死
- 解决方式：把耗时操作放到另一个线程，让消息循环继续

> "没有经过 Win32 时代的洗礼，那可能对这个消息循环并不是很清楚。" —— 周陆军

JavaScript 的事件循环，本质上就是浏览器为每个 tab 维护了一个类似的"消息循环"——只不过消息来源是 DOM 事件、定时器、HTTP 请求等。

## 单线程的根本原因

JavaScript 从诞生起就是单线程语言，设计初衷是避免多线程共享资源导致的复杂性（对网页脚本而言过于复杂）。

> Worker API 可以实现多线程，但 JavaScript 本身始终是单线程的。

单线程的问题：一旦遇到耗时任务，网页会"假死"，无法响应用户操作。

**反例对比**：
- **PHP**：单文件单线程，但服务器（Apache/Nginx/PHP-FPM）多线程
- **Python**："多线程"是假的——GIL 让单位时间只有一个线程跑在解释器中，多核只能并发不能并行
- 脚本语言本身效率就不高，设计目的就是应对 I/O 密集、高开发效率——脚本语言基本都是单线程

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
- [[mobile-timer-accuracy]] — mobile-timer-accuracy

## 横向对比：Java 定时器三种实现

Java 有三种定时任务方案，与 JavaScript 的 setTimeout/setInterval 异曲同工：

### 1. 线程 + sleep（最灵活，但需自己管理）

```java
new Thread(() -> {
    while (true) {
        // 业务代码
        Thread.sleep(1000);  // 同步延迟，会阻塞线程
    }
}).start();
```

### 2. Timer.schedule / scheduleAtFixedRate（单线程执行，有缺陷）

```java
Timer timer = new Timer();
timer.scheduleAtFixedRate(task, 5000, 5000);  // delay 5s 后每 5s 执行
```

**缺陷**：Timer 只有一个线程执行所有定时任务。如果某个任务耗时超过两个任务间隔，会发生任务堆积。**和 JavaScript 的 setInterval 累计效应一模一样。**

### 3. ScheduledExecutorService（线程池，最理想）

```java
ScheduledExecutorService service = Executors.newSingleThreadScheduledExecutor();
service.scheduleAtFixedRate(runnable, 10, 5, TimeUnit.SECONDS);
```

优势：
1. **线程池**：相比 Timer 的单线程，不会因一个慢任务阻塞全部
2. **灵活的首次延时**
3. **约定良好的周期设置**

**关键类比**：ScheduledExecutorService ≈ JavaScript 中"用 setTimeout 模拟 setInterval"——都是用递归 + 显式延时来避免累积效应。
