---
title: Consolidation Report 2026-07-30
category: synthesis
tags: [maintenance, consolidation, lint]
sources: []
summary: Auto-generated consolidation report from wiki-lint --consolidate run on 2026-07-30.
lifecycle: draft
lifecycle_changed: 2026-07-30
tier: peripheral
created: 2026-07-30T03:27:35Z
updated: 2026-07-30T03:27:35Z
base_confidence: 0.5
relationships: []
---

# Consolidation Report — 2026-07-30

## Summary
- Broken links fixed: 26 (13 files)
- Cross-references added (orphan rescue): 0 (skipped — needs user approval)
- Lifecycle states updated: 0
- Tier demotions: 0
- Tags normalized: 0
- base_confidence 补全: 5 files
- Contradiction callouts added: 0

## Broken Link Fixes

### Real fixes (2 真实修复)

| Source | Old | New |
|---|---|---|
| `synthesis/consolidation-2026-07-26.md` | `prompt-engineering-patterns` | `[[concepts/fabric-patterns]]` |
| `synthesis/Research: DESIGN.md 工作流.md` (×5) | `web-medium-com-devsecops-ai-...-integration` | `[[misc/web-medium-com-devsecops-ai-how-google-stitch-claude-codes-mcp-integration]]` |

第二行修复了 4 处截断的 misc 链接 + 1 处原文(共 5 次出现)。

### Placeholder removals (20 去除占位符)

`target\` / `target` / `page` / `...` 等 audit 报告占位符 → 转纯文本。涉及文件:

- `synthesis/consolidation-2026-07-07.md` (1)
- `synthesis/consolidation-2026-07-23.md` (3)
- `synthesis/consolidation-2026-07-26.md` (3 含 1 真 fix)
- `synthesis/Research: 学习AI大模型.md` (2)
- `concepts/llm-training-pipeline.md` (4)
- `concepts/test-time-compute.md` (2)
- `concepts/llm-learning-path.md` (1)
- `concepts/rag-vs-finetuning.md` (1)
- `concepts/mechanistic-interpretability.md` (1)
- `entities/sebastienrousseau-dotfiles.md` (1)
- `entities/sebastian-raschka.md` (1)
- `entities/andrej-karpathy.md` (1)

### Skipped: bash test 误识别 (6 处,保留原文)

`[[ -z "$pw" ]]` / `[[ -n "$BW_SESSION" ]]` / `[[ ! -f "$cred_file" ]]` / `[[ -z "$ZELLIJ" ]]` 全部在 ```bash 代码块内, 是 bash test 语法不是 wikilink, lint 正则误识别。**未修改** (否则会破坏 bash 代码)。**未来改进**: lint 工具的 wikilink 扫描应跳过代码块。

## base_confidence 补全 (5 files)

| File | 补值 | 依据 |
|---|---|---|
| `synthesis/consolidation-2026-07-26.md` | 0.40 | consolidation 报告型, 本身只是 audit |
| `concepts/kimi-delta-attention.md` | 0.65 | Research 报道, 一手 sources 中等 |
| `concepts/mixture-of-experts.md` | 0.65 | Research 报道, 一手 sources 中等 |
| `entities/kimi-k3.md` | 0.70 | 官方博客+多 sources, 发布时点新(2026-07-27) |
| `entities/moonshot-ai.md` | 0.65 | 一手 sources 较少, 公司层面信息偏市场口径 |

补值经人类审批后填入。下次 /wiki-research 重新摄入可触发 re-review 提升。

## 不在本次范围

- **Orphan 6 个** — 需 cross-linker 单独 rescue(已记录在 wiki-status)
- **#security fragmented tag** — 8 页 cohesion 0.04, 需 cross-linker 单跑
- **#research fragmented tag** — 实际已被 Research: 合成页覆盖,非真 gap
- **7 untagged PII 模式词** — 5 个是教程里引用鉴权机制, 应改 lint precision 不应污染教程
- **13 synthesis gap** — 下次 /wiki-synthesize 处理
- **trust-ledger 缺失** — 需人工审批 `trust-record --all --approved`, 不自动跑

## 风险与回滚

snapshot SHA: `8cad99e7`。若需回滚全部改动:

```bash
git reset --hard 8cad99e7
git clean -fd
```

## See also

- [[synthesis/consolidation-2026-07-26]] — earlier consolidation report
- [[synthesis/consolidation-2026-07-31]] — next consolidation report
- log — full audit log
