---
title: "DeepSeek Harness (dsh) — Plugin-Based Agent Harness"
category: entities
tags:
  - deepseek
  - agent-harness
  - typescript
  - cordis
  - monorepo
  - entity
summary: "DeepSeek-AI 开源 agent harness（命令行工具 dsh），MIT 许可，基于 vendored Cordis 框架的「everything is a plugin」架构，TypeScript + pnpm monorepo，24 个 package group + CLI / Web / JSON-RPC / ACP 入口，仍在 developer preview 阶段。"
sources:
  - "https://github.com/deepseek-ai/deepseek-harness"
  - "https://github.com/deepseek-ai/deepseek-harness/blob/main/AGENTS.md"
source_url: "https://github.com/deepseek-ai/deepseek-harness"
created: "2026-08-14T01:28:00Z"
updated: "2026-08-14T01:28:00Z"
provenance:
  extracted: 0.88
  inferred: 0.10
  ambiguous: 0.02
base_confidence: 0.78
lifecycle: draft
lifecycle_changed: "2026-08-14"
tier: supporting
relationships:
  - target: "[[entities/cordis]]"
    type: uses
  - target: "[[concepts/cordis-plugin-framework]]"
    type: related_to
---

# DeepSeek Harness (dsh) — Plugin-Based Agent Harness

> DeepSeek-AI 开源的 **agent harness**（命令行 `dsh`），MIT 许可，基于 vendored [Cordis](https://github.com/cordiverse/cordis) 框架。「everything is a plugin」架构 — 模型适配、工具注册、session log、agent 循环本身**全部是可替换的 plugin**。

## 关键事实

| 维度 | 值 |
|---|---|
| **版本** | developer preview（README 明示：「THERE WILL BE COMPATIBILITY-BREAKING CHANGES」）|
| **许可** | MIT + THIRD_PARTY_NOTICES.md 披露 |
| **运行时** | Node.js ^22.19 \|\| >=24 |
| **包管理** | pnpm workspaces |
| **语言** | TypeScript（strict + noImplicitAny），ESM everywhere |
| **代码规模** | 41 个顶层目录 + 24 个 package group，4764 git-tracked 文件 |
| **vendor/** | 内嵌 Cordis 源码（manifest + sync 流程）|
| **入口** | `dsh` CLI: `web` / `headless` / `acp` / `jsonrpc` 等多个 profile |

## 运行方式

```sh
# npm
npx @deepseek-ai/dsh web    # Web UI @ http://127.0.0.1:3080

# 从源码
git clone https://github.com/deepseek-ai/deepseek-harness.git
cd deepseek-harness
pnpm install
pnpm run build
pnpm dsh web
```

## Package Groups（24 个）

来自 AGENTS.md 的权威分类：

| Group | 角色 |
|---|---|
| `core/` | product API spine: session, system-prompt, tools, agent, agent-loop |
| `api/` | Remote BFF assembly + Typert RPC gateway |
| `typert/` | type graph generator + loader + runtime registry |
| `llm/` | LLM capability: Service Definition/Consumer + DeepSeek providers |
| `e2b/` | E2B POC: sandbox + FS/subprocess adapters |
| `shell/` | bash capability: Service Definition + local/pwsh providers |
| `subprocess/` | subprocess capability + local process-tree provider |
| `terminal/` | persistent sessions |
| `fs/` | filesystem capability + policy |
| `lsp/` | language-server capability |
| `skill/` | skill provider registry + local impl + catalog/loader |
| `web/` | web capability: search/fetch providers + tool Consumer |
| `compaction/` | compaction capability + basic provider |
| `context/` | request-context plugins |
| `subagent/` | subagent capability: providers + delegation Consumers |
| `bundle/` | installable `dsh --profile` patch-layer bundles |
| `workflow/` | workflow capability + worker-thread provider |
| `todo/` | `todo_write` tool |
| `plan/` | plan mode as logged state |
| `preset/` | per-session agent composition from preset `cordis.yml` |
| `guard/` | loop-hygiene + tool-timeout plugins |
| `self-modification/` | agent inspects/mounts its own plugins |
| `hooks/` | Claude Code / Codex hook bridges + wire-protocol library |
| `session/` | durable session data: persistence, projection, titles, telemetry |
| `identity/` | anonymous identity |
| `settings/` | user-settings capability + file provider |
| `credentials/` | credential-reference capability + env/.env provider |
| `acp/` | automation-only Agent Client Protocol server |
| `interaction/` | approval/interaction/permission/commands/ask-user |
| `boot/` | shared app-bin glue |
| `sdk/` | JSON-RPC protocol + server + TypeScript client |
| `examples/` | demo bundles (agent-spine + CLI/ACP/JSON-RPC bins) |
| `support/` | dev/test infrastructure |
| `util/` | zero-dependency utilities |

→ 完整 package hierarchy 见 [[references/dsh-package-hierarchy]]

## 开发约定（来自 AGENTS.md）

### 核心原则

1. **「everything is a plugin」** — 无 privileged core；每个贡献通过 `ctx.effect()` / `ctx.on()`
2. **Registrations are effects** — registry `register()` 返回 disposer；plugin unload 时自动 unwind
3. **Runtime invariants assert owned relationships** — 检查 authoritative event streams 或 mutable data，不靠 service 存在与否
5. **Typed events use declaration merging** — `SessionEventMap` 默认 required-on-read
6. **Switch on discriminant tags** — 关闭 union 末尾用 `assertNever`
7. **Waterfall listeners MUST call `next()`** — 不调就 short-circuit 链路
8. **Model-visible ⟺ logged** — 任何到模型的内容必须能从 session log 重建
9. **Plugins, not loop changes** — 新行为在文档化的 extension points
10. **Capability seam 三件套** — Service Definition / Service Provider / Consumer 必须完整
11. **Explicit > implicit at package boundaries** — `resolve(request): Spec` 显式步骤
12. **No hardcoded tunables in plugins** — 部署相关用 Config 字段
13. **Misconfiguration fails loud** — 永远不静默跳过缺失的引用
14. **Branded opaque cross-boundary ids** — `Branded<B>` from `dsh-brand`

### CI Gates（`pnpm run`）

| 命令 | 作用 |
|---|---|
| `pnpm run test` | vitest 单元测试 |
| `pnpm run test:coverage` | **CI coverage gate**（per-file 100% on `packages/*/*/src`）|
| `pnpm run test:e2e` | real-API 测试（无 `DEEPSEEK_API_KEY` 自跳）|
| `pnpm run test:snapshot` | keyless ACP/headless replay vs expected outputs |
| `pnpm run typecheck` | 严格 typecheck |
| `pnpm run lint` | oxlint |
| `pnpm run duplication` | 跨文件 TypeScript clone detection（jscpd）|
| `pnpm run build` | tsc emits `lib/` + types, tsdown bundles runtime |
| `pnpm run hygiene` | knip + publint + workspace constraints + NodeNext consumer check |
| `pnpm run doc-sync` | 所有 doc gates（`scripts/run-gates.ts`）|

**重要**：CI coverage gate 是 `test:coverage` 而非 `test`（100% per-file）。

## 「Pre-release stance」

> "Remove this section at the first tagged release. With no external consumers, prefer the correct foundation over compatibility shims."

- 不做兼容垫片
- 自由 rename / repackage + 同步更新所有引用
- Backends 直接 reject 旧 on-disk 格式
- SQLite 用 monotonic `SCHEMA_VERSION`
- `dsh-session` 保持 `SESSION_FORMAT_VERSION = 0`，**无兼容性承诺**

## Cordis 框架背景

dsh 完全基于 vendored Cordis（框架名 =「Core Dispatch System」）：

> "Cordis: plugins contribute services, typed events, and reversible effects to a shared context. Every part of the product is a plugin, including the model adapter, the tool registry, the session log, and the agent loop itself."

- [Cordis 论文](https://github.com/cordiverse/paper) — _A Programming Paradigm for Spatiotemporal Composability_
- `vendor/` 是 pinned source copies（manifest 含 upstream SHAs）

→ 详细机制见 [[concepts/cordis-plugin-framework]]

## 文件组织（顶层）

```
vendor/      Vendored Cordis source
packages/    @deepseek-ai/dsh-<pkg> workspaces
python/      Python SDK + bundled runtime
native/      @deepseek-ai/node-addon-landlock-run 源（Linux Landlock sandbox）
examples/    Runnable cordis.yml leaves over packages/examples bundles
.agents/    Agent workflows + Agent Notes（dsh 自己的 self-doc）
docs/        architecture + catalogs + postmortems + cookbook
scripts/     repo gates + generators
website/     VitePress projection of selected bilingual docs/ sources
```

## 与 vault 已有页面的呼应

- [[entities/cordis]] — vendored framework（vault 暂无，新页将补）
- [[concepts/ai-agent]] — dsh 是 agent 框架的工业实现
- [[concepts/deterministic-agent-memory]] — dsh 的 session log = 跨会话持久化的工程实现
- [[concepts/capability-seam]] — dsh 的核心抽象（三件套：Service Definition / Provider / Consumer）
- [[references/kimi-k3-official-blog]] — Kimi K3 也是 Moonshot 的 agent 路线，与 dsh 同类

## Open Questions

1. **dsh 与 Claude Code / Codex CLI / Gemini CLI 的关系** — 竞品 / 互补 / 同源？^[ambiguous]
2. **何时去掉 pre-release stance** — README 说「at first tagged release」，尚未 tag ^[ambiguous]
3. **Landlock 集成** — `native/landlock-run` 是 Linux 沙箱；macOS / Windows 等价物？^[inferred]
4. **Typert RPC gateway 的类型传播** — TypeScript 之外的客户端（Python SDK）如何处理 ^[ambiguous]

## 相关页面

- [[entities/cordis]] — 框架本体
- [[entities/deepseek-ai]] — 母公司
- [[concepts/cordis-plugin-framework]] — dsh 的架构基础
- [[concepts/capability-seam]] — 三件套抽象
- [[references/dsh-package-hierarchy]] — 24 个 package group 全景
- [[skills/deepseek-harness-dev-loop]] — 开发 loop 操作 skill