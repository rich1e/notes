---
title: "Jacob Ben-David — gemini-notebook-mcp-cli 的作者"
category: entities
tags:
  - people
  - python
  - mcp
  - notebooklm
summary: gemini-notebook-mcp-cli 的维护者,MIT 许可,公开表示该项目是 AI 辅助完成的,并欢迎经验丰富的 Python 开发者提交重构 PR。
sources:
  - https://github.com/jacob-bd/gemini-notebook-mcp-cli
created: 2026-08-06
updated: 2026-08-06
tier: supporting
lifecycle: draft
lifecycle_changed: "2026-08-06"
base_confidence: 0.80
provenance:
  extracted: 0.75
  inferred: 0.20
  ambiguous: 0.05
relationships:
  - target: "[[entities/gemini-notebook-mcp-cli]]"
    type: related_to
---

# Jacob Ben-David — gemini-notebook-mcp-cli 的作者

## 身份信息

| 字段 | 值 |
|-------|-------|
| GitHub | [`jacob-bd`](https://github.com/jacob-bd) |
| 项目 | gemini-notebook-mcp-cli |
| 仓库 | github.com/jacob-bd/gemini-notebook-mcp-cli |
| 持有许可 | MIT(作者) |
| 自我描述 | "使用 AI 编程助手的非开发者" |

## 为什么他在这个 vault 中值得关注

他维护着以编程方式访问 Google NotebookLM 的事实标准——一个 43 工具的 MCP server 加一个完整的基于 Typer 的 CLI,Gemini Notebook 社区已经围绕它形成了共识。该软件包取代了更早期 joydig 时代的 `notebooklm-mcp-server` 系列教程。

## 自我描述的工程立场

README 中有一段不同寻常的"Vibe Coding Alert"(氛围编程警示),值得原文引用:

> Full transparency: this project was built by a non-developer using AI coding assistants. If you're an experienced Python developer, you might look at this codebase and wince. That's okay.
>
> The goal here was to scratch an itch - programmatic access to Gemini Notebook - and learn along the way. The code works, but it's likely missing patterns, optimizations, or elegance that only years of experience can provide.
>
> **This is where you come in.** If you see something that makes you cringe, please consider contributing rather than just closing the tab. This is open source specifically because human expertise is irreplaceable. Whether it's refactoring, better error handling, type hints, or architectural guidance - PRs and issues are welcome.

这种坦诚——明确承认代码是 AI 辅助完成的,并直接邀请经验丰富的人来 review——对任何一位维护着热门开源库的独立维护者来说,都是一个值得借鉴的做法。它传达出谦逊,但并不为发布这件事道歉,还把"你本该做得更好"式的吐槽能量转化成了 PR。

## 可归于他的一些值得关注的设计决策

- **统一打包架构** — 单个 `notebooklm-mcp-cli` wheel 同时提供 `nlm` 和 `notebooklm-mcp` 两个二进制文件(取代了旧版 `notebooklm-cli` + `notebooklm-mcp-server` 的分裂状态)
- **基于 profile 的多账号支持** — `nlm login --profile work` 作为一等公民式的工作流
- **多工具安装器** — `nlm setup add <client>` 面向 9 个以上的 AI 客户端,而不需要手动编辑 JSON
- **自愈式认证** — v0.1.9+ 自动刷新 CSRF/session/cookie;v0.9.3+ 自动处理 `notebook.google.com` ↔ `notebook.google.com` 的改版问题
- **5 状态认证健康词汇表** — `configured` / `not_configured` / `stale` / `unverified` / `error`,专门设计用来防止 AI agent 因误报而反复循环地要求用户重新认证
- **多探测器式的 `AuthHealthChecker`** — 出自 Serdar Akın 的 PR #219,用于区分"凭证确实失效"与"监控本身判断不出来"

## 主要贡献者

已有 13 位以上具名的首次贡献者;完整名单见 [[entities/gemini-notebook-mcp-cli]]。

## 在哪里可以找到他

- GitHub: [@jacob-bd](https://github.com/jacob-bd)
- Buy Me a Coffee: [buymeacoffee.com/jacobbd](https://buymeacoffee.com/jacobbd)(README 中明确写道"测试 Gemini Notebook 的每一个功能都需要真实的时间和资源")
- 项目 issue: github.com/jacob-bd/gemini-notebook-mcp-cli/issues
