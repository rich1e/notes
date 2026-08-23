---
title: llm-training-pipeline × transformer-architecture
category: synthesis
tags: [llm, deep-learning, ai-coding, synthesis]
sources:
  - "[[concepts/llm-training-pipeline]]"
  - "[[concepts/transformer-architecture]]"
  - "[[concepts/instruction-tuning]]"
  - "[[concepts/scaling-laws]]"
  - "andrej-karpathy-zero-to-hero"
  - "sebastian-raschka-llms-from-scratch-book"
created: 2026-08-04T13:30:00Z
updated: 2026-08-04T13:30:00Z
summary: "架构(Transformer)与训练(三阶段 pipeline)是 LLM 学习的两条正交轴:架构是静态的'模型长什么样'、给容量;训练是动态的'模型怎么变成现在这样'、给能力。能力涌现只发生在训练轴上,这决定了'先学哪条轴'的路径。"
provenance:
  extracted: 0.3
  inferred: 0.65
  ambiguous: 0.05
base_confidence: 0.55
lifecycle: draft
lifecycle_changed: "2026-08-04"
relationships:
  - target: "[[concepts/llm-training-pipeline]]"
    type: related_to
  - target: "[[concepts/transformer-architecture]]"
    type: related_to
---

# llm-training-pipeline × transformer-architecture

## The Connection

[[concepts/transformer-architecture]] 讲**模型长什么样**:自注意力 + 多头 + 位置编码 + 残差前馈的堆叠骨架。[[concepts/llm-training-pipeline]] 讲**模型怎么变成现在这样**:Pretraining → SFT → RLHF/RLVR 三阶段。

单看任一页,容易把二者混成一件事("学 LLM")。叠起来才看清:**它们是两条正交的轴**——架构是**空间/静态**的(权重矩阵的形状与连接方式),训练是**时间/动态**的(这些权重的数值如何被数据一步步塑造)。同一套 Transformer 架构,经过不同训练阶段,能是 base model、也能是 chat model、还能是 reasoning model。

## Where They Co-occur

四个源页同时引用二者:[[concepts/instruction-tuning]](在固定架构上做 SFT)、[[concepts/scaling-laws]](架构容量 × 数据/算力如何联合决定 loss)、[[entities/andrej-karpathy]] 与 sebastian-raschka-llms-from-scratch-book(两份经典教程都是"先搭架构、再讲训练"的顺序)。它们反复把架构和训练摆在一起,却极少点破二者的分工。

## Cross-cutting Insight

**容量来自架构,能力来自训练;能力涌现只发生在训练轴上。**^[inferred]

- 架构决定了模型**能表示什么**——注意力头数、层数、隐藏维度设定了函数空间的上限。这是 [[concepts/scaling-laws]] 里"参数量 N"那一项。
- 训练决定了模型**实际学到什么**——同一个空架构,随机初始化时什么都不会;pretraining 灌入世界知识,SFT 对齐指令格式,RLHF/RLVR 对齐偏好与推理。
- 关键推论:**"指令遵循""对话""推理"这些能力不在架构里,而在训练轴的后段**。GPT 的 base model 和 chat model 架构完全相同,差别全在 SFT+RLHF。所以想改模型的**行为**,动训练;想改模型的**容量**,才动架构。

这直接映射到学习路径的分工([[concepts/llm-learning-path]]):
- Karpathy/Raschka 路线"先架构后训练"是对的——因为**不先理解 Q/K/V 怎么算,就无法理解 pretraining 的 loss 在优化什么**;架构是训练的前置词汇表。
- 但反过来,只懂架构不懂训练,会误以为"模型强 = 架构新"。实际 2025 的前沿分水岭([[concepts/test-time-compute]] / RLVR)几乎全在训练轴上,架构还是那个 Transformer。**架构近年趋于稳定,竞争主战场移到了训练。**

## Tensions and Trade-offs

- **MoE 模糊了边界。** [[concepts/mixture-of-experts]] 这类改动既是架构(稀疏激活的连接方式),又深度依赖训练(路由器的负载均衡靠训练目标塑造)——不是纯粹某一轴,是两轴耦合点。
- **"先学哪条"的取舍。** 应用方向的学习者可以几乎跳过架构细节(调 API、做 RAG),但研究方向的绕不开架构;这与 [[synthesis/Research: 学习AI大模型]] 里"先数学 vs 先动手"的分叉同源。
- **归因陷阱。** 把模型能力全归给架构(如"因为是 Transformer 所以强"),会忽略数据质量与训练配方这些真正的差异来源。

## Strongest Objection

**架构和训练也许并不正交,而是深度纠缠,拆成两条轴是过度简化。** 位置编码、注意力变体(如 FlashAttention、滑窗注意力)、KV-cache 友好的架构设计,都是为了让某种训练/推理更高效而反向塑造的架构选择;Chinchilla scaling law 也表明最优架构规模由训练算力预算决定。若架构选择本身就是训练目标的函数,那"架构给容量、训练给能力"的干净二分就站不住。

> test: 找一个"同数据同训练配方、只改架构"与"同架构、只改训练配方"的对照实验(如同规模 dense vs MoE,或 base vs instruct)。若能力差异主要由后者贡献,则两轴分工成立;若架构改动也大幅改变能力上限而非仅容量,则二分被削弱。

## Open Questions

- 近年"架构趋稳、训练主战场"的判断能撑多久?下一次架构级跃迁(如替代注意力的线性/状态空间模型)会不会把主战场拉回架构轴?
- 对中级学习者,"理解架构到什么深度"才够支撑理解训练?是否存在一个"够用就好"的架构知识边界?

## Related

- [[concepts/transformer-architecture]]
- [[concepts/llm-training-pipeline]]
- [[concepts/scaling-laws]]
- [[concepts/instruction-tuning]]
- [[concepts/test-time-compute]]
- [[concepts/mixture-of-experts]]
- [[concepts/llm-learning-path]]
- [[synthesis/Research: 学习AI大模型]]
