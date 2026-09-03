---
title: "/wiki-lint 技能概览"
category: skills
tags: [wiki-lint, maintenance, health-check, consolidation, vault-audit]
sources:
  - ".claude/skills/wiki-lint/SKILL.md (官方 skill 定义)"
created: 2026-08-24
updated: 2026-08-24
summary: wiki-lint 技能读取 vault 结构与 frontmatter 完整性，产出健康审计报告。--consolidate 模式在 dry-run 确认后自动修复 frontmatter 闭合、枚举值、生命周期提升、可见性标签等问题。
base_confidence: 0.7
provenance:
  extracted: 0.0
  inferred: 0.0
  ambiguous: 0.0
lifecycle: draft
lifecycle_changed: 2026-08-24
tier: supporting
---

# /wiki-lint 技能概览

## 占位说明

此页面是 **stub**，由 `/wiki-lint --consolidate` cross-linker 阶段自动创建，用于满足 `[[skills/wiki-lint]]` 的 2 处引用（来自 consolidation 报告）。

## 概要

`wiki-lint` 是 vault 维护技能，扫描整个 wiki 找出结构性问题：

- **orphans** —— 零入链 wikilink 的页面（知识孤岛）
- **broken wikilinks** —— `<!-- broken link: 'target' is a template placeholder -->` 指向不存在的页面
- **missing frontmatter** —— 缺 title/category/tags/sources/created/updated
- **stale content** —— `updated:` 时间戳过老
- **fragmented tags** —— 同 tag 但互链不足（cohesion < 0.15）
- **lifecycle enum** —— 不在 `{draft, reviewed, verified, disputed, archived}` 的值
- **typed relationship** —— 错误的关系类型或失效 target
- **visibility** —— 含敏感模式但无对应标签
- **provenance drift** —— frontmatter `provenance:` 与正文 marker 比例不符

## 两种模式

- **`--check` (默认)** —— 只读审计，输出报告
- **`--consolidate`** —— 在 dry-run + 用户确认后自动修复

## 安全协议

`--consolidate` 必须：1) 写入前 git snapshot；2) dry-run 输出 planned actions；3) 用户确认；4) 写入完成生成 `synthesis/consolidation-<date>.md` 报告。

## 相关

- `/wiki-lint` 的 SKILL.md 在 `.claude/skills/wiki-lint/`
- [[synthesis/consolidation-2026-08-24]] — 最近的 --consolidate 运行报告