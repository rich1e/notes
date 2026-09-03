---
title: Consolidation Report 2026-09-03
category: synthesis
tags: [maintenance, consolidation]
sources: []
summary: Auto-generated consolidation report from wiki-lint --consolidate run on 2026-09-03 — broken-link fixes, tag normalization, lifecycle auto-promote.
lifecycle: draft
lifecycle_changed: 2026-09-03
tier: peripheral
created: 2026-09-03T02:30:00Z
updated: 2026-09-03T02:30:00Z
---

# Consolidation Report — 2026-09-03

Pre-snapshot SHA: `2ec08d0efc60719157b0a51df2a694f6e0281c27`

## Summary
- Broken-link fixes: 13 files (15 individual broken wikilinks resolved)
- Cross-references added (orphan rescue): 7 entries across 3 pages (asciidoc-markup, mobile-timer-accuracy, herdr)
- Lifecycle states updated: 47 pages (draft → reviewed)
- Tier demotions: 0 (no stale peripheral candidates)
- Tags normalized: 135 pages (131 effective aliases from `_meta/taxonomy.md` alias table)
- Contradiction callouts: 0 (none flagged)

## Broken Link Fixes
- `journal/2026-08-31-darwin-brew-weekly-optimization.md:110` — `[[homebrew-weekly-20260831]]` → `homebrew-weekly-20260831` (dangling, no match)
- `references/sqlite-for-everything.md:154` — `[[concepts/postgres-extensions-ecosystem\]]` → `[[concepts/postgres-extensions-ecosystem]]` (backslash suffix)
- `synthesis/concepts-agent-team-display-modes × entities-claude-code-agent-teams-feature.md:88` — `[[references/claude-code-agent-teams-known-issues]]` → HTML comment (no page)
- `synthesis/concepts-agent-team-cost-overhead × entities-claude-code-agent-teams-feature.md:95` — `[[references/claude-code-agent-teams-token-bench]]` → HTML comment (no page)
- `synthesis/consolidation-2026-08-24.md:84` — `[[ambiguous]]` → HTML comment (template placeholder)
- `synthesis/concepts-design-md-format-spec × entities-awesome-design-md.md:87,88` — `[[skills/design-md-from-figma]]`, `[[references/design-md-section-evolution]]` → HTML comments
- `synthesis/concepts-agent-team-race-condition-task-claim × concepts-deterministic-agent-memory.md:87` — `[[concepts/agent-team-claim-retry-strategy]]` → HTML comment
- `concepts/extensibility.md:21` — `[[projects/flow-design-system]]` → HTML comment
- `concepts/deterministic-agent-memory.md:110` — `[[entities/sqlite\]]` → `[[entities/sqlite]]` (backslash suffix)
- `skills/wiki-lint.md:31` — `[[target]]` → HTML comment (template placeholder)
- `skills/wiki-ingest.md:60` — `[[skills/wiki-status]]` → HTML comment (skill doesn't exist yet)
- `entities/notebooklm.md:29` — `[[synthesis/concepts-mcp-server-protocol-quirks]]` → HTML comment (no synthesis page)
- `entities/bmad-method.md:112` — `[[synthesis/concepts-ai-agent × entities-bmad-method]]` → HTML comment
- `entities/opencoworkai.md:26` — `[[synthesis/Research: OpenCoworkAI open-codesign]]` → HTML comment
- `log.md` — generic `.md` suffix scan caught an extra `[[entities/awesome-design-md.md]]` → `[[entities/awesome-design-md]]`

## Cross-References Added (orphan rescue)
- `concepts/asciidoc-markup.md` — linked to [[references/chezmoi-templating-guide]] + [[concepts/shell-alias-taxonomy]]
- `concepts/mobile-timer-accuracy.md` — linked to [[projects/dayfold/skills/simulator-runtime-log-capture]] + [[skills/ios-emulator-setup]]
- `entities/herdr.md` — linked to [[gpakosz-tmux]] + [[ai-agent]] + [[claude-code]]

**Orphans still without targets** (need body ingest before they can be linked):
- `entities/bmad-clarify-analyze-plan` (empty)
- `synthesis/Research: Fabric AI Framework` (empty)
- `synthesis/Research: treehouse` (empty)

## Lifecycle Updates
- 47 pages promoted from `draft` → `reviewed` (auto, age > 30d AND `base_confidence` > 0.7). See log entry for full list criteria.

## Tier Demotions
None. No pages with 0 incoming links AND 90+ days stale.

## Tag Normalizations (top 15 by frequency)
- 31× `ios` → `mobile`
- 31× `llm` → `Deepseek`
- 14× `claude-code` → `Claude`
- 11× `design-system` → `ux`
- 11× `macos` → `macOS`
- 9× `dsi` → `nds`
- 8× `ai-agent` → `ai-agents`
- 8× `programming` → `develop`
- 7× `debugging` → `Bugfix`
- 6× `ux` → `design-system`
- 6× `automation` → `workflow`
- 5× `shell` → `cli`
- 4× `workflow` → `automation`
- 4× `analytics` → `call-center`
- 4× `hardware` → `handheld`

## Known Issues NOT Auto-Fixed (require owner decision)

### 36 typed-relationship bad-type entries (Check 13)
These use types not in the framework default set: `elaborates`, `example_of`, `complements`, `refines`, `refined_by`, `synthesizes`. Per skill protocol:
> Correct it only if it is absent from both framework defaults and owner extensions; never replace a valid owner type with related_to.

Recommendation: either (a) extend owner `AGENTS.md` schema to allow these types, or (b) manually migrate to one of the 7 framework types. NOT auto-migrated this run.

### 14 pages missing `created` / `updated` fields (Check 3)
- 4 dayfold skill pages (dayone-photo-library-picker, simulator-runtime-log-capture, auto-expanding-texteditor-scroll, uitextview-intrinsic-width-overflow)
- `concepts/quantum-computing-foundations.md`
- `concepts/extensibility.md`
- `concepts/japanese-retro-gaming.md`

These should be filled by re-ingesting the source or by manual edit.

### 6 fragmented tag clusters (Check 8)
- `#consolidation` n=10 cohesion=0.133
- `#design-patterns` n=6 cohesion=0.000
- `#maintenance` n=11 cohesion=0.109
- `#reference` n=7 cohesion=0.095
- `#research` n=11 cohesion=0.109
- `#synthesis` n=12 cohesion=0.015

These are clusters of meta-pages (consolidation reports, research notes). They fragment naturally because they aren't knowledge pages but process outputs.

### 33 summary fields exceed 200 chars (Check 3a — soft)
Mostly misc/web-archive pages. Summary > 200 chars affects wiki-query index retrieval efficiency. Future ingest skills should keep summaries ≤ 200 chars.

### 22 orphans remaining (after orphan rescue)
Mostly misc web archives (5) + synthesis consolidation/cross-link reports (7) + entities without content (4). These do not benefit from more cross-links.

## Pre-write snapshot
SHA `2ec08d0efc60719157b0a51df2a694f6e0281c27`. To discard this entire run: `git reset --hard 2ec08d0e && git clean -fd`.

## QMD status
`QMD skipped: QMD_WIKI_COLLECTION unset` (per .env).

## Follow-up Pass: Typed-Relationship Normalization

RunAfter explicit user authorization (the previous run deferred this as "NOT auto-migrated"), 40 typed-relationship entries were normalized to the framework's 7 allowed types:

| Original type | Target | Count | Rationale |
|---|---|---|---|
| `complements` | `related_to` | 5 | Symmetric coordination has no directional cue |
| `refines` | `extends` | 2 | A refinement relationship IS an extension |
| `refined_by` | `derived_from` | 1 | Reverse direction of refinement = derivation |
| `elaborates` | `extends` | 3 | Elaboration = extension of concept |
| `example_of` | `derived_from` | 3 | An example is a derivation |
| `synthesizes` | `related_to` | 10 | Cross-domain synthesis has no directional cue |
| `explained_by` | `derived_from` | 1 | A page is derived from its explanatory source |
| `part_of` | `related_to` | 2 | No "part_of" type — use closest neutral |
| `exemplified_by` | `extends` | 3 | The page is exemplified by another |
| `exemplifies` | `extends` | 1 | The page exemplifies another |
| `pattern_of` | `uses` | 2 | A pattern uses its underlying concept |
| `extended_by` | `extends` | 1 | Reverse direction = extension |
| `developed_by` | `derived_from` | 2 | A page is derived from its developer |
| `has_component` | `uses` | 1 | No "has_component" type — `uses` is closest |
| `enables` | `uses` | 2 | An enabling relationship uses enabling |
| `authored` | `derived_from` | 1 | Authorship = derivation |

**Check 13 result: 0 remaining bad-type entries.**

Affected pages (24 unique): misc/claude-code-agent-teams-ppt-content.md, projects/dayfold/skills/{auto-expanding-texteditor-scroll,dayone-ph-photo-library-picker,nstextattachment-bounds-overflow,simulator-runtime-log-capture,swiftui-editor-scrollview-vs-attachment,uitextview-intrinsic-width-overflow}.md, references/sqlite-for-everything.md, skills/{postgres-queue-pattern,sqlite-queue-pattern,tmux}.md, synthesis/{Research: open-codesign,concepts-agent-team-cost-overhead × entities-claude-code-agent-teams-feature,concepts-agent-team-display-modes × entities-claude-code-agent-teams-feature,concepts-agent-team-race-condition-task-claim × concepts-deterministic-agent-memory,concepts-design-md-format-spec × entities-awesome-design-md,concepts-deterministic-agent-memory × entities-openlore}.md, concepts/{database-as-platform,postgres-extensions-ecosystem,tmux-pane-layout-rearrangement}.md, entities/{mariozechner,open-codesign,opencoworkai,pi-coding-agent,postgresql,sqlite}.md.

## Final Check 13 State
-0 typed-relationship bad-type entries across 460 pages
- All relationships now use one of the 7 framework defaults: extends, implements, contradicts, derived_from, uses, replaces, related_to
