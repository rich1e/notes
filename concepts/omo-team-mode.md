---
title: "omo Team Mode（v4.0 lead + 8 members）"
category: concepts
tags:
  - omo
  - team-mode
  - claude-code-agent-teams
  - tmux
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
  - target: "[[concepts/agent-team-display-modes]]"
    type: extends
  - target: "[[concepts/agent-team-mailbox-protocol]]"
    type: extends
  - target: "[[concepts/claude-code-agent-teams]]"
    type: derived_from
  - target: "[[references/omo-team-mode-config-schema]]"
    type: related_to
summary: "omo Team Mode v4.0：lead agent + 最多 8 members + tmux 可视化，11 字段严格 resource cap（max_parallel_members=4 / max_wall_clock_minutes=120 等），比 Claude Code Agent Teams 更严格。"
---

# omo Team Mode（v4.0 lead + 8 members）

> omo **Team Mode**（v4.0）= 一个 lead agent + 最多 8 个并行 members + 12 个 `team_*` 工具 + tmux 可视化。**off by default**——按需启用。直接借鉴 Claude Code Agent Teams 但加了 omo 的工作流生态。

## 启用

JSONC 配置（`~/.omo/omo.jsonc` user 或 `.omo/omo.jsonc` project）：

```jsonc
{
  "team_mode": {
    "enabled": true,
    "max_parallel_members": 4,
    "max_members": 8,
    "tmux_visualization": true
  }
}
```

重启 opencode 后，**12 个 `team_*` 工具**解锁。

## 11 字段 Config Schema

详见 [[references/omo-team-mode-config-schema]]：

| 字段 | 类型 | 默认 |
|---|---|---|
| `enabled` | boolean | `false` |
| `tmux_visualization` | boolean | `false` |
| `max_parallel_members` | int 1..8 | 4 |
| `max_members` | int 1..8 | 8 |
| `max_messages_per_run` | int ≥1 | 10000 |
| `max_wall_clock_minutes` | int ≥1 | 120 |
| `max_member_turns` | int ≥1 | 500 |
| `base_dir` | optional string | `~/.omo` |
| `message_payload_max_bytes` | int ≥1024 | 32768 |
| `recipient_unread_max_bytes` | int ≥1024 | 262144 |
| `mailbox_poll_interval_ms` | int ≥500 | 3000 |

**特点**：

- `max_parallel_members` (4) < `max_members` (8)——可同时间跑 ≤4，team 总规模 ≤8
- 严格上限（resource cap 思维）——避免失控
- `base_dir` 显式配置 mailbox / task list 位置
- `mailbox_poll_interval_ms` = 3000（3 秒一次轮询）

## 何时用

> "Parallel exploration with bounded coordination. Long-running multi-step refactors split across specialised agents. Research + implementation pipelines that need shared task lists."

| 场景 | 适用 |
|---|---|
| **并行探索 + 有界协调** | ✓ |
| **长时间多步重构** 跨 specialists | ✓ |
| **研究 + 实施 pipeline** 需共享 task list | ✓ |
| **单文件 typo** | ✗ 用 Quick Mode |
| **深度单 agent 研究** | ✗ 用 Hephaestus |

## v4.2.1 修复

> "Bug-fix note: v4.2.1 adds a fresh-install regression test for this minimal config and logs the resolved `team_mode` state plus team tool count during startup. If the tools still do not appear after restart, inspect `oh-my-opencode.log` for the loaded config path and `[tool-registry] Built tool registry` entry."

**遇到 team_* tools 不出现的排查路径**：检查 `oh-my-opencode.log` 里的 config 加载路径 + `[tool-registry] Built tool registry` 条目。

## Team Spec 位置

```
~/.omo/teams/{name}/config.json          # user scope
<project>/.omo/teams/{name}/config.json # project scope
```

```json
{
  "name": "ccapi-explorers",
  "description": "Explore the ccapi project structure.",
  "lead": { "kind": "subagent_type", "subagent_type": "sisyphus" },
  ...
}
```

## 上层 Skill

Team Mode 解锁后，**两个 skill** 已经搭好：

| Skill | 配置 |
|---|---|
| **`hyperplan`** | 5 hostile agents 拆 plan（正交视角） |
| **`security-research`** | 3 vulnerability hunters + 2 PoC engineers 并行审计，按 *actual exploitability* 校准 severity |

## 与 Claude Code Agent Teams 的关系

| 维度 | Claude Code Agent Teams | omo Team Mode |
|---|---|---|
| 启用 | `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` | `team_mode.enabled: true` |
| teammates | 每个独立 Claude session | omo discipline agent |
| 通信 | Mailbox JSON | Mailbox（`base_dir` + `mailbox_poll_interval_ms`） |
| 显示 | 5 种 teammateMode | `tmux_visualization` boolean |
| Task claim | File lock | 推测相同机制 ambiguous |
| 上层 skill | （无官方） | `hyperplan` / `security-research` |

**omo Team Mode = Claude Code Agent Teams 的 omo 封装 + 上层 skill 生态**。

## 13 vs 12 个 `team_*` Tools

omo 提供 **12 个** `team_*` 工具（README 提到但未列全部名字）：

- `team_create`（建 team）
- `team_send_message`（成员间通信）
- `team_task_create`（建任务）
- `team_status`（查询状态）

加 `team_*` 前缀的其他工具共 12 个。

## 与 vault 已有概念的关系

| vault 已有 | 在 omo Team Mode 中的体现 |
|---|---|
| [[entities/claude-code-agent-teams-feature]] | 直接借鉴但加上层 skill 生态 |
| [[concepts/agent-team-display-modes]] | `tmux_visualization` 是 teammateMode 的子集 |
| [[concepts/agent-team-mailbox-protocol]] | `base_dir` + `mailbox_poll_interval_ms` 是具体实现 |
| [[concepts/agent-team-race-condition-task-claim]] | 应该用 file lock，但 README 未明 inferred |
| [[concepts/agent-team-cost-overhead]] | 11 字段严格上限是 token 节流的具体措施 |

## Open Questions

- 12 个 `team_*` 工具的**完整清单**——README 只列 4 个
- Team Mode 与 [[entities/claude-code-agent-teams-feature]] 的**差异点**——omo 文档没说哪些是独有功能 ambiguous
- Team Mode 与 **Hephaestus 单独调用** 怎么选？team 是为多 specialists + tmux 可视化场景的

## Related

- [[entities/oh-my-openagent]] — 框架本体
- [[concepts/omo-ultrawork-mode]] — 单 keyword 触发
- [[concepts/omo-discipline-agents]] — 5 disciplines 是 team 的构建块
- [[concepts/claude-code-agent-teams]] — 直接借鉴
- [[references/omo-team-mode-config-schema]] — 11 字段详解