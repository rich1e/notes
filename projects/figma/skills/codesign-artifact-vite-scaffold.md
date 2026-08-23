---
title: CoDesign artifact.jsx 在 Vite 上加载的脚手架
category: skills
tags: [codesign, vite, react, scaffolding, debugging]
sources:
  - store/project for X/figma session (2026-08-23)
created: 2026-08-23T16:15:00Z
updated: 2026-08-23T16:15:00Z
base_confidence: 0.85
lifecycle: draft
lifecycle_changed: "2026-08-23"
summary: CoDesign artifact.jsx 用全局 React/ReactDOM + 末尾自挂载,在 Vite 上需要去掉尾部 ReactDOM.createRoot + 加 export default,再用 main.jsx 包一层 createRoot
---

# CoDesign artifact.jsx 在 Vite 上的本地加载

## 适用场景

要把 CoDesign 客户端里的 React artifact(`App.jsx`,依赖全局 React/ReactDOM + 末尾自挂载)在本地用浏览器调试。Vite 5 + React 18 是最小依赖。

## 关键发现

### 两处必改

1. **删除 artifact 末尾的** `ReactDOM.createRoot(document.getElementById("root")).render(<App />)`
2. **替换为** `export default App;`

否则会发生 Vite 改造最易踩的坑 — 重复 createRoot:artifact 自带 + main.jsx 又一个,React 抛出 "root already exists" 触发静默失败(`root.innerHTML` 始终是空字符串)。

### 最小 Vite 脚手架

放在 `/tmp/figma-scaffold/`(或其他任意临时目录):

```bash
npm init -y
npm install react@18 react-dom@18
npm install -D vite@5 @vitejs/plugin-react@4
```

```
figma-scaffold/
├── package.json
├── vite.config.js       — defineConfig({ plugins: [react()] })
├── index.html            — <div id="root"></div> + <script src="/src/main.jsx">
└── src/
    ├── main.jsx          — createRoot().render(<App />)
    └── App.jsx           — 复制的 artifact (去掉尾巴 + export default)
```

**src/main.jsx**:

```jsx
import React from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.jsx'

createRoot(document.getElementById('root')).render(<App />)
```

**启动命令**:

```bash
./node_modules/.bin/vite --port 5173 --host 127.0.0.1 --strictPort
```

## 关键陷阱

### 1. 文件副本必须 cp 同步(不是 symlink)

Vite 加载的是 `/tmp/figma-scaffold/src/App.jsx`,**不**是磁盘 `/Users/rich1e/store/project for X/figma/App.jsx`。两处必须 `cp` 同步,否则编辑原项目源码看不到效果 — 这是排查屏8 看似"没渲染"时的核心 root cause。

```bash
cp /Users/rich1e/store/project for X/figma/App.jsx /tmp/figma-scaffold/src/App.jsx
```

### 2. React 静默吞掉错误

屏8 这种 75 个 SVG + 多内联样式的页面,渲染失败时 React error boundary 会吞错。Console 里看到的不是 `Error`,而是页面空白。要在浏览器里挂:

```js
window.addEventListener('error', (e) => {
  console.log('Caught:', e.message, e.filename, e.lineno);
});
window.addEventListener('unhandledrejection', (e) => {
  console.log('Rejection:', e.reason);
});
const origErr = console.error;
console.error = function(...args) {
  console.log('consoleError:', ...args);
  origErr.apply(console, args);
};
```

### 3. Chrome 截图工具在长页面靠后位置返回黑屏

Vite 页面动辄 15000+ px 高,Chrome screenshot 在滚动到下方 viewport 时可能返回空 PNG(工具自身的 race condition),但 DOM 实际正常。验证手段:

```js
document.elementFromPoint(600, 400)
// 应该返回屏 8 的 grid 容器 + 文字内容
document.body.scrollHeight
// 应该 ~18000
```

### 4. ESM 模式 + ES2020 保留字

JSX 中的 `width` / `height` 不能直接展开:`{ ... props.width, props.height }` 会触发 "Unexpected token"。用 `const width = props.width;` 解构后引用。

## 验证启动成功

```js
// 浏览器 console
document.getElementById('root').innerHTML.length > 0
// 应返回 true

document.querySelectorAll('*').length
// 七屏应 ~3172;八屏应 ~3900

document.body.innerText.includes('Eight screens')
// 八屏应 true
```

## 反向改造

如果要让 Vite 跑的 React 代码"喂"回 CoDesign 客户端,反向操作:
- 删 `export default App`
- 顶部加 `import React from 'react'` + `import ReactDOM from 'react-dom/client'`
- 末尾加回 `ReactDOM.createRoot(document.getElementById("root")).render(<App />)`

## Related

- [[projects/figma/figma]] — 项目概览
- [[projects/figma/skills/codesign-session-jsonl-recovery]] — 先恢复源码,再用本脚手架
- [[projects/figma/concepts/screen-08-photo-wall]] — 在 Vite 上验证屏8