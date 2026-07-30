---
title: Moonshot AI (月之暗面)
category: entities
tags: [chinese-ai, llm, research-lab]
sources:
  - "https://artificialintelligence-news.com/2025/07/kimi-k3-3-trillion-parameters/"
  - "https://www.kimi.com/"
created: 2026-07-23T08:00:00Z
updated: 2026-07-23T08:00:00Z
summary: >-
  中国 AI 研究公司，以 Kimi 品牌发布大语言模型，K 系列以超大规模开权重模型见长，2026 年推出全球首个 3T 级开权重模型 Kimi K3。
lifecycle: draft
lifecycle_changed: 2026-07-23
---

# Moonshot AI（月之暗面）

## 基本信息

- **品牌名称：** Kimi
- **总部：** 中国
- **产品方向：** 大语言模型（LLM）研究与商业化
- **定位：** 与 DeepSeek 并列的中国前沿 AI 代表性实验室

## 主要模型系列

| 模型 | 参数规模 | 特点 |
|---|---|---|
| Kimi K2（系列）| ~1T（Kimi-K2-Base/Instruct）| 多模态（Image-Text-to-Text）|
| [[entities/kimi-k3]] | ~2.8T（3T 级）| 全球首个开权重 3T 类模型，代码与 Agent 工作流优化 |
| Moonlight-16B-A3B | 16B | 小规模模型 |
| Kimi-VL-A3B | 16B | 视觉语言模型 |

## 技术理念

- 以架构创新应对算力约束（量化感知训练、[[concepts/kimi-delta-attention]]、Attention Residuals）
- 量化优先策略：4-bit 精度训练，降低硬件门槛，支持非 Nvidia 硬件
- 向 vLLM 等开源推理项目贡献代码（KV 缓存优化）

## 市场地位

- 与 DeepSeek 同被视为"逼迫西方 AI 实验室重新审视算力优势"的中国代表
- K3 发布后，Kimi 的定价从廉价层（DeepSeek 竞争）转向中高端层（$15/M 输出 token）
- 分析师（美国银行）将 K3 视为"大规模预训练 + 架构创新在算力限制下仍能产生阶跃式提升"的证明

## 相关页面

- [[entities/kimi-k3]] — K3 模型详细技术规格
- [[concepts/mixture-of-experts]] — K3 所用核心架构模式
- [[concepts/kimi-delta-attention]] — K3 推理优化技术
- [[synthesis/Research: Kimi K3]] — 综合研究报告
