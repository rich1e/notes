---
title: "gemini-notebook-mcp-cli — 43-tool reference card"
category: references
tags:
  - mcp
  - notebooklm
  - reference
  - cli
summary: Complete inventory of the 43 tools exposed by gemini-notebook-mcp-cli v0.9.x, grouped by domain, with their CLI command equivalents.
sources:
  - https://github.com/jacob-bd/gemini-notebook-mcp-cli/blob/main/docs/MCP_GUIDE.md
  - https://github.com/jacob-bd/gemini-notebook-mcp-cli/blob/main/docs/CLI_GUIDE.md
created: 2026-08-06
updated: 2026-08-06
tier: supporting
lifecycle: reviewed
lifecycle_changed: "2026-08-06"
base_confidence: 0.90
provenance:
  extracted: 0.90
  inferred: 0.05
  ambiguous: 0.05
relationships:
  - target: "[[entities/gemini-notebook-mcp-cli]]"
    type: related_to
  - target: "[[skills/gemini-notebook-mcp-cli-setup]]"
    type: related_to
---

# gemini-notebook-mcp-cli — 43-tool reference card

> Complete inventory of the 43 tools exposed by gemini-notebook-mcp-cli v0.9.x, grouped by domain. Each row maps to a CLI command via `nlm <verb> ...` (noun-first or verb-first style both work).

## Notebooks (6 tools, group `notebooks_read` + `notebooks_manage`)

| Tool | Purpose | CLI equivalent |
|------|---------|----------------|
| `notebook_list` | List all notebooks | `nlm notebook list` |
| `notebook_create` | Create new notebook | `nlm notebook create "Title"` |
| `notebook_get` | Get notebook details + sources | `nlm notebook get <id>` |
| `notebook_describe` | AI summary + suggested topics | `nlm notebook describe <id>` |
| `notebook_rename` | Rename a notebook | `nlm notebook rename <id> "New"` |
| `notebook_delete` | Delete notebook ⚠ requires `confirm=True` | `nlm notebook delete <id> --confirm` |

## Sources (7 tools, group `sources_read` + `sources_manage`)

| Tool | Purpose | CLI equivalent |
|------|---------|----------------|
| `source_add` | **Unified** — add URL, text, file, or Drive source | `nlm source add <notebook> --url/--text/--file/--drive` |
| `source_list_drive` | List sources with Drive freshness status; `skip_freshness=True` for speed | `nlm source list <notebook>` |
| `source_sync_drive` | Sync stale Drive sources ⚠ requires `confirm=True` | `nlm source sync <notebook> --confirm` |
| `source_delete` | Delete source ⚠ requires `confirm=True` | `nlm source delete <source-id> --confirm` |
| `source_describe` | AI summary + keyword chips | `nlm source describe <source-id>` |
| `source_get_content` | Raw text content (no AI processing); supports `wait` / `wait_timeout` / `poll_interval`; returns `download_url` on HTTP transport | `nlm source get <source-id>` |
| `source_rename` | Rename a source in a notebook | `nlm source rename <source-id> "New"` |

## Querying (4 tools, group `chat` + `query_multi`)

| Tool | Purpose | CLI equivalent |
|------|---------|----------------|
| `notebook_query` | Ask AI about sources in notebook | `nlm notebook query <id> "question"` |
| `notebook_query_start` | Start a query asynchronously (for large notebooks that may timeout) | `nlm notebook query --async <id> "question"` |
| `notebook_query_status` | Poll an async query | `nlm notebook query --status <query-id>` |
| `chat_configure` | Set chat goal + response length | `nlm chat configure <id> --goal ...` |

## Chat sessions (3 tools, group `chat`)

| Tool | Purpose | CLI equivalent |
|------|---------|----------------|
| `chat_list` | List chat sessions for a notebook | `nlm chats list <id>` |
| `chat_get` | Full transcript (defaults to latest session) | `nlm chats get <id> [session-id]` |
| `chat_export` | Export chat transcript to Markdown or JSON | `nlm chats export <id> [session-id]` |

## Studio content creation (4 tools, group `studio`)

| Tool | Purpose | CLI equivalent |
|------|---------|----------------|
| `studio_create` | **Unified** — create any artifact type | `nlm studio create / nlm audio create / nlm video create / ...` |
| `studio_status` | Check generation progress (paginated, default 20) | `nlm studio status <id>` |
| `studio_delete` | Delete artifact ⚠ requires `confirm=True` | `nlm studio delete <id> <artifact> --confirm` |
| `studio_revise` | Revise individual slides in an existing deck ⚠ requires `confirm=True` | `nlm slides revise <artifact> --slide 'N instruction'` |

**`studio_create` artifact types:** `audio` (deep_dive / brief / critique / debate), `video` (explainer / brief / cinematic / short), `report` (Briefing Doc / Study Guide / Blog Post), `quiz`, `flashcards`, `mind_map`, `slide_deck`, `infographic`, `data_table`.

## Downloads (2 tools, group `notebooks_read`)

| Tool | Purpose | CLI equivalent |
|------|---------|----------------|
| `download_artifact` | **Unified** — download any artifact type | `nlm download audio/video/report/mind-map/... <id>` |
| `download_all_artifacts` | Download every completed artifact of one notebook — or every notebook with `all_notebooks=True` | `nlm download all <id>` / `nlm download all --all-notebooks` |

## Exports (1 tool, group `notebooks_read`)

| Tool | Purpose |
|------|---------|
| `export_artifact` | Export Data Tables → Google Sheets, Reports → Google Docs |

## Research (3 tools, group `research`)

| Tool | Purpose | CLI equivalent |
|------|---------|----------------|
| `research_start` | Start web or Drive research (fast ~30s/10 sources, deep ~5min/40 sources) | `nlm research start "query"` |
| `research_status` | Poll research progress; `auto_import=True` does start→poll→import in one call | `nlm research status <id>` |
| `research_import` | Import discovered sources; supports `cited_only` for deep research and configurable `timeout` | `nlm research import <id> <task-id>` |

## Notes (1 unified tool, group `notes`)

| Tool | Purpose |
|------|---------|
| `note` | **Unified** — manage notes (action: `list`, `create`, `update`, `delete`) |

Actions: `note(notebook_id, action="list"|"create"|"update"|"delete", ...)`. The `delete` action requires `confirm=True`.

## Labels (1 tool, group `organization`)

| Tool | Purpose |
|------|---------|
| `label` | **Unified** — manage source labels (action: `auto`, `list`, `reorganize`, `create`, `rename`, `set_emoji`, `move_source`, `delete`) |

Auto-labeling requires 5+ sources. `reorganize` can target unlabeled-only (`unlabeled_only=True`) or replace all (`confirm=True`).

## Sharing (4 tools, group `sharing`)

| Tool | Purpose |
|------|---------|
| `notebook_share_status` | Get sharing settings + collaborators |
| `notebook_share_public` | Enable / disable public link (`is_public=True|False`) |
| `notebook_share_invite` | Invite one collaborator by email (role defaults to `viewer`) |
| `notebook_share_batch` | Invite multiple collaborators in one call |

## Auth (2 tools, group `auth`)

| Tool | Purpose |
|------|---------|
| `refresh_auth` | Reload auth tokens from disk; runs headless auth if saved profile is present |
| `save_auth_tokens` | Save cookies via Chrome DevTools MCP — FALLBACK only (prefer `nlm login`) |

## Server (1 tool, group `server`)

| Tool | Purpose |
|------|---------|
| `server_info` | Get version, check PyPI for updates, report `auth_status` |

## Batch & cross-notebook (2 tools, group `automation`)

| Tool | Purpose |
|------|---------|
| `batch` | **Unified** — batch ops across multiple notebooks (action: `query`, `add_source`, `create`, `delete`, `studio`) |
| `cross_notebook_query` | Query multiple notebooks, get aggregated answers with per-notebook citations |

**`batch` actions:** `query`, `add_source`, `create`, `delete`, `studio`. Can target by notebook names, tags, or `all=True`.

## Pipelines (1 tool, group `automation`)

| Tool | Purpose |
|------|---------|
| `pipeline` | **Unified** — list or run multi-step workflows (action: `list`, `run`) |

**Built-in pipelines:** `ingest-and-podcast`, `research-and-report`, `multi-format`. Custom YAML pipelines go in `~/.notebooklm-mcp-cli/pipelines/`.

## Tags & smart select (1 tool, group `organization`)

| Tool | Purpose |
|------|---------|
| `tag` | **Unified** — tag notebooks and find relevant ones (action: `add`, `remove`, `list`, `select`) |

`select` finds notebooks by tag matching — useful for grouping queries across topics.

## Group summary

| Group | Tools | Hide to reduce context |
|-------|-------|------------------------|
| `notebooks_read` | 2 | rarely needed alone |
| `notebooks_manage` | 4 | safe to hide for read-only users |
| `sources_read` | 3 | keep for inspection workflows |
| `sources_manage` | 4 | safe to hide for read-only users |
| `chat` | 5 | keep unless using API instead |
| `query_multi` | 2 | hide for single-notebook use |
| `organization` | 2 | hide if you don't tag |
| `automation` | 3 | hide for interactive use |
| `notes` | 1 | hide for read-only |
| `auth` | 2 | keep for self-recovery |
| `server` | 1 | keep — small |
| `sharing` | 4 | hide for solo use |
| `research` | 3 | hide if you don't research |
| `studio` | 4 | hide for query-only users |

`NOTEBOOKLM_DISABLED_GROUPS`, `NOTEBOOKLM_DISABLED_TOOLS`, and `NOTEBOOKLM_ENABLED_TOOLS` are resolved in that order; later wins. Unknown group names are silently ignored.

## Related

- [[entities/gemini-notebook-mcp-cli]] — the package itself
- [[skills/gemini-notebook-mcp-cli-setup]] — install + setup recipe
- [[references/gemini-notebook-mcp-cli-known-issues]] — failure catalog
- [[concepts/mcp-multi-tool-installer]] — the `nlm setup add <client>` pattern for wiring this CLI's MCP server into 7+ AI tools