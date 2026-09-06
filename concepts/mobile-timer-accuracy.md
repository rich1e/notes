---
title: 移动端定时器精度问题
category: concepts
tags:
  - ios
  - javascript
  - browser
  - debugging
summary: 移动端 setInterval/setTimeout 因锁屏、APP 后台、页面卡顿导致计时不准的根因与解决方案（visibilitychange + Web Worker）。
sources:
  - https://www.zhoulujun.cn/html/webfront/SGML/html5/2017_0927_8053.html
  - https://hcysun.me/2016/07/11/js-Worker-API-在倒计时中的使用/
created: 2026-06-29
updated: 2026-07-25
tier: peripheral
lifecycle: draft
lifecycle_changed: "2026-06-29"
base_confidence: 0.67
provenance:
  extracted: 0.80
  inferred: 0.15
  ambiguous: 0.05
relationships:
  - target: "[[concepts/javascript-event-loop]]"
    type: related_to
  - target: "[[concepts/browser-process-model]]"
    type: related_to
  - target: "[[references/open-codesign-prompt-system-deepwiki]]"
    type: related_to
  - target: "[[projects/figma/figma]]"
    type: related_to
  - target: "[[projects/figma/concepts/screen-08-photo-wall]]"
    type: related_to
---

# 移动端定时器精度问题

## 根因

### 1. 页面不可见时定时器被节流/冻结

浏览器对非激活页面有意节流：
- **PC 浏览器**（Firefox/Chrome/Safari）：未激活页面的定时器间隔最小值强制提升至 1 秒以上
- **移动浏览器**：内存/CPU 更宝贵，往往直接**冻结**所有未激活页面的定时器

触发场景：锁屏、Home 键切换应用、APP 进入后台。

### 2. 页面卡顿导致定时器延迟

JavaScript 单线程执行——当主线程忙于处理其他任务（长列表渲染、复杂计算、频繁 DOM 操作），`setInterval` 回调只能等主线程空闲后才能执行，实际触发时间远超设定间隔。

参见 [[concepts/javascript-event-loop]] 中的宏任务排队机制。

## 解决方案

### 方案一：visibilitychange 事件修正（适合 H5/Web）

```javascript
let startTime = Date.now()
let remaining = totalSeconds

document.addEventListener('visibilitychange', () => {
  if (document.visibilityState === 'visible') {
    // 页面回到前台时，用服务器时间或实际经过时间修正
    const elapsed = Math.floor((Date.now() - startTime) / 1000)
    remaining = Math.max(0, totalSeconds - elapsed)
    updateDisplay(remaining)
  }
})
```

**注意**：PC 端有效；移动 APP 内嵌 WebView 需要原生层监听 WebView 激活状态并通知前端（前端调用 SDK 接口）。

### 方案二：Web Worker 隔离定时器

Web Worker 运行在独立线程，不受主线程卡顿影响：

```javascript
// worker.js
let timer = null
self.onmessage = (e) => {
  if (e.data.type === 'start') {
    let count = e.data.seconds
    timer = setInterval(() => {
      count--
      self.postMessage({ count })
      if (count <= 0) clearInterval(timer)
    }, 1000)
  }
  if (e.data.type === 'stop') clearInterval(timer)
}

// main.js
const worker = new Worker('worker.js')
worker.postMessage({ type: 'start', seconds: 60 })
worker.onmessage = (e) => updateDisplay(e.data.count)
```

> 列表页倒计时的 Worker 使用警告（来自 [hcysun.me 原文](https://hcysun.me/2016/07/11/js-Worker-API-在倒计时中的使用/)）：不要循环 `new Worker()` 多个实例——可能导致应用卡死，Hybrid App H5 页面尤其容易闪退。**只 `new` 一个 Worker**，所有列表项的倒计时共享 worker，回调里靠循环更新视图。另外部分 Android 机型的 webview 不支持 Worker，需做能力探测后退回 `setInterval`。

### 方案三：基于服务器时间的差值计算（最可靠）

不依赖定时器计数，每次刷新时用服务器时间重新计算剩余秒数：

```javascript
const serverEndTime = serverTimestamp + durationSeconds * 1000

function tick() {
  const remaining = Math.max(0, Math.floor((serverEndTime - Date.now()) / 1000))
  updateDisplay(remaining)
  if (remaining > 0) setTimeout(tick, 1000)
}
tick()
```

结合 `visibilitychange` 在页面回到前台时立即调用 `tick()` 修正显示。

## 最佳实践

| 场景 | 推荐方案 |
|------|---------|
| 纯 Web H5 倒计时 | 方案三（服务器时间差值） + visibilitychange |
| APP 内嵌 WebView | 方案三 + 原生层通知前端激活状态 |
| 高精度需求（秒杀、竞拍） | 服务器时间 + 100ms 间隔轮询修正 |
| 页面卡顿场景 | Web Worker 隔离计时 |

## 相关页面

- [[concepts/javascript-event-loop]] — 定时器作为宏任务的排队机制
- [[concepts/browser-process-model]] — 渲染线程与 JS 引擎线程互斥关系

## Related
- [[synthesis/ptp-ieee1588]]
- [[projects/figma/concepts/screen-08-photo-wall]]
- [[projects/figma/figma]]

- [[references/open-codesign-prompt-system-deepwiki]]
