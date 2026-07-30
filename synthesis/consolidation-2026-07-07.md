---
title: Consolidation Report 2026-07-07
category: synthesis
tags: [maintenance, consolidation]
sources: []
summary: Auto-generated consolidation report from wiki-lint --consolidate run on 2026-07-07. Fixed 2 backslash artifacts in PTP page and added 1 cross-reference to rescue orphan chapter1 page.
base_confidence: 0.7
lifecycle: draft
lifecycle_changed: 2026-07-07
tier: peripheral
created: 2026-07-07T14:30:00Z
updated: 2026-07-07T14:30:00Z
---

# Consolidation Report — 2026-07-07

## Summary
- Broken links fixed: 2
- Cross-references added: 1
- Lifecycle states updated: 0
- Tier demotions: 0
- Tags normalized: 0
- Contradiction callouts added: 0
- Orphans remaining: 9 (down from 10; chapter1 rescued)

## Broken Link Fixes
- `concepts/ptp-message-types.md:51` — `[[concepts/ptp-bmca|BMCA]]` → `[[concepts/ptp-bmca|BMCA]]`
- `concepts/ptp-message-types.md:52` — `[[concepts/ptp-tlv-extension|TLV]]` → `[[concepts/ptp-tlv-extension|TLV]]`

Note: 13 other "broken" wikilinks the lint reported were false positives — they were already valid `page` form and the targets all resolve. The two fixed above had a stray `\` before `|` that needed stripping.

## Cross-References Added (orphan rescue)
- `journal/fire-emblem-mystery-chapter1` — now linked from: `journal/fire-emblem-new-mystery-prologue` (added "**下一章 →**" pointer)

## Lifecycle Updates
- None

## Tier Demotions
- None (no pages with 0 incoming links AND > 90 days stale)

## Tag Normalizations
- None (no alias matches in current frontmatter against `_meta/taxonomy.md`)

## Contradiction Callouts
- None (no `relationships: contradicts` blocks in the vault)

## Remaining Orphans (9)
Pages with zero incoming wikilinks. All created 2026-07-01..07 — natural state for new pages, awaiting `/cross-linker` run:

- `concepts/llm-speculative-decoding`
- `concepts/mobile-timer-accuracy`
- `concepts/asciidoc-markup`
- `concepts/animation-easing-functions`
- `skills/hackintosh-mini-build`
- `skills/ios-data-persistence` (incoming masked by alias-form wikilink in ios17 book table)
- `references/mechanical-watch-mechanics`
- `projects/trek/concepts/architecture-overview`
- `projects/jrfed-zaxd-mediation-tool/references/source-tree`

## Notes
- Fragmented tag cluster `#networking` (6 pages, cohesion 0.13) — still flagged, not auto-fixed by --consolidate; defer to `/cross-linker`
- Index drift: `index.md` lists 100 entries vs 71 actual pages — defer to `/daily-update`
- QMD refresh: skipped (QMD_WIKI_COLLECTION unset per config)

## 相关

- [[animation-easing-functions]] — animation-easing-functions
## 相关页面

- [[synthesis/consolidation-2026-07-23.md]]
