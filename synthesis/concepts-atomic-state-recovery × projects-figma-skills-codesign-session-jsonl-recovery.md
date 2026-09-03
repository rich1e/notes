---
title: "Session JSONL 作为 Second Source — 状态破坏时的二次证据路径"
category: synthesis
tags: [atomic-state-recovery, session-log, jsonl, codesign, Claude, treehouse, synthesis]
sources:
  - "[[concepts/atomic-state-recovery]]"
  - "[[projects/figma/skills/codesign-session-jsonl-recovery]]"
  - "[[concepts/durable-session-log]]"
  - "[[concepts/turn-step-flow]]"
created: 2026-08-24
updated: 2026-08-24
summary: 多源项目（CoDesign、Claude Code Agent Teams、treehouse、deepseek-harness）都将 session JSONL 作为状态的二次证据路径：主工作流（设计 / 工具 / agent）有完整快照失败风险时，JSONL append-only 日志是按时间窗回放重建的可靠来源。核心抽象：原子性破坏 ≠ 数据丢失。
base_confidence: 0.85
provenance:
  extracted: 0.55
  inferred: 0.40
  ambiguous: 0.05
lifecycle: draft
lifecycle_changed: 2026-08-24
tier: supporting
relationships:
  - target: "[[concepts/atomic-state-recovery]]"
    type: extends
  - target: "[[concepts/durable-session-log]]"
    type: related_to
---

# Session JSONL 作为 Second Source — 状态破坏时的二次证据路径

## 核心抽象

多个看似无关的项目共享同一个模式：**主工作流的原子快照破坏后**，**session JSONL 的 append-only 日志成为重建的二次证据**。

| 项目 | 主工作流 | JSONL 来源 | 重建方式 |
|---|---|---|---|
| **CoDesign (figma)** | 自包含 JSX 在 artifact 中编辑 | `~/Library/Application Support/@open-codesign/desktop/sessions/<designId>.jsonl`（8MB 审计日志） | 按时间窗截取 + 模糊匹配回放 `create` / `str_replace` / `insert` 完整操作序列 |
| **Claude Code Agent Teams** | teammate 通信 + 任务状态 | `~/.claude/teams/<team>/inboxes/<agent>.json`（每 agent 一个） | 逐条校验 inbox 条目，错误条目自动丢弃 |
| **treehouse** | worktree pool + agent sandbox | treehouse 内部 session log | worktree-durable-lease + atomic-state-recovery |
| **deepseek-harness** | Cordis 插件事件流 | dsh `durable-session-log` 抽象 | fork / resume / transcript / telemetry 全部派生 |

## 为什么是 JSONL 而不是 SQLite/快照

1. **append-only 语义**：write 永远是追加，不存在"修改某条记录"的事务。Crash 时丢失的只是"最后 N 行"，不是"任意时刻的视图"
2. **回放成本低**：按时间窗截取 + 顺序 parse 即可，无需协调多表 join
3. **不与主数据库竞争**：JSONL 是审计 / 事件流，主数据库（SQLite/Postgres）是当前状态视图 —— 两层分离，互不阻塞
4. **可被多消费者读取**：调试器 / replay 工具 / analytics pipeline 可以独立消费同一 JSONL

## 哲学对应

| 现象 | 哲学 |
|---|---|
| 状态破坏 ≠ 数据丢失 | 与 [[concepts/atomic-state-recovery]] 同源：atomic 失败时，下一层（disk / log / cloud）的恢复机制 |
| Invariant「Model-visible ⟺ logged」 | 与 [[concepts/durable-session-log]] 同源：dsh 主张事实序列是 source of truth,当前状态是派生 |
| Fork / resume / transcript 都从 JSONL 派生 | [[concepts/durable-session-log]] 的实现细节 |

## 跨域判断

**(J1)** Session JSONL 不是审计冗余，而是**主工作流原子性失败时的安全网** —— 与 git reflog 类似角色，但更细粒度（每个事件一个 JSON object）

**(J2)** 多个项目独立收敛到 JSONL 模式（无显式协调），说明这是一个**工程级共识**，而非偶然架构选择

**(J3)** 与 [[concepts/deterministic-agent-memory]] 互补：后者关注 hot-path 0 LLM（决策的稳定性），前者关注状态破坏后的恢复（系统韧性）

## 相关

- [[concepts/atomic-state-recovery]] — 原子性破坏 ≠ 数据丢失的工程哲学
- [[concepts/durable-session-log]] — dsh 的 append-only SessionEvent 抽象
- [[concepts/turn-step-flow]] — dsh agent loop 的事件流粒度
- [[projects/figma/skills/codesign-session-jsonl-recovery]] — CoDesign 的 8MB JSONL 回放实例
- [[projects/figma/concepts/screen-08-photo-wall]] — 屏8 探索早期版本因 str_replace 失败反复踩坑后的 JSONL 重建案例