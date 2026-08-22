---

title: "BMad 命名 Agent"
category: entities
tags:
  - bmad-method
  - ai-agents
  - persona
  - entity
sources:
  - "https://github.com/bmad-code-org/bmad-method"
created: "2026-08-05T07:00:00Z"
updated: 2026-08-23T09:05:00Z
summary: "BMad Method 5 个命名 agent（Mary BA / John PM / Sally UX / Winston Architect / Amelia Dev），各守 BMad 流程一个阶段；以 emoji + 名字 + 阶段稳定身份 + 可定制层（role/principles/style/icon/menu）平衡。"
provenance:
  extracted: 0.90
  inferred: 0.06
  ambiguous: 0.04
base_confidence: 0.72
lifecycle: draft
lifecycle_changed: "2026-08-05"
tier: supporting
relationships:
  - target: "[[entities/bmad-method]]"
    type: related_to
  - target: "[[concepts/bmad-named-agent-architecture]]"
    type: related_to
  - target: "[[concepts/bmad-delivery-loop]]"
    type: related_to---

# BMad 命名 Agent

> BMad Method 把"AI agent"做成**有名字、有 emoji、有阶段的稳定身份**——你"hey Mary, let's brainstorm"，Mary 就激活、跳进 brainstorming、跳过菜单。这是 [[concepts/bmad-named-agent-architecture]] 三腿凳模型中的"persona 连续性"那条腿。

## 5 个核心命名 Agent

| Agent | 阶段 | 模块 |
|---|---|---|
| 📊 **Mary**, Business Analyst | Analysis | 市场研究 / brainstorming / 产品简报 / PRFAQ |
| 📋 **John**, Product Manager | Planning | PRD 创建 / epic/story 拆分 / implementation readiness |
| 🎨 **Sally**, UX Designer | Planning | UX 设计规范 |
| 🏗️ **Winston**, System Architect | Solutioning | 技术架构 / 对齐检查 |
| 💻 **Amelia**, Senior Engineer | Implementation | story 执行 / build / code review / sprint planning |

**注意** 📚 **Paige**（Technical Writer）已 retire（v6.10 / #2658）——她的菜单项都是通用 LLM 默认而无领域实质；`bmad-document-project` 直接可调用，保留在 Analyst 菜单。Paige 暂休，将来会更强大地回归。

## 身份稳定性 vs 可定制层

每个 agent 有：

| 部分 | 性质 | 谁能改 |
|---|---|---|
| **名字 + 标题 + 领域** | 硬编码 | 不能改（品牌识别） |
| **角色 / 原则 / 通信风格 / icon / 菜单** | 可定制 | 团队 + 个人 override |

> "Brand recognition survives customization so 'hey Mary' always activates the analyst, regardless of how a team has shaped her behavior."

## 8 步激活流程

当你 invoke 一个命名 agent：

1. **Resolve the agent block** — 合并 shipped `customize.toml` + 团队 + 个人 override（Python resolver + stdlib `tomllib`）
2. **Execute prepend steps** — 团队配置的 pre-flight 行为
3. **Adopt persona** — 硬编码身份 + 定制角色 / 风格 / 原则
4. **Load persistent facts** — 组织规则、合规注意、可选 `file:` 前缀加载文件（如 `file:{project-root}/docs/project-context.md`）
5. **Load config** — 用户名、通信语言、输出语言、artifact 路径
6. **Greet** — 用配置语言 + emoji 前缀打招呼（一眼看出谁在说话）
7. **Execute append steps** — 团队配置的 post-greet 设置
8. **Dispatch or present the menu** — 如果首句映射到菜单项，直接走；否则渲染菜单等输入

**第 8 步 = intent × capability 交汇**：

- "Hey Mary, let's brainstorm" → `bmad-brainstorming` 是 Mary 菜单上 `BP` 明显匹配 → **跳过菜单**
- "Let's ideate on my SaaS idea" → 模糊 → **简短问一次**（不是 confirmation ritual）
- 完全对不上 → **正常继续对话**

## 与"菜单驱动"vs"空白 prompt"的对比

**为什么不要菜单驱动？** 菜单要求**用户向工具让步**——你得记住 brainstorming 在分析 agent 下 `BP` 码、PM 下不在这码、UX 又不在这码。认知负担被工具扔给用户。

**为什么不要空白 prompt？** 空白 prompt 假设用户知道 magic words——"Help me brainstorm" 或许行，"let's ideate on my SaaS idea" 可能不行，结果取决于你怎么措辞。变成 prompt engineering。

**命名 agent 把控制权拉回来**：

> "Named agents invert it. You say what you want, to whom, in whatever words feel natural. The agent knows who they are and what they do. When your intent is clear enough, they just go."

菜单保留作 fallback——探索时显示，不探索时跳过。

## 与 vault 已有概念的关系

| vault 已有 | 在 BMad 命名 agent 中的体现 |
|---|---|
| [[concepts/ai-agent]] | 命名 agent 是 AI agent 框架的"persona 连续性"落地 |
| [[concepts/agent-operating-system]] | BMad 5 命名 agent = AOS 五层中 "Knowledge Base" 层的具名化载体 |
| [[concepts/ai-tool-specialization]] | 5 agent 各守一阶段 = 工具栈专业化分工的最终形态 |
| [[concepts/claude-code-hooks-lifecycle]] | "8 步激活" = "hook 生命周期"的人格化版本 |

## Related
- [[entities/bmad-method]] — 框架本体
- [[concepts/bmad-named-agent-architecture]] — 三腿凳（skill / agent / customization）
- [[concepts/bmad-delivery-loop]] — 5 agent 各守的阶段
- [[entities/bmad-party-mode]] — 5 agent 进同一房间开会
- [[skills/bmad-customize-skill]] — 团队定制 agent 行为
- [[synthesis/concepts-agent-team-mailbox-protocol × entities-bmad-named-agent|Agent Team 邮箱协议 × BMad 命名 Agent 派发]] — synthesis
