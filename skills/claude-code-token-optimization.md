---
title: Claude Code Token 优化策略
category: skills
tags:
  - claude-code
  - token-optimization
  - prompt-caching
  - llm
summary: 理解 Claude Code 提示缓存机制，通过合理管理会话生命周期和上下文质量来降低 token 消耗。
sources:
  - https://baoyu.io/blog/2026-04-06/claude-code-token-optimization
created: 2026-06-29
updated: 2026-06-29
tier: core
lifecycle: draft
lifecycle_changed: "2026-06-29"
base_confidence: 0.67
provenance:
  extracted: 0.85
  inferred: 0.10
  ambiguous: 0.05
relationships:
  - target: "[[skills/claude-code-settings]]"
    type: related_to
  - target: "[[concepts/prompt-caching]]"
    type: uses
---

# Claude Code Token 优化策略

## 核心原理：提示缓存

Claude Code 每次请求需要"从头读"完整输入，包含三层：
1. **固定部分**：系统指令、工具定义、CLAUDE.md 项目规则（~5 万 token）
2. **对话历史**：所有历史轮次
3. **新消息**：当前输入

**提示缓存**将已计算的中间结果存储起来，读取缓存成本只有重新计算的 **1/10**。

缓存有效的前提：
- **前缀完全匹配**：从头开始一字不差匹配
- **缓存存活时间**：主智能体 1 小时，子智能体 5 分钟，API 用户默认 5 分钟
- 每次命中都会刷新计时器

> "Claude Code 是缓存利用率最高的框架。" — Claude Code 团队

## 会话管理决策

### 继续当前会话的条件
- 任务没变（同一 bug / 同一模块 / 同一组文件）
- 距上次消息不超过 1 小时（缓存仍热）
- 上下文内容对当前工作仍有用

### 开新会话的条件
- 任务切换（如：认证模块 → 支付功能）
- 闲置超过 1 小时（缓存大概率过期）
- 上下文被无关内容塞满（大量噪音）

**原则：能继续就继续，开新会话是特定条件触发的操作。**

## 三个反直觉策略

### 1. 缓存热时继续聊比重开便宜
频繁 `/clear` = 反复为固定基础设施（~5 万 token）付全价写入费。活跃会话中这些内容一直命中缓存，只付 1/10 价格。

### 2. 复杂任务一次做对更省
开着扩展思考一次搞定 vs 关掉后来回改三轮——后者因为每轮都重发完整上下文，往往更贵。

### 3. 长内容给路径别粘贴
把 10000 行日志文件路径发给 Claude，让它用 grep 自己提取。**最便宜的 token 永远是没进上下文的 token。**

## 1M 上下文窗口：慎用

从 2026 年 3 月起 Max/Team/Enterprise 默认 1M 上下文。但主要风险是**缓存失效代价极高**：
- 离开电脑超过 1 小时回来继续 → 1M token 全量重建
- 大多数日常会话在 80-120K 就触发压缩，根本用不到 1M
- 200K 以上模型表现明显下降，350K 以上基本靠运气

**建议配置**：

```json
{
  "env": {
    "CLAUDE_CODE_AUTO_COMPACT_WINDOW": "200000"
  }
}
```

禁用 1M 上下文：
```json
{
  "env": {
    "CLAUDE_CODE_DISABLE_1M_CONTEXT": "1"
  }
}
```

## 六条操作规则

| 规则 | 说明 |
|------|------|
| 用 Sonnet 做日常工作 | Opus 消耗 token 约是 Sonnet 的 2 倍，大多数编码任务 Sonnet 够用 |
| 别在会话中间换模型 | 缓存按模型隔离，换模型会触发全量重建 |
| 精简 CLAUDE.md | 官方建议控制在 200 行内，长说明移到技能里按需加载 |
| 命令行优先于 MCP | `gh` CLI 比 GitHub MCP 消耗少得多；MCP 工具定义本身占 token |
| 先计划再执行 | 计划模式让 Claude 先探索方案，总成本往往比方向错了重来更低 |
| 用 permissions.deny 限制读取范围 | 排除 `node_modules`、构建产物、大型数据文件，防止无意义扫描 |

```json
{
  "permissions": {
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)",
      "Read(./node_modules/**)",
      "Read(./build)"
    ]
  }
}
```

## 委派策略

- **子智能体**：隔离上下文，详细输出不留在主会话（但缓存窗口只有 5 分钟）
- **智能体团队**：并发加速有成本，约是标准会话的 7 倍 token 消耗

## 相关页面

- [[skills/claude-code-settings]] — 配置文件详细说明
- [[concepts/prompt-caching]] — 提示缓存原理
