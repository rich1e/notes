---
title: "MCP Multi-Tool Installer — `nlm setup add <client>` pattern"
category: concepts
tags:
  - mcp
  - cli
  - dx
  - pattern
summary: Ship MCP server configs to 7+ AI tools via one CLI command each, instead of asking users to hand-edit 7 different JSON config files at 7 different paths.
sources:
  - https://github.com/jacob-bd/gemini-notebook-mcp-cli/blob/main/docs/CLI_GUIDE.md
created: 2026-08-06
updated: 2026-08-06
tier: supporting
lifecycle: reviewed
lifecycle_changed: "2026-08-06"
base_confidence: 0.85
provenance:
  extracted: 0.80
  inferred: 0.15
  ambiguous: 0.05
relationships:
  - target: "[[entities/gemini-notebook-mcp-cli]]"
    type: uses
  - target: "[[concepts/mcp-server-protocol-quirks]]"
    type: related_to
  - target: "[[concepts/auth-status-semantics]]"
    type: related_to
---

# MCP Multi-Tool Installer — `nlm setup add <client>` pattern

> When your MCP server needs to be reachable from Claude Code + Claude Desktop + Gemini CLI + Cursor + Windsurf + GitHub Copilot + Cline + Antigravity + OpenCode + OpenClaw + ..., the user shouldn't hand-edit 7 different JSON config files at 7 different paths. One CLI command per tool: `nlm setup add <client>`.

## Why this is non-trivial

Every AI tool stores MCP server config in a different place, with a different JSON shape:

| Tool | Path | Top-level key | Sub-key | "Servers" array? |
|------|------|--------------|---------|------------------|
| Claude Code | `~/.claude.json` | `mcpServers` | `command` + `args` | dict |
| Claude Desktop (macOS current) | `~/Library/Application Support/Claude-3p/claude_desktop_config.json` | `mcpServers` | `command` | dict |
| Claude Desktop (macOS legacy) | `~/Library/Application Support/Claude/claude_desktop_config.json` | `mcpServers` | `command` | dict |
| Claude Desktop (Windows) | `%APPDATA%\Claude\claude_desktop_config.json` | `mcpServers` | `command` | dict |
| Claude Desktop (Linux) | `~/.config/Claude/claude_desktop_config.json` | `mcpServers` | `command` | dict |
| Gemini CLI | `~/.gemini/settings.json` | `mcpServers` | `command` + `args` | dict |
| Cursor | `~/.cursor/mcp.json` | `mcpServers` | `command` | dict |
| Windsurf | `~/.codeium/windsurf/mcp_config.json` | `mcpServers` | `command` | dict |
| GitHub Copilot | `.vscode/mcp.json` | `servers` ⚠️ | `command` + `args` | dict |
| Cline | `~/.cline/mcp.json` | `mcpServers` | `command` + `args` | dict |
| Antigravity | varies | varies | | |

That's 9 paths × 9 schemas, before you count Relay AI / 3P variants. **Hand-editing is error-prone at scale** — wrong path, wrong key, missing `mcpServers` wrapper, forgetting to restart the tool.

## The `nlm setup add <client>` interface

```bash
nlm setup add claude-code       # one command per tool
nlm setup add claude-desktop
nlm setup add gemini
nlm setup add cursor
nlm setup add windsurf
nlm setup add github-copilot
nlm setup add cline
nlm setup add antigravity
nlm setup add opencode
nlm setup add json              # wizard for anything else

nlm setup list                  # show status across all detected tools
nlm setup remove claude-desktop --profile regular
```

For unsupported tools, `nlm setup add json` is an **interactive wizard**: it asks uvx-vs-binary, full-path-vs-name, with-or-without `mcpServers` wrapper, then prints a JSON snippet to clipboard.

## Subtle but important behaviors

1. **Path detection, not creation.** The CLI refuses to write if the config path doesn't already exist. It does not bootstrap a new tool's config; it only modifies detected ones. (Important: this prevents the CLI from creating half-formed configs for tools the user hasn't installed.)
2. **Claude Desktop profile awareness.** Claude Desktop ships with two parallel profiles — `regular` and `Relay AI / 3P`. The CLI auto-detects both and asks which to target (or accepts `--profile regular|3p|both` for scripts).
3. **Process-already-running detection.** Claude (and some others) rewrites its config on shutdown. If the CLI detects a running Claude instance, it **refuses to write** and asks the user to quit first. Otherwise the change gets clobbered.
4. **Scoped removal.** Removal only offers profiles/configs that contain your server name OR a recognized legacy entry. Unrelated MCPs in the same config file are untouched.
5. **JSON merge, not overwrite.** The CLI merges into the existing config file using dict-update semantics — existing MCP entries are preserved, only the new one is added.

## The two-command install story

Combined with `nlm login`, the entire onboarding is two commands:

```bash
uv tool install notebooklm-mcp-cli   # step 1: get the binaries
nlm setup add claude-code            # step 2a: wire it into Claude Code
nlm login                           # step 2b: authenticate
```

Compare with the legacy [[skills/notebooklm-mcp-setup]] recipe which required:

1. `uv tool install` ✓
2. `claude mcp add --global ...` with the right name and scope ← tricky
3. Manually edit `~/.claude.json` if step 2 went wrong ← error-prone
4. Restart Claude Code
5. `notebooklm-mcp-auth` and paste cookies ← hostile

`nlm setup add` removes three of those five steps.

## What this pattern generalizes to

Any CLI that needs to install itself into multiple third-party tools can adopt the same pattern:

- **N target tools** × **M schema variations** × **K profile variants** → one CLI command per target
- **Detection** before **creation** (don't bootstrap configs for tools not installed)
- **Refuse-to-write** when the target process is running (else the change gets clobbered)
- **Interactive JSON wizard** as the escape hatch for unsupported tools

The `nlm setup add json` wizard in particular is worth copying wholesale — it's the same UX as `gh auth login` and avoids the "send me your tool's config file" support burden.

## Related

- [[concepts/mcp-server-protocol-quirks]] — the underlying scope/JSON-quirks this builds on
- [[entities/gemini-notebook-mcp-cli]] — production implementation
- [[concepts/auth-status-semantics]] — the `nlm doctor` companion