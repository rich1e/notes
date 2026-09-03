---
title: >-
  Andrej Karpathy
category: entities
tags: [Deepseek, education, research]
sources:
  - "https://github.com/karpathy/nn-zero-to-hero"
created: 2026-07-27T07:30:00Z
updated: 2026-07-27T07:30:00Z
tier: peripheral
summary: >-
  Andrej Karpathy：前 Tesla AI 总监、OpenAI 创始成员，现独立教育者。以「Neural Networks: Zero to Hero」视频系列、nanoGPT、nanochat 著称——LLM 教育的事实标准制定者。
provenance:
  extracted: 0.85
  inferred: 0.10
  ambiguous: 0.05
base_confidence: 0.90
lifecycle: reviewed
lifecycle_changed: 2026-09-03
lifecycle_reason: "auto-promoted by wiki-lint --consolidate: age>30d, confidence>0.9"
lifecycle_changed: 2026-07-27
---

# Andrej Karpathy

## 简介

Andrej Karpathy 是当代最有影响力的 AI 教育者之一。前 Tesla AI 总监（2017-2024，领导 Autopilot 视觉团队），OpenAI 创始成员（2015），现以独立研究者身份活跃在 YouTube / GitHub / X。

## 主要工作（provenance: extracted）

### 教育系列

- **Neural Networks: Zero to Hero**（2022-2025，8+ 讲）—— 见 andrej-karpathy-zero-to-hero
- **Deep Dive into LLMs like ChatGPT**（2025-02，3.5 小时）
- **Spelled-out intro to...** 系列：micrograd、makemore、GPT、tokenizer

### 开源项目

- **nanoGPT**（2023）—— 最简 GPT 训练库，≈300 行 PyTorch
- **nanochat**（2025-11）—— 全栈 ChatGPT 克隆（pretraining + SFT + RL + inference + UI），"$100 可买到的最佳 ChatGPT"
- **llm.c**（2024）—— 纯 C/CUDA 重写 GPT 训练，去掉 PyTorch 依赖
- **minbpe**（2024）—— BPE tokenizer 教学实现

### 重要观点（2025）

- **2025 范式转变**：RLVR（reinforcement learning from verifiable rewards）、"Jagged Intelligence"（AI 像"召唤的幽灵"不是"养大的动物"）、System Prompt Learning
- **教科书类比**：pretraining = 读课本，SFT = 做例题，RL = 做章末练习题

## 影响力判断（provenance: inferred）

- "Zero to Hero" 已成为事实标准 LLM 入门路径——任何中文/英文学习路线推荐**几乎都引用他**。
- nanoGPT 的"极简 + 可读"风格定义了 LLM 教学仓库的范式（rasbt/LLMs-from-scratch、Andrej 自己之后的项目都遵循）。
- 风格特征：**手写优先、不隐藏细节、强调直觉**——这与斯坦福学术派的"系统视角"形成对照。

## 关联

- andrej-karpathy-zero-to-hero
- [[entities/sebastian-raschka]]
- concepts/transformer-architecture
- [[concepts/llm-training-pipeline]]