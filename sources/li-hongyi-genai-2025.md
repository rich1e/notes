---
title: >-
  李宏毅 2025 — 生成式AI导论（NTU Spring 2025）
category: references
tags: [llm, education, course]
sources:
  - "https://speech.ee.ntu.edu.tw/~hylee/genai/2025-spring.php"
source_url: "https://speech.ee.ntu.edu.tw/~hylee/genai/2025-spring.php"
created: 2026-07-27T07:30:00Z
updated: 2026-07-27T07:30:00Z
summary: >-
  台大李宏毅 2025 春《生成式AI导论》13 讲中文课，零 ML 背景友好：ML/DL 基础 → 各模态生成模型 → 指令微调 → Agent → 测试时计算 → AI 安全对齐。
provenance:
  extracted: 0.75
  inferred: 0.15
  ambiguous: 0.10
base_confidence: 0.75
lifecycle: draft
lifecycle_changed: 2026-07-27
---

# 李宏毅 2025 — 生成式AI导论（NTU Spring 2025）

## URL

- 课程主页：https://speech.ee.ntu.edu.tw/~hylee/genai/2025-spring.php
- 平台：NTU COOL

## 课程定位（provenance: extracted）

台湾大学李宏毅教授主讲。**专门为初学者设计，无需机器学习背景**——从 ML 基本概念讲起，循序渐进到生成式 AI 的技术原理与最新发展。

## 13 讲大纲（provenance: extracted）

1. 机器学习基本概念
2. 深度学习简介
3. 各个模态的生成式 AI（文字、影像、声音等）
4. 基础语言模型
5. 基础影像生成模型
6. 指令微调（Instruction Tuning）
7. 各类 AI 代理（Agent）
8. 测试时计算（Test-time Computation）
9. 大语言模型相关议题
10. AI 安全与对齐
11. 影像相关研究主题
12. 语音相关研究主题

## 课程特色（provenance: extracted）

- 难度由浅入深，**适合中文母语零基础入门**
- 配有完整的作业设计
- 覆盖**多模态 AI**（与 Karpathy/Raschka 仅文本 LLM 的视角互补）
- **2025 春季新增**：测试时计算（Test-time Computation）模块——对应 o1/R1 风格的推理模型

## 价值判断（provenance: inferred）

- 是中文学习者**最重要的入门课**之一——李宏毅的口音与节奏对中文母语极友好，B 站上有大量搬运与笔记。
- 与 [[sources/andrej-karpathy-zero-to-hero]] 和 [[sources/sebastian-raschka-llms-from-scratch-book]] 形成**入门 × 入门 × 中文视角**：Karpathy 偏直觉，Raschka 偏工程，李宏毅偏概念地图。
- 把"测试时计算"和"AI 安全对齐"放在同一门课里，**反映了 2025 年的研究重点转移**——这两个主题在 2024 之前的课里通常不会出现或仅一笔带过。

## 局限性

- 主要讲概念，**实现深度不如 Karpathy/Raschka**——读者看完不一定能写出 GPT。
- 课程页面 URL 在抓取时 404；信息来自二手汇编（搜索结果片段）。
- 截至 2025 不深入 RLVR / GRPO 算法细节、不深入分布式训练、不深入推理优化。

## 关联

- [[entities/li-hongyi]]
- [[sources/andrej-karpathy-zero-to-hero]]
- [[sources/sebastian-raschka-llms-from-scratch-book]]
- [[concepts/instruction-tuning]]
- [[concepts/ai-agent]]
- [[concepts/test-time-compute]]