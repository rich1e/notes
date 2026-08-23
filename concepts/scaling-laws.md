---
title: Scaling Laws — 规模与性能的幂律经验规律
category: concepts
tags:
  - llm
  - deep-learning
  - concept
summary: Scaling laws 揭示模型损失随参数量、数据量、算力呈幂律下降；Chinchilla 进一步指出给定算力下参数与数据应等比放大,指导 LLM 训练资源分配。
sources:
  - "https://arxiv.org/abs/2001.08361"
created: 2026-07-31T07:10:00Z
updated: 2026-07-31T07:10:00Z
tier: supporting
lifecycle: draft
lifecycle_changed: "2026-07-31"
base_confidence: 0.55
provenance:
  extracted: 0.88
  inferred: 0.09
  ambiguous: 0.03
relationships:
  - target: "[[concepts/transformer-architecture]]"
    type: related_to
  - target: "[[concepts/llm-training-pipeline]]"
    type: related_to
---

# Scaling Laws — 规模与性能的幂律经验规律

> Scaling laws(Kaplan 等 2020;Chinchilla 2022)是一组经验规律:LLM 的测试损失随**参数量、数据量、算力**的增大而以**幂律**平滑下降,让训练效果在开跑前可被预测。

## 核心结论

| 规律 | 内容 |
|------|------|
| **幂律下降** | 损失 `L ∝ N^(-α)`(N=参数量),数据、算力各有类似指数 |
| **可预测性** | 小模型上拟合的曲线可外推到更大规模,先验估算收益 |
| **Chinchilla 最优** | 给定算力预算,参数量与训练 token 数应**等比放大**;此前的大模型普遍"欠训练"(数据太少) |

## 为什么重要

- **资源分配决策**:与其盲目堆参数,不如按 Chinchilla 配比同步扩数据,单位算力收益更高。
- **投资判据**:能量化"再投 10× 算力大约能降多少损失",支撑训练前的 ROI 评估。
- **架构无关性**:规律主要由 [[concepts/transformer-architecture]] 的可扩展性支撑,但对具体结构不敏感。

## 局限

- 损失下降 ≠ 下游能力线性提升;能力常呈**涌现(emergence)**的阶跃。
- 幂律指数随数据质量、架构改动而变,非普适常数。

## 相关页面

- [[concepts/transformer-architecture]] — scaling 的可扩展模型基础
- [[concepts/llm-training-pipeline]] — scaling 指导训练资源配比
- stanford-cs336-spring2025 — 含 Scaling 作业单元
