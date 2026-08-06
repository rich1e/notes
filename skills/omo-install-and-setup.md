---
title: "omo 安装与设置（让 LLM agent 帮你装）"
category: skills
tags:
  - omo
  - install
  - setup
  - llm-agent
  - skill
sources:
  - "https://github.com/code-yeongyu/oh-my-openagent"
created: "2026-08-05T07:30:00Z"
updated: "2026-08-05T07:30:00Z"
provenance:
  extracted: 0.90
  inferred: 0.06
  ambiguous: 0.04
base_confidence: 0.72
lifecycle: draft
lifecycle_changed: "2026-08-05"
tier: supporting
relationships:
  - target: "[[entities/oh-my-openagent]]"
    type: related_to
  - target: "[[concepts/omo-editions-ultimate-vs-light]]"
    type: related_to
---

# omo 安装与设置（让 LLM agent 帮你装）

> omo 安装**强烈建议让 LLM agent 帮你装**——Ultimate Edition 涉及 11 agent 模型选择 + per-provider 鉴权 + 订阅检测，人装易错。

## 官方建议

> "**Strongly recommended: let an LLM agent install this for you.** The Ultimate edition setup involves subscription detection, model selection across 11 agents, and per-provider authentication — humans fat-finger these. An LLM agent reads the full guide and walks every step correctly."

## Ultimate Edition 安装

```bash
# 推荐：让 agent 装
# 把这段贴到 Claude Code / AmpCode / Cursor 或任何 agent：
Install and configure oh-my-openagent by following the instructions here:
https://raw.githubusercontent.com/code-yeongyu/oh-my-openagent/refs/heads/dev/docs/guide/installation.md
```

```bash
# 手动（TUI 引导）
bunx oh-my-openagent install

# 两者都装
bunx oh-my-openagent install --platform=both
```

## Light Edition 安装

```bash
# 一行手动
npx lazycodex-ai install

# 非交互推荐（自动配 autonomous 权限）
npx lazycodex-ai install --no-tui --codex-autonomous
```

**Light Edition 不需要 Bun**——`npx` 走 Node/npm。

## Provider 鉴权

Ultimate Edition 涉及 **5 个 provider**：

- **Anthropic** —— Claude Code 订阅
- **OpenAI** —— ChatGPT 订阅
- **Gemini** —— Gemini API
- **Copilot** —— GitHub Copilot
- **Z.ai** —— GLM Coding Plan
- **OpenCode Zen** —— OpenCode 自带

每个 provider **API key / OAuth token** 都需要单独配。

## 推荐最低订阅（官方）

> "Even with only the following subscriptions, ultrawork works well"

- [ChatGPT Subscription ($20)](https://chatgpt.com/) — Hephaestus（GPT-5.6 Sol）
- [Kimi Code Subscription ($19)](https://www.kimi.com/code) — Sisyphus 默认 / GLM 备援
- [GLM Coding Plan ($10)](https://z.ai/subscribe) — Sisyphus fallback

**$49/月 vs Claude Code $200/月** → vault [[concepts/agent-team-cost-overhead]] 的实证。

## Telemetry

默认开——每天每机器最多 1 次事件，SHA256-hashed installation id，**不建 PostHog profile**。

```bash
# 关闭主插件
OMO_DISABLE_POSTHOG=1
OMO_SEND_ANONYMOUS_TELEMETRY=0

# 关闭 Codex Light
OMO_CODEX_DISABLE_POSTHOG=1
OMO_CODEX_SEND_ANONYMOUS_TELEMETRY=0
```

## 命名警告

| 命令 | 状态 |
|---|---|
| `bunx oh-my-openagent install` | ✓ 推荐 |
| `bunx oh-my-opencode install` | ✓ 旧名（仍可用） |
| `bunx omo install` | ✗ **不同作者的不同 npm 包**——package manager 可能解错 |

## 安装后第一步

```bash
ultrawork    # 或 ulw
```

打 `ultrawork`——Sisyphus 接管。

## 安装故障排查

| 症状 | 排查 |
|---|---|
| Team Mode `team_*` tools 不出现 | 看 `oh-my-opencode.log` 里的 config 加载路径 + `[tool-registry] Built tool registry` 条目（v4.2.1+ 加了 regression test） |
| 模型路由不到 | 确认 `team_mode.enabled` 与 model config 都到位 |
| `ultrawork` 无反应 | 确认 Light Edition 只识别关键词（完整 IntentGate 仅 Ultimate） |
| Telemetry 误关 | 检查 `OMO_DISABLE_POSTHOG` / `OMO_SEND_ANONYMOUS_TELEMETRY` 环境变量 |

## 与 vault 已有 skill 的关系

| vault 已有 | 在 omo 安装的特殊点 |
|---|---|
| [[skills/claude-code-settings]] | omo 安装涉及 11 agent 模型选择——比 Claude Code settings 更复杂 |
| [[skills/bmad-install-and-setup]] | 类似让 LLM agent 帮你装的策略 |
| [[concepts/mcp-server-protocol-quirks]] | Light Edition 走 plugin-scoped MCPs 避开全局坑 |
| [[concepts/claude-code-token-optimization]] | Skill-Embedded MCPs 直接落地 token 节流 |

## Related

- [[entities/oh-my-openagent]] — 框架本体
- [[concepts/omo-editions-ultimate-vs-light]] — 两个版本差异
- [[concepts/omo-ultrawork-mode]] — 装后第一步
- [[concepts/omo-skill-embedded-mcps]] — Skill-Embedded MCPs 是装后效果
- [[references/omo-github-readme]] — README 索引