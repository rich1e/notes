---
title: "obsidian-wiki 框架 — 本 vault 的运行环境"
category: entities
tags:
  - obsidian-wiki
  - framework
  - tool
  - skill-based
  - ai-agent
sources:
  - https://github.com/Ar9av/obsidian-wiki
  - _raw/github-Ar9av-obsidian-wiki.txt (gitingest export, Ar9av/obsidian-wiki main, 2026-08-04)
created: 2026-08-04T11:35:00Z
updated: 2026-08-04T11:35:00Z
summary: GitHub 仓库 Ar9av/obsidian-wiki — 本 vault 使用的 SKILL-based Obsidian 知识库框架,39 个 markdown skill + Python CLI 包 + Chrome capture 扩展,源自 Andrej Karpathy 的 LLM Wiki gist,支持多 agent(Claude Code / Codex / Cursor / Windsurf / Gemini / Hermes / OpenClaw / Pi / Copilot / Kiro)。
tier: core
lifecycle: verified
lifecycle_changed: "2026-08-04"
base_confidence: 0.95
provenance:
  extracted: 0.95
  inferred: 0.04
  ambiguous: 0.01
relationships:
  - target: "[[entities/Ar9av]]"
    type: derived_from
  - target: "[[concepts/obsidian-wiki-vault-structure]]"
    type: related_to
  - target: "[[concepts/wiki-framework-self-reference]]"
    type: related_to
---

# obsidian-wiki 框架

> 当前 vault 自身运行的框架——**自我引用页**。本仓库是 vault 所用工具的本源,与 vault 自身的内容 **不应重复 distill**(见 [[concepts/wiki-framework-self-reference]])。

## 是什么

[Ar9av/obsidian-wiki](https://github.com/Ar9av/obsidian-wiki) 是一个 SKILL-based Obsidian 知识库框架:

- **39 个 markdown skill**(`wiki-ingest`、`wiki-query`、`wiki-lint`、`wiki-status`、`wiki-synthesize`、`wiki-history-ingest claude/codex/hermes/...` 等)
- **Python 包** `obsidian_wiki/` 提供 CLI、cache、graph analysis、lint、setup、session brain
- **Chrome 扩展** `extensions/brain-capture/` 零构建捕获网页
- **多 agent bootstrap**:`CLAUDE.md` / `AGENTS.md` / `GEMINI.md` / `.hermes.md` / `.cursor/rules/obsidian-wiki.mdc` 等覆盖 Claude Code / Codex / Cursor / Windsurf / Gemini / Hermes / OpenClaw / Pi / Copilot / Kiro / OpenCode / Aider / Droid / Trae / Antigravity 15+ 工具

## 一句话

> "A digital brain you grow with your AI agent. It remembers what you figure out, connects it to what you already know, and answers when you ask."

## 设计哲学(README 第 462-466 行)

> "You solve a hard problem on a Tuesday. Three months later, in a different repo, you solve it again from scratch — because the answer lived in a chat log you'll never find. This fixes that."

底层思想来自 [Andrej Karpathy 的 LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f):**compile knowledge once and keep it current**,而不是每次问 LLM 同样的问题或重跑 RAG。

## 核心引擎(4 阶段 ingest pipeline)

| 阶段 | 做什么 | 谁做 |
|---|---|---|
| 1. Ingest | 读源(md / PDF / JSONL / log / 截图) | agent |
| 2. Pull | 抽概念 / 实体 / 命题 / 关系 / open questions | agent |
| 3. Merge | 与已有页合并,不重复 | agent |
| 4. Schema | 维持 category 一致、wikilink 真实、index 同步 | agent |

→ 详见 [[concepts/obsidian-wiki-vault-structure]]

## 安装

```sh
pip install obsidian-wiki
obsidian-wiki setup --vault ~/brain
```

或纯 agent 驱动:

```text
https://github.com/Ar9av/obsidian-wiki — set up my wiki
```

## 与 vault 现状的关系

本 vault `/Users/rich1e/workspace/code/notes` 的:

- `CLAUDE.md` / `AGENTS.md` —— 与 Ar9av/obsidian-wiki 的 `CLAUDE.md` 等价
- `.claude/skills/*` —— 39 个 symlink 指向 `~/.local/pipx/venvs/obsidian-wiki/.../obsidian_wiki/_data/skills/`
- `_meta/`, `_insights.md`, `_raw/` 等结构 —— 与框架文档完全一致

也就是说:**本 vault 已经在用这个框架,本身就是它的"实例化"**。

## 与"自我引用"相关的注意

Ingest 这个仓库时,**应避免重复 distill** 框架自带内容(已存在于本 vault 的 hot.md / CLAUDE.md / 各 skill 的引用中)。本次 ingest 只创建框架本体 / owner / 自指概念 3 页,**不复制架构 / skill 列表 / CLI 文档**。详见 [[concepts/wiki-framework-self-reference]]。

## 相关

- 框架 owner:[[entities/Ar9av]]
- 标准 vault 结构:[[concepts/obsidian-wiki-vault-structure]]
- 自我引用拓扑:[[concepts/wiki-framework-self-reference]]
- README:https://github.com/Ar9av/obsidian-wiki
- PyPI:https://pypi.org/project/obsidian-wiki/