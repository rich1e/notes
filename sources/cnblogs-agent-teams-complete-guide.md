---
title: "Claude Code Agent Teams 完整上手攻略（中文）"
category: sources
tags:
  - claude-code
  - ai-agents
  - chinese
  - tutorial
  - source
sources:
  - "https://www.cnblogs.com/dhcn/p/19694044"
source_url: "https://www.cnblogs.com/dhcn/p/19694044"
created: "2026-08-05T04:30:00Z"
updated: "2026-08-05T04:30:00Z"
summary: "博客园 _朝晖 的 Claude Code Agent Teams 中文完整教程：环境变量启用、4 类典型用法、3 层 teammates 模型（lead/同事/观察员）、生命周期 + 局限性 + 与单 session 的 token 成本对比。"
provenance:
  extracted: 0.78
  inferred: 0.16
  ambiguous: 0.06
base_confidence: 0.55
lifecycle: draft
lifecycle_changed: "2026-08-05"
tier: supporting
---

# Claude Code Agent Teams 完整上手攻略（中文）

> [[synthesis/Research: Claude Code Agent Teams]] 的**中文二手来源**之一。博客园 _朝晖 发布的中文完整上手攻略，提供与官方文档不同的"3 层 teammates 模型"框架（lead / 同事 / 观察员）。

## 文章基本信息

- **URL**: https://www.cnblogs.com/dhcn/p/19694044
- **作者**: _朝晖（博客园）
- **类型**: tutorial / blog
- **质量评级**: `blog`（personal blog）→ base_confidence 0.55

## 关键主张

### 启用方式（与官方一致）

```json
// ~/.claude/settings.json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

### 3 层 teammates 模型（独有抽象）

文章提出 lead / 同事 / 观察员 三层：

| 角色 | 权限 | 任务 |
|---|---|---|
| **Lead** | 最高 | 创建团队、拆任务、调度、协调、汇总 |
| **同事（teammates）** | 受限 | 各自执行任务、互相通信、向 lead 汇报 |
| **观察员（可选）** | 只读 | 旁观任务进度、无法操作 |

> **未在官方文档出现**——可能是作者个人框架。vault 暂不采纳为主框架（官方 4 组件架构更权威）。

### 4 类典型场景（与官方一致）

1. **多角度并行研究**——多 teammate 各查一个方面
2. **独立模块开发**——teammate 各分一个模块不冲突
3. **对抗式 debug**——5 个 teammate 互驳找真因
4. **跨层协作**——前端 / 后端 / 测试 各归一个

### 与单 session 的对比（token 维度）

文章给出一个粗略的 token 量级估计（具体数字未给）：

| 模式 | Token 量级 | 适用 |
|---|---|---|
| 单 session | 1x | 日常任务 |
| Subagents | 1.x（summarized back） | 独立子任务 |
| Agent Teams | N teammates × 各自 context | 复杂任务 |

## 与官方文档的差异

| 项 | 本文章 | 官方文档 |
|---|---|---|
| 启用 env var | `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` | `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` ✓ 一致 |
| teammates 角色模型 | 3 层（lead/同事/观察员） | 4 组件（lead/teammates/task list/mailbox） |
| 启用步骤 | 需先 `TeamCreate` 工具建队命名 | **v2.1.178 后自动建队**，TeamCreate 工具不存在 |
| Mailbox 协议 | 提到"消息系统"未细化 | 详细 JSON 文件路径 + 校验规则 |
| Token 数字 | 模糊估计 | "scales linearly" + 官方推荐 3-5 teammates |

**核心价值**：中文读起来更快 + 提供了不同于官方文档的 3 层抽象（虽不被官方背书）。**核心缺陷**：与官方文档有版本差异，TeamCreate 工具在 v2.1.178 后不存在。

## 适用场景

- **优先看** [[sources/anthropic-claude-code-agent-teams-docs]]（一手）
- 中文教程需求 / 需要不同心智模型时**看本篇**
- 二手编译时请**回到官方文档核字段**

## Related

- [[synthesis/Research: Claude Code Agent Teams]] — 综合分析
- [[sources/anthropic-claude-code-agent-teams-docs]] — 官方一手文档（权威）
- [[misc/web-youtube-com-watch-v-cskoa-ccmq0w]] — 视频教程（与本中文文章同步，都是二手）