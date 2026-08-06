---
title: "NotebookLM / Gemini Notebook — Google's AI notebook product"
category: entities
tags:
  - google
  - notebooklm
  - ai-product
  - rebranded
summary: Google NotebookLM was rebranded to "Gemini Notebook" in 2025; the v0.9.3+ client auto-detects which host your account lands on and routes requests there per-profile.
sources:
  - https://github.com/jacob-bd/gemini-notebook-mcp-cli/blob/main/docs/AUTHENTICATION.md
created: 2026-08-06
updated: 2026-08-06
tier: supporting
lifecycle: draft
lifecycle_changed: "2026-08-06"
base_confidence: 0.70
provenance:
  extracted: 0.60
  inferred: 0.30
  ambiguous: 0.10
relationships:
  - target: "[[entities/gemini-notebook-mcp-cli]]"
    type: related_to
  - target: "[[concepts/cdp-cookie-extraction]]"
    type: related_to
---

# NotebookLM / Gemini Notebook — Google's AI notebook product

## The rebrand

Google is rolling out a rebrand of Google NotebookLM that redirects some signed-in accounts to `notebook.google.com` instead of `notebook.google.com`. As of v0.9.3 of [[entities/gemini-notebook-mcp-cli]], this is **handled automatically**: `nlm login` records whichever host your account actually lands on (per-profile, in `metadata.json`), and every CLI/MCP request is routed to that host afterward.

**Resolution order if you need to override it manually:**

1. `NOTEBOOKLM_BASE_URL` env var, if set (also used for Enterprise / Workspace)
2. The host your account last signed in on (auto-detected)
3. The default `https://notebook.google.com`

## What the product is

Google's AI notebook tool — upload documents, videos, web pages, Google Drive files; chat with them; generate studio artifacts (podcasts, videos, mind maps, slides, infographics, reports, flashcards, quizzes, data tables). Free tier exists (~50 queries/day); Google AI Ultra tier ($249/mo) gives higher limits and may have additional capabilities.

**No public API.** All programmatic access — including the official-looking tools in Claude Code / Cursor / Gemini CLI — goes through undocumented internal `batchexecute` RPCs with rotated method IDs (e.g., `wXbhsf`). See [[concepts/rpc-drift-hot-patch]] for how clients survive that.

## Hosts

| Host | Audience | Notes |
|------|----------|-------|
| `https://notebook.google.com` | Consumer accounts | Default post-rebrand for most users |
| `https://notebooklm.cloud.google.com` | Workspace / Enterprise | Custom URL — set `NOTEBOOKLM_BASE_URL` |

The rebrand is partial and progressive: existing personal accounts may still land on either host depending on rollout state. The client tracks this per-profile so different users on the same machine can land on different hosts without conflict.

## Why the rebrand matters

Beyond branding, the rebrand signals Google's intent to position the product closer to the Gemini brand — suggesting deeper integration with the Gemini API surface over time. This is **speculative** ^[inferred] but consistent with Google's broader Gemini-everywhere strategy. Programmatic clients that hard-code `notebooklm.google.com` will silently break for users whose accounts have rolled over; the [[entities/gemini-notebook-mcp-cli]] `metadata.json` per-profile host detection is the correct mitigation pattern.

## Related

- [[entities/gemini-notebook-mcp-cli]] — production client, handles the rebrand
- [[concepts/cdp-cookie-extraction]] — auth bridge (Google does not offer OAuth for NotebookLM)
- [[references/gemini-notebook-mcp-cli-known-issues]] — failure modes, including rebrand fallout