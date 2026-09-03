---
title: >-
  Session 2026-08-31 — brew-weekly-blog 生成 + darwin-skill 优化两轮
category: journal
tags: [darwin-skill, brew-weekly-blog, homebrew, session-summary, skill-optimization]
sources:
  - conversation:2026-08-31
created: 2026-08-31T13:40:00Z
updated: 2026-08-31T13:40:00Z
summary: >-
  一次 session 完成两件事:生成第 0831 期 Homebrew 周报(主题「客户端被各种方向重做」),并用 darwin-skill 优化 brew-weekly-blog 技能(+8.5 分,2 轮 keep 0 回滚)。
provenance:
  extracted: 0.85
  inferred: 0.15
  ambiguous: 0.0
base_confidence: 0.9
lifecycle: draft
lifecycle_changed: 2026-08-31
---

# Session 2026-08-31 — brew-weekly-blog 生成 + darwin-skill 优化

*Session captured: 2026-08-31*

## Topics Covered

1. **第 0831 期 Homebrew 周报生成**(完成)
2. **darwin-skill 优化 brew-weekly-blog**(完成,+8.5 分)
3. **wiki-switch 切到 notes vault**(完成,实际为 idempotent 操作)
4. **本次 wiki-capture 知识归档**(完成)

## Key Takeaways

### 1. brew-weekly-blog 0831 期内容判断

**主题线索**:「客户端这件事正在被各种方向重做」

跨期叙事(0826 → 0817 → 0813 → 0831):
- 0826: agent 文件柜(deja-vu, skills-manager)
- 0817: 模型版本号有自己的家(inshellisense, ds4-control)
- 0813: agent 终于有工单(kata, opencrabs)
- **0831: 客户端被各种方向重做(readwise-cli, tele, crisp, betterglobekey)**

每个工具都有明确入选门槛:

- **readwise-cli** — 信号(产品对 agent 的态度在变化:从讨好 agent 到防 prompt injection)
- **tele** — 信号 + 对话(cgo-free 路线,b4n/bluetuith 同曲线延伸)
- **crisp** — 对话(b4n/bluetuith 是基础设施兜底,crisp 是显示器)
- **betterglobekey** — 细节(Globe 键具体到一个被重做的小工具)

### 2. 数据获取失败的处理

`brew update` 当周没有显示新增段(GitHub API 显示只有 outdated,新增 PR 要查 commit),fallback 到 GitHub Search API:

```bash
curl "https://api.github.com/search/issues?q=repo:Homebrew/homebrew-core+is:pr+is:merged+merged:2026-08-27..2026-08-31+label:%22new+formula%22&per_page=100"
```

`fetch_brew_activity.py` 因 token 401 失败 → 直接用 brew + GitHub Search 双源拼接。

这些 fallback 路径就是 darwin-skill Round 1 加的三段式 fallback 表里第 1-3 条的具体触发。

### 3. darwin-skill 优化记录

**Phase 1 baseline = 78.0**

最低维度:dim3(失败模式编码)= 6/10

**Round 1 = 85.7** (Δ=+7.7)
- 主杠杆:7 条三段式 fallback 表
- 顺带:发布前 8 条 CHECKPOINT(对齐反例黑名单)、Step 编号 3a/3b 修复

**Round 2 = 86.5** (Δ=+0.8)
- Runtime 红线清除(README "在 Claude Code 中调用此 skill" → "兼容任何支持 Agent Skills 标准的 runtime")
- 文件结构描述修正(`brew-weekly-template.md` 在根目录不是 assets/)
- 触发 HL-4:Round 2 Δ < 2,**见好就收,break 进 Phase 3**

### 4. wiki-switch 状态确认

`/wiki-switch notes` 是 idempotent 操作——`config` symlink 已经指向 `config.notes`。列出现有 vault:
- `notes` ← active
- `experience`(备用)

## Decisions Made

| 决策 | 理由 |
|---|---|
| 第 0831 期主题定为「客户端被各种方向重做」 | 跨期线索最强、且本期 4 个重点工具都有同一观察角度 |
| readwise-cli 放第一 | 它代表「产品对 agent 态度在变」——这是 2026 年稀有的、值得记的产品设计决策 |
| crisp 不配图,降级 ASCII | 官网只有单屏截图,ASCII 描述更紧凑 |
| betterglobekey 降级 ASCII | 键盘配置类工具,文字说明已足够 |
| 不为凑数硬写第 5 个重点 | 反例黑名单 #2 明确禁止 |
| Round 2 见好就收 | HL-4 触顶信号,Δ < 2 → break |
| Runtime 红线归类为 P0 | darwin-skill 强制 gate 项,不是可选改进 |

## Open Questions

1. **homebrew 周报未来主题线索如何避免「agent 工具链」单一曲线的疲劳?** 当前已连续 4 期围绕 agent——下一步可能需要切换到本地化 / 显示器 / 输入法 / 隐私 等新方向。

2. **brew-weekly-blog 的 dim8 实测是否需要每个 round 都重跑?** 本次 Round 1/2 没重测,假设保持——但严格来说 dim8 应该是每一轮都跑一次完整周报对比。资源权衡:跑一次完整周报 30+ 分钟,2 轮就 1 小时。

3. **darwin-skill 的 test-prompts.json 是否需要在每次优化后更新?** brew-weekly-blog 的 test-prompts.json 是这次新建的,下次优化可能需要根据当时的实际使用场景调整。

## Related

- [[synthesis/darwin-skill-brew-weekly-blog-optimization]] — 完整优化记录
- [[concepts/three-segment-fallback-table]] — 本次提炼的设计模式
- [[entities/homebrew-weekly-blog-skill]] — 被优化的 skill
- [[skills/darwin-skill-evaluation-rubric]] — 9 维评分框架
- [[homebrew-weekly-20260831]] — 本次生成的周报(若 vault 已索引)
