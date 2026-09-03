---
title: Claude Code Agent Teams 完整指南（PPT 综合）
category: misc
tags:
  - claude-code
  - agent-teams
  - multi-agent
  - llm-tooling
summary: >-
  基于 20 份一手资料的 Claude Code Agent Teams 综合指南（5 幻灯片）：架构四柱（独立 context / Mailbox IPC / 文件锁 / Lead 调度）、配置方法（5 种显示模式）、实践场景（对抗式调试）、9 项限制、与 omo / BMad 三方案对比。
sources:
  - concepts/agent-team-mailbox-protocol
  - concepts/agent-team-race-condition-task-claim
  - concepts/agent-team-display-modes
  - concepts/agent-team-cost-overhead
  - synthesis/Research: Claude Code Agent Teams.md
created: 2026-08-06
updated: 2026-08-27T00:00:00Z
tier: supporting
lifecycle: reviewed
lifecycle_changed: "2026-08-27"
base_confidence: 0.88
provenance:
  extracted: 0.90
  inferred: 0.08
  ambiguous: 0.02
relationships:
  - target: "[[synthesis/Research: Claude Code Agent Teams]]"
    type: derived_from
  - target: "[[concepts/agent-team-mailbox-protocol]]"
    type: extends
  - target: "[[concepts/claude-code-agent-teams]]"
    type: extends
  - target: "[[concepts/claude-code-three-modes]]"
    type: related_to
---

# Claude Code Agent Teams 完整指南

> 基于 20 份一手资料的综合分析（资深 AI 技术架构师视角）
> 数据截止：2026-08-06

---

## 目录

1. [Agent Teams 是如何架构](#slide-1-agent-teams-是如何架构)
2. [Agent Teams 如何配置](#slide-2-agent-teams-如何配置)
3. [Agent Teams 如何在工作中实践](#slide-3-agent-teams-如何在工作中实践)
4. [Agent Teams 有哪些短板与缺陷](#slide-4-agent-teams-有哪些短板与缺陷)
5. [与其他方案相比有什么区别](#slide-5-与其他方案相比有什么区别)

---

## Slide 1: Agent Teams 是如何架构

### 核心定义

Agent Teams 是一种**多 Claude 实例协作架构**，核心逻辑并非"一个模型扮演多个角色"，而是**多个对等的独立进程协作**。

> "With multiple independent investigators actively trying to disprove each other, the theory that survives is much more likely to be the actual root cause."
> —— Anthropic 官方文档

### 四大架构支柱

#### 1️⃣ 独立上下文窗口 (Independent Context)

每个 teammate 都是独立的 Claude Code 实例，拥有专属上下文窗口（最高支持 1M+ tokens）。

| 特性 | Subagents | Agent Team Teammate |
|------|-----------|---------------------|
| Context | 独立窗口，**结果回到主** | 独立窗口，**完全独立** |
| 通信 | 单向（向主汇报） | **双向**（teammate 间直接通信） |
| Token | Summarized back（low cost） | **Linear scaling**（high cost） |

#### 2️⃣ Mailbox 对等通信协议

基于文件系统的 **JSON IPC 机制**：

```
~/.claude/teams/{team-name}/inboxes/{agent-name}.json
```

- 每个 agent 一个 inbox JSON 文件
- **写文件即发送消息，读文件即接收消息**
- 打破了传统的"主从汇报"模式，实现队友间的**直接双向对话**

> 源：[[concepts/agent-team-mailbox-protocol]]

#### 3️⃣ 共享任务列表 + 任务级悲观锁 (File Lock)

- 所有队友共享同一个 Task List
- 系统内置文件锁机制，防止多个 agent 同时认领同一任务
- 状态机：`pending` → `in progress` → `completed`

> 源：[[concepts/agent-team-race-condition-task-claim]]

#### 4️⃣ 动态调度模型（Team Lead 纯调度）

Team Lead 负责：
- 理解问题 → "what's the job to be done here?"
- 拆任务列表 → "what are the different tasks?"
- 为每个 agent 写专属 prompt
- 逐个 spool up agent 直到所有 agent 进入"房间"
- 监控进度 → agent 完成后回收资源

**Lead 自己不干活**——纯调度者。

### 架构图

```
┌─────────────────────────────────────────────────┐
│ Team Lead (主 Claude Code session)              │
│  - 理解任务 / 拆任务 / 写 prompt / 监控          │
└─────────────┬───────────────────────────────────┘
              │
              │ spawn + 协调
              ↓
┌─────────────────────────────────────────────────┐
│ Shared Task List (文件锁防 race)                │
│  pending → in_progress → completed              │
└─────────────┬───────────────────────────────────┘
              │
              ├──→ Teammate 1 (独立 context) ──┐
              ├──→ Teammate 2 (独立 context) ──┤
              ├──→ Teammate 3 (独立 context) ──┼──→ Mailbox
              ├──→ Teammate 4 (独立 context) ──┤    (JSON IPC
              └──→ Teammate 5 (独立 context) ──┘     对等通信)
```

---

## Slide 2: Agent Teams 如何配置

### 启用开关

**必须通过环境变量** `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` 开启，而非 `settings.json` 的常规字段。

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

> ⚠️ 状态：Experimental / Disabled by default
> ⚠️ 必须使用环境变量，YouTube 教程中的 `experimentalAgents: "on"` 字段是错的

### 5 种显示模式

| 模式 | 行为 | 依赖 |
|------|------|------|
| **`"in-process"`** ⭐默认 | 所有 teammate 在主终端 agent panel；方向键 + Enter 进入 | 无 |
| `"split-panes"` | 每个 teammate 一个独立 pane | tmux 或 iTerm2 |
| `"auto"` | 在 tmux/iTerm2 内时自动 split-pane | tmux/iTerm2 |
| `"tmux"` | 强制 split-pane，tmux/iTerm2 自动检测 | tmux 或 iTerm2 |
| `"iterm2"` | 强制 iTerm2 native split-pane | iTerm2 + `it2` CLI |

### 依赖项要求

若需启用分屏模式，**必须安装 tmux 或 iTerm2**：

```bash
# macOS
brew install tmux

# iTerm2
brew install mkusaka/it2/it2
# + iTerm2 → Settings → General → Magic → Enable Python API
```

> ⚠️ **不支持的平台**：VS Code 集成终端、Windows Terminal、Ghostty

### 模型级联设置

推荐配置（成本优化策略）：

| 角色 | 推荐模型 | 理由 |
|------|---------|------|
| **Team Lead** | Opus 4.6 | 负责规划与分发 |
| **执行 teammates** | Sonnet / Haiku | 负责具体执行（省钱） |
| **可混合** | 关键模块用 Sonnet，QA 用 Haiku | 平衡成本与速度 |

**设置方式**：
- `/config` → "Default teammate model"
- 或 spawn 时显式：`Use Sonnet for each teammate`

### 价格参考（2026 年）

- Opus 4.6: **$5/M input, $25/M output**（200K context tier）
- dashboard 只算主 lead 时长，**真实账单应远高**

---

## Slide 3: Agent Teams 如何在工作中实践

### 触发方式

**必须在对话中显式要求**，可用措辞：

```
Create an agent team                              # 让 leader 自决 agent 数
Create three team members focus on A, B, C       # 显式指定 3 个
Use Sonnet for all the agents                    # 顺便指定模型
```

### 团队规模决策

#### 官方建议规模

| 数量 | 推荐 |
|------|------|
| **3-5 人** | ✅ **多数工作流最佳** |
| 6+ | ⚠️ 协调成本显著上升，需明确任务边界 |
| 15+ | ❌ **不建议**（协调爆炸）|
| 16 | 📊 Anthropic 演示用 16 agents 构建 C 编译器 |

#### 任务密度建议

- 每位 teammate 承担 **5-6 个任务**
- 15 个独立任务 → 3 个 teammate 是好起点
- split-pane 模式下 **4-5 个 agent 是视觉上限**

### 上下文桥接策略

**关键工程含义**：teammate 不共享原始对话上下文！

```
❌ 错的做法：
让 agent team 继续我们之前聊的 30 分钟 web search

✅ 对的做法：
1. 在 Lead 会话先把核心结论落 MD 文件
2. 然后用 "create an agent team to investigate X,
   please read the MD file <path> first" 这样的措辞
```

### 杀手级应用场景 ⭐

**对抗式假设调试 (Adversarial Debugging)**

通过让 **5 个独立调查员**尝试反驳彼此的假设，存活下来的理论最有可能是真正的根因。

> 官方原话："Sequential investigation suffers from anchoring: once one theory is explored, subsequent investigation is biased toward it."

### 4 类典型用例

| 场景 | 描述 |
|------|------|
| 🔍 Research and review | 多角度并行研究 |
| 🆕 New modules or features | 独立模块分别认领 |
| 🐛 Debugging with competing hypotheses | 5 互驳式排查（杀手场景） |
| 🔗 Cross-layer coordination | 前后端 + 测试各归一个 |

### 实战流程示例

```bash
# 1. 启动会话
tmux                    # 先 tmux 后 claude（强制顺序）
claude

# 2. 在 Lead 会话落 MD
echo "项目背景..." > /tmp/context.md

# 3. 触发团队
"Create an agent team of 4 members to investigate
performance issue. Read /tmp/context.md first."

# 4. Lead 自动：
#    - 拆任务给 4 个 teammate
#    - 每个 teammate 看自己的 prompt
#    - 共享 Task List（file lock 防 race）
#    - Mailbox 互通发现

# 5. Graceful shutdown
"Ask the backend teammate to shut down"
# 保留关键 agent 等 review，bug 继续修
```

---

## Slide 4: Agent Teams 有哪些短板与缺陷

### 9 项已知限制

| # | 限制 | 实战影响 |
|---|------|---------|
| 1 | **No session resumption** | `/resume` `/rewind` 后 lead 联系已不存在的 teammates |
| 2 | **Task status can lag** | teammates 有时不标 completed，依赖任务卡住 |
| 3 | **Shutdown can be slow** | teammate 必须等当前请求完成才退场 |
| 4 | **One team per session** | 团队状态无法跨 session 共享 |
| 5 | **No nested teams** | flat hierarchy，teammate 不能 spawn own teammates |
| 6 | **No background subagents** | `in-process` 模式下 teammate 无法启动后台 subagent |
| 7 | **Lead is fixed** | 不能 promote teammate 为 lead |
| 8 | **Permissions set at spawn** | spawn 时不能给独立 mode（spawn 后可改） |
| 9 | **Split panes = tmux/iTerm2 only** | 不支持 VS Code / Windows Terminal / Ghostty |

### 4 类不适用场景

| 反例 | 原因 |
|------|------|
| ❌ **串行任务** | 必须严格先后顺序，无法并行 |
| ❌ **同文件多人编辑** | 多 teammate 改同文件 = 覆盖风险 |
| ❌ **依赖密集工作** | 任务间大量交叉依赖，teammate 频繁阻塞 |
| ❌ **简单日常任务** | Token 成本线性增长，处理琐事不划算 |

### 核心短板：Token 成本线性增长

> "Agent teams use significantly more tokens than a single session. Each teammate has its own context window, and token usage scales with the number of active teammates."
> —— Anthropic 官方

**与 Subagents 对比**：

| 模式 | Token 模型 | 成本 |
|------|----------|------|
| 单 session | 1x 你的 context | 低 |
| Subagents | 子结果 **summarized back** | 中 |
| Agent Teams | N × **各自独立 context** | **高（线性增长）** |

**5 个 teammate ≈ 5x token 成本**（这是 YouTube 教程中"$1.15 跑 5 agent"误导的根本原因——dashboard 只算主 lead 时长）

### 常见失败模式

- **Task status lag**：teammates 有时不标 completed → 依赖任务卡住
- **Orphaned tmux sessions**：teammates tmux session 残留未清
- **Lead shuts down too early**：lead 误判"团队完工"
- **Mailbox stuck**（v2.1.207 前）：单条 malformed 会让整个 mailbox 每秒报错，需手动 `rm` 文件

---

## Slide 5: 与其他方案相比有什么区别

### 三大方案对比

| 维度 | Claude Code Agent Teams | omo Team Mode | BMad Party Mode |
|------|------------------------|---------------|-----------------|
| **触发方式** | 显式自然语言（"create an agent team"）| 单 keyword（`ultrawork` / `ulw`）| 命令行参数（`/bmad-party-mode --mode agent-team`）|
| **团队规模** | 3-5（6+ 协调难，15+ 不建议）| 1 lead + 最多 8 members | 默认 voicing 5 persona |
| **通信机制** | Mailbox JSON，对等通信 | Mailbox 轮询（3s 间隔）| Mailbox IPC（v6.10 修过广播陷阱）|
| **显示模式** | 5 种（in-process/split-panes/auto/tmux/iterm2）| `tmux_visualization` boolean | 依赖 Claude Code 显示能力 |
| **模型路由** | **手动/继承** | **自动化 Category Routing** | 模式驱动 |
| **持续推进** | 较弱（teammate 干完就退）| **极强**（Goal Audit + Todo Enforcer）| 中等 |
| **成本** | 高（线性增长）| **$49/月**（多模型组合）| 可控 |
| **严格度** | 任务级 File Lock | **11 字段资源 cap** | 降级链 |
| **跨 IDE** | ❌ 仅原生终端 | OpenCode 兼容多 provider | ❌ 仅 Claude Code |
| **适用场景** | 对抗式 Debug、独立模块并行 | 复杂长程任务、高频自动化审计 | 4 阶段交付、Persona 头脑风暴 |

### 三大核心差异

#### 1️⃣ 通信哲学

- **Claude Code**：引领 Mailbox 文件 IPC 潮流，让 agent 对等通信不再必须经 lead 中转
- **omo**：加 "Discipline Agents" 概念（Sisyphus / Hephaestus / Prometheus / Oracle / Librarian / Explore），明确职业分工
- **BMad**：v6.10 修正了 mailbox 误用为广播 channel 的 bug

#### 2️⃣ 资源保护

**omo 的 11 字段 cap** 是 Anthropic 文档从未给出的安全网：

```jsonc
{
  "team_mode": {
    "max_parallel_members": 4,
    "max_members": 8,
    "max_wall_clock_minutes": 120,
    "max_member_turns": 500,
    "max_messages_per_run": 10000,
    "mailbox_poll_interval_ms": 3000,
    // ...
  }
}
```

#### 3️⃣ 模型路由进化

| Claude Code（手动） | omo（自动化） |
|---------------------|--------------|
| 用户说"用 Opus 5 做架构" | Sisyphus 说"ultrabrain" → 自动选 GPT-5.6 Sol xhigh |
| 用户说"用 Sonnet 写测试" | agent 说"quick" → 自动选 Kimi 高速 |
| 用户需懂模型差异 | **用户不懂也 OK** |

### 场景化决策树

```
你的核心需求是什么？
│
├── 🎲 调试极其隐蔽、众说纷纭的 Bug
│   └── Claude Code Agent Teams（5-agent 对抗式 Debug）
│
├── 🏗️ 长程项目，多层级任务，想尽量自动化
│   └── omo Ultrawork 模式（Goal Audit 强行推进）
│
├── 💡 产品初期 PM/架构师/开发者头脑风暴
│   └── BMad Party Mode（预定义 Persona + 4 阶段流程）
│
├── 💰 预算 < $50/月，需处理复杂任务
│   └── omo（$49/月多模型组合订阅）
│
└── 🖥️ 在 VS Code 集成终端工作且不想切换
    └── ⚠️ 不要开 agent-team 模式
        ├── 用 Claude Code Subagents 模式
        └── 或 BMad session 模式（最便宜）
```

### 最终选型建议

| 需求 | 最佳方案 |
|------|---------|
| 真正的"团队协作感"（Mailbox + Task List + 独立思考空间）| **Claude Code Agent Teams**（工程闭环独特）|
| 想要更强的资源安全网 + 多模型自动化路由 + 一键触发 | **omo Ultrawork**（更严格的工程化）|
| 4 阶段标准交付流程 + Persona 头脑风暴 + 跨 IDE 降级链 | **BMad Party Mode** |
| 预算敏感 + 复杂任务 | **omo**（$49/月 vs Claude Code $200/月）|
| VS Code 集成终端 | ⚠️ **不要用** agent-team，改用 Subagents 或 BMad session |

---

## 附录：参考资料来源

参见 [[synthesis/Research: Claude Code Agent Teams]] 完整来源列表（20 份一手资料）。

**生成方式**：基于 NotebookLM 中 20 份一手资料，通过资深 AI 架构师视角综合整理  
**生成时间**：2026-08-06  
**文档版本**：v1.0
