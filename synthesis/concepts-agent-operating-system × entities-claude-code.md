---
title: agent-operating-system × claude-code
category: synthesis
tags: [ai-agents, agent-memory, Claude, mcp, synthesis]
sources:
  - "[[concepts/agent-operating-system]]"
  - "[[entities/claude-code]]"
  - "[[entities/openlore]]"
  - "[[misc/web-adamchanadam-github-io-agent-handoff-kit]]"
  - "[[misc/web-zhuanlan-zhihu-com-p-2013213227740325799]]"
created: 2026-08-04T13:30:00Z
updated: 2026-08-04T13:30:00Z
summary: "AOS 五层记忆是'宿主之上的框架层';Claude Code 原生只提供其中两层(KB=手写 CLAUDE.md、Working Memory=Auto Memory),其余三层(Handoff/Semantic/ADR)需靠工具或约定补齐——这划出了'框架该补什么'的精确边界。"
provenance:
  extracted: 0.25
  inferred: 0.68
  ambiguous: 0.07
base_confidence: 0.62
lifecycle: draft
lifecycle_changed: "2026-08-04"
relationships:
  - target: "[[concepts/agent-operating-system]]"
    type: related_to
  - target: "[[entities/claude-code]]"
    type: related_to
---

# agent-operating-system × claude-code

## The Connection

[[concepts/agent-operating-system]](AOS)把"多会话连续 AI 工作流"抽象成**五层记忆**:Handoff(任务交接)/ Auto(工作记忆)/ claude-mem(语义)/ ADR(决策)/ Knowledge Base(标准规范)。[[entities/claude-code]] 则是这套框架**实际跑在上面的宿主**。

单看两页都看不清一件事:**AOS 的五层里,宿主自己原生只兜底两层,剩下三层要么靠外部工具、要么靠人肉约定。** AOS 页把五层平铺陈述,像五个对等模块;claude-code 页只列自己的原生能力(CLAUDE.md / Auto Memory / MCP / 提示缓存)。把两者叠起来,才浮现"框架该补什么"的精确边界。

## Where They Co-occur

三个源页同时链到二者:[[entities/openlore]](把代码事实做成确定性记忆层)、[[misc/web-adamchanadam-github-io-agent-handoff-kit]](Handoff Kit 工具化任务交接层)、[[misc/web-zhuanlan-zhihu-com-p-2013213227740325799]](梳理 Claude Code 原生 CLAUDE.md + Auto Memory 两层机制)。这三处恰好各自补足 AOS 五层里宿主没原生兜底的一层。

## Cross-cutting Insight

把 AOS 五层逐一对到 Claude Code 原生能力上,得到一张**覆盖矩阵**^[inferred]:

| AOS 层 | Claude Code 原生 | 缺口靠谁补 |
|---|---|---|
| **Knowledge Base**(标准/规范) | ✅ `CLAUDE.md`(手写规则,四级作用域) | 宿主原生 |
| **Auto / Working Memory**(当前会话) | ✅ Auto Memory(`~/.claude/projects/*/memory/`,只加载前 200 行) | 宿主原生 |
| **claude-mem / Semantic**(长期语义) | ❌ 无 | [[entities/claude-mem]](hook 旁路捕获) |
| **Handoff / Task**(跨会话交接) | ❌ 无(compact 是压缩不是交接) | Agent Handoff Kit / 手写 checkpoint |
| **ADR / Decision**(决策与理由) | ❌ 无 | 人肉 ADR 文件 / OpenLore decisions gate |

**结论:AOS 不是要替换 Claude Code,而是给宿主的记忆缺口画了张施工图。** 宿主的两层原生能力(手写 KB + 自动 Working Memory)恰好是"最容易做、最不需要跨会话状态"的两层;越往"需要跨会话原子承诺"的层(Handoff、ADR)走,宿主越是空白,越需要外部工具顶上。这解释了为什么 vault 里 [[entities/claude-mem]] / Handoff Kit / [[entities/openlore]] 三个工具能并存不打架——它们各补一层,不重叠。

## Tensions and Trade-offs

- **compact ≠ Handoff。** Claude Code 的 compact 是"上下文塞满时的有损压缩",AOS 却要求把 compact 当成**主动的交接同步点**(`## Done / ## Todo / ## Decisions / ## Next Actions` 模板)。宿主的 compact 触发时机由 token 预算决定,不由任务边界决定——这是框架意图与宿主机制的根本错位^[ambiguous]。
- **"越界补层"的成本。** 每补一层就多一个工具/约定要维护;AOS 的五层完整性是理想,但对轻量任务,只用宿主原生两层可能就够,硬上五层是过度工程。
- **作用域漂移。** KB 层落在 `CLAUDE.md`(四级作用域,越具体越优先),但 Semantic 层落在 claude-mem 的 SQLite——两层的"这条知识在哪生效"语义不统一,跨层检索时容易错配。

## Strongest Objection

**这张覆盖矩阵可能是"拿 AOS 的分类去套宿主",而非宿主真实的架构。** AOS 是一份设计稿([[concepts/agent-operating-system]] 源自用户随手落 `_raw/` 的稿子,base_confidence 0.70),它的五层划分本身就是主观切法;硬把 Claude Code 的能力塞进这五个格子,可能制造出"缺三层"的假象——也许宿主根本不按记忆分层来设计,而是按"上下文窗口 + 文件系统"两个原语来设计,五层是强加的透镜。

> test: 找 Anthropic 官方对 Claude Code 记忆/持久化的架构描述,看它是否自述为"分层记忆",还是只讲 CLAUDE.md + Auto Memory 两个具体机制而无"层"的抽象。若官方从不提"层",则本页的五层对照是 AOS 单方视角,矩阵的"缺口"是分类假象而非真实空白。

## Open Questions

- Handoff 层若要在 Claude Code 上做成"原子承诺"(参考 [[concepts/worktree-durable-lease]] 的 lease CAS 语义),需要宿主提供什么钩子?compact hook 够不够?
- ADR 层目前全靠人肉;OpenLore 的 decisions gate 是否可以泛化成一个宿主无关的 ADR memory 后端?
- 五层里哪些是"任务规模无关的固定成本",哪些应随任务复杂度按需启用?

## Related

- [[concepts/agent-operating-system]]
- [[entities/claude-code]]
- [[entities/claude-mem]]
- [[concepts/claude-mem-memory-architecture]]
- [[concepts/claude-code-hooks-lifecycle]]
- [[misc/web-adamchanadam-github-io-agent-handoff-kit]]

