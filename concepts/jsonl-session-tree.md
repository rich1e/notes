---
title: "JSONL Session Tree — pi-coding-agent 的 append-only 树形事件流"
category: concepts
tags: [jsonl, session, tree-structure, pi-coding-agent, compaction, append-only, concept]
sources:
  - "[[references/pi-coding-agent-session-format]]"
created: 2026-08-24
updated: 2026-08-24
summary: pi-coding-agent session 是 JSONL 树:第一行 header(type/version/id/timestamp/cwd/parentSession),后续行是 entries 带 id/parentId 形成树。entry 类型 8 种 + AgentMessage union 7 种。compaction entry 用 firstKeptEntryId 标记 token 边界。open-codesign / dsh / CoDesign 都用此模式或其变体。
base_confidence: 0.90
provenance:
  extracted: 0.80
  inferred: 0.15
  ambiguous: 0.05
lifecycle: draft
lifecycle_changed: 2026-08-24
tier: core
relationships:
  - target: "[[entities/pi-coding-agent]]"
    type: derived_from
  - target: "[[concepts/atomic-state-recovery]]"
    type: extends
  - target: "[[concepts/durable-session-log]]"
    type: related_to
---

# JSONL Session Tree

## 抽象

Session 是一个 **append-only JSONL 文件**,其内容是一棵以 `id` 链 `parentId` 的事件树。第一行是 header,其余每行是一个 entry。

## 为什么是树不是列表

线性 JSONL(像 Claude Code 的 `projects.jsonl`)每条消息只有时间戳,无法:
- 分叉(尝试两种设计 A/B,对比)
- 编辑(用户撤销某次操作,后续 entry 不需要变)
- 紧凑保留(用 summary 替代前段,保留后段)

树形 JSONL 用 `parentId` 指向父 entry,允许:
- **分叉**: 同一父 entry 有多个子 entry,各走各的
- **撤销**: 新增一条 entry 指向旧 entry(parentId 不变),逻辑上"撤销"中间链
- **压缩**: `compaction` entry 用 summary 替代前段,后段仍以原 parentId 链

## 关键 schema

### Header

```json
{"type":"session","version":3,"id":"uuid","timestamp":"ISO-8601","cwd":"/path","parentSession":"optional"}
```

### Entry base

```json
{"type":"...", "id":"8-char-hex", "parentId":"...", "timestamp":"ISO-8601"}
```

### 8 个 entry 类型

| 类型 | 用途 |
|---|---|
| `message` | 用户/助手/工具结果消息,内嵌 AgentMessage |
| `compaction` | 上下文压缩摘要 + `firstKeptEntryId` + `tokensBefore` |
| `branch_summary` | 分叉上下文,跨分支导航时使用 |
| `custom` | 扩展私有 state(**不进 LLM context**) |
| `custom_message` | 扩展消息(**进 LLM context**,可显隐) |
| `label` | 用户 bookmark |
| `session_info` | session 显示名 |
| `model_change` / `thinking_level_change` | 配置变更追踪 |

## 压缩机制

compaction entry 的 schema:

```json
{
  "type": "compaction",
  "id": "...",
  "parentId": "...",
  "timestamp": "...",
  "summary": "前面 N 条消息的摘要文本",
  "firstKeptEntryId": "压缩后保留的第一条 entry id",
  "tokensBefore": 12345,
  "details": {"readFiles": [...], "modifiedFiles": [...]},
  "fromHook": false
}
```

回放时 `buildSessionContext()` 走 leaf → root 路径:
1. 遇 compaction: emit summary,跳到 `firstKeptEntryId`
2. 遇 message: emit 完整内容
3. 遇其他 entry: 跳过或按 type 处理

**好处**: 上下文从 200K tokens 缩到 30K,信息密度提升,但保留原始边界(可定位消息)。

## Live Event Stream(`--mode json`)

运行时的实时事件流(独立 JSONL):

```
{"type":"turn_start","turnId":"..."}
{"type":"message_start","messageId":"..."}
{"type":"message_update","delta":"..."}     // delta-only
{"type":"message_end","message":{...}}
{"type":"tool_execution_start","tool":"bash","args":{...}}
{"type":"tool_execution_end","result":"..."}
{"type":"turn_end"}
```

**`message_update` 是 delta-only**:不带累积 `partial` 快照,让流大小线性而非二次方。消费端自己做 state machine 累积。

## 与 vault 已有概念

| 概念 | 关系 |
|---|---|
| [[concepts/atomic-state-recovery]] | 同源 —— append-only 是原子性破坏的兜底 |
| [[concepts/durable-session-log]] | dsh 的抽象:append-only SessionEvent + invariant「Model-visible ⟺ logged」 |
| [[synthesis/concepts-atomic-state-recovery × projects-figma-skills-codesign-session-jsonl-recovery]] | CoDesign 用同一模式的 8MB audit log |
| [[concepts/deterministic-agent-memory]] | 互补:前者关注 hot-path 0 LLM 决策稳定性,本概念关注状态破坏后的恢复 |

## 跨域判断

**(J1)** **JSONL tree 是 Agent session 的事实标准** —— CoDesign / pi-coding-agent / Claude Code(线性 JSONL)/ dsh / LangSmith 都在用变体。共识方向:**append-only + 树形 + 压缩**。

**(J2)** **Compaction 比 RAG 优雅** —— RAG 是"重召回"的查询时方案;compaction 是"在源头把信息压成更少 token"的写时方案。对长 session,compaction 是正解(查询时无需再做 embedding + vector search)。

**(J3)** **`message_update` delta-only 是性能关键** —— 流式 UI 性能与流大小成正比,delta-only 让长 session 的实时渲染保持线性。Claude Code / Codex 等 agent 工具的 UI 都是这个模式。

## 相关

- [[references/pi-coding-agent-session-format]] —— 详细 schema
- [[entities/pi-coding-agent]]
- [[concepts/atomic-state-recovery]]
- [[concepts/durable-session-log]]
- [[synthesis/concepts-atomic-state-recovery × projects-figma-skills-codesign-session-jsonl-recovery]]
- [[projects/figma/skills/codesign-session-jsonl-recovery]]