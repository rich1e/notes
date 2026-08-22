---
title: "DeepSeek Harness Dev Loop — CI Gates + Pre-Push Checks"
category: skills
tags:
  - deepseek-harness
  - ci-gates
  - pre-push
  - pnpm
  - skills
summary: "dsh 开发 loop skill：从 pnpm install 到 pre-push 检查的全流程。CI coverage gate 是 test:coverage（per-file 100%）而非 test。Host sandbox 失败先用 narrowest escalation 试一次。匹配证据到 surface：focused tests / snapshots / doc-sync / build-hygiene / real-API e2e。"
sources:
  - "https://github.com/deepseek-ai/deepseek-harness/blob/main/AGENTS.md"
created: "2026-08-14T01:28:00Z"
updated: "2026-08-14T01:28:00Z"
provenance:
  extracted: 0.92
  inferred: 0.06
  ambiguous: 0.02
base_confidence: 0.7
lifecycle: draft
lifecycle_changed: "2026-08-14"
tier: supporting
relationships:
  - target: "[[entities/deepseek-harness]]"
    type: derived_from
---

# DeepSeek Harness Dev Loop — CI Gates + Pre-Push Checks

> dsh 项目的开发 loop skill：从 clone 到 pre-push 检查的完整工作流。

## 一次性 Setup

```sh
git clone https://github.com/deepseek-ai/deepseek-harness.git
cd deepseek-harness

# Node ^22.19 || >=24
node --version

# pnpm
npm install -g pnpm

# 安装依赖 + build
pnpm install
pnpm run build

# 验证 — 跑一遍核心 gates
pnpm run typecheck
pnpm run test
```

## 日常 Commands

### 测试分层

| 命令 | 用途 | 何时用 |
|---|---|---|
| `pnpm run test` | vitest 单元测试 | 本地常规验证 |
| **`pnpm run test:coverage`** | **CI coverage gate**（per-file 100% on `packages/*/*/src`）| **pre-push 必跑** |
| `pnpm run test:e2e` | real-API 测试（无 `DEEPSEEK_API_KEY` 自跳）| 改了 provider 时 |
| `pnpm run test:snapshot` | keyless ACP/headless replay vs expected outputs | 改了 model 输出或 UI 时 |
| `pnpm run test:snapshot:record` | re-record expected outputs（需要 key）| 故意改变输出时 |

### 静态检查

```sh
pnpm run typecheck   # tsc strict + noImplicitAny
pnpm run lint        # oxlint
pnpm run duplication # 跨文件 TypeScript clone detection (jscpd)
```

### Build / Hygiene

```sh
pnpm run build       # tsc emits lib/types + tsdown bundles runtime
pnpm run hygiene     # knip + publint + workspace constraints + NodeNext consumer check
pnpm run doc-sync    # 所有 doc gates（leaf list in scripts/run-gates.ts）
pnpm run website:build  # VitePress build（doubles作双验证 dead-link check）
```

## Pre-push Check 决策树

> "Match evidence to the surface: focused tests for behavior, snapshots for model or user output, `doc-sync` for docs, build/hygiene and built smokes for published paths, and real-API e2e for provider behavior."

```
改了 什么？
│
├─ 业务行为 / 单元代码 ──→ pnpm run test (focused)
│
├─ 模型 prompt / / UI 输出 ──→ pnpm run test:snapshot (record 必要时)
│
├─ 文档 / README / JSDoc ──→ pnpm run doc-sync
│
├─ 公开 API / 导出形状 ──→ pnpm run build + pnpm run hygiene + built smokes
│
├─ LLM provider / 模型适配 ──→ pnpm run test:e2e (needs DEEPSEEK_API_KEY)
│
└─ 任何「重要」改动 ──→ pnpm run test:coverage (CI gate)
```

**重要原则**：

> "Never default to the full suite or repeat a passing check for commit or push. CI owns exhaustive coverage and the platform matrix."

- **不要默认跑全套** — CI 负责
- **不要重复跑通过的检查** — 浪费 token
- **匹配改动 surface 到对应检查** — focused tests 给行为，snapshots 给输出

## Host Sandbox 失败处理

> "When required `gh`, `pnpm`, build, test, or generator commands fail because the agent sandbox blocks credentials, network, IPC, file watching, or nested `sandbox-exec`, retry unchanged with the narrowest host escalation before diagnosing authentication or project failure."

**步骤**：

1. 命令失败
2. **先 retry 一次 unchanged** + 用最窄的 host escalation（提供必要 credentials）
3. 仍失败 → 才诊断 authentication / project 问题
4. **不要**绕过 genuine test failure 或被测产品 sandbox

**反例**（错误做法）：
- 直接用 root 权限跑（bypass）
- 把 sandbox 禁用掉（破坏测试环境）
- 修改测试让它过（cheat）

## Subprocess 启动模式

dsh 的 source launch 走 tsx's ESM-only hook (`node --import tsx/esm`)，所以：

> "modules it reaches must stay ESM (no CJS-only exports)"

- 不要写 CJS-only exports
- Node 原生 TypeScript modes 不可用（engines 范围太广）

## 重要：CI Coverage Gate 是 `test:coverage`

> "`test:coverage`, not `test`, is the CI coverage gate"

- `pnpm run test` 不强制 100%
- `pnpm run test:coverage` 强制 per-file 100% on `packages/*/*/src`
- pre-push **必须跑** `test:coverage`

## Agent Note — 每个 PR 必须

> "Non-trivial changes MUST include an Agent Note in the same PR; only mechanical/local edits are exempt"

- 非平凡改动 = 必须有 Agent Note（在 `.agents/notes/`）
- 仅 mechanical / local edits 可豁免
- Archived notes **冻结**：never edit 或 treat as current authority

## Labels（GitHub PR）

```
Labels:
  - kind/*        (one — 主分类)
  - area/*        (material changes — 所有相关 area)
  - native Issue Type
```

详细 taxonomy：[.agents/notes/implemented/process/2026-08-08-unified-github-label-taxonomy.md](https://github.com/deepseek-ai/deepseek-harness/blob/main/.agents/notes/implemented/process/2026-08-08-unified-github-label-taxonomy.md)

## Vendoring Update 流程

```sh
# 1. 看 vendor/README.md 的 manifest
cat vendor/README.md

# 2. 按 sync procedure 拉 upstream
# (具体步骤在 vendor/README.md)

# 3. 重新应用或 retire logged local modifications

# 4. 跑全套验证
pnpm run test
pnpm run build
```

## 反向论证

| 误区 | 实际 |
|---|---|
| 「pre-push 跑完整 suite」 | CI 负责；本地跑 focused |
| 「passing 测试重跑确保」 | 浪费；CI 已覆盖 |
| 「Sandbox 失败就 disable」 | 先 narrowest escalation retry；不要 bypass |
| 「agent-loop 改了不需要更新 architecture.md」 | 「Plugins, not loop changes」 — 改 loop 必须更新 docs |
| 「改动归档 note」 | Archive notes frozen — 写新 note |

## Open Questions

1. **真实 API key 来源** — 团队共享 vs 个人 ^[ambiguous]
2. **Wine-on-Windows 的具体测试 surface** — CI 独有 ^[inferred]
3. **Snapshot 的 promotion 流程** — record → review → merge ^[ambiguous]

## 相关页面

- [[entities/deepseek-harness]] — dsh 项目
- [[concepts/cordis-plugin-framework]] — 架构基础
- [[concepts/capability-seam]] — 添加新 capability 的流程
- [[references/dsh-package-hierarchy]] — package 全景