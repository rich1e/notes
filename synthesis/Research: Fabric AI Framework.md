---
title: "Research: Fabric AI Framework"
category: synthesis
tags: [ai-tools, prompt-engineering, llm, open-source, research]
sources:
  - "https://github.com/danielmiessler/Fabric"
  - "https://github.com/danielmiessler/fabric/tree/main/data/patterns"
created: 2026-07-09T08:00:00Z
updated: 2026-07-09T08:00:00Z
summary: >-
  Fabric 框架研究综合：AI 集成问题的解法、Patterns 设计哲学、290+ Pattern 分类、多提供商架构、REST API 服务模式。
provenance:
  extracted: 0.85
  inferred: 0.10
  ambiguous: 0.05
base_confidence: 0.82
lifecycle: draft
lifecycle_changed: 2026-07-09
---

# Research: Fabric AI Framework

## Overview

Fabric 是 Daniel Miessler 于 2023 年底创建的开源 AI 增强框架，2024 年从 Python 迁移到 Go。核心洞察是：AI 的问题不在于能力不足，而在于**集成困难**——将 AI 融入日常生活和工作流的摩擦太大。Fabric 的解法是将 AI 能力标准化为可复用的 Prompt 单元（Patterns），通过 CLI、REST API 或 Shell 别名轻松调用。

## Key Findings

- **核心抽象是 Pattern**：每个 Pattern = 一个独立目录 + `system.md`（主要指令）+ 可选 `user.md`，对应一个真实任务 [[concepts/fabric-patterns]]
- **290+ 内置 Patterns**：覆盖分析、提取、创作、网络安全、代码、内容处理等大类，`extract_wisdom` 是旗舰 Pattern
- **20+ AI 提供商**：OpenAI、Anthropic、Gemini、Ollama、AWS Bedrock、Azure OpenAI 等，统一接口抽象 [[entities/fabric-ai]]
- **提示策略系统**：cot/cod/tot/aot/ltm 等策略可与任何 Pattern 组合，修改推理方式
- **REST API + Ollama 兼容**：可作为统一 AI 网关，Patterns 作为模型名暴露给 Ollama 生态
- **Go 语言重写**：原 Python 版已废弃，Go 版本性能更好，分发更简单（单二进制）

## Core Concepts

- [[concepts/fabric-patterns]] — Pattern 设计理念、分类目录、extract_wisdom 详解、Prompt Strategies
- [[concepts/prompt-caching]] — 相关：LLM 提示缓存机制背景

## Entities & Tools

- [[entities/fabric-ai]] — Fabric 工具实体卡：安装、用法、支持提供商、Obsidian 集成
- [[skills/fabric-usage-patterns]] — 高频使用场景：YouTube 分析、Shell 别名、REST API、Obsidian 保存

## Design Philosophy（设计哲学）

**"AI is a magnifier of human creativity"** — Fabric 不替代人，而是放大人的创造力。

三条核心设计原则：

1. **Markdown-first**：Pattern 用 Markdown 写，对人和 AI 都清晰可读
2. **System Prompt 优先**：指令放 System Prompt（而非 User Prompt），实践证明效果更稳定
3. **单一职责**：一个 Pattern 解一个具体问题，组合 Patterns 解复杂问题

**分解问题**的元方法：把复杂挑战拆成独立子问题，每个子问题用最合适的 Pattern 处理，再组合结果。这是 Unix 哲学在 AI 领域的应用。

## Pattern 架构细节

```
~/.config/fabric/
├── patterns/           # 内置 + 自定义 Pattern
│   └── extract_wisdom/
│       ├── system.md   # System Prompt（主体）
│       └── user.md     # User Prompt（可选）
├── strategies/         # 推理策略 JSON 文件
├── contexts/           # 持久上下文
└── sessions/           # 会话历史
```

自定义 Pattern 优先级高于内置，更新 Fabric 不影响自定义 Pattern。

## Contradictions & Open Questions

- **Pattern 质量差异**：290+ Patterns 由社区贡献，质量参差不齐——核心 Pattern（extract_wisdom、summarize）经过充分打磨，长尾 Pattern 可能效果一般
- **Python→Go 迁移**：大量早期教程基于 Python 版本，方法有差异，注意辨别版本
- **Ollama 兼容模式局限**：兼容端点有限（仅 3 个），不是完整 Ollama 实现，复杂场景可能有差异
- **Extensions 限制**：Extensions 仅在 Pattern 文件内可用，不支持直接 stdin 调用

## Sources Consulted

- [Fabric GitHub README](https://github.com/danielmiessler/Fabric) — 主文档，安装、Philosophy、用法示例
- [Pattern 目录](https://github.com/danielmiessler/fabric/tree/main/data/patterns) — 290+ Pattern 源码
- [pattern_explanations.md](https://github.com/danielmiessler/fabric/blob/main/data/patterns/pattern_explanations.md) — 所有 Pattern 的一行摘要
- [go.mod](https://github.com/danielmiessler/fabric/blob/main/go.mod) — 技术依赖：Gin、anthropic-sdk-go、openai-go、ollama、sqlite3 等
