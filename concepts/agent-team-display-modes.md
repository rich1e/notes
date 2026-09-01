---
title: "Agent Team 显示模式 5 选"
category: concepts
tags:
  - claude-code
  - ai-agents
  - tmux
  - iterm2
  - ux
  - concept
summary: "Claude Code Agent Teams 的 teammateMode 五种值：in-process / split-panes / auto / tmux / iterm2。CLI flag --teammate-mode 单次设置，与 settings.json 等效。"
sources:
  - "https://docs.claude.com/en/docs/claude-code/agent-teams"
    - "https://blog.csdn.net/qq_60735796/article/details/157912075"
created: "2026-08-05T04:30:00Z"
updated: "2026-08-13T01:40:00Z"
provenance:
  extracted: 0.92
  inferred: 0.06
  ambiguous: 0.02
base_confidence: 0.82
lifecycle: draft
lifecycle_changed: "2026-08-05"
tier: supporting
---

# Agent Team 显示模式 5 选

> Claude Code Agent Teams 提供了 **5 种 teammateMode** 控制 teammates 的可视化方式。settings.json 持久化或 `--teammate-mode` flag 单次设置。

## 5 种模式

| 模式 | 行为 | 依赖 |
|---|---|---|
| **`"in-process"`** | 所有 teammate 在主终端 agent panel；方向键 + Enter 进入 | 无 |
| **`"split-panes"`** | 每个 teammate 一个独立 pane | tmux 或 iTerm2 |
| **`"auto"`** | 在 tmux/iTerm2 内时自动用 split-pane，否则 in-process | tmux/iTerm2 |
| **`"tmux"`** | 强制 split-pane，tmux/iTerm2 自动检测 | tmux 或 iTerm2 |
| **`"iterm2"`** | 强制 iTerm2 native split-pane | iTerm2 + `it2` CLI |

**默认**: `"in-process"`（v2.1.179+；之前版本默认 `"auto"`）。

## 配置方式

### 持久化（settings.json）

```json
// ~/.claude/settings.json
{
  "teammateMode": "auto"
}
```

### 单次（CLI flag）

```bash
claude --teammate-mode auto
```

**注意**：flag 是实验性，**不显示**在 `claude --help` 输出里。

## 安装依赖

### tmux

```bash
# macOS
brew install tmux

# Linux
sudo apt install tmux
```

无需额外 settings，tmux 本身就够了。`which tmux` 能找到即可。

### iTerm2

1. 安装 `it2` CLI: `brew install mkusaka/it2/it2`（或从 GitHub release）
2. iTerm2 → **Settings → General → Magic → Enable Python API**

`"iterm2"` 模式如果 `it2` 缺失会**显式报错**并提示安装命令。

## 关键差异

| 维度 | in-process | split-pane |
|---|---|---|
| **可视化** | 单 terminal，agent panel | 多 pane 同时可见 |
| **交互** | 方向键选 + Enter / `x` / `Ctrl+T` / `Esc` | 点击 pane |
| **状态保留** | teammate 隐藏后保持 running | tmux pane 始终可见 |
| **平台支持** | 任何 terminal | 不支持 VS Code 集成 / Windows Terminal / Ghostty |
| **适用** | 单屏便携 | macOS + 大屏 |

## tmux 模式的 Pane 工作流（实战）

选 `"tmux"` 后 Claude Code 会自动为每个 Teammate 创建一个 pane。**3 个高频操作**：

| 操作 | 快捷键 | 用途 |
|---|---|---|
| **Zoom** | `Ctrl+B z` | 当前 pane 放大到全屏 → 再按一次恢复 |
| **Detach / Reattach** | `Ctrl+B d` / `tmux a -t <name>` | 让 Agent 在后台持续工作（关终端也不停） |
| **Scroll 历史** | `Ctrl+B [` → `PgUp/PgDn` → `q` 退出 | 查看 Teammate 的完整输出历史 |

**Lead 的 Delegate 模式**（防抢活）：在 Lead pane 中按 `Shift+Tab` 进入 Delegate 模式 — Lead 只能用协调工具，**不能自己写代码**，专注分配任务。

**CLAUDE.md 是 Teammate 的唯一上下文来源**（Teammate 不继承 Lead 的对话历史），所以项目级信息必须在 `CLAUDE.md` 里写清楚 — 包括文件分工（不同 Teammate 写不同文件，避免 git conflict）。

完整实战 skill（含 `.tmux.conf` 推荐配置、5 大故障排查、远程服务器场景）见 [[skills/tmux-agent-teams-pane-workflow]]。

## macOS 特别说明

> "`tmux` has known limitations on certain operating systems and traditionally works best on macOS. Using `tmux -CC` in iTerm2 is the suggested entrypoint into `tmux`."

→ iTerm2 + `tmux -CC` 是 macOS 上跑 tmux 的**官方推荐入口**，比直接 `tmux` 体验更好。

## in-process 模式的快捷键（官方）

| 键 | 行为 |
|---|---|
| `↑` / `↓` | 选择 teammate |
| `Enter` | 打开 teammate transcript，可直接发消息 |
| `x` | 停掉选中的 teammate |
| `Ctrl+T` | 切换 task list |
| `Esc` | 中断当前 turn |

## idle 行折叠规则（v2.1.199+）

- 整个 panel 都 idle 后 **30 秒**，idle 行折叠隐藏
- 下次 teammate turn 自动重现
- **>3 idle** 时折叠成 `N idle agents`，Enter 展开
- 工作中 / 失败 / 当前查看的 teammate **始终保留**独立行

## 已知限制

**split-pane 不支持**的 terminal：
- VS Code 集成终端
- Windows Terminal
- Ghostty

vs vault 已有 [[concepts/tmux-pane-split-for-agents]] 的判断"tmux 不在 VS Code/Cursor 工作"——**官方确认**且更广：split-pane 模式仅 tmux / iTerm2 native 支持。

## 与 vault 已有 tmux 知识的关系

vault 已有 6 个 tmux 概念页（gpakosz cluster）— **本模式系统**把它们统一到 Claude Code agent teams 场景：

| vault 已有 | 在 agent teams 里的角色 |
|---|---|
| [[concepts/tmux-pane-split-for-agents]] | 视频教程视角的 split-pane 配置 |
| [[concepts/tmux-pane-maximize-stateful]] | maximize 当前 working teammate pane |
| [[skills/tmux]] | tmux 通用速查 |
| [[entities/gpakosz-tmux]] | tmux 配置哲学 |

## Related

- [[concepts/claude-code-agent-teams]] — Agent Teams 总体
- [[concepts/tmux-pane-split-for-agents]] — 视频教程视角（与本官方版对比有字段差异）
- anthropic-claude-code-agent-teams-docs — 官方一手
- [[synthesis/concepts-agent-team-display-modes × entities-claude-code-agent-teams-feature|Agent Teams 显示模式 × Agent Teams 特性]] — synthesis(隔离域选择)