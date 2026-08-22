---
title: Figwright 项目
category: project
tags: [figma, mcp, codegen, design-tools, figwright]
sources:
  - https://github.com/awdr74100/figwright
created: 2026-08-14T08:00:00Z
updated: 2026-08-14T08:00:00Z
base_confidence: 0.5
lifecycle: draft
lifecycle_changed: "2026-08-14"
summary: 双向 Figma MCP server(awdr74100, MIT, pnpm monorepo + 3 packages + 2 skills):provider-first codegen + 本地 WebSocket 中继 + 免 Dev Mode 付费座位
---

# Figwright 项目

**Figwright** = `Where Playwright drives the browser, Figwright drives Figma.`

双向 Figma MCP server —— 让 AI agent(Claude Code/Cursor/Codex/任何 MCP client)直接读写 Figma 画布,而非只读。

## 项目元信息

- **仓库**:`https://github.com/awdr74100/figwright`
- **作者**:Roya(@awdr74100)
- **License**:MIT
- **运行时**:Node.js >= 24.0.0(package.json `engines`,与 README "20.19+/22.12+" 矛盾 ^[ambiguous])
- **包管理**:pnpm@11.21.0,Corepack 锁定
- **commit SHA**: `4eb134065cc63e9851bf5c4058b5facda8851646`(gitingest 抓取时)
- **发布的包**:`@figwright/mcp`(MCP server, npx 启动)

## 三仓架构(pnpm workspace)

```
figwright/
├── packages/
│   ├── mcp/        ← @figwright/mcp(Node MCP server,本地 stdio 启动)
│   │   ├── src/election/        ← leader/follower 选举
│   │   ├── src/relay/           ← WebSocket relay
│   │   ├── src/tokens/          ← 设计 token 索引与扫描
│   │   ├── src/join/            ← Figma→code 映射(component/token/icon)
│   │   ├── src/scan/            ← 代码仓库扫描
│   │   ├── src/tools/           ← 112 个 MCP tool 实现
│   │   └── src/prompts/         ← prompt templates
│   ├── plugin/     ← Figma 端插件(Vue 3 iframe + sandbox)
│   │   ├── src/handlers/        ← Figma Plugin API 调用 handlers
│   │   ├── src/relay/           ← WebSocket client
│   │   ├── protocol/            ← 协议桥
│   │   └── ui/                  ← Vue 3 面板 UI
│   └── shared/     ← 跨仓协议(codec/envelope/heartbeat/rpc/protocol/...)
├── skills/
│   ├── figma-codegen/SKILL.md   ← Figma → code(读方向)
│   └── figma-build/SKILL.md     ← code/spec → Figma(写方向)
└── scripts/
    ├── release.mjs              ← 自定义 changelogen release 脚本
    └── sync-skills.mjs          ← 同步 skills/ ↔ .claude/skills/ 的 postinstall
```

## 核心设计哲学

1. **Provider-first codegen** —— 不发固定模板;先 `analyze_project` 探测代码库真实栈(框架 + 样式系统 + 现有组件/token/icon),再让模型生成与现有 codebase 风格一致的代码
2. **Local-only relay** —— MCP client ↔ `@figwright/mcp`(stdio)↔ WebSocket(`127.0.0.1:3055`)↔ Figma plugin(sandbox);**所有流量 loopback**,无云依赖
3. **Leader/follower 选举** —— 多 client 共享一个 plugin,自动选 leader 拥有连接;follower 通过 HTTP /rpc 转发;leader 退出自动接管
4. **112 tool 三分类** —— Read(选择/样式/变量/组件/Motion/截图)+ Write(frame/text/auto-layout/styles/variables/components/Motion + batch)+ Grounding(`get_design_context`、`component_map`、`token_map`、`icon_map`、`design_diff`)
5. **心跳 + 幂等 + session resume** —— "busy ≠ dead" heartbeat,断线后续上而非重连失败

## 与 vault 已有知识的连接

- **vs Google Stitch** [[entities/google-stitch]]:Stitch 是 AI 生成设计(design 产出);Figwright 是 design ↔ code 双向;两者可串联("用 Stitch 出设计 → 用 Figwright 落代码"或反向)
- **vs 设计系统 MD 类** [[concepts/design-system-as-ai-context]]:DESIGN.md 是给 agent 的硬约束输入文本;Figwright 是给 agent 的活体 Figma API 桥
- **vs Figma 官方 Dev Mode MCP**:官方只读 + 付费;Figwright 双向 + 零成本
- **MCP 多客户端范式** 与 vault [[concepts/mcp-multi-tool-installer]] 同源 —— "检测而非创建 + 进程运行拒写" 的 `nlm setup add` 模式可对标 `npx skills add`

## vault 内部页面索引

- 项目子页:
  - [[projects/figwright/concepts/provider-first-codegen]] —— 探测+复用哲学
  - [[projects/figwright/concepts/mcp-local-relay-architecture]] —— stdio + WebSocket + leader/follower
  - [[projects/figwright/concepts/loopback-security-host-origin-headers]] —— DNS rebinding + CORS 三件套
  - [[projects/figwright/concepts/design-context-grounding]] —— `get_design_context` 抽象
  - [[projects/figwright/skills/figma-codegen-workflow]] —— figma-codegen 5 步工作流
  - [[projects/figwright/skills/figma-build-workflow]] —— figma-build 反向工作流
  - [[projects/figwright/references/figwright-tool-taxonomy]] —— 112 tool 三分类
  - [[projects/figwright/references/figwright-shared-protocol]] —— shared package 7 文件职责

## 快速上手(来自 README)

```json
// .mcp.json
{
  "mcpServers": {
    "figwright": {
      "command": "npx",
      "args": ["-y", "@figwright/mcp@latest"]
    }
  }
}
```

```
1. 在 Figma desktop: Menu → Plugins → Development → Import plugin from manifest
2. 选从 GitHub latest release 下载的 figwright-plugin.zip 解压后的 manifest.json
3. 在 Figma 打开 plugin(Plugins → Development → Figwright),自动连本地 server
4. 用 agent 跑 ping 确认链接
5. (可选)npx skills add awdr74100/figwright/skills 装 2 个 skill
```

## Open Questions

- **engines 矛盾**: README "Node 20.19+ or 22.12+" vs `package.json` `engines.node: ">=24.0.0"` —— 谁为准?(实际 `@figwright/mcp` 包的 engines 字段待查,根 workspace 的 engines 不一定代表运行时)
- **provider-first 落地完整性**:`analyze_project` 工具是否覆盖所有现代栈(Vue 3 / Svelte 5 / Astro / Remix / TanStack Start)或仍有边缘场景
- **`design_diff` baseline 存储**:JSON 文件?SQLite?是否进 git 仓?跨 commit 怎么比?
- **leader 选举算法**:`packages/mcp/src/election/election.ts` 实现细节(基于 lease?基于 heartbeat?基于 "most recently active file"?README 提到)
- **plugin 的 Vue 3 iframe 在 Figma sandbox 限制下能用的库** —— Figma plugin runtime 不是完整浏览器,Vue 3 / Composition API / Pinia 哪些能跑
- **安全性**:`Host`/`Origin` 头校验具体在 WebSocket 升级时还是 HTTP /rpc 时执行