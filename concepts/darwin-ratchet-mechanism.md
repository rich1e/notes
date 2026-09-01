---
title: >-
  Darwin Ratchet Mechanism
category: concepts
tags: [darwin-skill, ratchet, optimization, hill-climbing, dim5, handoff-decision]
sources:
  - conversation:2026-08-31
created: 2026-08-31T14:00:00Z
updated: 2026-08-31T14:00:00Z
summary: >-
  Darwin-skill 的棘轮机制:只保留改进版本,自动回滚退步;HL-4 触顶信号(连续 2 轮 Δ<2)作为见好就收的自动 break 条件,防止为凑分增冗余。
provenance:
  extracted: 0.4
  inferred: 0.6
  ambiguous: 0.0
base_confidence: 0.8
lifecycle: draft
lifecycle_changed: 2026-08-31
---

# Darwin Ratchet Mechanism

## What It Is

Darwin-skill 的**单向棘轮优化机制**:每个优化循环只接受分数严格更高的版本,退步自动 revert。HL-4 触顶信号作为自动 break 条件,防止 hill-climbing 陷入局部最优或为凑分增冗余。

## How It Works

### 棘轮核心

```bash
if 新总分 > 旧总分:
  status = "keep"
else:
  status = "revert"
  git revert HEAD  # 不用 reset --hard,保留可追溯链
```

**绝对单向**:不靠"差不多"判断,严格 > 才保留。

### HL-4 触顶信号

```
if last_delta < 2.0 and this_delta < 2.0:
  print("触顶信号:连续 2 轮边际收益 < 2 分,停止优化避免过度调整")
  break
```

**为什么是 2 分**:Round 1 涨 7+ 分(有意义改进)→ Round 2 涨 < 2 分(可能是凑字数)。分界线经验值。

### 防反模式

- **同 context 自评自改**:改完后立刻打分会有乐观偏差(SkillLens 实证 LLM-as-judge 仅 46.4%)→ 必须独立子 agent
- **为凑分增冗余**:Round 1 涨分内容沉淀下来后,Round 2+ 没有真改进就是凑数 → HL-4 break
- **跳过 test-prompts**:没有实测的 dim8 是凭空打分,权重 23% 等于编造 → Phase 0.5 强制

## When to Use

适用:
- 任何 hill-climbing 类优化流程
- A/B 测试之外没有明确 ground truth 但需要可量化的迭代
- 多维度评分系统(dim1-9)的优化

不适用:
- 一锤子定型的任务
- 需要 human-in-the-loop 重判断的场景(本机制是为了减少 human 判断频次)

## 实战数据

2026-08-31 brew-weekly-blog 优化:
- Round 1 Δ=+7.7(keep,三段式 fallback 表)
- Round 2 Δ=+0.8(keep,但 HL-4 触发 break)
- 总分 +8.5,**0 回滚**

如果硬凑 MAX_ROUNDS=3,会进入「为凑分增冗余」反模式——加废话/加段落让 LLM 觉得更详细,实际质量不变。

## Related

- [[skills-darwin-skill-evaluation-rubric]] — 评分依据
- [[synthesis-darwin-skill-brew-weekly-blog-optimization]] — HL-4 实战记录
- [[concepts-three-segment-fallback-table]] — 与 dim3 优化的关系
- [[journal-2026-08-31-darwin-brew-weekly-optimization]] — 本次 session
