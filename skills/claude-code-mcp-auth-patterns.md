---
title: "Claude Code MCP 鉴权模式：API Key 头 vs OAuth Proxy"
category: skills
tags: [mcp, Claude, oauth, api-key, stitch, skill]
summary: "两种把外部 MCP server 接进 Claude Code 的鉴权范式：(1) HTTP API key 作为 header 直接传，适合轻量服务；(2) Google Cloud OAuth + community proxy，适合长期重度使用。用 Stitch MCP 作为示例，分别给出命令、陷阱和故障清单。"
sources:
  - "https://medium.com/devsecops-ai/how-google-stitch-claude-codes-mcp-integration-changed-the-way-i-build-products-63ecb8ed7f5a"
created: "2026-07-28T00:00:00Z"
updated: "2026-07-28T00:00:00Z"
tier: supporting
lifecycle: draft
lifecycle_changed: "2026-07-28"
base_confidence: 0.45
provenance:
  extracted: 0.80
  inferred: 0.15
  ambiguous: 0.05
relationships:
  - target: "[[concepts/mcp-server-protocol-quirks]]"
    type: related_to
  - target: "[[entities/google-stitch]]"
    type: related_to
  - target: "[[entities/claude-code]]"
    type: related_to
  - target: "[[skills/notebooklm-mcp-setup]]"
    type: related_to
---

# Claude Code MCP 鉴权模式：API Key 头 vs OAuth Proxy

> 两种接 MCP server 的范式——按使用强度选，不要混搭。

## 什么时候用哪种

| 维度 | Path 1：API Key 头 | Path 2：OAuth Proxy |
|------|---------------------|---------------------|
| 适用场景 | 一次性、轻量、个人使用 | 长期重度、多项目 |
| 配置耗时 | 5 分钟 | 10–20 分钟 |
| Token 刷新 | 手动 rotate | 自动 |
| 依赖 | 服务端托管 MCP 端点 | `gcloud` CLI + community proxy |
| 稳定性 | 服务商控端点，相对稳 | 社区包，可能有 rough edges |

经验法则：**先走 Path 1**，撞到刷新 / 配额限制再迁 Path 2。

---

## Path 1：HTTP API Key 作为 Header

适用：服务商托管 MCP 端点，文档明确给出 `X-...-Api-Key` 或 `Authorization: Bearer` 形式的 header。

### 步骤

1. **生成 key**（以 Stitch 为例：登录 stitch.withgoogle.com → 头像 → Stitch settings → API key → Create key。**立即复制保存**，关闭后不可见）。
2. **注册到 Claude Code**：

   ```bash
   claude mcp add stitch --transport http https://stitch.googleapis.com/mcp \
     --header "X-Goog-Api-Key: YOUR-API-KEY" -s user
   ```

   `-s user` ≈ `--global`，写到顶层 `mcpServers`（见 [[concepts/mcp-server-protocol-quirks]]）。

3. **验证连接**：在 Claude Code 会话里说"列出我的 Stitch 项目"，应返回项目列表。

### 安全清单

- ✅ 把 `.claude.json` 和 `.mcp.json` 加入 `.gitignore`——key 是明文。
- ✅ 复制后立刻校验**无尾随空格**——Sachin Sharma 第一次就栽在这。
- ✅ 一旦怀疑泄露（截图、commit、log），立即在服务商后台 rotate。
- ❌ 不要把 key 写进 CLAUDE.md——CLAUDE.md 走提示缓存前缀，会被反复读取放大泄露面。

### 故障清单

| 现象 | 原因 | 解决 |
|------|------|------|
| 工具列表里没出现 MCP | 缺 `-s user` / `--global` | 重新加，或编辑 `~/.claude.json` 把 `projects.<path>.mcpServers` 移到顶层 |
| 401 Unauthorized | key 复制漏字符 / 带空格 | 重新复制并校验 |
| 503 Service Unavailable | 服务商端点暂时不可用 | 重试；持续不可用换 Path 2 或换服务商 |

---

## Path 2：Google Cloud OAuth + Community Proxy

适用：长期使用、自动 refresh 是刚需、能接受额外 10 分钟 setup。

### 步骤

1. **安装并登录 gcloud**：

   ```bash
   # 来自 https://cloud.google.com/sdk
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   gcloud auth application-default set-quota-project YOUR_PROJECT_ID
   ```

2. **启用 API**：

   ```bash
   gcloud beta services mcp enable stitch.googleapis.com --project=YOUR_PROJECT_ID
   ```

3. **初始化 OAuth**：

   ```bash
   npx @_davideast/stitch-mcp init
   ```

   - 在 WSL / SSH / Docker 里浏览器不会自动弹出。**复制终端里的 OAuth URL**到本机浏览器即可（错误信息不会主动告诉你这点）。

4. **注册到 Claude Code**（二选一）：

   **JSON 配置**（编辑 `~/.claude/claude_desktop_config.json`）：
   ```json
   {
     "mcpServers": {
       "stitch": {
         "command": "npx",
         "args": ["-y", "@_davideast/stitch-mcp", "proxy"],
         "env": { "GOOGLE_CLOUD_PROJECT": "YOUR_PROJECT_ID" }
       }
     }
   }
   ```

   **或 CLI**：
   ```bash
   claude mcp add -e GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID \
     -s user stitch -- npx -y @_davideast/stitch-mcp proxy
   ```

### 故障清单（重点！）

| 现象 | 真正原因 | 解决 |
|------|----------|------|
| 跑 `init` / `proxy` 时报 `invalid character 'd'` | 项目根有 `.env` 文件干扰 dotenv 解析 | **先挪开或重命名 `.env`** 再跑 |
| OAuth URL 浏览器没自动打开 | 处于 WSL/SSH/Docker 无 GUI 环境 | 手动复制 URL 到本机浏览器 |
| 用了一小时后开始 401 | 直接 API token 过期；proxy 没生效 | 确认跑的是 `proxy` 子命令而非直连；proxy 会自动 refresh |
| 工具列表里没出现 | `~/.claude/claude_desktop_config.json` 路径放错或 JSON 损坏 | Claude Code 默认读 `~/.claude.json` 顶层 `mcpServers`，CLI 命令走的也是这条 |

### Path 2 额外能力

OAuth 模式下还能从终端直接浏览设计：

```bash
npx @_davideast/stitch-mcp view --projects
npx @_davideast/stitch-mcp view --project YOUR_PROJECT_ID --screen YOUR_SCREEN_ID
npx @_davideast/stitch-mcp serve -p YOUR_PROJECT_ID   # 本地 dev server 预览
```

---

## 决策矩阵速查

```text
你能接受 5 分钟配置？
  └─ 是 → 用 API Key 头（Path 1）
  └─ 否 →
       你需要长期 / 多项目 / 自动 refresh？
         └─ 是 → 用 OAuth Proxy（Path 2）
         └─ 否 → 仍然用 Path 1
```

## 相关页面

- [[concepts/mcp-server-protocol-quirks]] — `-s user` / `--global` 作用域陷阱
- [[entities/google-stitch]] — 本文示例服务
- [[entities/claude-code]] — 注册 MCP 的 agent 端
- [[skills/notebooklm-mcp-setup]] — 另一种 MCP（NotebookLM）的完整流程
- [[concepts/design-md-format-spec]] — Stitch 落地的 DESIGN.md 文件格式
- [[entities/google-labs-code-design]] — 官方 lint CLI（`npx @google/design.md lint DESIGN.md`）
- [[entities/awesome-design-md]] — 74 个真实站点 DESIGN.md 精选集，可直接复用到项目根
- [[synthesis/Research: DESIGN.md 工作流]] — 综合研究页
- [[concepts/ai-cli-hard-limits]] — AI provider CLI 通用隐藏陷阱抽象（HTTP 200 但 `error.message` 承载真因、boolean flag 风格不统一等），与本文"文档-实测落差"主题同构