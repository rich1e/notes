---

title: "BMad Method 框架"
category: entities
tags:
  - bmad-method
  - ai-agents
  - agile
  - framework
  - entity
sources:
  - "https://github.com/bmad-code-org/bmad-method"
created: "2026-08-05T07:00:00Z"
updated: 2026-08-23T09:05:00Z
summary: "BMad Method（BMad Code, LLC 出品，MIT）是 AI 驱动敏捷交付框架：Clarify→Plan→Build→Learn 闭环 + 5 个命名 agent + 命名技能 + 4 层 customization。适用于新项目 + 既有 codebase。"
provenance:
  extracted: 0.88
  inferred: 0.08
  ambiguous: 0.04
base_confidence: 0.70
lifecycle: draft
lifecycle_changed: "2026-08-05"
tier: supporting
relationships:
  - target: "[[concepts/bmad-delivery-loop]]"
    type: related_to
  - target: "[[concepts/bmad-named-agent-architecture]]"
    type: related_to
  - target: "[[entities/bmad-named-agent]]"
    type: related_to
  - target: "[[entities/bmad-party-mode]]"
    type: related_to

  - target: [[concepts-agent-operating-system × concepts-deterministic-agent-memory]]
    type: related_to
---
# BMad Method 框架

> BMad Method 是 [BMad Code, LLC](https://bmadcode.com) 出品的**开源 AI 驱动敏捷交付框架**（MIT）。它把"用 LLM 写代码"扩展为"用 LLM 做整个交付周期"——从模糊想法 / 改动请求到能运行的软件，把决策显式化、context 持续携带、过程按工作量自动 size。

## 是什么

**Agile AI Driven Development (AiDD)** 覆盖整个 effort，不只是 code：what to build、how it holds together、how it changes as you learn。BMad Method 是做这件事的**敏捷方式**：

- 决策保持**显式**
- Context **向前传递**而不是每次重解释
- 过程按工作量 size 自己——小改动直进 Build，复杂工作才拿它需要的深度

> "The same method covers a weekend prototype and a system with years of history behind it."

## 核心特性（README 6 条）

| 特性 | 含义 |
|---|---|
| **Right-sized process** | 清晰改动直接实现，复杂 initiative 加更深的 planning |
| **New or existing code** | 从零起，或在 inherited codebase 上建立 verified context 后从真实状态工作 |
| **Durable context** | 产品和技术决策**向前传递**，不每次重解释 |
| **Specialized perspectives** | 调入产品 / 架构 / UX / 开发 / 测试 视角 |
| **Guided collaboration** | 用结构化工作流 + 多 agent 讨论，**不交出判断权** |
| **One delivery path** | 从早期思考到 reviewed implementation 到纠错到学习 |

## 一行安装

```bash
npx bmad-method install
```

**前置**：Node.js 20.12+ / Python 3.10+ / uv（Astral 出品的 Python 包/版本管理，BMad v7 起必用，v6.10 已开始检查）。

`bmad-build` 是核心实施工作流——告诉它要改什么、保留重要决策。`bmad-help` 随时给"下一步建议"。

## 生态（6 个仓库）

| Module | 用途 |
|---|---|
| **[BMad Method](https://github.com/bmad-code-org/BMAD-METHOD)** | 计划与交付软件（新原型到既有 codebase） |
| **[BMad Builder](https://github.com/bmad-code-org/bmad-builder)** | Skill / workflow / agent 的构造器 |
| **[BMad Creative Intelligence Suite](https://github.com/bmad-code-org/bmad-module-creative-intelligence-suite)** | 创新 / 设计思维 / 故事讲述的创意伙伴 |
| **[BMad Test Architect](https://github.com/bmad-code-org/bmad-method-test-architecture-enterprise)** | 企业测试 add-on |
| **[BMad Loop](https://github.com/bmad-code-org/bmad-loop)** | 全自动构建 / 验证 / 复盘整个 epic（unattended） |
| **[BMad Game Dev Studio](https://github.com/bmad-code-org/bmad-module-game-dev-studio)** | Unity / Unreal / Godot / Phaser 游戏开发 |

## Web bundles

`[bmadcode.com/web-bundles/](https://bmadcode.com/web-bundles/)` 把 BMad 工作流打包为 **Google Gemini Gems** 和 **ChatGPT Custom GPTs**——可以在 web 订阅里做 planning，再把 artifacts 带进 coding 工具做实现。

## 与 vault 已有知识的关系

| vault 已有 | 在 BMad 框架的位置 |
|---|---|
| [[concepts/ai-agent]] | BMad 是"多 agent 协作"的商业化产品 |
| [[concepts/agent-operating-system]] | BMad 命名 agent = AOS 的具名 persona 落地 |
| [[concepts/claude-code-three-modes]] | BMad Party Mode 的 4 modes 直接借鉴 subagent/agent team 模式 |
| [[concepts/claude-code-agent-teams]] | BMad `agent-team` 模式 = Claude Code Agent Teams 的应用 |
| [[concepts/agent-team-mailbox-protocol]] | BMad Party Mode `subagent` / `agent-team` 都用 Mailbox 通信 |
| [[concepts/ai-tool-specialization]] | BMad 5 命名 agent 各守一阶段 = "工具栈专业化分工" |
| [[concepts/deterministic-agent-memory]] | BMad sprint_planning.py 把 epic 解析 / status 合并做"deterministic fact layer" |
| [[entities/claude-mem]] | BMad memlog (`_bmad/scripts/memlog.py`) 是 v6.9+ 标准 working-memory 原语 |
| [[entities/openlore]] | 同 vault "hot path 0 LLM + 失败显式分桶"哲学——sprint_planning.py 的失败语义 |

## Open Questions

- BMad v7 全面转 `uv run` 的迁移路径——本 vault 内无既有 Python 技能可参考
- "bmad-loop unattended"的具体安全边界（如 review 自动批准 / 自动合并的约束）— README 提到但未深入 ambiguous
- "Web bundles"对 vault 工作流（macOS Claude Code 终端）的桥接价值——值得后续尝试

## Related
- [[synthesis/concepts-ai-tool-specialization × entities-bmad-method]] — synthesis

- [[references/bmad-method-github-readme]] — 完整 README + 文件索引
- [[concepts/bmad-delivery-loop]] — Clarify→Plan→Build→Learn 闭环
- [[concepts/bmad-named-agent-architecture]] — 三腿凳模型
- [[entities/bmad-named-agent]] — 5 个具名 agent
- [[entities/bmad-party-mode]] — 多 agent 房间
- [[skills/bmad-install-and-setup]] — 安装流程
- <!-- broken link: this synthesis page does not exist -->（未来可生成） — 通用 AI agent 框架 × 具体落地产品
- [[synthesis/concepts-deterministic-agent-memory × entities-bmad-method|确定性 Agent 记忆 × BMad 方法论]] — synthesis
