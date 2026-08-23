---
title: "Claude Code 三种工作模式"
category: concepts
tags:
  - claude-code
  - ai-agents
  - concept
summary: "Claude Code 三种工作模式：Default（单会话系统管理员）、Subagents（主会话+短命子任务，token 节流）、Agent Teams（多独立 Claude Code session + lead 委派 + Mailbox IPC + 9 已知限制）。核心差异是会话数 + 通信能力。"
sources:
  - "https://www.youtube.com/watch?v=cSkoaCCmq0w"
  - "https://docs.claude.com/en/docs/claude-code/agent-teams"
created: "2026-08-05T03:30:00Z"
updated: "2026-08-05T04:30:00Z"
provenance:
  extracted: 0.88
  inferred: 0.10
  ambiguous: 0.02
base_confidence: 0.78
lifecycle: draft
lifecycle_changed: "2026-08-05"
tier: supporting
relationships:
  - target: "[[concepts/claude-code-agent-teams]]"
    type: related_to
  - target: "[[entities/claude-code]]"
    type: related_to
  - target: "[[entities/claude-code-agent-teams-feature]]"
    type: related_to
---

# Claude Code 三种工作模式

> Claude Code（Anthropic 终端编码 agent）有三种根本不同的会话结构，对应三种典型使用场景。**核心差异不是"能力"而是"会话数 + 通信能力"**——能力上三者重叠 90%，区别在**会话如何管理 / teammate 间能否直接通信 / token 如何节流**。本概念综合 [[misc/web-youtube-com-watch-v-cskoa-ccmq0w]]（视频教程）与 anthropic-claude-code-agent-teams-docs（Anthropic 官方 v2.1.178+ 文档）。

## 三模式对照

| 模式 | 会话数 | 主控者 | 何时用 |
|---|---|---|---|
| **Default** | 1（你直接对话） | 你 | 系统管理员 / 选模型 / 看技能 / 简单编码 |
| **Subagents** | 1 主 + N 短命子 | 你 | 跑远活要节省主上下文 token |
| **Agent Teams** | 1 leader + N 独立长会话 | Team leader | 大任务、需要多视角、agent 间通信 |

> "Everything you can do in agent team mode and sub agent mode, you can also do in default mode. The biggest difference is in how the session is managed."

## Default：通用系统管理员

新终端 → `claude` → 直接对话。能写代码、debug、web search、做研究。

**现在 Default 的真正主战场**：`/model` 选模型、`/skills` 看技能、项目初始化、subagent 配置、team 组建规划。

不要把 Default 当"做所有事的地方"——一旦上下文超过 200K，模型开始 tunnel vision（锁定单一方向）+ yes-man 综合症（重复你已有偏见）。

## Subagents：token 节流的"远房跑腿"

**类比**：保安公司控制室 → 大楼某层有异常 → 派一个 agent 下电梯、拐弯、问 5 个人、进房间查问题 → 回来只报"修好了，Bart 在乱跑"。

主会话不积累中间过程 token，**只增加一条结论**。子 agent 失败则回报新 issue 而非用无效 token 拖累主。

典型用法：已有密码+邮箱登录，要加 Google 登录——派 subagent 加功能，主线程继续做别的。

## Agent Teams：强制多视角

**类比**：保安公司接到"整栋楼今晚要办活动，10 层 ×10 房全要安保" → team leader 把任务拆给左右各 5 层 → 每 agent 独立工作 → 用对讲机互通"三楼五号有人乱跑"→ 活动结束 leader 关团队。

**6 个关键工程机制**：

1. **触发必须显式** —— 关键词如 `create an agent team`
2. **Leader 负责 plan + task list + prompt per agent**
3. **Agent 不共享原对话上下文** —— 用户必须先落 MD，leader 才分发
4. **Race-condition task lock** —— 防双 agent 抢同一任务浪费 token
5. **每 agent 可指定模型** —— 不是每个都 Opus，Sonnet/Haiku 也行
6. **Graceful shutdown** —— coding 场景默认保留 idle 等 review；research 场景自动全关

## 何时用哪个

```
任务复杂度 / 需要多视角？
├── 低 → Default
├── 中（单一线性工作但 token 多）→ Subagents
└── 高（多维度、需要互相通信）→ Agent Teams
```

**判断速记**：
- **你只是跟一个 agent 说话** → Default
- **你跟一个 agent 说话但它会叫帮手** → Subagents
- **你跟一个 leader 说话，它叫一群 agent 互相转告** → Agent Teams

## Related

- [[misc/web-youtube-com-watch-v-cskoa-ccmq0w]] — 视频源（Opus 4.6 引入 Agent Teams）
- [[synthesis/Research: Claude Code Agent Teams]] — 三轮调研综合
- anthropic-claude-code-agent-teams-docs — 官方一手文档
- [[concepts/claude-code-agent-teams]] — Agent Teams 工程机制详解
- [[concepts/agent-team-display-modes]] — 5 种 teammateMode
- [[concepts/agent-team-cost-overhead]] — Linear scaling token 成本
- [[concepts/agent-operating-system]] — 三模式的会话管理差异 = AOS 五层记忆如何被不同模式分摊
- [[concepts/ai-agent]] — 三模式是通用 AI agent 框架在 Claude Code 内的具体实现
- [[entities/claude-code]] — 主体工具
- [[entities/claude-code-agent-teams-feature]] — Agent Teams 功能实体