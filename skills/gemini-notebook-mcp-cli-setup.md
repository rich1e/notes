---
title: "Setup gemini-notebook-mcp-cli — install + nlm setup add + nlm login"
category: skills
tags:
  - mcp
  - claude-code
  - notebooklm
  - install
  - google
summary: Install gemini-notebook-mcp-cli, configure MCP for any AI tool with `nlm setup add`, then authenticate via CDP-driven browser login.
sources:
  - https://github.com/jacob-bd/gemini-notebook-mcp-cli
  - https://github.com/jacob-bd/gemini-notebook-mcp-cli/blob/main/docs/GETTING_STARTED.md
  - https://github.com/jacob-bd/gemini-notebook-mcp-cli/blob/main/docs/AUTHENTICATION.md
  - https://github.com/jacob-bd/gemini-notebook-mcp-cli/blob/main/docs/CLI_GUIDE.md
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
  - target: "[[entities/gemini-notebook-mcp-cli]]"
    type: related_to
  - target: "[[concepts/cdp-cookie-extraction]]"
    type: uses
  - target: "[[concepts/mcp-multi-tool-installer]]"
    type: uses
  - target: "[[concepts/multi-profile-google-auth]]"
    type: uses
  - target: "[[concepts/auth-status-semantics]]"
    type: related_to
  - target: "[[concepts/mcp-server-protocol-quirks]]"
    type: related_to
  - target: "[[references/gemini-notebook-mcp-cli-known-issues]]"
    type: related_to
  - target: "[[references/gemini-notebook-mcp-cli-tools]]"
    type: related_to
  - target: "[[skills/notebooklm-mcp-setup]]"
    type: replaces
---

# Setup gemini-notebook-mcp-cli

> **Replaces** the legacy [[skills/notebooklm-mcp-setup]] recipe. If you installed the old `notebooklm-mcp-server`, follow the migration at the bottom of this page.

## 5-minute install

```bash
# 1. Install (uv is recommended; pip and pipx also work)
uv tool install notebooklm-mcp-cli

# 2. Verify
nlm --version                  # → notebooklm-mcp-cli 0.9.x
which notebooklm-mcp            # → ~/.local/bin/notebooklm-mcp

# 3. Auto-configure MCP for your AI tool (no JSON editing)
nlm setup add claude-code      # or: claude-desktop, gemini, cursor, windsurf,
                                # github-copilot, cline, antigravity, opencode
nlm setup list                  # verify

# 4. Authenticate (launches a managed browser session)
nlm login

# 5. Restart your AI tool, then ask:
#    "List all my Gemini Notebook notebooks"
```

That's it — 5 commands, no manual JSON, no cookie pasting (the CDP browser flow handles auth).

## How auth actually works

`nlm login` does NOT use OAuth (Google does not expose one for NotebookLM). It launches a dedicated Chromium browser profile (`~/.notebooklm-mcp-cli/chrome-profiles/default/`) via Chrome DevTools Protocol, you log into Google there once, and the cookies + CSRF token + session ID are extracted and cached in `~/.notebooklm-mcp-cli/profiles/default/auth.json`. Subsequent logins reuse the saved browser profile — just extracting fresh cookies, no human in the loop.

```
┌────────────────────┐   CDP launch    ┌──────────────────────────┐
│  nlm login         │ ──────────────→ │  Managed Chrome profile   │
│  (CLI / standalone)│                 │  (~/.notebooklm-mcp-cli/ │
└────────────────────┘                 │   chrome-profiles/default)│
                                       └──────────┬───────────────┘
                                                  │ user logs in to Google
                                                  ↓
                                       ┌──────────────────────────┐
                                       │  profiles/default/       │
                                       │   auth.json (cookies +   │
                                       │   CSRF + session + email)│
                                       └──────────────────────────┘
```

Auth lifecycle is fully automated in v0.1.9+:
- Cookies rotate on each request → auto-refresh via CDP against the saved profile
- CSRF token expires in minutes → auto-extracted on MCP startup
- Session ID rotates per session → auto-extracted on MCP startup
- Build label (`bl` param) → auto-extracted during login / CSRF refresh

If you want to inspect auth state:

```bash
nlm login --check                 # live status (bypasses cache)
nlm doctor                        # all-in-one diagnostic
```

The MCP server also exposes `server_info` which reports one of 5 auth states — see [[concepts/auth-status-semantics]].

## `nlm setup add <client>` — the multi-tool installer

The killer feature. Instead of hand-editing 7 different JSON config files for 7 different AI tools, one command per tool:

```bash
nlm setup add claude-code         # writes to ~/.claude.json via `claude mcp add`
nlm setup add claude-desktop      # auto-detects regular + Relay AI/3P profiles
nlm setup add gemini              # writes ~/.gemini/settings.json
nlm setup add cursor              # writes ~/.cursor/mcp.json
nlm setup add windsurf            # writes ~/.codeium/windsurf/mcp_config.json
nlm setup add github-copilot      # writes .vscode/mcp.json
nlm setup add cline
nlm setup add antigravity
nlm setup add opencode
nlm setup add json                # interactive wizard for any other tool
```

For Claude Desktop, the CLI is profile-aware:
- Auto-detects `regular` vs `Relay AI / 3P` profiles
- Refuses to write while Claude is running (Claude rewrites config on shutdown and would clobber the change)
- Never creates a missing profile; only modifies detected ones
- Removal only offers profiles containing `gemini-notebook-mcp` or a recognized legacy entry — unrelated MCPs are not touched

The `nlm setup add json` mode is a wizard: it asks uvx-vs-binary, full-path-vs-name, with-or-without `mcpServers` wrapper, and prints the JSON snippet for copy-paste.

The pattern generalizes — see [[concepts/mcp-multi-tool-installer]].

## Multi-account support

Work + personal Google accounts in parallel:

```bash
nlm login --profile work         # opens browser — log in with work account
nlm login --profile personal     # opens browser — log in with personal account
nlm login profile list           # → work: jane@corp.com, personal: jane@gmail.com

nlm login switch personal        # change MCP server's default
nlm notebook list --profile work # one-off override

# rename / delete
nlm login profile rename work company
nlm login profile delete old
```

Each profile is fully isolated: separate `profiles/<name>/auth.json`, separate Chromium profile directory, separate captured email. You can be logged into multiple Google accounts simultaneously without any browser-level session juggling.

The MCP server always uses the active default profile, so `nlm login switch <name>` instantly re-aims the running MCP at a different Google account — see [[concepts/multi-profile-google-auth]].

## Skill installation for non-MCP tools

Some AI tools (Cline, Antigravity, OpenClaw, Codex, OpenCode, Claude Code, Gemini CLI, Alef Agent) benefit from a SKILL.md that teaches the agent how to use the MCP. Install it for your tool:

```bash
nlm skill install claude-code    # user-level (requires tool detected first)
nlm skill install claude-code --level project   # project-local
nlm skill install codex
nlm skill install gemini-cli
nlm skill install agents         # generic .agents/skills/ target
nlm skill install alef-agent     # separate ~/.alef-agent/workspace/skills/ target
nlm skill list                   # show status across all targets
nlm skill update                 # refresh installed skills
```

## Selective tool exposure (context window control)

The MCP exposes **43 tools** by default — that's a lot of context. Use group-or-name filters:

```bash
# Read-only setup: hide mutating groups
export NOTEBOOKLM_DISABLED_GROUPS="notebooks_manage,sources_manage,studio,research,sharing,notes"

# Hide one extra tool but keep studio_status visible
export NOTEBOOKLM_DISABLED_TOOLS="tag"
export NOTEBOOKLM_ENABLED_TOOLS="studio_status"

# Resolution order: DISABLED_GROUPS → DISABLED_TOOLS → ENABLED_TOOLS
```

Available groups: `notebooks_read`, `notebooks_manage`, `sources_read`, `sources_manage`, `chat`, `query_multi`, `organization`, `automation`, `notes`, `auth`, `server`, `sharing`, `research`, `studio`. Unknown groups are ignored; changes take effect on server restart. See [[concepts/mcp-server-protocol-quirks]] for the broader context-window-control patterns.

## Verification

After install + auth, the canonical smoke test:

```bash
nlm notebook list --json         # CLI: returns JSON array of notebooks
```

In your AI assistant, the equivalent natural-language test:

> "List all my Gemini Notebook notebooks"

If `notebook_list` returns your real notebooks, you're wired up. If you get auth errors, see [[references/gemini-notebook-mcp-cli-known-issues]].

## Migrating from legacy `notebooklm-mcp-server`

If you previously installed the **separate** `notebooklm-cli` + `notebooklm-mcp-server` packages (the joydig-era setup documented at [[skills/notebooklm-mcp-setup]]):

```bash
# 1. Check what's installed
uv tool list | grep notebooklm
# Look for: notebooklm-cli (old) and/or notebooklm-mcp-server (old)

# 2. Remove the old packages
uv tool uninstall notebooklm-cli
uv tool uninstall notebooklm-mcp-server

# 3. Reinstall the unified package (--force fixes uv symlink races)
uv tool install --force notebooklm-mcp-cli

# 4. Re-authenticate (cookies usually survive, but verify)
nlm login --check
nlm login     # only if --check reports stale

# 5. If you had another browser-automation NotebookLM MCP registered under a
#    different name (e.g. "notebooklm"), remove it BEFORE adding the new one.
#    Agents like Hermes get confused when two servers expose overlapping
#    tool names (notebook_create, source_add, notebook_query).
nlm setup add claude-code   # registers as "gemini-notebook-mcp"
```

After migration, restart your AI tool so it picks up the new MCP registration.

## Uninstalling

```bash
uv tool uninstall notebooklm-mcp-cli    # remove the binaries
rm -rf ~/.notebooklm-mcp-cli            # remove cached state (optional)

# Remove from each AI tool:
nlm setup remove claude-code
nlm setup remove cursor
# ...
```