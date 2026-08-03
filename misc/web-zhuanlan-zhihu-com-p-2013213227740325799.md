---
title: "深入理解 Claude Code 的项目记忆机制：Auto Memory + CLAUDE.md"
category: misc
tags: [claude-code, memory, ai-tools]
sources:
  - "https://zhuanlan.zhihu.com/p/2013213227740325799"
source_url: "https://zhuanlan.zhihu.com/p/2013213227740325799"
created: "2026-07-31T00:00:00"
updated: "2026-07-31T00:00:00"
tier: peripheral
summary: "知乎文章系统梳理 Claude Code 的两层项目记忆：开发者手写的 CLAUDE.md（显式规则）与 Claude 自维护的 MEMORY.md/Auto Memory（自动积累经验），含作用域、200 行限制、@ 导入、.claude/rules/ 与子智能体记忆。"
affinity: {}
promotion_status: misc
stub: false
provenance:
  extracted: 0.85
  inferred: 0.1
  ambiguous: 0.05
base_confidence: 0.45
lifecycle: draft
lifecycle_changed: "2026-07-31"
---

# 深入理解 Claude Code 的项目记忆机制：Auto Memory + CLAUDE.md

## Overview

来源于知乎专栏作者「技术极简主义」的教程文章,系统介绍 Claude Code 的**项目记忆体系**。核心观点:记忆由两个互补部分组成——开发者手动编写的 `CLAUDE.md`(显式规则)和 Claude 自动维护的 `MEMORY.md`/Auto Memory(自动积累的经验)。前者是「主动告诉 Claude 的规则」,后者是「Claude 使用中逐渐记下的经验」。目的是解决「会话即失忆」问题,让每次会话启动就自动加载项目背景,减少重复解释。

## Key Points

- **两层记忆分工**:`CLAUDE.md` = 开发者手写的规则(项目约定、规范、可团队共享);Auto Memory / `MEMORY.md` = Claude 自动记录的使用模式、调试经验、偏好,仅当前用户按项目私有。
- **CLAUDE.md 作用域分级**(路径越具体优先级越高):组织级(系统目录) → 项目级(`./CLAUDE.md` 或 `./.claude/CLAUDE.md`) → 用户级(`~/.claude/CLAUDE.md`) → 本地级(`./CLAUDE.local.md`,不提交 Git)。Claude 从 CWD 向上遍历目录树,加载沿途所有 `CLAUDE.md`。
- **`MEMORY.md` 的 200 行限制**:每次会话启动只加载前 200 行,控制上下文消耗、保持信息新鲜;详细内容拆到主题文件(如 `debugging.md`)按需加载。此限制**只对 `MEMORY.md` 生效**,`CLAUDE.md` 会完整加载。
- **Auto Memory 存储位置**:`~/.claude/projects/<project>/memory/`,`<project>` 从 git 仓库路径推导——同一仓库的所有 worktree 与子目录共享同一记忆目录;非 git 项目用项目根目录。目录内 `MEMORY.md` 是索引,其余为主题文件。
- **CLAUDE.md 编写四原则**:① 控制篇幅(≤200 行,过长费 token 且难遵循);② 结构清晰(用标题/列表);③ 具体明确(「用 2 空格缩进」优于「格式化代码」);④ 避免冲突(定期清理过时/矛盾指令)。
- **`@` 语法导入**:`CLAUDE.md` 可用 `@path/to/file` 导入 README、`package.json` 等,相对路径基于含 `@` 的文件解析,最多嵌套 5 层;首次导入外部文件会弹批准框。
- **`.claude/rules/` 模块化**:大型项目把指令拆成主题文件(code-style / testing / api-design / security),递归加载,可按 `frontend/`、`backend/` 分类;规则文件可用 YAML frontmatter 的 `paths` 字段限定作用范围,支持 glob 与花括号扩展;支持软链接跨项目共享;`~/.claude/rules/` 为用户级(优先级低于项目级)。
- **子智能体持久化记忆**:subagent 的 markdown 加 `memory` 字段(`user` / `project` / `local` 三种作用域),启用后自动加载记忆目录 `MEMORY.md` 前 200 行并挂载 Read/Write/Edit 工具。最佳实践:默认 `user` 作用域,任务前让其查记忆、任务后让其更新记忆。
- **启用/禁用 Auto Memory**(默认开启):`/memory` 命令界面切换 / 项目配置 `"autoMemoryEnabled": false` / 环境变量 `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`。
- **monorepo 排除无关配置**:`settings.local.json` 的 `claudeMdExcludes` 字段可忽略其他团队的 `CLAUDE.md`。
- **常见坑**:`/compact` 后指令「丢失」通常是因为指令只存在于对话里、从未写入 `CLAUDE.md`——需手动固化。^[extracted]
- 该「两层」框架与本 vault 实际采用的机制吻合:vault 的 `CLAUDE.md`/`AGENTS.md` 提供框架规则,而 `~/.claude/projects/.../memory/MEMORY.md` 索引则是 Auto Memory 的实际落地。^[inferred]

## Concepts

- [[concepts/claude-mem-memory-architecture]] — 第三方插件 claude-mem 的捕获/压缩/注入记忆架构,与官方 Auto Memory 是同一问题(会话失忆)的两种解法
- [[concepts/agent-operating-system]] — agent 长期记忆是 AOS 的组成要素之一
- [[concepts/claude-code-hooks-lifecycle]] — hook 生命周期是 claude-mem 注入记忆的挂载点,与本文的原生记忆机制形成对照

## Entities

- [[entities/claude-code]] — 本文的主角工具
- [[entities/claude-mem]] — 开源的 Claude Code 自动记忆管理插件(文章末尾亦推荐)

## Related

- [[skills/claude-code-settings]] — Claude Code 四级配置作用域体系,与本文的 CLAUDE.md 作用域分级同源
- [[skills/claude-mem-memory-usage]] — 用 claude-mem 管理长期记忆的实操(安装/检索/调优)
- [[skills/claude-code-token-optimization]] — CLAUDE.md 篇幅控制、200 行限制本质都是 token/上下文优化

## Open Questions

- 官方 Auto Memory 与第三方 claude-mem 在同一项目并存时,记忆是否重复/冲突?二者的注入时机与优先级如何协调?^[inferred]
- `MEMORY.md` 200 行限制下,主题文件的「按需加载」由谁触发——模型自主判断还是有显式索引路由?^[ambiguous]
