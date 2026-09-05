---
title: "DESIGN.md Shared Memory — 设计 token 文件作为 agent 上下文"
category: concepts
tags: [design-md, shared-memory, design-tokens, agent-context, versioning, concept]
sources:
  - "[[references/open-codesign-readme]]"
  - "[[references/open-codesign-changelog]]"
created: 2026-08-24
updated: 2026-08-24
summary: DESIGN.md 是 open-codesign 的 shared memory 文件:不是"模型记忆里的 prompt",而是真实可读可改可版本化的 markdown 文件,内含品牌 token + 设计系统决策 + 组件模式。模型每次生成前读它,提取 token 作为 prompt 一部分。
base_confidence: 0.80
provenance:
  extracted: 0.70
  inferred: 0.25
  ambiguous: 0.05
lifecycle: draft
lifecycle_changed: 2026-08-24
tier: supporting
relationships:
  - target: "[[entities/open-codesign]]"
    type: derived_from
  - target: "[[concepts/skill-progressive-disclosure]]"
    type: related_to
  - target: "[[concepts/design-md-format-spec]]"
    type: related_to
  - target: [[concepts-design-system-as-ai-context × entities-google-stitch]]
    type: related_to
---

# DESIGN.md Shared Memory

## 核心抽象

DESIGN.md 是 open-codesign 的 **设计决策文件** —— 不是"模型记忆里的某条 prompt",而是真实存在的 markdown 文件。

| 旧模式(prompt-only) | 新模式(DESIGN.md 文件) |
|---|---|
| "请用我们的品牌色 (#FF6B35)" | `DESIGN.md` 里有 `colors.primary: #FF6B35` |
| 隐式,易丢 | 显式,可 grep |
| 跨 session 不共享 | 跨 session 共享 |
| 模型重新训才生效 | 编辑文件即生效(下次生成) |
| 设计师改不动 | 设计师用 Markdown 编辑 |

## 内容形态

典型 DESIGN.md 应包含:

```markdown
# Brand Identity

## Colors
- Primary: #FF6B35
- Secondary: #004E89
- Accent: #FFC857

## Typography
- Heading: Inter Bold 32/40
- Body: Inter Regular 16/24
- Code: JetBrains Mono 14/20

## Spacing
- Base unit: 4px
- Section: 32px
- Card padding: 24px

## Component Patterns
- Buttons: 8px radius, primary/secondary/ghost variants
- Cards: shadow-1, 16px padding, 12px radius
- Forms: 44px input height, focus ring #FF6B35 at 20%
```

## 与 skill 系统的互补

| skill | DESIGN.md |
|---|---|
| "怎么做" | "做这样" |
| 一次性指令 | 持久 token |
| 加载到 context 后用一次 | 每次生成前必读 |
| 程序员视角 | 设计师视角 |

举例:
- skill `frontend-design-anti-slop`: "避免 AI 烂品味"
- DESIGN.md: "我们品牌的烂品味定义为:圆角 < 8px 用 rounded-none,hover 用 transition-200"

模型组合使用两者:
1. 读 DESIGN.md 提取 token
2. 按 skill 加载的指令组织代码
3. 输出符合品牌的设计

## 可版本管理

DESIGN.md 是文件 → 可 git 版本化:

```bash
$ git log DESIGN.md
commit abc123 — feat: add dark mode tokens
commit def456 — fix: primary color contrast WCAG AA
commit 789xyz — docs: clarify heading hierarchy
```

设计师改动 → 自动进 git diff → reviewer 可审 → release notes 自动生成。

## 与 vault 已有概念的关系

- [[concepts/design-md-format-spec]] —— vault 已有 DESIGN.md 格式规范(从 awesome-design-md 蒸馏)
- [[concepts/design-md-token-interpolation]] —— token 插值语法
- [[concepts/design-md-anti-patterns]] —— 反模式
- [[concepts/design-system-as-ai-context]] —— "设计系统作为 AI 上下文" 是上位概念
- [[entities/google-stitch]] —— Google Stitch 是同源的"AI + 设计系统"产品

## 与 SKILL.md 的对比

| 维度 | DESIGN.md | SKILL.md |
|---|---|---|
| 关注 | **产出** (长什么样) | **过程** (怎么写) |
| 受众 | 设计师 | 程序员 / prompt 工程师 |
| 例子 | "Primary color is #FF6B35" | "Use semantic naming for CSS variables" |
| 修改者 | 设计师 | 程序员 |
| 加载时机 | 每次生成前 | agent 选择 skill 时 |

## 跨域判断

**(J1)** **DESIGN.md 是 prompt engineering 的成熟化** —— 把"对齐品牌指南"从模糊的 prompt 调试变为可编辑、可审计、可版本化的资产。这是 LLM 应用产品化的必经之路。

**(J2)** **DESIGN.md + skills 是 v0.2.0 的"3 大支柱"之一** —— workspace + permission + DESIGN.md(共享记忆)。三者缺一不可:
- 没 workspace → agent 状态不可恢复
- 没 permission → 安全不可控
- 没 DESIGN.md → 跨 session 品牌一致性丢失

**(J3)** **与 code 的 CLAUDE.md / AGENTS.md 是同源** —— 都是"用 markdown 文件给 agent 持久 context"。open-codesign 把这个 idea 搬到设计领域。

## 相关

- [[references/open-codesign-readme]]
- [[references/open-codesign-changelog]]
- [[entities/open-codesign]]
- [[concepts/skill-progressive-disclosure]]
- [[concepts/design-md-format-spec]] —— vault 已有 DESIGN.md 格式规范
- [[concepts/design-system-as-ai-context]] —— 上位概念
- [[entities/google-stitch]] —— 同源产品
- [[synthesis/concepts-agentic-design × concepts-design-md-shared-memory]] — synthesis: DESIGN.md 是 agentic design 的「已编译状态」