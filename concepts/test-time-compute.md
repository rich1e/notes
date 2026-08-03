---
title: >-
  Test-Time Compute / RLVR — 2025 推理模型新范式
category: concepts
tags: [llm, reasoning, alignment]
sources:
  - "http://cs336.stanford.edu/spring2025/"
  - "https://speech.ee.ntu.edu.tw/~hylee/genai/2025-spring.php"
created: 2026-07-27T07:30:00Z
updated: 2026-07-27T07:30:00Z
tier: peripheral
summary: >-
  2024 末–2025 关键转向：让模型在推理时"多想一会"（CoT 展开、verifier 引导搜索）而非一次吐完；用可验证奖励（RLVR）训练，无须人类反馈。代表：DeepSeek-R1、OpenAI o1/o3。
provenance:
  extracted: 0.70
  inferred: 0.20
  ambiguous: 0.10
base_confidence: 0.75
lifecycle: draft
lifecycle_changed: 2026-07-27
---

# Test-Time Compute / RLVR — 2025 推理模型新范式

## 核心定义

**Test-Time Compute Scaling**：在推理（inference）阶段投入更多算力，让模型"多想一会儿"，换更高的任务准确率——而不是单纯靠训练时把模型做大。

这是 2024 末 DeepSeek-R1、OpenAI o1/o3 之后整个行业的**新范式**。

## 三层范式对比（provenance: extracted）

| 范式 | 何时花算力 | 代表 | 代价 |
|------|----------|------|------|
| **Train-time compute** | 训练时（pretrain + SFT + RL） | GPT-4、Llama 3 | 单次训练千万美元+ |
| **Test-time compute（Naive CoT）** | 推理时给 prompt 加 "think step by step" | 任何 LLM | 推理慢、效果不稳 |
| **Test-time compute（Scaled）** | 推理时做大量内部 CoT + verifier 引导搜索 | o1/o3、DeepSeek-R1 | 推理成本 10-100× |

## 关键技术

### 1. Chain-of-Thought（CoT）规模化

- 模型在最终答案前先生成长长的思考过程（"Let's think step by step..."）
- 训练时就让它习惯写长思考链
- 推理时**展开更多 token** → 表现更强（数学/代码/逻辑任务）

### 2. Verifier 引导搜索

- 训练一个 **verifier**（判别器）判断中间步骤是否正确
- 推理时用 **beam search / MCTS** 在候选 CoT 路径里搜索
- 代表：OpenAI o1（被披露使用过程奖励模型 PRM）
- 数学/代码特别有效——因为有 ground truth 可验证

### 3. RLVR（Reinforcement Learning from Verifiable Rewards）

- **不要人类反馈**（不像 RLHF）
- 用**可客观验证**的奖励：数学题答案对错、单元测试通过率、SQL 查询执行结果
- 算法：GRPO（DeepSeek-R1）、PPO with rule-based rewards
- **优势**：数据生成便宜、避免 reward hacking、训练稳定

## 为什么这是 2025 关键转向（provenance: inferred）

1. **训练边际收益递减**：模型从 7B 到 70B 到 700B，性能提升是次线性的；再加 10× 算力可能只换 5% 准确率。
2. **推理成本相对可分摊**：test-time compute 是按查询付费，用户可以选"快速模式 vs 深度思考模式"。
3. **可验证任务占比大**：数学、代码、定理证明——这些任务奖励信号清晰，RLVR 训练稳定。
4. **开源跟上**：DeepSeek-R1 把整套 pipeline 开源，让中等团队也能训练自己的"推理模型"。

## 学习路径

1. **先理解 CoT**：Wei et al. 2022 "Chain-of-Thought Prompting" 论文
2. **再理解 RLHF → RLVR**：Anthropic / OpenAI RLHF 论文 → DeepSeek-R1 技术报告
3. **动手**：Raschka 仓库的 `reasoning` 姊妹项目提供 GRPO/RLVR 完整代码
4. **系统视角**：Stanford CS336 L15-L17（Alignment 系列）

## 局限性 / 开放问题（provenance: ambiguous）

- **不可验证任务怎么办**？创意写作、对话风格、审美——RLVR 无 ground truth，仍需要 RLHF 或人类评估。
- **推理成本爆炸**：o1 pro mode 单次查询可能 $10+——不是所有应用能负担。
- **过思考 (overthinking)**：模型在简单任务上也会展开长 CoT，浪费算力。
- **CoT 是否真"推理"**：学术界有争议；Anthropic 的 interpretability 团队认为模型经常"伪装思考"，实际靠 pattern matching。

## 关联

- [[concepts/llm-training-pipeline]]
- concepts/rlvr
- concepts/scaling-laws
- [[sources/stanford-cs336-spring2025]]
- [[sources/li-hongyi-genai-2025]]

## Related

- [[synthesis/Research: 学习AI大模型]] — 综合页:2025 Test-Time Compute 范式转向的上下文
