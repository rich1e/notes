---
title: "Auth-Status Semantics — 5-state health vocabulary for browser-cookie auth"
category: concepts
tags:
  - authentication
  - health-checks
  - mcp
  - pattern
summary: A 5-state auth health vocabulary (configured / not_configured / stale / unverified / error) that distinguishes "creds bad" from "monitoring can't tell", so users don't get false re-auth prompts.
sources:
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
    type: uses
  - target: "[[concepts/cdp-cookie-extraction]]"
    type: related_to
  - target: "[[concepts/multi-profile-google-auth]]"
    type: related_to
---

# Auth-Status Semantics — 5-state health vocabulary for browser-cookie auth

> Reporting "auth is broken" or "auth is fine" is too coarse. Browser-cookie auth can fail in five distinct ways — and the action you should take depends on which. The 5-state vocabulary (`configured` / `not_configured` / `stale` / `unverified` / `error`) distinguishes "credentials bad" from "monitoring can't tell", so AI agents don't nag users with false re-auth prompts.

## The 5 states

| State | Meaning | User action |
|-------|---------|-------------|
| `configured` | Live check passed. Credentials are good. | Nothing. |
| `not_configured` | No credentials stored at all (first run). | Run `nlm login`. |
| `stale` | Credentials known-bad: redirected to `accounts.google.com`, on-disk profile failed to load, or last successful validation is older than 7 days. | Run `nlm login` to refresh. Subsequent API calls will fail. |
| `unverified` | Live check could not complete (network timeout, DNS failure, proxy block, non-200 HTTP). Cached credentials on disk are still intact and may work. | **Retry later.** Do not assume the user needs to re-auth. |
| `error` | Unexpected exception inside the check itself. | File a bug with the traceback. |

## Why the distinction matters

The classic naive check is "can I make one API call right now?". If yes → "ok". If no → "broken, re-auth please!".

But there are several "no" reasons:

1. **Cookies genuinely expired** → must re-auth
2. **Your network is down** → no amount of re-auth will help; retry later
3. **Google's risk engine blocked your IP** → not the user's fault at all
4. **Health-check itself crashed** → bug, not auth problem

A binary "broken / ok" loses this. Users get nagged to re-auth when their network is the problem. Worse, AI agents in a loop will keep prompting for re-auth every few turns, eating context and annoying the user.

## The probe structure

The `AuthHealthChecker` is **multi-probe** — it doesn't trust one signal:

1. **Homepage fetch probe** — GET `https://notebook.google.com/`, check if the response contains a session-valid marker (NOT a redirect to `accounts.google.com`)
2. **API fallback probe** — try a lightweight authenticated RPC (e.g., notebook list) and check for 401/403
3. **On-disk validation** — verify `auth.json` exists, is readable, contains expected fields (cookies, CSRF, session ID, email)
4. **Last-validated timestamp** — reject profiles older than the 7-day heuristic

Each probe has different failure modes. Combining them into a single state requires reasoning:

- All green → `configured`
- Probe 4 stale + probe 1 green → `configured` (heuristic override; the live check is more authoritative than the 7-day clock)
- Probe 1 redirected to login → `stale` (cookies known-bad)
- Probe 1 timed out + probes 2/3 OK → `unverified` (network problem, credentials probably fine)
- Any probe raised an exception → `error`

## Caching: 30-second TTL with mtime bypass

The `server_info` tool result is cached for 30 seconds (the checker's `CACHE_TTL`). On every subsequent call, the checker checks if any auth file on disk has been rewritten (mtime check); if so, it bypasses the cache. This means an external `nlm login` is reflected in the next `server_info` call without waiting for the TTL.

`nlm login --check` is always live (no cache) so users can confirm a fresh re-auth.

## Implications for AI agents

**Critical rule for tool-using agents:**

> If `auth_status = "stale"`, prompt the user to re-authenticate.
> If `auth_status = "unverified"` while recent operations are succeeding, **treat it as a transient monitoring failure and continue**. Re-auth is not required.

A naive agent that treats `unverified` as "stale" will loop the user into "please log in again, please log in again, please log in again" while their network is the actual problem. The whole point of the 5-state vocabulary is to give agents enough signal to act correctly.

## Generalization

The same 5-state pattern works for any auth subsystem that probes an external service:

| State | When |
|-------|------|
| `configured` | Probe confirms valid session |
| `not_configured` | No credentials on disk at all |
| `stale` | Probe confirms invalid session |
| `unverified` | Probe can't reach the service |
| `error` | Probe itself crashed |

The `unverified` state is the load-bearing one — it's what makes a binary health check into a useful diagnostic. Don't drop it from your vocabulary just because "we don't usually have network problems".

## Related

- [[concepts/cdp-cookie-extraction]] — the underlying CDP auth mechanism
- [[concepts/multi-profile-google-auth]] — how profiles interact with health checks
- [[entities/gemini-notebook-mcp-cli]] — production implementation