---
title: claude-mem 记忆架构 — 捕获 / 压缩 / 注入三段
category: concepts
tags:
  - memory
  - claude-code
  - mcp
  - concept
sources:
  - https://github.com/thedotmack/claude-mem
  - "本地插件: ~/.claude/plugins/cache/thedotmack/claude-mem/13.12.4/skills/how-it-works/SKILL.md"
  - "Clippings/开源 Claude Code 自动记忆管理插件 Claude-Mem 完整上手攻略.md (兔兔AGI, 2026-03-03, 二手)"
created: 2026-07-29T09:04:00Z
updated: 2026-07-31T12:10:00Z
summary: >-
  claude-mem 把跨会话记忆拆成三段：hook 捕获工具调用 → 便宜模型压成 observation 存 SQLite+Chroma
  → 第二次会话起 SessionStart 自动注入相关记忆。3 层检索省 10× token。
provenance:
  extracted: 0.85
  inferred: 0.1
  ambiguous: 0.05
base_confidence: 0.68
lifecycle: draft
tier: core
lifecycle_changed: "2026-07-29"
---

# claude-mem 记忆架构

[[entities/claude-mem]] 的长期记忆本质是一条 **capture → compress → inject** 的流水线。理解这三段，就理解了「Claude 如何跨会话记住东西」。

## 1. 捕获（capture）

每次 Claude 执行 Read / Edit / Bash，`PostToolUse` hook 异步（`async: true`）把这次调用送进 worker。并非所有工具都记——`CLAUDE_MEM_SKIP_TOOLS` 默认跳过 `ListMcpResourcesTool,SlashCommand,Skill,TodoWrite,AskUserQuestion`（噪音工具）。`PreToolUse(Read)` 还会为读文件补充上下文。

## 2. 压缩 + 存储（compress）

- **压缩模型**：默认 `claude-haiku-4-5`（便宜快），可切 OpenRouter / Gemini。有 tier routing：简单任务用 haiku，复杂总结可路由到 sonnet（`CLAUDE_MEM_TIER_SMART_MODEL`）。
- **observation 结构**：每条含 `title / subtitle / narrative / facts / concepts / files`，并分类型（bugfix ● / feature ◆ / refactor ↻ / decision / discovery / change）——类型定义来自可切换的 **mode**（`code` / `law-study` / `email-investigation` 等，含 30 种语言变体）。
- **存储双库**：
  - **SQLite** — `sessions` / `observations` / `summaries` 三类记录，结构化查询主力。
  - **Chroma 向量库** — 本地模式（`CLAUDE_MEM_CHROMA_MODE=local`，端口 8000），做混合「语义 + 关键词」检索。
- **总结时机**：`Stop` hook 在会话结束时把本会话 observation 汇总成 summary。

## 3. 注入（inject）

- **触发时机**：**记忆注入从项目的第二次会话开始**。第一次会话是"播种"，之后每次 `SessionStart(startup|clear|compact)` hook 把相关历史注入新会话开头。
- **注入量**：默认 `CLAUDE_MEM_CONTEXT_OBSERVATIONS=50` 条 observation + 最近 `CONTEXT_SESSION_COUNT=10` 个会话摘要。
- **前置全库**：跑 `/learn-codebase` 可一次性把整个 repo 读进记忆（约 5 分钟，可选），把认知缓存前置。

### 注入的第二形态：目录级 CLAUDE.md

除了会话开头的 prompt 注入，claude-mem 还把记忆**落到文件系统**——为被操作的项目文件夹自动生成/维护 `CLAUDE.md`（`CLAUDE_MEM_FOLDER_INDEX_ENABLED` 控制）。流程：识别文件夹 → 查该目录相关 observation → 整理成活动时间线（observation ID、时间、类型 emoji、标题、预估 token）→ 写入并用 `<claude-mem-context>` 标签包裹。这利用了 Claude Code 原生「自动读目录 `CLAUDE.md`」的机制，把记忆变成**被动注入**（无需 MCP 调用即被读到）。

关键设计：**`<claude-mem-context>` 标签之外的用户内容在重新生成时保留**——用户可在生成块上下写手工文档、目录指令、架构约定，与自动时间线共存。标签因此既是「自动生成区边界」，也是幂等重写的锚点。

```
# Authentication Module        ← 用户手写，保留
This folder contains auth code.

<claude-mem-context>           ← 系统自动生成/覆盖区
# Recent Activity
| ID | Time | Type | Title | Tokens |
| #1234 | 4:30 PM | 🔵 | Implemented user auth | ~250 |
</claude-mem-context>

## Manual Notes                ← 用户手写，保留
- OAuth providers go in /providers/
```

## 3 层检索（省 10× token）

查历史记忆遵循固定工作流，避免一次拉全量：

1. **`search`** → 返回索引表（ID + 时间 + 类型 + 标题，约 50–100 token/条）
2. **`timeline`** → 围绕某 anchor 取前后 N 条上下文
3. **`get_observations(ids=[…])`** → 只对筛选后的 ID 批量取全文（约 500–1000 token/条）

先筛后取，比无脑拉全文省约 10× token。这与 [[skills/claude-code-token-optimization]] 的思路一致——**检索也是 token 预算的一部分**。

## 数据存哪、隐私边界

全部在 `~/.claude-mem/`（SQLite + Chroma + logs + settings）。默认除压缩 provider 调用外不出机器。可选 cmem.ai Pro 云同步会上传 observation 叙述 + 完整 prompt——是**本地免费 / 上云付费**的明确边界。

## 无尽模式（Endless Mode，beta）— 架构级扩展

标准架构在约 50 次工具调用后会触上下文上限。beta 的**无尽模式**用**仿生记忆**思路把这一上限推到约 **1000 次工具使用（~20 倍）**：不再让原始工具输出在窗口里累积，而是**实时压缩每次调用的输出**，把 token 用量削减约 **95%**，从而把上下文增长的扩展复杂度从 **O(N²) 降到 O(N)**。

这是把三段流水线里的「压缩」从**会话结束时的旁路**提前到**每次工具调用后的实时同步路径**——代价随之显性化：每次调用生成 observation 加 **60–90 秒延迟**。取舍逻辑：跨天/周的深度会话里延迟摊薄可接受；快速连续调用时延迟成瓶颈。经 Web 查看器（[[entities/claude-mem]]）→ 设置 → 版本频道切 beta 启用。

## 相关页面

- [[entities/claude-mem]] — 插件本体
- [[concepts/claude-code-hooks-lifecycle]] — 驱动这条流水线的 6 个 hook
- [[skills/claude-mem-memory-usage]] — 把架构落成日常操作
- [[concepts/prompt-caching]] — 同属「上下文复用」哲学（KV 缓存 vs 跨会话记忆）

## Related

- [[synthesis/Research: claude-mem 长期记忆]] — 综合页:capture→compress→inject 流水线的端到端实操
