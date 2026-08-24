---
title: "open-codesign CHANGELOG — v0.1 → v0.2 Agentic Design 演进"
category: references
tags: [open-codesign, changelog, agentic-design, release-notes]
sources:
  - "https://github.com/OpenCoworkAI/open-codesign/blob/main/CHANGELOG.md"
source_url: "https://github.com/OpenCoworkAI/open-codesign/blob/main/CHANGELOG.md"
created: 2026-08-24
updated: 2026-08-24
summary: v0.2.0 (2026-05-09) Agentic Design:workspace-backed sessions + permissioned agent loop + JSONL 历史 + DESIGN.md shared memory + 8 工具(ask/scaffold/skill/preview/gen_image/tweaks/todos/done)。
base_confidence: 0.9
provenance:
  extracted: 0.90
  inferred: 0.05
  ambiguous: 0.05
lifecycle: draft
lifecycle_changed: 2026-08-24
tier: supporting
---

# open-codesign CHANGELOG — 关键演进

## v0.2.0 — Agentic Design(2026-05-09)

将 open-codesign 从"一次性生成器"转变为"本地设计 agent":

### 架构转向

- **Workspace-backed sessions** —— 每个 design 拥有真实 workspace 文件夹,包含 generated sources / assets / exports / `AGENTS.md` / `DESIGN.md` 作为磁盘上的文件,而非密封的 app state
- **Agent loop + tool harness** —— runtime 通过 pi primitives + open-codesign 工具层路由生成:内置 `ask` / `scaffold` / `skill` / `preview` / `gen_image` / `tweaks` / `todos` / `done`
- **Session migration** —— v0.1 数据迁移到 JSONL-backed sessions + workspace 文件,带冲突与缺 workspace 状态检测
- **Desktop UX polish** —— 设置重整、评论模式、tweak 持久化加固、hub 缩略图缓存、生成状态同步

### Provider / 安全 / 安装

- ChatGPT Plus / Codex OAuth 切到 pi-ai 的 `openai-codex-responses` 协议
- DeepInfra / DeepSeek / Kimi / MiniMax / OpenRouter / relay 网关 可靠性加固(超时、回退、可报告 provider 错误)
- 安全: SVG option 清洗、Electron safeStorage 存 secrets、诊断 redact 加密 secret 行、私网探测需显式 opt-in、reference URL 抓取拒绝私网/link-local

## v0.1.x 历史(现已 superseded)

| 版本 | 日期 | 主要变化 |
|---|---|---|
| **v0.1.0** | 2026-04-18 | 首次公开 Electron release,12 内置 design skill,15 demo prompts,HTML/JSX preview,inline comment → AI patch loop,可调滑块,local-first SQLite + 加密 TOML |
| **v0.1.1** | — | JSX preview 解锁(React UMD 替换),基于大小的 context 剪枝,interactive-depth prompt mandate,keyless Codex-import proxies,release pipeline smoke tests |
| **v0.1.2 / 0.1.3** | — | 打包 manifest + SHA256SUMS.txt + CycloneDX SBOM |
| **v0.1.4** | — | AI image generation(gpt-image-2, OpenRouter image models),ChatGPT Plus 登录,CLIProxyAPI 一键导入,原生模块修复(macOS arm64 + Intel x64 DMG) |
| **v0.2.0** | 2026-05-09 | 用 agentic loop 替代一次性生成;workspace-backed sessions + tool harness 全新增;v0.1 数据迁移到 JSONL sessions |

## 演进哲学

**v0.1.x**: 一屏一次性生成,SQLite 存设计 + 元数据,HTML 多次版本以 `design-v{N}.html` 累积。
**v0.2.0**: 设计变可恢复的 agent 会话 —— JSONL tree + workspace 文件夹,跨 session 可重放、可分叉、可压缩。

这一转向与 vault 中 [[concepts/atomic-state-recovery]] 同源:state destruction 不等于 data loss,append-only JSONL 是状态破坏后的二次证据路径。

## 关键贡献者

代码/PR: @hqhq1025 / @Sun-sunshine06 / @snowopsdev / @mussonking / @MoveCloudROY / @cifuentesantonio / @VoidLight00 / @Jiangxy-1 / @GoDiao / @L4b0R / @cydxxzg + dependabot。

安全加固: @snowopsdev (#311)。workspace + Files panel: @mussonking (#271), @MoveCloudROY (#173)。

## 相关

- [[references/open-codesign-readme]] — README 总览
- [[synthesis/Research: open-codesign]] — 综合分析
- [[concepts/agentic-design]] — v0.2.0 引入的 agent loop 抽象
- [[concepts/atomic-state-recovery]] — vault 已有同源概念