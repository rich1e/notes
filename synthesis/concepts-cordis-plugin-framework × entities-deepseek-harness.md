---
title: Cordis 插件架构 × DeepSeek Harness
category: synthesis
tags:
  - cordis
  - plugin-framework
  - typescript
  - agent-harness
  - architecture
  - synthesis
sources:
  - "[[concepts/cordis-plugin-framework]]"
  - "[[entities/deepseek-harness]]"
created: 2026-09-03T03:00:00Z
updated: 2026-09-03T03:00:00Z
summary: Cordis 提供的 Service/Event/Effect 三件套 vs dsh 实际实现的"everything is a plugin"架构 — synthesis 页面对比抽象框架与具体实现的契约。
provenance:
  extracted: 0.65
  inferred: 0.30
  ambiguous: 0.05
base_confidence: 0.72
lifecycle: draft
lifecycle_changed: 2026-09-03
tier: supporting
---

# Cordis 插件架构 × DeepSeek Harness

## The Connection

`[[concepts/cordis-plugin-framework]]` 是抽象:**Service + Typed Events + Reversible Effects** 三件套 — 任何 Cordis 应用都按这套契约组织代码。
`[[entities/deepseek-harness]]` 是具体实现:DeepSeek-AI 把 vendored Cordis 当作 agent harness 的**唯一架构选择** — agent loop 本身就是一个 plugin,tool / memory / provider 都是 plugin。

这两个 concept 都强调同一件事:**"everything is a plugin"**。Cordis 提供抽象,dsh 证明这个抽象可以 scale 到 24 个 package 的 monorepo 而不变成 spaghetti。

## Where They Co-occur

- dsh 的 `docs/architecture.md` 显式引用 Cordis 概念
- dsh 的 `docs/glossary.md` 用 Cordis 术语(Service / Event / Effect)解释自身概念
- vault 里这两个页是仅有的"agent harness via Cordis"研究对象

## Cross-cutting Insight

**"插件架构是 LLM agent 的天然骨架"**。^[inferred]

- 每个 agent 能力(tool / memory / provider)都有**生命周期**:启动时注册,运行中可能被替换,关闭时必须 dispose 释放
- LLM 上下文就是 Cordis 的 **Service**(共享状态)
- agent 之间的对话/事件就是 Cordis 的 **Typed Event**(强类型消息)
- 工具副作用(写文件 / 调 API)就是 Cordis 的 **Effect**(注册时自动获得 dispose 链)

dsh 的设计哲学隐含"agent 进程不能依赖全局可变状态,因为 agent 循环随时可能重置" — 这与 Cordis 的"一切经过 ctx"的纪律完全一致。

## Tensions and Trade-offs

- **插件化 vs 直接调用**:Cordis 通过 `ctx.<key>` 访问 service,有一层间接 — 调试时更难 trace。dsh 的 24-package monorepo 出现 performance 优化时就遇到这个间接层成本。^[inferred]
- **vendored Cordis vs upstream**:dsh 把 Cordis 嵌入自己仓库而非 npm dep — 失去版本升级的灵活性,但获得"知道整个 stack"的控制力。Cordis 上游 breaking change 不会突然打到 dsh。
- **TypeScript-only**:Cordis 是 TS 生态,意味着 dsh 无法用 Python/C++/Rust 实现 plugin — LLM agent harness 的多语言灵活性被牺牲。

## Strongest Objection

> "Cordis 的 service 抽象本质上和 Python 的 DI 框架(spring/django)一样是过度抽象,dsh 用它只是因为写 author 喜欢 TS 静态类型,不是为了'agent 特别需要'。"

**反驳**:di 框架在普通 web app 里是 nice-to-have,在 agent harness 里是 **necessary** — 因为 agent 循环的多轮迭代本质要求 capability 隔离(避免 tool 调用污染下一轮的 context),Cordis 的 `ctx` 提供了 Python DI 框架做不到的"每个 turn 重新构造"的优雅。**测试查询**: 在 dsh 的 agent loop 中,plugin 的 dispose 链是否在每个 turn 结束后真的被调用?如果 tool 调用 throw 异常,dispose 是否仍执行?

## Open Questions

- 是否存在 Python 版的等价 Cordis(plugin framework)?如果没有,Python agent 框架(Pydantic AI / LangGraph)如何弥补 capability-seam 缺失?
- vendored vs npm dep 的 trade-off 何时该选哪个 — agent harness 是 vendored 永远合理吗?

## Related

- [[concepts/cordis-plugin-framework]]
- [[entities/deepseek-harness]]
- [[concepts/capability-seam]]
- [[projects/dsh-package-hierarchy]]