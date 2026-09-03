---
title: >-
  RAG vs Fine-tuning vs Prompt Engineering — 何时用什么
category: concepts
tags: [Deepseek, engineering, rag]
sources:
  - "https://github.com/rasbt/LLMs-from-scratch"
created: 2026-07-27T07:30:00Z
updated: 2026-07-27T07:30:00Z
tier: peripheral
summary: >-
  改造 LLM 的三种主流方式：prompt engineering（最便宜）、RAG（注入新知识）、fine-tuning（改风格/技能）；2025 共识是"先用 prompt，不行加 RAG，再不行才 fine-tune"。
provenance:
  extracted: 0.75
  inferred: 0.20
  ambiguous: 0.05
base_confidence: 0.80
lifecycle: reviewed
lifecycle_changed: 2026-09-03
lifecycle_reason: "auto-promoted by wiki-lint --consolidate: age>30d, confidence>0.8"
lifecycle_changed: 2026-07-27
---

# RAG vs Fine-tuning vs Prompt Engineering — 何时用什么

## 决策总表（2025 共识）

| 维度 | Prompt Engineering | RAG | Fine-tuning |
|------|------------------|-----|-------------|
| **成本** | 几乎免费 | 中（向量库 + 检索） | 高（GPU + 数据 + 时间） |
| **速度** | 即时 | 几十-几百 ms（检索延迟） | 训练数小时-数天 |
| **改的是什么** | 怎么问问题 | 模型能查到什么 | 模型本身的行为 |
| **改的"知识"vs"行为"** | 临时任务说明 | 外部知识库（可热更新） | 行为/格式/风格 |
| **典型场景** | 通用任务、quick win | 私域知识、fact grounding | 特定语气/输出格式、新技能 |
| **风险** | 模型知识有截止 | 检索质量决定上限 | 灾难性遗忘、幻觉 |

## 关键区分（provenance: extracted）

### "知识" vs "行为"

这是 **2025 年最重要的概念区分**：

- **Fine-tuning 改的是"行为"**——模型怎么处理输入、输出什么格式、有什么语气。**它不擅长注入新事实**。
- **RAG 改的是"知识"**——模型回答问题时能查到的事实。**它不擅长教模型新的思维方式**。
- 想要模型"知道 2026 年 7 月的新闻"？用 RAG。  
  想要模型"用医疗报告的格式写回执"？用 fine-tuning。

## 何时使用（决策树）

```
需要私有/最新知识吗？
  ├─ 是 → 优先 RAG（+ 必要时 fine-tune 改输出格式）
  └─ 否 → 见下面

需要严格的输出格式/语气吗？
  ├─ 是 → 优先 Fine-tuning（LoRA/QLoRA 经济可行）
  └─ 否 → Prompt Engineering 即可

两者都需要？
  └─ RAG + Fine-tuning 组合（先 RAG 喂事实，再 FT 校风格）
```

## 何时**不要**用 Fine-tuning（2025 共识）

| 场景 | 为什么不该 fine-tune | 该用什么 |
|------|---------------------|---------|
| 注入新事实/知识 | FT 教行为不教事实；模型会幻觉 | RAG |
| 项目早期 / 频繁迭代 | FT 一次要数小时；prompt 改一行即生效 | Prompt |
| 没有几百条高质量样本 | FT 容易过拟合/遗忘 | Prompt 或 few-shot |
| 想"消除幻觉" | FT 不会解决底层幻觉问题 | RAG + 更好的 prompt + 输出校验 |
| 团队没人懂训练 | 训练失败难 debug | 用托管 API |

## 何时**不要**用 RAG

| 场景 | 为什么 RAG 不适合 | 替代 |
|------|-----------------|------|
| 任务不需要外部知识 | 检索增加延迟无收益 | Prompt |
| 知识库非常小且稳定 | 检索 overhead 不值得 | 把内容塞进 prompt（context window 够大时） |
| 需要精确控制输出 | 检索结果不确定 | Fine-tuning |

## 2025 趋势

- **Fine-tuning 成本下降**：开源权重（Qwen3、Llama 3.3）+ 便宜 GPU + QLoRA 让消费级 4090（24GB）也能 FT 7B 模型——使中小公司的"专属模型"成为常态。
- **RAG 仍是默认**：知识密集型应用（客服、文档问答、研究）的首选；LangChain + LlamaIndex 是事实标准框架。
- **Prompt engineering 复杂化**：从简单的 few-shot 演进到 structured output、tool use、agentic patterns（ReAct、Reflexion）。

## 组合实践（生产级）

典型生产系统 = Prompt + RAG + FT 的**组合**：

1. **Prompt**：定义角色、输出格式、约束
2. **RAG**：检索相关文档塞进 context
3. **Fine-tuning**：让模型学某种风格/格式（如"先引用再回答"）

## 关联

- [[concepts/llm-training-pipeline]]
- [[concepts/llm-learning-path]]
- concepts/instruction-tuning
- sebastian-raschka-llms-from-scratch-book

## Related

- [[synthesis/Research: 学习AI大模型]] — 综合页:Prompt/RAG/FT 决策矩阵的完整版
