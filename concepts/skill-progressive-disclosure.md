---
title: "Progressive Skill Disclosure — 技能不烤进 prompt,按需加载"
category: concepts
tags: [skills, progressive-disclosure, prompt-engineering, token-economy, concept]
sources:
  - "[[references/open-codesign-prompt-system-deepwiki]]"
created: 2026-08-24
updated: 2026-08-24
summary: progressive skill disclosure 模式:skill 文件(YAML frontmatter + markdown body,1536 字符描述上限)不烤进系统 prompt,agent 通过 skill(name) 工具按需加载到 context。节省 token + 用户可扩展 + 可版本管理。
base_confidence: 0.85
provenance:
  extracted: 0.80
  inferred: 0.15
  ambiguous: 0.05
lifecycle: draft
lifecycle_changed: 2026-08-24
tier: supporting
relationships:
  - target: "[[entities/open-codesign]]"
    type: derived_from
  - target: "[[concepts/design-md-shared-memory]]"
    type: related_to
  - target: "[[skills/chezmoi-keyring-template]]"
    type: related_to
---

# Progressive Skill Disclosure

## 核心问题

如果把 12+ 个 skill 的完整 body 全烤进 system prompt:
- **Token 浪费**: 每次请求都带 N × skill_size(可能 5-15K tokens 闲置)
- **Context 稀释**: 模型注意力分散在大量无关内容
- **可扩展性差**: 用户加新 skill = 改 system prompt = 重启

## 解法:Progressive Disclosure

```
[System Prompt]
You have access to the skill(name) tool. Available skills:
- data-viz-recharts: Recharts 图表最佳实践 (description ≤1536 chars)
- mobile-mock: 移动端 mockup 模式
- pitch-deck: 演示幻灯片结构
- frontend-design-anti-slop: 避免 AI 烂品味
... (descriptions only, no bodies)

[During agent loop]
Model thinks: "this task needs a chart → skill('data-viz-recharts')"
Tool returns: full skill body (markdown instructions + examples)
Model continues with skill body in context
```

## Skill 文件格式

```yaml
---
schemaVersion: 1
name: data-viz-recharts        # 用于 skill(name) 查找
description: ...               # ≤1536 字符,出现在 system prompt
---
[markdown body]
[instructional content]
[code examples]
[best practices]
```

**description 上限 1536 字符**: 防止 prompt 膨胀,鼓励 skill 作者精简。

## 三大好处

| 好处 | 解释 |
|---|---|
| **Token 经济** | 12 个 skill 全加载 = 数千 token 闲置;按需加载 = 0(不调用就不消耗) |
| **可扩展** | 用户加 `SKILL.md` 到项目目录,模型通过 `skill(name)` 即时学会新 taste |
| **可版本管理** | skill 是文件,可 git diff / 版本化 / 跨项目同步 |

## open-codesign 的具体实现

- Markdown skills: `packages/core/src/skills/`(打包到 `apps/desktop/resources/templates/skills/`)
- JSX skills: `userData/templates/design-skills/`
- 加载器: `loadSkillsFromDir(dir)` 扫描 `.md` → 校验 schemaVersion: 1 → 校验 description ≤ 1536 → 注册到 in-memory registry
- Agent loop 看到 `skill(name)` 工具,调用时按 name 查 registry 返回完整 body

## 类似模式对照

| 系统 | 模式 | 备注 |
|---|---|---|
| **open-codesign** | `skill(name)` 工具返回 markdown body | 显式工具调用 |
| **Claude Code** | 系统提示中描述 skills(`.claude/skills/` SKILL.md) | 部分 progressive:description 烤入,body 按需 |
| **Anthropic Agent Teams** | skill 通过 agent 注册 | 配置驱动 |
| **LangChain Tools** | tool definition + tool body 一起 | 不 progressive,全在 prompt |

## 跨域判断

**(J1)** **Progressive disclosure 是 LLM 应用的标准模式** —— 类似 web 开发的 "lazy loading":不全加载,按需 fetch。Anthropic / OpenAI 的 function calling 都鼓励这种 design。

**(J2)** **1536 字符 description 上限是 product design 而非 technical limit** —— 技术上可以无限长,但 description 越长 system prompt 越膨胀,反而损害模型选 skill 的准确性。1536 字符是"足够描述 + 足够精简"的实用平衡。

**(J3)** **用户加 SKILL.md 是低代码扩展点** —— 类似 Cursor 的 `.cursorrules`、Claude Code 的 `CLAUDE.md`。open-codesign 的"add a SKILL.md to teach the model your taste"是与这两者同源的 UX 模式。

## 与 vault 已有概念

- [[skills/chezmoi-keyring-template]] —— chezmoi 的 `{{ keyring ... }}` 模板也是 progressive disclosure:key 不在 dotfile 仓库,运行时按需展开。本质同源
- [[concepts/design-md-shared-memory]] —— skill 是"怎么做"的指令,DESIGN.md 是"做这样"的 token。两者都是文件级别的 agent context 注入
- [[concepts/extensibility]] —— skill 模式是扩展性模式的一种(plugin / hook / capability seam)

## 相关

- [[references/open-codesign-prompt-system-deepwiki]]
- [[entities/open-codesign]]
- [[concepts/design-md-shared-memory]]
- [[concepts/extensibility]]
- [[skills/chezmoi-keyring-template]]