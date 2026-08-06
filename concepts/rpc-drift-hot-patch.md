---
title: "RPC Drift Hot-Patch — surviving undocumented API rotations"
category: concepts
tags:
  - api-stability
  - undocumented-apis
  - resilience
  - mcp
summary: When a vendor rotates internal RPC method IDs without notice, detect drift loudly, allow env-var hot-patching of the new ID, and retry on throttling — without forcing a release.
sources:
  - https://github.com/jacob-bd/gemini-notebook-mcp-cli/blob/main/CLAUDE.md
  - https://github.com/jacob-bd/gemini-notebook-mcp-cli/blob/main/docs/KNOWN_ISSUES.md
created: 2026-08-06
updated: 2026-08-06
tier: supporting
lifecycle: reviewed
lifecycle_changed: "2026-08-06"
base_confidence: 0.80
provenance:
  extracted: 0.75
  inferred: 0.20
  ambiguous: 0.05
relationships:
  - target: "[[entities/gemini-notebook-mcp-cli]]"
    type: uses
  - target: "[[references/gemini-notebook-mcp-cli-known-issues]]"
    type: related_to
  - target: "[[concepts/cdp-cookie-extraction]]"
    type: related_to
---

# RPC Drift Hot-Patch — surviving undocumented API rotations

> When your code depends on a vendor's internal `batchexecute` RPC IDs (e.g. `wXbhsf` for "list notebooks") and Google rotates them without notice, you have three problems at once: detect the drift loudly, allow operators to fix it without a release, and degrade gracefully on transient failures. `NOTEBOOKLM_RPC_OVERRIDES` is the textbook solution.

## The failure mode

```
NOTICE: NotebookLM (internal API) rotated wXbhsf → aBcD12
        (no announcement, no version bump visible to clients)

SYMPTOM: every notebook_list call returns empty / parsing error
          / silently returns wrong shape
```

If your client silently returns an empty list, the user thinks "I have no notebooks" — a critical data-loss illusion. The first requirement is **detect drift loudly**.

## The detection: `RPCDriftError`

A correctly-designed client checks whether the response contains the RPC ID it asked for. If the server responds with **different** `wrb.fr` RPC IDs than the one requested, the client raises:

```python
class RPCDriftError(Exception):
    """The server returned different RPC IDs than requested."""
```

Not a generic exception — a typed error the calling code can catch and surface. An empty response still returns silently (no comparison points), so the operator must run with `--debug` to inspect that case.

## The discovery: `--debug` logging

With `--debug`, the client logs `RPC IDs in response: [...]`. The new ID for the call appears there. This is the operator's signal that an ID rotated. They then need a way to override.

## The hot-patch: `NOTEBOOKLM_RPC_OVERRIDES`

Env var, JSON object, mapping the client's RPC attribute name to the new ID:

```bash
export NOTEBOOKLM_RPC_OVERRIDES='{"RPC_LIST_NOTEBOOKS": "aBcD12"}'
```

Restart the MCP server (env var is read once at client init, not per call). The CLI picks it up on the next invocation automatically. **No release needed.**

The override format uses the `BaseClient` RPC attribute name (e.g., `RPC_LIST_NOTEBOOKS`), not the old ID value. This means an override stays valid even if the new ID rotates again — only the mapping changes.

## The auto-retry: throttling

`RESOURCE_EXHAUSTED` (RPC error code 8) is Google's "you've made too many calls" response. The client auto-retries these with exponential backoff — no operator action needed for transient rate-limit hits.

The broader rate-limit guidance from [[references/gemini-notebook-mcp-cli-known-issues]]:

> Poll a known Studio artifact by ID instead of repeatedly listing the notebook.
> Space out operations.
> After a Studio rate-limit error, wait 1-2 minutes before retrying.

## Why "hot-patch without release" matters

For a closed-source vendor that does not commit to API stability, the alternative to hot-patching is:

1. Vendor rotates ID → client breaks
2. Users file bug reports
3. Maintainer investigates, identifies new ID, cuts a release
4. Users `uv tool upgrade`
5. Restart MCP server

That cycle takes hours to days. With hot-patching:

1. Vendor rotates ID → `RPCDriftError` fires loudly
2. Operator (or a watchful community member) runs `--debug`, sees the new ID
3. Operator sets env var, restarts MCP → fixed in minutes
4. Maintainer files an issue / PR with the new ID for permanent fix at leisure

The release-pressure off-ramp is what makes an undocumented-API integration sustainable.

## What this pattern is and isn't

✅ **Is:**
- A typed-error-first design philosophy ("fail loudly with a name")
- An env-var escape hatch scoped to one config concern
- An auto-retry for transient throttling
- A debug-mode introspection path

❌ **Isn't:**
- A general-purpose API-stability abstraction (this is Google-specific)
- A long-term substitute for the vendor exposing a stable API
- A way to fix structural response-shape changes (only ID rotations)

## Generalization

The pattern applies to any consumer of undocumented / internal APIs:

1. **Wrap every RPC call** with a typed error for "ID mismatch"
2. **Always log** the actual IDs in debug mode
3. **Make the ID mapping configurable** via env var, JSON, or local file
4. **Auto-retry** transient errors (throttling, network) with backoff
5. **Document the override syntax** so operators can self-serve

Combined with [[concepts/auth-status-semantics]] (which surfaces upstream auth problems), this gives operators a complete survival kit for undocumented-API integrations.

## Related

- [[entities/gemini-notebook-mcp-cli]] — production implementation
- [[references/gemini-notebook-mcp-cli-known-issues]] — the broader failure catalog
- [[concepts/cdp-cookie-extraction]] — the other major fragile surface area