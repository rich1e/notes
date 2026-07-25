---
title: Fabric Patterns × Claude Code 配置管理
category: synthesis
tags: [ai-tools, prompt-engineering, claude-code, llm, productivity]
sources:
  - "concepts/fabric-patterns"
  - "skills/claude-code-settings"
  - "entities/fabric-ai"
  - "skills/fabric-usage-patterns"
  - "skills/claude-code-token-optimization"
created: 2026-07-23T00:00:00Z
updated: 2026-07-23T00:00:00Z
summary: "Fabric 把 AI 能力标准化为可分享的 Pattern 单元，Claude Code 把 AI 会话行为标准化为可版本控制的配置——两者都在解决'AI 集成的一致性'问题，但一个从 Prompt 侧，一个从工具侧。"
provenance:
  extracted: 0.25
  inferred: 0.65
  ambiguous: 0.10
base_confidence: 0.72
lifecycle: draft
lifecycle_changed: 2026-07-23
relationships:
  - target: "[[concepts/fabric-patterns]]"
    type: derived_from
  - target: "[[skills/claude-code-settings]]"
    type: derived_from
  - target: "[[entities/fabric-ai]]"
    type: related_to
---

# Fabric Patterns × Claude Code 配置管理

## The Connection

两个系统都在解决同一个工程问题：**如何让 AI 的行为可复现、可分享、可版本控制？** ^[inferred]

- [[concepts/fabric-patterns]] 的答案：把 Prompt 写成 Markdown 文件，放进 Git 仓库，用目录名作为命令名。任何人 `fabric --pattern extract_wisdom` 都能复现同一个推理行为。
- [[skills/claude-code-settings]] 的答案：把工具权限、钩子脚本、环境变量写进 `.claude/settings.json`，提交到仓库。团队成员 `git pull` 后立刻获得相同的 Claude Code 会话行为。

前者标准化**推理逻辑**（Prompt），后者标准化**工具行为**（权限和钩子）。^[inferred]

## Where They Co-occur

两者在 [[skills/claude-code-token-optimization]] 中间接共现：Claude Code 的 Prompt Caching 和 Fabric 的 `--model` 参数都涉及如何降低 AI 推理成本，都属于"AI 工具配置"知识域。

实际工作流中可以组合使用：
1. 用 Fabric 的 `extract_wisdom` Pattern 把长文档压缩为结构化摘要
2. 把摘要作为 Claude Code 的上下文输入，减少 token 消耗
3. Claude Code 的 CLAUDE.md 配置（相当于 Fabric 的 System Prompt 全局设置）

## Cross-cutting Insight

**两者都是"AI Unix 哲学"的实践，但在不同管道节点。** ^[inferred]

Unix 哲学：小工具，做好一件事，管道组合。

Fabric 把这个哲学应用到 **Prompt 层**：每个 Pattern 是一个"AI 算子"，`stdin | fabric --pattern summarize | fabric --pattern extract_insights` 就是 AI 管道。

Claude Code 的 CLAUDE.md + settings.json 把这个哲学应用到**工具配置层**：钩子（hooks）是事件驱动的管道连接点，`PreToolUse` / `PostToolUse` 让你把任意 shell 命令插入 AI 工具的执行序列。

两者组合可以构建完整的"AI 增强开发流水线"——但它们各自的文档都没有把对方当作一个系统节点来描述。^[inferred]

## Tensions and Trade-offs

**Fabric 的 Pattern = 全局状态，Claude Code 的 CLAUDE.md = 项目状态**

Fabric Patterns 存储在 `~/.config/fabric/patterns/`，是用户级全局配置。Claude Code 的 `.claude/settings.json` 在项目仓库里，是项目级配置。两者的作用域不对齐：如果你在不同项目中需要不同的 Fabric Pattern 行为，需要手动管理，没有 Claude Code 那种"四级作用域"机制。^[extracted]

**可组合性的幻觉**

Fabric 的管道组合（`| fabric --pattern A | fabric --pattern B`）在实践中受限于上下文窗口——每次 `fabric` 调用都是一个全新的 LLM 请求，没有跨调用的状态。Claude Code 的工具链（MCP servers + hooks）则在一个持续会话中共享状态。两者的"管道"语义根本不同。^[inferred]

## Strongest Objection

"两个工具只是碰巧都用文件存配置——Fabric 用 Markdown 文件存 Prompt，Claude Code 用 JSON 文件存权限。这不比'Vim 和 Git 都用文本文件'更有洞见。把'用文件配置'归纳为'AI Unix 哲学'是在过度类比。"

> test: 找一个不使用文件配置的 AI 工具（如完全 UI 配置的 Cursor），检查它是否也能实现类似的"可复现行为"。如果 Cursor 的项目规则（`.cursorrules`）也是文件驱动的，则"文件即 Unix 管道"不是 Fabric/Claude Code 的特殊设计选择，而是 AI 工具领域的普遍模式，本页的论点需要修订为"这是行业共识，不是创新"。

## Open Questions

- Claude Code 的 CLAUDE.md 和 Fabric 的 System Prompt 在语义上最接近——能否把一个 Fabric Pattern 的 `system.md` 直接作为 CLAUDE.md 使用？两者的指令格式是否兼容？
- MCP（Model Context Protocol）是否是两者之间的桥梁——Fabric 作为一个 MCP 工具暴露给 Claude Code？
- Fabric 的 REST API 模式（`fabric --serve`）与 Claude Code 的 MCP server 集成有多大的工程距离？

## Related

- [[concepts/fabric-patterns]] — Fabric Pattern 设计原则与分类
- [[skills/claude-code-settings]] — Claude Code 四级配置体系
- [[entities/fabric-ai]] — Fabric 项目整体介绍
- [[skills/fabric-usage-patterns]] — Fabric 实际工作流集成
- [[skills/claude-code-token-optimization]] — Claude Code Token 优化（共同关注 AI 成本）
