---
title: 提示缓存（Prompt Caching）
category: concepts
tags:
  - llm
  - prompt-caching
  - token-optimization
  - claude-code
summary: LLM 提示缓存机制：将已计算的 KV 缓存存储复用，读取成本约为重新计算的 1/10，需要前缀完全匹配才能命中。
sources:
  - https://baoyu.io/blog/2026-04-06/claude-code-token-optimization
created: 2026-06-29
updated: 2026-06-29
tier: core
lifecycle: draft
lifecycle_changed: "2026-06-29"
base_confidence: 0.67
provenance:
  extracted: 0.80
  inferred: 0.15
  ambiguous: 0.05
relationships:
  - target: "[[skills/claude-code-token-optimization]]"
    type: related_to
---

# 提示缓存（Prompt Caching）

## 原理

大语言模型处理输入时，需要将完整输入序列"从头读一遍"——每次请求都重新计算 KV 缓存（Key-Value Cache），计算量与输入长度成正比。

**提示缓存**将首次计算的 KV 缓存存储起来，后续请求若输入前缀完全匹配，则直接读取缓存，跳过重新计算。

**读取缓存的成本约为重新计算的 1/10。**

## 命中条件

1. **前缀完全匹配**：从第一个 token 开始，一字不差地匹配到某个检查点。中间哪怕改动一个字符，该位置之后的缓存全部失效。
2. **缓存仍在存活窗口内**：Claude Code 中，主智能体缓存存活 1 小时，子智能体 5 分钟，API 用户默认 5 分钟（可付费开启 1 小时）。每次命中会刷新计时器。

## 在 Claude Code 中的意义

Claude Code 输入结构（从前到后）：
1. 系统指令 + 工具定义（~5 万 token，不变）
2. CLAUDE.md 项目配置（不变）
3. 对话历史（每轮追加）
4. 新消息（当前输入）

同一活跃会话中，每轮只在尾部追加新内容，前面的大段内容天然命中缓存。

若开新会话，前缀从零开始，之前积累的缓存全部失效——等于为那 ~5 万 token 的基础设施付了全价。

## 缓存失效的高代价场景

| 场景 | 代价 |
|------|------|
| 闲置超过缓存存活时间后继续 | 全量重建，与上下文大小成正比 |
| 会话中间换模型 | 缓存按模型隔离，切换即失效 |
| 频繁 `/clear` 重开会话 | 每次都为固定基础设施付全价 |
| 1M 上下文缓存过期 | 代价是 200K 场景的 5 倍+ |

## 相关页面

- [[skills/claude-code-token-optimization]] — 基于缓存原理的实操策略
