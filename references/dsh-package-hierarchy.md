---
title: "DeepSeek Harness Package Hierarchy — 24 Package Groups 全景"
category: references
tags:
  - deepseek-harness
  - monorepo
  - package-hierarchy
  - capability-seam
  - reference-table
summary: "DeepSeek Harness (`dsh`) 的 24 个 package group 全景索引：按 AGENTS.md 的分类，标注每个 group 的角色（core / api / llm / fs / 等）和它在 capability seam 中的位置。"
sources:
  - "https://github.com/deepseek-ai/deepseek-harness/blob/main/AGENTS.md"
source_url: "https://github.com/deepseek-ai/deepseek-harness"
created: "2026-08-14T01:28:00Z"
updated: "2026-08-14T01:28:00Z"
provenance:
  extracted: 0.95
  inferred: 0.04
  ambiguous: 0.01
base_confidence: 0.85
lifecycle: draft
lifecycle_changed: "2026-08-14"
tier: peripheral
relationships:
  - target: "[[entities/deepseek-harness]]"
    type: derived_from
  - target: "[[concepts/capability-seam]]"
    type: related_to
---

# DeepSeek Harness Package Hierarchy — 24 Package Groups 全景

> dsh 项目的 24 个 package group 完整索引（按 AGENTS.md 分类）。每个 group 标注角色（product core / capability / utility）和它在 capability seam 中的位置。

## 完整列表（按 AGENTS.md 顺序）

### Product Core (core/)

| Package | Owns | `ctx` key |
|---|---|---|
| `core/session` | append-only `SessionEvent` log + in-memory store | `ctx.sessions` |
| `core/system-prompt` | prompt section + tool schema assembly | `ctx.systemPrompt` |
| `core/tools` | scoped tool registry + guarded execution pipeline | `ctx.tools` |
| `core/agent` | `Agent` interface + live registry + `agent/*` events | `ctx.agents` |
| `core/agent-loop` | default driver implementing that interface | `ctx.agentLoop` |
| `core/scope` | per-agent scoped-registration primitive | library, no key |

### API & Type System (api/, typert/)

| Package | Owns |
|---|---|
| `api/` | Remote BFF assembly + Typert RPC gateway |
| `typert/` | type graph generator, loader, runtime registry |

### LLM Capability (llm/)

| Package | Owns |
|---|---|
| `llm/` | LLM capability: Service Definition/Consumer + DeepSeek providers |

### Sandbox (e2b/)

| Package | Owns |
|---|---|
| `e2b/` | E2B POC: sandbox + FS/subprocess adapters |

### Execution Capabilities (shell/, subprocess/, terminal/)

| Package | Owns |
|---|---|
| `shell/` | bash capability: Service Definition + local/pwsh providers + shell Consumers |
| `subprocess/` | subprocess capability + local process-tree provider |
| `terminal/` | persistent sessions |

### File & Language (fs/, lsp/)

| Package | Owns |
|---|---|
| `fs/` | filesystem capability + policy |
| `lsp/` | language-server capability |

### Skills & Content (skill/, web/, compaction/)

| Package | Owns |
|---|---|
| `skill/` | skill provider registry + local impl + catalog/loader tool |
| `web/` | web capability: Service Definition + search/fetch providers + tool Consumer |
| `compaction/` | compaction capability + basic provider |

### Context & Subagent (context/, subagent/)

| Package | Owns |
|---|---|
| `context/` | request-context plugins |
| `subagent/` | subagent capability: Service Definition + providers + delegation Consumers |

### Workflow & State (bundle/, workflow/, plan/, todo/)

| Package | Owns |
|---|---|
| `bundle/` | installable `dsh --profile` patch-layer bundles |
| `workflow/` | workflow capability + worker-thread provider + tool Consumer |
| `plan/` | plan mode as logged state |
| `todo/` | `todo_write` tool |

### Composition & Guards (preset/, guard/)

| Package | Owns |
|---|---|
| `preset/` | per-session agent composition from preset cordis.yml files |
| `guard/` | loop-hygiene + tool-timeout plugins |

### Meta-Capabilities (self-modification/, hooks/)

| Package | Owns |
|---|---|
| `self-modification/` | the agent inspects/mounts its own plugins |
| `hooks/` | Claude Code / Codex hook bridges + wire-protocol library |

### Persistence & Identity (session/, identity/)

| Package | Owns |
|---|---|
| `session/` | durable session data: persistence, projection, titles, telemetry |
| `identity/` | anonymous identity |

### Settings & Credentials (settings/, credentials/)

| Package | Owns |
|---|---|
| `settings/` | user-settings capability + file provider |
| `credentials/` | credential-reference capability + env/.env provider |

### Interface (acp/, interaction/)

| Package | Owns |
|---|---|
| `acp/` | automation-only Agent Client Protocol server |
| `interaction/` | approval/interaction capabilities, permission, commands, ask-user |

### Infrastructure (boot/, sdk/, examples/, support/, util/)

| Package | Owns |
|---|---|
| `boot/` | shared app-bin glue |
| `sdk/` | JSON-RPC protocol, server, TypeScript client |
| `examples/` | demo bundles (agent-spine + CLI/ACP/JSON-RPC bins) |
| `support/` | dev/test infrastructure |
| `util/` | zero-dependency utilities |

### External (vendor/, python/, native/)

| Path | Owns |
|---|---|
| `vendor/` | Vendored Cordis source — manifest + sync procedure in `vendor/README.md` |
| `python/` | Python SDK + bundled runtime (see `python/README.md`) |
| `native/` | `@deepseek-ai/node-addon-landlock-run` source of record (see `native/README.md`) |

## Capability Seam 全景（按「哪个 group 是 Definition」）

| Capability | Definition Group | Providers (in dsh) | Consumers |
|---|---|---|---|
| **llm** | `llm/` | DeepSeek (同包), OpenAI (third-party) | `llm/` (同包 Consumer) |
| **shell** | `shell/` | local, pwsh, sandbox | `shell/` Consumers |
| **subprocess** | `subprocess/` | local | bash, terminal Consumers |
| **terminal** | `terminal/` | local | `dsh-tool-terminal` |
| **fs** | `fs/` | local, sandbox | file tools |
| **lsp** | `lsp/` | local | LSP-aware tools |
| **skill** | `skill/` | local | `skill-catalog` tool |
| **web** | `web/` | search, fetch | `dsh-tool-web` |
| **subagent** | `subagent/` | fork, delegate | delegation tools |
| **workflow** | `workflow/` | worker | workflow tool |
| **compaction** | `compaction/` | basic | (internal) |
| **credentials** | `credentials/` | env | (internal) |

## 添加新 Package 的 Checklist

> "Adding a capability means designing all three."

1. **先确定 capability 类型** — core capability / utility / infrastructure？
2. **检查现有 seam 是否复用** — 是否在 `shell/` 已经定义过？
3. **新建 group**（如 `core/`, `llm/`, `tools/`）：
 - `dsh-<name>` = Service Definition
 - `dsh-<name>-<impl>` = Provider
 - `dsh-tool-<name>` = Consumer（model-facing tool）
4. **更新 resolver manifest dependencies**
5. **更新 cordis.yml / profile bundle**
6. **更新架构 docs**（`docs/architecture.md` 的「Where new behavior goes」表）

## 反向论证

| 误区 | 实际 |
|---|---|
| 「单包就够了」 | 三件套（Definition / Provider / Consumer）通常分 |
| 「utils 进 examples」 | examples 是 demo bundle，不是 utility |
| 「native 是 plugin」 | native 是 native node-addon（Landlock）— 是 binary |
| 「vendor 是 npm 依赖」 | vendored = 内嵌源码，可本地修改 |

## Open Questions

1. **每个 group 内的子包数量** — README 提到 `packages/<group>/<pkg>/` 模式 ^[ambiguous]
2. **跨 group 依赖的可见性** — 由 resolver manifest 控制 ^[inferred]
3. **Native (Landlock) 的 macOS/Windows 替代** — 推测 sandbox provider 抽象会处理 ^[ambiguous]

## 相关页面

- [[entities/deepseek-harness]] — dsh 项目
- [[concepts/capability-seam]] — 三件套抽象
- [[concepts/cordis-plugin-framework]] — 框架基础
- [[skills/deepseek-harness-dev-loop]] — 开发 loop