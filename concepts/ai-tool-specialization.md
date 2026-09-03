---
title: "AI 工具栈的专业化分工"
category: concepts
tags: [ai-coding, ai-agents, mcp, concept, Deepseek]
summary: "让每个 AI 工具承担自己擅长的窄任务（Stitch = 视觉、Claude Code = 逻辑），通过 MCP 做协议级协作，而不是堆砌一个全能的 mega-agent。这是从旧模式（描述→生成→修）转向新模式（拆任务→专业化→组合）的关键。"
sources:
  - "https://medium.com/devsecops-ai/how-google-stitch-claude-codes-mcp-integration-changed-the-way-i-build-products-63ecb8ed7f5a"
created: "2026-07-28T00:00:00Z"
updated: "2026-07-28T00:00:00Z"
tier: supporting
lifecycle: draft
lifecycle_changed: "2026-07-28"
base_confidence: 0.40
provenance:
  extracted: 0.50
  inferred: 0.45
  ambiguous: 0.05
relationships:
  - target: "[[concepts/design-system-as-ai-context]]"
    type: related_to
  - target: "[[concepts/mcp-server-protocol-quirks]]"
    type: related_to
  - target: "[[entities/google-stitch]]"
    type: related_to
  - target: "[[entities/claude-code]]"
    type: related_to
  - target: "[[projects/flow-design-system/concepts/ai-vs-core-component-source-routing]]"
    type: related_to
---

# AI 工具栈的专业化分工

> 把活拆给擅长的工具，让 MCP 做翻译，而不是造一个"什么都会但什么都半吊子"的 mega-agent。

## 旧模式 vs 新模式

| 维度 | 旧模式（全能 mega-agent） | 新模式（专业化分工） |
|------|--------------------------|---------------------|
| 工具数 | 一个 agent 干所有事 | 每个 agent 守一段（视觉 / 逻辑 / 数据） |
| 上下文分配 | 全部塞进同一个上下文窗口 | 按任务分发，token 不重叠浪费 |
| 衔接方式 | 人工复制粘贴 | MCP 等协议级自动交接 |
| 失败模式 | "padding 多一点" 让 agent 反复重写 | 设计 token 一锤定音，agent 读 token 表 |
| 工具开发压力 | 一个 agent 要会所有事 | 每个工具可以专精 |

Sachin Sharma 在 Stitch + Claude Code 文末点出：

> "大多数用 AI 编码工具的人还在用旧模型——描述需求、生成代码、修、再生成。**它把 token 烧在了错的地方。**更好的模型是**专业化**——让每个工具做它真正擅长的事。"

## 三个关键判断点

### 1. 这件事谁真正擅长

问自己：在没有 AI 的时候，哪个工具/人做这一步最好？

- 视觉决策 → 设计工具（Stitch / Figma AI）
- 逻辑与代码 → Claude Code / Cursor
- 数据查询 → NotebookLM MCP / 数据库 MCP
- 构建与 CI → shell agent 或专门的 devops agent

把这件事交给它，不要绕道。

### 2. 协议能否去掉人工搬运

判断标准：**当前任务流是否依赖"人把 A 的输出复制到 B 的输入"**？如果是，就要找一条协议或 MCP server 把这一步自动化。

- 设计稿 → 代码：Stitch MCP
- 笔记本问答 → Claude：NotebookLM MCP（见 [[skills/notebooklm-mcp-setup]]）
- 文档查询 → Claude：Stitch MCP、NotebookLM MCP

### 3. 上下文是否能复用

专业化分工的杠杆来自**每个 agent 的上下文独立且互不污染**：

- Stitch 的上下文：屏幕描述 + 视觉 token
- Claude Code 的上下文：项目代码 + 设计 token + 任务说明

两个上下文重叠越少，token 利用率越高。[[concepts/design-system-as-ai-context]] 描述的 `DESIGN.md` 是这一原则的具体实现——视觉与逻辑共享一份硬约束文件，但各自的会话上下文保持精简。

## 适用边界与反例

不是所有任务都该拆：

- **简单一行修复**（改 typo、加 console log）：直接让 Claude Code 干，搭一套分工是过度工程。
- **探索性原型**（不知道自己想要什么）：一个全能 agent 反而更省心——因为此时还不知道边界在哪。
- **真正的协同场景**：当**任务边界已清晰**（视觉归 Stitch、逻辑归 Claude Code），专业化分工才有意义。

## 与 MCP 生态的关系

MCP 是专业化分工的**协议基础**——它让"窄而专"的 agent 能以标准化方式拼装：

- 每个服务（设计、数据库、文档、CI）暴露一个 MCP server。
- 每个 agent（Claude Code、其他终端 agent）作为 MCP client。
- 组合灵活：换工具不换协议。

没有 MCP，专业化分工会被"每个工具的私有 API 集成"拖累；有了 MCP，分工才成为可组装的基础设施。

## 相关页面

- [[misc/web-medium-com-devsecops-ai-how-google-stitch-claude-codes-mcp-integration]] — 实操来源
- [[concepts/design-system-as-ai-context]] — 视觉与逻辑边界的硬约束载体
- [[entities/google-stitch]] — 视觉侧的代表
- [[entities/claude-code]] — 逻辑侧的代表
- [[concepts/mcp-server-protocol-quirks]] — 让分工可组装的协议层基础

## Related

- [[synthesis/concepts-ai-tool-specialization × entities-oh-my-openagent]] — synthesis

- [[synthesis/concepts-ai-tool-specialization × entities-bmad-method]] — synthesis
