---
title: CoDesign artifact.jsx 在 Vite 上加载的脚手架
slug: codesign-artifact-vite-scaffold
created: 2026-08-23
tags: [codesign, vite, react, scaffolding]
sources:
  - "figma project session (2026-08-23)"
summary: >-
  CoDesign 的 artifact.jsx 用全局 React/ReactDOM + 末尾自挂载,在 Vite 上需要
  去掉尾部 ReactDOM.createRoot + 加 export default,再用 main.jsx 包一层。
project: store/project for X/figma
base_confidence: 0.85
provenance:
  extracted: 0.8
  inferred: 0.2
  ambiguous: 0.0
lifecycle_changed: 2026-08-23
---

# CoDesign artifact.jsx 在 Vite 上的本地加载

## Context

CoDesign 客户端在自己的 plugin host 里跑 `App.jsx`,依赖全局 React + 末尾自带的 `ReactDOM.createRoot(...).render(<App />)`。要在本地用 Vite 调试这份 artifact,需要把它改造成标准 ES Module。

## Finding

### 改造点(只需两处)

1. **删除末尾的 `ReactDOM.createRoot(document.getElementById("root")).render(<App />)`**,替换为 `export default App;`。
2. **新建 `src/main.jsx`** 用 Vite 入口模式挂载:
   ```jsx
   import React from 'react'
   import { createRoot } from 'react-dom/client'
   import App from './App.jsx'
   createRoot(document.getElementById('root')).render(<App />)
   ```

### 最小 Vite 脚手架(`/tmp/figma-scaffold/`)

```
package.json   — react@18 + react-dom@18 + vite@5 + @vitejs/plugin-react
vite.config.js — defineConfig({ plugins: [react()] })
index.html     — <div id="root"></div> + /src/main.jsx
src/main.jsx   — createRoot().render(<App/>)
src/App.jsx    — 复制的 artifact,去掉尾巴 + export default
```

### 关键陷阱

- **重复 createRoot**:artifact 自带的 createRoot + main.jsx 的 createRoot 会让 React 抛出"root already exists",触发静默失败(root.innerHTML 始终是空)。这是 Vite 改造最容易踩的坑。
- **HMR 与文件缓存**:Vite 加载的是 `/tmp/figma-scaffold/src/App.jsx`,**不**是磁盘 `/Users/rich1e/store/project for X/figma/App.jsx`。两处必须 `cp` 同步,否则编辑源码看不到效果。

## Implications

- 任何 CoDesign artifact 都可以用这套脚手架(<20 行配置 + 5 个文件)本地启起来。
- 反过来,如果要让 Vite 跑的 React 代码"喂"给 CoDesign 客户端,需要做反向改造:把 `export default App` 删掉、显式 import React/ReactDOM、加回末尾 createRoot。
- Vite 自身不带 React Refresh 错误栈,屏8 那种 75 个 SVG + 多内联样式的页面渲染失败时,error 会被 React error boundary 吞掉,需要在浏览器里挂 `window.onerror` + `window.addEventListener('unhandledrejection')` 才能捕获到。

## Related

- [[codesign-session-jsonl-recovery]] — 当 artifact 被破坏时,先恢复源码,再用本脚手架启动