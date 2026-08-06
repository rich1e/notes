---
title: "Anthropic Claude Code Agent Teams 官方文档"
category: sources
tags:
  - claude-code
  - ai-agents
  - anthropic
  - opus-4
  - source
sources:
  - "https://docs.claude.com/en/docs/claude-code/agent-teams"
source_url: "https://docs.claude.com/en/docs/claude-code/agent-teams"
created: "2026-08-05T04:30:00Z"
updated: "2026-08-05T04:30:00Z"
summary: "Anthropic 官方文档（v2.1.178+）：Agent Teams 实验性功能架构、teammateMode 五种显示模式、3 个 hook 事件、Mailbox JSON 协议、TaskList 文件锁防 race、9 项已知限制。"
provenance:
  extracted: 0.92
  inferred: 0.05
  ambiguous: 0.03
base_confidence: 0.92
lifecycle: reviewed
lifecycle_changed: "2026-08-05"
tier: core
---

# Anthropic Claude Code Agent Teams 官方文档

> 本页是 [[synthesis/Research: Claude Code Agent Teams]] 的**首要一手来源**。Anthropic 官方 v2.1.178+ 文档页面（`docs.claude.com/en/docs/claude-code/agent-teams`）。

## 文档基本信息

- **URL**: https://docs.claude.com/en/docs/claude-code/agent-teams
- **作者**: Anthropic（Claude Code 团队）
- **覆盖版本**: v2.1.178 及以上（页面明确"this page describes agent teams as of v2.1.178"）
- **状态**: Experimental / Disabled by default
- **相关子页**: `docs.claude.com/en/docs/claude-code/sub-agents`、`docs.claude.com/en/docs/claude-code/worktrees`、`docs.claude.com/en/docs/claude-code/model-config`、`docs.claude.com/en/docs/claude-code/hooks`、`docs.claude.com/en/docs/claude-code/permissions`、`docs.claude.com/en/docs/claude-code/costs#agent-team-token-costs`

## 启用方式（官方）

环境变量 / settings.json `env` 块：

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

**默认值**：关闭。不设这个环境变量，session 启动时不会创建 team 目录、不 spawn teammates。

> **修正**：YouTube 教程 [[misc/web-youtube-com-watch-v-cskoa-ccmq0w]] 提到的 `experimentalAgents: "on"` 是错的——这是**环境变量**而非 camelCase settings 字段。[[misc/web-youtube-com-watch-v-cskoa-ccmq0w]] 的两个 Open Questions 之一（O5）已通过本官方文档明确否定。

## 架构 4 组件

| 组件 | 角色 |
|---|---|
| **Team lead** | 主 Claude Code session，spawn teammates + 协调 |
| **Teammates** | 独立 Claude Code 实例，各自有 context window |
| **Task list** | 共享任务列表，teammates 认领/完成 |
| **Mailbox** | 队友间直接消息系统（JSON 文件） |

**关键差异**（vs subagents）：subagents 只向主 agent 单向汇报；agent teams 里 teammate 间**直接互相通信**（不必经 lead）。也可以**直接**与任一 teammate 交互（in-process 模式下方向键选 + Enter；split-pane 模式下点击 pane）。

## 文件位置（v2.1.178+）

- **Team config**（运行时状态，session 结束删）: `~/.claude/teams/{team-name}/config.json`
  - 含 session IDs / tmux pane IDs —— **不要手动编辑**，下次状态更新会被覆盖
- **Task list**（持久保留，遵循 `cleanupPeriodDays`）: `~/.claude/tasks/{team-name}/`
- **Mailbox**（每个 agent 一个 JSON）: `~/.claude/teams/{team-name}/inboxes/{agent-name}.json`
  - 文件被读时**逐条校验**：不合法条目被丢弃并报错，合法消息继续投递
  - **v2.1.207 前** 单条 malformed 会让整个 mailbox 每秒报错，需手动删文件

Team 名称 = `session-` + session ID 前 8 字符，**自动生成**，无需 `TeamCreate`。

> **修正**：YouTube 教程 + 几篇 CSDN 文章都说要 `TeamCreate` 工具建队、命名——**v2.1.178 后这工具不存在了**。spawn 第一个 teammate 时自动建队，session 结束自动清理。

## 显示模式 5 种

`teammateMode` setting（`~/.claude/settings.json`）：

| 模式 | 行为 |
|---|---|
| `"in-process"` | **默认**——所有 teammate 在主终端 agent panel，方向键切换 + Enter 进入 |
| `"split-panes"` | 每个 teammate 一个独立 pane（tmux 或 iTerm2） |
| `"auto"` | 在 tmux/iTerm2 内时自动用 split-pane，否则 in-process |
| `"tmux"` | 强制 split-pane，tmux/iTerm2 自动检测 |
| `"iterm2"` | 强制 iTerm2 native split-pane（需 `it2` CLI + Python API 启用） |

**CLI flag**：单次设置 `--teammate-mode auto`（实验性，不在 `claude --help` 里）。

**快捷键（in-process）**：方向键选、Enter 看 transcript、`x` 停、`Ctrl+T` 切 task list、`Esc` 中断当前 turn。

**idle 行折叠规则**（v2.1.199+）：整个 panel 都 idle 后 30 秒，idle 行折叠隐藏；下次 turn 自动重现。>3 idle 时折叠成 `N idle agents`，Enter 展开。

> **修正**：YouTube 教程 [[misc/web-youtube-com-watch-v-cskoa-ccmq0w]] 提到的 `tmux.splitPanes: true` settings 字段是**错的**——官方字段是 `teammateMode` 字符串。tmux 本身**不需要 settings 配置**，只需要 `which tmux` 能找到即可。

## 任务管理 3 状态 + 2 模式 + file lock

**3 状态**: pending → in progress → completed
**依赖**: 有未完成依赖的 pending 任务**不能被认领**

**2 种 assignment 模式**:
- **Lead assigns**（"把 X 任务给 Y teammate"）
- **Self-claim**（teammate 完成当前任务后自动认领下一个未分配未阻塞的任务）

**Race condition 防扣**（官方原话）：

> "Task claiming uses file locking to prevent race conditions when multiple teammates try to claim the same task simultaneously."

这与 YouTube 教程"race-condition task lock"描述吻合——但**实现机制是文件系统锁**而非 Anthropic 内部调度。

> **延伸**：把 [[concepts/deterministic-agent-memory]] 的"同 query 同答案 / 失败显式分桶"哲学从"静态查询"扩到"动态调度"——task claim file lock = "一次只一个 teammate 能 claim"。

## Hooks（3 个新事件）

| Hook | 触发 | 退出码 2 的效果 |
|---|---|---|
| `TeammateIdle` | teammate 即将 idle | 给反馈让 teammate 继续工作 |
| `TaskCreated` | 任务正在被创建 | 阻止创建 + 给反馈 |
| `TaskCompleted` | 任务正在被标 completed | 阻止完成 + 给反馈 |

把 agent teams 与现有 [[concepts/claude-code-hooks-lifecycle]] 体系缝起来——这是 vault hook 知识簇的天然扩展点。

## Plan approval（复杂/危险任务的安全闸）

可在 spawn 时要求 teammate **先 plan 不实现**（read-only plan mode）。teammate plan 完成后发请求给 lead，lead 自动批准或拒绝并给反馈。

**设计意图**：lead 的批准决策自主，但你**可影响**：在 spawn prompt 里给标准（如"only approve plans that include test coverage"）。

## Permissions（共享 lead 模式）

- spawn 时**不能**给 teammate 设独立 mode——它们继承 lead 的 mode
- spawn 后**可以**单独改某个 teammate 的 mode
- **lead 用 `--dangerously-skip-permissions`** → 所有 teammate 也都跳过
- teammate 间 `SendMessage` 通知"消息来自另一个 Claude session"，**不是**用户授权
- teammate 不能替你批准权限提示；自动模式（auto）下 relay 的 approval claim 被视为不可信输入

## Token cost（核心权衡）

官方原话：

> "Agent teams use significantly more tokens than a single session. Each teammate has its own context window, and token usage scales with the number of active teammates."

> "Each teammate has its own context window and consumes tokens independently."

**对比**：
- **Subagents**: result summarized back to main context（low cost）
- **Agent teams**: each teammate is a separate Claude instance（high cost）

**官方建议团队规模**：3-5 个 teammate（平衡并行 + 可控协调）。"5-6 tasks per teammate" 保持高效。15 个独立任务用 3 个 teammate 起步——>3 会协调爆炸。

> **修正**：YouTube 教程里"$1.15 跑 4 agent research"暗示 5 agent 仍是廉价——官方明确说**线性扩展**，5 teammate ≈ 5x cost。YouTube 例子可能仅算主 lead 时长（dashboard bug）。

## 9 项已知限制

| # | 限制 | 影响 |
|---|---|---|
| 1 | **No session resumption** with in-process teammates | `/resume` `/rewind` 后 lead 试图联系已不存在的 teammates |
| 2 | **Task status can lag** | teammates 有时不标 completed，依赖任务卡住 |
| 3 | **Shutdown can be slow** | teammates 等当前请求/tool 完成才退 |
| 4 | **One team per session** | 不能跨 session 共享 team |
| 5 | **No nested teams** | teammates 不能 spawn own teammates |
| 6 | **No background subagents from in-process teammates** | teammate 不能跑后台 subagent（它会随 lead 进程死） |
| 7 | **Lead is fixed** | 不能 promote teammate 为 lead |
| 8 | **Permissions set at spawn** | 不能 spawn 时给独立 mode |
| 9 | **Split panes require tmux or iTerm2** | 不支持 VS Code 集成终端 / Windows Terminal / Ghostty |

**好消息**：`CLAUDE.md` 在 agent teams 里**正常工作**——每个 teammate 都读自己 CWD 的 CLAUDE.md。这是把 [[concepts/agent-operating-system]] Handoff 层延伸到 agent teams 的核心机制。

## 4 类典型用例（官方推荐）

1. **Research and review**（多角度并行）
2. **New modules or features**（独立模块分别认领）
3. **Debugging with competing hypotheses**（对抗式假设测试）
4. **Cross-layer coordination**（前后端 + 测试各归一个 teammate）

**反例（不要用）**：sequential tasks / same-file edits / many dependencies——subagent 或单 session 更划算。

## 关键引语

> "Sequential investigation suffers from anchoring: once one theory is explored, subsequent investigation is biased toward it."

> "With multiple independent investigators actively trying to disprove each other, the theory that survives is much more likely to be the actual root cause."

→ **5-agent 互驳式 debug** 是这个特性的杀手场景。

## Open Questions（本官方文档仍留白）

- "agent team token costs" 子页（`docs.claude.com/en/docs/claude-code/costs#agent-team-token-costs`）未在本页展开，需单独 fetch
- 各 teammate 模型的精确 token 报价（200K vs 1M context vs premium tier）未给具体数字
- "effort 切换"在 v2.1.186+ 才在 split-pane mode 生效，更早版本 teammate 不继承 lead effort

## Related

- [[synthesis/Research: Claude Code Agent Teams]] — 综合分析
- [[misc/web-youtube-com-watch-v-cskoa-ccmq0w]] — 22 分钟视频教程（Opus 4.6 引入 Agent Teams），与本官方文档**多处矛盾**，已在每个矛盾处显式标注修正
- [[concepts/claude-code-agent-teams]] — 工程机制概念页（同步更新以官方文档为准）
- [[concepts/claude-code-three-modes]] — 三模式抽象
- [[concepts/tmux-pane-split-for-agents]] — tmux 配置（同步更新字段名）
- [[entities/claude-code]] — 主体工具
- [[concepts/claude-code-hooks-lifecycle]] — 与新 3 个 hooks 事件同源
- [[concepts/deterministic-agent-memory]] — race lock 是其"动态调度"延伸