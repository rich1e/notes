---
title: Consolidation Report 2026-08-03
category: synthesis
tags: [maintenance, consolidation]
sources: []
summary: Auto-generated consolidation report from wiki-lint --consolidate run on 2026-08-03: 1 orphan rescue + 71 lifecycle promote + 0 tag alias (false positive)。
lifecycle: reviewed
lifecycle_reason: "auto-promoted by wiki-lint --consolidate: age>30d, confidence>0.9"
lifecycle_changed: 2026-08-03
base_confidence: 0.9
tier: peripheral
created: 2026-08-03T13:25:00Z
updated: 2026-08-03T13:25:00Z
---

# Consolidation Report — 2026-08-03

## Summary
- Pre-write snapshot: `3bcc833c6d61409ec9e4b8dbbe5627420adaadc4`(独立 git repo,21 个 dirty 文件已 commit)
- Orphan rescue: 1
- Lifecycle auto-promote (draft → reviewed): 71
- Tier demotion: 0(无候选)
- Tag alias fixes: 0(原 4 个候选为 false positive,详见末尾说明)
- Contradiction callouts: 0(无 `relationships: contradicts` 条目)

## Orphan Rescue
- `synthesis/consolidation-2026-07-30.md` — 末尾追加 "See also" 段,反链到 [[synthesis/consolidation-2026-07-26]]、[[synthesis/consolidation-2026-07-31]]、log

## Lifecycle Auto-Promote(71 页,全部 age>30d + base_confidence>0.7)

按页分类:

| 簇 | 数量 | 代表 |
|---|---|---|
| PTP | 7 | [[concepts/ptp-ieee1588]]、[[concepts/ptp-bmca]]、[[concepts/ptp-clock-types]] 等 |
| iOS / Swift | 5 | [[concepts/arc-memory-management]]、[[concepts/ios-app-architecture]]、[[concepts/swift-concurrency]] 等 |
| Zustand | 3 | [[concepts/zustand-core-architecture]]、[[concepts/zustand-middleware-system]]、[[concepts/zustand-react-integration]] |
| AI / LLM | ~12 | [[concepts/claude-mem-memory-architecture]]、[[concepts/claude-code-hooks-lifecycle]]、[[concepts/llm-training-pipeline]] 等 |
| Design.md / Stitch | ~10 | [[concepts/design-md-format-spec]]、[[concepts/design-md-token-interpolation]]、[[concepts/design-md-anti-patterns]] 等 |
| chezmoi | ~7 | [[concepts/chezmoi-templating]]、[[concepts/chezmoi-attribute-prefixes]]、chezmoi-* 等 |
| n8n / workflow | ~4 | [[concepts/workflow-automation-platform]]、[[concepts/fair-code-license]] 等 |
| Misc concepts/refs/skills | ~23 | 杂项 |

每个页都加了 `lifecycle_changed: 2026-08-03` + `lifecycle_reason: "auto-promoted by wiki-lint --consolidate: age>30d, confidence>0.7"`,并 bump `updated` 时间戳。

## Tier Demotion
无候选(0 个 `tier: supporting` + 0 incoming + > 90 天 stale 的页面)。

## Tag Alias Fixes — 0(原计划 4 全为 false positive)

dry-run 检测到 4 个候选含 `frontend` 字面 → `f2e`。但实际看 frontmatter 后:

- `concepts/browser-process-model.md` → tags: `browser, performance`(无 frontend)
- `concepts/claude-code-hooks-lifecycle.md` → tags: `claude-code, hooks, ai-tool`(无 frontend)
- `concepts/javascript-event-loop.md` → tags: `javascript, web`(无 frontend)
- `projects/jrfed-zaxd-mediation-tool/references/source-tree.md` → tags: `chrome-extension, source-tree`(无 frontend)

**原因**:dry-run 用 `\bfrontend\b` 匹配 body 内容,命中 `[[concepts/frontend-storage-cache]]` 之类的 wikilink,而非真 tags 字段。**这是 dry-run 脚本的 false positive**,Action 5 已取消执行,无文件被改。

## Contradiction Callouts
无(vault 中无 `relationships: contradicts` 条目)。

## 不做的事
- 不合并任何页(由 `wiki-dedup` 处理)
- 不改任何 `base_confidence`(由 `wiki-lint --check` + `obsidian-wiki trust-check` 处理)
- 不自动 demote `tier: core` 页(那些是人工设置)
- 不删文件,只追加/修改 frontmatter

## 回滚
如需回滚所有本次改动:

```sh
cd /Users/rich1e/workspace/code/notes
git reset --hard 3bcc833c6d61409ec9e4b8dbbe5627420adaadc4
```