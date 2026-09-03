---

title: "设计系统作为 AI 上下文"
category: concepts
tags: [ux, ai-context, design-tokens, concept, Deepseek]
summary: "把设计系统（颜色 token、字号、布局规则）编码为 agent 可读的 DESIGN.md，作为 AI 编码 agent 的硬约束输入，避免 agent 在设计决策上反复猜测耗 token。"
sources:
  - "https://medium.com/devsecops-ai/how-google-stitch-claude-codes-mcp-integration-changed-the-way-i-build-products-63ecb8ed7f5a"
created: "2026-07-28T00:00:00Z"
updated: 2026-08-23T09:05:00Z
tier: core
lifecycle: draft
lifecycle_changed: "2026-07-28"
base_confidence: 0.42
provenance:
  extracted: 0.55
  inferred: 0.40
  ambiguous: 0.05
relationships:
  - target: "[[concepts/ai-tool-specialization]]"
    type: related_to
  - target: "[[entities/google-stitch]]"
    type: derived_from
  - target: "[[entities/claude-code]]"
    type: related_to
  - target: "[[skills/claude-code-token-optimization]]"
    type: related_to
  - target: "[[concepts/design-md-format-spec]]"
    type: extends
  - target: "[[entities/google-labs-code-design]]"
    type: related_to
  - target: "[[entities/awesome-design-md]]"
    type: related_to
  - target: "[[projects/flow-design-system/concepts/triple-repo-component-contract]]"
    type: related_to

---
# 设计系统作为 AI 上下文

> 设计系统不是给人看的文档，是给 AI agent 的硬约束输入。

## 核心观点

当一个 AI 编码 agent（典型如 Claude Code）进入一个**没有显式设计系统**的项目时，它对 UI 决策只能靠**猜测 + 多轮对话修正**：

```text
用户：把 dashboard 的布局收拾一下
Claude：重写 JSX、调整 padding、用了一堆 CSS 库……
用户：再贴近原来的样子
Claude：再改一轮……
```

每一轮都在重新生成"贴近"的近似值。15 轮下来整个上下文窗口几乎被间距、颜色、字体这类**非 Claude 擅长的决策**吃光——真正留给逻辑和接线的位置所剩无几。

**解法**：把设计系统从"散落在 CSS 变量和人类脑中"的状态，**外化成 agent 可读的 markdown / JSON 文件**（如 `DESIGN.md`），作为固定的工程输入物：

```markdown
# DESIGN.md
- primary: #1A73E8
- font-display: Inter 600 32px
- card-radius: 12px
- spacing-scale: 4 / 8 / 12 / 16 / 24 / 32
- ……
```

这样 agent 读到的是**硬约束**而不是**模糊偏好**——它不是在"猜你想要哪个 padding"，而是在"读 token 表"。

## 为什么这一招管用

| 维度 | 无设计系统 | 有 DESIGN.md |
|------|------------|--------------|
| agent 的 UI 决策来源 | 猜测 + 反复修正 | 直接读 token 表 |
| 单轮对话消耗 | 高（要描述和重新解释） | 低（一次到位） |
| 上下文窗口占用 | 被设计决策反复吃光 | 设计部分在缓存层固定 |
| 视觉一致性 | 跨会话漂移 | 跨会话保持一致 |
| 设计师 / 工程师协作 | 凭记忆口口相传 | 文件即契约 |

Sachin Sharma 的经验值：用 Google Stitch + DESIGN.md 后，"design → code" 的衔接从大约 4-5 个会话烧光上下文，下降到单会话一次到位。

## 实操路径

### 1. 工具自动产出（如 Google Stitch）

Stitch 把生成的设计系统直接导出为 `DESIGN.md`，放在项目根目录，agent 下次启动自动读到。

### 2. 手工维护（不用 AI 设计工具时）

把设计 token 写到 `DESIGN.md` 或 `design-tokens.json`，并纳入版本控制：

```json
{
  "color": { "primary": "#1A73E8", "bg": "#0F172A" },
  "typography": { "display": "Inter 600 32/40" },
  "spacing": [4, 8, 12, 16, 24, 32]
}
```

agent 启动时通过 CLAUDE.md 中的指令读取这份文件。

### 3. 设计决策的 SPEC 而不是 PREFERENCE

`DESIGN.md` 写"间距按 4 / 8 / 12 阶梯" 而不是"间距差不多就行"。agent 对**明确阶梯**的执行远比对**"差不多"**的稳定。

## 与提示缓存的协同

[[skills/claude-code-token-optimization]] 指出：Claude Code 的固定基础设施（系统提示、工具定义、CLAUDE.md）走提示缓存，读到成本只有重新计算的 1/10。**`DESIGN.md` 一旦放进项目根并由 CLAUDE.md 引用，自然落在缓存前缀**——后续每轮 UI 迭代都不用重新读它，直接复用。这是把设计系统升级为"AI 上下文" 与 token 经济学的天然契合点。

## 适用边界

不是所有项目都受益：

- **MVP / 一次性原型**：还没定型设计系统，硬写 DESIGN.md 是过度工程。
- **小型个人项目**：单文件 CSS 变量可能够用。
- **真正受益**：长期维护、多角色协作、UI 是核心卖点的项目。

## 相关页面

- [[misc/web-medium-com-devsecops-ai-how-google-stitch-claude-codes-mcp-integration]] — 实操来源
- [[entities/google-stitch]] — 自动化生成 DESIGN.md 的工具
- [[entities/claude-code]] — DESIGN.md 主要的"读者"
- [[concepts/ai-tool-specialization]] — 上下游：把视觉与逻辑拆给不同 agent
- [[skills/claude-code-token-optimization]] — DESIGN.md 进入缓存前缀的杠杆

## Related

- [[synthesis/concepts-design-system-as-ai-context × entities-claude-code|设计系统作为 AI 上下文 × Claude Code 消费]] — synthesis
