---
title: Consolidation Report 2026-08-12
category: synthesis
tags: [maintenance, consolidation]
sources: []
summary: "wiki-lint --consolidate 自动维护报告：12 处破损链接修复，1 处 orphan rescue，11 页 lifecycle 晋升，4 处 tag alias 规范化，2 处 relationship 类型修复。"
lifecycle: draft
lifecycle_changed: "2026-08-12"
tier: peripheral
base_confidence: 0.9
created: 2026-08-12T14:20:00Z
updated: 2026-08-12T14:20:00Z
---

# Consolidation Report — 2026-08-12

Pre-write snapshot: `eb0029cc3bbadc334577bdea86c0a75470e4bc35`

## Summary

| 动作 | 数量 |
|---|---|
| 破损链接修复 | 12 |
| Orphan rescue（反链新增） | 1 |
| Lifecycle draft → reviewed | 11 |
| Tier demotion | 0 |
| Tag alias 规范化 | 4 |
| Relationship 类型修复 | 2 |
| **合计修改文件** | **29** |

---

## 破损链接修复（12 处）

| 文件 | 旧链接 | 新链接 |
|---|---|---|
| `concepts/bmad-named-agent-architecture.md` | `[[concepts/claude-code-settings]]` | `[[skills/claude-code-settings]]` |
| `concepts/omo-skill-embedded-mcps.md` (×3) | `[[concepts/claude-code-token-optimization]]` | `[[skills/claude-code-token-optimization]]` |
| `concepts/bmad-build-workflow.md` | `[[concepts/claude-code-token-optimization]]` | `[[skills/claude-code-token-optimization]]` |
| `concepts/omo-editions-ultimate-vs-light.md` | `[[concepts/claude-code-token-optimization]]` | `[[skills/claude-code-token-optimization]]` |
| `concepts/omo-discipline-agents.md` | `[[concepts/claude-code-token-optimization]]` | `[[skills/claude-code-token-optimization]]` |
| `skills/omo-install-and-setup.md` | `[[concepts/claude-code-token-optimization]]` | `[[skills/claude-code-token-optimization]]` |
| `entities/oh-my-openagent.md` | `[[concepts/claude-code-token-optimization]]` | `[[skills/claude-code-token-optimization]]` |
| `concepts/agent-team-race-condition-task-claim.md` | `[[concepts/openlore]]` | `[[entities/openlore]]` |
| `entities/gpakosz-tmux.md` | `[[concepts/terminal-music]]` | `[[skills/terminal-music]]` |
| `concepts/omo-intent-gate.md` | `[[concepts/bmad-party-mode]]` | `[[entities/bmad-party-mode]]` |
| `concepts/bmad-preventing-agent-conflicts.md` | `[[concepts/agent-team-preventing-conflicts]]`（已删页）| `[[concepts/bmad-preventing-agent-conflicts]]`（自引用 → 本页） |
| `concepts/bmad-advanced-elicitation.md` | `[[concepts/agent-team-party-mode]]`（已删页）| `[[entities/bmad-party-mode]]` |

---

## Orphan Rescue（1 处）

| 页面 | 反链新增位置 |
|---|---|
| `entities/Ar9av.md` | `concepts/obsidian-wiki-vault-structure.md` 末尾 Related 节加 `[[entities/Ar9av]]` |

---

## Lifecycle 晋升（draft → reviewed，11 页）

条件：lifecycle=draft AND created < 2026-07-13（>30天）AND base_confidence > 0.7

| 页面 | created | confidence |
|---|---|---|
| `references/cs193p-spring-2025.md` | 2026-07-10 | 0.83 |
| `references/pattern-catalog-battle-tested-patterns.md` | 2026-07-08 | 0.85 |
| `synthesis/ptp-ieee1588 × linuxptp.md` | 2026-07-07 | 0.88 |
| `synthesis/Research: Fabric AI Framework.md` | 2026-07-09 | 0.82 |
| `synthesis/zustand-core-architecture × zustand.md` | 2026-07-07 | 0.86 |
| `synthesis/trek-auth-system × trek-mcp-server.md` | 2026-07-07 | 0.84 |
| `synthesis/arc-memory-management × swift-concurrency.md` | 2026-07-07 | 0.86 |
| `concepts/fabric-patterns.md` | 2026-07-09 | 0.75 |
| `skills/fabric-usage-patterns.md` | 2026-07-09 | 0.75 |
| `entities/fabric-ai.md` | 2026-07-09 | 0.80 |
| `entities/battle-tested-patterns.md` | 2026-07-08 | 0.75 |

---

## Tag Alias 规范化（4 处）

| 文件 | 旧 tag | 新 tag |
|---|---|---|
| `Clippings/nds折腾.md` | `DSTWO` | `flashcard` |
| `Clippings/浅谈 R4iSDHC 用户体验.md` | `DSTWO` | `flashcard` |
| `Clippings/电波的电玩记忆-NDS世代.md` | `DSTWO` | `flashcard` |
| `Clippings/姚期智万字长文演讲.md` | `AI` | `llm` |

---

## Relationship 类型修复（2 处）

| 文件 | 旧 type | 新 type | 说明 |
|---|---|---|---|
| `skills/notebooklm-mcp-setup.md` [rel:2] | `replaced_by` | `related_to` | `replaced_by` 不在允许集；本页被替代语义用 `related_to` + lifecycle=archived 表达 |
| `skills/notebooklm-mcp-setup.md` [rel:3] | `replaced_by` | `related_to` | 同上 |

---

## 跳过（需人工决策）

- `index.md` 6 条 flow-design-system 路径错误（需确认 `projects/` 目录实际结构）
- omo 9 页缺失 `summary:` 字段（语义内容，不自动生成）
- 2 个 consolidation 报告缺 `base_confidence`（不自动写 confidence）
- 碎片化 tag 集群（`#security` cohesion=0.04 等）→ 建议运行 `/cross-linker`
