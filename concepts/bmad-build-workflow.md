---
title: "BMad Build 工作流（最少人工、最大安全）"
category: concepts
tags:
  - bmad-method
  - build
  - workflow
  - concept
summary: "BMad `bmad-build` 是 canonical 实施工作流：先压缩 intent → 路由到最小安全路径 → 让模型跑更久更少监督 → 在正确层诊断失败 → 只在需要时拉人回来。"
sources:
  - "https://github.com/bmad-code-org/bmad-method"
created: "2026-08-05T07:00:00Z"
updated: "2026-08-05T07:00:00Z"
provenance:
  extracted: 0.88
  inferred: 0.08
  ambiguous: 0.04
base_confidence: 0.68
lifecycle: draft
lifecycle_changed: "2026-08-05"
tier: supporting
relationships:
  - target: "[[entities/bmad-method]]"
    type: related_to
  - target: "[[concepts/bmad-delivery-loop]]"
    type: related_to
  - target: "[[concepts/bmad-preventing-agent-conflicts]]"
    type: related_to
---

# BMad Build 工作流（最少人工、最大安全）

> `bmad-build` 是 BMad **canonical 实施工作流**——接任何东西（自由 intent / issue / 完全 planned story），**最少人在环回合 + 最大安全** 出代码改动。

## 入口兼容

Upstream planning **始终可选 + 可变**：

- 清晰改动直接进
- 大 initiative 带 PRD / UX / 架构 / epics / stories / readiness / sprint 计划进来

这些 artifacts **加强实施 context**，**不是选不同开发工作流**。

Planned story 进 Build 时，story 仍是 upstream 产品 / acceptance context。**Build 创建自己的执行 record**——让实施决策 + review findings 可追溯，**不替换 story**。

## 5 步核心设计

### 1. 先压缩 intent

工作流**开始时**让人和模型**把请求压成一个连贯目标**。输入可以是：

- 几句粗 intent
- bug tracker 链接
- plan mode 输出
- chat 会话抄来的文本
- BMad 自己的 epics / sprint artifacts 的 planned story

工作流用任何存在的 upstream context + 解决需要安全实施的 gaps。

> "This workflow does not eliminate human control. It relocates it to a small number of high-value moments: intent clarification, spec approval, review of the final product."

### 2. 路由到最小安全路径

目标清晰后，**工作流决定这是真 one-shot 还是需要完整路径**。

- **小 / 零 blast-radius 改动** → 直接实施
- **其他** → 走 planning，让模型有更强边界后再无人监督跑

### 3. 跑更久更少监督

路由决定后，**模型能更多自己 carry**。完整路径上，**approved spec 成为模型执行的边界**——少监督——这正是设计的全部意义。

### 4. 在正确层诊断失败

> "If the implementation is wrong because the intent was wrong, patching the code is the wrong fix. If the code is wrong because the spec was weak, patching the diff is also the wrong fix."

如果实施错**因为 intent 错**——**patching code 是错 fix**。如果 code 错**因为 spec 弱**——**patching diff 也是错 fix**。

工作流设计成**诊断失败在哪层进入系统 → 回到那层 → 从那层重新生成**。

Review findings 用于**判断问题来自 intent / spec 生成 / 本地实施**。**只有真本地问题才本地 patch**。

### 5. 只在需要时拉人回来

Intent interview 人在环，但**不是 recurring checkpoint 那种打断**。工作流**试图让那些 recurring checkpoint 保持最少**。

主要回来的时刻：
- **Intent-gap resolution** —— review 证明工作流无法安全推断意图时
- **Final review** —— 决定结果是否可接受

## 与 vault 已有概念的关系

| vault 已有 | 在 bmad-build 中的体现 |
|---|---|
| [[skills/claude-code-token-optimization]] | "跑更久更少监督" = token 优化的人力侧 |
| [[concepts/deterministic-agent-memory]] | "在正确层诊断失败" = deterministic agent memory 的"失败显式分桶" |
| [[concepts/bmad-preventing-agent-conflicts]] | Build 工作流的"上游 planning"= 防 agent 冲突的架构护栏 |
| [[concepts/ai-tool-specialization]] | 5 阶段由 5 命名 agent 各守 = build 阶段由 Amelia 主推 |

## 关键洞察

**Build 不消除人在 control——它把 control relocate 到少数高价值时刻**：

1. **Intent 澄清** —— 把 messy 请求变连贯目标，无隐藏矛盾
2. **Spec 批准** —— 确认 frozen understanding 是要 build 的正确东西
3. **最终 review** —— 主要 checkpoint，人决定结果是否可接受

## Related

- [[entities/bmad-method]] — 框架本体
- [[concepts/bmad-delivery-loop]] — Build 是闭环一阶段
- [[concepts/bmad-preventing-agent-conflicts]] — 上游 planning 防冲突
- [[concepts/bmad-advanced-elicitation]] — review 之后的二次审视