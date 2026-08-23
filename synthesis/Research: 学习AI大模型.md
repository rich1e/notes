---
title: >-
  Research: 学习 AI 大模型 — 系统化路径与资源地图
category: synthesis
tags: [llm, education, research, career]
sources:
  - "https://github.com/karpathy/nn-zero-to-hero"
  - "https://github.com/rasbt/LLMs-from-scratch"
  - "http://cs336.stanford.edu/spring2025/"
  - "https://speech.ee.ntu.edu.tw/~hylee/genai/2025-spring.php"
  - "https://github.com/Dakingrai/awesome-mechanistic-interpretability-lm-papers"
created: 2026-07-27T07:30:00Z
updated: 2026-07-27T07:30:00Z
summary: >-
  3 轮研究综合：LLM 学习不是单一直线而是「工程师 vs 研究员」双轨 + 四阶段路径；三套顶级资源（Karpathy 视频 / Raschka 书 / CS336 课程）形成完整坐标系；2025 关键转向是 Test-Time Compute 与 RLVR。
provenance:
  extracted: 0.75
  inferred: 0.18
  ambiguous: 0.07
base_confidence: 0.82
lifecycle: draft
lifecycle_changed: 2026-07-27
---

# Research: 学习 AI 大模型 — 系统化路径与资源地图

## Overview

学习 AI 大模型在 2025 年已是一个**清晰可解**的问题。核心结论有三条：(1) 学习路径不是直线而是**双轨**——工程师（用模型搭产品）vs 研究员（改进模型本身），资源与目标完全不同；(2) 三套顶级资源（Karpathy 视频、Raschka 书/CS336 课程）形成完整的**坐标系**——任一认真走完都能达到"中级 LLM 从业者"水平；(3) 2024 末–2025 的**关键范式转向**是 Test-Time Compute（推理时多想一会儿）+ RLVR（用可验证奖励而非人类反馈），代表作为 DeepSeek-R1 与 OpenAI o1/o3，理解这个转向是判断"前沿"的分水岭。

## Key Findings

### F1. 三阶段训练流程是所有现代 LLM 的标准（共识）

**Pretraining → SFT → RLHF/RLVR** 是从 GPT 到 Claude 到 Qwen 到 DeepSeek 的**通用 pipeline**。理解这三阶段（特别是它们各自消耗多少算力、解决什么问题）是入门的最深锚点——见 [[concepts/llm-training-pipeline]]。Karpathy 2025 的"教科书"类比（读课本→做例题→做练习）已成为这一框架的标准解释方式。

### F2. 三套顶级资源形成完整坐标系（共识）

- **Karpathy "Zero to Hero"** ——视频/手写直觉，8 讲从 micrograd 到 GPT；先修最轻
- **Raschka "LLMs from Scratch"** ——书+GitHub 仓库，工程化 PyTorch 实现，普通笔记本可跑；覆盖面最广
- **Stanford CS336 Spring 2025** ——Hashimoto & Liang 主讲，研究级实现密集课，含 5 次作业（Basics/Systems/Scaling/Data/Alignment）；门槛最高

三者**互不替代**：Karpathy 给直觉、Raschka 给工程、CS336 给系统视角。中文学习者可以加 **李宏毅 2025《生成式AI导论》** 作为概念地图（覆盖多模态、Agent、Test-Time Compute、AI 安全）。

### F3. Engineer vs Scientist 是首要分叉（共识）

不同来源反复强调的**第一个选择**：
- **LLM Engineer**（应用方向）：LangChain、LlamaIndex、vLLM、HuggingFace——构建产品
- **LLM Scientist**（研究方向）：PyTorch、Triton、TransformerLens——改进模型

2025 薪资范围：Engineer $130K-$300K，Scientist $180K-$400K+。**常见错误**是只学 API 调用或只啃理论——CS336 风格的"系统视角"（推理优化、KV 缓存、Triton kernel）是高阶工程师与"普通 API 调用者"的分水岭。

### F4. Prompt → RAG → Fine-tuning 的决策顺序（共识）

2025 年改造 LLM 的**默认顺序**：先用 Prompt Engineering（免费）；不行加 RAG（注入新事实）；最后才 Fine-tuning（改风格/格式/技能）。**关键概念区分**：Fine-tuning 改的是**行为**，RAG 改的是**知识**——想要模型"知道新事实"用 RAG，想要"用某种风格回答"用 FT。生产系统通常三者组合。

### F5. Test-Time Compute 是 2024 末–2025 关键转向（共识）

代表：OpenAI o1/o3、DeepSeek-R1。核心思想：**让模型在推理时"多想一会儿"**（长 CoT + verifier 引导搜索），而不是单纯靠训练时把模型做大。配套训练范式 **RLVR**（Reinforcement Learning from Verifiable Rewards）用可客观验证的奖励（数学题答案、单元测试通过率）取代 RLHF 的人类反馈——更便宜、更稳定、更开源友好。这是 2025 年所有前沿 LLM 都在卷的方向——见 [[concepts/test-time-compute]]。

### F6. 四阶段路径 + 时间预算（综合推荐）

按 6 个月业余时间（约 800 小时）：
- **阶段 1（基础 4-8 周）**：数学（线代/微积分/概率）+ Python + NumPy
- **阶段 2（深度学习 + Transformer 8-12 周）**：Karpathy Zero to Hero Lecture 1-6
- **阶段 3（LLM 全栈 12-16 周）**：Raschka Ch 2-7 + Karpathy Deep Dive + HuggingFace Course
- **阶段 4（专业深化 持续）**：CS336（系统视角）+ Mech Interp（理解方向）

### F7. Mechanistic Interpretability 是"打开黑箱"路径（小众但深刻）

研究神经网络内部的电路：用 SAE（稀疏自编码器）找单义特征、用 path patching 因果定位、用 induction heads 解释 ICL……代表工具：TransformerLens、CircuitsVis、Neuronpedia。是**研究科学家方向**而非应用工程师——但理解"为什么 LLM 能 ICL"等问题时绕不开——见 [[concepts/mechanistic-interpretability]]。

## Core Concepts

- [[concepts/llm-training-pipeline]] — 预训练 → SFT → RLHF/RLVR 三阶段（最重要的概念框架）
- [[concepts/llm-learning-path]] — 双轨选择 + 四阶段路径 + 时间预算 + 资源映射
- [[concepts/rag-vs-finetuning]] — Prompt vs RAG vs Fine-tuning 的决策矩阵
- [[concepts/test-time-compute]] — 2025 范式转向：推理时扩展 + RLVR
- [[concepts/mechanistic-interpretability]] — SAE、induction heads、circuit discovery
- concepts/transformer-architecture — 通用 Transformer 概念（已存在于 vault）
- [[concepts/mixture-of-experts]] — MoE 架构（已存在）
- concepts/scaling-laws — Chinchilla 等 scaling law（应作为补充概念引用）

## Entities & Tools

- [[entities/andrej-karpathy]] — Karpathy，Zero to Hero 系列作者
- [[entities/sebastian-raschka]] — Raschka，LLMs from Scratch 书/仓库作者
- [[entities/li-hongyi]] — 李宏毅，中文 ML/GenAI 课程主讲
- 工具（应单独建实体页但本轮未建，下次补）：
  - HuggingFace Transformers / Datasets
  - vLLM（推理服务）
  - TensorRT-LLM（NVIDIA 推理优化）
  - LangChain / LlamaIndex（RAG/Agent 框架）
  - TransformerLens（可解释性）

## Contradictions & Open Questions

### C1. "先学数学还是先动手"的两派分歧

- **派 A（先数学）**：CS336、传统 ML 教育路径——没有数学理解后期寸步难行
- **派 B（先动手）**：Karpathy 系列、Medium "How I Would Learn LLMs in 2026"——先跑通再补数学

**判断**：取决于目标。如果目标是**做应用**，派 B 更高效（2 周内就能跑通 RAG demo）。如果目标是**改模型/做研究**，派 A 不可省。**反模式**：两者都不做（既不学数学也不动手）。

### C2. "用 API 还是本地跑开源"的经济边界

- **API 派**（OpenAI/Anthropic API）：零启动成本，按调用付费，无运维
- **本地派**（开源 Llama/Qwen/DeepSeek）：数据隐私、可微调、单次推理便宜

**2025 边界**：消费级 4090（24GB）能 FT 7B 模型 + QLoRA → 中小公司开始拥有"专属模型"。但**新模型首发往往只在 API 上**（如 o1）——存在 3-12 个月的"开源滞后"。

### C3. "CoT 是否真在'推理'"的学术争议

- **正方**：CoT + verifier 引导搜索在数学/代码上明显更强（OpenAI o1、DeepSeek-R1 实证）
- **反方**（Anthropic interpretability 团队等）：模型经常"伪装思考"，实际靠 pattern matching；真正的 reasoning 需要新架构

**目前无法定论**——这是 2025–2026 最活跃的研究辩论之一。

### C4. 某些网络来源的可信度问题

本次研究中部分 WebSearch 返回了**虚构 URL / 错误年代 / 一致性差**的内容（例如声称 2026 年的 roadmap.sh/llm-2026）。判断准则：与多个独立来源交叉验证；优先 GitHub 仓库、Manning/Stanford 等可验证一手来源；对模糊二手汇编降低权重。

## Sources Consulted

### 一手来源（高置信度）

- andrej-karpathy-zero-to-hero — Karpathy GitHub Zero to Hero 仓库
- sebastian-raschka-llms-from-scratch-book — Raschka LLMs from Scratch GitHub + Manning
- stanford-cs336-spring2025 — Stanford CS336 官方课程页面
- dakingrai-mech-interp-papers — Mechanistic Interpretability 论文清单

### 中文与教学来源（中等置信度）

- li-hongyi-genai-2025 — 李宏毅 2025《生成式AI导论》课程大纲

### 二手汇编（低置信度，仅作背景）

- 知乎、CSDN、搜狐等中文社区的"大模型学习路线"文章——反复出现的**共识信息**已纳入正文；**独有信息**因无法一手验证未单独引用

## 学习路线总图

```
[零基础] → Python + 数学基础（4-8 周）
          ↓
        深度学习 + Transformer（8-12 周）
          ↓ Karpathy Zero to Hero 1-6
        LLM 全栈（12-16 周）
          ↓ Raschka LLMs from Scratch + HuggingFace
        [分叉] ─── Engineer 路径 ─── Scientist 路径
        应用：CS336 系统部分    研究：CS336 全部 + Mech Interp
        + vLLM/TensorRT-LLM   + TransformerLens
        + LangChain/LlamaIndex + arXiv 每日读
```

## 关联

- [[synthesis/Research: chezmoi]] — 同一研究模式的早期示例
- [[synthesis/Research: Kimi K3]] — 同一研究模式的另一个示例
- [[concepts/llm-training-pipeline]]
- [[concepts/llm-learning-path]]