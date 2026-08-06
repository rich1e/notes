---
title: "omo Hashline Edits（LINE#ID 内容哈希防 stale-line error）"
category: concepts
tags:
  - omo
  - edit-tool
  - hashline
  - harness-problem
  - concept
sources:
  - "https://github.com/code-yeongyu/oh-my-openagent"
created: "2026-08-05T07:30:00Z"
updated: "2026-08-05T07:30:00Z"
provenance:
  extracted: 0.90
  inferred: 0.06
 ambiguous: 0.04
base_confidence: 0.75
lifecycle: draft
lifecycle_changed: "2026-08-05"
tier: supporting
relationships:
  - target: "[[entities/oh-my-openagent]]"
    type: related_to
  - target: "[[concepts/omo-discipline-agents]]"
    type: related_to
---

# omo Hashline Edits（LINE#ID 内容哈希防 stale-line error）

> omo 的 **Hash-Anchored Edit Tool**：每行带内容哈希标签（`LINE#ID`），agent 编辑引用标签——文件已变则 hash 不匹配，**edit 在任何 corruption 前被拒绝**。受 [oh-my-pi](https://github.com/can1357/oh-my-pi) 启发。

## 核心机制

普通 edit tool 用行号定位——agent 读文件时记录"line 11 是 `function hello()`"，然后 `edit line 11`：

```
11: function hello() {
12:   return "world";
13: }
```

**问题**：agent 写 edit 时**文件可能已变**——line 11 现在是 `function goodbye()`。agent 用旧内容产生新内容 → corruption。

omo 的 Hashline 解决：

```
11#VK| function hello() {
22#XJ|   return "world";
33#MB| }
```

**每行带短哈希后缀**。Agent 编辑时引用 `11#VK`：

> "The agent edits by referencing those tags. If the file has changed since the last read, the hash won't match and the edit is rejected before any corruption. No whitespace reproduction. No stale-line errors."

## 为什么这是真的

> "Most agent failures aren't the model's fault; it's the edit tool."

> "None of these tools give the model a stable, verifiable identifier for the lines it wants to change... They all rely on the model reproducing content it already saw. When it can't - and it often can't - the user blames the model."

> — [Can Bölük, The Harness Problem](https://blog.can.ac/2026/02/12/the-harness-problem/)

**agent 失败的根因之一是 edit tool**——给 model 行号 ≠ 给 model 行的稳定身份。

## 性能数据

> "Grok Code Fast 1: **6.7% → 68.3%** success rate, just from changing the edit tool."

**同一模型，仅换 edit tool**：成功从 6.7% 跳到 68.3%。这是[[concepts/deterministic-agent-memory]] 哲学"显式失败 / 状态分桶"的工具级落地。

## 关键设计点

### 1. 哈希短而非长

`#VK` / `#XJ` / `#MB` 是 8 字符左右短哈希——不占 context 但足以防 collision。

### 2. 拒绝 corruption 而非容错

普通 edit tool 失败时报错但已写入——**Hashline 在写入前拒绝**。

### 3. 无 whitespace reproduction

LLM 的常见错误是 reproduce whitespace 错（tab vs spaces、trailing space）。Hashline 不依赖 LLM 重打内容——只改指定内容，whitespace 自然保持。

## 与 vault 已有概念的关系

| vault 已有 | 在 Hashline 中的体现 |
|---|---|
| [[concepts/deterministic-agent-memory]] | "失败显式分桶" + "显式身份"哲学的编辑工具级落地 |
| [[entities/openlore]] | OpenLore 的"fresh/stale/ambiguous/not-found"也是同一哲学 |
| [[concepts/agent-team-race-condition-task-claim]] | "显式 lock" 在文件编辑层而非任务层 |
| [[concepts/ai-agent]] | Hashline 让 agent 的行动（act）更可靠 |

## 启发来源

[oh-my-pi](https://github.com/can1357/oh-my-pi) — Can Bölük 出品。omo 的 hashline 是受其启发。

## 已知限制

- **agent 必须先 read** 才能 edit——line#ID 来自 read 输出
- **跨多文件编辑** 仍需分别 read + edit——Hashline 不解决并行协调
- **冲突 merge**（多人同时改同一文件）未详述 [[ambiguous]]

## Related

- [[entities/oh-my-openagent]] — 框架本体
- [[concepts/omo-discipline-agents]] — Hashline 让 Hephaestus 等 deep worker 改文件更可靠
- [[concepts/deterministic-agent-memory]] — 上层哲学