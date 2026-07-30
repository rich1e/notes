---
title: >-
  Stanford CS336 — Language Modeling from Scratch (Spring 2025)
category: references
tags: [llm, education, research]
sources:
  - "http://cs336.stanford.edu/spring2025/"
  - "https://github.com/stanford-cs336/spring2025-lectures"
source_url: "http://cs336.stanford.edu/spring2025/"
created: 2026-07-27T07:30:00Z
updated: 2026-07-27T07:30:00Z
summary: >-
  Stanford CS336（Hashimoto & Liang 主讲，Spring 2025）从零实现一个 LLM：数据、架构、训练系统、对齐全栈覆盖；含 5 次作业（Basics/Systems/Scaling/Data/Alignment）。
provenance:
  extracted: 0.90
  inferred: 0.05
  ambiguous: 0.05
base_confidence: 0.92
lifecycle: draft
lifecycle_changed: 2026-07-27
---

# Stanford CS336 — Language Modeling from Scratch (Spring 2025)

## URL

- 课程主页：http://cs336.stanford.edu/spring2025/
- 讲义仓库：https://github.com/stanford-cs336/spring2025-lectures

## 课程定位（provenance: extracted）

5 学分实现密集型课。学生从零搭建一个语言模型，涵盖**数据收集/清洗、Transformer 构建、训练、评估**。"代码量至少比其他课大一个数量级"（Liang 原话）。

## 讲师

- Tatsunori Hashimoto（Stanford NLP）
- Percy Liang（Stanford CRFM 主任）

## 先修要求（provenance: extracted）

- Python 熟练度（课程脚手架最少）
- 深度学习与系统优化经验（PyTorch、内存层级）
- 大学微积分与线性代数（如 MATH 51、CME 100）
- 基础概率统计（如 CS 109）
- 机器学习（如 CS221、CS229、CS230、CS124、CS224N）

## 作业（5 次，in order）

1. **Basics**（4/1 出，4/15 交）：实现 tokenizer、模型架构、optimizer；训练一个最小 LM
2. **Systems**（4/15 出，4/30 交）：用 Triton-based FlashAttention2 剖析/基准测试；构建分布式训练
3. **Scaling**（4/29 出，5/6 交）：通过训练 API 拟合 scaling laws
4. **Data**（5/6 出，5/23 交）：处理 Common Crawl；过滤和去重
5. **Alignment and Reasoning RL**（5/23 出，6/6 交）：SFT 与 RL 用于数学推理；可选 DPO/安全部分

## 讲座主题（按 topic 分组，provenance: extracted）

### Architectures
- L1（4/1）Overview、tokenization（Percy）
- L3（4/8）Architectures、hyperparameters（Tatsu）
- L4（4/10）Mixture of experts（Tatsu）

### Systems
- L2（4/3）PyTorch、resource accounting（Percy）
- L5（4/15）GPUs（Tatsu）
- L6（4/17）Kernels、Triton（Tatsu）
- L7（4/22）Parallelism（Tatsu）
- L8（4/24）Parallelism（Percy）
- L10（5/1）Inference（Percy）

### Data
- L13（5/13）Data（Percy）
- L14（5/15）Data（Percy）

### Scaling
- L9（4/29）Scaling laws basics（Tatsu）
- L11（5/6）Scaling details（Tatsu）

### Evaluation
- L12（5/8）Evaluation（Percy）

### Alignment
- L15（5/20）Alignment - SFT/RLHF（Tatsu）
- L16（5/22）Alignment - RL/RLVR（Tatsu）
- L17（5/27）Alignment - RL（Percy）

### Guest Lectures
- L18（5/29）Junyang Lin（Qwen）
- L19（6/3）Mike Lewis（AI2）

## 课程政策（provenance: extracted）

- **Late days**：总共 6 天，每次作业最多 3 天
- **AI 工具**：允许 LLM 用于低级/高级问题；**应禁用** AI autocomplete（Cursor Tab、GitHub CoPilot）
- **合作**：允许学习小组；提交个人作业并列出成员
- **既有代码**：除非另有说明，否则不允许
- **提交**：仅 Gradescope；截止前无限次提交

## GPU 资源（自学用，H100 80GB，June 2025）

| 提供商 | 价格（/小时） |
|--------|------------|
| RunPod | $1.99–$2.99 |
| Lambda Labs | $2.49–$3.29 |
| Paperspace | $2.24 |
| Together | $2.85（最少 8 卡） |

## 价值判断（provenance: inferred）

- 是**严肃 LLM 工程师 / 研究员**的"对标"——CS336 与 Raschka 的区别是**单机实现 × 系统视角**。
- Hashimoto 与 Liang 的组合代表了"Stanford NLP 学术训练"与"CRFM 工程实践"的合并；Junyang Lin（Qwen）与 Mike Lewis（AI2）的客座讲座保证前沿视角。
- **禁用 AI autocomplete** 这条政策值得注意——CS336 把"自己写代码"视为训练目标之一，而非效率工具。

## 局限性

- 是 Stanford 校内课程，作业批改/GPU 配额对外不可得；自学者只能看讲义。
- 与 Karpathy / Raschka 路径相比**门槛高得多**——CS336 假设你已会 ML/系统基础。

## 关联

- [[sources/andrej-karpathy-zero-to-hero]]
- [[sources/sebastian-raschka-llms-from-scratch-book]]
- [[concepts/llm-training-pipeline]]
- [[concepts/scaling-laws]]
- [[concepts/mixture-of-experts]]