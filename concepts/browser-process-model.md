---
title: 浏览器进程/线程模型
category: concepts
tags:
  - browser
  - performance
summary: Chrome 多进程架构分析：Browser 进程、Renderer 进程、Plugin 进程的职责分工及隔离优势，浏览器组件构成。
sources:
  - https://www.zhoulujun.cn/html/webfront/browser/webkit/2020_0610_8455.html
created: 2026-06-29
updated: 2026-07-25
tier: supporting
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
  - target: "[[concepts/frontend-storage-cache]]"
    type: related_to
---

# 浏览器进程/线程模型

## 浏览器组件

| 组件 | 职责 |
|------|------|
| 界面控件 | 地址栏、前进/后退、书签菜单等非网页区域 |
| 浏览器引擎 | 查询与操作渲染引擎的接口 |
| 渲染引擎 | 解析 HTML/CSS，负责显示请求内容 |
| 网络 | HTTP 请求处理，平台无关接口 |
| UI 后端 | 绘制基础元件（组合框、窗口等） |
| JS 解释器 | 解析执行 JavaScript 代码 |
| 数据存储持久层 | Cookie、Web Database 等持久化存储 |

## Chrome 多进程架构

Chrome 与传统浏览器不同，采用**多进程架构**（而非单进程多线程）：
- **Browser 进程**：唯一，主控整个系统，管理 UI、网络请求、文件访问等
- **Renderer 进程**：可有多个，负责页面渲染和 JavaScript 执行
- **Plugin 进程**：每个插件类型一个
- **GPU 进程**：处理 GPU 任务

进程间通过 **IPC（Inter Process Communication）** 通信。

## Chrome 支持的进程模型

| 模型 | 说明 | 启动方式 |
|------|------|---------|
| **Process-per-site-instance** | 从同一网站链开的页面共用一个进程（默认） | 默认 |
| **Process-per-site** | 同域名页面共用一个进程 | `--process-per-site` |
| **Process-per-tab** | 每个 Tab 一个进程 | `--process-per-tab` |
| **Single Process** | 传统单进程多线程模式 | `--single-process` |

## 多进程的优势

**稳定性**：一个 Renderer 进程崩溃不影响 Browser 进程和其他 Tab。

**安全性**：多进程隔离限制了漏洞的危害范围——Renderer 进程无法获取 Browser 进程的私密信息（如其他域名的密码）。

**内存回收**：进程关闭后，操作系统自动回收该进程的全部内存（利于处理内存泄露问题）。

## Renderer 进程内的线程

每个 Renderer 进程（一个 Tab 页）包含：

- **GUI 渲染线程**：解析 HTML/CSS，构建 DOM/渲染树，与 JS 引擎线程互斥
- **JavaScript 引擎线程**：执行 JS（同一时刻只有一个）
- **定时触发器线程**：管理 `setTimeout` / `setInterval`
- **事件触发线程**：管理事件循环队列
- **异步 HTTP 请求线程**：处理网络请求回调

**GUI 渲染线程与 JS 引擎线程互斥**：JS 执行期间渲染被挂起，这是 JS 阻塞导致页面卡顿的根本原因。

## 导航（Navigation）流程

参考 Zhoulujun 文章的精细化阶段分解：

1. **处理输入** — UI thread 判断输入是搜索关键词还是 URL；若是搜索，跳默认搜索引擎
2. **开始导航** — UI thread 把 URL 交给 network thread，UI thread 显示加载状态
3. **读取响应** — network thread 解析 HTTP 报文，看 MIME 类型；HTML 进入渲染流程，其它走下载管理器；同步做 Safe Browsing + CORB 检查
4. **查找渲染进程** — network thread 通知 UI thread；为优化延迟，浏览器在第二步就开始预查找/启动渲染进程；遇到重定向则重启
5. **提交导航** — Browser 通过 IPC 发送导航确认，Renderer 接收数据后回传 IPC；地址栏小锁、history list 更新
6. **初始化加载完成** — 页面 + 所有 iframe onload 后，Renderer 发 IPC；UI thread 停止 loading 图标

> **注**：Chrome 72 之后 network thread 已被独立为 Network Service Process，通过 `chrome://flags/#network-service-in-process` 可降级回 Browser 进程内的线程模式。

## SharedWorker 进程的特殊性

SharedWorker 不隶属于某个 Render 进程，可被多个 Render 共享。Chrome 为每个相同 JS 的 SharedWorker **单独创建进程**，与 Tab 进程隔离。

Worker vs SharedWorker 通信：

```javascript
// Worker — 一对一
window.worker.port.postMessage('get')

// SharedWorker — 多页共享；通过 port 通信
```

## 相关页面

- [[concepts/javascript-event-loop]] — Renderer 进程内 JS 引擎的执行机制
- [[concepts/frontend-storage-cache]] — 浏览器数据存储层
