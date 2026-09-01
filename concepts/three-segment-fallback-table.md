---
title: >-
  三段式 Fallback 表 — 失败模式编码的具体形态
category: concepts
tags: [fallback-design, error-recovery, darwin-skill, dim3, skill-pattern, failure-mode-encoding]
sources:
  - conversation:2026-08-31
created: 2026-08-31T13:35:00Z
updated: 2026-08-31T13:35:00Z
summary: >-
  「触发条件 / 一线修复 / 仍失败兜底」三段式 fallback 表的设计模式——比两列式「症状/解法」多一层决策路径,符合 SkillLens meta-skill failure-mechanism encoding 维度。
provenance:
  extracted: 0.6
  inferred: 0.4
  ambiguous: 0.0
base_confidence: 0.75
lifecycle: draft
lifecycle_changed: 2026-08-31
---

# 三段式 Fallback 表

## What It Is

一种**显式编码失败模式**的设计模式,把每个可预期的失败点写成「触发条件 / 一线修复 / 仍失败兜底」三段。比两列式「症状/解法」多一层决策路径。

## How It Works

### 三段结构

```markdown
| 触发条件 | 一线修复 | 仍失败兜底 |
|---|---|---|
| 明确的失败信号(错误码/异常/为空) | 第一选择(优先尝试) | 如果一线也失败,第二选择(必然成功或可接受) |
```

### 与两列式的差异

两列式:

```markdown
| 症状 | 解法 |
|---|---|
| API 401 | 检查 token |
| API 403 | 减小 per_page |
```

LLM 解析时只能看到「症状匹配后用解法」。但一线修复可能本身失败,需要兜底——这是大多数 skill 文档缺的部分。

三段式:

```markdown
| 触发条件 | 一线修复 | 仍失败兜底 |
|---|---|---|
| `fetch_x.py` 返回 `401 Unauthorized` | 检查 `~/.zshrc` 中 `GITHUB_TOKEN` 无多余空格/引号,`source ~/.zshrc` 后重试 | 直接用 `brew update` 输出 + GitHub Search API(无需 token)双源拼接 |
```

LLM 在解析时能 step-by-step 匹配,失败后还有第二路径——这是 SkillLens 论文实证的 LLM 友好形式。

### 何时用三段 vs 两段

- **三段**:失败可能连锁(API 失败 → 重试也可能失败 → 需要 fallback 路径)
- **两段**:失败是终端性的(就是某个静态错误,只有一种修法)
- **一段(只写触发条件)**:留作「不要做的事」清单的一部分,不写解法

### 三段式的隐性约束

- **触发条件必须是机器可检测的信号**——错误码、HTTP status、异常类型、空输出。模糊描述如「失败」不算。
- **一线修复必须是低成本尝试**——30 秒内能完成。如果一线修复本身需要 10 分钟,应该直接跳到兜底。
- **兜底必须是「可接受退化」而不是「完美替代」**——例如 fallback 到无 token 模式拿到 80% 数据,而不是反复重试拿 100%。

## When to Use

适用场景:

- 任何调用外部 API / 工具的 skill
- 失败模式已知且有限(可以枚举 5-10 条)
- LLM 解析 skill 后会自主执行——需要明确的失败路径

不适用场景:

- 一次性脚本(失败了就看错误,不用 codify)
- 失败模式未知且多发(只能写通用 try/except)
- 实时性极强(没时间切到 fallback,必须主路径一次成功)

## 实战来源

2026-08-31 在 [[entities-homebrew-weekly-blog-skill]] 优化中提炼。当时 dim3(失败模式编码)是最低维度(6/10),仅在末尾「故障排除」章节零散提到。Round 1 把 7 条失败场景写成三段式 fallback 表,dim3 涨到 9/10,总分 +7.7 分。

7 条场景模板:

1. **主数据源无信号**(`brew update` 无新增段) → 备用 API 查询(给完整 curl) → 「零新增」叙事策略
2. **API 限流**(`403 rate limit`) → 等 60s / 减小请求量 → 走脚本路径 / 切换数据源
3. **认证失败**(`401 Unauthorized`) → 检查 token 配置 / source 环境 → 直接用无 token 备选
4. **图片资源缺失**(三步全失败) → ASCII 降级 / 不配图 → 删除该工具推荐位(不凑数)
5. **外部信息源为空**(README 太简略) → 切换信息源(`brew info` / GitHub API) → 移出重点
6. **跨期内容重叠**(连续 N 期主题撞) → 换具体拐点角度 → 退场式收尾
7. **安全信号但作者未标注**(含 prompt injection 等字样) → 不进重点 → 删除工具

每条都满足三段式的隐性约束:机器可检测信号 / 低成本一线修复 / 可接受退化兜底。

## Related

- [[skills-darwin-skill-evaluation-rubric]] — dim3 的评分依据
- [[synthesis-darwin-skill-brew-weekly-blog-optimization]] — 7 条场景的实战上下文
- [[concepts-darwin-ratchet-mechanism]] — 触顶信号与三段式的质量关系
- [[concepts-skill-failure-mode-encoding]] — 抽象层面的失败模式编码理论
