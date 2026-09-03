---
title: >-
  Skill Runtime Neutrality Grep
category: skills
tags: [runtime-neutrality, gate-item, grep, darwin-skill, multi-runtime]
sources:
  - conversation:2026-08-31
created: 2026-08-31T14:05:00Z
updated: 2026-08-31T14:05:00Z
summary: >-
  Darwin-skill 的 Runtime 适配性审查是 P0 gate 项,用固定 grep 模式扫描 SKILL.md/README.md 找"在 Claude Code 里"等会让其他 runtime 拒装的措辞,修复模板是改写为"兼容任何支持 Agent Skills 标准的 runtime"。
provenance:
  extracted: 0.6
  inferred: 0.4
  ambiguous: 0.0
base_confidence: 0.85
lifecycle: draft
lifecycle_changed: 2026-08-31
---

# Skill Runtime Neutrality Grep

## What It Is

Darwin-skill 强制 Runtime 适配性审查的具体命令——一个固定 grep 模式,扫描 SKILL.md/README.md 找会触发其他 runtime(Marvis / OpenClaw / Hermes 等)拒装的措辞。

## How It Works

### Grep 命令

```bash
grep -nE "(在 Claude Code|Claude Code skill|Claude Code 用户|Cursor only|Codex 中|^\[!\[Claude Code|~/\.claude/skills/[a-z]|/plugin install\b)" SKILL.md README.md 2>/dev/null
```

**输出非空 = 红灯命中** → Phase 2 第一轮强制 P0 修复。

### 红灯命中示例

```markdown
## 使用方法

在 Claude Code 中调用此 skill:

\`\`\`bash
/brew-weekly-blog
\`\`\`
```

↑ `README.md:14` 命中 "在 Claude Code 中调用此 skill"——其他 runtime(Marvis)会判为"不是给我用的"拒装。

### 修复模板

```diff
- 在 Claude Code 中调用此 skill:
- ```bash
- /brew-weekly-blog
- ```
+ > 此 skill 兼容任何支持 Agent Skills 标准的 runtime
+   (Claude Code / Codex / Cursor / OpenClaw / Hermes / Gemini CLI 等)。
+
+ 在支持的 runtime 中调用:
+ ```
+ /brew-weekly-blog
+ ```

### 例外(允许的 Claude Code 痕迹)

- frontmatter 触发词(如 `description: ...` 提到 Claude Code)
- 花叔生态内部 skill 名引用
- 明确标注 runtime-specific 章节
- commit message

这些正当出现不算红灯。

## When to Use

触发条件:
- 任何新创建或修改的 skill,发布前必跑
- darwin-skill Phase 1 baseline 时强制跑一次
- 给其他 runtime 用户分发 skill 前(避免被拒装)

## 实战记录

brew-weekly-blog 2026-08-31:Round 2 命中一条红线(README L14),修复 +0.8 分。
该 skill 已确认可在 Claude Code / Codex / Cursor / OpenClaw / Hermes / Gemini CLI 等 runtime 使用。

## Related

- [[skills/darwin-skill-evaluation-rubric]] — Runtime 适配性是 gate 项,不是 dim6 子项
- [[synthesis/darwin-skill-brew-weekly-blog-optimization]] — 实战示例
- [[entities/homebrew-weekly-blog-skill]] — 被修复的 skill 实体
- [[journal/2026-08-31-darwin-brew-weekly-optimization]] — 本次 session
