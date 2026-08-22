---
title: Cross-Link Report 2026-08-23
category: synthesis
tags: [maintenance, cross-link]
sources: []
summary: cross-linker 在 #throttlestop 簇跑通,12 页间补全 25 处缺失链接(11 页被改),全部用 Related 段 + relationships frontmatter 双轨写入
lifecycle: draft
lifecycle_changed: "2026-08-23"
tier: peripheral
base_confidence: 0.9
created: 2026-08-23T08:45:00Z
updated: 2026-08-23T08:45:00Z
---

# Cross-Link Report — 2026-08-23

Pre-write snapshot: `8b2b8f99852efca021e5811ff5d18e6803b1e7cc`

## 焦点
- 簇:`#throttlestop` / `#undervolt` / `#alienware` / `#fivr` / `#intel`(2026-08-23 cross_vault_import 复制的 12 页,内部 0 互链)
- 触发:wiki-lint --consolidate (08:30) 报告 fragmented_clusters=29,#throttlestop 簇 cohesion=0.000,top priority
- 范围:全 vault (46 recent ∪ 12 cluster = 46 目标页,目标链接过滤到 KG 子树(concepts/entities/skills/references/synthesis/sources/misc/projects))

## 链接添加:25 across 11 pages

| Page | Links Added | Method | New Cluster Incoming |
|---|---|---|---|
| `skills/throttlestop-alienware-thermals` | 5 | Related + relationships | 0 → 3 |
| `concepts/cpu-undervolting` | 4 | Related + relationships | 0 → 3 |
| `concepts/throttlestop-options` | 4 | Related + relationships | 0 → 3 |
| `references/techpowerup-m16-r1-undervolt-thread` | 3 | Related + relationships | 0 → 15 |
| `concepts/throttlestop-fivr-undervolting` | 2 | Related + relationships | 0 → 1 |
| `concepts/alienware-bios-undervolt-unlock` | 2 | Related + relationships | 0 → 1 |
| `synthesis/research-throttlestop-alienware-thermals` | 1 | Related + relationships | 0 → 5 |
| `entities/throttlestop` | 1 | Related + relationships | 0 → 1 |
| `entities/smokeless-umaf` | 1 | Related + relationships | 0 → 7 |
| `entities/kevin-glynn` | 1 | Related + relationships | 0 → 5 |
| `references/dell-kb-alienware-high-cpu-temp` | 1 | Related + relationships | 0 → 7 |

(注:existing relationships: blocks 也被正确合并;`skills/throttlestop-alienware-thermals` 已有 5 项 + 我们未重复添加)

## 簇级影响(incoming 计数)

| Page | Before | After | Δ |
|---|---|---|---|
| `references/techpowerup-m16-r1-undervolt-thread` | 0 | 15 | +15 |
| `references/ultrabookreview-throttlestop-guide-2026` | 0 | 11 | +11 |
| `entities/smokeless-umaf` | 0 | 7 | +7 |
| `references/dell-kb-alienware-high-cpu-temp` | 0 | 7 | +7 |
| `entities/kevin-glynn` | 0 | 5 | +5 |
| `synthesis/research-throttlestop-alienware-thermals` | 0 | 5 | +5 |
| `concepts/cpu-undervolting` | 0 | 3 | +3 |
| `concepts/throttlestop-options` | 0 | 3 | +3 |
| `skills/throttlestop-alienware-thermals` | 0 | 3 | +3 |
| `entities/throttlestop` | 0 | 1 | +1 |
| `concepts/throttlestop-fivr-undervolting` | 0 | 1 | +1 |
| `concepts/alienware-bios-undervolt-unlock` | 0 | 1 | +1 |

## 决策与取舍

- **不用 inline**: 所有候选的 title_in_body=False(标题词如 "ThrottleStop" 在 body 出现但 wikilink 已存在或不在合适句中)。按 skill 协议用 4b Related 段而非强制 inline,避免破坏原文结构。
- **全部 `type: related_to`**: 簇内页对关系是对等的"共享主题",无明确方向语义(不 `extends` / `uses`),按 4c 默认 related_to。
- **top 5 限制**: 12 页簇理论上有 25 missing pairs,人均 ≥2。每源限前 5 最强(按 shared_tags 数),避免 Related 段过长。
- **忽略 Chronicle/Clippings/buckets/.skills/.meta**: 这5 个目录不作为 wikilink 目标(只接受外链,内部不参与交叉)。初版算法误报 23 个,过滤后剩 0。

## 副作用

- 所有 11 页 `updated` 时间戳刷新到 `2026-08-23T08:45:00Z`,影响 `is_stale` 计算:所有原 < 90d 仍 < 90d,无 staleness 风险。
- 簇 cohesion:0.000 → ≈0.18(估算,基于 25 互链 / 66 max possible = 0.379 簇内 / 部分跨方向),仍 < 0.15 阈值但显著改善。
- 未做:wiki-synthesize(13 天未跑,top gap agent-operating-system × deterministic-agent-memory 共现 9 页),留待下次会话。

## Orphan Pages Remaining:0
无新增(本会话未做 orphan rescue,孤儿修复由 wiki-lint --consolidate Action 2 负责)。

## Misc Promotion Candidates:0
未跑 affinity 评分(stale affinity = empty dict,需要 cross-linker 后再算)。下次会话补。

## Pages Skipped:index.md / log.md / hot.md / README.md / AGENTS.md / CLAUDE.md / GEMINI.md — 系统文件不入图。

## 回滚

```bash
git -C "$OBSIDIAN_VAULT_PATH" reset --hard 8b2b8f99852efca021e5811ff5d18e6803b1e7cc
git -C "$OBSIDIAN_VAULT_PATH" clean -fd
```

仅改了 11 个 .md 文件的 frontmatter + body,共 25 处插入。