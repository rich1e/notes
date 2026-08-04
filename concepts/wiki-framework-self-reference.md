---
title: "Wiki 框架自我引用 — 当仓库本身就是 vault 的运行时"
category: concepts
tags:
  - obsidian-wiki
  - meta
  - topology
  - self-reference
sources:
  - https://github.com/Ar9av/obsidian-wiki
  - _raw/_archived/github-Ar9av-obsidian-wiki.txt (gitingest export, 2026-08-04)
created: 2026-08-04T11:35:00Z
updated: 2026-08-04T11:35:00Z
summary: Ingest 框架本源仓库(Ar9av/obsidian-wiki)时的特殊拓扑:框架是 vault 的运行时,vault 的内容已通过 39 个 symlink + CLI 包 + 多 agent bootstrap 间接"持有"框架;直接 distill 等于把已有内容重复入库,正确做法只保留框架本体 / owner / 结构 3 页作为索引,框架细节指向已存在的 CLAUDE.md/hot.md/_meta/taxonomy 等页。
tier: supporting
lifecycle: draft
lifecycle_changed: "2026-08-04"
base_confidence: 0.85
provenance:
  extracted: 0.7
  inferred: 0.25
  ambiguous: 0.05
relationships:
  - target: "[[entities/obsidian-wiki-framework]]"
    type: related_to
  - target: "[[concepts/obsidian-wiki-vault-structure]]"
    type: related_to
---

# Wiki 框架自我引用

> 当你 ingest 某个 GitHub 仓库,而这个仓库恰好是 **vault 自身的运行框架**,会发生什么?

## 问题

`Ar9av/obsidian-wiki` 是本 vault 用的框架。它的 README、AGENTS.md、docs/architecture.md、docs/cli.md、docs/skills.md 几乎逐字相同于:

- `/Users/rich1e/workspace/code/notes/CLAUDE.md`(vault 的主 agent context)
- `/Users/rich1e/workspace/code/notes/AGENTS.md`(等价)
- `~/.claude/skills/wiki-*/SKILL.md`(39 个 skill,各自定义)
- `_meta/taxonomy.md`(本 vault 的受控标签词表)

也就是说:**vault 已经在引用 / 镜像框架内容**,再 distill = 重复入库,可能产生循环引用、orphan、tier 升级污染等问题。

## 处理原则

| 原则 | 含义 |
|---|---|
| **只保留指向,不重复内容** | vault 已有的部分(CLAUDE.md / hot.md / 各 skill)不再生成对应 wiki 页 |
| **保留 3 页索引** | 框架本体 / 作者 / 标准结构,作为 vault 自指锚点 |
| **明确标注 "本 vault 已用此框架"** | 避免误读为新内容 |
| **保留 tier:core** | 让 wiki-query 知道"任何 wiki 操作最终都依赖此框架" |

## 实际实现(2026-08-04 Ar9av/obsidian-wiki ingest)

新增 3 页:

- `entities/obsidian-wiki-framework` —— 框架本身,框架名 / 39 skill / 多 agent bootstrap / 设计哲学 / 安装
- `entities/Ar9av` —— 框架作者(GitHub + X + 贡献列表)
- `concepts/obsidian-wiki-vault-structure` —— 框架规定的 vault 结构,标注 "本 vault 完全遵循"

**未**创建的内容(避免重复):

- `concepts/wiki-framework-architecture`(已在 CLAUDE.md / hot.md 里)
- `concepts/wiki-skill-system`(每个 wiki-* skill 都有自己的 SKILL.md)
- `concepts/wiki-cli-commands`(`obsidian-wiki --help` 即可查)
- `concepts/wiki-tier-system`(在 `_meta/taxonomy.md`)
- `entities/wiki-claude-code`、`entities/wiki-cursor` 等(框架 bootstrap 文件,已在 vault 里通过 .claude/skills symlink 体现)

## 自指拓扑示意

```text
       Ar9av/obsidian-wiki (GitHub source)
       │
       │ ← gitingest clone
       ↓
   _raw/_archived/github-Ar9av-obsidian-wiki.txt
       │
       │ ← wiki-ingest-with-token (本次)
       ↓
   entities/obsidian-wiki-framework ──┐
   entities/Ar9av                    │
   concepts/obsidian-wiki-vault-structure
   concepts/wiki-framework-self-reference ← 你在这里
                                    │
   但每个 wiki-* skill 在 vault 里有 ─┘
   自己的 SKILL.md 定义 ──→ 直接
   symlink 回 Ar9av/obsidian-wiki 的 .skills/*

   已有 vault 内容(CLAUDE.md / hot.md /
   _meta/taxonomy.md)直接镜像框架 ──→ 不
   通过 wiki-ingest,git 直接同步
```

## 何时应该打破原则

如果框架有新版本(例如 OKF v0.2、新的 trust ledger 设计、新的 session brain 算法),**应该**走完整 ingest + synthesize 流程,**但**只摘取**与 vault 现状差异的部分**到现有页(例如 merge 到 `_meta/taxonomy.md`),而不是新建重复页。

## 反模式

| 反模式 | 后果 |
|---|---|
| 把框架 README 蒸馏成 `concepts/obsidian-wiki-readme` | 与 CLAUDE.md 重复,产生相同 wikilink 引用环 |
| 把 39 个 skill 摘要进 `skills/wiki-skill-system` | 与各 skill 的 SKILL.md 重复,base wiki-lint 会报"redundant wikilink" |
| 把 docs/architecture.md 完整 distill | 重复 vault hot.md 已有的内容 |
| 不创建任何新页,直接 ingest 后放弃 | 浪费一次 ingest,manifest 还得多一条 |

## 相关

- 框架本体:[[entities/obsidian-wiki-framework]]
- 标准结构:[[concepts/obsidian-wiki-vault-structure]]
- 框架作者:[[entities/Ar9av]]
- 一般 ingest 流程(非自指场景):[[skills/wiki-ingest]]
- 带 keychain token 的 ingest 流程:[[skills/wiki-ingest-with-token]]