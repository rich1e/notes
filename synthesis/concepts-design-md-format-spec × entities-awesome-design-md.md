---
title: DESIGN.md 格式规范 × awesome-design-md — 规范与其最大下游样本集
category: synthesis
tags:
  - design-md
  - stitch
  - google-labs
  - voltagent
  - awesome-list
  - design-system
  - ai-context
sources:
  - "[[concepts/design-md-format-spec]]"
  - "[[entities/awesome-design-md]]"
  - "[[concepts/design-system-as-ai-context]]"
  - "[[concepts/agentic-design]]"
  - "[[concepts/design-md-shared-memory]]"
  - "[[entities/google-stitch]]"
  - "[[entities/google-labs-code-design]]"
created: 2026-08-31T04:27:59Z
updated: 2026-08-31T04:27:59Z
summary: DESIGN.md 格式规范是 _what should be_;awesome-design-md 是 _what actually is_——74 个真实站点的精选集反向校准规范:从 8 个必备章节到 11 章节扩展、token 命名冲突、生产站点从不遵循的妥协清单。规范 ↔ 样本集是 DESIGN.md 生态的标准互校准机制。
tier: supporting
lifecycle: draft
lifecycle_changed: 2026-08-31
base_confidence: 0.82
provenance:
  extracted: 0.70
  inferred: 0.25
  ambiguous: 0.05
relationships:
  - target: "[[concepts/design-md-format-spec]]"
    type: related_to
  - target: "[[entities/awesome-design-md]]"
    type: related_to
  - target: "[[concepts/design-system-as-ai-context]]"
    type: related_to
  - target: "[[concepts/agentic-design]]"
    type: related_to
  - target: [[concepts-design-system-as-ai-context × entities-google-stitch]]
    type: related_to
---

# DESIGN.md 格式规范 × awesome-design-md

## The Connection

`design-md-format-spec` 是 Google Labs 提出的 _规范性_ 文档:YAML frontmatter 承载 token(colors/typography/spacing/components),Markdown body 按 8 个必备章节承载人类可读 rationale。`awesome-design-md` 是 VoltAgent 团队维护的 _样本性_ 仓库:74 个真实站点(Claude / Vercel / Notion / Stripe / Linear)的 DESIGN.md 精选。两个页面单看各执一词:规范说"应该这样",样本集说"实际是这样"——两者并置才能看出规范 _vs_ 现实的差距,即 awesome 仓库把章节从 8 扩展到 11 的根因。这是 vault 里少见的"标准 ↔ 实践校准"型合成。

## Where They Co-occur

6 个 wiki 页同时引用两者,典型语境:

- **设计系统作为 AI 上下文**:[[concepts/design-system-as-ai-context]] 是 DESIGN.md 的 _why_——为什么用 markdown 承载设计系统而不是 Figma API
- **Agentic 设计哲学**:[[concepts/agentic-design]] 把 DESIGN.md 视为 _已编译的_ 设计决策,与代码事实同构
- **共享记忆**:[[concepts/design-md-shared-memory]] 强调 DESIGN.md 是 _跨 agent 持久化的_ 设计契约
- **Stitch / Google Labs**:[[entities/google-stitch]] 与 [[entities/google-labs-code-design]] 分别是规范的 _作者_ 与 _相关项目_
- **awesome 仓库作为下游**:[[entities/awesome-design-md]] 是规范的最大下游样本集,反向校准规范的 _可落地性_

## Cross-cutting Insight

**DESIGN.md 生态有一个隐含的 _校准回路_**——规范 ↔ 样本集 ↔ 反向校准 ↔ 规范修订:

1. **规范出 draft**(Google Labs / Stitch 团队):8 章节 + YAML frontmatter,基于 _理论_ 设计
3. **样本集积累**(VoltAgent / awesome-design-md):74 个真实站点 _采纳_ 的 DESIGN.md,统计哪些章节 _真的_ 被填写、哪些 _跳过_
5. **校准出新规范**:基于样本数据,规范 _扩展_ 到 11 章节(awesome 仓库的扩展路径),或 _修订_ token 命名冲突
7. **循环重复**:每个规范版本都对应 _新一轮_ 样本积累

**核心推论**:DESIGN.md 不是 _一次性规范_,而是 _永远在校准_ 的开放生态。awesome-design-md 仓库 _本身_ 就是规范的一部分——没有样本集,规范就是 _空中楼阁_。这是 awesome 列表在 DESIGN.md 领域里 _不可替代_ 的根因:它不只是"参考集合",而是规范的 _校准数据源_。^[inferred]

## Tensions and Trade-offs

| 维度 | 规范视角 | 样本视角 | 张力 |
|---|---|---|---|
| 章节完整性 | 必须 8/11 章节 | 多数站点只填 3-5 章节 | 完整 vs 实用 |
| Token 命名 | 推荐 `color/primary` 路径风格 | Stripe / Vercel 用 `colors.brand.500` 平铺 | 嵌套 vs 平铺 |
| Markdown 体例 | 推荐 1 H1 + 多 H2 | 多数站点用 _多个_ H1(每个 token 一节) | 标准 vs 习惯 |
| frontmatter 必需性 | 必备 | Claude / Linear 在 body 内手写 | 机器可读 vs 人类可读 |
| 版本演进 | 单调扩张(8 → 11) | 站点用 _旧版本_ 或 _自定义_ 版本 | 标准 vs 灵活 |

## Strongest Objection

**批评**:把 awesome-design-md 包装成"规范的校准数据源"是 _过度浪漫化_——它本质上是一个 _GitHub trending list_,voltagent 团队的 _编辑判断_ 决定收录哪些,不收录哪些。74 个样本远不是 _统计显著_ 的;即使全收录也是 _选择性_ 样本。把 awesome 列表当成"规范的真理"会和 _任何一个_ awesome 列表一样带有编辑偏见。

> test: 对比 awesome-design-md 收录的 74 个 DESIGN.md 与 _未收录的_ 100 个真实站点 DESIGN.md(可从 GitHub Code Search `path:/DESIGN.md` 抽样)。如果未收录样本的章节分布 _显著不同_ 于已收录样本,说明 awesome 列表是 _选择性_ 而非 _代表性_,作为校准数据源不可靠。

## Open Questions

- vault 没有 _DESIGN.md 反向_ 工具(从 Figma/Sketch 自动生成 DESIGN.md)的页——是否值得补一篇 <!-- broken link: no design-md-from-figma page found -->
- 8 章节 vs 11 章节的 _diff_ 没有单独页——值得一篇 <!-- broken link: no design-md-section-evolution page found -->
- awesome-design-md 仓库本身 _是否_ 遵循 DESIGN.md 规范?若不,这是 _元规范_ 的 _良性违反_ 还是 _生态分裂_ 的信号?
- DESIGN.md 与 [[concepts/design-system-as-ai-context]] 的关系(co 之外):后者是 _AI 消费侧_,前者是 _人类生产侧_——AI 工具链是否直接读 DESIGN.md 或需中间转换?

## Related

- [[concepts/design-md-format-spec]]
- [[entities/awesome-design-md]]
- [[concepts/design-system-as-ai-context]]
- [[concepts/agentic-design]]
- [[concepts/design-md-shared-memory]]
- [[entities/google-stitch]]
- [[entities/google-labs-code-design]]
- [[synthesis/concepts-agentic-design × concepts-design-md-shared-memory]]