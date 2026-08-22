---
title: "Tmux Split-Pane 给 AI Agent 团队"
category: concepts
tags:
  - tmux
  - claude-code
  - ai-agents
  - workflow
summary: "在 Claude Code Agent Teams 场景下用 tmux split-pane：每个 teammate 一个独立 pane + teammateMode=tmux 配置 + 启动顺序强制 + 与 gpakosz .local 覆写模式兼容。"
sources:
  - "https://www.youtube.com/watch?v=cSkoaCCmq0w"
  - "https://docs.claude.com/en/docs/claude-code/agent-teams"
created: "2026-08-05T03:30:00Z"
updated: "2026-08-05T04:30:00Z"
provenance:
  extracted: 0.85
  inferred: 0.10
  ambiguous: 0.05
base_confidence: 0.72
lifecycle: draft
lifecycle_changed: "2026-08-05"
tier: supporting
relationships:
  - target: "[[concepts/agent-team-display-modes]]"
    type: derived_from
  - target: "[[sources/anthropic-claude-code-agent-teams-docs]]"
    type: derived_from
---

# Tmux Split-Pane 给 AI Agent 团队

> Agent Teams（Claude Code Opus 4.6+ 多会话模式）默认所有 teammate 在**同一个终端**互相喊话——视频原话："5 个 agent 在同一房间互相喊话，根本没法看谁在做什么"。**tmux split-pane 是 5 种显示模式之一**：每个 teammate 一个 pane，可独立 inspect、interact、shutdown。详见 [[concepts/agent-team-display-modes]]；实战 skill（pane 操作 / CLAUDE.md 共享上下文 / Delegate 模式 / 5 大故障排查）见 [[skills/tmux-agent-teams-pane-workflow]]。

## 强制启动顺序

```
# 错的：直接开 claude，5 个 teammate 挤在同终端
claude --dangerously-skip-permissions

# 对的：先 tmux（分配房间），再 claude
tmux
claude --dangerously-skip-permissions
```

**不能在 VS Code / Cursor 集成终端使用**——必须原生 terminal（官方明确 split-pane 不支持 VS Code 集成 / Windows Terminal / Ghostty）。

## settings.json 全局配置（官方修正版）

官方 `teammateMode` setting（`~/.claude/settings.json`）5 种值：

```jsonc
// ~/.claude/settings.json
{
  "teammateMode": "tmux"  // 强制 split-pane，tmux/iTerm2 自动检测
}
```

| 字段值 | 行为 |
|---|---|
| `"in-process"` | **默认**——所有 teammate 在主终端 agent panel |
| `"split-panes"` | 强制 split-pane（tmux 或 iTerm2） |
| `"auto"` | 在 tmux/iTerm2 内时自动 split-pane，否则 in-process |
| `"tmux"` | 强制 split-pane，tmux/iTerm2 自动检测 |
| `"iterm2"` | 强制 iTerm2 native（需 `it2` CLI） |

CLI 单次设置：`claude --teammate-mode tmux`（实验性，不在 `claude --help` 里）。

> **修正视频教程**：[[misc/web-youtube-com-watch-v-cskoa-ccmq0w]] 提到的 `tmux.splitPanes: true` settings 字段是**错的**——官方只接受 `teammateMode` 字符串。tmux 本身**不需要 settings 配置**，`which tmux` 能找到即可。

视频推荐**全局**而非项目级（避免每次新 session 改配置）：

```jsonc
// ~/.claude/settings.json
{
  "tmux.splitPanes": true,
  "experimentalAgents": "on"
}
```

| 字段 | 作用 |
|---|---|
| `tmux.splitPanes` | 启用 tmux pane 自动分配（Agent Teams 必备） |
| `experimentalAgents` | 等价勾选 Agent Teams 功能开关 |

与 [[concepts/mcp-server-protocol-quirks]] 的"默认项目级"陷阱对照——这里**显式选全局**是 Agent Teams 的"少踩坑"决策。

## 与 gpakosz .local 覆写兼容

如果你已在用 [[entities/gpakosz-tmux]] 配置（双 prefix、`.tmux.conf.local` 用户层）：

- **双 prefix 不冲突** —— Agent Teams 不强制某 prefix
- **`.local` 用户层可加 Agent Teams 友好设置**：
  ```bash
  # ~/.tmux.conf.local
  # Agent Teams pane title prefix
  set -g pane-border-format "#{pane_title}"
  set -g pane-border-status top
  ```
  让每个 agent pane 显示自己的 agent 名（"research / bull-case / bear-case / QA"）

## 替代方案：Zellij

[[skills/zellij-terminal-multiplexer]] 也有 split-pane + YAML 布局文件，理论上也兼容 Agent Teams——但视频未实测，且 Zellij 不在 Claude Code 官方推荐列表。**判断**：tmux 是更稳的选择。

## pane 操作快捷键

| 操作 | 快捷键 |
|---|---|
| 横向 split | `PREFIX "` |
| 纵向 split | `PREFIX %` |
| pane 间切换 | `PREFIX o`（或 `PREFIX 方向键`） |
| 关闭 pane | `PREFIX x` |
| maximize 当前 pane | `PREFIX +`（gpakosz 增强版，跨 window 仍可继续 split） |

最大化 pane 后与 Agent Teams 配合尤其爽：聚焦当前在干活的 agent，其他 pane 折叠。

## 工程坑

- **Panes 太多反而看不清**：视频建议 4-5 个 agent 上限，超过就要拆 team
- **Agent 死后 pane 不自动关**：手动 `PREFIX x` 关闭（graceful shutdown 后 team leader 会自动关大部分，但保留 idle 的仍占 pane）
- **跨 pane 不能直接复制**：要看 agent 输出只能 `PREFIX o` 跳过去或截图发回 GPT/Claude 二次解读

## Related

- [[misc/web-youtube-com-watch-v-cskoa-ccmq0w]] — 视频源
- [[concepts/claude-code-agent-teams]] — Agent Teams 工程机制
- [[concepts/claude-code-three-modes]] — 三模式对照
- [[skills/tmux]] — 通用 tmux 速查
- [[entities/gpakosz-tmux]] — gpakosz 配置哲学；本文用其 `.local` 用户层扩展
- [[concepts/tmux-pane-maximize-stateful]] — pane maximize 与 Agent Teams 配合
- [[skills/zellij-terminal-multiplexer]] — 替代复用器