---
title: "Multi-Profile Google Auth — N accounts, N isolated browser profiles"
category: concepts
tags:
  - authentication
  - google
  - profiles
  - mcp
summary: Drive N Google accounts concurrently by giving each one its own Chromium profile directory + its own auth.json, with a separate "active default" pointer.
sources:
  - https://github.com/jacob-bd/gemini-notebook-mcp-cli/blob/main/docs/AUTHENTICATION.md
created: 2026-08-06
updated: 2026-08-06
tier: supporting
lifecycle: reviewed
lifecycle_changed: "2026-08-06"
base_confidence: 0.80
provenance:
  extracted: 0.70
  inferred: 0.25
  ambiguous: 0.05
relationships:
  - target: "[[entities/gemini-notebook-mcp-cli]]"
    type: uses
  - target: "[[concepts/cdp-cookie-extraction]]"
    type: related_to
  - target: "[[concepts/auth-status-semantics]]"
    type: related_to
---

# Multi-Profile Google Auth — N accounts, N isolated browser profiles

> One MCP server, N Google accounts, all live simultaneously. No browser-level session juggling, no OAuth token multiplexing — just **N isolated filesystem directories + N isolated Chromium profiles + a "default" pointer**.

## The pattern

```
~/.notebooklm-mcp-cli/
├── config.toml                      # auth.default_profile = "personal"
├── profiles/                        # auth data per profile
│   ├── default/auth.json
│   ├── work/auth.json
│   └── personal/auth.json
└── chrome-profiles/                 # Chromium profile dirs per profile
    ├── default/
    ├── work/
    └── personal/
```

Each profile pair is fully self-contained: own cookies, own CSRF/session tokens, own account email, own Chromium profile (cookies, history, login state — none of it shared). The active default is a single line in `config.toml`; the MCP server reads it on startup and uses that one.

## The CLI verbs

```bash
nlm login --profile work            # create + auth a new profile
nlm login --profile personal        # create + auth another
nlm login profile list              # list with email addresses
nlm login switch personal           # change default (instant for MCP)
nlm login profile rename work company
nlm login profile delete old-profile

# One-off override without changing default
nlm notebook list --profile work
```

`nlm login switch <name>` is the magic verb — it rewrites `config.toml` and the running MCP server re-reads its default on the next call. No restart required.

## Why isolated Chromium profiles are non-negotiable

If you tried to drive a single Chromium instance with N Google accounts:

1. **Cookie collision** — Google session cookies for account A would clobber account B
2. **Anti-fraud detection** — Google's risk engine flags rapid account switching from the same fingerprint
3. **Login state pollution** — Logging out of one logs out all
4. **Browser data leakage** — Extensions, history, autofill from one account visible to the next

Chromium's `--user-data-dir` flag is the escape hatch — each directory is a fully isolated browser install. The CLI always passes `--user-data-dir=~/.notebooklm-mcp-cli/chrome-profiles/<name>/`.

## The "MCP always uses default" subtlety

The MCP server cannot pick a profile per-call — it picks one at startup and sticks with it. To run two Google accounts concurrently in two MCP servers (e.g., for a personal Claude Code and a work Claude Code), you need two separate MCP server processes with two different `auth.default_profile` settings. The package does not currently support this — but you can hack it by:

```bash
# Terminal 1: work
NOTEBOOKLM_PROFILE=work nlm mcp-serve

# Terminal 2: personal
NOTEBOOKLM_PROFILE=personal nlm mcp-serve
```

(Requires `--transport http` and distinct ports.) See [[concepts/cdp-cookie-extraction]] for the transport details.

## What gets duplicated, what doesn't

| Resource | Per-profile? | Notes |
|----------|-------------|-------|
| Cookies | ✅ | isolated by Chromium profile |
| CSRF + session tokens | ✅ | parsed from the profile's session |
| Captured email | ✅ | for display in `profile list` |
| Saved browser login | ✅ | Chrome's persistent cookies |
| `config.toml` (default pointer) | ✗ single | points to ONE profile at a time |
| MCP server identity | ✗ single | always acts as the default profile |
| UI / CLI flag overrides | per-invocation | `--profile work` on any `nlm` call |

## Failure modes worth knowing

| Symptom | Cause | Fix |
|---------|-------|-----|
| `nlm login --profile work` opens browser but no Google login UI | Existing Chromium instance using the same profile dir | Quit all Chromium windows; the CLI launches a fresh dedicated profile so this rarely happens |
| `profile list` shows wrong email | Stale `auth.json` from before re-auth | Re-run `nlm login --profile <name>` |
| Two profiles show the same email | You logged into both with the same account | Delete one |
| MCP server acts as wrong account after `nlm login switch` | The MCP process cached the old profile at startup | Restart the MCP server (or use `refresh_auth` to force re-read) |

## Generalization

The pattern works for any service where:

1. Auth is browser-cookie-based (no OAuth)
2. Each user has a single identity at any moment
3. The user might want to switch identities without re-logging-in interactively

Anything CDP-driven inherits this naturally: [[entities/gemini-notebook-mcp-cli]] is the textbook case; [[entities/claude-mem]] uses a single-profile variant.

## Related

- [[concepts/cdp-cookie-extraction]] — the underlying auth primitive
- [[concepts/auth-status-semantics]] — how to surface profile health to the user
- [[entities/gemini-notebook-mcp-cli]] — the production implementation