---
title: Claude Code 配置管理
category: skills
tags:
  - claude-code
  - settings
  - security
summary: Claude Code 四级配置作用域体系、settings.json 格式、权限系统及企业 MDM 托管部署方案。
sources:
  - https://www.claudecode.xyz/articles/claude-code-mm4tlbbs
  - https://moksaweb.com/claude-code-terminal-configuration/
created: 2026-06-29
updated: 2026-07-25
tier: core
lifecycle: draft
lifecycle_changed: "2026-07-25"
base_confidence: 0.83
provenance:
  extracted: 0.90
  inferred: 0.08
  ambiguous: 0.02
relationships:
  - target: "[[skills/claude-code-token-optimization]]"
    type: related_to
  - target: "[[skills/tmux]]"
    type: related_to
---

# Claude Code 配置管理

## 四级配置作用域

优先级从高到低：

| 作用域 | 位置 | 影响范围 | 与团队共享？ |
|--------|------|----------|------------|
| **Managed（托管）** | 系统级 managed-settings.json | 机器上所有用户 | 是（IT 部署） |
| **命令行参数** | 临时会话覆盖 | 当前命令 | — |
| **Local（本地）** | `.claude/*.local.*` | 仅你，当前仓库 | 否（gitignore） |
| **Project（项目）** | 仓库中 `.claude/settings.json` | 所有协作者 | 是（提交 git） |
| **User（用户）** | `~/.claude/settings.json` | 你的所有项目 | 否 |

## 配置文件位置

```
~/.claude/settings.json          # 用户级（跨所有项目）
.claude/settings.json            # 项目级（提交 git，团队共享）
.claude/settings.local.json      # 项目本地（不提交，个人偏好）
```

各作用域对应功能：

| 功能 | User | Project | Local |
|------|------|---------|-------|
| Settings | `~/.claude/settings.json` | `.claude/settings.json` | `.claude/settings.local.json` |
| Subagents | `~/.claude/agents/` | `.claude/agents/` | — |
| MCP servers | `~/.claude.json` | `.mcp.json` | `~/.claude.json`（按项目） |
| CLAUDE.md | `~/.claude/CLAUDE.md` | `CLAUDE.md` | `CLAUDE.local.md` |

## settings.json 完整示例

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": [
      "Bash(npm run lint)",
      "Bash(npm run test *)",
      "Read(~/.zshrc)"
    ],
    "deny": [
      "Bash(curl *)",
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)"
    ]
  },
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp"
  },
  "autoMemoryEnabled": true,
  "theme": "dark"
}
```

## 权限系统

通配符说明：
- `*` — 匹配单个路径组件
- `**` — 匹配任意深度路径
- `Bash(npm run *)` — 只允许以 `npm run` 开头的命令

## 终端配置（Terminal Configuration）

### 终端选择建议
- **macOS**：iTerm2（支持最完整，支持 Nerd Font、true color、Semantic History）
- **跨平台**：Warp（Rust-based，内置 AI 命令建议）
- **Windows**：Windows Terminal + WSL2

### 推荐的 iTerm2 配置
- Font：MesloLGS NF 或 Hack Nerd Font Mono
- Color Preset：Solarized Dark 或 One Dark

### 关键环境变量

```bash
export ANTHROPIC_API_KEY=sk-...
export ANTHROPIC_MODEL=claude-sonnet-4-6
export CLAUDE_CODE_DISABLE_AUTOUPDATE=1
export HTTPS_PROXY=http://proxy.company.com:8080  # 企业代理
```

## 企业部署

### MDM/系统策略

**macOS（Jamf/Kandji）**：通过配置文件部署 `com.anthropic.claudecode` 托管偏好域

**Windows（Group Policy/Intune）**：
- `HKLM\SOFTWARE\Policies\ClaudeCode`（管理员级，最高优先级）
- `HKCU\SOFTWARE\Policies\ClaudeCode`（用户级）

### 文件部署路径

| 平台 | managed-settings.json 位置 |
|------|--------------------------|
| macOS | `/Library/Application Support/ClaudeCode/` |
| Linux/WSL | `/etc/claude-code/` |
| Windows | `C:\Program Files\ClaudeCode\` |

### 企业安全配置示例

```json
{
  "permissions": {
    "deny": [
      "Bash(curl *)",
      "Bash(wget *)",
      "Read(/etc/passwd)",
      "Write(/etc/**)"
    ]
  },
  "telemetry": {
    "enabled": true,
    "endpoint": "https://your-internal-otlp-endpoint.com"
  },
  "strictKnownMarketplaces": true
}
```

### 服务端托管（零接触部署）

通过 Claude.ai 管理控制台，管理员可以从服务端推送配置：

1. 登录 Claude.ai 管理控制台
2. 进入 Settings → Claude Code
3. 配置组织级设置
4. 设置自动同步到所有该组织账号用户——无需在每台机器上手动部署

## 配置文件备份

Claude Code 自动创建带时间戳的配置文件备份，并**保留最近 5 个备份**，防止数据丢失。

## 环境变量配置

部分设置可通过环境变量覆盖：

```bash
# 禁用遥测
export CLAUDE_CODE_DISABLE_TELEMETRY=1

# 设置代理（企业环境）
export HTTPS_PROXY=http://proxy.company.com:8080
export HTTP_PROXY=http://proxy.company.com:8080

# 禁用自动更新
export CLAUDE_CODE_DISABLE_AUTOUPDATE=1
```

## 最佳实践

- **个人开发者**：偏好放 `~/.claude/settings.json`，敏感信息放 `CLAUDE.local.md`
- **团队协作**：权限规则和 Hook 放 `.claude/settings.json` 并提交 git，MCP 配置放 `.mcp.json`
- **企业**：Managed 作用域强制安全策略，通过 MDM 统一部署

## 相关页面

- [[skills/claude-code-token-optimization]] — Token 优化策略
- [[skills/tmux]] — 终端复用，配合 Claude Code 使用
- [[synthesis/fabric-patterns × claude-code-settings]] — Claude Code 配置与 Fabric Pattern 的 AI Unix 管道哲学
