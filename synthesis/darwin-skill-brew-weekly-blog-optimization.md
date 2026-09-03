---
title: >-
  Darwin-Skill 9 维评估在 brew-weekly-blog 上的实战
category: synthesis
tags: [darwin-skill, skill-optimization, Homebrew, brew-weekly-blog, evaluation-rubric, runtime-neutrality]
sources:
  - conversation:2026-08-31
created: 2026-08-31T13:30:00Z
updated: 2026-08-31T13:30:00Z
summary: >-
  用 darwin-skill 评估并优化 brew-weekly-blog 的完整实战记录:基线 78.0 → 86.5 (+8.5),两轮 keep 0 回滚,三段式 fallback 表+发布前 CHECKPOINT 是主要杠杆,Runtime 红线修复是隐性 gate 项。
provenance:
  extracted: 0.7
  inferred: 0.3
  ambiguous: 0.0
base_confidence: 0.85
lifecycle: draft
lifecycle_changed: 2026-08-31
---

# Darwin-Skill 9 维评估在 brew-weekly-blog 上的实战

## Context

[[skills/darwin-skill-evaluation-rubric]] 的 9 维评分框架已在多次 skill 优化中验证,但本实战是**第一次在「跨期上下文密集 + 数据依赖外部 API + 强叙事写作类」的复杂 skill 上跑完整流程**。brew-weekly-blog 不仅要执行工具命令,还要生成有文风的博客——dim8(实测表现)的评估本身就需要生成一份完整产物。

评估时点:2026-08-31,目标 skill 文件体积 684 行,已有较成熟的反例黑名单(dim9 是已知强项)。

## Finding / Decision

**两轮 keep 0 回滚 +8.5 分,杠杆集中在 dim3 + dim4,dim6 由 Runtime 红线 gate 触发。**

具体数值:

| 维度 | 基线 | R1 | R2 | 权重 | 改进来源 |
|---|---|---|---|---|---|
| 1 Frontmatter | 7 | 7 | 7 | 0.07 | 未动 |
| 2 工作流清晰度 | 8 | 9 | 9 | 0.12 | Step 编号修复 3a/3b(原 4/3 倒序) |
| **3 失败模式编码** | 6 | 9 | 9 | 0.12 | **+3**:7 条三段式 fallback 表 |
| **4 检查点设计** | 7 | 9 | 9 | 0.06 | **+2**:发布前 8 条 CHECKPOINT 打勾清单 |
| 5 可执行具体性 | 8 | 9 | 9 | 0.17 | fallback 表给具体 curl/PR 查询参数 |
| **6 资源整合度** | 7 | 7 | 9 | 0.04 | **+2**:Runtime 红线清除 + 文件结构修正 |
| 7 整体架构 | 8 | 8 | 8 | 0.12 | 未动 |
| 8 实测表现 | 9 | 9 | 9 | 0.23 | 同期跑过一次完整周报 |
| 9 反例黑名单 | 9 | 9 | 9 | 0.06 | 已是本 skill 强项,未动 |

总权重分:(7×0.07 + 9×0.12 + 9×0.12 + 9×0.06 + 9×0.17 + 9×0.04 + 8×0.12 + 9×0.23 + 9×0.06) × 10 = **86.5**

## Reasoning

### 三段式 fallback 表为什么是 dim3 的核心杠杆

dim3 满分要求"显式编码失败模式:写出'如果 X 失败 → Y'的明确分支",原文仅在末尾「故障排除」章节提 API 401/403。

Round 1 把 fallback 搬到「失败模式与 Fallback(必读)」独立章节,**且每条用「触发条件 / 一线修复 / 仍失败兜底」三段式**——这比单纯的「症状/解法」两列多一层决策路径。SkillLens 论文(meta-skill failure-mechanism encoding 维度)的实证:三段式让 LLM 在解析时能 step-by-step 匹配,而不是只看到症状再倒推解法。

7 条具体场景:

| 触发条件 | 一线修复 | 仍失败兜底 |
|---|---|---|
| `brew update` 无新增段 | GitHub Search API 查 PR(给完整 curl) | 走"零新增"策略 4 |
| API `403 rate limit` | 等 60s 重试或减小 per_page | 走脚本路径 |
| `401 Unauthorized` | 检查 token 格式/source .zshrc | brew + GitHub Search 双源拼接 |
| 图片三步全失败 | GUI/TUI 降级 ASCII,CLI 不配图 | 删去该工具推荐位 |
| WebFetch README 空 | `brew info` + GitHub API `/repos/` | 移出重点,在感受带过 |
| 跨期内容重叠 | 换角度聚焦具体拐点 | 当期退场式收尾 |
| README 含不安全字样但作者未标注 | 不写重点,感受里说顾虑 | 删除该工具 |

### Runtime 红线是隐性 gate,不是 dim6 子项

darwin-skill 强制 Runtime 适配性审查(`grep -nE "(在 Claude Code|Claude Code skill|...)"`)。brew-weekly-blog 的 README 第 14 行命中 "在 Claude Code 中调用此 skill"——这是一个 **P0 gate 项**,即使结构分都满分,Runtime 措辞问题也会让 skill 在其他 runtime(Marvis / OpenClaw / Hermes 等)被拒装。

修复模板:

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

**伴生修复**:文件结构描述要从 `assets/brew-weekly-template.md` 改成实际路径(项目根目录)。这个错误本身在反例黑名单 dim9 #7 里,但仅在 README 才出现。

### HL-4 触顶信号实战

Round 1 Δ=+7.7,Round 2 Δ=+0.8。Round 2 < 2,触发见好就收。

如果硬凑 MAX_ROUNDS=3,**会进入 HL 反例黑名单 #3「为凑分增冗余」**——加废话/加段落让 LLM 觉得更详细,实际质量不变。本实战的正确做法:Round 2 之后 break 进 Phase 3,**+8.5 是有意义改进,不是凑数**。

## Implications

### 可复用模式

1. **「数据依赖外部 API + 强叙事写作」类 skill 的优化第一刀都在 dim3**——这类 skill 的失败模式天然分散(数据获取/工具研究/图片/写作各一段),把它显式编码成三段式 fallback 表几乎是必杀技。

2. **Runtime 红线扫描应该在 Phase 0 启动时跑一次,而不是优化完才发现**。本实战的 Round 2 是「顺手修了 Runtime 红线」,理想路径是 Phase 0 baseline 时就把 runtime_warn 标记到 results.tsv。

3. **发布前 CHECKPOINT 比筛选 CHECKPOINT 更重要**。筛选 CHECKPOINT(选哪些工具)是「该选哪个」的判断,发布前 CHECKPOINT(8 条打勾清单)是「这一篇能不能发」的硬性拦门——后者对最终质量的影响远大于前者。

4. **HL-4 触顶信号在 dim5(具体性)维度最容易误判**。具体性补 fallback 参数会让 dim5 涨,但如果内容是「为具体而具体」(罗列),Δ 会小。要区分「真正涨分」和「凑字数」。

### 不应套用本经验的场景

- **新建 skill(基线 0)**——darwin-skill 优化的是「已有 SKILL.md」,不适用从零起草
- **纯执行型 skill(无 dim8 写作维度)**——dim8 实测会变成 dry_run,失去基线意义
- **运行时频繁变动的 skill**——例如 Claude Code 设置类,基线本身会过期

## Related

- [[skills/darwin-skill-evaluation-rubric]] — 9 维评分框架
- [[concepts/three-segment-fallback-table]] — 三段式 fallback 设计模式(本次实战提炼)
- [[skills/skill-runtime-neutrality-grep]] — Runtime 红线扫描的固化流程
- [[concepts/darwin-ratchet-mechanism]] — ratchet 机制 + HL-4 触顶信号
- [[entities/homebrew-weekly-blog-skill]] — 本次被优化的 skill 实体
- [[journal/2026-08-31-darwin-brew-weekly-optimization]] — 本次实战的 session journal
