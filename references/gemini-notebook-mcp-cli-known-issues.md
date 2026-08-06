---
title: "gemini-notebook-mcp-cli — known issues & fragility"
category: references
tags:
  - mcp
  - notebooklm
  - troubleshooting
  - google
summary: Catalog of fragility in gemini-notebook-mcp-cli: undocumented `bl` build label, cookie rotation, ~50/day free-tier rate limits, internal API drift, Chrome 136+ lockdown, Claude Desktop profile quirks.
sources:
  - https://github.com/jacob-bd/gemini-notebook-mcp-cli/blob/main/docs/KNOWN_ISSUES.md
  - https://github.com/jacob-bd/gemini-notebook-mcp-cli/blob/main/docs/AUTHENTICATION.md
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
    type: related_to
  - target: "[[concepts/cdp-cookie-extraction]]"
    type: related_to
  - target: "[[concepts/rpc-drift-hot-patch]]"
    type: related_to
  - target: "[[concepts/auth-status-semantics]]"
    type: related_to
  - target: "[[references/gemini-notebook-mcp-cli-tools]]"
    type: related_to
---

# gemini-notebook-mcp-cli — known issues & fragility

> Six classes of breakage to expect, with current mitigations and the diagnostic command for each. This catalog is **load-bearing** — the package depends on undocumented internal APIs by design, so "fragility" is the steady state, not a corner case.

## 1. Build Label (`bl`) parameter

**What it is.** A frontend version identifier required by `batchexecute` RPCs. Looks like:

```
boq_labs-tailwind-frontend_20260219.16_p2
```

**Current status (v0.3.11+).** Resolved — auto-extracted from the page during `nlm login` and during CSRF refresh. Stays current without manual intervention.

**Manual override** (rarely needed):

```bash
export NOTEBOOKLM_BL="boq_labs-tailwind-frontend_YYYYMMDD.XX_pN"
```

Resolution priority: env var > auto-extracted > hardcoded fallback.

## 2. Cookie expiration

**What it is.** Browser cookies extracted from a Chrome session have a limited lifespan.

**When it breaks** (~2-4 weeks after `nlm login`):

- `ValueError: Cookies have expired. Please re-authenticate...`
- API calls redirect to Google login page
- Auth errors on previously-working operations

**Fix — three options, in increasing order of intervention:**

```bash
# A. CLI auto-extraction (recommended — handles browser launch + login)
nlm login

# B. Chrome DevTools MCP (in-agent, fastest if you have the MCP available)
save_auth_tokens(cookies=<cookie_header>, request_body=<request_body>, request_url=<request_url>)

# C. Manual paste (fallback)
# Chrome DevTools → Network → filter "batchexecute" → click a request →
# Request Headers → copy the `cookie:` value → set NOTEBOOKLM_COOKIES env var
```

## 3. Rate limits

**What it is.** Free tier of Gemini Notebook has server-enforced usage limits.

**Current observed limits** (approximate, not officially documented):

- ~50 queries per day
- Studio content generation may have separate limits

**Symptoms:**

- API returns rate limit errors
- Operations start failing mid-session

**Mitigation:**

- Space out operations
- Create videos **sequentially** (brief auto-retries only cover transient failures; after a Studio rate-limit error, wait 1-2 minutes before retrying)
- Avoid tight polling loops
- **Poll a known Studio artifact by ID** instead of repeatedly listing the notebook
- Batch queries where the API supports it (`cross_notebook_query`, `batch` action)

The PRO / Ultra tiers have higher limits but no published quota numbers.

## 4. API instability (undocumented internal APIs)

**What it is.** The MCP uses internal, undocumented APIs that Google can change at any time without notice.

**What can break:**

- RPC IDs (e.g., `wXbhsf` for list notebooks) may be renamed
- Request/response structure may change
- New required parameters may appear
- Endpoints may be deprecated or moved

**Symptoms:**

- Parsing errors (unexpected response shape)
- `None` results from previously working operations
- New error messages from the API

**What to do when it breaks:**

1. Check if the issue is widespread (Google may have deployed changes)
2. Run with `--debug` to log `RPC IDs in response: [...]` and discover the new IDs
3. Apply `NOTEBOOKLM_RPC_OVERRIDES` env var as a hot-patch (see [[concepts/rpc-drift-hot-patch]])
4. Submit a PR with the new IDs once confirmed stable

## 5. CSRF token and session ID

**What it is.** The MCP auto-extracts CSRF token (`SNlM0e`) and session ID (`FdrFJe`) from the Gemini Notebook homepage on first use.

**When it breaks:**

- Homepage structure changes (Google deploys a new frontend)
- Tokens are per-session and must be refreshed if the page isn't accessible

**Symptoms:**

- `ValueError: Could not extract CSRF token from page`
- Debug HTML saved to `~/.notebooklm-mcp-cli/debug_page.html`

**Fix:**

1. Inspect `~/.notebooklm-mcp-cli/debug_page.html` to see what the homepage returned
2. Manually extract CSRF and session from Chrome DevTools Network tab if auto-extraction fails
3. Pass them via `save_auth_tokens(cookies=..., request_body=..., request_url=...)`

## 6. Claude Desktop profile setup

**Symptoms:**

- MCP doesn't appear in Claude Desktop after setup
- `nlm setup add claude-desktop --profile 3p` says Claude is still running even though the window was closed

**Cause.** Claude Desktop keeps separate regular and Relay AI/3P profiles. Claude or Relay AI can also rewrite its configuration while the app is open. macOS may leave a Crashpad helper process behind after the window closes — that helper is not an active Claude Desktop instance and is ignored by current `nlm` versions.

**Fix:**

1. Fully quit the selected Claude Desktop profile and stop the Relay AI launcher if it owns the 3P instance
2. Run `nlm setup add claude-desktop --profile 3p` (or `regular`)
3. Reopen the selected Claude Desktop profile and check its Developer settings

The CLI never creates a missing profile. Removal only offers profiles that contain `gemini-notebook-mcp` or a recognized legacy entry, leaving unrelated MCP servers unchanged.

## 7. Chrome 136+ remote-debugging lockdown

**What it is.** Chrome 136+ (and other Chromium-based browsers at the same version) restrict remote debugging on the **default profile** for security reasons.

**Mitigation (automatic):**

1. CLI uses dedicated profile directories (`~/.notebooklm-mcp-cli/chrome-profiles/<name>/`)
2. Adds `--remote-allow-origins=*` to the Chromium command line

No user action required. If you're adapting the [[concepts/cdp-cookie-extraction]] pattern yourself, **don't** try to attach to the user's existing default profile — you'll fail to connect.

## 8. The "auth loop" trap

**Symptoms:** Repeated `Authentication expired` errors even after `nlm login` or `refresh_auth`.

**Cause:** `NOTEBOOKLM_COOKIES` is set as an environment variable in the MCP config. This takes absolute priority over all other auth sources — `auth.json`, profile cookies, `save_auth_tokens`, and `nlm login`. When those hardcoded cookies expire, no recovery action can fix a running MCP process because the stale env var is baked into its environment.

**Fix (pick one):**

1. Update the cookie value in your MCP config with fresh cookies, then restart your AI tool
2. **Remove the `NOTEBOOKLM_COOKIES` env var** from your config entirely and use `nlm login` instead (recommended — auth recovery then works automatically)

`NOTEBOOKLM_CSRF_TOKEN` and `NOTEBOOKLM_SESSION_ID` are deprecated and auto-extracted; remove them if present. Stale values can prevent auto-refresh.

## 9. Browser-bound replay (rare)

**Symptoms:** `nlm login` succeeds, fresh cookies land on disk, but every API call still fails.

**Cause:** Google's risk engine flags the cookies as device-bound. The cookies work in the browser but fail when replayed through httpx from a different process.

**Diagnosis:**

```bash
nlm doctor auth-replay
```

This compares four lanes — saved cookies through httpx, httpx after a forced cookie rotation, cookies freshly re-extracted from a live browser (also via httpx), and an in-page CDP fetch from that same browser session. If the in-page CDP lane succeeds while httpx lanes fail, the verdict is `browser_bound_replay`.

**Fix:** Opt into the experimental CDP-RPC transport:

```bash
NOTEBOOKLM_RPC_TRANSPORT=cdp nlm notebook list
```

For MCP clients, set the same env var in the server config:

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

This runs supported form POSTs through `fetch` inside the saved browser profile. Off by default; only opt in when `auth-replay` returns `browser_bound_replay`. Uploads/downloads/artifact transfers still use the normal HTTP paths.

## Reporting issues

When filing a bug:

1. The specific tool/operation that failed
2. The error message (redact sensitive info — cookies, account email)
3. Whether the operation worked before
4. The current date (to correlate with potential Google deployments)

Attach `~/.notebooklm-mcp-cli/debug_page.html` if auto-extraction failed.

## Related

- [[entities/gemini-notebook-mcp-cli]] — package
- [[concepts/cdp-cookie-extraction]] — the auth pattern's failure modes
- [[concepts/rpc-drift-hot-patch]] — surviving undocumented-API rotations
- [[concepts/auth-status-semantics]] — distinguishing "stale" from "unverified"
- [[references/gemini-notebook-mcp-cli-tools]] — 43-tool reference