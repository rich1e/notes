---
title: LLM 推测解码（Speculative Decoding）
category: concepts
tags: [llm, performance, automation]
sources:
  - "https://www.ifanr.com/1670249"
  - "https://github.com/deepseek-ai/DeepSpec/blob/main/DSpark_paper.pdf"
created: 2026-07-02
updated: 2026-07-02
summary: 推测解码通过轻量级草稿模型生成候选 token、目标模型并行验证来加速 LLM 推理，核心权衡在于草稿质量与验证成本。
base_confidence: 0.67
lifecycle: draft
lifecycle_changed: "2026-07-02"
tier: supporting
provenance:
  extracted: 0.75
  inferred: 0.20
  ambiguous: 0.05
relationships:
  - target: "[[concepts/prompt-caching]]"
    type: related_to
---

# LLM 推测解码（Speculative Decoding）

## 问题背景

主流 LLM 采用**自回归（autoregressive）**方式逐 token 生成：每生成一个 token 都需要一次完整的前向计算。输出越长，延迟越高。在实时聊天、Agent workflow、代码助手等高交互场景中，生成速度直接影响用户体验和 GPU 利用率。

## 核心思路

推测解码（speculative decoding）用一个**轻量级 draft model（草稿模型）**先生成一批候选 token，再由**目标模型（target model）一次性并行验证**。

- 验证通过的 token 全部接受
- 某位置被拒绝后，该位置之后的候选全部作废，target model 生成修正 token
- 由于验证可并行，在不改变输出分布的前提下提升生成速度

关键指标：**accepted length**（每轮平均被接受的候选 token 数），越高代表草稿质量越好。

## 两类草稿方案的权衡

| 方案 | 优点 | 缺点 |
|------|------|------|
| **Autoregressive draft model** | 前后连贯，后缀 token 质量高 | draft 阶段本身也是逐 token，候选越多越慢 |
| **Parallel draft model**（如 DFlash） | 一次生成多个候选，速度快 | 缺乏块内 token 依赖，出现"后缀衰减（suffix decay）" |

**后缀衰减**：并行草稿在第一个 token 表现强，但越往后接受率越低，因为不同续写路径的 token 混入同一候选块（如把 "of course" 和 "no problem" 混成 "of problem"）。

## DSpark：半自回归架构

DeepSeek 与北京大学联合提出的推理加速框架，已上线 DeepSeek-V4-Flash/Pro 生产环境。

### 生成侧：semi-autoregressive 架构

保留 parallel draft model 主干（速度），在输出端加入**轻量级顺序模块（Markov head）**让后续 token 参考已采样的前序 token，减少后缀衰减。

- Markov head：建模相邻 token 转移关系，计算成本低
- 2 层 DSpark > 5 层 DFlash：轻量顺序建模比单纯增加并行层数更有效

### 验证侧：confidence-scheduled verification

为每个候选位置预测**置信度分数**（在前序 token 均被接受的条件下当前位置被接受的概率）。

**hardware-aware prefix scheduler** 根据三个因素动态决定验证多少 token：
1. 当前系统负载
2. 各位置置信度
3. 引擎在不同 batch size 下的吞吐曲线

系统空闲 → 验证更长前缀；系统繁忙 → 缩短低置信度请求的验证长度，减少对 batch capacity 的占用。^[inferred]

### 线上效果

在相同系统总吞吐下，与 MTP-1 基线对比：
- DeepSeek-V4-Flash：单用户生成速度提升 **60–85%**
- DeepSeek-V4-Pro：单用户生成速度提升 **57–78%**

在 120 token/s/user 的严格 SLA 目标下，名义吞吐优势达 661%（MTP-1 已接近承载边界，DSpark 打开了该性能区间）。

## 任务差异

不同任务的 accepted length 差异显著：

| 任务 | Qwen3-4B 上的 DSpark accepted length |
|------|--------------------------------------|
| 数学推理 | 5.57 |
| 代码生成 | 5.12 |
| 开放聊天 | 3.49 |

数学/代码路径更稳定，聊天不确定性高。固定验证长度会浪费资源。^[inferred]

## 关键洞察

- **推测解码不只是模型结构问题，也是系统调度问题**：候选质量、通过率、验证长度、系统负载、吞吐目标互相牵扯
- 单纯多生成候选 token ≠ 服务更快；验证预算的动态分配才是关键
- 开源：DeepSpec（https://github.com/deepseek-ai/DeepSpec）包含 Eagle3、DFlash、DSpark 训练代码和模型权重

## 相关页面

- [[concepts/prompt-caching]] — 另一类降低 LLM 推理成本的技术
- [[skills/claude-code-token-optimization]] — 实践层面的 token 效率优化
