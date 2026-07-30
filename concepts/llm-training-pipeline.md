---
title: >-
  LLM Training Pipeline — 大模型训练三阶段
category: concepts
tags: [llm, training, alignment]
sources:
  - "https://github.com/karpathy/nn-zero-to-hero"
  - "http://cs336.stanford.edu/spring2025/"
created: 2026-07-27T07:30:00Z
updated: 2026-07-27T07:30:00Z
summary: >-
  现代 LLM 训练分三阶段：预训练（读课本）→ 监督微调 SFT（看例题）→ 强化学习 RLHF/RLVR（做练习）。这是 2025 年所有主流 LLM 的标准流程。
provenance:
  extracted: 0.80
  inferred: 0.15
  ambiguous: 0.05
base_confidence: 0.85
lifecycle: draft
lifecycle_changed: 2026-07-27
---

# LLM Training Pipeline — 大模型训练三阶段

## 核心定义

LLM 从零到有用的训练**几乎都是这三阶段**：

```
[1. Pretraining] → [2. Supervised Fine-Tuning, SFT] → [3. RLHF / RLVR]
读互联网文本          学习人类示范答案               用反馈/可验证奖励
                                                       继续优化
```

## 三阶段类比（Karpathy 2025 教科书类比）

| 阶段 | 教科书类比 | 数据 | 计算占比 |
|------|-----------|------|---------|
| Pretraining | 读课本（背景知识） | 万亿 token 原始文本 | ≈ 95% |
| SFT | 做例题（学专家解法） | 几万-几十万条人工示范 | ≈ 4% |
| RLHF / RLVR | 做章末练习题（试错） | 几十万-几百万条偏好/可验证题 | ≈ 1% |

## 各阶段细节

### 1. Pretraining（预训练）

- **目标**：next-token prediction 自监督任务
- **数据**：Common Crawl 等网页 + 书籍 + 代码 + Wikipedia
- **架构**：Dense Transformer / MoE / SSM 等
- **算力**：几千-几万张 GPU × 几个月
- **产物**：base model（如 Llama-3-8B-base）——能续写文本但不会对话

### 2. Supervised Fine-Tuning（SFT，监督微调 / 指令微调）

- **目标**：让模型学会"回答问题"而非"续写"
- **数据**：人工编写的指令-回答对（instruction-response pairs）
- **典型规模**：1万-100万条
- **产物**：instruct model（如 Llama-3-8B-Instruct）——能用 chat 形式响应

### 3. RLHF / RLVR（人类反馈强化学习 / 可验证奖励强化学习）

- **RLHF**（Reinforcement Learning from Human Feedback）：人类对多个回答打分，训练 reward model，再用 PPO 等 RL 算法微调 LLM
- **RLVR**（Reinforcement Learning from Verifiable Rewards，2025 新范式）：用**可客观验证**的奖励（数学题答案、代码测试用例、单元测试通过率）——不要人类反馈，要 ground truth

RLVR 是 2024 末–2025 的关键转向，代表作：DeepSeek-R1、OpenAI o1/o3。

## 与"教科书"三阶段的对照（更技术化）

| 教科书阶段 | LLM 阶段 | 关键技术 |
|----------|---------|---------|
| 识字 → 看课本 | Pretraining | Tokenization, Transformer/MoE, AdamW, Distributed Training (FSDP/Megatron/DeepSpeed) |
| 例题讲解 | SFT | Instruction datasets, LoRA/QLoRA, Flash Attention |
| 单元测试 | RLHF / RLVR | Reward Model, PPO/DPO/GRPO, Verifier |

## 学习路径建议

- **入门先理解 pretraining**——这是 LLM 一切能力的来源；看完 [[sources/andrej-karpathy-zero-to-hero]] 的「Let's build GPT」就掌握核心。
- **再学 SFT**——[[sources/sebastian-raschka-llms-from-scratch-book]] Ch 7 是最干净的入门。
- **最后学 RLHF/RLVR**——这是前沿、变化最快，建议直接看 DeepSeek-R1 论文与 Stanford CS336 L15-L17。

## 关联

- concepts/transformer-architecture
- concepts/instruction-tuning
- concepts/rlvr
- [[concepts/mixture-of-experts]]
- concepts/scaling-laws
- [[sources/andrej-karpathy-zero-to-hero]]
- [[sources/stanford-cs336-spring2025]]