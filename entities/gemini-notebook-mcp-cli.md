---

title: gemini-notebook-mcp-cli — 面向 Google NotebookLM 的统一 CLI + MCP
category: entities
tags:
  - mcp
  - claude-code
  - notebooklm
  - google
  - ai-coding
  - python
summary: 由 Jacob Ben-David 开发的统一 `nlm` CLI + 43 工具 MCP server,面向 Google NotebookLM,MIT 许可。取代了旧版的 `notebooklm-mcp-server`。
sources:
  - https://github.com/jacob-bd/gemini-notebook-mcp-cli
created: 2026-08-06
updated: 2026-08-23T09:05:00Z
tier: core
lifecycle: reviewed
lifecycle_changed: "2026-08-06"
base_confidence: 0.85
provenance:
  extracted: 0.80
  inferred: 0.15
  ambiguous: 0.05
relationships:
  - target: "[[skills/notebooklm-mcp-setup]]"
    type: replaces
  - target: "[[skills/gemini-notebook-mcp-cli-setup]]"
    type: related_to
  - target: "[[concepts/cdp-cookie-extraction]]"
    type: uses
  - target: "[[concepts/mcp-multi-tool-installer]]"
    type: uses
  - target: "[[concepts/multi-profile-google-auth]]"
    type: uses
  - target: "[[concepts/auth-status-semantics]]"
    type: uses
  - target: "[[concepts/rpc-drift-hot-patch]]"
    type: uses
  - target: "[[concepts/mcp-server-protocol-quirks]]"
    type: related_to
  - target: "[[references/gemini-notebook-mcp-cli-tools]]"
    type: related_to
  - target: "[[references/gemini-notebook-mcp-cli-known-issues]]"
    type: related_to
  - target: "[[concepts/nlm-artifact-id-required-for-download]]"
    type: related_to
  - target: "[[concepts/nlm-studio-create-source-scoping]]"
    type: related_to---

# gemini-notebook-mcp-cli — 面向 Google NotebookLM 的统一 CLI + MCP

> **事实标准**,用于以编程方式访问 Google NotebookLM。单个 PyPI 包(`notebooklm-mcp-cli`)同时提供一个 43 工具的 MCP server(`notebooklm-mcp`)和一个完整的基于 Typer 的 CLI(`nlm`)。MIT 许可,已有 13 位以上具名贡献者。

## 身份信息

| 字段 | 值 |
|-------|-------|
| **包名** | `notebooklm-mcp-cli` |
| **CLI 二进制文件** | `nlm` |
| **MCP 二进制文件** | `notebooklm-mcp` |
| **MCP server 名称** | `gemini-notebook-mcp`(可执行文件名沿用旧名以保持向后兼容) |
| **许可证** | MIT |
| **Python** | ≥ 3.11 |
| **作者** | Jacob Ben-David(`jacob-bd`) |
| **状态** | Beta(v0.9.7)——但对个人使用场景而言已是事实上的生产可用 |

## 一个包,两个产品

同一个 PyPI wheel 给你两样东西:

```bash
nlm              # CLI:可脚本化、JSON 输出、别名、批量操作
notebooklm-mcp   # MCP server:43 个工具,多客户端自动配置
```

大多数用户安装一次之后,用 `nlm` 做脚本自动化,同时让 Claude Code/Cursor/Gemini CLI/Antigravity/Codex/Cline/OpenClaw 通过 MCP server 访问笔记本。

## 相比旧版 `notebooklm-mcp-server` 增加了什么

该 vault 之前追踪的是 [[skills/notebooklm-mcp-setup]](原始的 `notebooklm-mcp-server`,来自一份无人维护的 joydig 教程)。这个新 CLI 用一个规模大得多的能力面取代了它:

| 维度 | 旧版 `notebooklm-mcp-server` | 新版 `notebooklm-mcp-cli` |
|-----------|------------------------------|--------------------------|
| 工具数量 | 2(笔记本列表、查询) | **43**(全面覆盖) |
| 认证方式 | 仅支持 `--manual` 手动粘贴 cookie | 自动 CDP 浏览器登录 + 手动回退 |
| 多账号 | ✗ | 具名 profile(`--profile work`) |
| 安装配置 | 手动编辑 `~/.claude.json` | `nlm setup add <client>` 支持 7+ 个工具 |
| Skill | ✗ | `nlm skill install` 支持 9 种 agent 目标 |
| 批量操作 | ✗ | `batch` + `cross_notebook_query` + `pipeline` |
| Studio 生成 | ✗ | 音频、视频、幻灯片、信息图、思维导图、测验、闪卡、报告 |
| 健康检查 | ✗ | `nlm doctor`、多探测器式的 `auth_status` |
| 传输方式 | 仅 stdio | stdio / HTTP / SSE |

## 核心架构决策

1. **薄封装分层** — `cli/` 和 `mcp/` 只是薄的 UX 封装层;所有业务逻辑都在 `services/` 中;只有 `services/` 可以导入 `core/`。这是"端口与适配器"模式在 CLI+MCP 产品上的经典应用。来源:`CLAUDE.md` 的 Layering Rules 一节。
2. **CDP 驱动的认证** — 认证过程通过 Chrome DevTools Protocol,针对一个受管理的浏览器会话(`~/.notebooklm-mcp-cli/chrome-profiles/<name>/`)完成。不存在 OAuth 流程,因为 Google 没有提供一个;CDP 是唯一可靠的桥梁。
3. **依赖内部 API,并优雅降级** — Google 并未公开文档化 `batchexecute` RPC ID(形如 `wXbhsf` 的字符串)。该包通过 `RPCDriftError` 检测漂移,支持通过 `NOTEBOOKLM_RPC_OVERRIDES` 环境变量在不发版的情况下热修复,并对 `RESOURCE_EXHAUSTED`(RPC 错误码 8)自动做指数回退重试。
4. **按目录隔离 profile** — 每个 Google 账号都拥有 `profiles/<name>/auth.json` 和独立的 Chromium profile。MCP server 始终使用当前的默认 profile(`auth.default_profile`),因此 `nlm login switch` 能立刻改变 MCP server 的身份。
5. **统一工具而非工具堆砌** — `source_add`、`studio_create`、`download_artifact`、`note`、`label`、`batch`、`pipeline` 都是**用参数区分动作**的,而不是每个子类型对应一个独立工具。这样能把工具总数控制在可管理的范围内,以可发现性换取了紧凑性。

## 安装占用情况

```bash
uv tool install notebooklm-mcp-cli   # 同时给你 nlm 和 notebooklm-mcp
```

- PyPI 包名:`notebooklm-mcp-cli`(自 v0.2.0 起为单一 wheel)
- uv tool 目录:`~/.local/bin/nlm` + `~/.local/bin/notebooklm-mcp`
- 状态目录:`~/.notebooklm-mcp-cli/{config.toml, aliases.json, profiles/, chrome-profiles/}`
- v0.9.3+ 通过按 profile 记录你的账号实际落在哪个域名上,自动处理 `notebook.google.com` ↔ `notebook.google.com` 改版问题。

## 已测试的矩阵

- ✅ 免费版 / Pro 个人账号
- ✅ Google AI Ultra($249/月)套餐
- ⚠️ Google Workspace / NotebookLM Enterprise — **未经测试**;该包提供了 `NOTEBOOKLM_BASE_URL` 用于自定义 host,但没有官方的 Enterprise 验证。PR #114 添加了这个可配置的 base URL。
- ✅ Windows、macOS、Linux
- ✅ WSL2(PR #138,Kyle Brodeur)

## 它不做的事

- **HTTPS / 调用方认证** — HTTP 传输方式在暴露 server 时没有 TLS,也没有按用户的认证机制。作者提醒不要把它部署在公共网络上;具体限制见 `docs/REMOTE_MCP.md`。
- **多租户** — 每个 MCP 进程只支持单个 Google 账号。多账号是通过 profile 实现的(在同一进程中是顺序切换,而非并发)。
- **对上游 API 的保证** — 全部 43 个工具都依赖未公开文档的内部 API。作者明确声明不提供生产级支持保证。

## 致谢(来自 README)

13 位以上具名的首次贡献者:

- Jacob Ben-David(作者 + 维护者)
- Le Anh Tuan — HTTP 传输、debug 日志、性能优化
- David Szabo-Pele — `source_get_content`、Linux 认证
- Tony Hansmann — `nlm setup`、`nlm doctor`、CLI 使用指南
- Fabiana Furtado — 批量操作 + 跨笔记本查询 + pipeline + 智能选择/打标签(PR #90)
- Amy-Ra-lph — TOCTOU 安全的凭证存储、日志中的 cookie 脱敏、SHA 锚定的 CI(PR #205–207)
- Robiton — Enterprise base-URL(PR #114)
- Kyle Brodeur — WSL2 认证(PR #138)
- pjeby — 连接池、快速启动(PR #54)
- beausea — 可配置的 `NOTEBOOKLM_HL` 语言区域(PR #59)
- JumpLao — 扩展的音频/视频/图片格式支持(PR #82)
- cbruyndoncx — 查询输出中的 `cited_text`(PR #81)
- zxyasfas — 仅导入被引用来源的研究结果(PR #188)
- Serdar Akın — 多探测器式 `AuthHealthChecker`,修复错误的 `"stale"` 报告(PR #219)

README 中还有一个"Vibe Coding Alert"(氛围编程警示)段落——作者公开表示这个项目是由 AI 辅助完成的,并欢迎经验丰富的 Python 开发者提交重构 PR。

## 关键相关页面

- [[skills/gemini-notebook-mcp-cli-setup]] — 安装 + `nlm setup add` 配方
- [[references/gemini-notebook-mcp-cli-tools]] — 43 工具参考
- [[references/gemini-notebook-mcp-cli-known-issues]] — `bl` 参数、cookie 轮换、API 漂移
- [[concepts/cdp-cookie-extraction]] — 这个项目所依托的认证原语
- [[concepts/mcp-multi-tool-installer]] — 把 `nlm setup add` 当作一种模式来看
- [[concepts/mcp-server-protocol-quirks]] — `--global` / `-s user` / project vs user scope 依然适用
- [[concepts/nlm-artifact-id-required-for-download]] — `download_artifact` 必须显式传 `artifact_id`，否则取到旧产物
- [[concepts/nlm-studio-create-source-scoping]] — `source_ids`（硬边界）vs `custom_prompt`（软引导）+ CLI `--focus` 命名差异

## Related

- [[synthesis/concepts-mcp-server-protocol-quirks × entities-gemini-notebook-mcp-cli|MCP 协议怪癖 × gemini-notebook-mcp-cli 实现]] — synthesis
