---
title: "Jacob Ben-David — author of gemini-notebook-mcp-cli"
category: entities
tags:
  - people
  - python
  - mcp
  - notebooklm
summary: Maintainer of gemini-notebook-mcp-cli, MIT-licensed, openly states the project is AI-assisted and welcomes refactoring PRs from experienced Python developers.
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

# Jacob Ben-David — author of gemini-notebook-mcp-cli

## Identity

| Field | Value |
|-------|-------|
| GitHub | [`jacob-bd`](https://github.com/jacob-bd) |
| Project | gemini-notebook-mcp-cli |
| Repository | github.com/jacob-bd/gemini-notebook-mcp-cli |
| License held | MIT (author) |
| Self-description | "non-developer using AI coding assistants" |

## Why he's notable in the vault

He maintains the de facto standard for programmatic access to Google NotebookLM — a 43-tool MCP server + full Typer-based CLI that the Gemini Notebook community has consolidated around. The package supersedes older joydig-era `notebooklm-mcp-server` guides.

## Self-described engineering stance

The README includes an unusual "Vibe Coding Alert" section worth quoting verbatim:

> Full transparency: this project was built by a non-developer using AI coding assistants. If you're an experienced Python developer, you might look at this codebase and wince. That's okay.
>
> The goal here was to scratch an itch - programmatic access to Gemini Notebook - and learn along the way. The code works, but it's likely missing patterns, optimizations, or elegance that only years of experience can provide.
>
> **This is where you come in.** If you see something that makes you cringe, please consider contributing rather than just closing the tab. This is open source specifically because human expertise is irreplaceable. Whether it's refactoring, better error handling, type hints, or architectural guidance - PRs and issues are welcome.

This framing — explicit acknowledgment that the code is AI-assisted, with a direct invitation for experienced reviewers — is a useful pattern for any solo maintainer of a popular library. It signals humility without apologizing for shipping, and converts "you should have done X better" energy into PRs.

## Notable design decisions attributable to him

- **Unified-package architecture** — single `notebooklm-mcp-cli` wheel ships both `nlm` and `notebooklm-mcp` binaries (replaces the legacy `notebooklm-cli` + `notebooklm-mcp-server` split)
- **Profile-based multi-account** — `nlm login --profile work` as a first-class workflow
- **Multi-tool installer** — `nlm setup add <client>` for 9+ AI clients instead of hand-editing JSON
- **Auto-resilient auth** — v0.1.9+ auto-refreshes CSRF/session/cookies; v0.9.3+ auto-handles the `notebook.google.com` ↔ `notebook.google.com` rebrand
- **5-state auth health vocabulary** — `configured` / `not_configured` / `stale` / `unverified` / `error`, designed to keep AI agents from looping users into false re-auth prompts
- **Multi-probe `AuthHealthChecker`** — Serdar Akın PR #219, to distinguish "stale credentials" from "monitoring can't tell"

## Major contributors

13+ named contributors with first-time credit; see [[entities/gemini-notebook-mcp-cli]] for the full list.

## Where to find him

- GitHub: [@jacob-bd](https://github.com/jacob-bd)
- Buy Me a Coffee: [buymeacoffee.com/jacobbd](https://buymeacoffee.com/jacobbd) (the README explicitly notes "testing every Gemini Notebook feature takes real time and resources")
- Project issues: github.com/jacob-bd/gemini-notebook-mcp-cli/issues