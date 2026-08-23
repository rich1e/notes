---

title: 确定性 agent 记忆(非概率的"事实层")
category: concepts
tags:
  - ai-agent
  - memory
  - deterministic
  - ai-safety
  - openlore
  - claude-mem
sources:
  - https://github.com/clay-good/OpenLore
  - _raw/_archived/github-clay-good-OpenLore.txt (gitingest export, clay-good/OpenLore, 2026-08-03)
created: 2026-08-03T12:15:00Z
updated: 2026-08-23T09:05:00Z
summary: 用确定性算法(图分析 / BM25 / grep / git diff / 签名比对)而非 embedding 检索,给 agent 提供"事实层"记忆:同问题同答案、stale 显式标注、引用可点回源码。
tier: supporting
lifecycle: draft
lifecycle_changed: 2026-08-03
base_confidence: 0.82
provenance:
  extracted: 0.92
  inferred: 0.08
  ambiguous: 0
relationships:
  - target: "[[entities/openlore]]"
    type: derived_from
  - target: "[[concepts/static-analysis-knowledge-graph]]"
    type: extends
  - target: "[[concepts/no-llm-hot-path]]"
    type: related_to
  - target: "[[concepts/claude-mem-memory-architecture]]"
    type: related_to
  - target: "[[concepts/agent-operating-system]]"
    type: related_to

---
# 确定性 agent 记忆(非概率的"事实层")

> "An agent's expensive failure mode isn't ignorance — it's confidence." —— OpenLore README
>
> 模型不知道某函数存在会去查;模型"知道"一个**陈旧的事实**会自信地基于它盖楼,review 时一起付账。

## 一句话定义

agent 拿到一个事实 / 一个推荐 / 一个判定时,**能立刻回放到具体代码行或 commit 的引用链**——而不是 embedding 余弦相似度的模糊排序。

## 为什么这跟"普通 agent memory"不一样

| 维度 | 普通 memory(SQLite + embedding) | 确定性 fact layer |
|---|---|---|
| 回答一致 | 同 query 可能不同(model drift / 服务版本) | 同一仓库永远一致 |
| 失败模式 | "看起来对" — 静默错 | 显式 stale / unresolved / no-evidence |
| 引用 | "nearest match" 百分比 | 文件 + 行号 + commit hash |
| 离线可用 | embedding 服务挂了降级或不可用 | 完全离线 |
| 成本 | 持续 token / API 费用 | 一次性 CPU + 磁盘 |
| 适合承担 | "我们上次怎么修的?" | "X 函数还安全吗?" |

## 三大支柱(OpenLore 的实现)

### 1. **静态分析图作骨架**

详见 [[concepts/static-analysis-knowledge-graph]]。每条边可追到源码,可重放。

### 2. **BM25 + 签名比对作 fallback**

无 embedding 服务时 `search_code` / `orient` / `suggest_insertion_points` 自动降级到 BM25 关键词检索 + 签名级比对。语义弱但**确定**。

### 3. **freshness verdict(stale 显式标注)**

```
fresh     索引与文件一致,offset 可信,带 contentHash 完整性 token
stale     文件已变,只给 re-analyze 提示,**不给 offset**(拒绝给你一个自己都没验证过的字节位置)
ambiguous 同一名字 + 路径有多个候选,返回候选列表,**不**模糊猜
not-found 不给相似替代
```

`locate_symbol_span` 工具的返回格式——这是 agent "**精确编辑已知符号**"的安全契约。

## "事实层"接哪几类问题

| 问题 | 确定性回答的来源 |
|---|---|
| "实现 X 的函数在哪?" | call graph + signature index |
| "改 X 会影响哪些 caller?" | 逆向依赖闭包 |
| "X 是否还合并在 main?" | git ref reachability |
| "X 是否被某个 spec 覆盖?" | spec → source file 映射 |
| "上次人批准的决策是?" | synced ADR + `record_decision` 链 |
| "改 X 后是否打开了 sensitive boundary?" | 边界声明 × 改后可达图 |
| "agent 说 X 是 dead code,对吗?" | `verify_claim` 返回 confirmed/refuted/unverifiable + Evidence |

## 反面:概率记忆的失效模式

- ❌ "X 大概是 dead code" → LLM 据此改 → caller 静默受影响
- ❌ "这个 spec 跟我的工作相关" → 实际已过时 → 在错的契约上盖楼
- ❌ "上次修过类似问题" → 实际是更老的会议笔记,跟代码现状无关
- ❌ "找到 5 个可能的 import" → 缺 fresh 验证,选了一个 stale 的

确定性 fact layer 的核心价值不是"答得准",而是**答得显式**:stale 显式、unverifiable 显式、not-found 显式。Agent 拿不到"模糊对",就只能回去查或停下来问。

## 与 vault 已有 memory 簇的关系

- **claude-mem**(PostToolUse hook 捕获 → haiku 压缩 → SQLite + Chroma 注入) → **补 session 间的"经验记忆"**(怎么修过哪些 bug、做过哪些决策)
- **OpenLore**(静态分析 → 图 + 签名 → on-disk 索引) → **补"代码结构记忆"**(代码本身的形状与契约)
- **两者正交不重叠**:

| 类型 | 持久化 | 触发 | 内容 |
|---|---|---|---|
| claude-mem | SQLite + Chroma | hook | observation、decision 摘要、session 摘要 |
| OpenLore | JSON 图 + BM25 + 可选 vector | 主动调用 MCP | 函数签名、调用关系、spec 覆盖、决策 Evidence |

详见 [[concepts/claude-mem-memory-architecture]] 与 [[concepts/agent-operating-system]]。

## 实现这个模式的清单

```text
[ ] 同 query 永远返回同答案(确定性算法,无随机)
[ ] 每条事实带显式引用(file:line / commit / ADR id)
[ ] stale 显式标注,不静默给错位置
[ ] 离线 / 无 embedding 也能降级到 BM25 / 签名匹配
[ ] LLM 完全不在 hot path
[ ] freshness verdict + contentHash 完整性 token
[ ] agent 拿不到"模糊对"——只有 fresh / stale / ambiguous / not-found
[ ] 增量 watch 模式设 stale 边界(超过预算显式标 stale,不静默)
[ ] "Honesty contract":亏损挨着赢一起发,benchmark 全公开
```

## 谁该用确定性 fact layer

- 私有 / 垂直 / 模型没训过的代码
- Polyglot + IaC 仓库(单一 embedding 模型覆盖不全)
- CI / pre-commit 必须给可重放结果
- 长期 agent 任务(decision 几个月后还要查得回)
- 多人 / 多 agent 协作(必须同 query 同答案)

## 相关

- [[entities/openlore]] —— 参考实现
- [[concepts/static-analysis-knowledge-graph]] —— 图骨架
- [[concepts/no-llm-hot-path]] —— hot path 设计原则
- [[concepts/commit-gate-guardrails]] —— 落地到 CI
- [[concepts/claude-mem-memory-architecture]] —— 互补的经验记忆层
- [[concepts/agent-operating-system]] —— 上层五层 memory 框架

## Related

- [[synthesis/concepts-deterministic-agent-memory × entities-bmad-method|确定性 Agent 记忆 × BMad 方法论]] — synthesis
