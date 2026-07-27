---
title: Consolidation Report 2026-07-23
category: synthesis
tags: [maintenance, consolidation]
sources: []
summary: Auto-generated consolidation report from wiki-lint --consolidate run on 2026-07-23.
lifecycle: draft
lifecycle_changed: 2026-07-23
tier: peripheral
created: 2026-07-23T00:00:00Z
updated: 2026-07-23T00:00:00Z
base_confidence: 1.0
---

# Consolidation Report — 2026-07-23

## Summary

- Broken links fixed: 20（反斜杠 parser artifact）+ 1（真实破损转为注释）= 21
- Cross-references added: 6（孤立页救援）
- Lifecycle states updated: 4（Fabric 页面 `active` → `draft`）
- base_confidence added: 3（Fabric 概念/实体/技能页）
- Tier demotions: 0（无符合条件页面）
- Tags normalized: 8（`NDS`→`nds`、`state-machine`→`state-management`、`photography`→`media` 等真实别名修复）
- Contradiction callouts added: 0
- Taxonomy alias errors noted: taxonomy.md 中存在双向循环别名定义（`llm`↔`Deepseek`、`ios`↔`mobile` 等），跳过这些混乱映射

Pre-write git snapshot: `fcd71c4ecf5df4912ffae2c852fbfe12dd712e5b`

---

## Broken Link Fixes

### 反斜杠伪链接（Parser Artifact，20 个）

这些链接使用了 `[[target\|display]]` 格式，反斜杠导致链接目标解析失败。目标页面均存在，仅链接语法有误。

- `entities/ios17-app-development-book.md` — 10 个（`xcode-ide-guide\`、`swift-fundamentals\` 等）
- `concepts/ptp-ieee1588.md` — 2 个（`ptp-tlv-extension\`、`white-rabbit\`）
- `references/ique-dsi-menu-software.md` — 5 个（`ique-dsi-camera\`、`ique-dsi-sound\` 等）
- `synthesis/consolidation-2026-07-07.md` — 3 个（`ptp-bmca\`、`ptp-tlv-extension\`、`page\`）

修复方式：将 `[[target\|display]]` → `[[target|display]]`

### 真实破损链接（1 个）

- `entities/fabric-ai.md:98` — ``concepts/prompt-engineering-patterns`` 目标页不存在 → 转为注释文本：`提示工程思想 <!-- broken link -->`

---

## Cross-References Added（孤立页救援）

| 孤立页 | 新增入链来源 |
|---|---|
| `concepts/animation-easing-functions` | `synthesis/consolidation-2026-07-07`（追加相关节）|
| `concepts/mobile-timer-accuracy` | `concepts/javascript-event-loop`（加入相关概念节）|
| `skills/ios-data-persistence` | `concepts/ios-app-architecture`（追加相关节）|
| `synthesis/Research: Fabric AI Framework` | `concepts/fabric-patterns`（加入相关节）|
| `synthesis/Research: Fabric AI Framework` | `entities/fabric-ai`（加入相关概念节）|
| `synthesis/Research: Fabric AI Framework` | `skills/fabric-usage-patterns`（加入相关节）|

仍有孤立页（无文本提及，需人工处理）：
- `concepts/asciidoc-markup`
- `concepts/llm-speculative-decoding`
- `references/mechanical-watch-mechanics`
- `skills/hackintosh-mini-build`
- `projects/xk-ai-talk-desk-ui/concepts/call-center-sdk-integration`
- `projects/xk-ai-talk-desk-ui/skills/phonebar-call-flow`

---

## Lifecycle Updates

| 页面 | 变更 | 原因 |
|---|---|---|
| `concepts/fabric-patterns.md` | `active` → `draft` + `base_confidence: 0.75` | `active` 不是有效枚举值（同 jrfed 问题，2026-07-07 已有先例）|
| `entities/fabric-ai.md` | `active` → `draft` + `base_confidence: 0.80` | 同上 |
| `skills/fabric-usage-patterns.md` | `active` → `draft` + `base_confidence: 0.75` | 同上 |
| `synthesis/Research: Fabric AI Framework.md` | `active` → `draft` | 同上（synthesis 页不自动填 base_confidence）|

---

## Tag Normalizations

| 页面 | 变更 |
|---|---|
| `skills/ique-ds-download-play.md` | `NDS` → `nds` |
| `concepts/ptp-port-state-machine.md` | `state-machine` → `state-management` |
| `synthesis/zustand-core-architecture × zustand.md` | `state-machine` → `state-management` |
| `projects/xk-ai-talk-desk-ui/concepts/agent-state-machine.md` | `state-machine` → `state-management` |
| `projects/dayfold/concepts/fetchrequest-vs-observedobject.md` | `state-machine` → `state-management` |
| `skills/ique-dsi-sound.md` | `photography` → `media` |
| `skills/ique-dsi-camera.md` | `photography` → `media` |
| `projects/dayfold/skills/entry-editor-image-dirty-tracking.md` | `photography` → `media` |

**跳过的混乱别名：** taxonomy.md 中存在循环/双向映射（如 `llm↔Deepseek`、`ios↔mobile`），这些映射语义矛盾，不应机械执行。建议修复 taxonomy.md 本身。

---

## Fragmented Tag Clusters（报告，不自动修复）

需运行 `/cross-linker` 处理：

| Tag | 页数 | 凝聚度 | 建议 |
|---|---|---|---|
| `#swiftui` | 9 | 0.10 | `/cross-linker` |
| `#architecture` | 6 | 0.00 | `/cross-linker` |
| `#core-data` | 6 | 0.13 | `/cross-linker` |
| `#design-system` | 5 | 0.00 | `/cross-linker` |
| `#security` | 5 | 0.05 | `/cross-linker` |

---

## Synthesis Gaps（Top 3，报告仅）

运行 `/wiki-synthesize` 可自动填充：

| 对 | 共现次数 |
|---|---|
| `ios17-app-development-book × swift-fundamentals` | 9 |
| `swift-concurrency × swiftui-framework` | 6 |
| `swift-fundamentals × swiftui-framework` | 6 |

---

## Taxonomy Issues（待人工修复）

`_meta/taxonomy.md` 中存在以下循环别名定义，需人工整理：
- `llm` 的别名列 `Deepseek`，同时 `Deepseek` 的规范形式也是 `llm`（循环）
- `ios` 与 `mobile` 互为别名（语义上不等价）
- `macOS` 与 `macos` 互相对应（大小写规范化可以，但方向需统一）
## 相关页面

- [[synthesis/consolidation-2026-07-07.md]]
