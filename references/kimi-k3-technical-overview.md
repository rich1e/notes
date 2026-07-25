---
title: Kimi K3 — Technical Overview (AI News Summary)
category: references
tags: [ai, llm, chinese-ai, open-source]
sources:
  - "https://artificialintelligence-news.com/2025/07/kimi-k3-3-trillion-parameters/"
source_url: "https://artificialintelligence-news.com/2025/07/kimi-k3-3-trillion-parameters/"
created: 2026-07-23T08:00:00Z
updated: 2026-07-23T08:00:00Z
summary: >-
  AI News 对 Kimi K3 的技术深度分析，涵盖 2.8T MoE 架构、Delta Attention、QAT、基准结果、定价和地缘政治影响。
provenance:
  extracted: 0.85
  inferred: 0.10
  ambiguous: 0.05
base_confidence: 0.67
lifecycle: draft
lifecycle_changed: 2026-07-23
---

# Kimi K3 — Technical Overview (AI News)

**来源：** https://artificialintelligence-news.com/2025/07/kimi-k3-3-trillion-parameters/
**发布时间：** 2026 年 7 月（估计）

## 主要内容

本文对 Kimi K3 发布进行深度技术分析，是目前最完整的英文技术报道之一。

## 关键声明

### 规模
- 2.8 万亿参数 → 首个开权重 3T 级模型（超越 DeepSeek V4 Pro 的 1.6T）[extracted]

### 架构
- MoE：896 专家，每 token 激活 16 个（~1.8% 稀疏率）[extracted]
- 上下文窗口：100 万 token [extracted]
- Kimi Delta Attention：解决长上下文 KV 缓存内存问题，6.3× 解码加速（1M token 下）[extracted]
- Attention Residuals：~25% 训练效率提升，<2% 额外成本 [extracted]
- 量化感知训练（4-bit），权重 ~1.4TB vs FP16 ~5.6TB [extracted]

### 基准
- Chatbot Arena Frontend Code：1,679 分，排名第一 [extracted]
- 整体落后于 Fable 5 和 GPT 5.6 Sol（Moonshot 官方承认）[extracted]
- SWE Marathon 比较存在方法论质疑（Fable 5 有 35% fallback）[extracted]

### 定价
- 输入 $3/M、输出 $15/M、缓存命中 $0.30/M [extracted]

### 硬件
- 推荐：64+ 加速器内存池化
- 测试平台：H200S、L20、未披露供应商 GPU [extracted]

## 局限性

- 权重尚未发布（预计 2026-07-27），所有技术声明为第一方，待独立复现
- Delta Attention 的具体算法机制未公开
- 标准推理框架（vLLM 等）在发布时暂不支持新特性

## 关联页面

- [[entities/kimi-k3]] — 模型实体页
- [[concepts/mixture-of-experts]] — MoE 架构概念
- [[concepts/kimi-delta-attention]] — Delta Attention 技术
- [[synthesis/Research: Kimi K3]] — 综合研究报告
