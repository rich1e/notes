---
title: "BMad Party Mode 四种模式"
category: concepts
tags:
  - bmad-method
  - multi-agent
  - mode
  - concept
summary: "BMad Party Mode 4 种运行模式：session（单模型内联）/ auto（按需 spawn）/ subagent（每 round spawn）/ agent-team（持久 team）。区别在『谁在思考』——独立模型 vs 同一模型。"
sources:
  - "https://github.com/bmad-code-org/bmad-method"
created: "2026-08-05T07:00:00Z"
updated: "2026-08-05T07:00:00Z"
provenance:
  extracted: 0.92
  inferred: 0.06
  ambiguous: 0.02
base_confidence: 0.75
lifecycle: draft
lifecycle_changed: "2026-08-05"
tier: supporting
relationships:
  - target: "[[entities/bmad-party-mode]]"
    type: related_to
  - target: "[[concepts/claude-code-three-modes]]"
    type: related_to
  - target: "[[concepts/claude-code-agent-teams]]"
    type: related_to
  - target: "[[concepts/agent-team-mailbox-protocol]]"
    type: related_to
---

# BMad Party Mode 四种模式

> Party Mode 有 4 种运行模式——**每 session 选一种**，决定"**谁在思考**"：一个模型 voicing 所有人，还是分开的 agent 独立推理。

## 4 种模式对照

| Mode | 行为 | 何时用它 |
|---|---|---|
| **`session`** | 默认。**一个模型** inline voicing 每个 persona。快、完全对话式。 | 多数对话——banter / brainstorming / 快速来回。 |
| **`auto`** | 轻量 round inline voicing；**只在独立性会改变答案时** spawn 独立 agent。 | 多数时候要速度，但硬 round 要真独立。 |
| **`subagent`** | 每个实质 round 给每个 persona spawn 一个**分开 agent**——单 mind 不染色全部。 | 诚实 review / focus group，voice 不能互相渗透。 |
| **`agent-team`** | 让 personas 作为**持久 team** 互相直接 address。**仅 Claude Code**。 | 活生生的 hands-off 圆桌，agent 之间相互交谈。 |

## 为什么选择重要

> "The choice matters because one model voicing five personas can quietly converge: they share a mind."

**一个模型 voicing 5 personas 会悄悄收敛**——它们共享 mind。Spawn 真 agent 让推理独立，这正是 review panel 或 focus group 的**全部意义**。

- `session` —— 最便宜、最流畅
- spawn 模式 —— 更贵但**保护独立性**
- `auto` —— 试图兼得，只在 round 需要时 spawn

## 降级链

`session` 是默认，**其他模式在 harness 不支持时降级到 session**：

```
agent-team → subagent → session
```

每个模式依次降级到下一个更轻量的模式直到 `session`。Configured 默认存你的 customization 里，runtime override 单 session 赢。

```bash
/bmad-party-mode --mode subagent    # 单次 override 默认
/bmad-party-mode --mode auto
/bmad-party-mode --mode agent-team
/bmad-party-mode --mode session
```

## 与 Claude Code Agent Teams 的对应

| Party Mode | 对应 Claude Code 模式 |
|---|---|
| `session` | 单 LLM 模型多 persona 内联 |
| `auto` | 按需 spawn（BMad 自实现，未必完全对应 Claude Code 内置模式） |
| `subagent` | Claude Code **Subagent**（1 主 + N 短命子） |
| `agent-team` | Claude Code **Agent Teams**（1 leader + N 独立长会话） |

**关键约束**：`agent-team` **仅 Claude Code**——其他 IDE（如 Cursor / Codex）跑不了。`subagent` 模式是更广泛的 fallback。

## 通信机制

不同模式对应不同通信通道：

- `session` —— 单模型内部推理
- `auto` —— 混合：轻 round 用 session，硬 round 切换到 subagent spawn
- `subagent` —— **Mailbox IPC**（subagent 回主 session）
- `agent-team` —— **Mailbox IPC**（teammate 间**直接**通信，不需要经 lead）

详见 [[concepts/agent-team-mailbox-protocol]]。

## v6.10 fix：Agent-team sync 改成点对点

> "Claude Code Agent Teams communicate mailbox-style, not over a shared broadcast channel, so an idle member doesn't see exchanges it isn't addressed in. Docs updated so the lead relays turns; subagent mode, which is genuinely broadcast, is unchanged."

修正前 Party Mode `agent-team` 模式错误把 mailbox 当广播 channel——idle member 会看到它没被 address 的交流。**修正**：lead relays turns；`subagent` 是真广播不变。

这是 [[concepts/agent-team-mailbox-protocol]] "每个 agent 一个 JSON inbox" 设计哲学的**应用陷阱**——错误理解为 broadcast channel 会让 idle member 受干扰。

## 与 vault 已有概念的关系

| vault 已有 | Party Mode 4 模式对应 |
|---|---|
| [[concepts/claude-code-three-modes]] | 4 模式与 Default / Subagents / Agent Teams 直接对应 |
| [[concepts/claude-code-agent-teams]] | `agent-team` 模式 = Claude Code Agent Teams |
| [[concepts/agent-team-display-modes]] | Party Mode `subagent` / `agent-team` 都依赖 Claude Code 5 种显示模式 |
| [[concepts/agent-team-cost-overhead]] | spawn 模式成本更高——`session` 是最便宜的 |
| [[entities/claude-code-agent-teams-feature]] | Party Mode 是 Agent Teams 能力的"产品化封装" |

## 模式选择决策树

```
需要真独立性 / 防收敛？
├── 否（banter / brainstorming）→ session（最便宜）
├── 部分（多数轻量，少数要独立）→ auto（按需）
└── 是（诚实 review / focus group）
    ├── Claude Code 可用 → agent-team（持久 team）
    └── 跨 IDE → subagent（每 round spawn）
```

## Related

- [[entities/bmad-party-mode]] — Party Mode 实体
- [[concepts/claude-code-three-modes]] — 三模式对照
- [[concepts/claude-code-agent-teams]] — `agent-team` 模式底层
- [[concepts/agent-team-mailbox-protocol]] — 通信机制