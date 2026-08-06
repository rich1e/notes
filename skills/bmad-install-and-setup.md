---
title: "BMad 安装与设置"
category: skills
tags:
  - bmad-method
  - install
  - setup
  - skill
summary: "BMad Method 安装流程：`npx bmad-method install`；前置 Node.js 20.12+ / Python 3.10+ / uv；安装器检查 uv 并指向设置；既有 codebase 走 `bmad-document-project` 建 verified context。"
sources:
  - "https://github.com/bmad-code-org/bmad-method"
created: "2026-08-05T07:00:00Z"
updated: "2026-08-05T07:00:00Z"
provenance:
  extracted: 0.90
  inferred: 0.06
  ambiguous: 0.04
base_confidence: 0.72
lifecycle: draft
lifecycle_changed: "2026-08-05"
tier: supporting
relationships:
  - target: "[[entities/bmad-method]]"
    type: related_to
  - target: "[[skills/bmad-customize-skill]]"
    type: related_to
---

# BMad 安装与设置

> 在项目根目录一行命令装 BMad。前置依赖 + 安装器行为 + 既有 codebase 路径。

## 前置

- **Node.js** 20.12+
- **Python** 3.10+
- **[uv](https://docs.astral.sh/uv/)** —— Astral 出品的 Python 包/版本管理工具
  - v6.10 起安装器检查 uv
  - **v7 起所有 BMad Python 脚本标准化用 `uv run`** 而非直接 `python3`
  - v6 时期 `uv` 缺失只**警告不阻塞**——但有些 skills 性能降级
  - **现在该装**：让 AI agent "install and set up uv for me" 即可

## 一行安装

```bash
npx bmad-method install
```

打开项目在 AI coding 工具里，调 `bmad-build` + 你想改什么，保留重要决策。任何时候想要引导用 `bmad-help`。

## 两种安装路径

| 路径 | 何时用 |
|---|---|
| **[Build your first project with BMad](https://docs.bmad-method.org/tutorials/getting-started/)** | 从零起 |
| **[Add BMad to an existing codebase](https://docs.bmad-method.org/how-to/established-projects/)** | 既有 codebase |

## 既有 Codebase 的 verified context 流程

BMad 的"既有 codebase"路径不是简单装上插件——要先**建立 verified context**：

1. 装 BMad → 安装器检测到非空项目
2. 跑 `bmad-document-project` —— Mary (Analyst) 或直接调
3. **生成 verified context artifact** —— 把代码库现状"考古"出来
4. 之后 BMad 工作流从 verified context 出发，**不从零猜测**

这把 [[concepts/deterministic-agent-memory]] 的"同 query 同答案"哲学用到 codebase 文档——verified context = codebase 的 deterministic fact layer。

## v7 迁移：全标准化 `uv run`

v6.9 changelog 明确预告 v7 breaking：

> "In the v7 release, every skill that runs a Python script will standardize on `uv run` instead of calling `python3` directly — `uv` provisions the interpreter and manages dependencies, so scripts run consistently regardless of what's on your PATH."

**理由**：行业向 uv 收敛；uv 配 interpreter + 管依赖，scripts 跨机器一致。

**现在能做的**：

- 装 + 配 uv（`docs.astral.sh/uv/`）
- 自定义 skills / overrides 现在直接 `python3` 的**规划迁移**到 `uv run`
- **不装也行**——v6 仍只警告不阻塞，但有些 skills 需 AGENTS.md 之类 shim

## 非交互式安装 + CI/CD

- **非交互**：prerelease / CI/CD 用 `--yes` flag（`post-install-message` 非阻塞）
- **预发布**：prerelease builds 走 `npx bmad-method@prerelease install`（或类似）
- **配置 override**：通过 TOML 文件
- **完整指南**：[install-bmad](https://docs.bmad-method.org/how-to/install-bmad/)

## 升级到 v6

已有 v5 / v4 项目：

```bash
npx bmad-method@latest install
```

按 [upgrade-to-v6](https://docs.bmad-method.org/how-to/upgrade-to-v6/) 指南迁移。

## 安装后第一件事

调 `bmad-help` —— 给你"下一步建议"或"哪些是 optional"。

## 与 vault 已有 skill 的关系

| vault 已有 | BMad 安装的特殊点 |
|---|---|
| [[skills/obsidian-wiki-daily-cron-macos]] | 本 vault 已有 launchd cron 安装经验可类比 BMad 的 TOML 解析链 |
| [[skills/claude-code-token-optimization]] | "uv run" 标准化 = 类似 Claude Code 的 token 优化纪律 |
| [[concepts/mcp-server-protocol-quirks]] | BMad 支持加 MCP 集成——通过 customize.toml 的 TOML 覆盖 |

## Related

- [[entities/bmad-method]] — 框架本体
- [[skills/bmad-customize-skill]] — 安装后的定制
- [[references/bmad-method-github-readme]] — 完整 README 索引