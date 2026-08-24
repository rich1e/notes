---
title: "Agentic Design — open-codesign v0.2.0 的 workspace-backed agent 抽象"
category: concepts
tags: [open-codesign, agentic-design, agent-loop, workspace, permissioned-tools, concept]
sources:
  - "[[references/open-codesign-readme]]"
  - "[[references/open-codesign-changelog]]"
  - "[[references/open-codesign-prompt-system-deepwiki]]"
created: 2026-08-24
updated: 2026-08-24
summary: v0.2.0 Agentic Design 把 open-codesign 从一次性生成器转向 workspace-backed 设计 agent:每个 design 拥有真实 workspace + JSONL 历史 + permissioned tool use + DESIGN.md shared memory + 8 专用工具。核心抽象:设计工作是有状态的、可恢复的 agent 任务而非无状态请求-响应。
base_confidence: 0.85
provenance:
  extracted: 0.75
  inferred: 0.20
  ambiguous: 0.05
lifecycle: draft
lifecycle_changed: 2026-08-24
tier: supporting
relationships:
  - target: "[[entities/open-codesign]]"
    type: related_to
  - target: "[[entities/pi-coding-agent]]"
    type: derived_from
  - target: "[[concepts/jsonl-session-tree]]"
    type: uses
  - target: "[[concepts/design-md-shared-memory]]"
    type: uses
  - target: "[[concepts/skill-progressive-disclosure]]"
    type: uses
---

# Agentic Design — open-codesign v0.2.0

## 核心转变(v0.1 → v0.2)

| 维度 | v0.1.x 一次性生成 | v0.2.0 Agentic Design |
|---|---|---|
| **状态** | SQLite + 加密 TOML 密封 app state | 真实 workspace 文件夹 + JSONL 历史 |
| **生成模型** | 请求-响应 | Agent loop + tool use |
| **可恢复** | 单次失败需重做 | JSONL tree 可重放 / 分叉 / 压缩 |
| **token 缓存** | 弱 | 内置 JSON stream delta + compaction |
| **工具** | 内置 RPC | 8 专用工具 + pi 内置工具集 |
| **样式记忆** | 每次重提 | DESIGN.md 文件持久化 |

## 三大支柱

### 1. Workspace-backed sessions

每个 design 拥有真实文件系统文件夹:

```
<workspace>/
├── AGENTS.md              # 行为约定
├── DESIGN.md              # 品牌 token + 设计系统决策
├── session.jsonl          # pi session 树(完整事件流)
├── sources/               # 生成的源代码(JSX / TS)
├── assets/                # 图片、字体
└── exports/               # 导出产物(HTML / PDF / PNG)
```

**关键**: 状态在磁盘,不在 app state。崩溃 = 文件恢复,无数据丢失。

### 2. Permissioned agent loop

工具集分两层,均经过 permission UI:

**pi 内置 7 个**(只读 + 基础编辑):
- `read` / `write` / `edit` / `bash` / `grep` / `find` / `ls`

**open-codesign 专用 8 个**(设计领域):
| 工具 | 用途 |
|---|---|
| `ask` | 向用户提问澄清 |
| `scaffold` | 加载 starter code 模板 |
| `skill` | 按需加载 skill body(YAML+markdown) |
| `preview` | 渲染预览 |
| `gen_image` | AI 图像生成(OpenAI / OpenRouter / ChatGPT) |
| `tweaks` | 调整可调滑块 |
| `todos` | 任务列表 |
| `done` | 标记任务完成 |

Permission UI 在每次工具调用前让用户确认(类 Claude Code 的 `Bash` 授权)。

### 3. DESIGN.md shared memory

DESIGN.md 是**机器可读**的设计决策文件 —— 不是"模型记忆里的某条 prompt"。

**关键差异**:
- prompt 模型记忆: 隐式、易丢、跨 session 不共享
- DESIGN.md: 显式文件、可 git 版本、跨 session 共享、可人类编辑

模型在每次生成前读 DESIGN.md,提取 token(colors / typography / spacing / component patterns),作为 prompt 的一部分。

## 与 vault 已有概念的关系

- [[concepts/atomic-state-recovery]] —— workspace 文件 + JSONL tree 是其实践
- [[synthesis/concepts-atomic-state-recovery × projects-figma-skills-codesign-session-jsonl-recovery]] —— 同哲学另一面
- [[concepts/durable-session-log]] —— dsh 同源 (append-only SessionEvent + invariant「Model-visible ⟺ logged」)
- [[concepts/design-md-shared-memory]] —— 完整 vault-side 抽象

## 跨域判断

**(J1) 设计工具正在走 IDE 走过的路** —— 从"打开编辑器写代码" 到 "AI agent 在 workspace 里持续工作"。open-codesign 在设计领域做的是 Claude Code 在代码领域做的同一件事。

**(J2) Permission UI 是产品差异点** —— 技术上 agent loop + tool harness 是基建(pi-coding-agent 给的);产品差异在 UX 层(什么时候弹权限弹窗、怎么呈现 allow/deny/always-allow-for-session 三选项)。

**(J3) DESIGN.md 是反 prompt engineering 的胜利** —— 把"对齐品牌指南"从 prompt engineering 升级为 token 文件 + 版本控制。design system 是设计领域的 schema,DESIGN.md 是其 compiled form,LLM 读它就像 IDE 读 tsconfig。

## 与 vault 已有 figma 项目

vault 中 [[projects/figma/figma]] 是用户本地的 figma 项目,运行于 open-codesign 客户端。[[projects/figma/skills/codesign-session-jsonl-recovery]] 是其 session JSONL 恢复技巧 —— 与本概念的 JSONL tree 同源。

## 相关

- [[entities/open-codesign]]
- [[entities/pi-coding-agent]]
- [[references/open-codesign-readme]]
- [[references/open-codesign-changelog]]
- [[concepts/jsonl-session-tree]]
- [[concepts/design-md-shared-memory]]
- [[concepts/skill-progressive-disclosure]]
- [[projects/figma/figma]]