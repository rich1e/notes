---
title: "gemini-notebook-mcp-cli — known issues & fragility"
category: references
tags:
  - mcp
  - notebooklm
  - troubleshooting
  - google
summary: >-
  gemini-notebook-mcp-cli 的脆弱点汇总：未文档化的 `bl` build label、cookie 轮换、~50/天免费额度限流、内部 API 漂移、Chrome 136+ 锁定策略、Claude Desktop profile 的怪异行为。
sources:
  - https://github.com/jacob-bd/gemini-notebook-mcp-cli/blob/main/docs/KNOWN_ISSUES.md
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
    type: related_to
  - target: "[[concepts/cdp-cookie-extraction]]"
    type: related_to
  - target: "[[concepts/rpc-drift-hot-patch]]"
    type: related_to
  - target: "[[concepts/auth-status-semantics]]"
    type: related_to
  - target: "[[references/gemini-notebook-mcp-cli-tools]]"
    type: related_to
---

# gemini-notebook-mcp-cli — known issues & fragility

> 预计会遇到的六大类故障，附当前的缓解方案与每类问题的诊断命令。这份清单是**承重结构**——该包设计上就依赖未文档化的内部 API，因此"脆弱"是常态，不是边缘情况。

## 1. Build Label（`bl`）参数

**是什么。** `batchexecute` RPC 要求携带的前端版本标识符，形如：

```
boq_labs-tailwind-frontend_20260219.16_p2
```

**当前状态（v0.3.11+）。** 已解决——在 `nlm login` 及 CSRF 刷新过程中会自动从页面提取，无需手动干预即可保持最新。

**手动覆盖**（很少需要）：

```bash
export NOTEBOOKLM_BL="boq_labs-tailwind-frontend_YYYYMMDD.XX_pN"
```

解析优先级：环境变量 > 自动提取 > 硬编码兜底值。

## 2. Cookie 过期

**是什么。** 从 Chrome 会话提取的浏览器 cookie 有生命周期限制。

**何时会失效**（`nlm login` 后约 2-4 周）：

- `ValueError: Cookies have expired. Please re-authenticate...`
- API 调用被重定向到 Google 登录页
- 此前正常工作的操作出现认证错误

**修复方案——三种手段，干预程度从低到高：**

```bash
# A. CLI 自动提取（推荐——自动处理浏览器启动 + 登录）
nlm login

# B. Chrome DevTools MCP（agent 内直接操作，若已有该 MCP 则最快）
save_auth_tokens(cookies=<cookie_header>, request_body=<request_body>, request_url=<request_url>)

# C. 手动粘贴（兜底方案）
# Chrome DevTools → Network → 筛选 "batchexecute" → 点击一个请求 →
# Request Headers → 复制 `cookie:` 的值 → 设置 NOTEBOOKLM_COOKIES 环境变量
```

## 3. 速率限制

**是什么。** Gemini Notebook 免费层由服务端强制限制用量。

**当前观察到的限制**（近似值，非官方文档）：

- 每天约 50 次查询
- Studio 内容生成可能有独立的限制

**症状：**

- API 返回速率限制错误
- 操作在会话中途开始失败

**缓解措施：**

- 拉长操作间隔
- **顺序**创建视频（简单的自动重试只覆盖临时性失败；遇到 Studio 速率限制错误后，等 1-2 分钟再重试）
- 避免高频轮询循环
- **按已知 ID 轮询某个 Studio 产物**，而不是反复列出整个 notebook
- 在 API 支持的地方批量查询（`cross_notebook_query`、`batch` action）

PRO / Ultra 档位限额更高，但没有公开的配额数字。

## 4. API 不稳定（未文档化的内部 API）

**是什么。** 该 MCP 使用的是内部、未文档化的 API，Google 可以随时无通知地更改。

**可能出问题的地方：**

- RPC ID（例如列出 notebook 用的 `wXbhsf`）可能被重命名
- 请求/响应结构可能变化
- 可能出现新的必填参数
- 端点可能被弃用或迁移

**症状：**

- 解析错误（响应形状与预期不符）
- 此前正常的操作返回 `None`
- API 返回新的错误信息

**出问题时该怎么做：**

1. 检查问题是否范围广泛（Google 可能刚部署了变更）
2. 用 `--debug` 运行，记录 `RPC IDs in response: [...]` 日志以发现新的 ID
3. 通过 `NOTEBOOKLM_RPC_OVERRIDES` 环境变量打热补丁（见 [[concepts/rpc-drift-hot-patch]]）
4. 确认稳定后提交 PR，附上新的 ID

## 5. CSRF token 与 session ID

**是什么。** 该 MCP 首次使用时会自动从 Gemini Notebook 首页提取 CSRF token（`SNlM0e`）和 session ID（`FdrFJe`）。

**何时会失效：**

- 首页结构发生变化（Google 部署了新前端）
- token 是按会话生成的，若页面不可访问则需要刷新

**症状：**

- `ValueError: Could not extract CSRF token from page`
- 调试用 HTML 会保存到 `~/.notebooklm-mcp-cli/debug_page.html`

**修复：**

1. 查看 `~/.notebooklm-mcp-cli/debug_page.html`，确认首页实际返回了什么
2. 若自动提取失败，从 Chrome DevTools 的 Network 面板手动提取 CSRF 和 session
3. 通过 `save_auth_tokens(cookies=..., request_body=..., request_url=...)` 传入

## 6. Claude Desktop profile 设置

**症状：**

- 设置完成后 MCP 未出现在 Claude Desktop 中
- 即便窗口已关闭，`nlm setup add claude-desktop --profile 3p` 仍提示 Claude 还在运行

**原因。** Claude Desktop 分别维护常规 profile 和 Relay AI/3P profile。Claude 或 Relay AI 在应用打开期间也可能重写自身配置。macOS 可能在窗口关闭后遗留一个 Crashpad 辅助进程——该进程并非活跃的 Claude Desktop 实例，当前版本的 `nlm` 会忽略它。

**修复：**

1. 完全退出选定的 Claude Desktop profile；若 Relay AI 启动器持有该 3P 实例，也要停止它
2. 运行 `nlm setup add claude-desktop --profile 3p`（或 `regular`）
3. 重新打开选定的 Claude Desktop profile，检查其 Developer 设置

CLI 从不会创建一个缺失的 profile。移除操作只会列出包含 `gemini-notebook-mcp` 或可识别的旧版条目的 profile，不会动到其他无关的 MCP 服务器。

## 7. Chrome 136+ 远程调试锁定

**是什么。** Chrome 136+（以及同版本的其他 Chromium 系浏览器）出于安全考虑，限制了**默认 profile** 上的远程调试。

**缓解措施（自动）：**

1. CLI 使用专用的 profile 目录（`~/.notebooklm-mcp-cli/chrome-profiles/<name>/`）
2. 在 Chromium 命令行中追加 `--remote-allow-origins=*`

无需用户操作。如果你自己在改造 [[concepts/cdp-cookie-extraction]] 模式，**不要**尝试挂接到用户已有的默认 profile——连接会失败。

## 8. "认证死循环"陷阱

**症状：** 即便执行了 `nlm login` 或 `refresh_auth`，仍反复出现 `Authentication expired` 错误。

**原因：** MCP 配置中把 `NOTEBOOKLM_COOKIES` 设成了环境变量。它的优先级绝对高于其他所有认证来源——`auth.json`、profile cookie、`save_auth_tokens`、`nlm login`。当这些硬编码的 cookie 过期后，任何恢复操作都无法修复正在运行的 MCP 进程，因为过期的环境变量已经固化在其运行环境中。

**修复（任选一种）：**

1. 在 MCP 配置中把 cookie 值更新为新鲜值，然后重启 AI 工具
2. **彻底移除配置中的 `NOTEBOOKLM_COOKIES` 环境变量**，改用 `nlm login`（推荐——之后认证恢复会自动生效）

`NOTEBOOKLM_CSRF_TOKEN` 和 `NOTEBOOKLM_SESSION_ID` 已废弃且会自动提取；如果配置中还存在，请移除。过期的值会阻碍自动刷新。

## 9. 浏览器绑定重放（罕见）

**症状：** `nlm login` 执行成功，新 cookie 已落地到磁盘，但每次 API 调用仍然失败。

**原因：** Google 的风控引擎将这些 cookie 标记为设备绑定。这些 cookie 在浏览器里可用，但从另一个进程通过 httpx 重放时会失败。

**诊断：**

```bash
nlm doctor auth-replay
```

该命令会比较四条链路——通过 httpx 使用已保存的 cookie、强制轮换 cookie 后再走 httpx、从活跃浏览器重新提取的新鲜 cookie（同样走 httpx）、以及来自该浏览器会话的页内 CDP fetch。如果页内 CDP 链路成功而 httpx 链路失败，判定结果为 `browser_bound_replay`。

**修复：** 启用实验性的 CDP-RPC 传输方式：

```bash
NOTEBOOKLM_RPC_TRANSPORT=cdp nlm notebook list
```

对于 MCP 客户端，在服务器配置中设置同样的环境变量：

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

该方式会在已保存的浏览器 profile 内部通过 `fetch` 发出受支持的表单 POST 请求。默认关闭；仅当 `auth-replay` 返回 `browser_bound_replay` 时才启用。上传/下载/产物传输仍走正常的 HTTP 路径。

## 问题反馈

提交 bug 时请附上：

1. 具体失败的工具/操作
2. 错误信息（请隐去敏感信息——cookie、账号邮箱）
3. 该操作此前是否正常工作过
4. 当前日期（用于与 Google 可能的部署变更做时间关联）

如果自动提取失败，请附上 `~/.notebooklm-mcp-cli/debug_page.html`。

## 相关

- [[entities/gemini-notebook-mcp-cli]] — 该软件包
- [[concepts/cdp-cookie-extraction]] — 该认证模式的失败模式
- [[concepts/rpc-drift-hot-patch]] — 应对未文档化 API 的漂移
- [[concepts/auth-status-semantics]] — 区分"stale（过期）"与"unverified（未验证）"
- [[references/gemini-notebook-mcp-cli-tools]] — 43 个工具的参考手册