---
title: AI Agent — 感知-规划-行动闭环的自主系统
category: concepts
tags:
  - llm
  - ai-agent
  - concept
summary: AI Agent 是以 LLM 为大脑、通过感知-规划-行动循环自主完成目标的系统,核心是工具调用 + 记忆 + 多步推理,把「会聊天」升级为「会办事」。
sources:
  - "https://lilianweng.github.io/posts/2023-06-23-agent/"
created: 2026-07-31T07:10:00Z
updated: 2026-07-31T07:10:00Z
tier: core
lifecycle: draft
lifecycle_changed: "2026-07-31"
base_confidence: 0.55
provenance:
  extracted: 0.82
  inferred: 0.14
  ambiguous: 0.04
relationships:
  - target: "[[concepts/ai-agent-node-pattern]]"
    type: related_to
  - target: "[[concepts/agent-operating-system]]"
    type: related_to
---

# AI Agent — 感知-规划-行动闭环的自主系统

> AI Agent 是以 LLM 为"大脑",通过**感知(perceive)→ 规划(plan)→ 行动(act)** 的循环,自主调用工具、维护记忆、分多步完成一个目标的系统。相比单轮问答,它把"会聊天"升级为"会办事"。

## 核心构成

| 组件 | 作用 |
|------|------|
| **LLM 大脑** | 推理、分解任务、决定下一步 |
| **工具调用(Tool Use)** | 通过 API/函数/MCP 与外部世界交互(搜索、执行、读写) |
| **记忆(Memory)** | 短期上下文 + 长期外部记忆,跨步骤/跨会话保持状态 |
| **规划(Planning)** | 任务分解、反思(reflection)、重规划 |

## 典型循环

```
目标 → 观察环境 → LLM 决策(思考+选工具) → 执行工具 → 观察结果 → 循环直至完成
```

代表范式:ReAct(推理与行动交织)、Reflexion(自我反思)、Plan-and-Execute。

## 可靠性前提

- **强指令遵循**:Agent 能稳定调工具,依赖 [[concepts/instruction-tuning]] 打好的指令遵循基础。
- **工具协议**:MCP 等标准化了工具接入,降低集成成本。

## 与本 vault 相邻概念的关系

- [[concepts/ai-agent-node-pattern]] — 把 Agent 各能力拆成工作流节点的**工程实现**(n8n 等)
- [[concepts/agent-operating-system]] — 面向多会话连续工作流的 Agent **记忆/编排框架**

## 相关页面

- [[concepts/instruction-tuning]] — 指令遵循是 Agent 可靠调工具的前提
- [[sources/li-hongyi-genai-2025]] — 含 Agent 专讲

## Related

- [[synthesis/concepts-agent-operating-system × concepts-ai-agent]]
