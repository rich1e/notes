---
title: >-
  Mechanistic Interpretability — 机制可解释性
category: concepts
tags: [llm, interpretability, research]
sources:
  - "https://github.com/Dakingrai/awesome-mechanistic-interpretability-lm-papers"
created: 2026-07-27T07:30:00Z
updated: 2026-07-27T07:30:00Z
summary: >-
  机制可解释性是逆向工程神经网络内部"电路"的研究方向。核心工具：SAE（稀疏自编码器找单义特征）、path patching（因果定位电路）、induction heads（ICL 核心组件）。
provenance:
  extracted: 0.75
  inferred: 0.20
  ambiguous: 0.05
base_confidence: 0.80
lifecycle: draft
lifecycle_changed: 2026-07-27
---

# Mechanistic Interpretability — 机制可解释性

## 核心定义

**Mechanistic Interpretability（MI）**：把神经网络当"机械装置"反向工程——找到负责特定行为的最小神经元/注意力头/电路，理解模型内部到底在算什么。

与"行为可解释性"（behavioral interpretability，即观察输入输出）不同，MI 试图打开黑箱看里面。

## 主要技术（provenance: extracted）

### 1. Logit Lens

- 把每一层 hidden state 直接接到 unembedding 看预测分布
- 揭示模型"何时决定"输出什么 token

### 2. Probing

- 训练一个简单分类器看 hidden state 里有没有某信息（语法、实体、情感）
- 揭示模型学到了什么表示

### 3. Sparse Autoencoders（SAE）— **2023 起的主流工具**

- 把多层 activations 分解为**单义**（monosemantic）特征的稀疏组合
- 解决"多义神经元"（一个神经元对多个不相关概念都激活）问题
- 代表作：Bricken et al. "Towards Monosemanticity"，Cunningham et al. "SAE Find Highly Interpretable Features"（ICLR'24）

### 4. Path Patching / Activation Patching

- **因果定位**：用某次 forward 的 activation 替换另一次 forward 的同位置 activation，看输出如何变化
- 如果变化 → 那条路径**对当前行为有因果贡献**
- 代表作：Wang et al. "Interpretability in the Wild: IOI Circuit"

### 5. ACDC（Automatic Circuit Discovery）

- 自动化剪枝掉不影响目标行为的边/节点
- 代表作：Conmy et al. NeurIPS'23

### 6. Attribution Patching

- Path patching 的梯度近似版，速度快 100-1000×
- 大模型上才变得可行

## 核心发现（provenance: extracted）

### Induction Heads（ICL 核心）

- Olsson et al. 发现 ICL（in-context learning）的关键电路是"归纳头"
- 一种 2 头注意力电路：A 头复制上一个 token，B 头把复制的内容移到下一个位置
- **跨模型通用**：GPT-2 / Llama / Mistral 都有

### IOI Circuit

- Wang et al. 找到负责"Indirect Object Identification"任务的精确电路
- 揭示了 attention head 间的"层级通信"

### Superposition Hypothesis

- Elhage et al. "Toy Models of Superposition"：模型倾向于把更多特征压缩进更少维度
- 解释了为什么 SAE 有效：把叠加特征再拆开

### Universality（跨模型通用）

- Successor heads、induction heads、duplication heads 在不同模型/尺度上**反复出现**
- 暗示 LLM 训练可能收敛到类似的内部电路

## 工具栈

| 工具 | 用途 |
|------|------|
| **TransformerLens** | Hook 介入 transformer forward，支持任意 patching |
| **CircuitsVis** | 可视化 attention pattern、head 重要性 |
| **Neuronpedia** | 公开 SAE feature 浏览器 |
| **Pyvene** | 干预实验库 |
| **nnsight** | 跨框架 interpretability |
| **Penzai** | JAX-based tree 形模型操作 |

## 入门路径

1. **Neel Nanda 的 blog**（尤其 "A Pragmatic Stance on Mechanistic Interpretability"）
2. **TransformerLens 教程** + Colab 练习
3. **读核心论文**：IOI、SAE、Induction Heads、Grokking
4. **复现小实验**：用 TransformerLens 在 GPT-2 small 上找 induction heads

## 价值判断（provenance: inferred）

- 是**理解 LLM 行为的最深路径**——不是看输入输出，而是看内部。
- 2025 已是 Anthropic / DeepMind / OpenAI 安全团队的核心研究方向。
- 对**应用工程师**价值有限——更多是研究科学家方向。
- 与 [[concepts/llm-training-pipeline]] 互补：训练决定能力，MI 解释能力来源。

## 关联

- [[concepts/llm-training-pipeline]]
- concepts/transformer-architecture
- [[sources/dakingrai-mech-interp-papers]]

## Related

- [[synthesis/Research: 学习AI大模型]] — 综合页:Mechanistic Interp 在 Scientist 轨道的位置
