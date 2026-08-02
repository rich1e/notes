---
title: 开源 Claude Code 自动记忆管理插件 Claude-Mem 完整上手攻略
source: https://mp.weixin.qq.com/s?__biz=MjM5NzA1NzMyOQ==&mid=2247486757&idx=1&sn=c459993de81e2c5ec77c80840b22972c&scene=21&poc_token=HDL-a2qjunMFULDmy5GMhSdNe2W9utfe8ZZuXLHt
author:
  - "[[兔兔AGI]]"
published:
created: 2026-07-31
description: Claude-mem 是一个开源的 Claude Code 插件，用来解决跨会话上下文丢失的问题。它会自动记录工具调用中的关键信息，将其压缩成语义摘要，并在后续会话中按需提供，从而让项目相关的上下文得以持续保留。
tags:
  - clippings
  - "#claude-mem"
  - memory
---
兔兔AGI 技术极简主义 *2026年3月3日 11:23*

用过 Claude Code 的朋友应该都有过这种经历：每次关闭终端或断开连接后，下次再打开项目时，Claude 就像失忆了一样，完全不记得之前的对话内容。你的项目架构、最近的代码重构决策、调试时发现的问题、以及各种设计模式，统统都得重新解释一遍。这不仅消耗了大量 token，更打断了开发思路的连续性。

目前开发者们通常会通过手动维护 `CLAUDE.md` 文件、在单独的文档里记笔记、或者在每次会话开始时重新介绍项目上下文来应对这个问题。但这些方法都很脆弱、耗时，而且永远无法完整捕捉开发历史的全貌。

Claude-mem 正是为了解决这一问题而设计的。它能够自动捕获每次会话中的工具调用结果，将其压缩成语义化的记忆摘要，并在后续会话中智能注入相关上下文。

## 什么是 Claude-mem

![[assets/Clippings/开源 Claude Code 自动记忆管理插件 Claude-Mem 完整上手攻略/IMG-20260731225953506.png|图片]]

Claude-mem 是一个开源的 Claude Code 插件，用来解决跨会话上下文丢失的问题。它会自动记录工具调用中的关键信息，将其压缩成语义摘要，并在后续会话中按需提供，从而让项目相关的上下文得以持续保留。

简单来说，它让 Claude 在会话结束或重新连接后，仍然「记得」你正在做什么。

### 核心能力

- • **自动记录** ：无需人工介入，所有工具调用的关键信息都会被自动捕获
- • **语义压缩** ：将上千 token 的原始输出压缩为约 500 token 的可复用摘要
- • **按需检索** ：通过 MCP 工具实现三层渐进式检索，减少不必要的上下文加载
- • **目录级上下文** ：为项目目录自动生成并维护 `CLAUDE.md`
- • **隐私保护** ：支持使用 `<private>` 标签隔离敏感内容

官方数据显示，相比手动维护上下文，这套机制在单个会话中可节省约 2,250 个 token，整体效率提升接近一个数量级。

## 核心架构设计

Claude-mem 的核心是一套 **持久化的记忆压缩机制** 。它直接接入 Claude Code 的执行流程，自动收集工具调用产生的结果，并通过 **Claude Agent SDK** 将大量上下文整理成精炼、可检索的语义记录。

这些记录会按决策、修复、功能等类型归类，同时关联相关文件和概念，最终存储在支持全文搜索的本地 SQLite 数据库中，用于跨会话恢复上下文。

### 核心组件

- • **生命周期钩子（共 6 个脚本）** ： `SessionStart` 、 `UserPromptSubmit` 、 `PostToolUse` 、 `Stop` 、 `SessionEnd`
- • **智能安装** ：缓存依赖检查器（前置钩子脚本，不属于生命周期钩子）
- • **Worker 服务** ：运行在端口 `37777` 的 HTTP API，包含 Web 查看器 UI 和 10 个搜索端点，由 Bun 管理
- • **SQLite 数据库** ：存储会话记录、观察结果和摘要
- • **mem-search 技能** ：支持渐进式自然语言查询
- • **Chroma 向量数据库** ：结合语义搜索与关键词搜索，用于智能上下文检索

### 工作原理

```
┌─────────────────────────────────────────────────────────────┐
│ Session Start → Inject context from last 10 sessions        │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ User Prompts → Create session, save user prompts            │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Tool Executions → Capture observations (Read, Write, etc.)  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Worker Processes → Extract learnings via Claude Agent SDK   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Session Ends → Generate summary, ready for next session     │
└─────────────────────────────────────────────────────────────┘
```

系统会在五个关键节点自动记录上下文，用来支撑跨会话记忆：

| Hook 名称 | 触发时机 | 作用 |
| --- | --- | --- |
| SessionStart | 会话开始 | 注入之前会话中相关的上下文信息 |
| UserPromptSubmit | 用户提交指令 | 记录查询内容，用于后续模式分析 |
| PostToolUse | 工具调用完成 | 捕获工具执行过程及输出结果 |
| Stop | Claude 完成响应 | 汇总当前会话，生成摘要 |
| SessionEnd | 会话结束 | 持久化存储数据并执行清理 |

### 压缩机制

一次工具调用的原始输出通常在 1,000–10,000 token 之间。Claude-mem 会通过 Claude Agent SDK，将这些内容压缩为约 500 token 的语义化记录，用于后续检索和复用。

### 核心优势

这套架构采用的是 **渐进式披露** 思路，通过分层的记忆检索，在上下文覆盖范围和 token 成本之间取得平衡。

系统不会一次性加载全部历史信息，而是根据当前任务逐层取用真正相关的内容，这也是它能显著降低 token 消耗的关键原因。

## 快速上手指南

### 系统要求

- • **Node.js** ：18.0.0 或更高版本
- • **Claude Code** ：支持插件的最新版本
- • **Bun** ：JavaScript 运行时与进程管理器（如缺失会自动安装）
- • **SQLite 3** ：用于持久化存储（已内置，无需额外安装）

### 方式一：插件市场（推荐）

这是最简单的方式，直接从市场安装

```bash
# 从插件市场添加
/plugin marketplace add thedotmack/claude-mem

# 安装插件
/plugin install claude-mem
```

安装完成后，重启 Claude Code 即可生效。

![[assets/Clippings/开源 Claude Code 自动记忆管理插件 Claude-Mem 完整上手攻略/IMG-20260731225953596.png|图片]]

插件会自动完成以下工作：

- • 下载并配置预编译的二进制文件
- • 安装所需依赖（包括 Bun 和 SQLite）
- • 注册会话生命周期相关的钩子
- • 在首次会话启动时拉起 Worker 服务

### 方式二：从源码构建

如果你需要开发测试或者使用 beta 功能，可以直接从 GitHub 源码构建：

```
# 克隆仓库
git clone https://github.com/thedotmack/claude-mem.git
cd claude-mem

# 安装依赖
npm install

# 构建项目
npm run build

# 启动 Worker 服务
npm run worker:start
```

这种方式让你可以直接修改代码，或者使用一些官方还没推正式版的新特性。

### 验证安装

安装完成后，可通过以下步骤确认系统是否正常运行：

**检查插件状态** ：

```bash
cat plugin/hooks/hooks.json
```

**确认 Worker 服务运行** ：

```
curl http://localhost:37777/api/health
```

**查看 Worker 日志** ：

```
npm run worker:logs
```

**测试上下文注入** ：

启动一个新的 Claude Code 会话，你应该能看到初始提示中自动加载了来自之前会话的上下文信息。

### 数据存储与配置

#### 存储位置

Claude-mem 的所有数据都存储在本地 `~/.claude-mem/` 目录中：

| 文件/目录 | 用途 |
| --- | --- |
| `claude-mem.db` | SQLite 数据库（支持 FTS5 全文搜索） |
| `.worker.pid` | Worker 进程 ID 文件 |
| `.worker.port` | Worker 端口文件 |
| `logs/` | 日志文件目录 |
| `settings.json` | 配置文件 |

#### 自定义数据目录

如果想改变默认数据存储位置，可以通过环境变量设置：

```
export CLAUDE_MEM_DATA_DIR=/custom/path
```

#### 关键配置项

主要配置存放在 `~/.claude-mem/settings.json` ：

- • `CLAUDE_MEM_CONTEXT_OBSERVATIONS` ：会话开始时注入的观察记录数量，默认值为 50
- • `CLAUDE_MEM_FOLDER_INDEX_ENABLED` ：是否启用文件夹级 `CLAUDE.md` 的自动生成

## MCP 记忆搜索工具

Claude-mem 通过 **MCP（Model Context Protocol）** 提供了四个搜索工具，采用 **三层渐进式检索** ，在尽量节省 token 的同时保证检索相关性。

### 三层检索流程

```
1. search：获取紧凑索引（含 ID）
           ↓ ~50-100 token/结果
2. timeline：获取特定观察的时间上下文
           ↓ 了解前后关联
3. get_observations：获取筛选后的完整观察详情
           ↓ ~500-1,000 token/结果
```

**第一层：搜索（索引）**

首先执行搜索，获取轻量级索引结果：

```
search(query="authentication bug", type="bugfix", limit=10)
```
- • **返回内容** ：ID、标题、日期、类型的精简表格
- • **成本** ：每条结果约 50–100 token
- • **目的** ：快速概览相关观察内容，在获取详情前筛选目标

**第二层：时间线（上下文）**

在获取索引后，可以查看特定观察的前后事件：

```
timeline(anchor=<observation_id>, depth_before=3, depth_after=3)
```

或者结合搜索直接生成时间线：

```
timeline(query="authentication", depth_before=2, depth_after=2)
```
- • **返回内容** ：展示选中观察及其前后事件的时序视图
- • **成本** ：根据 `depth_before` 和 `depth_after` 参数而定
- • **目的** ：理解事件前后脉络，便于判断因果关系和逻辑顺序

**第三层：获取观察结果（详情）**

在筛选到目标 ID 后，可以获取完整的观察记录：

```
get_observations(ids=[123, 456, 789])
```
- • **返回内容** ：每条观察的完整详情，包括叙述、事实、涉及文件和相关概念
- • **成本** ：每条观察约 500–1,000 token
- • **目的** ：深入分析特定的、经过验证的观察记录

这种「先索引再获取详情」的策略，相比直接拉取完整记录， **可以节省约 10 倍的 token** 。

### 可用 MCP 工具

1. 1\. **`search`** ：全文索引搜索，支持按类型、日期、项目过滤，是所有查询的起点。
2. 2\. **`timeline`** ：获取时间上下文，了解某条决策或 bug 修复的前因后果。
3. 3\. **`get_observations`** ：批量获取完整详情，建议一次传入多个 ID，以降低开销。
4. 4\. **`__IMPORTANT`** ：工作流文档，对 Claude 可见，指导如何高效使用记忆系统。

### 实战场景演示

**场景一：找出数据库连接出错的原因** ：

```
# 步骤一：搜索相关修复记录
search(query="error database connection", type="bugfix", limit=10)
# → 查看索引，识别可能相关的观察结果 #245、#312、#489

# 步骤二：查看时间上下文
timeline(anchor=312, depth_before=3, depth_after=3)
# → 理解修复 #312 前后发生的事件顺序

# 步骤三：获取完整观察详情
get_observations(ids=[312, 489])
# → 获取相关修复的完整内容，包括叙述、事实、涉及文件和概念
```

**场景二：审查有关身份验证的架构选择** ：

```
# 步骤一：搜索相关决策记录
search(query="authentication", type="decision", limit=5)
# → 查找身份验证相关的决策观察结果

# 步骤二：获取完整观察详情
get_observations(ids=[<relevant_ids>])
# → 获取完整决策依据、权衡考虑以及相关事实
```

**场景三：查找特定文件的修改细节** ：

```
# 步骤一：搜索提及该文件的观察记录
search(query="worker-service.ts", limit=20)
# → 返回所有与该文件相关的观察结果

# 步骤二：查看时间上下文
timeline(query="worker-service.ts refactor", depth_before=2, depth_after=2)
# → 查看重构前后发生的事件

# 步骤三：获取完整观察详情
get_observations(ids=[<specific_observation_ids>])
# → 获取文件修改和重构的详细信息
```

### 自然语言查询

你不需要记住任何具体命令，直接用自然语言提问：

- • `“我们之前是如何处理错误的？”`
- • `“身份验证功能是怎么实现的？”`
- • `“API 层修复了哪些 Bug？”`
- • `“显示数据库架构的所有变更”`

系统会自动调用合适的 MCP 工具查找相关上下文，并在结果中附上 `claude-mem://` URI，直接指向对应的记录。

## 上下文捕获与处理机制

### 自动化捕获流程

在启用 Claude-mem 的情况下使用 Claude Code 时，系统会自动记录 **每一次工具调用** 。无论是读取文件、执行 bash 命令、使用 glob 搜索，还是修改代码，相关的输入和输出都会被捕获并处理。

### 提取的语义信息

Worker 服务会对捕获到的观察记录进行处理，并提取以下语义字段：

| 字段 | 说明 |
| --- | --- |
| **Title** | 事件的简要描述 |
| **Subtitle** | 补充的背景信息 |
| **Narrative** | 对操作过程的详细描述 |
| **Facts** | 关键结论与要点（列表形式） |
| **Concepts** | 相关标签与分类 |
| **Type** | 记录类型（decision、bugfix、feature、refactor、discovery、change） |
| **Files** | 涉及的文件（读取或修改） |

整个压缩过程完全自动完成。原始工具输出可能包含数千个 token，但最终存储的语义记录通常只有约 500 个 token，在保留关键信息的同时去除了无关细节。

### 会话摘要生成

当 Claude 完成一次响应（触发 Stop Hook）时，Claude-mem 会自动生成一份会话摘要，主要包含：

- • **Request** ：本次会话的用户请求
- • **Investigated** ：过程中探索和分析的内容
- • **Learned** ：得到的关键结论或经验
- • **Completed** ：已完成的工作
- • **Next Steps** ：建议的后续行动

这些摘要会与具体的观察记录一起注入到后续会话中，用于在保留细节的同时，快速恢复整体上下文。

## 自动生成文件夹上下文文件

Claude-mem 会在项目文件夹中自动生成 `CLAUDE.md` 文件，为该文件夹创建与全局记忆数据库互补的 **活动时间线** 。

### 工作原理

当你操作某个文件夹中的文件时，Claude-mem 会执行以下流程：

1. 1\. **识别文件夹路径** ：确定被访问文件所属的唯一文件夹
2. 2\. **查询观察记录** ：获取与该文件夹相关的最近观察记录
3. 3\. **生成时间线** ：将观察记录整理为格式化的活动时间线
4. 4\. **写入 CLAUDE.md** ：将时间线写入文件夹下的 `CLAUDE.md` ，并使用 `<claude-mem-context>` 标签包裹

每个文件夹的 `CLAUDE.md` 包含一个「最近活动」部分，显示观察 ID、时间戳、类型指示器（bug 修复、功能、发现）、简要标题和预估 token 数量。

### 用户内容保留机制

自动生成的内容会被包裹在 `<claude-mem-context>` 标签中。 **你在这些标签之外添加的内容会在文件重新生成时被保留** 。

这让你可以：

- • 在生成内容的上方或下方添加自己的文档
- • 编写针对 Claude 的文件夹特定指令
- • 包含架构注释或项目约定

**示例 CLAUDE.md 结构** ：

```
# Authentication Module

This folder contains all authentication-related code.
Follow the established patterns for new auth providers.

<claude-mem-context>
# Recent Activity

| ID | Time | Type | Title | Tokens |
|----|------|------|-------|--------|
| #1234 | 4:30 PM | 🔵 | Implemented user authentication | ~250 |
| #1235 | 4:45 PM | 🔴 | Fixed login redirect bug | ~180 |
</claude-mem-context>

## Manual Notes

- OAuth providers go in /providers/
- Session handling uses Redis
```

## 隐私控制与安全

Claude-mem 提供细粒度的隐私控制，防止敏感数据被存入记忆系统。

### Private 内容标签

使用 `<private>` 标签包裹的内容不会被写入存储系统，例如：

```makefile
<private>
API_KEY=sk-live-abc123xyz789
DATABASE_PASSWORD=supersecret456
</private>
```

系统会在处理阶段直接忽略这些内容，确保敏感信息不会进入数据库。这一机制主要用于保护 API 密钥、访问凭据以及其他不应被记录的实现细节。

### 双重标签隐私系统

Claude-mem 采用双重标签机制来保护敏感信息和系统内容：

| 标签 | 类型 | 用途 |
| --- | --- | --- |
| `<private>` | 用户控制 | 保护敏感内容 |
| `<claude-mem-context>` | 系统级别 | 防止重复存储 |

## Web 监控界面

Claude-mem 提供一个 Web 查看器，运行在 `http://localhost:37777` ，用于实时可视化记忆流。

![[assets/Clippings/开源 Claude Code 自动记忆管理插件 Claude-Mem 完整上手攻略/IMG-20260731225953710.webp|图片]]

界面功能包括：

- • **实时观察流** ：通过 emoji 指示器显示事件的重要性
- • **会话时间线** ：按时间顺序显示操作和观察记录
- • **搜索界面** ：快速查询记忆记录
- • **设置面板** ：调整配置选项
- • **版本切换** ：在稳定版和 beta 版本之间切换

> 提示：该 UI 对基本使用不是必需的，但对于理解 Claude-mem 捕获的内容和整理开发历史非常有帮助。

## 测试版功能：无尽模式（Endless Mode）

测试版通道提供 **无尽模式** ，这是一种用于延长会话的仿生记忆架构。

- • **容量提升** ：不再在约 50 次工具调用后触及上下文限制，支持约 **1,000 次工具使用** —— 相当于 **20 倍增长**
- • **技术实现** ：通过实时压缩工具输出，将 token 使用量减少约 95%，并将扩展复杂度从 O(N²) 降低到 O(N)

### 权衡

- • 每次工具调用生成观察记录会增加 **60-90 秒** 的延迟
- • 对于跨越数天或数周的深度编码会话，这种延迟通常可接受
- • 对于快速连续的工具使用，延迟可能成为瓶颈

### 启用方法

通过 Web 查看器访问 `http://localhost:37777` → **设置** → **版本频道** ，切换到测试版以启用无尽模式

## 故障排查指南

### Worker 服务无法启动

工作进程在端口 `37777` 上启动失败：

```
# 检查端口占用
lsof -i :37777

# 配置备用端口
export CLAUDE_MEM_WORKER_PORT=8080

# 手动启动 Worker
bun plugin/scripts/worker-service.cjs
```

### 记忆无法保存

如果 Claude 不记得之前的会话:

```
# 验证 Worker 运行
npm run worker:status

# 检查数据库文件
ls -la ~/.claude-mem/claude-mem.db

# 查看错误日志
npm run worker:logs
```

### 上下文注入问题

如果会话开始时出现上下文过多或过少的情况，可以通过调整观察结果（Observation）的限制来解决。

```
export CLAUDE_MEM_CONTEXT_OBSERVATIONS=10  # 减少
export CLAUDE_MEM_CONTEXT_OBSERVATIONS=100 # 增加
```

### 空 CLAUDE.md 文件

这是 `v9.0.5` 的已知问题。临时解决方案：手动删除创建的目录、在 `.gitignore` 中添加模式，或等待后续版本修复。

## 总结

Claude-mem 让 Claude Code 从一个 **无状态的辅助工具** ，转变为能够长期协作的开发伙伴。它会在使用过程中持续积累对代码库的理解，而不是在每次会话中重新开始。

通过自动捕获工具调用、将关键信息压缩为可搜索的记忆，并在需要时按需检索相关上下文，Claude-mem 有效减少了重复解释背景所带来的时间和 token 开销。

基于分层检索的 MCP 工具、按目录生成的 `CLAUDE.md` 以及明确的隐私边界，这套渐进式上下文机制在完全本地、可控的前提下，相比手动管理上下文，实现了约一个数量级的 token 效率提升。

**Github 地址** ： [https://github.com/thedotmack/claude-mem](https://github.com/thedotmack/claude-mem)

**既然看到这里了，如果觉得有启发，随手点个赞、推荐、转发三连吧，你的支持是我持续分享干货的动力。**

推荐阅读： [开源多平台 AI 智能体上下文驱动开发技能 Conductor 完整上手攻略](https://mp.weixin.qq.com/s?__biz=MjM5NzA1NzMyOQ==&mid=2247486750&idx=1&sn=b4010dc1e43190da9570963d796354d1&scene=21#wechat_redirect)

**微信扫一扫赞赏作者**

claude教程 · 目录