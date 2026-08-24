---
title: "open-codesign Prompt System & Design Skills — DeepWiki 4.2"
category: references
tags: [open-codesign, skills, prompt-system, deepwiki, progressive-disclosure]
sources:
  - "https://deepwiki.com/OpenCoworkAI/open-codesign/4.2-prompt-system-and-design-skills"
source_url: "https://deepwiki.com/OpenCoworkAI/open-codesign/4.2-prompt-system-and-design-skills"
created: 2026-08-24
updated: 2026-08-24
summary: DeepWiki 4.2 章:markdown skills 在 packages/core/src/skills/(YAML frontmatter + body,schemaVersion 1,1536 字符描述上限),JSX design skills 在 userData/templates/design-skills/;progressive disclosure — 技能不烤进系统提示,agent 通过 skill(name) 工具按需加载。
base_confidence: 0.8
provenance:
  extracted: 0.75
  inferred: 0.20
  ambiguous: 0.05
lifecycle: draft
lifecycle_changed: 2026-08-24
tier: supporting
---

# open-codesign Prompt System & Design Skills — DeepWiki 4.2

## 文件路径

```
packages/core/src/skills/
  ├── index.ts              # 入口
  ├── loader.ts             # 加载逻辑(loadSkillsFromDir)
  └── loader.test.ts        # 测试
```

`apps/desktop/resources/templates/skills/` 目录下 bundle 内置 markdown skills。

`userData/templates/design-skills/` 目录下放内置 JSX design skills。

## Skill 文件格式

**Markdown skills** (`.md` 文件):

```yaml
---
schemaVersion: 1
name: data-viz-recharts
description: ...   # ≤1536 字符
---
[markdown body with instructional content]
```

**JSX design skills** (`.jsx` 文件):

- 高质量组件模板
- 通过 skill name 索引,dashboard / landing-page / chart-svg / glassmorphism / editorial-typography / heroes / pricing / footers / chat-ui / data-table / calendar / slide-deck 等

## 加载机制 — Progressive Disclosure

> Skills are not baked into the system prompt.

关键设计: **skill 不烤进系统提示**,而是通过 `skill(name)` 工具按需加载。

加载流程:

1. `loadSkillsFromDir(dir)` 扫描 `.md` 文件
2. 校验 `schemaVersion: 1`
3. 强制 1536 字符的 `description` 上限(防止 prompt 膨胀)
4. 注册到 in-memory skill registry
5. Agent 在 prompt 里看到可用的 `skill(name)` 工具
6. Agent 通过调用该工具按需把 skill body 注入上下文

这种模式的好处:
- **节省 context window**: 12 个 skill 同时加载 = 数千 token;按需加载 = 0
- **可扩展**: 用户加 `SKILL.md` 到项目目录即可教模型新 taste
- **可分版本**: skill 是文件,可 git 版本管理

## 内置 skill 名(截至 v0.2.0)

### Markdown skills(`packages/core/src/skills/`)

| name | 用途(推测) |
|---|---|
| `data-viz-recharts` | 数据可视化 + Recharts |
| `mobile-mock` | 移动端 mockup |
| `pitch-deck` | 演示幻灯片 |
| `frontend-design-anti-slop` | 前端设计"避免 AI 烂品味"清单 |

### JSX design skills(`userData/templates/design-skills/`)

- `dashboard` / `landing-page` / `chart-svg` / `glassmorphism` / `editorial-typography` / `heroes` / `pricing` / `footers` / `chat-ui` / `data-table` / `calendar` / `slide-deck`

## "Every skill is available in every generation"

README 明确:模型在写 CSS 前会先 reasoning layout intent,选择适用的 skill(s)。

## 与 vault 已有概念的关系

- [[concepts/skill-progressive-disclosure]] —— 完整 vault-side 抽象
- [[concepts/design-md-shared-memory]] —— DESIGN.md 与 skill 互补:skill 是 "怎么做" 的指令,DESIGN.md 是 "做这样" 的 token
- [[skills/chezmoi-keyring-template]] —— 类似 progressive disclosure 模式 chezmoi 也有(`{{ keyring ... }}` 模板按需展开)

## 限制

- DeepWiki 4.2 章未详列 8 个工具的 input/output schema,需要源码或其他源补充
- 未能确认 `skill(name)` 工具返回的格式(是 markdown body 字符串?还是完整 AgentMessage?)
- "12 个 markdown skill" 与 "12 个 JSX design skill" 数量相同,可能只是巧合,需要进一步核实

## 相关

- [[references/open-codesign-readme]]
- [[synthesis/Research: open-codesign]]
- [[concepts/skill-progressive-disclosure]]