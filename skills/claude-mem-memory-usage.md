---
title: 在 Claude 中用 claude-mem 管理长期记忆 — 安装、检索、知识 Agent、调优
category: skills
tags:
  - claude-code
  - memory
  - mcp
  - skill
sources:
  - https://github.com/thedotmack/claude-mem
  - "本地插件 v13.12.4 skills/ + settings.json"
created: 2026-07-29T09:04:00Z
updated: 2026-07-29T09:04:00Z
summary: >-
  claude-mem 实操手册：插件市场装（别用 npm -g）→ 第二次会话起自动注入记忆 → 用 search/timeline/
  get_observations 3 层查历史 → /knowledge-agent 建知识大脑 → settings.json 调优。
provenance:
  extracted: 0.9
  inferred: 0.07
  ambiguous: 0.03
base_confidence: 0.7
lifecycle: draft
lifecycle_changed: "2026-07-29"
---

# 在 Claude 中用 claude-mem 管理长期记忆

回答「如何在 Claude 中用 [[entities/claude-mem]] 管理长期记忆」的完整操作指南。原理见 [[concepts/claude-mem-memory-architecture]]，hook 机制见 [[concepts/claude-code-hooks-lifecycle]]。

## 1. 安装（关键：别用 npm -g）

```bash
# 推荐：插件市场，自动注册 hook
/plugin marketplace add thedotmack/claude-mem
/plugin install claude-mem

# 或 CLI 安装器
npx claude-mem install
```

⚠️ `npm install -g claude-mem` **只装 SDK 库、不注册 hook**——记忆不会生效。装完确认 `~/.claude-mem/settings.json` 存在。

**要求**：Node ≥ 20.12；Bun、uv 缺失会自动装；SQLite3 已 bundled。

## 2. 让它开始"记住"

- **零操作，自动运行**：装好后每次会话的 Read/Edit/Bash 都被自动压成 observation，无需手动保存。
- **记忆注入从「第二次会话」开始**：第一次会话是播种，之后新会话开头自动带上相关历史。
- **前置整个代码库（可选）**：新项目里跑 `/learn-codebase`，约 5 分钟把整个 repo 读进记忆，之后开发都有全局上下文。

## 3. 查历史记忆 — 3 层工作流（省 10× token）

问「我们上次怎么解决的 X？」「上周做了啥？」时，用 `mem-search` skill 的 MCP 工具，**永远先筛后取**：

```text
# ① 搜索：拿索引（ID+标题，~50-100 token/条）
search(query="authentication", limit=20, project="my-project", obs_type="bugfix")

# ② 时间线：围绕某条取前后文
timeline(anchor=11131, depth_before=3, depth_after=3)

# ③ 取全文：只对筛出的 ID 批量取（~500-1000 token/条）
get_observations(ids=[11131, 10942])
```

`search` 参数：`query` / `limit`(≤100) / `project` / `type`(observations|sessions|prompts) / `obs_type`(bugfix,feature,decision,discovery,change) / `dateStart` / `dateEnd` / `orderBy`(date_desc|date_asc|relevance)。

> 直接用自然语言问 Claude「我们上次怎么处理 auth 的?」也会触发 `mem-search` skill 自动走这套流程。

## 4. 建「知识大脑」— knowledge-agent

想要综合回答而非原始记录时，用 `/knowledge-agent` 把 observation 编译成可对话语料：

```text
build_corpus name="hooks-expertise" description="hooks 生命周期一切" concepts="hooks" limit=500
prime_corpus name="hooks-expertise"
query_corpus name="hooks-expertise" question="5 个生命周期 hook 分别何时触发?"
```

- **聚焦的语料最好用**——「hooks 架构」胜过「所有东西」
- prime 一次可多次 query；语料漂了就 `reprime_corpus`；有新记忆就 `rebuild_corpus` 后重新 prime

## 5. 调优（`~/.claude-mem/settings.json`）

实测本机关键项：

| 键 | 默认/本机值 | 作用 |
|---|---|---|
| `CLAUDE_MEM_MODEL` | `claude-haiku-4-5` | 压缩用模型（便宜快） |
| `CLAUDE_MEM_CONTEXT_OBSERVATIONS` | `50` | 每次注入多少条 observation |
| `CLAUDE_MEM_CONTEXT_SESSION_COUNT` | `10` | 注入最近几个会话摘要 |
| `CLAUDE_MEM_SKIP_TOOLS` | 见下 | 不记录的噪音工具 |
| `CLAUDE_MEM_MODE` | `code` | observation 分类模式（可切 law-study 等 + 30 语言） |
| `CLAUDE_MEM_EXCLUDED_PROJECTS` | 空 | 按项目排除记忆 |
| `CLAUDE_MEM_TIER_ROUTING_ENABLED` | `true` | 简单用 haiku、复杂路由 sonnet |

`SKIP_TOOLS` 默认跳过 `ListMcpResourcesTool,SlashCommand,Skill,TodoWrite,AskUserQuestion`。

## 6. 隐私 & 卸载

- **默认全本地**（`~/.claude-mem/`）；`<private>` 标签排除敏感内容不入库。
- **卸载干净**：`npx claude-mem uninstall` 移除全部数据。
- **可选云同步**（cmem.ai Pro，付费）会上传 observation 叙述 + 完整 prompt——按需开，隐私边界要清楚。

## 常见坑

1. `npm -g` 装了但记忆没生效 → 用插件市场或 `npx claude-mem install` 重装。
2. 第一次会话没看到注入的记忆 → 正常，**从第二次会话才注入**。
3. 查历史一次拉爆 token → 走 search→timeline→get_observations 三层，别直接 get 全量。

## 相关页面

- [[entities/claude-mem]] / [[concepts/claude-mem-memory-architecture]] / [[concepts/claude-code-hooks-lifecycle]]
- [[skills/claude-code-token-optimization]] — 记忆检索也是 token 预算的一部分
- [[skills/claude-code-settings]] — 配置作用域
