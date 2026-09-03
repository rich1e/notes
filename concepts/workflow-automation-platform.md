---
title: "工作流自动化平台"
category: concepts
tags: [workflow-automation, workflow, n8n, zapier, make]
sources:
  - "https://n8n.io/"
  - "https://github.com/n8n-io/n8n"
  - "https://www.c-sharpcorner.com/article/zapier-vs-make-vs-n8n-the-ultimate-comparison-for-workflow-automation-in-2025/#comments"
created: "2026-07-30"
updated: "2026-07-30"
summary: "用可视化拖拽 + 预制集成节点把跨应用任务流编排为 DAG 的低代码平台，主流代表：Zapier（云 SaaS 老大）、Make（视觉最强）、n8n（开源+自托管+代码注入）。"
provenance:
  extracted: 0.75
  inferred: 0.20
  ambiguous: 0.05
base_confidence: 0.75
lifecycle: draft
lifecycle_changed: "2026-07-30"
tier: supporting
---

# 工作流自动化平台

## 概念

**工作流自动化平台** = 把跨 SaaS / DB / API 的任务流用「节点 + 连线」的可视化方式编排为 DAG 的低代码工具。开发者/非开发者都能用，核心价值是**省下重复性集成代码**。

## 核心抽象

| 概念 | 含义 |
|---|---|
| **Trigger 节点** | 工作流起点（webhook / 定时 / 事件 / 手动） |
| **Action / Function 节点** | 执行步骤（HTTP / DB / 转换 / AI） |
| **Connections** | 数据流路径（节点之间的「电线」） |
| **Workflow** | 整个 DAG = 一次完整自动化 |
| **Credentials** | 各服务 API key / OAuth 集中管理（n8n 有专门 UI） |

## 三主流对比（2025 年底口径）

| 维度 | Zapier | Make | n8n |
|---|---|---|---|
| 类型 | 纯云 SaaS | 纯云 SaaS | 开源 + 自托管 + 云 |
| 集成数 | 7000+ ^[extracted] | 中等 | 1500+ ^[inferred, GitHub README] |
| 上手难度 | 最易（线性 trigger→action） | 中等（视觉 scenario） | 中等偏高（节点多 + 代码节点） |
| 灵活度 | 受限（不支持复杂循环/分支） | 中等 | 高（JS/Python 任意节点注入 + 自定义节点） |
| 性能 | 70% 用户 20 步以内够用 | 500+ 并发/秒开始延迟 +23% ^[inferred] | 200+ 并发 ~800ms ^[inferred] |
| 价格 | Free → $19.99/mo → Enterprise ~$5999/年 | 中端 | Cloud $20/mo / 自托管免费 |
| 数据主权 | 无（云端） | 无（云端） | 有（自托管） |

## 决策框架 ^[inferred]

- **非技术用户 / 简单场景**：Zapier
- **视觉学习者 / 中等复杂度**：Make
- **开发者 / 数据敏感 / 成本敏感 / 复杂逻辑**：n8n
- **AI agent 工作流**：n8n（LangChain + MCP + multi-agent 编排）> Make > Zapier

## 设计取舍

- **可视化 vs 代码**：n8n 的核心差异化是「同一画布支持 JS/Python 节点」——其他工具非此即彼
- **托管 vs 自托管**：自托管需要 Queue Mode（Redis + Postgres + main/webhook/worker 三角色），运维成本 ≠ 0
- **线性 vs DAG**：Zapier 强制线性，n8n/Make 支持任意 DAG（含循环、分支、并行）

## 相关

- [[entities/n8n]] · [[entities/zapier]] · [[entities/make]]
- n8n-github-repo · n8n-queue-mode
- [[synthesis/Research: n8n]]