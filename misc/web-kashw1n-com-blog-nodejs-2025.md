---
title: "Modern Node.js in 2025 — ESM / Fetch / Built-in Test Runner / Streams / Workers"
category: misc
tags:
  - nodejs
  - esm
  - web-standards
  - runtime
  - misc
sources:
  - "https://kashw1n.com/blog/nodejs-2025/"
source_url: "https://kashw1n.com/blog/nodejs-2025/"
created: "2026-08-13T09:37:00Z"
updated: "2026-08-13T09:37:00Z"
summary: "2025 现代 Node.js 范式综述：ESM + node: 前缀取代 CommonJS、fetch/AbortController 内置替代 axios、node:test 取代 Jest、Streams + Web Streams 互转、Worker Threads 真并行、--watch/--env-file 取代 nodemon/dotenv、permission model、single executable application (SEA)、diagnostics_channel 监控。"
affinity: {}
promotion_status: misc
stub: false
provenance:
  extracted: 0.85
  inferred: 0.12
  ambiguous: 0.03
base_confidence: 0.45
lifecycle: draft
lifecycle_changed: "2026-08-13"
tier: peripheral
---

# Modern Node.js in 2025 — ESM / Fetch / Built-in Test Runner / Streams / Workers

> kashw1n.com 个人博客 2025 长文：Node.js 从 callback-heavy + CommonJS 时代到 clean web-standards 时代的演变，覆盖 10 大现代化主题，每节都给出 old-vs-modern 代码对比。

## Overview

- **根本转变**：从 CommonJS 主导到 ES Modules 为新标准；从外部 HTTP 测试库依赖到 Node.js 自带 fetch + test runner + streams + workers。
- **核心主题**：Node.js 拥抱 web standards、减少外部依赖、提供更直观的开发者体验。
- **代码风格**：每节都给「老方式 vs 新方式」对照，老代码用 `require/module.exports`，新代码用 `import` + `node:` 前缀 + 内置 API。

## 10 大现代化主题

### 1. Module System — ESM 是新标准

**老路 (CommonJS)**：

```js
// math.js
function add(a, b) { return a + b; }
module.exports = { add };

// app.js
const { add } = require('./math');
```

**新路 (ESM + `node:` 前缀)**：

```js
// math.js
export function add(a, b) { return a + b; }

// app.js
import { add } from './math.js';
import { readFile } from 'node:fs/promises';
import { createServer } from 'node:http';
```

**关键点**：
- `node:` 前缀 — 不只是约定，更是**给开发者和工具的清晰信号**：你引入的是 Node.js 内置而非 npm 包，避免包名冲突。
- **Top-level await** — 无需再用 IIFE 包裹整个 app：

```js
// app.js — 干净初始化
import { readFile } from 'node:fs/promises';

const config = JSON.parse(await readFile('config.json', 'utf8'));
const server = createServer(/* ... */);
```

### 2. 内置 Web APIs — 告别 axios / node-fetch

**Fetch API 内置** + `AbortSignal.timeout()` 内置超时：

```js
async function fetchData(url) {
  try {
    const response = await fetch(url, {
      signal: AbortSignal.timeout(5000)
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    if (error.name === 'TimeoutError') throw new Error('Request timed out');
    throw error;
  }
}
```

**AbortController** — 跨 Node.js API 统一的取消机制（fetch、file ops、DB query 都支持）。

### 4. 内置 Test Runner — Jest/Mocha 不再必需

```js
// test/math.test.js
import { test, describe } from 'node:test';
import assert from 'node:assert';

describe('Math functions', () => {
  test('adds numbers correctly', () => {
    assert.strictEqual(add(2, 3), 5);
  });
});
```

```bash
node --test               # run all tests
node --test --watch       # watch mode (development feedback)
node --test --experimental-test-coverage   # coverage (Node.js 20+)
```

### 5. 高级异步模式

- **`Promise.all` 并行 + try/catch 单点错误处理**：
```js
const [config, userData] = await Promise.all([
  readFile('config.json', 'utf8'),
  fetch('/api/user').then(r => r.json())
]);
```
- **AsyncIterators 处理事件流**：
```js
class DataProcessor extends EventEmitter {
  async *processStream() {
    for (let i = 0; i < 10; i++) {
      this.emit('data', `chunk-${i}`);
      yield `processed-${i}`;
      await new Promise(resolve => setTimeout(resolve, 100));
    }
  }
}

const processor = new DataProcessor();
for await (const result of processor.processStream()) {
  console.log('Processed:', result);
}
```

### 6. Streams 现代化 + Web Streams 互转

**`pipeline()` + promises** — 自动清理与错误处理：

```js
import { Readable, Transform } from 'node:stream';
import { pipeline } from 'node:stream/promises';
import { createReadStream, createWriteStream } from 'node:fs';

const upperCaseTransform = new Transform({
  objectMode: true,
  transform(chunk, encoding, callback) {
    this.push(chunk.toString().toUpperCase());
    callback();
  }
});

await pipeline(
  createReadStream(inputFile),
  upperCaseTransform,
  createWriteStream(outputFile)
);
```

**Web Streams 互转** — 与浏览器/边缘运行时兼容：

```js
const webReadable = new ReadableStream({
  start(controller) {
    controller.enqueue('Hello ');
    controller.enqueue('World!');
    controller.close();
  }
});

const nodeStream = Readable.fromWeb(webReadable);
const backToWeb = Readable.toWeb(nodeStream);
```

### 7. Worker Threads — 真并行 for CPU-bound

```js
// worker.js — 隔离计算环境
import { parentPort, workerData } from 'node:worker_threads';

function fibonacci(n) {
  if (n < 2) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
}

parentPort.postMessage(fibonacci(workerData.number));

// main.js — 非阻塞委托
import { Worker } from 'node:worker_threads';
import { fileURLToPath } from 'node:url';

const result = await new Promise((resolve, reject) => {
  const worker = new Worker(
    fileURLToPath(new URL('./worker.js', import.meta.url)),
    { workerData: { number: 40 } }
  );
  worker.on('message', resolve);
  worker.on('error', reject);
});
```

### 8. 开发体验增强

**`--watch` + `--env-file`** — 取代 nodemon + dotenv：

```json
{
  "scripts": {
    "dev": "node --watch --env-file=.env app.js",
    "test": "node --test --watch"
  }
}
```

### 9. Security & Performance 内置

**Permission model** (实验性，最小特权原则)：

```bash
node --experimental-permission --allow-fs-read=./data --allow-fs-write=./logs app.js
node --experimental-permission --allow-net=api.example.com app.js  # ^ 注意：allow-net PR 已合并但尚未发布 ^[ambiguous]
```

**PerformanceObserver 内置 APM**：

```js
import { PerformanceObserver, performance } from 'node:perf_hooks';

const obs = new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    if (entry.duration > 100) console.log(`Slow: ${entry.name} ${entry.duration}ms`);
  }
});
obs.observe({ entryTypes: ['function', 'http', 'dns'] });
```

### 10. 应用分发 — Single Executable Application (SEA)

```bash
node --experimental-sea-config sea-config.json
```

```json
{
  "main": "app.js",
  "output": "my-app-bundle.blob",
  "disableExperimentalSEAWarning": true
}
```

→ 适合 CLI 工具 / 桌面应用 / 不想让用户装 Node.js 的场景。

### 11. 现代错误处理与诊断

**结构化 AppError 类** + `diagnostics_channel`：

```js
class AppError extends Error {
  constructor(message, code, statusCode = 500, context = {}) {
    super(message);
    this.name = 'AppError';
    this.code = code;
    this.statusCode = statusCode;
    this.context = context;
    this.timestamp = new Date().toISOString();
  }
}

import diagnostics_channel from 'node:diagnostics_channel';
const dbChannel = diagnostics_channel.channel('app:database');
dbChannel.subscribe((message) => {
  console.log('DB op:', message.operation, message.duration);
});
```

## Concepts

> vault 暂无现代 Node.js 主题的 concept 页（vault 强项是 AI agent + 软件工程）。本节列出本文可蒸馏的概念，留待未来有兴趣时建。

- **[[concepts/esm-vs-cjs-migration]]** (建议) — CommonJS → ESM 迁移路径 + `node:` 前缀语义 + top-level await 的运行时成本 (^[inferred] module top-level await 延迟模块加载图)
- **[[concepts/node-built-in-web-apis]]** (建议) — Node.js 把 Fetch / AbortController / ReadableStream / FormData / crypto 等 web API 拉进 runtime 的统一策略，与浏览器/边缘运行时打通
- **[[concepts/node-built-in-test-runner]]** (建议) — `node:test` 与 Jest/Vitest 的功能对比、watch mode、--experimental-test-coverage 限制
- **[[concepts/node-web-streams-interop]]** (建议) — Node.js Streams 与 Web Streams 的双向互转 `Readable.fromWeb` / `Readable.toWeb` 的应用场景（边缘运行时同构代码）
- **[[concepts/worker-threads-vs-cluster]]** (建议) — Worker Threads 与 Cluster 的取舍：CPU-bound vs 多进程隔离
- **[[concepts/single-executable-application]]** (建议) — Node.js SEA 原理 + 限制（动态 require 不支持）+ 与 Bun/Bun:Bundler 的对比
- **[[concepts/permission-model-runtime]]** (建议) — Node.js `--experimental-permission` 的设计哲学（最小特权）vs 浏览器 web permissions API 的对比

## Entities

> vault 无相关 entity；本节列建议 future entities。

- **[[entities/nodejs]]** (建议) — Node.js runtime 主体。
- **[[entities/jacob-bd]]** (vault 已有) — 与本文无关，但展示了「个人 vibe coder 写小工具」的同类作者范式。
- **[[entities/node-tc-39]]** (建议) — TC39 与 Node.js evolution（CommonJS 退出策略 / `node:` 前缀的 RFC 来源）。

## Open Questions

1. **`--experimental-permission --allow-net` 何时正式 GA？** 文章提到 PR 已合并但尚未发布 ^[ambiguous] — 当前 production 是否可用？
2. **SEA 是否会原生支持 native modules (e.g. `better-sqlite3`)**？— 当前 SEA 不支持动态 require，社区方案是把 native module 作为外部文件。
3. **Top-level await 在循环依赖 / 大型模块图中的性能影响？** — 模块加载图会变 DAG，await 节点会推迟整个图。
4. **`node:test` vs Vitest 在大型 monorepo 中的实测对比？** — 文章没给数据。
5. **Web Streams 与 Node.js Streams 的 API 心智模型差异？** — Web Streams 用 pull-based backpressure，Node Streams 同时支持 push + pull。
7. **Worker Threads 是否适合 I/O-bound 任务？** — 文章只演示 CPU-bound (Fibonacci)；I/O-bound 用 worker 反而增加开销 ^[inferred]。

## Related

- (暂无直接相关 — vault 暂无现代 Node.js / JavaScript runtime 主题的页面)
- [[misc/web-xda-developers-com-the-last-generation-of-fully-upgradeable-pcs]] — 同样是 2025/2026 趋势评论 (PC 硬件)

---

## Provenance

- **extracted**: 0.85 — 大量代码示例和 API 描述是文章直接陈述（ESM 语法、fetch 调用、`node --test`、`pipeline()` 用法）
- **inferred**: 0.12 — Open Questions #3/#5/#7 是文中未说但合逻辑的推论（top-level await 性能影响、Worker vs I/O、心智模型差异）
- **ambiguous**: 0.03 — allow-net 何时 GA 是文中明确未定的状态
- **base_confidence**: 0.45 — 个人博客（kashw1n.com 是个人站点）+ 单一来源；技术内容本身可由 Node.js 官方文档交叉验证 ^[inferred] 但本帖未引用官方

---

> **Source**: https://kashw1n.com/blog/nodejs-2025/
> **Ingested at**: 2026-08-13T09:37:00Z
> **Mode**: misc（vault 即 obsidian-wiki repo, no project context）
> **Affinity**: {}（无已索引项目连接 — 等待未来 cross-linker 评估）