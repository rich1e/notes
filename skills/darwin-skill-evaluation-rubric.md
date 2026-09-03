---
title: >-
  Darwin-Skill Evaluation Rubric — 9 维评分框架
category: skills
tags: [darwin-skill, evaluation, rubric, skill-optimization, dim8, score-system]
sources:
  - conversation:2026-08-31
created: 2026-08-31T13:50:00Z
updated: 2026-08-31T13:50:00Z
summary: >-
  darwin-skill 的 9 维评分框架速查 — 6 个结构维度 + 1 个实测维度 + 1 个反例维度 + 1 个 meta 维度,权重总和 100,实测维度(dim8)权重最大(23)。
provenance:
  extracted: 0.5
  inferred: 0.5
  ambiguous: 0.0
base_confidence: 0.8
lifecycle: draft
lifecycle_changed: 2026-08-31
---

# Darwin-Skill Evaluation Rubric — 9 维评分框架

> 来源:`/Users/rich1e/.claude/skills/darwin-skill/SKILL.md`。
> 基于 SkillLens 论文(arXiv 2605.23899)+ SkillOpt 论文(arXiv 2605.23904)。

## 9 维评分表

| # | 维度 | 权重 | 评分标准 |
|---|---|---|---|
| 1 | Frontmatter 质量 | 7 | name 规范、description 含触发词、≤1024 字符、**禁空话尾巴** |
| 2 | 工作流清晰度 | 12 | 步骤明确可执行、有序号、每步有明确输入/输出 |
| 3 | **失败模式编码** | 12 | **必须显式编码失败模式**(写出「如果 X 失败 → Y」);有 fallback 路径、错误恢复 |
| 4 | 检查点设计 | 6 | 关键决策前有用户确认;**检查点必须显性标记(🔴/STOP/CHECKPOINT)** |
| 5 | 可执行具体性 | 17 | 不模糊、有具体参数/格式/示例;**禁止「建议/可以考虑/根据情况」等软化措辞** |
| 6 | 资源整合度 | 4 | references/scripts/assets 引用正确、路径可达 |
| 7 | 整体架构 | 12 | 结构层次清晰、不冗余不遗漏、与花叔生态一致;**冗余/AI 腔废话扣分** |
| 8 | **实测表现** | 23 | 用测试 prompt 跑一遍,对比 baseline 与带 skill 的输出 |
| 9 | **反例与黑名单** | 6 | 必须有「不要做什么」的反例清单;只写「应该做 X」扣 ≥3 分 |

## 评分规则

- 维度 1-7、9:每个维度打 1-10 分,乘以权重得到该维度得分
- 维度 8:跑 2-3 个测试 prompt,按输出质量打 1-10 分
- **总分 = Σ(维度分 × 权重) / 10**,满分 100
- 改进后总分必须**严格高于**改进前才保留

## HL 操作精髓(High-Leverage)

- **HL-1(dim4)**:显性视觉标记(🔴 CHECKPOINT / 🛑 STOP)是杠杆。靠「必须」措辞不行——LLM 解析时扫描视觉标记。4 行改动撬动 dim4 +3 分
- **HL-2(dim3)**:if-then 三段式 fallback 表(触发条件 / 一线修复 / 仍失败兜底)
- **HL-3**:dim2/3/4 是相关簇——修 dim3 时 dim2 常跟着涨
- **HL-4**:连续 2 轮 Δ < 2 分 → break,见好就收

## 实战数据

- brew-weekly-blog 2026-08-31:78.0 → 86.5 (+8.5),2 轮 keep 0 回滚
- huashu-gpt-image: +10.85
- huashu-weread-advisor: +14.9
- claude-design: +16.5
- (详见 [[synthesis/darwin-skill-brew-weekly-blog-optimization]] 的实战记录)

## 配套工具

- **Runtime 红线扫描**:`grep -nE "(在 Claude Code|Claude Code skill|...)"` SKILL.md
- **test-prompts.json**:每个 skill 目录存 2-3 个测试 prompt,用于 dim8 实测
- **results.tsv**:每次优化的基线/keep/revert 记录

## Related

- [[concepts/three-segment-fallback-table]] — HL-2 的具体形态
- [[concepts/darwin-ratchet-mechanism]] — HL-4 的机制
- [[synthesis/darwin-skill-brew-weekly-blog-optimization]] — 实战示例
- [[journal/2026-08-31-darwin-brew-weekly-optimization]] — 本次 session
