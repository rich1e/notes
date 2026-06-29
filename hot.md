---
title: Hot Cache
updated: 2026-06-29T10:00:00Z
---

# Hot Cache

*A ~500-word semantic snapshot of recent activity. Updated after every major write operation.*

## Recent Activity

- [2026-06-29T10:00:00Z] WIKI_UPDATE xk-ai-talk-desk-ui — 首次同步，创建 4 页：项目总览、CC SDK 集成（useSoftbar）、坐席状态机、PhoneBar 通话流程
- [2026-06-29T09:30:00Z] INGEST Clippings/ — 15 个网页剪藏蒸馏为 13 个 wiki 页面，覆盖 Claude Code 优化、前端核心概念、复古游戏与工具类知识
- [2026-06-29T09:16:46Z] INIT — vault created at /Users/rich1e/workspace/code/notes

## Active Threads

**xk-ai-talk-desk-ui（进行中）**：AI 外呼热转坐席前端，`dev_1.0.0` 分支活跃开发。核心是 `useSoftbar` Hook 封装信科 LaihuAPI，事件驱动管理通话生命周期。当前迭代聚焦：热转/手动详情字段调整、电话条样式优化、日期组件优化。

**Claude Code 知识集群**：已建立 `skills/claude-code-token-optimization` 和 `skills/claude-code-settings` 两个核心页面，`concepts/prompt-caching` 作为理论基础页面支撑两者。

**前端核心概念**：已建立 Event Loop → 浏览器进程模型 → 存储缓存 → 移动端定时器四页互链体系。

## Key Takeaways

- **信科 CC SDK 集成关键**：双通道签入（CC only vs CC+WebRTC），外呼号码须加 `9` 前缀；`DeliveredEvt.dialogue` 携带 AI 对话历史，是热转场景的核心数据
- Claude Code 提示缓存：**缓存热时继续聊比重开更便宜**；1M 上下文慎用（缓存失效代价极高）
- 移动端定时器不准根因：浏览器对后台页面冻结定时器；解法：visibilitychange + 服务器时间差值
- NDS 最佳烧录卡：DS Two（已停售）；GBA Slot-2：SuperCard Mini SD + SuperFW 固件

## Flagged Contradictions

*None yet.*
