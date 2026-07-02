---
title: Claude Code 配置管理完全指南 - 作用域、权限与企业部署
source: https://www.claudecode.xyz/articles/claude-code-mm4tlbbs
author:
  - "[[ClaudeEagle]]"
published: 2026-02-27
created: 2026-06-25
description: 深度解析 Claude Code 四级配置作用域、权限系统、settings.json 格式及企业 MDM 托管部署方案，适合团队和企业用户。
tags:
  - clippings
  - claude-code
---
Claude Code 拥有灵活的多层级配置系统，从个人偏好到企业安全策略都能精细控制。理解这个配置体系对于团队协作和企业部署至关重要。

## 配置作用域体系

Claude Code 采用四级作用域决定配置的生效范围：

| 作用域 | 位置 | 影响范围 | 与团队共享？ |
| --- | --- | --- | --- |
| **Managed（托管）** | 系统级 managed-settings.json | 机器上所有用户 | 是（IT 部署） |
| **User（用户）** | `~/.claude/` 目录 | 你的所有项目 | 否 |
| **Project（项目）** | 仓库中的 `.claude/` | 所有协作者 | 是（提交到 git） |
| **Local（本地）** | `.claude/*.local.*` 文件 | 仅你，当前仓库 | 否（已 gitignore） |

### 优先级规则

当同一设置在多个作用域中配置时，更具体的作用域优先级更高：

1. **Managed** （最高）- 无法被任何设置覆盖
2. **命令行参数** - 临时会话覆盖
3. **Local** - 覆盖 Project 和 User 设置
4. **Project** - 覆盖 User 设置
5. **User** （最低）- 其他设置都不指定时生效

## Settings.json 配置文件

`settings.json` 是官方支持的配置机制，通过层级设置控制 Claude Code 行为。

### 文件位置

- **用户设置** ： `~/.claude/settings.json` （跨所有项目）
- **项目设置** ：`.claude/settings.json` （提交到版本控制，团队共享）
- **项目本地设置** ：`.claude/settings.local.json` （不提交，个人偏好）

### 完整配置示例

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

### 作用域功能对照表

| 功能 | User 位置 | Project 位置 | Local 位置 |
| --- | --- | --- | --- |
| **Settings** | `~/.claude/settings.json` | `.claude/settings.json` | `.claude/settings.local.json` |
| **Subagents** | `~/.claude/agents/` | `.claude/agents/` | — |
| **MCP servers** | `~/.claude.json` | `.mcp.json` | `~/.claude.json` （按项目） |
| **Plugins** | `~/.claude/settings.json` | `.claude/settings.json` | `.claude/settings.local.json` |
| **CLAUDE.md** | `~/.claude/CLAUDE.md` | `CLAUDE.md` 或 `.claude/CLAUDE.md` | `CLAUDE.local.md` |

## 权限管理

### 权限模式

Claude Code 的权限系统控制 Claude 可以执行哪些工具调用：

```json
{
  "permissions": {
    "allow": [
      "Bash(git *)",
      "Bash(npm run *)",
      "Read(**)",
      "Write(src/**)"
    ],
    "deny": [
      "Bash(rm -rf *)",
      "Bash(sudo *)",
      "Read(./secrets/**)"
    ]
  }
}
```

### 权限通配符说明

- `*` - 匹配单个路径组件
- `**` - 匹配任意深度的路径
- `Bash(npm run *)` - 只允许以 `npm run` 开头的命令

## 企业托管设置

### MDM/系统策略部署

**macOS（Jamf/Kandji 等 MDM）** ： 通过配置文件部署 `com.anthropic.claudecode` 托管偏好域。

**Windows（Group Policy/Intune）** ： 设置注册表键：

- `HKLM\SOFTWARE\Policies\ClaudeCode` （管理员级，最高优先级）
- `HKCU\SOFTWARE\Policies\ClaudeCode` （用户级，最低优先级）

值： `Settings` （REG\_SZ 或 REG\_EXPAND\_SZ），包含 JSON 格式配置。

### 文件部署方式

将 `managed-settings.json` 部署到系统目录：

- **macOS** ： `/Library/Application Support/ClaudeCode/`
- **Linux/WSL** ： `/etc/claude-code/`
- **Windows** ： `C:\Program Files\ClaudeCode\`

### 企业配置示例

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

## 服务端托管设置

通过 Claude.ai 管理控制台，管理员可以从服务端推送配置，无需在每台机器上手动部署：

1. 登录 Claude.ai 管理控制台
2. 进入 Settings → Claude Code
3. 配置组织级设置
4. 这些设置会自动同步到所有使用该组织账号的用户

## 配置文件备份

Claude Code 自动创建带时间戳的配置文件备份，并保留最近 5 个备份，防止数据丢失。

## 环境变量配置

部分设置可通过环境变量配置：

```bash
# 禁用遥测
export CLAUDE_CODE_DISABLE_TELEMETRY=1

# 设置代理（企业环境）
export HTTPS_PROXY=http://proxy.company.com:8080
export HTTP_PROXY=http://proxy.company.com:8080

# 禁用自动更新
export CLAUDE_CODE_DISABLE_AUTOUPDATE=1
```

## 最佳实践建议

### 个人开发者

- 个人偏好（主题、编辑器设置）放在 `~/.claude/settings.json`
- 敏感信息（API key 路径等）放在 `CLAUDE.local.md`
- 不同项目的特定设置放在 `.claude/settings.local.json`

### 团队协作

- 权限规则、Hook 配置放在 `.claude/settings.json` 并提交到 git
- MCP 服务器配置放在 `.mcp.json` 并提交到 git
- 每个人的个人偏好通过 User 作用域管理，不污染项目配置

### 企业部署

- 使用 Managed 作用域强制执行安全策略
- 通过 MDM 或 Group Policy 统一部署
- 利用服务端托管设置实现零接触部署
- 通过 `strictKnownMarketplaces` 限制插件来源

## 总结

Claude Code 的配置体系从个人到企业都有完善的解决方案。理解四级作用域的优先级规则，合理利用权限系统，能够在保证安全性的同时给予开发者足够的灵活性。企业用户可通过 MDM 或服务端托管设置实现统一管理。

---

**来源** ： [Claude Code 官方文档 - Settings](https://code.claude.com/docs/en/settings) **原文作者** ：Anthropic Team