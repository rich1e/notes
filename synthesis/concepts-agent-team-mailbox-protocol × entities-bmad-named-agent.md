---
title: Agent Team 邮箱协议 × BMad 命名 Agent 派发
category: synthesis
tags: [ai-agent, agent-teams, mailbox, bmad, named-agent, synthesis]
sources:
  - concepts/agent-team-mailbox-protocol
  - entities/bmad-named-agent
  - concepts/bmad-preventing-agent-conflicts
  - concepts/omo-discipline-agents
  - entities/bmad-method
  - entities/bmad-party-mode
created: 2026-08-23T09:00:00Z
updated: 2026-08-23T09:00:00Z
summary: 邮箱协议(JSON inbox + 逐条校验 + error 自愈)是 Agent Teams 工程级 IPC;BMad 命名 Agent(Mary BA/John PM 等)是产品化 IPC(每 agent 一份"任务契约")。两者都解决"多 agent 同时改同一文件"但用截然不同的抽象层。
provenance:
  extracted: 0.15
  inferred: 0.75
  ambiguous: 0.10
base_confidence: 0.65
lifecycle: draft
lifecycle_changed: "2026-08-23"
---

# Agent Team 邮箱协议 × BMad 命名 Agent 派发

## The Connection

`[[concepts/agent-team-mailbox-protocol]]` 是 Agent Teams 的工程级 IPC 实现:每个 agent 一个 `~/.claude/teams/{team-name}/inboxes/{agent-name}.json` inbox 文件,逐条 JSON 校验,v2.1.207+ 单条 malformed 自愈。这是**文件级 message queue**,把"agent 间通信"落到磁盘。

`[[entities/bmad-named-agent]]`(Mary BA / John PM / Sally UX / Winston Architect / Amelia Dev)是产品化 IPC:每个 agent 锚定一阶段(分析/规划/UX/架构/开发),hardcoded identity + customizable layer 平衡。这是**角色级任务契约**,把"agent 间通信"抽象为人与人协作。

## Where They Co-occur

4 个 co-occurring 页全部围绕"多 agent 派发与冲突避免":

- `[[concepts/bmad-preventing-agent-conflicts]]` — 用 ADR + FR/NFR + standards 防多 agent 同时实施系统时的冲突技术决策
- `[[concepts/omo-discipline-agents]]` — 5 specialists 协调(Sisyphus 委派),与 BMad 5 命名 agent 同结构
- `[[entities/bmad-method]]` — BMad 框架本体
- `[[entities/bmad-party-mode]]` — 多 agent 房间(4 模式:session / auto / subagent / agent-team),核心是把"房间"作为 mailbox 的产品化包装

## Cross-cutting Insight

邮箱协议与命名 Agent 是同一问题在两个抽象层的解:

| 抽象层 | 邮箱协议 | BMad 命名 Agent |
|---|---|---|
| **协议** | JSON 文件 IPC | 角色身份 IPC |
| **冲突解决** | file lock + 逐条校验 | ADR 文档 + 阶段排序 |
| **失败语义** | malformed 单条自愈 | elicitation + 二次审视 |
| **可视性** | inbox 文件路径 | agent 名称 + skill 锚点 |
| **可重放** | JSON 文件天然可重读 | 角色契约 + customizations |

**核心 insight**:**Agent Teams 的 mailbox 协议是 BMad 命名 Agent 范式的底层 transport**。BMad Party Mode 的 `agent-team` 模式(v6.10+) 实际上就是 Agent Teams + 命名 agent 层 cast 的组合——上层 cast(产品化身份)是 BMad 的"产品包装",下层 mailbox(工程化 IPC)是 Anthropic 的"协议基础"。

具体证据:`[[entities/bmad-party-mode]]` 的 4 模式中,**`agent-team` 模式是 v6.10+ 加 mailbox 修正**(v6.10 sprint_planning.py 用 epic 解析 + status 合并做 deterministic)。即 BMad 在 v6.10 才决定"走 Agent Teams mailbox",v6.10 之前是 BMad 自实现邮箱协议(可能基于 Socket.IO 或文件)。

这意味着:**BMad Party Mode `agent-team` 模式是 vault 里 [[concepts/claude-code-agent-teams]] 的产品化封装**——cast 抽象加在 Claude Code Agent Teams 上层。

## Tensions and Trade-offs

- **邮箱协议是基础,但缺乏角色语义**:Agent Teams mailbox 只传消息,不知道"这条消息是 BA 的还是 PM 的"。BMad 命名 agent 解决了这个,但增加了"硬编码身份 → 失去灵活性"的成本
- **命名 agent 适合知识工作,但不适合工程任务**:Mary BA 适合产品 brainstorm,不适合代码 review。Amelia Dev 适合 scaffold,不适合 architectural decision。BMad 5 命名 agent 本质是"产品/UX 阶段分工",不是"工程阶段分工"
- **mailbox 自愈 vs ADR 静态文档**:Agent Teams mailbox 单条 malformed 自愈是运行时韧性,BMad ADR 是事前防御。两套机制叠加才好,但维护成本翻倍

## Strongest Objection

> 反对者:BMad 命名 Agent 只是"Anthropic Agent Teams + persona 文件"的产品化外壳。Party Mode 的 `agent-team` 模式在 v6.10 加 mailbox 后,Bmad 的差异化几乎消失——任何团队都可以在 Agent Teams 上定义 cast,BMad 的"5 个固定名字"是营销不是技术。

> 反驳:但 BMad 的差异化在**工作流绑定**(Clarify → Plan → Build → Learn 4 阶段),不在 agent 名字。agent 名字是 cast 的 shorthand,真正价值是阶段纪律。同样的 cast 名字去掉阶段就退化成 vanilla Agent Teams。

> test: 把 BMad 的 5 命名 agent 拆成 5 个 Claude Code Agent Teams role,跑同一个产品 brainstorm task,对比 BMad Party Mode 与裸 Agent Teams 的**输出结构化程度**。若 BMad 显著更高,差异化在纪律;若差不多,Bmad 的 cast 是营销。

## Open Questions

- BMad 的 `sprint_planning.py` 是否是 mailbox 协议的 BMad-specific 实现,还是直接调用 Agent Teams API?文档没说 ^[ambiguous]
- omo 的 5 specialists(Sisyphus / Hephaestus / Oracle / Librarian / Explore)与 BMad 5 命名 agent 是否同源(都从 PM-BA-Dev-UX-Architect 5 阶段模型派生)?
- Agent Teams v2.1.207+ 的 mailbox 单条 malformed 自愈与 BMad 的 elicitation(method 二次审视)是否在做同一件事的工程 vs 产品两层?

## Related

- [[concepts/agent-team-mailbox-protocol]] — Agent Teams 工程级 IPC
- [[entities/bmad-named-agent]] — BMad 5 命名 agent 产品化 IPC
- [[concepts/bmad-preventing-agent-conflicts]] — ADR 防冲突
- [[entities/bmad-party-mode]] — 4 模式 + mailbox 修正
- [[synthesis/concepts-bmad-named-agent-architecture × concepts-omo-discipline-agents]] — BMad persona 三腿凳 vs omo capability-defines-persona