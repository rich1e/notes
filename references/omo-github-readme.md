---
title: "omo GitHub README"
category: references
tags:
  - omo
  - github
  - readme
  - reference
sources:
  - "https://github.com/code-yeongyu/oh-my-openagent"
source_url: "https://github.com/code-yeongyu/oh-my-openagent"
created: "2026-08-05T07:30:00Z"
updated: "2026-08-05T07:30:00Z"
summary: "omo 仓库 README + highlights 完整表（20 项特性 × 2 版本对比）+ 5 discipline agents 详情 + Team Mode v4.0 + 4 category model routing + SUL-1.0 许可证。"
provenance:
  extracted: 0.92
  inferred: 0.04
 ambiguous: 0.04
base_confidence: 0.82
lifecycle: reviewed
lifecycle_changed: "2026-08-05"
tier: core
---

# omo GitHub README

> [[entities/oh-my-openagent]] 仓库主入口。gitingest 抓取（commit `19abf74` / 2026-08-05）。

## 仓库元信息

- **URL**: https://github.com/code-yeongyu/oh-my-openagent
- **License**: SUL-1.0（Stackable Use License，**非 OSI 开源**——可自托管可改但有 stackable 限制）
- **Stars/contribs**: contrib.rocks image（具体数未抓）
- **npm**: `oh-my-opencode`（rename 期间 dual-published `oh-my-openagent`）+ `lazycodex-ai`（Light 安装器）
- **当前 commit**: `19abf74feb0eb1b82f37e70a2dd68a519cf88a08`
- **文件数 / Token**: 526 文件 / 1.1M tokens / 4.31MB（gitingest `--include-pattern "*.md"` 后）

## 公告（README 顶部）

### OmO for Codex（LazyCodex）

> "We loved Anthropic models enough to get blocked. Now we are backing Codex."

npx lazycodex-ai install — 看 [lazycodex.ai](https://lazycodex.ai)

### Multi-Harness Agent OS 重构中

> "We are restructuring the codebase to support multiple agent harnesses (OpenCode, Codex, Pi, Claude Code, and others)."

读 [ROADMAP.md](./ROADMAP.md) 再贡献。PR 用 `ROADMAP` label。

### Building in Public

> "The maintainer builds and maintains oh-my-openagent in real-time with Jobdori, an AI assistant running on a heavily customized fork of OpenClaw."

看 [Discord #building-in-public](https://discord.gg/PUwSMR9XNk) 看实况。

## 哲学宣言

> "Anthropic blocked OpenCode because of us. Yes, this is true."

> "They want you locked in. Claude Code is a nice prison, but it's still a prison."

> "You don't need to pay $200 for 2 hours of work. The future isn't picking one winner; it's orchestrating them all."

## 4 用户评价（README 收录）

- "It made me cancel my Cursor subscription." — Arthur Guiot
- "If Claude Code does in 7 days what a human does in 3 months, Sisyphus does it in 1 hour." — B, Quant Researcher
- "Knocked out 8000 eslint warnings with Oh My Opencode, just in a day." — Jacob Ferrari
- "I converted a 45k line tauri app into a SaaS web app overnight using Ohmyopencode and ralph loop." — James Hargis

## Highlights 完整表（20 项）

| Feature | Edition | 做什么 |
|---|---|---|
| 🤖 **Discipline Agents** | Ultimate | Sisyphus 协调 Hephaestus / Oracle / Librarian / Explore |
| 🧩 **Codex CLI Light Edition** | Light | Portable OMO 组件跑在 OpenAI Codex CLI 里 |
| 👥 **Team Mode** (v4.0, opt-in) | Ultimate | lead + 8 members + tmux 可视化 + team_* tools |
| ⚡ **`ultrawork` / `ulw`** | Both | 一词触发，全 agent 激活，不停直到完成 |
| 🚪 **IntentGate** | Ultimate | 分析真实意图，Light 只识别关键词 |
| 🔗 **Hash-Anchored Edit Tool** | Ultimate | `LINE#ID` 内容哈希验证（受 oh-my-pi 启发）|
| 🛠️ **LSP 集成** | Both | diagnostics / navigation / symbols / rename |
| 🔎 **AST-Grep** | Ultimate | 25 种语言 pattern-aware 代码搜索 |
| 🧠 **Background Agents** | Ultimate | 5+ specialists 并行 |
| 📚 **Built-in MCPs** | Ultimate | Exa / Context7 / Grep.app |
| 🔁 **Goal / `/goal`** | Ultimate | session 级持久目标 |
| ✅ **Todo Enforcer** | Ultimate | agent idle 系统拽回 |
| 💬 **Comment Checker** | Both | 防 AI slop 注释 |
| 📐 **Rules Injection** | Both | AGENTS.md / .omo/rules/** 自动加载 |
| 🎯 **Ulw Loop** | Both | durable multi-goal + evidence audit |
| 🖥️ **Tmux 集成** | Ultimate | 完整交互式终端 |
| 🔌 **Claude Code 兼容** | Ultimate | 所有 hooks / commands / skills / MCPs / plugins 兼容 |
| 🧬 **Skill-Embedded MCPs** | Ultimate | skill 自带 MCP，spinning up on-demand |
| 📋 **Prometheus Planner** | Ultimate | interview-mode 战略规划 |
| 🔍 **`/init-deep`** | Ultimate | 自动生成层级 AGENTS.md |

## 5 Discipline Agents

| Agent | 默认模型 | 角色 |
|---|---|---|
| **Sisyphus** | claude-opus-5 / **kimi-k3** / **glm-5** | 主 orchestrator（计划 + 委派 + 持续推进） |
| **Hephaestus** | gpt-5.6-sol（OpenAI / Copilot / Vercel / OpenCode，medium effort）| Autonomous Deep Worker（自主端到端） |
| **Prometheus** | claude-fable-5 / **kimi-k3** | Strategic Planner（interview mode） |
| **Oracle** | （未列具体模型）^[ambiguous] | 推测：架构 / 决策顾问 |
| **Librarian** | （未列具体模型）^[ambiguous] | 推测：知识库 / 文档检索 |
| **Explore** | （未列具体模型）^[ambiguous] | 推测：codebase 探索 |

> "We run best on Opus or Kimi K3, but Kimi K3 + GPT-5.6 Sol already beats vanilla Claude Code. Zero config needed."

## Team Mode JSONC 示例

```jsonc
{
  "team_mode": {
    "enabled": true,
    "max_parallel_members": 4,
    "tmux_visualization": true
  }
}
```

## 4 Category Routing

| Category | 用途 |
|---|---|
| `visual-engineering` | 前端 / UI/UX / 设计 |
| `deep` | 自主研究 + 执行 |
| `quick` | 单文件改动 / typo |
| `ultrabrain` | 硬逻辑 / 架构决策 |

## Hashline Edit Tool

```
11#VK| function hello() {
22#XJ|   return "world";
33#MB| }
```

> "Grok Code Fast 1: **6.7% → 68.3%** success rate, just from changing the edit tool."

## 两个版本

| | Ultimate | Light |
|---|---|---|
| 安装 | `bunx oh-my-openagent install` | `npx lazycodex-ai install` |
| Harness | OpenCode | OpenAI Codex CLI |
| Agents | 11 | 0（用 Codex CLI 原生） |
| Hooks | 54+ | 8 组件 |
| MCPs | 5（Ultimate 内置） | 5（plugin-scoped） |

## 链接资源

- 文档：[omo.vibetip.help/docs](https://omo.vibetip.help/docs)
- DeepWiki：[deepwiki.com/code-yeongyu/oh-my-openagent](https://deepwiki.com/code-yeongyu/oh-my-openagent)
- Discord：[discord.gg/PUwSMR9XNk](https://discord.gg/PUwSMR9XNk)
- 主维护者 X：[x.com/justsisyphus](https://x.com/justsisyphus)
- Sisyphus Labs：[sisyphuslabs.ai](https://sisyphuslabs.ai)

## Related

- [[entities/oh-my-openagent]] — 框架本体
- [[entities/sisyphus-agent]] / [[entities/hephaestus-agent]] — 核心 agents
- [[concepts/omo-ultrawork-mode]] / [[concepts/omo-team-mode]] / [[concepts/omo-hashline-edits]] / [[concepts/omo-editions-ultimate-vs-light]]
- [[skills/omo-install-and-setup]] — 安装流程
- [[references/omo-team-mode-config-schema]] — 11 字段配置详解
- `_raw/github-code-yeongyu-oh-my-openagent.txt` — 完整 gitingest 抓取（526 文件 / 1.1M tokens）