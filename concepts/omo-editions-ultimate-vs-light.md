---
title: "omo Editions 对比（Ultimate vs Light）"
category: concepts
tags:
  - omo
  - editions
  - opencode
  - codex-cli
  - concept
sources:
  - "https://github.com/code-yeongyu/oh-my-openagent"
created: "2026-08-05T07:30:00Z"
updated: "2026-08-05T07:30:00Z"
provenance:
  extracted: 0.92
  inferred: 0.06
  ambiguous: 0.02
base_confidence: 0.78
lifecycle: draft
lifecycle_changed: "2026-08-05"
tier: supporting
relationships:
  - target: "[[entities/oh-my-openagent]]"
    type: related_to
  - target: "[[skills/omo-install-and-setup]]"
    type: related_to
summary: "omo 两个发行版对比：Ultimate（OpenCode harness，11 agents / 54 hooks / 5 MCP，全功能）vs Light（Codex CLI，8 组件，轻量便携），相同 SUL-1.0 许可。"
---

# omo Editions 对比（Ultimate vs Light）

> omo **同一产品两个版本**——Ultimate Edition（OpenCode，完整）与 Light Edition（Codex CLI，portable 组件）。**同源两用**。

## 版本对比

| 维度 | Ultimate Edition | Light Edition |
|---|---|---|
| **目标 harness** | OpenCode | OpenAI Codex CLI |
| **安装命令** | `bunx oh-my-openagent install` | `npx lazycodex-ai install` |
| **agents 数** | **11** | 0（用 Codex CLI 原生 agent） |
| **lifecycle hooks** | **54+** | 8 组件 |
| **内置 MCP** | **5**（Exa / Context7 / Grep.app 等） | **5**（grep_app / context7 / codegraph / git_bash / lsp） |
| **Team Mode** | ✓ | ✗（Codex CLI 自带） |
| **`ultrawork` / `ulw`** | ✓ | ✓ |
| **`ulw-loop`** | ✓ | ✓ |
| **`hashline` 编辑** | ✓ | ✗（Codex 用自己 edit tool） |
| **IntentGate** | 完整 | 仅 `ultrawork`/`ulw` 关键词识别 |
| **AST-Grep** | ✓ | ✗ |
| **Tmux 集成** | ✓ | ✗（Codex 自带） |
| **background agents** | ✓ | ✗ |
| **Goal / Todo Enforcer** | ✓ | ✗ |

## 安装与配置

| 想要 | 命令 | 落到磁盘 |
|---|---|---|
| **Ultimate** | `bunx oh-my-openagent install`（TUI 引导） | OpenCode plugin 注册 + agent/model 配置 + provider 鉴权 |
| **Light** | `npx lazycodex-ai install` | `~/.codex/plugins/cache/sisyphuslabs/omo/` + Codex marketplace cache + `~/.codex/config.toml` 块 |
| **两个都要** | `bunx oh-my-openagent install --platform=both` | 两套都装 |

## 8 个 Light Edition 组件

| 组件 | 用途 |
|---|---|
| `rules` | 项目规则注入（AGENTS.md / .omo/rules/**） |
| `comment-checker` | 防 AI slop 注释 |
| `git-bash` | Git 操作 |
| `lsp` | LSP（diagnostics / navigation） |
| `ultrawork` | 单 keyword 触发全 agent |
| `ulw-loop` | durable multi-goal orchestration |
| `start-work-continuation` | session 持续推进 |
| `telemetry` | 匿名遥测 |

**Light Edition 没有 `team_*` 工具**——"Codex CLI's own surface does that work"。

## 设计哲学

> "oh-my-openagent ships in two editions of the same product."

**同一产品，两个市场**：

- Ultimate Edition 卖给 **OpenCode 用户**（完整 multi-agent orchestration）
- Light Edition 卖给 **Codex CLI 用户**（portable 组件，不与 Codex 自带功能重复）

**关键判断**：用户装 Light Edition 不需要 Bun——`npx lazycodex-ai install` 走 Node/npm。

## 与 vault 已有概念的关系

| vault 已有 | 在两个 Edition 中的体现 |
|---|---|
| [[concepts/ai-tool-specialization]] | 两个 Edition 各自专业化——Ultimate 多 agent / Light portable 组件 |
| [[skills/claude-code-token-optimization]] | Light Edition 也走 Skill-Embedded MCPs，token 节流同策略 |
| [[concepts/mcp-server-protocol-quirks]] | 两个 Edition 都有 plugin-scoped MCPs，避开全局注册的坑 |
| [[entities/bmad-method]] | 类似的"core + module"分版本策略 |

## 命名注意

> "The published npm package and CLI binary are still named `oh-my-opencode` (dual-published as `oh-my-openagent` during the rename transition)."

npm 包名 + CLI binary 仍是 `oh-my-opencode`（改名期间 dual-published `oh-my-openagent`）。`omo` 是 bin alias，**但**：

> "**do not** use `bunx omo` or `npx omo` — `omo` is a different, unrelated npm package by a different author, and the package manager may resolve the wrong one."

`omo` 是另一作者的不同 npm 包——**不要用 `bunx omo`**！

## Codex Marketplace 细节

- **marketplace 仓库**: `code-yeongyu/lazycodex`
- **marketplace 名**: `sisyphuslabs`
- **plugin 名**: `omo`
- **Codex 看到**: `omo@sisyphuslabs`

## Related

- [[entities/oh-my-openagent]] — 框架本体
- [[skills/omo-install-and-setup]] — 安装流程
- [[concepts/omo-skill-embedded-mcps]] — 两个 Edition 都有 plugin-scoped MCPs