---
title: "Auth-Status Semantics — 浏览器 cookie 认证的 5 状态健康词汇表"
category: concepts
tags:
  - authentication
  - health-checks
  - mcp
  - pattern
summary: 一套 5 状态认证健康词汇表(configured / not_configured / stale / unverified / error),区分"凭证坏了"与"监控本身无法判断",避免给用户误报重新认证提示。
sources:
  - https://github.com/jacob-bd/gemini-notebook-mcp-cli/blob/main/docs/AUTHENTICATION.md
created: 2026-08-06
updated: 2026-08-06
tier: supporting
lifecycle: reviewed
lifecycle_changed: "2026-08-06"
base_confidence: 0.85
provenance:
  extracted: 0.80
  inferred: 0.15
  ambiguous: 0.05
relationships:
  - target: "[[entities/gemini-notebook-mcp-cli]]"
    type: uses
  - target: "[[concepts/cdp-cookie-extraction]]"
    type: related_to
  - target: "[[concepts/multi-profile-google-auth]]"
    type: related_to
---

# Auth-Status Semantics — 浏览器 cookie 认证的 5 状态健康词汇表

> 只报告"认证坏了"或"认证正常"太粗糙了。浏览器 cookie 认证可能以五种不同方式失败——而你应该采取的应对方式取决于具体是哪一种。这套 5 状态词汇表(`configured` / `not_configured` / `stale` / `unverified` / `error`)区分了"凭证确实坏了"与"监控本身判断不出来",这样 AI agent 就不会用虚假的重新认证提示去打扰用户。

## 5 个状态

| 状态 | 含义 | 用户应采取的行动 |
|-------|---------|-------------|
| `configured` | 实时检查通过。凭证有效。 | 无需操作。 |
| `not_configured` | 本地根本没有存储任何凭证(首次运行)。 | 运行 `nlm login`。 |
| `stale` | 凭证已确认失效:被重定向到 `accounts.google.com`、磁盘上的 profile 加载失败,或上次成功验证已超过 7 天。 | 运行 `nlm login` 刷新。后续 API 调用会失败。 |
| `unverified` | 实时检查未能完成(网络超时、DNS 失败、代理拦截、非 200 的 HTTP 响应)。磁盘上缓存的凭证仍完好,可能仍然有效。 | **稍后重试。** 不要假设用户需要重新认证。 |
| `error` | 检查本身内部发生了意外异常。 | 附带 traceback 提交 bug。 |

## 为什么这个区分很重要

最朴素的检查方式是"我现在能不能发起一次 API 调用?"。能→"正常"。不能→"坏了,请重新认证!"

但"不能"背后有好几种原因:

1. **cookie 确实过期了** → 必须重新认证
2. **你的网络断了** → 再怎么重新认证也没用,稍后重试即可
3. **Google 的风控引擎拦截了你的 IP** → 完全不是用户的问题
4. **健康检查本身崩溃了** → 是 bug,不是认证问题

一个二元的"坏了/正常"会丢掉这些信息。用户会因为网络问题被要求重新认证。更糟的是,处于循环中的 AI agent 会每隔几轮就提示一次重新认证,白白消耗上下文还惹恼用户。

## 探测结构

`AuthHealthChecker` 是**多探测器**式的——它不会只信任单一信号:

1. **首页抓取探测** — GET `https://notebook.google.com/`,检查响应中是否包含会话有效的标记(而不是被重定向到 `accounts.google.com`)
2. **API 回退探测** — 尝试一次轻量的认证 RPC(例如笔记本列表),检查是否返回 401/403
3. **磁盘校验** — 验证 `auth.json` 是否存在、可读,并包含预期字段(cookies、CSRF、session ID、email)
4. **上次验证时间戳** — 拒绝超过 7 天启发式阈值的 profile

每个探测器的失效模式各不相同。把它们合并为单一状态需要一定的推理:

- 全绿 → `configured`
- 探测器 4 过期 + 探测器 1 通过 → `configured`(启发式覆盖;实时检查比 7 天的时钟更权威)
- 探测器 1 被重定向到登录页 → `stale`(cookie 确认失效)
- 探测器 1 超时 + 探测器 2/3 正常 → `unverified`(网络问题,凭证大概率没问题)
- 任一探测器抛出异常 → `error`

## 缓存:30 秒 TTL,带 mtime 绕过机制

`server_info` 工具的结果会被缓存 30 秒(checker 的 `CACHE_TTL`)。每次后续调用时,checker 都会检查磁盘上是否有认证文件被重写过(通过 mtime 检测);如果有,就绕过缓存。这意味着外部执行的 `nlm login` 会在下一次 `server_info` 调用时立刻反映出来,不必等 TTL 到期。

`nlm login --check` 始终是实时的(不缓存),方便用户确认重新认证是否成功。

## 对 AI agent 的启示

**面向使用工具的 agent 的关键规则:**

> 如果 `auth_status = "stale"`,提示用户重新认证。
> 如果 `auth_status = "unverified"` 但最近的操作仍在成功执行,**应视为一次瞬时的监控失效并继续工作**。此时不需要重新认证。

一个朴素的 agent 如果把 `unverified` 当作 `stale` 处理,就会在用户网络本身有问题的情况下,反复循环地提示"请重新登录、请重新登录、请重新登录"。这套 5 状态词汇表的整个意义就在于,给 agent 提供足够的信号来做出正确的判断。

## 泛化

同样的 5 状态模式适用于任何探测外部服务的认证子系统:

| 状态 | 触发时机 |
|-------|------|
| `configured` | 探测确认会话有效 |
| `not_configured` | 磁盘上根本没有凭证 |
| `stale` | 探测确认会话已失效 |
| `unverified` | 探测无法触达该服务 |
| `error` | 探测本身崩溃了 |

`unverified` 状态是承重的那一环——正是它让一个二元的健康检查变成了真正有用的诊断工具。不要因为"我们通常不会遇到网络问题"就把它从词汇表里去掉。

## 相关

- [[concepts/cdp-cookie-extraction]] — 底层的 CDP 认证机制
- [[concepts/multi-profile-google-auth]] — profile 如何与健康检查互动
- [[entities/gemini-notebook-mcp-cli]] — 生产环境实现
