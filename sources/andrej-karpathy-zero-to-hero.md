---
title: >-
  Andrej Karpathy — Neural Networks: Zero to Hero
category: references
tags: [llm, education, research]
sources:
  - "https://github.com/karpathy/nn-zero-to-hero"
source_url: "https://github.com/karpathy/nn-zero-to-hero"
created: 2026-07-27T07:30:00Z
updated: 2026-07-27T07:30:00Z
summary: >-
  Karpathy 的「Neural Networks: Zero to Hero」视频系列，从 micrograd 手写反向传播一路推到 GPT 与 tokenizer 共 8 讲，是 LLM 学习的事实标准入门路径。
provenance:
  extracted: 0.85
  inferred: 0.10
  ambiguous: 0.05
base_confidence: 0.85
lifecycle: draft
tier: core
lifecycle_changed: 2026-07-27
---

# Andrej Karpathy — Neural Networks: Zero to Hero

## URL

https://github.com/karpathy/nn-zero-to-hero

## 内容概述

Karpathy（前 Tesla AI 总监、OpenAI 创始成员）录制的 8 讲动手系列，从零手写反向传播出发，逐步构建到完整 GPT 与 BPE tokenizer。配套 Jupyter notebooks 公开在 lectures/ 目录。

## 关键事实（provenance: extracted）

- **先修要求**：仅 Python 基础 + 高中微积分的"模糊记忆"（Karpathy 原话）。
- **8 讲顺序**（截至 2025）：
  1. **The spelled-out intro to neural networks and backpropagation: building micrograd** — 手写 scalar autograd 引擎，搭建反向传播的肌肉记忆
  2. **makemore Part 1: Bigrams** — 字符级 bigram 语言模型，引入 torch.Tensor
  3. **makemore Part 2: MLP** — 多层感知器，引入 train/dev/test 拆分、过拟合诊断
  4. **makemore Part 3: Activations, Gradients, BatchNorm** — 激活/梯度诊断，BatchNorm
  5. **makemore Part 4: Backprop Ninja** — 手动反向传播不调 loss.backward()
  6. **makemore Part 5: WaveNet** — 树状 CNN 架构
  7. **Let's build GPT: from scratch, in code, spelled out** — 完整 GPT 实现（≈ nanoGPT 90%）
  8. **Let's build the GPT Tokenizer** — 手写 BPE，链接 LLM 怪相到 tokenization

- **后续扩展讲座**（2025）：
  - **Let's reproduce GPT-2 (124M)** — 4 小时现场训练复现 GPT-2
  - **Deep Dive into LLMs like ChatGPT**（2025-02，3.5 小时）— 预训练 / SFT / RLHF 全流程
  - **nanochat**（2025-11，GitHub: karpathy/nanochat）— 全栈 ChatGPT 克隆，比 nanoGPT 多了完整训练+推理管道

## 价值判断（provenance: inferred）

- 系列以"先手写、再调用库"为方法论核心；不靠 PyTorch 隐藏细节。
- 在所有学习路径推荐中反复出现的"通用前置资源"——Karpathy 风格已成为事实标准。
- 与 [[entities/sebastian-raschka]] 的 [[sources/sebastian-raschka-llms-from-scratch-book]] 形成"视频+书籍"对照：Karpathy 是手写直觉，Raschka 是工程化实现。

## 局限性

- 截至 2025 年系列**不覆盖**：MoE、Mamba/SSM 等非 Transformer 架构；多模态；RLVR/推理模型；分布式训练细节
- 用 PyTorch 但不教 PyTorch，需要读者自行补充

## 关联

- [[entities/andrej-karpathy]]
- [[sources/sebastian-raschka-llms-from-scratch-book]]
- [[concepts/transformer-architecture]]
- [[concepts/llm-training-pipeline]]