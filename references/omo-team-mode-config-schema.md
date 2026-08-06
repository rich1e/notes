---
title: "omo Team Mode 11 字段配置 Schema"
category: references
tags:
  - omo
  - team-mode
  - config-schema
  - jsonc
  - reference
sources:
  - "https://github.com/code-yeongyu/oh-my-openagent"
source_url: "https://github.com/code-yeongyu/oh-my-openagent/blob/dev/docs/guide/team-mode.md"
created: "2026-08-05T07:30:00Z"
updated: "2026-08-05T07:30:00Z"
summary: "omo Team Mode `team_mode` 配置 11 字段详细：enabled / tmux_visualization / max_parallel_members / max_members / max_messages_per_run / max_wall_clock_minutes / max_member_turns / base_dir / message_payload_max_bytes / recipient_unread_max_bytes / mailbox_poll_interval_ms。"
provenance:
  extracted: 0.95
  inferred: 0.03
  ambiguous: 0.02
base_confidence: 0.88
lifecycle: reviewed
lifecycle_changed: "2026-08-05"
tier: supporting
relationships:
  - target: "[[concepts/omo-team-mode]]"
    type: derived_from
  - target: "[[entities/oh-my-openagent]]"
    type: related_to
---

# omo Team Mode 11 字段配置 Schema

> 完整 schema 来自 [[concepts/omo-team-mode]] 的 11 字段 `team_mode` 配置。所有字段住在 `~/.omo/omo.jsonc`（user）或 `.omo/omo.jsonc`（project）的 `team_mode` 块下。

## 完整配置示例

```jsonc
{
  "team_mode": {
    "enabled": true,
    "max_parallel_members": 4,
    "max_members": 8,
    "max_messages_per_run": 10000,
    "max_wall_clock_minutes": 120,
    "max_member_turns": 500,
    "base_dir": "~/.omo",
    "message_payload_max_bytes": 32768,
    "recipient_unread_max_bytes": 262144,
    "mailbox_poll_interval_ms": 3000,
    "tmux_visualization": false
  }
}
```

## 11 字段详解

| # | 字段 | 类型 | 默认 | 范围 | 作用 |
|---|---|---|---|---|---|
| 1 | `enabled` | boolean | `false` | - | Team Mode 主开关 |
| 2 | `tmux_visualization` | boolean | `false` | - | tmux pane 可视化 |
| 3 | `max_parallel_members` | int | `4` | 1..8 | 同时并行跑的 members 上限 |
| 4 | `max_members` | int | `8` | 1..8 | team 总成员上限 |
| 5 | `max_messages_per_run` | int | `10000` | ≥1 | 一次 run 消息数上限 |
| 6 | `max_wall_clock_minutes` | int | `120` | ≥1 | 总运行时间上限（分钟） |
| 7 | `max_member_turns` | int | `500` | ≥1 | 单 member turn 数上限 |
| 8 | `base_dir` | string (optional) | `~/.omo` | - | mailbox / task list 根目录 |
| 9 | `message_payload_max_bytes` | int | `32768` | ≥1024 | 单条消息大小上限 |
| 10 | `recipient_unread_max_bytes` | int | `262144` | ≥1024 | 收件人未读累积上限 |
| 11 | `mailbox_poll_interval_ms` | int | `3000` | ≥500 | mailbox 轮询间隔（毫秒） |

## 关键设计

### 双层并发上限

- `max_parallel_members` (4) **<** `max_members` (8)
- 可同时间跑 ≤4 个 member
- team 总规模可达 8 个 member
- 设计意图：避免 8 个 agent 同时跑失控

### 严格 resource cap 思维

每个字段都有**硬上限**：

- 时间：`max_wall_clock_minutes` = 120（2 小时）
- turn：`max_member_turns` = 500
- 消息：`max_messages_per_run` = 10000
- 字节：`message_payload_max_bytes` = 32KB、`recipient_unread_max_bytes` = 256KB
- 间隔：`mailbox_poll_interval_ms` ≥ 500

**防止 agent team 失控消耗资源**——与 vault [[concepts/agent-team-cost-overhead]] 的"linear scaling token 成本"对应。

### base_dir 显式

`base_dir` 不只影响 mailbox——也影响 team config / task list。默认值 `~/.omo` 解析为 user home 下的隐藏目录。

```bash
# user scope
~/.omo/teams/{name}/config.json
~/.omo/tasks/{name}/

# project scope（覆盖 base_dir）
<project>/.omo/teams/{name}/config.json
<project>/.omo/tasks/{name}/
```

## 与 Claude Code Agent Teams 的对比

| 维度 | Claude Code | omo Team Mode |
|---|---|---|
| 启用 | env var | boolean field |
| 并发上限 | 无硬上限（仅 9 限制） | `max_parallel_members` (4) + `max_members` (8) |
| 时间上限 | 无 | `max_wall_clock_minutes` (120) |
| 轮询间隔 | 无显式 | `mailbox_poll_interval_ms` (3000) |
| 消息大小 | 无 | `message_payload_max_bytes` (32KB) |

omo 的 **resource cap 比 Claude Code 严格**——直接可配。

## v4.2.1 修复

> "Bug-fix note: v4.2.1 adds a fresh-install regression test for this minimal config and logs the resolved `team_mode` state plus team tool count during startup."

如果 team_* tools 不出现，**v4.2.1+ 应有 startup log**：

- 看 `oh-my-opencode.log` 里的 config 加载路径
- 找 `[tool-registry] Built tool registry` 条目

## 配置层级

| 层级 | 路径 | 用途 |
|---|---|---|
| User | `~/.omo/omo.jsonc` | 用户级全局配置 |
| Project | `.omo/omo.jsonc` | 项目级覆盖 |

**两层切分**与 vault [[concepts/mcp-server-protocol-quirks]] 的 `-s user` / 默认项目级同源。

## 最小启用配置

```jsonc
{
  "team_mode": {
    "enabled": true,
    "max_parallel_members": 4,
    "max_members": 8,
    "tmux_visualization": false
  }
}
```

其他字段用默认值即可启用。

## 与 vault 已有概念的关系

| vault 已有 | 在 11 字段中的体现 |
|---|---|
| [[concepts/agent-team-cost-overhead]] | 严格 resource cap 防止 linear scaling 失控 |
| [[concepts/agent-team-mailbox-protocol]] | `base_dir` + `mailbox_poll_interval_ms` 是具体实现 |
| [[concepts/mcp-server-protocol-quirks]] | user / project 两层配置切分 |
| [[concepts/agent-team-display-modes]] | `tmux_visualization` 是 5 种显示模式之一 |

## Related

- [[concepts/omo-team-mode]] — 概念级 + 工作流
- [[entities/oh-my-openagent]] — 框架本体
- [[references/omo-github-readme]] — README 索引