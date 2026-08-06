---
title: gemini-notebook-mcp-cli — Unified CLI + MCP for Google NotebookLM
category: entities
tags:
  - mcp
  - claude-code
  - notebooklm
  - google
  - ai-coding
  - python
summary: Unified `nlm` CLI + 43-tool MCP server for Google NotebookLM, MIT, by Jacob Ben-David. Supersedes the legacy `notebooklm-mcp-server`.
sources:
  - https://github.com/jacob-bd/gemini-notebook-mcp-cli
created: 2026-08-06
updated: 2026-08-06
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
    type: related_to
---

# gemini-notebook-mcp-cli — Unified CLI + MCP for Google NotebookLM

> **The de facto standard** for programmatic access to Google NotebookLM. Single PyPI package (`notebooklm-mcp-cli`) ships both a 43-tool MCP server (`notebooklm-mcp`) and a full Typer-based CLI (`nlm`). MIT licensed, 13+ named contributors.

## Identity

| Field | Value |
|-------|-------|
| **Package** | `notebooklm-mcp-cli` |
| **CLI binary** | `nlm` |
| **MCP binary** | `notebooklm-mcp` |
| **MCP server name** | `gemini-notebook-mcp` (the executable name is kept for backwards compat) |
| **License** | MIT |
| **Python** | ≥ 3.11 |
| **Author** | Jacob Ben-David (`jacob-bd`) |
| **Status** | Beta (v0.9.7) — but de-facto production for personal use |

## Two products, one package

The same PyPI wheel gives you:

```bash
nlm              # CLI: scriptable, JSON output, aliases, batch ops
notebooklm-mcp   # MCP server: 43 tools, multi-client auto-config
```

Most users install once, then use `nlm` for scripting and let Claude Code/Cursor/Gemini CLI/Antigravity/Codex/Cline/OpenClaw access notebooks via the MCP server.

## What it adds vs the legacy `notebooklm-mcp-server`

The vault previously tracked [[skills/notebooklm-mcp-setup]] (the original `notebooklm-mcp-server` by an unmaintained joydig tutorial). The CLI replaces it with a much larger surface:

| Dimension | Legacy `notebooklm-mcp-server` | New `notebooklm-mcp-cli` |
|-----------|------------------------------|--------------------------|
| Tools | 2 (notebook list, query) | **43** (full coverage) |
| Auth | `--manual` cookie paste only | Auto CDP browser login + manual fallback |
| Multi-account | ✗ | Named profiles (`--profile work`) |
| Setup | Hand-edit `~/.claude.json` | `nlm setup add <client>` for 7+ tools |
| Skills | ✗ | `nlm skill install` for 9 agent targets |
| Batch | ✗ | `batch` + `cross_notebook_query` + `pipeline` |
| Studio generation | ✗ | Audio, video, slides, infographic, mindmap, quiz, flashcards, reports |
| Health checks | ✗ | `nlm doctor`, multi-probe `auth_status` |
| Transport | stdio only | stdio / HTTP / SSE |

## Core architectural decisions

1. **Thin-wrapper layering** — `cli/` and `mcp/` are thin UX wrappers; all business logic lives in `services/`; only `services/` may import `core/`. This is the canonical "ports & adapters" pattern applied to a CLI+MCP product. Source: `CLAUDE.md` Layering Rules.
2. **CDP-driven auth** — Authentication goes through Chrome DevTools Protocol against a managed browser session (`~/.notebooklm-mcp-cli/chrome-profiles/<name>/`). No OAuth flow exists because Google does not expose one; CDP is the only reliable bridge.
3. **Internal-API reliance with graceful degradation** — Google does not document `batchexecute` RPC IDs (`wXbhsf`-style strings). The package detects drift via `RPCDriftError`, supports `NOTEBOOKLM_RPC_OVERRIDES` env var for hot-patching without a release, and auto-retries `RESOURCE_EXHAUSTED` (RPC code 8) with exponential backoff.
4. **Profile isolation by directory** — Each Google account gets `profiles/<name>/auth.json` + a separate Chromium profile. The MCP server always uses the active default profile (`auth.default_profile`), so `nlm login switch` changes the MCP server's identity instantly.
5. **Unified tools over tool-spam** — `source_add`, `studio_create`, `download_artifact`, `note`, `label`, `batch`, `pipeline` are **action-parameterized** rather than separate tools per subtype. Keeps total tool count manageable; trades discoverability for compactness.

## Installation footprint

```bash
uv tool install notebooklm-mcp-cli   # gives you both nlm + notebooklm-mcp
```

- PyPI: `notebooklm-mcp-cli` (single wheel since v0.2.0)
- uv tool directory: `~/.local/bin/nlm` + `~/.local/bin/notebooklm-mcp`
- State directory: `~/.notebooklm-mcp-cli/{config.toml, aliases.json, profiles/, chrome-profiles/}`
- v0.9.3+ auto-handles the `notebook.google.com` ↔ `notebook.google.com` rebrand by recording the host your account actually lands on, per-profile.

## Tested matrix

- ✅ Free / Pro personal accounts
- ✅ Google AI Ultra ($249/mo) tier
- ⚠️ Google Workspace / NotebookLM Enterprise — **untested**; the package has `NOTEBOOKLM_BASE_URL` for custom hosts but no first-party Enterprise validation. PR #114 added the configurable base URL.
- ✅ Windows, macOS, Linux
- ✅ WSL2 (PR #138, Kyle Brodeur)

## What it does NOT do

- **HTTPS / caller auth** — The HTTP transport exposes the server without TLS or per-user authentication. The author warns against deploying it on a public network; see `docs/REMOTE_MCP.md` for the limitations.
- **Per-user multi-tenancy** — Single Google account per MCP process. Multi-account is via profiles (sequential, not concurrent in one process).
- **Upstream API guarantees** — All 43 tools depend on undocumented internal APIs. The author explicitly disclaims production support.

## Credits (from README)

13+ named contributors with first-time attribution:

- Jacob Ben-David (author + maintainer)
- Le Anh Tuan — HTTP transport, debug logging, perf
- David Szabo-Pele — `source_get_content`, Linux auth
- Tony Hansmann — `nlm setup`, `nlm doctor`, CLI Guide
- Fabiana Furtado — batch + cross-notebook query + pipelines + smart select/tagging (PR #90)
- Amy-Ra-lph — TOCTOU-safe credential storage, cookie redaction in logs, SHA-pinned CI (PRs #205–207)
- Robiton — Enterprise base-URL (PR #114)
- Kyle Brodeur — WSL2 auth (PR #138)
- pjeby — connection pooling, fast startup (PR #54)
- beausea — `NOTEBOOKLM_HL` configurable locale (PR #59)
- JumpLao — extended audio/video/image formats (PR #82)
- cbruyndoncx — `cited_text` in query output (PR #81)
- zxyasfas — cited-only research import (PR #188)
- Serdar Akın — multi-probe `AuthHealthChecker` to fix false `"stale"` reports (PR #219)

The README also includes a "Vibe Coding Alert" — the author openly states the project is AI-assisted and welcomes refactoring PRs from experienced Python developers.

## Key related pages

- [[skills/gemini-notebook-mcp-cli-setup]] — install + `nlm setup add` recipe
- [[references/gemini-notebook-mcp-cli-tools]] — 43-tool reference
- [[references/gemini-notebook-mcp-cli-known-issues]] — `bl` param, cookie rotation, API drift
- [[concepts/cdp-cookie-extraction]] — the auth primitive this builds on
- [[concepts/mcp-multi-tool-installer]] — `nlm setup add` as a pattern
- [[concepts/mcp-server-protocol-quirks]] — `--global` / `-s user` / project vs user scope still applies
- [[concepts/nlm-artifact-id-required-for-download]] — `download_artifact` 必须显式传 `artifact_id`，否则取到旧产物
- [[concepts/nlm-studio-create-source-scoping]] — `source_ids`（硬边界）vs `custom_prompt`（软引导）+ CLI `--focus` 命名差异