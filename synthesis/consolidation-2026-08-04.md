---
title: "Wiki 自愈报告 — 2026-08-04 consolidate"
category: synthesis
tags:
  - wiki-lint
  - consolidation
  - maintenance
  - self-healing
sources:
  - wiki-lint --consolidate (2026-08-04)
created: 2026-08-04T12:10:00Z
updated: 2026-08-04T12:10:00Z
summary: 2026-08-04 wiki-lint --consolidate 自愈:修复 13 处 xk-ai-talk-desk-ui 项目页 wikilink 双前缀断链、6 处 bad_type 关系(example_of/documented_by → related_to)、救援 4 个孤儿页(3 个项目页随断链修复复挂 + entities/chezmoi 补 chezmoi-patterns-recipes)。剩余 8 个孤儿均为终端节点(consolidation/Research 报告 + 新 capture 页),按设计保留。
tier: peripheral
lifecycle: verified
lifecycle_changed: "2026-08-04"
base_confidence: 0.95
provenance:
  extracted: 0.98
  inferred: 0.02
  ambiguous: 0.0
relationships:
  - target: "[[skills/wiki-lint]]"
    type: related_to
---

# Wiki 自愈报告 — 2026-08-04

> `wiki-lint --consolidate` 全量自愈。Pre-write 快照 commit `003dbbb`(回滚:`git reset --hard 003dbbb`)。

## 摘要

| 维度 | 数量 |
|---|---|
| links_fixed | 13 |
| orphans_rescued | 4 |
| relationship_type_fixes | 6 |
| lifecycle_updates | 0 |
| tier_demotions | 0 |
| tag_fixes | 0 |
| contradiction_callouts | 0 |
| 受影响文件 | 8 |

## Action 1 — 断链修复(13 处)

`xk-ai-talk-desk-ui` 项目内 4 个页的 wikilink 使用了**双前缀** `[[xk-ai-talk-desk-ui/...]]`,而项目页实际位于 `projects/xk-ai-talk-desk-ui/` 下,导致 Obsidian 解析失败。统一修正为 `[[projects/xk-ai-talk-desk-ui/...]]`:

| 文件 | 修复处数 |
|---|---|
| `projects/xk-ai-talk-desk-ui/xk-ai-talk-desk-ui.md` | 5 |
| `projects/xk-ai-talk-desk-ui/concepts/call-center-sdk-integration.md` | 3 |
| `projects/xk-ai-talk-desk-ui/skills/phonebar-call-flow.md` | 3 |
| `projects/xk-ai-talk-desk-ui/concepts/agent-state-machine.md` | 2 |

## Action 2 — 孤儿救援(4 页)

- **3 个项目页**(`call-center-sdk-integration` / `phonebar-call-flow` / `agent-state-machine` 相关)随 Action 1 断链修复被重新挂上入链——原"孤儿"实为双前缀断链的副产物。
- **`references/chezmoi-patterns-recipes`**:在核心枢纽 `entities/chezmoi.md` 的"相关链接"区补一条指向它的 wikilink。

### 按设计保留的 8 个终端节点(不强行补链)

| 页 | 保留原因 |
|---|---|
| `synthesis/consolidation-2026-07-07` 等 4 个 | 历史 lint 报告,天然终端节点 |
| `synthesis/Research: OpenLore` / `Research: treehouse` | wiki-research 独立报告 |
| `skills/gitingest-token-error` | 本 session 新 capture,尚未被引用属正常 |
| `concepts/asciidoc-markup` | Clippings 产物,无自然母页 |

## Extra — 关系类型修复(6 处)

`relationships[].type` 用了非受控值(`example_of` / `documented_by`),不在允许集合 `{extends, implements, contradicts, derived_from, uses, replaces, related_to}` 内。统一改为 `related_to`(`entities/obsidian-wiki-framework` 对 `Ar9av` 的 `derived_from` 保留):

| 文件 | 修复处数 |
|---|---|
| `entities/obsidian-wiki-framework.md` | 2 |
| `concepts/obsidian-wiki-vault-structure.md` | 2 |
| `concepts/wiki-framework-self-reference.md` | 2 |

## 未处理 / 后续

- gitingest token 校验过严问题仍未解(见 [[skills/gitingest-token-error]]),属框架/工具层,非 vault 内容问题。
- 无 tier 变动(本次 consolidate 不含 tier 扫描;上一次批量降 tier 见 commit `5db4946`)。

## 相关

- lint skill:[[skills/wiki-lint]]
- 上一份自愈报告:[[synthesis/consolidation-2026-08-03]]
