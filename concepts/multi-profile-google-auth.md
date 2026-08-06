---
title: "Multi-Profile Google Auth — N 个账号,N 个隔离的浏览器 profile"
category: concepts
tags:
  - authentication
  - google
  - profiles
  - mcp
summary: 为每个 Google 账号分配独立的 Chromium profile 目录和独立的 auth.json,再用一个单独的"当前默认"指针,从而并发驱动 N 个 Google 账号。
sources:
  - https://github.com/jacob-bd/gemini-notebook-mcp-cli/blob/main/docs/AUTHENTICATION.md
created: 2026-08-06
updated: 2026-08-06
tier: supporting
lifecycle: reviewed
lifecycle_changed: "2026-08-06"
base_confidence: 0.80
provenance:
  extracted: 0.70
  inferred: 0.25
  ambiguous: 0.05
relationships:
  - target: "[[entities/gemini-notebook-mcp-cli]]"
    type: uses
  - target: "[[concepts/cdp-cookie-extraction]]"
    type: related_to
  - target: "[[concepts/auth-status-semantics]]"
    type: related_to
---

# Multi-Profile Google Auth — N 个账号,N 个隔离的浏览器 profile

> 一个 MCP server,N 个 Google 账号,全部同时存活。不需要在浏览器层面倒腾会话,也不需要做 OAuth token 多路复用——只需要 **N 个隔离的文件系统目录 + N 个隔离的 Chromium profile + 一个"默认"指针**。

## 这个模式

```
~/.notebooklm-mcp-cli/
├── config.toml                      # auth.default_profile = "personal"
├── profiles/                        # 每个 profile 的认证数据
│   ├── default/auth.json
│   ├── work/auth.json
│   └── personal/auth.json
└── chrome-profiles/                 # 每个 profile 对应的 Chromium 目录
    ├── default/
    ├── work/
    └── personal/
```

每一对 profile 都是完全自包含的:各自的 cookie、各自的 CSRF/session token、各自的账号邮箱、各自的 Chromium profile(cookie、历史记录、登录状态——彼此完全不共享)。当前默认账号只是 `config.toml` 里的一行;MCP server 启动时读取这一行,并使用对应的那个 profile。

## CLI 命令

```bash
nlm login --profile work            # 创建并认证一个新 profile
nlm login --profile personal        # 再创建并认证一个
nlm login profile list              # 列出所有 profile 及对应邮箱
nlm login switch personal           # 切换默认(对 MCP 即时生效)
nlm login profile rename work company
nlm login profile delete old-profile

# 一次性覆盖,不改变默认值
nlm notebook list --profile work
```

`nlm login switch <name>` 是关键命令——它会重写 `config.toml`,正在运行的 MCP server 会在下一次调用时重新读取其默认值。不需要重启。

## 为什么隔离的 Chromium profile 是不可妥协的

如果你试图用单个 Chromium 实例同时驱动 N 个 Google 账号:

1. **cookie 会互相冲突** — 账号 A 的 Google 会话 cookie 会覆盖账号 B 的
2. **触发反欺诈检测** — Google 的风控引擎会标记来自同一指纹的快速账号切换
3. **登录状态互相污染** — 退出其中一个账号会导致所有账号一起退出
4. **浏览器数据泄露** — 一个账号的扩展、历史记录、自动填充会暴露给下一个账号

Chromium 的 `--user-data-dir` 参数就是这个问题的应急出口——每个目录都是一个完全隔离的浏览器安装实例。该 CLI 始终会传入 `--user-data-dir=~/.notebooklm-mcp-cli/chrome-profiles/<name>/`。

## "MCP 始终使用默认账号"这个微妙之处

MCP server 不能按每次调用去挑选 profile——它在启动时选定一个,之后就一直用这个。要在两个 MCP server 中并发运行两个 Google 账号(例如一个个人用的 Claude Code、一个工作用的 Claude Code),你需要两个独立的 MCP server 进程,并分别设置不同的 `auth.default_profile`。该软件包目前并不原生支持这一点——但你可以这样绕过去:

```bash
# 终端 1:工作账号
NOTEBOOKLM_PROFILE=work nlm mcp-serve

# 终端 2:个人账号
NOTEBOOKLM_PROFILE=personal nlm mcp-serve
```

(需要 `--transport http` 并使用不同端口。)传输细节参见 [[concepts/cdp-cookie-extraction]]。

## 哪些内容会被复制,哪些不会

| 资源 | 是否按 profile 隔离? | 说明 |
|----------|-------------|-------|
| Cookies | ✅ | 由 Chromium profile 隔离 |
| CSRF + session token | ✅ | 从该 profile 的会话中解析得到 |
| 采集到的邮箱 | ✅ | 用于在 `profile list` 中显示 |
| 保存的浏览器登录状态 | ✅ | Chrome 的持久化 cookie |
| `config.toml`(默认指针) | ✗ 全局唯一 | 同一时刻只指向一个 profile |
| MCP server 身份 | ✗ 全局唯一 | 始终作为默认 profile 运行 |
| UI / CLI flag 覆盖 | 按每次调用 | 任意 `nlm` 调用上加 `--profile work` |

## 值得了解的失效模式

| 症状 | 原因 | 解决办法 |
|---------|-------|-----|
| `nlm login --profile work` 打开了浏览器但没有 Google 登录界面 | 已有 Chromium 实例占用了同一个 profile 目录 | 退出所有 Chromium 窗口;CLI 会启动一个全新的专用 profile,所以这种情况很少见 |
| `profile list` 显示的邮箱不对 | 重新认证之前留下的旧 `auth.json` | 重新运行 `nlm login --profile <name>` |
| 两个 profile 显示同一个邮箱 | 你用同一个账号登录了两个 profile | 删除其中一个 |
| `nlm login switch` 之后,MCP server 用的账号仍是旧的 | MCP 进程在启动时缓存了旧 profile | 重启 MCP server(或用 `refresh_auth` 强制重新读取) |

## 泛化

这个模式适用于任何满足以下条件的服务:

1. 认证基于浏览器 cookie(没有 OAuth)
2. 每个用户在任意时刻只有一个身份
3. 用户可能想在不重新交互登录的情况下切换身份

任何基于 CDP 驱动的实现都天然继承了这个模式:[[entities/gemini-notebook-mcp-cli]] 是教科书式的案例;[[entities/claude-mem]] 使用的是单 profile 的简化变体。

## 相关

- [[concepts/cdp-cookie-extraction]] — 底层的认证原语
- [[concepts/auth-status-semantics]] — 如何向用户呈现 profile 健康状态
- [[entities/gemini-notebook-mcp-cli]] — 生产环境实现
