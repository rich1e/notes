---
title: "pi-coding-agent — Mario Zechner 的 agent loop 框架"
category: entities
tags: [pi-coding-agent, mariozechner, pi-ai, agent-loop, jsonl, session-format]
sources:
  - "[[references/pi-coding-agent-session-format]]"
  - "[[references/open-codesign-readme]]"
created: 2026-08-24
updated: 2026-08-24
summary: pi-coding-agent(@mariozechner/pi-ai 同作者)是极简主义 coding agent 框架,提供 session JSONL tree + tool harness + JSON stream mode events。open-codesign v0.2.0 直接以此为基础搭建设计领域 agent。
base_confidence: 0.85
provenance:
  extracted: 0.80
  inferred: 0.15
  ambiguous: 0.05
lifecycle: draft
lifecycle_changed: 2026-08-24
tier: supporting
relationships:
  - target: "[[entities/open-codesign]]"
    type: related_to
  - target: "[[entities/mariozechner]]"
    type: developed_by
  - target: "[[concepts/jsonl-session-tree]]"
    type: implements
---

# pi-coding-agent

## 概述

`@mariozechner/pi-coding-agent`(同作者有 `@mariozechner/pi-ai`)是极简主义 coding agent 框架,open-codesign v0.2.0 直接以其为 AI 运行时。

## 仓库

- **GitHub**: `badlogic/pi-mono`(monorepo,含 pi-ai + pi-coding-agent)
- **文档**: `pi.dev`

## 关键能力

| 能力 | 解释 |
|---|---|
| **Session JSONL tree** | header + entries (id/parentId 形成树),8 个 entry 类型,compaction with `firstKeptEntryId` |
| **Tool harness** | agent 通过 tool 调用 bash/read/write/edit/grep/find/ls 等内置工具 |
| **JSON stream mode** | `--mode json` 实时事件流,`message_update` 是 delta-only |
| **BYOK providers** | 多 provider 抽象(Claude / GPT / Gemini / 自定义 HTTP) |
| **Compaction** | 自动压缩长 session,保留关键 message + summary |

## Session 路径

```
~/.pi/agent/sessions/<encoded-cwd>/<timestamp>_<id>.jsonl
```

## 源码结构

```
packages/coding-agent/src/core/
  ├── session-manager.ts     # SessionManager + entry types
  ├── messages.ts            # Extended message types
packages/ai/src/
  └── types.ts               # Base message types
packages/agent/src/
  └── types.ts               # AgentMessage union
packages/coding-agent/docs/
  ├── session.md             # Session format
  └── json.md                # JSON stream mode
```

## 与 open-codesign 的集成

open-codesign 在 pi-coding-agent 之上叠加 8 个领域专用工具(`ask` / `scaffold` / `skill` / `preview` / `gen_image` / `tweaks` / `todos` / `done`),通过 permission UI gate 所有工具调用。

## 关键哲学

- **JSONL tree 而非线性日志** —— 支持分叉、撤销、压缩
- **delta-only 事件流** —— 流大小线性而非二次方,长 session 实时 UI 可用
- **compaction 而非 RAG** —— 源头压缩信息,查询时无需 embedding search
- **BYOK 而非托管** —— 用户控制 provider 选择

## 相关

- [[entities/mariozechner]] —— 作者
- [[entities/open-codesign]] —— 上层应用
- [[concepts/jsonl-session-tree]] —— session 格式抽象
- [[concepts/agentic-design]] —— open-codesign 上的实现
- [[references/pi-coding-agent-session-format]]