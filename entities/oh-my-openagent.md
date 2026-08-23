---

title: "Oh My OpenAgent (omo)"
category: entities
tags:
  - omo
  - agent-orchestration
  - multi-model
  - opencode
  - entity
sources:
  - "https://github.com/code-yeongyu/oh-my-openagent"
created: "2026-08-05T07:30:00Z"
updated: 2026-08-23T09:05:00Z
summary: "oh-my-openagent（code-yeongyu, SUL-1.0）是 OpenCode 的多模型 agent 编排框架：11 个 discipline agents + 54+ 生命周期 hooks + 5 内置 MCP + Team Mode + ultrawork 单 keyword。Ultimate Edition 完整 + Light Edition (Codex CLI) 轻量。"
provenance:
  extracted: 0.92
  inferred: 0.06
  ambiguous: 0.02
base_confidence: 0.78
lifecycle: draft
lifecycle_changed: "2026-08-05"
tier: supporting
relationships:
  - target: "[[entities/sisyphus-agent]]"
    type: related_to
  - target: "[[entities/hephaestus-agent]]"
    type: related_to
  - target: "[[concepts/omo-ultrawork-mode]]"
    type: related_to
  - target: "[[concepts/omo-team-mode]]"
    type: related_to
  - target: "[[concepts/omo-editions-ultimate-vs-light]]"
    type: related_to

---
# Oh My OpenAgent (omo)

> [code-yeongyu / oh-my-openagent](https://github.com/code-yeongyu/oh-my-openagent) 是 **OpenCode 上的多模型 agent 编排框架**——SUL-1.0 许可证。**两个版本**：Ultimate Edition（OpenCode，11 agents / 54+ hooks / 5 MCP / Team Mode / ultrawork / hashline edits）+ Light Edition（Codex CLI，8 组件 portable）。

## 一句话定位

> "Multi-model agent orchestration harness for OpenCode. Not locked to Claude. Not locked to OpenAI. Not locked to anyone. Just better results, cheaper models, real orchestration."

## 安装

```bash
# Ultimate (OpenCode)
bunx oh-my-openagent install

# Light (Codex CLI)
npx lazycodex-ai install

# 两者都装
bunx oh-my-openagent install --platform=both
```

**强烈建议让 LLM agent 帮你装**——Ultimate 涉及 11 agent 模型选择 + per-provider 鉴权，人装易错。给 agent：

```
Install and configure oh-my-openagent by following the instructions here:
https://raw.githubusercontent.com/code-yeongyu/oh-my-openagent/refs/heads/dev/docs/guide/installation.md
```

## 17 项 Highlights

| # | 特性 | 版本 | 做什么 |
|---|---|---|---|
| 🤖 | **Discipline Agents** | Ultimate | Sisyphus 协调 Hephaestus / Oracle / Librarian / Explore。完整 AI dev team 并行 |
| 🧩 | **Codex CLI Light Edition** | Light | 8 个 portable 组件跑在 OpenAI Codex CLI 里 |
| 👥 | **Team Mode** (v4.0, opt-in) | Ultimate | lead + 8 个并行成员 + tmux 可视化 + `team_*` 工具族。`hyperplan`（5 hostile critics）+ `security-research`（3 hunters + 2 PoC engineers） |
| ⚡ | **`ultrawork` / `ulw`** | Both | 一个词。每个 agent 激活。不停直到完成 |
| 🚪 | **IntentGate** | Ultimate | 行动前分析真实意图。Light 版只识别 `ultrawork`/`ulw` |
| 🔗 | **Hash-Anchored Edit Tool** | Ultimate | `LINE#ID` 内容哈希验证每次改动。受 [oh-my-pi](https://github.com/can1357/oh-my-pi) 启发 |
| 🛠️ | **LSP 集成** | Both | diagnostics / navigation / symbols / workspace rename |
| 🔎 | **AST-Grep** | Ultimate | 25 种语言 pattern-aware 代码搜索/改写 |
| 🧠 | **Background Agents** | Ultimate | 5+ specialists 并行 |
| 📚 | **Built-in MCPs** | Ultimate | Exa（web）/ Context7（docs）/ Grep.app（GitHub search） |
| 🔁 | **Goal / `/goal`** | Ultimate | session 级持久目标。完成审计说 done 才停 |
| ✅ | **Todo Enforcer** | Ultimate | agent idle? 系统拽回 |
| 💬 | **Comment Checker** | Both | 防 AI slop 注释 |
| 📐 | **Rules Injection** | Both | AGENTS.md / .omo/rules/** 自动加载 |
| 🎯 | **Ulw Loop** | Both | durable multi-goal orchestration + evidence audit |
| 🖥️ | **Tmux 集成** | Ultimate | 完整交互式终端 |
| 🔌 | **Claude Code 兼容** | Ultimate | 所有 hooks / commands / skills / MCPs / plugins 都兼容 |
| 🧬 | **Skill-Embedded MCPs** | Ultimate | skill 自带 MCP，spinning up on-demand |
| 📋 | **Prometheus Planner** | Ultimate | 面试式战略规划 |
| 🔍 | **`/init-deep`** | Ultimate | 自动生成层级 AGENTS.md |

## 核心哲学

> "Anthropic blocked OpenCode because of us. Yes, this is true."

> "The future isn't picking one winner; it's orchestrating them all. Models get cheaper every month. Smarter every month. No single provider will dominate."

omo 不绑定任何单一模型。Opus 5 编排 + 视觉；GPT-5.6 Sol 深度推理；Kimi K3 / GLM 5.2 视觉备援；Kimi 高速做 quick 任务。**全部自动协作**。

## 模型路由（4 个 category）

| Category | 用途 |
|---|---|
| `visual-engineering` | 前端 / UI/UX / 设计 |
| `deep` | 自主研究 + 执行 |
| `quick` | 单文件改动 / typo |
| `ultrabrain` | 硬逻辑 / 架构决策 |

agent 说它需要什么类型的工作，harness 自动选对模型。`ultrabrain` 现在路由到 **GPT-5.6 Sol xhigh**（通过 OpenAI / Vercel），fallback 到 GPT-5.6 Sol xhigh。

## 推荐订阅（官方）

> "Even with only the following subscriptions, ultrawork works well (this project is not affiliated):"

- [ChatGPT Subscription ($20)](https://chatgpt.com/)
- [Kimi Code Subscription ($19)](https://www.kimi.com/code)
- [GLM Coding Plan ($10)](https://z.ai/subscribe)

**判断**：vault [[concepts/ai-tool-specialization]] 与 [[concepts/agent-team-cost-overhead]] 的实战案例——$19 + $10 + $20 = $49/月 vs Claude Code $200/月。

## Telemetry（匿名）

匿名遥测默认开。每天每个机器最多发一次（SHA256-hashed installation id），不建 PostHog profile。

```bash
# 关闭主插件
OMO_DISABLE_POSTHOG=1
OMO_SEND_ANONYMOUS_TELEMETRY=0

# 关闭 Codex Light
OMO_CODEX_DISABLE_POSTHOG=1
OMO_CODEX_SEND_ANONYMOUS_TELEMETRY=0
```

## 与 vault 已有概念的关系

| vault 已有 | 在 omo 中的体现 |
|---|---|
| [[entities/claude-code-agent-teams-feature]] | Team Mode 直接借鉴 + 扩展（12 team_* tools + hyperplan + security-research） |
| [[entities/bmad-method]] | omo 的 "Discipline Agents" 与 BMad "named agent" 同源哲学 |
| [[concepts/agent-team-display-modes]] | Team Mode 用 tmux pane 可视化（与 Claude Code `teammateMode: tmux` 同思路） |
| [[concepts/agent-team-mailbox-protocol]] | Team Mode 12 team_* tools 应基于 mailbox JSON 通信 |
| [[concepts/agent-team-cost-overhead]] | omo 推荐 $49/月 = vault token 优化实战示例 |
| [[concepts/ai-tool-specialization]] | omo 4 category routing = 按工作类型选模型的最成熟实现 |
| [[concepts/agent-team-race-condition-task-claim]] | Team Mode 任务分配应同样用 file lock |
| [[skills/claude-code-token-optimization]] | Skill-Embedded MCPs = MCP schema 不进主 context 的实现 |

## Open Questions

- "Hashline edits" 的具体 Git diff / 冲突解决语义——README 给 `LINE#ID` 格式但未给完整算法 ambiguous
- `omo` npm bin alias 与同名包冲突——README 警告但未深究 ambiguous
- Anthropic blocked OpenCode 的具体故事背景——thdxr 推文链接是孤证 ambiguous

## Related
- [[entities/sisyphus-agent]] / [[entities/hephaestus-agent]] — 核心 agents
- [[concepts/omo-ultrawork-mode]] — 单 keyword 触发
- [[concepts/omo-team-mode]] — v4.0 多 agent
- [[concepts/omo-hashline-edits]] — 防 stale-line error 的编辑工具
- [[concepts/omo-agent-category-routing]] — 4 category → model 自动选择
- [[concepts/omo-skill-embedded-mcps]] — skill 自带 MCP
- [[concepts/omo-intent-gate]] — 行动前分析意图
- [[concepts/omo-editions-ultimate-vs-light]] — 两版本对比
- [[skills/omo-install-and-setup]] — 安装流程
- [[references/omo-github-readme]] — README 索引
- [[references/omo-team-mode-config-schema]] — 11 字段 team_mode 配置
- `_raw/github-code-yeongyu-oh-my-openagent.txt` — 完整 gitingest 抓取（526 文件 / 1.1M tokens）
- [[synthesis/concepts-agent-team-cost-overhead × entities-oh-my-openagent|Agent Team 成本 × omo 编排器]] — synthesis
