---
title: "DESIGN.md 中的 AI 反模式与 Do's and Don'ts"
category: concepts
tags: [design-system, ai-coding, ai-taste, anti-pattern, concept]
summary: "DESIGN.md 第 8 必备章节 'Do's and Don'ts' 是约束 agent 行为的关键段：明示允许与禁止的设计决策，避免 AI 生成的 UI 漂向通用 gradient/glow/emoji 默认审美（俗称 'AI taste'）。"
sources:
  - "https://github.com/VoltAgent/awesome-design-md"
  - "https://github.com/google-labs-code/design.md"
created: "2026-07-28T01:00:00Z"
updated: "2026-07-28T01:00:00Z"
tier: supporting
lifecycle: draft
lifecycle_changed: "2026-07-28"
base_confidence: 0.70
provenance:
  extracted: 0.65
  inferred: 0.30
  ambiguous: 0.05
    type: related_to
relationships:
  - target: "[[concepts/design-system-as-ai-context]]"
    type: related_to
  - target: "[[concepts/design-md-format-spec]]"
    type: related_to
  - target: "[[entities/awesome-design-md]]"
    type: related_to
  - target: "[[entities/google-labs-code-design]]"
    type: related_to

---

# DESIGN.md 中的 AI 反模式与 Do's and Don'ts

> "AI taste" 不是设计感缺失——是模型训练数据里的平均审美漂移。DESIGN.md 的 Do's and Don'ts 段是约束这种漂移的硬约束。

## 什么是 "AI taste"

来自第三方综述（CSDN / cnblogs 等中文 AI 社区，[muyeseocom](https://blog.csdn.net/muyeseocom/article/details/161808011) 文章）观察到的模式：

- **审美均值化**：模型倾向输出"通用漂亮"——渐变背景、玻璃拟态卡片（glassmorphism）、emoji 装饰、过多的 shadow / glow。
- **结构似曾相识**：button 永远圆角 + 主色填充，card 永远 1px hairline border + 12px 圆角，导航永远 sticky。
- **配色趋同**：蓝紫渐变 + 暖色高光是 LLM 训练数据里出现最多的"成功 UI"——所以模型默认就会渲染这类。
- **决策无依据**：能用 token 的地方，模型却**现场编**：选了 `#3B82F6` 因为"看着对"，但没说为什么。

不约束时，agent 会把 "make it pretty" 这种 prompt 渲染成训练集均值——这就是 "AI taste"。

## Do's and Don'ts 章节的形式

[[entities/awesome-design-md.md|awesome-design-md]] 真实样本（Notion）的反模式段：

```markdown
## Do's and Don'ts

### Do
- Use the deep navy hero band as the anchor of every marketing surface
- Pair the navy hero with pastel-tinted feature cards
- Treat the purple pill button as the highest-priority CTA only

### Don't
- Don't use the purple pill for inline links (use link-blue instead)
- Don't introduce gradients on hero bands beyond what the navy allows
- Don't apply the pastel tints to anything other than feature cards
```

这类 `Do / Don't` 段是 spec 的第 8 必备章节，由 entities/google-labs-code-design.md|google-labs-code/design(https://github.com/google-labs-code/design.md) 强制要求。

## 反模式的几个常见分类

| 类别 | 反模式 | DESIGN.md 通常的 Don't |
|------|--------|-----------------------|
| **装饰** | emoji 装饰、过度渐变、glow / blur / glassmorphism | "Don't add emoji or icons not in the system" |
| **结构** | 不必要的 card / sticky 元素、hairline border 滥用 | "Don't introduce new card patterns" |
| **颜色** | 越界使用 primary（如 primary 用作 inline link）、暖冷混用 | "Don't use primary for inline links — use link-blue" |
| **间距** | 凭感觉选 padding、跳过 spacing scale | "Default to `{typography.body-md}` for body" |
| **字体** | 引入未在 token 里定义的字体、滥用 italic | "Don't use the display family for body copy" |
| **组件复用** | 新建变体而非扩展 components | "Add new variants as separate `components:` entries" |

## 为什么 Do's and Don'ts 比 token 更重要

token 决定**能用什么值**；Do's and Don'ts 决定**在什么场景用哪个值**。

- 没有 Do's and Don'ts：agent 拿到 Stripe DESIGN.md，仍可能选错按钮颜色（Stripe 有 gradient + pill + outline + ghost，agent 可能每次选不同的）。
- 加上 Do's and Don'ts：agent 知道 *最高优先级 CTA 用 gradient pill；次要 CTA 用 outline；icon-only 用 ghost*——选择有依据。

这是 DESIGN.md 与"简单 CSS 变量"的核心差异——DESIGN.md 是**带决策规则的**设计系统，不只是颜色表。

## 与 AI 工具栈分工的呼应

[[concepts/ai-tool-specialization]] 指出 "AI 工具栈专业化分工" 是 2026 工作流原则——DESIGN.md + Do's and Don'ts 是这条原则的**具体载体**：

- 没 Do's and Don'ts 的 DESIGN.md → 让 Claude Code 兼做"决策"——它会按 AI taste 漂移。
- 有 Do's and Don'ts 的 DESIGN.md → 让 Stitch / 设计 agent 做"决策"——Claude Code 只**执行**决策。

这就是 [[entities/google-stitch]] + DESIGN.md 的真正价值：把"决策"与"执行"分离，让每个 agent 守一段。

## Iteration Guide：awesome-design-md 的扩展

`Do's and Don'ts` 是 spec 必备；`Iteration Guide` 是 awesome-design-md 自加的扩展章节，明确告诉 agent 修改时该怎么做：

```markdown
## Iteration Guide

1. Focus on ONE component at a time
2. Reference component names and tokens directly
3. Run `npx @google/design.md lint DESIGN.md` after edits
4. Add new variants as separate `components:` entries
5. Default to `{typography.body-md}` for body
6. Keep `{colors.primary}` (purple) as the primary CTA — distinct from `{colors.link-blue}` for inline links
7. Use `{rounded.md}` for buttons, `{rounded.lg}` for cards, `{rounded.full}` for pill tabs/badges only
```

第 3 条 `npx @google/design.md lint` 把验证闭环**写进 agent 的工作流**——这是社区贡献的实践。

## 局限

- **人类写、机器读**：Do's and Don'ts 是人类撰写的 prose，agent 不一定能严格遵守。它是"建议"不是"语法约束"——这点与 token 引用不同。
- **覆盖不到"为什么"**：Do's and Don'ts 给 *做什么*，但很少解释 *为什么*。HagiCode 的 [Newbe36524 文章](https://www.cnblogs.com/newbe36524/p/19833995) 提到 *"AI can't understand why a design choice was made or when to apply a pattern"*——这是结构化描述的根本限制。^[ambiguous]
- **跨设计系统不通用**：每个品牌的 Do's and Don'ts 都高度专属——把 Stripe 的 Don't 套到 Linear 会出问题。

## 相关页面

- [[concepts/design-md-format-spec]] — 第 8 章节在整体 schema 中的位置
- [[concepts/design-system-as-ai-context]] — 上游：DESIGN.md 为何是硬约束
- [[concepts/ai-tool-specialization]] — 决策与执行分离原则
- [[entities/google-stitch]] — Stitch 是 DESIGN.md 的天然生产者
