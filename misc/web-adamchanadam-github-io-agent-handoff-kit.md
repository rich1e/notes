---
title: "Agent Handoff Kit — AI agent 跨会话接力工具"
category: misc
tags: [ai-tools, ai-agent, claude-code, memory]
sources:
  - "https://adamchanadam.github.io/agent-handoff-kit/agent-handoff-kit-guide.html"
source_url: "https://adamchanadam.github.io/agent-handoff-kit/agent-handoff-kit-guide.html"
created: "2026-07-31T00:00:00"
updated: "2026-07-31T00:00:00"
summary: "Adam Chan 的 npm 工具 @adamchanadam/agent-handoff-kit（v0.3.56）:一句 init 在项目文件夹铺好交接文件 + 分任务工作规则包,让本地 AI agent(Claude Code/Codex/Gemini CLI 等)跨会话「开工/收工」接力,高风险操作强制停手确认。"
affinity: {}
promotion_status: misc
stub: false
provenance:
  extracted: 0.85
  inferred: 0.1
  ambiguous: 0.05
base_confidence: 0.6
lifecycle: draft
lifecycle_changed: "2026-07-31"
relationships:
  - target: "[[concepts/agent-operating-system]]"
    type: implements
  - target: "[[concepts/claude-mem-memory-architecture]]"
    type: related_to
---

# Agent Handoff Kit — AI agent 跨会话接力工具

## Overview

Adam Chan 开发的开源命令行工具(npm 包 `@adamchanadam/agent-handoff-kit`,本页对齐 v0.3.56)。它解决的核心问题是 **AI agent 的跨会话失忆与接力**:一句 `npx @adamchanadam/agent-handoff-kit@latest init` 就在项目文件夹里铺好一整套交接文件 + 分任务的「工作规则包」,让能读写本地文件夹的 AI agent(Claude Code / OpenAI Codex / Gemini CLI / Antigravity 等)通过「开工 / 收工」两个自然语言指令,在多次对话、多个工具、多天之间**接住同一根接力棒**。它管的是「对话**之间**」的连续性——与管「单次对话质素」的 [Adam-AI-Instructions](https://github.com/prompt-templates/Adam-AI-Instructions) 互补不重叠。

## Key Points

- **一句 init 铺 21 个文件**:`init` 命令建立三个入口(`AGENTS.md` / `CLAUDE.md` / `GEMINI.md`,同一套规则的三个桥接口)+ 交接文件 + 工作规则包,写入前先确认、不覆盖既有文件。
- **「开工」只看状态,不自动干活**:单独说 `Start Agent Handoff`/「开工」时,AI 只读权威 `SESSION_HANDOFF` 的最低必要状态,输出状态卡(交接状态 / 当前目标 / 注意事项 / 建议下一步)后**停下等待**;只有同句写明任务时才开始工作。开工句 ≠ 执行授权。^[extracted]
- **分任务工作规则包**(`dev/RULE_PACKS.md` 为路由表,按需加载而非全塞进上下文):`onboarding`(新手引导)、`safety`(删档/Git/发布/机密)、`writing`(文案/README)、`research`(查资料/标不确定性)、`coding`(源码/测试)、`agent-governance`(交接治理)、`release`(版本/tag/deploy/npm)、`knowledge`(Notion/Drive/Obsidian 真源分工)、`integrations`(Connector/MCP/Plugin 凭证边界)、`communication`(语言/输出格式)。
- **五阶段工作流**:计划 → 读取 → 改动 → 检查 → 正式执行。计划阶段先写清目标/范围/验收标准,读取阶段收集真实事实(不凭估计),改动阶段写好但不直接执行,高风险动作停手等确认。
- **安全模式强制护栏**:不可逆动作(文件移动/删除/覆写/`git reset --hard`/推送/发布)必须先讲计划;大批量文件操作强制**预演(dry-run)列清单 + 用户明确确认**才正式执行;禁 `rm -rf`、系统根路径操作;强制推送须另取授权并核对受影响 ref;AI「不可以悄悄做」。
- **「收工」触发完整接力流程**:一句「收工」/`Wrap up Agent Handoff`/`wrap up`/`done for today` 等,AI 即**对账式更新**交接文件(逐段改为当前事实,不追加旧状态下面避免「新日期配旧快照」)、写工作日志、并把接力内容同步到 `START_NEXT_SESSION_PROMPT.txt` 副本。日志长期使用后旧条目自动缩为短索引再封存。
- **文件接入治理(governance bridge)**:重要文件(stock list / production guide / runbook / checklist / source-of-truth)完成后,用「把 `docs/x.md` 接入 Agent Handoff Kit」让 AI 只读审核——检查文件是否写清用途、`PROJECT_INDEX.md` 是否登记、`DOC_SYNC_REGISTRY.md` 是否有同步规则、是否有旧版真源;输出「已接合/缺口/建议补丁/需你判断」,不自动删改合并。避免重要文件变「孤儿」。
- **跨工具接力一致**:同一套交接资料,今天 Claude、明天 Codex/Antigravity 都接得上;新 AI 读入口 + 交接文件即知上次做到哪、下一步、有何风险,无需重述背景。
- **外部工具「代执行 + 回读核对」**:已连好 GitHub/Notion/Drive 等 MCP/Connector 时,AI 可代建 repo、推送、建 release,写入后立即回读核对一致性;未连好则降级为「列手动步骤」。凭证由 AI 工具安全存储管理,**不写入 `dev/` 任何治理文件**(机密分离)。
- **资源收口(ownership)**:长任务用完 MCP/browser/notebook/helper server 后,能证明属本任务的可关闭;不明/共享/他人拥有的资源只列证据等确认。
- 三个日常情景(整理下载目录 / 咖啡店市场调查 / 长期 AI 项目演进)共享同一「开工看状态 → 讲任务 → 确认计划 → 收工写下次提示」骨干节奏,证明流程跨任务/跨工具/跨天复用。^[extracted]

## Concepts

- [[concepts/agent-operating-system]] — AOS 五层记忆架构的**第一层就是「Handoff (Task Memory)」**;Agent Handoff Kit 正是这一层的工具化落地实现(交接文件=Task Memory,收工=compact checkpoint 同步点)
- [[concepts/claude-mem-memory-architecture]] — claude-mem 覆盖 AOS 的 Semantic Memory 层;本工具覆盖 Handoff/治理层,二者互补
- [[concepts/claude-code-hooks-lifecycle]] — 与 hook 驱动的自动记忆不同,本工具靠自然语言「开工/收工」显式触发接力

## Entities

- [[entities/claude-code]] — 本工具支持的主力 AI agent 之一(亦支持 Codex / Gemini CLI / Antigravity)
- [[entities/claude-mem]] — 同为解决 AI 会话失忆的工具,但走「自动语义记忆」路线而非「显式交接文件」路线

## Related

- [[misc/web-zhuanlan-zhihu-com-p-2013213227740325799]] — Claude Code 官方 CLAUDE.md + Auto Memory 记忆机制;本工具的 `AGENTS.md`/`CLAUDE.md` 入口正是建立在这套原生机制之上
- [[skills/claude-code-token-optimization]] — 本工具「按需加载规则包、不全塞上下文」「日志自动缩为短索引」都是 token/上下文优化实践

## Open Questions

- 本工具的显式交接文件(`SESSION_HANDOFF.md`)与 Claude Code 原生 Auto Memory(`MEMORY.md`)在同一项目并存时,状态如何避免重复/漂移?谁是权威真源?^[inferred]
- `RULE_PACKS.md` 的任务路由由 AI 自主判断加载哪个规则包——判断错误(如高风险任务未加载 safety 包)时的兜底机制是什么?^[ambiguous]
