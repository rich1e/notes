---
title: >-
  LLM Learning Path — 从零到能用的系统化路径
category: concepts
tags: [llm, education, career]
sources:
  - "https://github.com/rasbt/LLMs-from-scratch"
  - "https://github.com/karpathy/nn-zero-to-hero"
  - "http://cs336.stanford.edu/spring2025/"
created: 2026-07-27T07:30:00Z
updated: 2026-07-27T07:30:00Z
summary: >-
  学习 LLM 不是单一直线，而是「工程师 vs 研究员」双轨 + 四阶段（基础/应用/原理/系统）；常见反模式是只学调用不学原理、或反过来。
provenance:
  extracted: 0.70
  inferred: 0.20
  ambiguous: 0.10
base_confidence: 0.75
lifecycle: draft
lifecycle_changed: 2026-07-27
---

# LLM Learning Path — 从零到能用的系统化路径

## 双轨选择：Engineer vs Scientist

任何"LLM 学习路线"都隐含这个分叉：

| 维度 | LLM Engineer（应用） | LLM Scientist（研究） |
|------|---------------------|----------------------|
| **目标** | 用现成模型搭产品 | 改进模型本身/发现新能力 |
| **核心技能** | RAG / Agent / 微调 / 推理优化 | 读论文 / 复现 / 训练小模型 |
| **核心工具** | LangChain、LlamaIndex、vLLM、HuggingFace | PyTorch、Triton、TransformerLens |
| **代表作** | ChatGPT 套壳应用 | Qwen、DeepSeek、Kimi |
| **薪资范围**（2025） | $130K-$300K | $180K-$400K+ |
| **入门资源** | HuggingFace Course + Raschka | Karpathy + CS336 |

**关键洞察**：工程轨道**不等于**只学 API 调用——CS336 风格的内容（推理优化、KV 缓存、Triton kernel）才是高阶工程师与"普通 API 调用者"的分水岭。

## 四阶段路径（综合 Karpathy / Raschka / CS336 / 中文社区）

### 阶段 1：基础（4-8 周）

- **数学**：线性代数（矩阵乘法/特征值）、微积分（链式法则/梯度）、概率（KL 散度/cross-entropy）
- **Python + NumPy + Jupyter**
- **速通**：3Blue1Brown 线性代数系列、李宏毅 ML 课前 5 讲
- **验证标准**：能手写一个 softmax + cross-entropy loss 的反向传播

### 阶段 2：深度学习与 Transformer（8-12 周）

- **核心资源**：
  - Karpathy「Zero to Hero」Lecture 1-6（micrograd → makemore MLP）
  - Karpathy「Let's build GPT」
- **必须掌握**：attention、multi-head attention、positional encoding、layer norm、residual connection
- **验证标准**：能不看教程从零实现一个 nano-GPT

### 阶段 3：LLM 全栈（12-16 周）

- **核心资源**：
  - Raschka「LLMs from Scratch」Ch 2-7（tokenization→pretraining→SFT）
  - Karpathy「Deep Dive into LLMs like ChatGPT」（3.5h 总览）
  - HuggingFace Course（应用方向）
- **必须掌握**：
  - Tokenization（BPE 原理）
  - Pretraining 循环
  - SFT / DPO / LoRA
  - RAG 流程（embedding + retrieval + reranking）
  - Agent 基础（ReAct、tool use）
- **验证标准**：能在单卡上 fine-tune 一个 1B 模型并评测

### 阶段 4：专业深化（持续）

- **应用方向**：vLLM、TensorRT-LLM、量化、Agent 框架（LangGraph、CrewAI）、评测（Braintrust、Inspect）
- **研究方向**：RLVR/GRPO、Mechanistic Interpretability、Scaling Laws、MoE、SSM/Mamba
- **入门资源**：Stanford CS336（系统视角）+ [[sources/dakingrai-mech-interp-papers]]（interpretability）

## 常见反模式

1. **只学 API 调用**：会写 prompt engineering + LangChain 链，但不理解 attention 机制——遇到性能瓶颈或幻觉问题时无能为力。
2. **只啃理论不练手**：读完论文但没写过一行 PyTorch——三个月后忘掉 80%。
3. **跳过数学**：以为"做应用不需要数学"——但在生产环境中 debug（训练 loss 不收敛、attention mask 错误、KV 缓存溢出）时必须懂数学。
4. **追新弃旧**：每个新模型出来就切换方向。Karpathy 建议：先用一份资源**走到 80%** 完成度，再切换。
5. **忽略评测**：fine-tune 完不看 benchmark 直接上线——生产事故的最大单一来源。

## 时间分配参考

按 6 个月（约 800 小时）业余时间投入：

| 阶段 | 周数 | 时长占比 |
|------|------|---------|
| 基础 | 8 周 | 30% |
| 深度学习 + Transformer | 10 周 | 30% |
| LLM 全栈 | 12 周 | 30% |
| 专业深化 | 持续 | 10% |

## 学习资源映射（按阶段）

| 阶段 | 视频 | 书 | 论文/文档 |
|------|------|----|----------|
| 基础 | 3Blue1Brown、李宏毅 ML | 《Python 编程：从入门到实践》 | — |
| 深度学习 + Transformer | Karpathy Zero to Hero 1-6 | 《深度学习入门：基于 Python 的理论与实现》（斋藤康毅） | "Attention is All You Need" |
| LLM 全栈 | Karpathy Deep Dive、HuggingFace Course | Raschka LLMs from Scratch | GPT-2/GPT-3 论文 |
| 专业深化 | Stanford CS336 公开讲义 | "LLM Engineer's Handbook"（2025） | DeepSeek-R1、Mamba |

## 关联

- [[concepts/transformer-architecture]]
- [[concepts/llm-training-pipeline]]
- [[sources/andrej-karpathy-zero-to-hero]]
- [[sources/sebastian-raschka-llms-from-scratch-book]]
- [[sources/stanford-cs336-spring2025]]
- [[sources/li-hongyi-genai-2025]]