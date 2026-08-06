---
title: "CDP Cookie Extraction — Chrome DevTools Protocol as the auth bridge"
category: concepts
tags:
  - cdp
  - authentication
  - mcp
  - google
  - browser-automation
summary: When a service has no OAuth, drive a managed browser via Chrome DevTools Protocol and harvest cookies/CSRF/session from the logged-in session.
sources:
  - https://github.com/jacob-bd/gemini-notebook-mcp-cli/blob/main/docs/AUTHENTICATION.md
  - https://github.com/jacob-bd/gemini-notebook-mcp-cli/blob/main/CLAUDE.md
created: 2026-08-06
updated: 2026-08-06
tier: core
lifecycle: reviewed
lifecycle_changed: "2026-08-06"
base_confidence: 0.85
provenance:
  extracted: 0.75
  inferred: 0.20
  ambiguous: 0.05
relationships:
  - target: "[[entities/gemini-notebook-mcp-cli]]"
    type: uses
  - target: "[[concepts/multi-profile-google-auth]]"
    type: related_to
  - target: "[[concepts/auth-status-semantics]]"
    type: related_to
  - target: "[[concepts/mcp-server-protocol-quirks]]"
    type: related_to
---

# CDP Cookie Extraction — Chrome DevTools Protocol as the auth bridge

> When a service exposes no OAuth flow but does enforce cookie-based auth (Google NotebookLM, many internal admin tools, etc.), the only reliable programmatic path is **drive a real Chromium via Chrome DevTools Protocol, log in interactively once, then reuse the saved browser profile to harvest fresh cookies on every token rotation.**

## The pattern

```
┌────────────────────────────────┐
│ CLI / MCP server (headless)    │
│                                │
│  needs cookies for service X   │
└────────────────┬───────────────┘
                 │ CDP websocket
                 ↓
┌────────────────────────────────┐
│ Managed Chromium profile       │
│ (~/.cache/<app>/chrome/<name>) │
│                                │
│ - already logged into service X│
│ - cookies persist across runs  │
│ - extensions disabled          │
└────────────────────────────────┘
```

The CLI does NOT see your real browser session — it spins up a **dedicated** Chromium profile so your day-to-day browsing state, extensions, and other Google logins stay untouched.

## Why CDP and not Puppeteer/Playwright/Selenium?

| Dimension | CDP (raw) | Puppeteer | Playwright | Selenium |
|-----------|-----------|-----------|------------|----------|
| Cookie + header access via Network domain | ✅ native | ✅ via CDP | ✅ via CDP | ⚠️ requires DevTools shim |
| Persistent profile control | ✅ | ✅ | ✅ | ⚠️ |
| Multi-browser support | ⚠️ Chromium-family only | ⚠️ | ✅ Firefox/Safari/WebKit | ✅ |
| Zero extra deps | ✅ `websocket-client` is enough | ❌ large | ❌ even larger | ❌ Java |

`gemini-notebook-mcp-cli` uses raw CDP via `websocket-client` (one of the listed deps). That's deliberate — the entire auth subsystem is ~300 lines because they only need Network + Page domains.

## What gets extracted (NotebookLM case)

From one `nlm login` invocation, the CLI harvests four pieces and caches them in `profiles/<name>/auth.json`:

1. **Cookies** — `__Secure-1PSID`, `__Secure-3PSID`, `SID`, `HSID`, `SSID`, `APISID`, `SAPISID`, etc.
2. **CSRF token** (`SNlM0e`) — embedded in the homepage HTML, parsed with regex
3. **Session ID** (`FdrFJe`) — also homepage-derived
4. **Account email** — read from the account chooser / profile chip

v0.1.9+ removed the requirement to manually pass CSRF/session — they're auto-extracted on MCP startup. v0.9.3+ also auto-records the host your account lands on (`notebook.google.com` vs `notebook.google.com` post-rebrand) and routes subsequent requests there.

## The "remote debugging" trap

Chrome 136+ restricted remote debugging on the **default profile** for security. The CLI works around this automatically by:

1. Always launching with a dedicated profile directory (`chrome-profiles/<name>/`)
2. Adding `--remote-allow-origins=*` to the Chromium command line

Users don't need to do anything — but if you're adapting the pattern, **do not** try to attach to the user's existing default profile; you will fail to connect.

## Refresh strategy

Cookies last ~2-4 weeks, CSRF lasts minutes, session ID rotates per MCP init. The CLI handles this transparently:

| Token | Lifetime | Refresh mechanism |
|-------|----------|-------------------|
| Cookies | weeks | re-launch CDP against saved profile → re-extract |
| CSRF (`SNlM0e`) | minutes | re-fetch homepage → re-parse on every MCP startup |
| Session ID | per-session | re-fetch homepage → re-parse on every MCP startup |
| Build label (`bl`) | per Google deploy | re-extracted during login / CSRF refresh |

If full re-auth fails (Google login fully expired, or genuine device-bound replay where cookies fail outside the browser), `nlm doctor auth-replay` distinguishes `stale_cookies` (just re-login) from `browser_bound_replay` (switch to `NOTEBOOKLM_RPC_TRANSPORT=cdp` for browser-backed fetch).

## The experimental CDP-RPC escape hatch

When cookies alone won't authenticate (browser-bound replay), the package offers `NOTEBOOKLM_RPC_TRANSPORT=cdp` — this runs the Gemini Notebook `fetch` POSTs *inside* the saved browser session via `fetch` via CDP. The browser supplies its live cookies. Off by default; opt in only after `nlm doctor auth-replay` returns `browser_bound_replay`.

```bash
NOTEBOOKLM_RPC_TRANSPORT=cdp nlm notebook list
```

For MCP clients, add the env var to the server config:

```json
{
  "mcpServers": {
    "gemini-notebook-mcp": {
      "command": "notebooklm-mcp",
      "env": { "NOTEBOOKLM_RPC_TRANSPORT": "cdp" }
    }
  }
}
```

Uploads, downloads, and artifact file transfers still use the normal HTTP paths — only `batchexecute` RPC + notebook chat are tunneled through the browser.

## Why this pattern generalizes

The same recipe works for any internal Google product (or any other browser-only auth service) where:

1. You can drive Chromium on the user's machine
2. The user is willing to log in interactively once
3. Cookies are accepted by the backend APIs

[[entities/gemini-notebook-mcp-cli]] is the textbook example. The same pattern appears in [[entities/claude-mem]] (uses Playwright for session capture) and OpenClaw's browser manager. **It's the de facto auth pattern when OAuth isn't an option.**

## Related concepts

- [[concepts/multi-profile-google-auth]] — how to isolate N Google accounts in N managed browser profiles
- [[concepts/auth-status-semantics]] — the 5-state health vocabulary used to surface auth problems
- [[concepts/mcp-server-protocol-quirks]] — broader MCP auth landscape (API key, OAuth proxy, cookies)
- [[references/gemini-notebook-mcp-cli-known-issues]] — what to do when it breaks