---
title: Kimi Delta Attention
category: concepts
tags: [ai, llm, attention-mechanism, long-context]
sources:
  - "https://artificialintelligence-news.com/2025/07/kimi-k3-3-trillion-parameters/"
  - "https://www.kimi.com/blog/kimi-k3"
created: 2026-07-23T08:00:00Z
updated: 2026-07-23T12:00:00Z
summary: >-
  Moonshot AI 在 Kimi K3 中提出的 Attention 变体，针对长上下文推理时 KV 缓存内存爆炸问题，声称在 100 万 token 上下文下解码速度提升最高 6.3×。
lifecycle: draft
lifecycle_changed: 2026-07-23
---

# Kimi Delta Attention

## 问题背景

标准 Transformer 的 KV 缓存随上下文长度线性增长。在 [[entities/kimi-k3]] 的 100 万 token 上下文窗口中，**KV 缓存本身（而非模型权重）成为最大的内存负担**：

- 2.8T 参数在 4-bit 量化下 ≈ 1.4TB（静态）
- 100 万 token KV 缓存在 FP16 下可达数十到数百 GB（动态，随序列增长）

## 核心机制

Moonshot 公开的技术细节有限（权重尚未发布），已知：
- 以"Delta"（差值/增量）的方式表示相邻 token 或层间的 Attention 状态变化，减少冗余存储
- 目标是压缩 KV 缓存的内存增长曲线，而非减少激活参数数量

## 性能声明

| 场景 | 提升 |
|---|---|
| 100 万 token 上下文解码速度 | 最高 6.3× |

⚠️ 目前为 Moonshot 第一方声明，尚待独立复现（权重发布日：2026-07-27）

## 与其他技术的关系

| 技术 | 方向 | 目标 |
|---|---|---|
| Kimi Delta Attention | 推理端 | 压缩 KV 缓存内存 |
| Attention Residuals | 训练端 | 提升训练效率（~25%）|
| [[concepts/mixture-of-experts]] | 架构端 | 降低每 token 算力 |
| [[concepts/llm-speculative-decoding]] | 推理端 | 加速 token 生成 |
| [[concepts/prompt-caching]] | 系统端 | 复用跨请求的 KV 缓存 |

## 与 Attention Residuals 的协同

官方博客明确描述了 KDA 与 AttnRes 的分工：
- **KDA**：提供高效的长序列扩展 Attention 基础，改善信息跨序列长度的流动
- **AttnRes**：跨模型深度**有选择地**提取表示，而非均匀累积（"selectively retrieves representations across depth rather than accumulating them uniformly"）
- 两者构成 K3"设计为可在万亿参数以上扩展"的架构主干

## 服务侧效益

KDA 与 prefill 缓存结合，使 K3 能以有竞争力的 token 价格提供服务（Kimi API 缓存命中输入仅 $0.30/MTok），尽管模型规模极大。

## 工程状态

- Moonshot 向 vLLM 社区贡献了对应的 KV 缓存实现（与模型权重同步发布）
- KDA 的 prefill 缓存支持已随 K3 发布
- 技术细节将在 K3 技术报告中发布（与权重同步）

## 相关页面

- [[entities/kimi-k3]] — 使用此技术的模型
- [[entities/moonshot-ai]] — 开发方
- [[concepts/mixture-of-experts]] — K3 的另一个核心架构创新
