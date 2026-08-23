---
title: "omo IntentGate（行动前分析真实意图）"
category: concepts
tags:
  - omo
  - intent
  - routing
  - concept
sources:
  - "https://github.com/code-yeongyu/oh-my-openagent"
created: "2026-08-05T07:30:00Z"
updated: "2026-08-05T07:30:00Z"
provenance:
  extracted: 0.78
  inferred: 0.16
  ambiguous: 0.06
base_confidence: 0.55
lifecycle: draft
lifecycle_changed: "2026-08-05"
tier: supporting
relationships:
  - target: "[[entities/oh-my-openagent]]"
    type: related_to
  - target: "[[concepts/omo-ultrawork-mode]]"
    type: related_to
summary: "omo IntentGate：行动前分析用户真实意图而非字面解读，Ultimate 有完整 IntentGate，Light Edition 仅识别 ultrawork/ulw 关键词触发全 agent 模式。"
---

# omo IntentGate（行动前分析真实意图）

> omo **IntentGate** = 行动前**分析真实用户意图**，然后才分类与执行。**避免字面误读**。Ultimate Edition 完整实现；Light Edition 仅识别 `ultrawork`/`ulw` 关键词。

## 是什么

> "Analyzes true user intent before classifying or acting. No more literal misinterpretations."

**用户说"修 bug"**——IntentGate 不直接 grep "bug" 字段，而是分析：

- 是**报告 bug**（让 agent 知道有这问题）
- 是**修 bug**（让 agent 改代码）
- 还是**解释 bug**（让 agent 讲清楚）

不同意图 → 不同行动路径。

## Light Edition 简化

> "(Light edition only recognises the `ultrawork`/`ulw` keyword.)"

Light Edition（Codex CLI）只识别 `ultrawork`/`ulw` 关键词——**没有完整 IntentGate**。

## 与 vault 已有概念的关系

| vault 已有 | IntentGate 的体现 |
|---|---|
| [[entities/bmad-method]] | BMad 的 IntentGate-style——Mary 接收"Hey Mary, let's brainstorm"判断意图 |
| [[concepts/bmad-named-agent-architecture]] | 8 步激活流程里"dispatch or present the menu"——dispatch 即 IntentGate |
| [[concepts/claude-code-three-modes]] | 类似 Claude Code "intent matches capability" |
| [[entities/bmad-party-mode]] | Party Mode 也有 intent 判断——决定 4 种 mode 之一 |

## 与"关键词触发"的对比

| 触发方式 | 优点 | 缺点 |
|---|---|---|
| **关键词触发** (`ultrawork`/`ulw`) | 简单、用户可预测 | 模糊请求不能用 |
| **IntentGate** | 模糊请求也 OK | 实现复杂；用户不可预测 |
| **两者结合**（omo Ultimate） | 各取所长 | 实施更复杂 |

## Open Questions

- IntentGate 的具体**判断算法**——是基于 keyword 兜底 + LLM 推断，还是纯 LLM？README 未给 ambiguous
- "true user intent" 的**判定标准**——是 "用户想达成什么"，还是 "用户用什么表达想达成什么"？ambiguous
- IntentGate 是否会**问澄清问题**——若用户意图完全模糊，是停下来问还是猜？ambiguous

## Related

- [[entities/oh-my-openagent]] — 框架本体
- [[concepts/omo-ultrawork-mode]] — Ultrawork 是 IntentGate 触发的最强路径
- [[concepts/omo-editions-ultimate-vs-light]] — Ultimate 完整，Light 仅关键词识别