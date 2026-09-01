---
title: Agent Teams 显示模式 × Agent Teams 特性 — 抽象与功能的耦合约束
category: synthesis
tags:
  - claude-code
  - agent-teams
  - tmux
  - iterm2
  - pane-management
  - feature-flag
  - experimental
sources:
  - "[[concepts/agent-team-display-modes]]"
  - "[[entities/claude-code-agent-teams-feature]]"
  - "[[concepts/agent-team-cost-overhead]]"
  - "[[concepts/agent-team-mailbox-protocol]]"
  - "[[skills/tmux-agent-teams-pane-workflow]]"
  - "[[concepts/agent-team-race-condition-task-claim]]"
created: 2026-08-31T04:27:59Z
updated: 2026-08-31T04:27:59Z
summary: 显示模式抽象(in-process / split-panes / auto / tmux / iterm2)的五个值不是平行选项——它们和特性门控 env var、token 成本、tmux 实战 skill 形成一张耦合约束网。理解了耦合就理解了为什么官方推荐 tmux/auto 而非 in-process。
tier: supporting
lifecycle: draft
lifecycle_changed: 2026-08-31
base_confidence: 0.78
provenance:
  extracted: 0.65
  inferred: 0.30
  ambiguous: 0.05
relationships:
  - target: "[[concepts/agent-team-display-modes]]"
    type: synthesizes
  - target: "[[entities/claude-code-agent-teams-feature]]"
    type: synthesizes
  - target: "[[concepts/agent-team-cost-overhead]]"
    type: related_to
  - target: "[[skills/tmux-agent-teams-pane-workflow]]"
    type: related_to
---

# Agent Teams 显示模式 × Agent Teams 特性

## The Connection

`teammateMode` 五个取值看起来是平行选项(`in-process` / `split-panes` / `auto` / `tmux` / `iterm2`),但实际它们 _不是_——`agent-teams-feature` 的 4 组件架构 + 9 限制对每个模式施加了不同的可行性约束。`in-process` 模式理论上免费,但 `agent-team-cost-overhead` 揭示 teammate 数线性放大 token;`tmux` / `iterm2` 看似最重,反而是唯一能把"可观测性"和"可介入性"两个需求同时满足的选项。这两个页面单看都不够——只读显示模式看不到 _为什么推荐 tmux_,只读特性架构看不到 _为什么有 5 个而非 1 个模式_。

## Where They Co-occur

7 个 wiki 页同时引用两者,典型语境:

- **tmux 实战层**:[[skills/tmux-agent-teams-pane-workflow]] 的 3 pane 操作(zoom/detach/scroll) + Delegate 模式防抢活——只有显示模式选 tmux/auto 才能用上
- **成本约束驱动选型**:[[concepts/agent-team-cost-overhead]] 推荐 3-5 teammates + 5-6 tasks per teammate,这一预算的 _可视化前提_ 是 split-panes/tmux 的多窗格显示
- **架构组件 ↔ 显示介质**:entity 页的 4 组件(team-lead / mailbox / IPC / display)在不同模式下 IPC 走进程内管道(in-process)或 OS 进程(tmux/iterm2),成本模型随之分裂
- **race-condition 容错**:[[concepts/agent-team-race-condition-task-claim]] 的 file-locking 机制在 in-process 模式下意义减弱(共享内存即可),在 tmux/iterm2 模式下才显出价值

## Cross-cutting Insight

**显示模式不是 UI 选择,它是 _隔离域_ 选择**。每个 `teammateMode` 值定义了 teammate 进程的边界:

| 模式 | 进程边界 | IPC 通道 | 可观测性 | 可介入性 | 推荐场景 |
|---|---|---|---|---|---|
| `in-process` | 同一 Claude Code 进程 | 内存管道 | 低(共享 stdout) | 低(无独立 pane) | 调试、小规模 |
| `split-panes` | 同进程 + 多 pane | 内存管道 | 中(独立窗格) | 中(可单独 focus) | 临时实验 |
| `auto` | OS 子进程 | 自动选择 | 中–高 | 中 | 一般默认 |
| `tmux` | 独立 OS 进程 | file + tmux socket | 高(独立 pane + 状态条) | 高(pane 独立 detach) | **生产** |
| `iterm2` | 独立 OS 进程 | file + AppleScript | 高 | 高(macOS 限定) | macOS 生产 |

`teammateMode` 单次 CLI flag 与 `settings.json` 等效,但 _运行时切换_ 是有损的(已在跑的 teammate 进程不会跟着改)。这把"选 mode"推到 _启动前决策_——配合 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` 的特性门控,实际用法是"决定要做 Agent Teams → 选 mode → 启进程 → 跑全程"。^[inferred]

## Tensions and Trade-offs

- **可观测性 ↔ 启动开销**:tmux/iterm2 模式每个 teammate 一个独立进程,启动 + 状态同步成本约 200–500ms/进程;3 teammates 损失 ≈ 1s。但换来的是 _任意时刻可以 Ctrl-B z 放大 pane 看日志_——这把"调试延迟"换成"运行延迟"
- **可介入性 ↔ 自动化**:in-process 模式无法中途"接管"一个 teammate——它和 lead 共享 stdout;tmux/iterm2 模式下可 `tmux attach` + 直接对 pane 输入
- **跨平台 ↔ 模式覆盖**:`iterm2` 只在 macOS 有效——Linux 用户只剩 tmux。auto 模式依据平台自动选择,但选择 _逻辑不公开_
- **特性门控 ↔ 文档稳定性**:整个 Agent Teams 是 experimental(`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` + v2.1.178+),9 个已知限制中包含"mailbox 偶尔丢消息"——显示模式的 _所有优点_ 都不抵消这条不稳定性

## Strongest Objection

**批评**:把 `teammateMode` 当成"隔离域选择"是 _后见之明_——Anthropic 推出 5 个模式的初衷大概率是 _用户偏好_ 而不是 _架构分层_。把"推荐 tmux"包装成"工程最佳实践"是过度解读;真实情况可能是 _tmux 在 early adopters 中呼声最高_,官方文档才把它放进 default `auto` 优先级。

> test: 翻 `claude-code-agent-teams-feature` 历史的 changelog(`v2.1.178` → `v2.1.220+`),看 `teammateMode` 字段是否曾从 _6+ 值_ 简化为 _5 值_。如果早期版本有过"in-process / panes / vscode / tmux / iterm2 / 远程 SSH"等更多选项,后被官方收敛,说明选型是被 _用户反馈_ 驱动而非 _架构理论_ 驱动。

## Open Questions

- `teammateMode` 是否会支持"混合模式"——lead 跑 tmux、worker 跑 in-process 以降低总成本?
- vault 当前对 `auto` 模式的 _真实选择逻辑_ 没有权威描述;是否存在公开算法?
- `split-panes` 模式与 [[skills/tmux-agent-teams-pane-workflow]] 的 3-pane 操作有重叠,但 tmux skill 假设 _已经是 tmux 模式_。两者在 `split-panes` 模式下的关系是冗余还是替代?
- 9 个已知限制的完整列表未在 vault 中集中——是 wiki-lint 候选,值得补一篇 [[references/claude-code-agent-teams-known-issues]]

## Related

- [[concepts/agent-team-display-modes]]
- [[entities/claude-code-agent-teams-feature]]
- [[concepts/agent-team-cost-overhead]]
- [[concepts/agent-team-mailbox-protocol]]
- [[concepts/agent-team-race-condition-task-claim]]
- [[skills/tmux-agent-teams-pane-workflow]]
- [[synthesis/Research: Claude Code Agent Teams]]
- [[concepts/claude-code-agent-teams]]