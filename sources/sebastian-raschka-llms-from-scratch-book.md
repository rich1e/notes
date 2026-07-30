---
title: >-
  Sebastian Raschka — Build a Large Language Model (From Scratch)
category: references
tags: [llm, book, education]
sources:
  - "https://github.com/rasbt/LLMs-from-scratch"
  - "https://www.manning.com/books/build-a-large-language-model-from-scratch"
source_url: "https://github.com/rasbt/LLMs-from-scratch"
created: 2026-07-27T07:30:00Z
updated: 2026-07-27T07:30:00Z
summary: >-
  Raschka 的「Build a Large Language Model (From Scratch)」Manning 书与同名 GitHub 仓库（≈9k+ stars），从零用 PyTorch 实现 GPT 全流程：数据→注意力→模型→预训练→指令微调。
provenance:
  extracted: 0.85
  inferred: 0.10
  ambiguous: 0.05
base_confidence: 0.90
lifecycle: draft
lifecycle_changed: 2026-07-27
---

# Sebastian Raschka — Build a Large Language Model (From Scratch)

## URL

- GitHub: https://github.com/rasbt/LLMs-from-scratch
- Manning: https://www.manning.com/books/build-a-large-language-model-from-scratch

## 内容概述

Manning 2024 出版的实战书（ISBN 978-1633437166）。GitHub 仓库是书的开源版本，持续迭代加入新架构与新主题。

## 章节结构（provenance: extracted）

**Setup & Preliminaries**
- Setup recommendations（Python/Docker/环境）
- Ch 1: Understanding Large Language Models（纯概念）

**主体**
- Ch 2: Working with Text Data — tokenization、dataloader
- Ch 3: Coding Attention Mechanisms — 多头注意力实现
- Ch 4: Implementing a GPT Model from Scratch — 完整 GPT 架构
- Ch 5: Pretraining on Unlabeled Data — 训练循环、生成、加载权重
- Ch 6: Finetuning for Text Classification — 分类器适配
- Ch 7: Finetuning to Follow Instructions — 指令微调、评估、DPO

**附录**
- A: PyTorch 入门（含分布式训练）
- B: 参考文献与延伸阅读
- C: 习题答案
- D: 训练循环增强（学习率调度、超参）
- E: 参数高效微调 LoRA

## 增量扩展（provenance: extracted）

仓库持续追加新主题的 Bonus 章节：
- **注意力变体**：Grouped-Query、Multi-Head Latent、Sliding Window、Gated DeltaNet、DSA、Cross-Layer KV sharing
- **其他架构**：Llama 3.2、Qwen3（dense + MoE）、Gemma 3、Olmo 3、Tiny Aya、Qwen3.5、Gemma 4
- **Tokenization**：BPE 从零实现、tiktoken 扩展
- **Reasoning（姊妹仓库）**：GRPO/RLVR、verifier/MMLU evals、inference scaling
- **UI**：Gradio 界面（预训练 / 分类 / 指令微调）

## 先修要求（provenance: extracted）

- **强 Python 基础**（最重要）
- 深度神经网络经验有帮助但非必需
- PyTorch 熟悉度有用（附录 A 涵盖要点）
- **不需要专门硬件**——代码可在普通笔记本跑，自动用 GPU

## 价值判断（provenance: inferred）

- 与 Karpathy 系列对照：**Karpathy = 手写直觉**，**Raschka = 工程化实现**——Raschka 用 PyTorch 但不隐藏细节，每行代码都在建立心智模型。
- "普通笔记本可跑"这一点是该书**最重要的实用卖点**——读者不会被硬件门槛劝退。
- 增量架构扩展使其**长期保持新鲜度**：截至 2025 已经覆盖了 Llama 3.2、Qwen3（含 MoE）、Gemma 3 等前沿架构。

## 局限性

- **不教 PyTorch 本身**（要查附录 A）
- 截至 2025 仍未单独成章讲：分布式训练（DeepSpeed/FSDP/Megatron）、推理优化（vLLM/TensorRT-LLM）、RLVR、agent/工具调用
- 单机单卡视角，与 Stanford CS336 形成"工程实现 × 系统设计"对照

## 关联

- [[entities/sebastian-raschka]]
- [[sources/andrej-karpathy-zero-to-hero]]
- [[sources/stanford-cs336-spring2025]]
- [[concepts/transformer-architecture]]
- [[concepts/llm-training-pipeline]]