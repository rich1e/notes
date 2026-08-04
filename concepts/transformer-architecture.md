---
title: Transformer 架构 — 自注意力驱动的序列建模骨架
category: concepts
tags:
  - llm
  - deep-learning
  - concept
summary: Transformer 用自注意力替代循环/卷积做序列建模，靠 Q/K/V 注意力 + 多头 + 位置编码 + 残差前馈堆叠，是当代 LLM（GPT/BERT 等）的统一骨架。
sources:
  - "https://arxiv.org/abs/1706.03762"
created: 2026-07-31T07:10:00Z
updated: 2026-07-31T07:10:00Z
tier: core
lifecycle: draft
lifecycle_changed: "2026-07-31"
base_confidence: 0.55
provenance:
  extracted: 0.9
  inferred: 0.07
  ambiguous: 0.03
relationships:
  - target: "[[concepts/llm-training-pipeline]]"
    type: related_to
  - target: "[[concepts/mechanistic-interpretability]]"
    type: related_to
---

# Transformer 架构 — 自注意力驱动的序列建模骨架

> Transformer(Vaswani 等 2017,《Attention Is All You Need》)用**自注意力**取代 RNN/CNN 做序列建模,让每个 token 直接与序列中所有 token 交互,是当代大模型的统一骨架。

## 核心组件

| 组件 | 作用 |
|------|------|
| **自注意力(Self-Attention)** | 每个 token 用 Query/Key/Value 与其余 token 加权聚合,`softmax(QKᵀ/√d)·V` |
| **多头(Multi-Head)** | 并行多组 Q/K/V,捕捉不同关系子空间 |
| **位置编码** | 注意力本身无序,靠位置编码(正弦 / 可学习 / RoPE)注入顺序信息 |
| **前馈网络(FFN)** | 每 token 独立的两层 MLP,非线性变换 |
| **残差 + LayerNorm** | 稳定深层堆叠的训练 |

## 为什么重要

- **可并行**:相比 RNN 的时序依赖,注意力可整序列并行计算,契合 GPU。
- **长程依赖**:任意两 token 一跳可达,弱化了梯度消失对长依赖的限制。
- **可扩展**:堆叠层数 / 加宽维度 / 堆数据,性能可预测提升——这正是 [[concepts/scaling-laws]] 的经验基础。

## 两大范式

- **Decoder-only(GPT 系)**:因果掩码自回归生成,当代主流 LLM 形态。
- **Encoder-only(BERT 系)**:双向编码做理解类任务。

## 相关页面

- [[concepts/llm-training-pipeline]] — Transformer 是训练流水线的模型主体
- [[concepts/scaling-laws]] — 描述 Transformer 规模与性能的经验规律
- [[concepts/mechanistic-interpretability]] — 逆向解析 Transformer 内部计算
- [[sources/andrej-karpathy-zero-to-hero]] — 手写 GPT 讲透注意力
- [[sources/sebastian-raschka-llms-from-scratch-book]] — 从零实现 Transformer
- [[sources/dakingrai-mech-interp-papers]] — 以 Transformer 为解析对象
- [[synthesis/concepts-llm-training-pipeline × concepts-transformer-architecture]] — synthesis:架构(静态容量)与训练(动态能力)的正交分工
