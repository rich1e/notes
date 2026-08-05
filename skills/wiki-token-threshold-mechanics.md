---
title: "wiki-status token 阈值机制 — 为何常是假警报"
category: skills
tags:
  - obsidian-wiki
  - token-optimization
  - wiki-status
  - vault-maintenance
  - operations
sources:
  - wiki-status SKILL.md (Step 3b token footprint)
  - wiki-query SKILL.md (tiered retrieval, line 108/180)
  - 本 session 实测 (2026-08-04, KG 273 pages)
created: 2026-08-04T13:00:00Z
updated: 2026-08-04T13:00:00Z
summary: wiki-status 报的 token footprint 是"全量入 context"的最坏情况(全 vault 字节÷4),但没有任何常规操作会全量加载;真实单次 query 因分层检索(index+top3+跳 peripheral)只 ~18K。超阈值多为假警报,根治靠调 WIKI_TOKEN_WARN_THRESHOLD 而非降 tier(降 tier 不删字节)。阈值应≈最坏单次加载量,与 vault 全量规模弱相关。
tier: supporting
lifecycle: verified
lifecycle_changed: "2026-08-04"
base_confidence: 0.92
provenance:
  extracted: 0.6
  inferred: 0.38
  ambiguous: 0.02
relationships:
  - target: "[[skills/claude-code-token-optimization]]"
    type: related_to
  - target: "[[concepts/obsidian-wiki-vault-structure]]"
    type: related_to
---

# wiki-status token 阈值机制

> `⚠️ Full wiki exceeds 100K tokens` 这个告警在成熟 vault 上**常是假警报**。它衡量的是一个**永不发生**的最坏情况。

## 这个数字到底衡量什么

`wiki-status` 的 token footprint(SKILL Step 3b):把 **vault 所有页的字节数 ÷ 4**(4 chars/token 启发式)相加,拿这个**全量总和**去比 `WIKI_TOKEN_WARN_THRESHOLD`(默认 100000)。

它回答的问题是:「假如把整个 vault 一次性塞进 context,要多少 token?」—— 但**没有任何常规操作会这么做**。

## 真实成本 vs 全量指标(2026-08-04 实测,KG 273 页)

| 操作 | 真实 token | 说明 |
|---|---|---|
| **index-only pass**(query 起手) | **~14.4K** | 只扫 frontmatter title+summary+tags |
| **典型 query**(index + 展开 3 页) | **~18.6K** | 分层检索的实际负载 |
| 全量加载(**阈值比的就是这个**) | ~227K | 永不发生 |

wiki-query 是**分层检索**(wiki-query SKILL 第 108/180 行):
1. 先扫 frontmatter 索引 → 打分排序
2. **只 Read 前 3 页全文**
3. **`skip peripheral pages unless they are the only match`** —— peripheral 默认被跳过

所以进 context 的永远是「索引 + 少数几页」≈ 15-20K,离 100K 有 5 倍余量。

## 三个关键结论

### 1. 超阈值的成因
- 页数多(273 页)+ supporting 占大头(143 页 / ~167K)+ 默认阈值 100K 对成熟 vault 偏低。
- 大多数 supporting 页 in≥5,是「连接密集的健康页」,**不是冗余**。

### 2. 为何"降 tier 减 token"无效
**降 tier 不删字节。** `tier:` 只是 frontmatter 一行值,改它不改文件大小。降 peripheral 的**唯一**作用是让 query 更早跳过该页 —— 但 query 本来就只读 top 3、本来就跳 peripheral。为一个不存在的瓶颈做大规模 frontmatter 改动 = 伪优化。

> 另一障碍:框架硬规则「demote:in≤1 **AND** 90d+ stale」。对 <90 天的年轻 vault,**0 个合规 demote 候选**——降 tier 这条路连入口都没有。

### 3. 阈值调整取决于什么
取决于**最大的单次加载操作**(≈ index-only 成本 × 安全系数),**不是** vault 全量总和。

| 量 | 与 vault 规模的关系 |
|---|---|
| 全量总和(告警比的数) | **强正相关**(线性,随 ingest 一直涨) |
| 真实 query 成本 | **几乎无关**(永远只读 top 3) |
| index-only pass | 弱正相关(273 页才 14.4K,涨到 2000 页也才 ~100K) |

**根治办法**:调高阈值到 ≈ 覆盖最坏单次加载的量级。本 vault 已设 `WIKI_TOKEN_WARN_THRESHOLD=250000`(见 `~/.obsidian-wiki/config`),留足增长空间;真到 25 万才该考虑拆 vault。设 `0` 可完全关闭。

## 何时才是真问题(不是假警报)

- **单次 query 本身**逼近阈值(index-only 就几万 token)→ frontmatter/summary 写太长,或页数真的爆炸(数千页)。
- 这时才该考虑:精简 summary、拆 vault、或对确实过时的长尾走 `wiki-rebuild` 归档。

## 相关

- 通用 token 优化:[[skills/claude-code-token-optimization]]
- vault 结构与 tier 定义:[[concepts/obsidian-wiki-vault-structure]]
- 同属框架运维:[[skills/obsidian-wiki-daily-cron-macos]] — launchd 每日维护定时任务安装
