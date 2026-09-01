---
title: >-
  Homebrew Weekly Blog Skill
category: entities
tags: [brew-weekly-blog, homebrew, skill, agent-tooling, content-generation]
sources:
  - conversation:2026-08-31
created: 2026-08-31T13:55:00Z
updated: 2026-08-31T13:55:00Z
summary: >-
  brew-weekly-blog 是位于 /Users/rich1e/.claude/skills/brew-weekly-blog 的 skill,生成随笔风格 Homebrew 周报中文博客,涵盖新增 formulae/casks、重大更新、值得关注的变化。2026-08-31 经 darwin-skill 评估从 78.0 优化到 86.5。
provenance:
  extracted: 0.8
  inferred: 0.2
  ambiguous: 0.0
base_confidence: 0.95
lifecycle: draft
lifecycle_changed: 2026-08-31
---

# Homebrew Weekly Blog Skill

## What It Is

位于 `~/.claude/skills/brew-weekly-blog/SKILL.md` 的 skill(684 → 712 行,经 2026-08-31 优化)。

## How It Works

### 工作流(7 步)

0. **建立跨期上下文** — 扫描最近 2-3 期博客,找本期的"对话对象"
1. **获取数据** — brew update / GitHub Search API / fetch_brew_activity.py(7+ 种 fallback 路径)
2. **筛选工具** — 2-4 个,每个明确对应入选门槛(🔴 CHECKPOINT)
3a. **研究工具** — brew info / WebFetch / GitHub API
3b. **收集配图** — find_tool_images.py / WebFetch / ASCII 降级(🔴 CHECKPOINT)
4. **生成内容** — 个人感受 + 结语 有专项规则
5. **输出** — 文件名 `homebrew-weekly-YYYYMMDD.md`(🔴 发布前 8 条 CHECKPOINT)

### 关键资源

- `scripts/fetch_brew_activity.py` — 追踪新增+重大更新+值得注意的变化
- `scripts/find_tool_images.py` — 自动查找工具配图
- `brew-weekly-template.md`(项目根目录) — 博客结构模版
- `test-prompts.json`(新建) — dim8 实测的 prompt 集

### 反例黑名单(8 条)

1. GUI Cask 工具不配图 → 必须截图或 ASCII
2. 凑数进入重点推荐 → 宁可少写
3. 个人感受是正文缩写 → 只写新判断或反向判断
4. 结语可以用在任何一期 → 必须引用本期具体工具/事件
5. 跳过跨期上下文 → Step 0 必做
6. 图片用外部链接且不验证 → 优先本地
7. 模版路径用 `assets/brew-weekly-template.md` → 实际在项目根目录
8. GitHub API 失败就跳过 → fallback 到 WebFetch README

## When to Use

触发场景:
- "生成 homebrew 周报"
- "brew 更新博客"
- "macOS 工具动态"
- "Homebrew formulae/casks 内容创作"

## Related

- [[synthesis-darwin-skill-brew-weekly-blog-optimization]] — 本 skill 的 darwin 优化记录
- [[concepts-three-segment-fallback-table]] — 本 skill 提炼的设计模式
- [[skills-darwin-skill-evaluation-rubric]] — 评估依据
- [[journal-2026-08-31-darwin-brew-weekly-optimization]] — 本次 session
