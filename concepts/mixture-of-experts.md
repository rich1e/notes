---
title: Mixture-of-Experts (MoE)
category: concepts
tags: [ai, llm, architecture, deep-learning]
sources:
  - "https://artificialintelligence-news.com/2025/07/kimi-k3-3-trillion-parameters/"
created: 2026-07-23T08:00:00Z
updated: 2026-07-23T08:00:00Z
summary: >-
  LLM 架构模式：将参数划分为多个专家模块，每次推理只激活少数专家，以极低的每 token 算力代价实现超大模型规模。
lifecycle: draft
lifecycle_changed: 2026-07-23
---

# Mixture-of-Experts（混合专家架构）

## 核心思想

将模型参数分成 N 个"专家"（Expert）子网络 + 一个路由器（Router）。推理时，路由器为每个 token 选择少数几个（通常 2～16 个）专家处理，其余专家不参与计算。

**关键权衡：**
- **内存（Memory）**：所有专家必须常驻显存，总参数量巨大
- **算力（FLOP）**：每个 token 只激活少数专家，实际算力与激活参数量成比例，不随总参数量线性增长

## 关键指标

- **总参数量（Total Parameters）**：决定内存需求
- **激活参数量（Active Parameters）**：决定每 token 算力成本
- **稀疏率（Sparsity）**：= 激活专家数 / 总专家数，越低算力越省

## 代表性规格

| 模型 | 总参数 | 激活专家数 / 总专家数 | 稀疏率 |
|---|---|---|---|
| [[entities/kimi-k3]] | 2.8T | 16 / 896 | ~1.8% |
| DeepSeek V4 Pro | 1.6T | — | — |

## 优势与局限

**优势：**
- 相同算力预算下，MoE 可训练远超 Dense 模型的参数量
- 推理吞吐量高（单 token 算力低）

**局限：**
- 内存需求不可压缩（所有专家必须加载）
- 专家负载不均（需精细的路由损失设计）
- 分布式部署复杂（All-to-All 通信开销）

## 与相关技术的关系

- **量化感知训练（QAT）**：与 MoE 结合可进一步压缩内存（K3 从 5.6TB 压至 1.4TB）
- **[[concepts/kimi-delta-attention]]**：解决 MoE 大模型的长上下文 KV 缓存内存问题
- **[[concepts/llm-speculative-decoding]]**：另一类推理加速方向，与 MoE 正交

## 参考页面

- [[entities/kimi-k3]] — 2.8T/896 专家 MoE 的具体实现
- [[entities/moonshot-ai]] — Kimi K3 的开发商

- [[synthesis/concepts-mixture-of-experts × entities-kimi-k3]] — synthesis
