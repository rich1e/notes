---
title: 指令微调 — 让预训练模型听懂并执行指令
category: concepts
tags:
  - llm
  - deep-learning
  - concept
summary: 指令微调(instruction tuning)在预训练后用「指令-回答」数据集有监督微调,使模型从「续写」转向「按指令办事」,是 InstructGPT/ChatGPT 对齐流程的关键一步。
sources:
  - "https://arxiv.org/abs/2203.02155"
created: 2026-07-31T07:10:00Z
updated: 2026-07-31T07:10:00Z
tier: supporting
lifecycle: draft
lifecycle_changed: "2026-07-31"
base_confidence: 0.55
provenance:
  extracted: 0.87
  inferred: 0.1
  ambiguous: 0.03
relationships:
  - target: "[[concepts/llm-training-pipeline]]"
    type: related_to
  - target: "[[concepts/transformer-architecture]]"
    type: related_to
---

# 指令微调 — 让预训练模型听懂并执行指令

> 指令微调(instruction tuning / SFT)在预训练之后,用大量**「指令 → 期望回答」**样本做有监督微调,把只会"续写下一个 token"的基座模型改造成"按人类指令办事"的助手。

## 在训练流水线中的位置

```
预训练(海量无标注文本) → 指令微调(SFT) → 偏好对齐(RLHF/DPO)
```

- **预训练**给出语言与世界知识,但只会续写;
- **指令微调**教会模型识别指令意图、遵循格式;
- **偏好对齐**再让输出更符合人类偏好(有用、无害)。

## 关键点

| 要素 | 说明 |
|------|------|
| **数据形态** | (instruction, [input], output) 三元组;多任务、多领域覆盖越广泛化越好 |
| **效果** | 显著提升 zero-shot 指令遵循,无需针对每任务再训 |
| **代表工作** | InstructGPT、FLAN、Alpaca 等 |
| **与 RLHF 关系** | SFT 是对齐的第一步,RLHF/DPO 在其之上进一步优化偏好 |

## 相关页面

- [[concepts/llm-training-pipeline]] — 指令微调是流水线中承上启下的一环
- [[concepts/transformer-architecture]] — 被微调的底层模型架构
- [[concepts/ai-agent]] — 强指令遵循是 Agent 能可靠调工具的前提
- li-hongyi-genai-2025 — 含指令微调专讲
