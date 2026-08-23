---
title: "BMad Party Mode"
category: entities
tags:
  - bmad-method
  - ai-agents
  - multi-agent
  - workflow
  - entity
sources:
  - "https://github.com/bmad-code-org/bmad-method"
created: "2026-08-05T07:00:00Z"
updated: "2026-08-05T07:00:00Z"
summary: "BMad Party Mode 把 5 个命名 agent 召进同一对话房间对话，4 种运行模式（session/auto/subagent/agent-team），可自建 cast + 持久化自定义 party。"
provenance:
  extracted: 0.88
  inferred: 0.08
  ambiguous: 0.04
base_confidence: 0.70
lifecycle: draft
lifecycle_changed: "2026-08-05"
tier: supporting
relationships:
  - target: "[[entities/bmad-named-agent]]"
    type: related_to
  - target: "[[entities/bmad-method]]"
    type: related_to
  - target: "[[concepts/bmad-party-mode-modes]]"
    type: related_to
  - target: "[[concepts/claude-code-agent-teams]]"
    type: related_to
---

# BMad Party Mode

> Party Mode 把 5 个 BMad 命名 agent **召进同一对话**——PM、Architect、Dev、UX Designer、按需加。他们用 persona 说话、互相认同 / 反对 / 接力。你掌控房间。[[concepts/bmad-party-mode-modes]] 4 种模式决定"谁在思考"。

## 是什么

`bmad-party-mode` 把**已安装的 BMad agents** 召进同一房间对话——默认就是你安装的 lineup（PM + Architect + Dev + UX Designer + 你选的模块加的）。他们 in-character 回答、同意 / 不同意 / 互相接力。你 steer——追问 / push back / 拉某个声音向前 / 换话题。房间跑到你结束为止。

**核心机制**：personas 持有不同优先级。Architect 守 design、PM 守 scope、Dev 守 what's actually buildable。**关进同一房间，tradeoff 在对话里浮现，而不是 sprint 进去三周后**。

## 何时用

- 有真实 tradeoffs 的决策
- brainstorming 与 "我们漏了什么？"
- post-mortems 与 retrospectives
- 提交前的 plan 压力测试

Party Mode 也是**快速 + 真正有趣的** brainstorming——personas 有意见会冲突。可以从任何其他工作流**中间**开个 party：brainstorm 中、PRD 中、coding 中、销售角、创意件塑造中。任何时候想要更多视角，**拉个房间而不用放下当前事**。

> **Example**:
> - You: 单体 vs 微服务 for MVP？
> - Architect: 单体起步。微服务加运维成本，千用户级别不需要。
> - PM: 同意。Time to market 比尚未证实的扩展更重要。
> - Dev: 单体，但带干净模块边界，让后来拆服务不用重写。

## 启动 party

| 目标 | 输入 |
|---|---|
| 默认模式开 party | `/bmad-party-mode` |
| 指定模式开 | `/bmad-party-mode --mode auto`（也 `session` / `subagent` / `agent-team`） |
| 一次性非交互运行 | `/bmad-party-mode --non-interactive "review this PR"` |
| 开保存的 party | `/bmad-party-mode --party code-review-crew` |
| 即兴召 cast | "party mode with the bridge crew of the Enterprise" |
| 创建或加 party | "party mode, create a new party" |
| 编辑既有 party | "party mode, edit the writers' room" |
| 定制 skill | `/bmad-customize bmad-party-mode` |

## 默认 interactive 行为

Party 默认**交互式**：开场问句是起始话题，不是停止信号，房间一轮一轮保持开直到你结束。**回答第一个问题不自动结束 party**。要反过来——服务一个意图就停——用 `--non-interactive`：跑到自然 close、收尾、释放 spawn 的 agents。

## 与 vault 已有概念的关系

| vault 已有 | 在 BMad Party Mode 的体现 |
|---|---|
| [[concepts/claude-code-three-modes]] | Party Mode 4 模式借鉴 subagent / agent teams |
| [[concepts/claude-code-agent-teams]] | Party Mode `agent-team` 模式 = Claude Code Agent Teams 的应用 |
| [[concepts/agent-team-mailbox-protocol]] | `subagent` 与 `agent-team` 模式都用 mailbox 通信 |
| [[entities/bmad-named-agent]] | Party 的 cast 由命名 agent 提供 |
| [[concepts/agent-team-race-condition-task-claim]] | Party Mode 不直接面对 race condition（不像 Build 工作流），但底层 multi-agent 通信仍依赖 Mailbox |

## 自建 cast（custom parties）

默认用 installed BMad agents。**更大用法**是从任何你能描述的 personas 自建 cast，**保存供重用**。通过**同一 skill** 编写 party——它检测你想 run 还是 build，结果写到你的 override 通过 [[skills/bmad-customize-skill]]。

Party Mode 可定制如所有 BMad skill。`/bmad-customize bmad-party-mode` 直接设默认：把你建过的任一 group pin 成默认 party 让它无 flag 加载、选起始模式、设整个 session 房间要遵守的 house rules。

## 反一致 club（v6.10+ 新）

Party Mode 在 v6.10 加了一个 **anti-consensus club** 内置 persona 组（Wildcard / Level / Killjoy / Splinter）——决策房间**抵抗快速达成一致**但仍保留人在 control。启动：

```bash
--party=anti-concensus-club
--mode subagent   # 最佳结果
```

可在 bmad customize 设成默认。

## Open Questions

- "anti-consensus club" 的具体 persona 行为差异（Wildcard 是什么倾向？Killjoy 怎么反驳？）— README 只列名字未给详细角色定义 ambiguous
- "saved party" 跨项目共享的机制——是 git committed 还是 per-user？

## Related

- [[entities/bmad-method]] — 框架本体
- [[entities/bmad-named-agent]] — Party 的 cast 成员
- [[concepts/bmad-party-mode-modes]] — 4 种运行模式详解
- [[concepts/claude-code-agent-teams]] — 底层 agent teams 模式
- [[skills/bmad-customize-skill]] — 定制 party 默认