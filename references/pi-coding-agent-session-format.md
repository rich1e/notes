---
title: "pi-coding-agent Session File Format — JSONL Tree"
category: references
tags: [pi-coding-agent, jsonl, session-format, tree-structure, compaction]
sources:
  - "https://hochej.github.io/pi-mono/coding-agent/session"
source_url: "https://hochej.github.io/pi-mono/coding-agent/session"
created: 2026-08-24
updated: 2026-08-24
summary: pi-coding-agent session 是 JSONL tree(v3 header + entries with id/parentId);entry 类型 8 种(message/compaction/branch_summary/custom/custom_message/label/session_info/thinking_level_change/model_change);compaction 用 firstKeptEntryId 标记边界。open-codesign v0.2.0 直接复用此格式存 design session。
base_confidence: 0.9
provenance:
  extracted: 0.85
  inferred: 0.10
  ambiguous: 0.05
lifecycle: draft
lifecycle_changed: 2026-08-24
tier: supporting
---

# pi-coding-agent Session File Format

open-codesign v0.2.0 用 pi-coding-agent 的 session 格式存 design session 历史。本页是该格式的参考。

## 存储路径

```
~/.pi/agent/sessions/<encoded-cwd>/<timestamp>_<id>.jsonl
```

open-codesign 在 `userData/sessions/<designId>/...` 下复用此结构。

## Header(第一行)

```json
{"type":"session","version":3,"id":"uuid","timestamp":"ISO-8601","cwd":"/path","parentSession":"optional-path"}
```

- `parentSession` 可选,`/fork` 或 `newSession({ parentSession })` 时存在
- 版本演进: v1 线性 → v2 树形 → v3 重命名 `hookMessage` → `custom`

## SessionEntry Base

```
type: string
id: string                    // 8-char hex
parentId: string | null       // 第一条 entry 的 parentId 为 null
timestamp: string             // ISO timestamp
```

所有 entry(除 header)都基于此。

## Entry 类型

### 通用(从 pi-ai)

**`SessionMessageEntry`** (`type: "message"`) —— 包裹 AgentMessage,`message` 字段是 union 之一

**`ModelChangeEntry`** (`type: "model_change"`) —— `provider` + `modelId`

**`ThinkingLevelChangeEntry`** (`type: "thinking_level_change"`) —— `thinkingLevel` (e.g. `"high"`)

### 压缩与分支

**`CompactionEntry`** (`type: "compaction"`):
- `summary: string`
- `firstKeptEntryId: string` —— 压缩后保留的第一条 entry
- `tokensBefore: number`
- `details?` —— 可选实现细节(e.g. `{ readFiles, modifiedFiles }`)
- `fromHook?` —— `true` 表示 extension-generated

**`BranchSummaryEntry`** (`type: "branch_summary"`):
- `fromId: string`
- `summary: string`
- `details?` + `fromHook?`

### 扩展

**`CustomEntry`** (`type: "custom"`) —— 扩展 state,**不在 LLM context**:
- `customType: string`
- `data?: any`

**`CustomMessageEntry`** (`type: "custom_message"`) —— 扩展消息,**在 LLM context**:
- `customType: string`
- `content: string | (TextContent | ImageContent)[]`
- `display: boolean`
- `details?`

### 用户交互

**`LabelEntry`** (`type: "label"`) —— entry 上的 bookmark:
- `targetId: string`
- `label: string | undefined`

**`SessionInfoEntry`** (`type: "session_info"`) —— session 显示名:
- `name: string`

## AgentMessage Union

```
AgentMessage =
  | UserMessage
  | AssistantMessage
  | ToolResultMessage
  | BashExecutionMessage
  | CustomMessage
  | BranchSummaryMessage
  | CompactionSummaryMessage;
```

### Base (pi-ai)

- `UserMessage` — `role: "user"`, `content: string | (TextContent|ImageContent)[]`, `timestamp`
- `AssistantMessage` — `role: "assistant"`, `content: (TextContent|ThinkingContent|ToolCall)[]`, `api`, `provider`, `model`, `usage`, `stopReason`, `errorMessage?`, `timestamp`
- `ToolResultMessage` — `role: "toolResult"`, `toolCallId`, `toolName`, `content`, `details?`, `isError: boolean`, `timestamp`

### Extended (pi-coding-agent)

- `BashExecutionMessage` — `role: "bashExecution"`, `command`, `output`, `exitCode`, `cancelled`, `truncated`, `fullOutputPath?`, `excludeFromContext` (true for `!!`), `timestamp`
- `CustomMessage` — `role: "custom"`, `customType`, `content`, `display`, `details?`, `timestamp`
- `BranchSummaryMessage` — `role: "branchSummary"`, `summary`, `fromId`, `timestamp`
- `CompactionSummaryMessage` — `role: "compactionSummary"`, `summary`, `tokensBefore`, `timestamp`

## Content Blocks

| 类型 | 字段 |
|---|---|
| `TextContent` | `type: "text"`, `text: string` |
| `ImageContent` | `type: "image"`, `data: base64 string`, `mimeType: string` |
| `ThinkingContent` | `type: "thinking"`, `thinking: string` |
| `ToolCall` | `type: "toolCall"`, `id`, `name`, `arguments: Record<string, any>` |

## 压缩回放机制

`buildSessionContext()` 从当前 leaf 走回 root。路径上有 `compaction` entry 时:

1. 先 emit summary
2. 然后从 `firstKeptEntryId` 到 compaction 之间的 message
3. 然后压缩后的新 message

这样既保留上下文边界,又能用 summary 节省 token。

## JSON Stream Mode(Live Events)

`pi --mode json` 实时事件流(也 JSONL)。事件类型:

| 类别 | 事件 |
|---|---|
| Agent lifecycle | `agent_start`, `agent_end` |
| Turn lifecycle | `turn_start`, `turn_end` |
| Message lifecycle | `message_start`, `message_update` (delta), `message_end` |
| Tool execution | `tool_execution_start`, `tool_execution_update`, `tool_execution_end` |
| Queue | `queue_update` (steering + follow-up) |
| Compaction | `compaction_start`, `compaction_end` |

`message_update` 是 **delta-only** —— 不带累积 `partial` 快照,让流大小线性而非二次方。

## 与 vault 已有概念

- [[concepts/atomic-state-recovery]] —— 同哲学:append-only JSONL 是状态破坏后的二次证据
- [[synthesis/concepts-atomic-state-recovery × projects-figma-skills-codesign-session-jsonl-recovery]] —— CoDesign 用同一格式
- [[concepts/durable-session-log]] —— dsh 同源 (append-only SessionEvent + invariant「Model-visible ⟺ logged」)

## 相关

- [[references/open-codesign-readme]]
- [[synthesis/Research: open-codesign]]
- [[concepts/jsonl-session-tree]] —— 抽象概念
- [[concepts/agentic-design]] —— v0.2.0 agent loop