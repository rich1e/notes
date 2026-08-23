---
title: "obsidian-wiki vault 标准结构 — 8 类目 + 4 系统文件"
category: concepts
tags:
  - obsidian-wiki
  - vault-structure
  - schema
  - file-organization
sources:
  - https://github.com/Ar9av/obsidian-wiki
  - _raw/_archived/github-Ar9av-obsidian-wiki.txt (gitingest export, 2026-08-04)
created: 2026-08-04T11:35:00Z
updated: 2026-08-04T11:35:00Z
summary: obsidian-wiki vault 框架规定的目录结构:9 类目(concepts/entities/skills/references/synthesis/journal/projects/misc/sources) + 4 系统文件(index.md / log.md / hot.md / .manifest.json) + 3 内部目录(_meta/ / _insights.md / _raw/) + 2 可选目录(_staging/ / _readouts/),每个 wiki 页都有 title/category/tags/sources/created/updated 必备 frontmatter。
tier: core
lifecycle: verified
lifecycle_changed: "2026-08-04"
base_confidence: 0.95
provenance:
  extracted: 0.95
  inferred: 0.04
  ambiguous: 0.01
relationships:
  - target: "[[entities/obsidian-wiki-framework]]"
    type: related_to
  - target: "[[concepts/wiki-framework-self-reference]]"
    type: related_to
---

# obsidian-wiki vault 标准结构

> 框架规定的目录布局。每个 vault 必须严格遵循,否则 `obsidian-wiki` CLI 的命令(`lint` / `query` / `cache-check` 等)会报错。

## 完整结构

```text
$OBSIDIAN_VAULT_PATH/
├── index.md                # Master index — 每页列出,每次写后必须更新
├── log.md                  # 时间序活动日志(ingest / update / lint)
├── hot.md                  # ~500 词语义快照,write skill 必须更新
├── .manifest.json          # 摄入 ledger:每条源路径 / 时间戳 / 产出页
│
├── _meta/                  # vault 内部元数据
│   ├── taxonomy.md         # 受控标签词表
│   └── *.base              # Obsidian Bases dashboard 定义
│
├── _insights.md            # wiki-status insights 模式产出(graph hubs / bridges / dead ends)
│
├── _raw/                   # staging 区 — 下次 ingest 时 promote
├── _staging/               # review queue(仅 WIKI_STAGED_WRITES=true 时启用)
├── _archives/              # 时间戳快照,wiki-rebuild / restore 用
├── _readouts/              # wiki-narrate 产出的叙事报告,**不是知识页**
│
├── concepts/               # 抽象概念 / 模式 / 心智模型
├── entities/               # 实体 — 人物 / 工具 / 库 / 公司
├── skills/                 # how-to 知识 / 技巧 / 流程
├── references/             # 事实速查 — 规范 / API / 配置
├── synthesis/              # 跨页综合分析
├── journal/                # 时限条目 — 日志 / session 笔记
├── projects/               # 一个项目一个 .md,由 wiki-update 同步
└── misc/                   # URL 摄入等待项目归属的页(misc 模式)
```

## 9 个类目的边界

| 类目 | 装什么 | 不装什么 |
|---|---|---|
| **concepts/** | 抽象 / 模式 / 框架层想法 | 具体工具 / 人 / 书 |
| **entities/** | 名字指向的事物(工具 / 库 / 公司 / 人) | 抽象概念(用 concepts) |
| **skills/** | 怎么做(操作步骤 / 工具用法 / 流程) | 概念本身(用 concepts) |
| **references/** | 事实速查(API 端点 / CVE / 配置项) | 长篇论述(用 synthesis) |
| **synthesis/** | 跨 ≥2 个概念的交叉分析 | 单概念扩展(放回源页) |
| **journal/** | 时间序记录,daily bucket | 永久知识(放其他类目) |
| **projects/** | 项目专属知识(架构 / 决策 / 任务进度) | 通用知识(用全局类目) |
| **misc/** | URL 摄入无项目归属的暂存 | 已归属的页 |
| **sources/** | 一手资料(paper / 官方文档) | 二手评论(用 references) |

## 必备 frontmatter

每个 wiki 页 frontmatter 必须含:

```yaml
title: <string>
category: <concepts|entities|skills|references|synthesis|journal|projects|misc|sources>
tags: [<list of kebab-case strings>]
sources:
  - <url or path>
created: <ISO timestamp>
updated: <ISO timestamp>
```

推荐加:`summary:`(≤200 字符,用于 wiki-query 索引)、`tier:`(core / supporting / peripheral)、`lifecycle:`(draft / reviewed / verified / disputed / archived)、`base_confidence:`、`provenance:`(extracted / inferred / ambiguous 三段比例)、`relationships:`(typed edges)。

## 4 个系统文件 + hot cache

| 文件 | 谁写 | 用途 |
|---|---|---|
| `index.md` | ingest / update / lint / synthesize / status | 全 vault 每页的入口索引 |
| `log.md` | 任何写操作 | 时间序操作流水 |
| `hot.md` | ingest / update / capture | ~500 词语义快照,**新 session 起步就靠它** |
| `.manifest.json` | ingest | 摄入 ledger,cache-check 用来计算 delta |

## 链接约定

- **默认**:`page-name` 或 `page-name` —— Obsidian 风格 wikilink
- **可切**:在 `~/.obsidian-wiki/config` 设 `OBSIDIAN_LINK_FORMAT=markdown`,改为标准 markdown `[text](url)` 链接

## 与本 vault 现状的关系

本 vault 完全遵循这套结构:

- `_meta/` ✓
- `_insights.md` ✓(2026-08-03 覆盖写)
- `_raw/` ✓(treehouse / OpenLore / gpakosz-tmux 3 个 staging 副本)
- 8 个类目(concepts 74 / entities 39 / skills 36 / references 25 / synthesis 38 / projects 4 / journal 3 / misc 5)

## 相关

- 框架本体:[[entities/obsidian-wiki-framework]]
- 自我引用拓扑:[[concepts/wiki-framework-self-reference]]
- token 阈值机制:[[skills/wiki-token-threshold-mechanics]]
- 框架 README:https://github.com/Ar9av/obsidian-wiki/blob/main/docs/architecture.md
- 框架作者:[[entities/Ar9av]]