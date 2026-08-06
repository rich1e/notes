---
title: "BMad 三腿凳：Skill / 命名 Agent / Customization"
category: concepts
tags:
  - bmad-method
  - architecture
  - persona
  - concept
summary: "BMad 命名 agent 模型由三个原语组成：Skill（能力）/ Named Agent（persona 连续性）/ Customization（个性化）。抽掉任一条腿体验就崩。"
sources:
  - "https://github.com/bmad-code-org/bmad-method"
created: "2026-08-05T07:00:00Z"
updated: "2026-08-05T07:00:00Z"
provenance:
  extracted: 0.90
  inferred: 0.06
  ambiguous: 0.04
base_confidence: 0.72
lifecycle: draft
lifecycle_changed: "2026-08-05"
tier: supporting
relationships:
  - target: "[[entities/bmad-named-agent]]"
    type: related_to
  - target: "[[entities/bmad-method]]"
    type: related_to
  - target: "[[skills/bmad-customize-skill]]"
    type: related_to
---

# BMad 三腿凳：Skill / 命名 Agent / Customization

> BMad 的 agent 模型建立在三个原语之上，**三者组合**才让"用 AI 写代码"变成"用 AI 交付软件"。抽掉任何一条腿，体验就崩。

## 三腿

| 原语 | 提供什么 | 住哪里 |
|---|---|---|
| **Skill** | **能力** —— 一件 assistant 能做的具体事（brainstorm / 起草 PRD / 实现 story） | `.claude/skills/{skill-name}/SKILL.md`（或 IDE 等价位置） |
| **Named Agent** | **Persona 连续性** —— 一个可识别的身份，把一组相关 skills 装进一致 voice / principles / 视觉 | 目录以 `bmad-agent-*` 开头的 skills |
| **Customization** | **变你的** —— 重塑 agent 行为、加 MCP 集成、换模板、叠加组织约定的 override | `_bmad/custom/{skill-name}.toml`（committed 团队）+ `.user.toml`（个人，gitignored） |

## 抽掉每条腿的后果

> "Pull any leg away and the experience collapses:"

- **没 agent 的 skills** —— 用户得按名字 / 代码导航能力列表
- **没 skills 的 agents** —— 有 persona 但啥也做不了
- **没 customization** —— 每个用户拿到的开箱行为一致，org 特有需求都得 fork

## 三腿在 8 步激活流程中的协作

1. **Resolve the agent block** —— 合并 shipped `customize.toml` + 团队 + 个人 override（**Customization** 腿）
2. **Execute prepend steps** —— 团队配置的 pre-flight 行为
3. **Adopt persona** —— 硬编码身份 + 定制角色 / 风格 / 原则（**Named Agent** 腿）
4. **Load persistent facts** —— 组织规则、合规注意、可选 `file:` 加载
5. **Load config** —— 用户名 / 通信语言 / 输出语言 / artifact 路径
6. **Greet** —— 用配置语言 + emoji 前缀打招呼
7. **Execute append steps** —— 团队配置的 post-greet 设置
8. **Dispatch or present the menu** —— 首句映射到菜单项就直接走，否则渲染菜单（**Skill** 腿）

## 与 vault 已有概念的关系

| vault 已有 | 三腿凳映射 |
|---|---|
| [[concepts/ai-agent]] | "感知-规划-行动"循环对应 Skill 腿（行动能力） |
| [[concepts/agent-operating-system]] | 三腿 = AOS 的 5 层 memory 在"agent 产品化"上的简化 |
| [[concepts/ai-tool-specialization]] | Named Agent 腿是工具栈专业化的"具名化" |
| [[concepts/claude-code-settings]] | Customization 腿的 TOML resolver 与 Claude Code settings 四级作用域是同源设计 |
| [[concepts/mcp-server-protocol-quirks]] | Customization 腿支持加 MCP 集成——和 Claude Code MCP 的坑同源 |

## Customization 是"first-class citizen"

> "The customization model is what lets this scale beyond a single developer."

三腿凳的**关键差异化**——Customization 不仅是配置，是**一等公民**。两层 override：

- **`_bmad/custom/*.toml`** —— committed 团队 override
- **`.user.toml`** —— 个人，gitignored

这种"团队 / 个人"二层切分与 [[concepts/mcp-server-protocol-quirks]] 的"`-s user` / `--global`"等价，与 [[skills/claude-code-settings]] 的四级作用域同源——vault 已有可参考的模式。

## 抽掉 customization 的真实代价

不让你改 agent——每个团队 fork 一份改版的 Mary 与 John。命名冲突、upstream 升级接不上、培训文档爆炸。Customization 让**单源 + 多变体**可能。

## Related

- [[entities/bmad-named-agent]] — 5 命名 agent 是 Named Agent 腿的实例
- [[entities/bmad-method]] — 框架本体
- [[skills/bmad-customize-skill]] — Customization 腿的操作指南
- [[concepts/bmad-delivery-loop]] — 三腿凳如何支持 4 阶段闭环