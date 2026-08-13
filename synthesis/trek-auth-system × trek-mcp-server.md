---
title: Trek 认证系统 × MCP 服务器 — AI 工具暴露的认证特化
category: synthesis
tags: [auth, oauth, mcp, api-design, security]
sources:
  - "[[projects/trek/concepts/auth-system]]"
  - "[[projects/trek/concepts/mcp-server]]"
  - "[[projects/trek/concepts/addon-system]]"
  - "[[projects/trek/concepts/architecture-overview]]"
  - "[[projects/trek/concepts/realtime-sync]]"
created: 2026-07-07T10:22:17Z
updated: 2026-07-07T10:22:17Z
summary: "Trek 的 OAuth 2.1 不是 auth-system 的子集——它是针对 AI 客户端的认证特化：受众绑定到 /mcp、scope 切分到 27 项、刷新 token 重放级联吊销、插件切换使会话失效。"
provenance:
  extracted: 0.55
  inferred: 0.4
  ambiguous: 0.05
base_confidence: 0.84
lifecycle: reviewed
lifecycle_changed: "2026-08-12"
lifecycle_reason: "auto-promoted by wiki-lint --consolidate: age>30d, confidence>0.7"
tier: core
---

# Trek Auth × MCP Server

## The Connection

Trek 的 [[projects/trek/concepts/auth-system|认证系统]] 表面上有五种机制（JWT、OIDC、Passkey、TOTP、OAuth 2.1），初看会以为 OAuth 2.1 只是其中一种，与其它四种并列。**实际上不是**——OAuth 2.1 是为 [[projects/trek/concepts/mcp-server|MCP 服务器]] 单独设计的认证通道，与 Web UI 的 JWT 会话**完全分离**。它的设计被四组针对 AI 客户端的特殊约束所驱动：受众绑定到 `/mcp`、scope 拆成 27 项细粒度授权、刷新 token 重放触发级联吊销、插件切换使所有活跃会话失效。这四组约束**只有 AI 客户端场景才需要**——人类用户通过 Web UI 不需要 scope 切分到 27 项。

## Where They Co-occur

`auth-system` 页和 `mcp-server` 页在以下 5 个位置交叉：OAuth 2.1 端点列表（`/.well-known/oauth-protected-resource`、`/oauth/authorize`、`/oauth/token`）、token 轮转策略（1h access / 30d refresh）、SSRF 防护（防止 MCP 工具被诱骗访问内网）、CORS/HSTS（针对 MCP 客户端域）、重放检测与级联吊销。在 `addon-system` 中也能看到 MCP 作为插件的边界——管理员启用/禁用 MCP 插件会**强制吊销所有 MCP 活跃会话**。

## Cross-cutting Insight

Trek 的 OAuth 2.1 实现揭示了**AI 客户端认证**与**人类用户认证**的四组本质差异：

1. **受众绑定（RFC 8707）**：人类用户的 JWT 只关心"是哪个用户在操作"，但 AI 客户端的 token 必须**明确绑定到 `/mcp` 端点**——同一个 access token 不能在 Web API 路径上使用。这防止"拥有 MCP token 等于拥有整个 Trek"。

2. **细粒度 scope 切分**：Web UI 用户通常拥有"对所有自己数据的完全访问权"，没有细粒度拆分。但 AI 客户端（Claude Desktop、Cursor）的使用模式是"完成特定任务"，因此需要 27 项 scope（trips、places、atlas、packing、todos、budget、reservations、collab、notifications、vacay、geo、weather、journey）按需授权。**这反映了"AI 是一次性任务授权、人类是持续登录会话"的根本差异**。

3. **重放级联吊销**：人类用户 token 被偷通常意味着攻击者可以在该 token 有效期内冒充用户。但 AI 客户端场景下，攻击者**可以等待用户做了一次刷新操作后，**重放**已被使用过的 refresh token**——这在 Web UI 场景下不存在（人类用户不会保存已用 refresh token）。Trek 的应对是**一旦检测到 refresh token 被重用，整个 token 链级联吊销**——这一逻辑在 Web UI 场景下过激，但在 AI 场景下是必要的。

4. **插件边界强制失效**：Web UI 用户的 session 寿命**与插件状态无关**——管理员禁用某个插件不影响已登录用户。但 AI 客户端的 MCP 工具集合**在 plugin 切换时整体失效**——因为 AI 客户端的 context（已加载的 trip 摘要、已授权的 scope）全部依赖插件状态。这导致 MCP session 与 addon system **强耦合**。

这四组差异是**AI 工具暴露场景独有的设计模式**——Trek 把它沉淀到了 auth-system 与 mcp-server 的交叉地带。^[inferred]

## Tensions and Trade-offs

- **细粒度 scope vs 客户端复杂度**：27 项 scope 给了用户精细控制，但每个 MCP 客户端（Claude Desktop、Cursor、Continue.dev）需要在初始化时**枚举并征求用户授权**所有可能用到的 scope。这导致授权页一次性列出 27 项 checkbox，**UX 体验下降**。如果降到 5-6 项大 scope 则失去最小权限原则。
- **重放级联吊销 vs 用户体验**：级联吊销在检测到 refresh token 重用时撤销整个 token 链。**但检测**可能误报（例如时钟漂移导致 token 提前过期被刷新了一次）。误报会让正常用户**无故下线**，这对 Web UI 用户是罕见，对 AI 客户端则更严重——AI 任务可能执行到一半被中断。
- **插件切换失效 vs AI 工作流连续性**：管理员关闭 MCP 插件会导致 AI 客户端的整个工作流中断。**对管理员**是必要的安全控制（关闭插件 = 立即停止 AI 访问），**对用户**是破坏性的（AI 工作流可能被中途切断）。
- **OAuth 2.1 元数据 vs 部署复杂度**：Trek 同时实现 `/.well-known/oauth-protected-resource` (RFC 9728) 和 `/.well-known/oauth-authorization-server` (RFC 8414) 以及动态客户端注册 (RFC 7591)。这三套标准**单独看都合理**，组合起来要求**严格**的 `APP_URL` 设置——任何 subdomain mismatch 都会让整个 OAuth 流程失败。

## Strongest Objection

最尖锐的批评可能是：**"Trek 把人类认证和 AI 认证用两套完全独立的 token 系统管理是过度设计——完全可以共用 JWT 加上 scope claim 字段实现"**。这个批评有道理：JWT 已经支持任意 claim，OAuth 2.1 完全可以基于已有 JWT 体系扩展 scope claim 而不必另起炉灶。Trek 选择分立 token 系统的实际理由可能是**隔离爆炸半径**——AI 客户端的 token 被偷只影响 `/mcp` 路径，不影响 Web UI 的会话——但这未必是**架构上必需**的，而可能是**实现上更省事**的。

> test: 如果 Trek 取消独立的 OAuth 2.1 token 体系，改为 JWT + scope claim + audience claim，AI 客户端场景下会出现哪些**架构性**问题（不是实现性）？换言之：把"分立 token"换成"统一 JWT + 多 claim"会导致什么样的**不可逆**问题？

## Open Questions

- **Scope 升级协议**——如果 AI 客户端在执行任务中发现需要新 scope（"我想更新 packing list，但我只有 read scope"），Trek 当前的设计是**拒绝**并要求用户重新走 OAuth 流程。是否存在**scope 升级**的标准化协议（如 RFC 8693 token exchange）适用于 AI 客户端？
- **AI 客户端的可观测性**——人类用户登录后的所有操作都有 IP、user-agent、时间戳日志。AI 客户端的 MCP 调用是否能**区分"是用户主动操作"还是"是 AI 在自动执行"**？这关系到审计（用户能否看到"AI 在我不在时做了 X"）。
- **级联吊销的可逆性**——一旦检测到 refresh token 重用就吊销整链，但**如果用户是误操作**（如同时在两个设备上登录），无法撤销。是否存在"软吊销"（要求下次操作时二次认证）vs"硬吊销"（直接断开）的中间状态？

## Related

- [[projects/trek/concepts/auth-system]]
- [[projects/trek/concepts/mcp-server]]
- [[projects/trek/concepts/addon-system]] — MCP 是插件之一，插件切换强制失效 MCP 会话
- [[projects/trek/concepts/architecture-overview]] — 整体架构（中间件 pipeline）
- [[projects/trek/concepts/realtime-sync]] — WebSocket 临时 token 与 MCP 共享 WebSocket
- [[projects/trek/trek]] — Trek 项目根页
- [[projects/trek/references/environment-variables]] — `APP_URL` 等 OAuth 相关环境变量
