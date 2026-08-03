---
title: >-
  Awesome Mechanistic Interpretability LM Papers (Dakingrai)
category: references
tags: [llm, interpretability, research]
sources:
  - "https://github.com/Dakingrai/awesome-mechanistic-interpretability-lm-papers"
source_url: "https://github.com/Dakingrai/awesome-mechanistic-interpretability-lm-papers"
created: 2026-07-27T07:30:00Z
updated: 2026-07-27T07:30:00Z
tier: peripheral
summary: >-
  Dakingrai 维护的机制可解释性论文清单，按 taxonomy 分组（Techniques/Evaluation/Findings/Tools），配套 Rai et al. 2024 综述（arXiv:2407.02646）。
provenance:
  extracted: 0.85
  inferred: 0.10
  ambiguous: 0.05
base_confidence: 0.85
lifecycle: draft
lifecycle_changed: 2026-07-27
---

# Awesome Mechanistic Interpretability LM Papers (Dakingrai)

## URL

https://github.com/Dakingrai/awesome-mechanistic-interpretability-lm-papers

## 内容概述

配套综述 *"A Practical Review of Mechanistic Interpretability for Transformer-Based Language Models"*（Rai et al., 2024, arXiv:2407.02646）的论文清单。按 taxonomy（Figure 1）组织，含 beginner's roadmap（Figure 2）。

## 四大主题分组（provenance: extracted）

### 1. Techniques — 解释方法

- Logit lens、probing
- **SAE（稀疏自编码器）**
- **Activation/path patching**（因果定位）
- ACDC（自动电路发现）
- Attribution patching（梯度近似版）

### 2. Evaluation — 评估解释质量

- Faithfulness（解释是否真实反映模型行为）
- Completeness（是否覆盖所有相关组件）
- Minimality（是否最小）
- Plausibility（人能否理解）
- Automated explanation scores

### 3. Findings and Applications — 实证发现

**Features**：
- Neurons、superposition（叠加假设）、monosemanticity（单义性）

**Circuits**：
- 解释 LM 行为
- 解释 Transformer 组件

**Universality**（跨模型通用）：
- Successor heads、induction heads、duplication heads 跨尺度反复出现

**Capabilities**：
- ICL（in-context learning）、arithmetic、CoT

**Learning Dynamics**：
- Grokking、phase changes

**Applications**：
- Knowledge editing（ROME）
- Safety steering
- Adversarial examples

### 4. Tools — 库

- **TransformerLens** — 主流 hook 库
- **CircuitsVis** — attention/head 可视化
- **Neuronpedia** — 公开 SAE feature 浏览器
- **Pyvene** — 干预实验
- **nnsight** — 跨框架
- **Penzai** — JAX tree 形操作

## 必读基础论文（provenance: extracted）

| 论文 | 贡献 |
|------|------|
| Elhage et al. "Softmax Linear Units" | 引入 SoLU、发现 "Base64 neurons" |
| Elhage et al. "Mathematical Framework for Transformer Circuits" | 基础框架：attention heads + residual stream = 单向通信 |
| Olsson et al. "In-context Learning and Induction Heads" | 发现 induction heads 是 ICL 核心 |
| Wang et al. "IOI Circuit"（ICLR'23）| mean-ablation + path patching + IOI circuit |
| Cunningham et al. "SAE Find Highly Interpretable Features"（ICLR'24）| SAE 现代方法 |
| Bricken et al. "Towards Monosemanticity" | SAE 训练方法 |
| Elhage et al. "Toy Models of Superposition" | superposition 假说 |
| Meng et al. "Locating and Editing Factual Associations in GPT"（NeurIPS'22）| ROME 知识编辑 |
| Conmy et al. "ACDC"（NeurIPS'23）| 自动电路发现 |
| Goldowsky-Dill et al. "Causal Scrubbing" | 严格假设检验 |
| Nanda et al. "Progress Measures for Grokking"（ICLR'23）| grokking 现象 |

## 跨切主题

- **Universality**：同一类电路在不同模型反复出现——暗示训练收敛性
- **Circuit reuse**：同一组件服务多任务（induction heads 既在 IOI 也在 ICL）
- **SAE 是 2023+ 的范式**：从 polysemanticity 走向 monosemanticity

## 关联

- [[concepts/mechanistic-interpretability]]
- [[concepts/transformer-architecture]]