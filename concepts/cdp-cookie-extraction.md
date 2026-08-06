---
title: "CDP Cookie Extraction — 以 Chrome DevTools Protocol 作为认证桥梁"
category: concepts
tags:
  - cdp
  - authentication
  - mcp
  - google
  - browser-automation
summary: 当某个服务没有 OAuth 时,通过 Chrome DevTools Protocol 驱动一个受管理的浏览器,从已登录的会话中获取 cookie/CSRF/session。
sources:
  - https://github.com/jacob-bd/gemini-notebook-mcp-cli/blob/main/docs/AUTHENTICATION.md
  - https://github.com/jacob-bd/gemini-notebook-mcp-cli/blob/main/CLAUDE.md
created: 2026-08-06
updated: 2026-08-06
tier: core
lifecycle: reviewed
lifecycle_changed: "2026-08-06"
base_confidence: 0.85
provenance:
  extracted: 0.75
  inferred: 0.20
  ambiguous: 0.05
relationships:
  - target: "[[entities/gemini-notebook-mcp-cli]]"
    type: uses
  - target: "[[concepts/multi-profile-google-auth]]"
    type: related_to
  - target: "[[concepts/auth-status-semantics]]"
    type: related_to
  - target: "[[concepts/mcp-server-protocol-quirks]]"
    type: related_to
---

# CDP Cookie Extraction — 以 Chrome DevTools Protocol 作为认证桥梁

> 当一个服务不提供任何 OAuth 流程,却强制使用基于 cookie 的认证(Google NotebookLM、许多内部管理工具等)时,唯一可靠的编程路径就是**通过 Chrome DevTools Protocol 驱动一个真实的 Chromium 实例,交互式登录一次,然后复用保存下来的浏览器 profile,在每次 token 轮换时重新提取新鲜的 cookie。**

## 这个模式

```
┌────────────────────────────────┐
│ CLI / MCP server (headless)    │
│                                │
│  needs cookies for service X   │
└────────────────┬───────────────┘
                 │ CDP websocket
                 ↓
┌────────────────────────────────┐
│ Managed Chromium profile       │
│ (~/.cache/<app>/chrome/<name>) │
│                                │
│ - already logged into service X│
│ - cookies persist across runs  │
│ - extensions disabled          │
└────────────────────────────────┘
```

这个 CLI **不会**接触你真实的浏览器会话——它会启动一个**专用**的 Chromium profile,这样你日常的浏览状态、扩展程序以及其他 Google 登录都不会受到影响。

## 为什么用 CDP,而不是 Puppeteer/Playwright/Selenium?

| 维度 | CDP(原生) | Puppeteer | Playwright | Selenium |
|-----------|-----------|-----------|------------|----------|
| 通过 Network domain 访问 cookie + header | ✅ 原生 | ✅ 经由 CDP | ✅ 经由 CDP | ⚠️ 需要 DevTools shim |
| 持久化 profile 控制 | ✅ | ✅ | ✅ | ⚠️ |
| 多浏览器支持 | ⚠️ 仅限 Chromium 系 | ⚠️ | ✅ Firefox/Safari/WebKit | ✅ |
| 零额外依赖 | ✅ 只需 `websocket-client` | ❌ 体积大 | ❌ 体积更大 | ❌ 需要 Java |

`gemini-notebook-mcp-cli` 通过 `websocket-client`(所列依赖之一)使用原生 CDP。这是刻意为之的选择——整个认证子系统只有约 300 行代码,因为它只需要用到 Network 和 Page 这两个 domain。

## 具体提取了什么(以 NotebookLM 为例)

一次 `nlm login` 调用后,CLI 会采集四项内容,并缓存到 `profiles/<name>/auth.json`:

1. **Cookies** — `__Secure-1PSID`、`__Secure-3PSID`、`SID`、`HSID`、`SSID`、`APISID`、`SAPISID` 等
2. **CSRF token**(`SNlM0e`) — 嵌在首页 HTML 中,用正则解析出来
3. **Session ID**(`FdrFJe`) — 同样从首页解析得到
4. **账号邮箱** — 从账号选择器/profile 头像处读取

v0.1.9+ 版本去掉了手动传入 CSRF/session 的要求——它们会在 MCP 启动时自动提取。v0.9.3+ 还会自动记录你的账号落在哪个域名上(改版前后是 `notebook.google.com` 对 `notebook.google.com`),并把后续请求路由到那个域名。

## "远程调试"这个陷阱

Chrome 136+ 出于安全考虑,限制了**默认 profile** 上的远程调试。CLI 会自动绕开这个限制,做法是:

1. 始终使用专用的 profile 目录启动(`chrome-profiles/<name>/`)
2. 在 Chromium 命令行中添加 `--remote-allow-origins=*`

用户不需要做任何操作——但如果你在借用这个模式做自己的实现,**不要**尝试挂接到用户已有的默认 profile;那样会连接失败。

## 刷新策略

Cookie 大约能存活 2-4 周,CSRF 只能存活几分钟,session ID 每次 MCP 初始化都会轮换。CLI 对此完全透明地处理:

| Token | 生命周期 | 刷新机制 |
|-------|----------|-------------------|
| Cookies | 数周 | 针对已保存的 profile 重新启动 CDP → 重新提取 |
| CSRF(`SNlM0e`) | 数分钟 | 重新抓取首页 → 每次 MCP 启动时重新解析 |
| Session ID | 每个会话 | 重新抓取首页 → 每次 MCP 启动时重新解析 |
| Build label(`bl`) | 每次 Google 部署变化 | 登录/CSRF 刷新时重新提取 |

如果完整重新认证失败(Google 登录彻底过期,或存在真正的设备绑定重放问题——cookie 在浏览器外无法生效),`nlm doctor auth-replay` 会区分出 `stale_cookies`(直接重新登录即可)和 `browser_bound_replay`(需要切换到 `NOTEBOOKLM_RPC_TRANSPORT=cdp` 走浏览器代理的请求方式)。

## 实验性的 CDP-RPC 应急通道

当仅靠 cookie 无法完成认证时(浏览器绑定重放问题),该包提供了 `NOTEBOOKLM_RPC_TRANSPORT=cdp`——这会让 Gemini Notebook 的 `fetch` POST 请求*在*已保存的浏览器会话*内部*通过 CDP 发起 `fetch`。浏览器提供其实时的 cookie。默认关闭;只有在 `nlm doctor auth-replay` 返回 `browser_bound_replay` 之后才建议开启。

```bash
NOTEBOOKLM_RPC_TRANSPORT=cdp nlm notebook list
```

对于 MCP 客户端,把这个环境变量加到 server 配置里:

```json
{
  "mcpServers": {
    "gemini-notebook-mcp": {
      "command": "notebooklm-mcp",
      "env": { "NOTEBOOKLM_RPC_TRANSPORT": "cdp" }
    }
  }
}
```

上传、下载和产物文件传输仍走正常的 HTTP 路径——只有 `batchexecute` RPC 和笔记本聊天会被隧道到浏览器中。

## 为什么这个模式可以泛化

同样的方案适用于任何满足以下条件的内部 Google 产品(或任何其他仅支持浏览器认证的服务):

1. 你能够在用户机器上驱动 Chromium
2. 用户愿意交互式登录一次
3. 后端 API 接受 cookie 认证

[[entities/gemini-notebook-mcp-cli]] 是这个模式的教科书式范例。同样的模式还出现在 [[entities/claude-mem]] 中(使用 Playwright 做会话捕获)以及 OpenClaw 的浏览器管理器中。**当 OAuth 不可用时,这就是事实上的标准认证模式。**

## 相关概念

- [[concepts/multi-profile-google-auth]] — 如何在 N 个受管理的浏览器 profile 中隔离 N 个 Google 账号
- [[concepts/auth-status-semantics]] — 用于呈现认证问题的 5 状态健康词汇表
- [[concepts/mcp-server-protocol-quirks]] — 更广义的 MCP 认证生态(API key、OAuth 代理、cookie)
- [[references/gemini-notebook-mcp-cli-known-issues]] — 出问题时该怎么办
