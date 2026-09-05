---
title: 设计系统作为 AI 上下文 × Google Stitch
category: synthesis
tags:
  - ai-coding
  - design-systems
  - ai-context
  - google-stitch
  - synthesis
sources:
  - "[[concepts/design-system-as-ai-context]]"
  - "[[entities/google-stitch]]"
  - "[[concepts/design-md-shared-memory]]"
  - "[[concepts/design-md-anti-patterns]]"
  - "[[concepts/ai-tool-specialization]]"
  - "[[entities/awesome-design-md]]"
  - "[[skills/claude-code-token-optimization]]"
  - "[[skills/stitch-upload-design-md]]"
created: 2026-09-05T07:00:00Z
updated: 2026-09-05T07:00:00Z
summary: 设计系统作为 AI 上下文(范式:把 design tokens / components 当作可机读的"代码事实")与 Google Stitch(产品:第一个大规模实现该范式的 AI 设计工具)的关系 — Stitch 是该范式从概念到生产的第一个完整链路,同时暴露范式本身的新约束(MCP 鉴权 + token 经济)。
provenance:
  extracted: 0.20
  inferred: 0.65
  ambiguous: 0.15
base_confidence: 0.55
lifecycle: draft
lifecycle_changed: 2026-09-05
tier: supporting
---

# 设计系统作为 AI 上下文 × Google Stitch

## The Connection

**设计系统作为 AI 上下文**(concepts/design-system-as-ai-context)是范式:把 design tokens / components / layout primitives 当作可机读的"代码事实",让 AI agent 能像 IDE 一样理解设计意图。**Google Stitch**(entities/google-stitch)是第一个大规模实现该范式的 AI 设计工具:Figma plugin + Gemini 多模态 + MCP 协议 → 从设计 prompt 到 Figma 原型。

这两个 concept 在 vault **10 个**同时提及两者的页面中成对出现 — 它们从**哲学层**和**产品层**两个抽象层次回答同一个问题:"AI 如何消费设计上下文而不只是消费文本"。

## What This Synthesis Covers

- **DESIGN.md shared memory**(concepts/design-md-shared-memory)是"代码事实住文件"的同构:把设计决策也编译成可机读的 markdown,与 design tokens 共用同一类范式
- **DESIGN.md anti-patterns**(concepts/design-md-anti-patterns)是该范式在文本层的失败模式
- **AI 工具专业化分工**(concepts/ai-tool-specialization)把 Stitch 定位为"设计子任务专业化"的代表性产品
- **Awesome Design.md**(entities/awesome-design-md)是 DESIGN.md 范式的下游样本集,与 Stitch 生态互为校准数据源
- **Claude Code Token 优化**(skills/claude-code-token-optimization):Stitch 集成暴露的隐性约束 — MCP 鉴权 token 与 AI 生成 token 的双层经济
- **Stitch 上传 DESIGN.md**(skills/stitch-upload-design-md)是该范式的具体 skill 化

## Strongest Objection

> "Stitch 只是 Figma + Gemini 的 UI 包装,没有真正的"AI 消费设计系统"创新 — 把 design tokens 当 JSON 喂给 LLM 任何团队都能做,算不上范式突破。"

### Testable 反驳

1. **MCP 集成是范式级的**:Stitch 不是把 tokens 当 JSON 喂,而是把 MCP 协议作为"设计系统↔AI"的统一接口(参考 entities/claude-code 描述);这是 Claude Code / Gemini 协议的同构,不是简单 API 调用
2. **DESIGN.md 校准回路**:awesome-design-md(74 站点样本)作为规范校准数据源,Stitch 作为产品出口 — 二者形成"规范→产品→样本→校准规范"的飞轮,这是 vault 现有 `synthesis/concepts-design-md-format-spec × entities-awesome-design-md.md` 已识别的模式
3. **figwright 适配**:projects/figwright 把 Stitch 协议复用到 Claude Code → Figma 的反向 codegen 链路,证明该范式可被产品家族化而不只是单点工具

## Related Pages

- [[concepts/design-system-as-ai-context]]
- [[entities/google-stitch]]
- [[concepts/design-md-shared-memory]]
- [[concepts/design-md-anti-patterns]]
- [[concepts/ai-tool-specialization]]
- [[entities/awesome-design-md]]
- [[skills/claude-code-token-optimization]]
- [[skills/stitch-upload-design-md]]
- [[projects/figwright/figwright]]
- [[projects/dayfold/references/stitch-design-system]]

## Provenance Note

本合成基于 vault 10 个共现页面的模式归纳(co=15 顶级未覆盖对)。Strongest Objection 来自"Stitch 是 UI 包装"的常见质疑;3 个 testable 反驳引用 vault 一手证据(MCP 协议集成 / DESIGN.md 校准回路 / figwright 反向 codegen)。`base_confidence: 0.55` 反映范式-产品合成的推断成分,但有 10 个共现页面 + 2 个独立 skill 化(stitch-upload-design-md / claude-code-token-optimization)支撑。
