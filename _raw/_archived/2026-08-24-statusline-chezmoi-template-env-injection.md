---
title: "Statusline env-injected chezmoi templates break API auth"
date: 2026-08-24
tags: [claude-code, statusline, chezmoi, macos-keychain, gotcha]
summary: "If a shell source file exports a chezmoi `{{ keyring ... }}` template that hasn't been rendered, Claude Code statusline injects the literal template string as an env var, which then fails the upstream API auth (e.g. MINIMAX 1004) and falls through to `unavailable`."
project: null
base_confidence: 0.85
provenance:
  extracted: 0.9
  inferred: 0.1
lifecycle_changed: 2026-08-24
sources:
  - "rich1e session (2026-08-24)"
---

## Finding

`statusline.sh` reads `${MINIMAX_API_KEY:-}` from the environment first, falls back to the macOS keychain only when that env var is empty. When `~/.zsh-extend.sh` exports keys via chezmoi templates (`export MINIMAX_API_KEY="{{ keyring "minimax-api-key" "rich1e" }}"`) **and the file hasn't been rendered by `chezmoi apply`**, the literal 126-byte template string ends up in the statusline subshell's environment and is used as the Bearer token. The upstream API (`https://www.minimaxi.com/v1/token_plan/remains`) returns HTTP 200 with `base_resp.status_code: 1004` ("login fail: Please carry the API secret key"). The statusline check on `status_code == 0` then avoids caching, `model_remains` is empty, and the panel shows `MINIMAX │ unavailable`.

## Reproduction (key dimensions only, no secret bytes)

| Branch | Resulting "key" length | API `base_resp.status_code` |
|---|---|---|
| env from unrendered template | ~22 bytes (template fragment) | **1004** login fail |
| keychain fallback after stripping `go-keyring-base64:` + base64 -d | full real key | **0** success |

The template-vs-decoded asymmetry is the smoking gun. The statusline trusts env over keychain, so as long as the unrendered template is in env, the bug is silent.

## Fix shape (already applied to `/Users/rich1e/.claude/statusline.sh`)

Add a guard that resets the env value when it looks like an unrendered chezmoi template, so the existing keychain fallback path takes over:

```bash
# If MINIMAX_API_KEY was injected by sourcing zsh-extend.sh but the file
# wasn't rendered by chezmoi, the literal `{{ keyring ... }}` template
# ends up in env. Treat it as missing and fall through to keychain.
if [ -n "$minimax_api_key_value" ] \
  && printf '%s' "$minimax_api_key_value" | grep -q "{{"; then
  minimax_api_key_value=""
fi
```

The `grep -q "{{"` heuristic only matches literal double-braces, so a real key with curly braces somewhere in its bytes (very unlikely for an API token) wouldn't trigger the reset.

## Generalization

The same pattern can break any statusline that reads a secret via env-first + keychain-fallback. The fix isn't "render chezmoi" (which is the clean long-term fix) — that path is gated by the user running `chezmoi apply`, and the statusline needs to survive that lag. Defense-in-depth belongs in the statusline itself: when the env value is obviously not a usable secret (contains `{{`, has wrong length, has a known wrong prefix), fail closed to the fallback.

## Related

- [[claude-code-statusline]]
- [[chezmoi-keyring-template]]
- [[macos-keychain-getBase64Key]]
