---
title: claude-mem-memory-architecture × claude-code-settings
category: synthesis
tags: [claude-code, agent-memory, mcp, ai-agents, synthesis]
sources:
  - "[[concepts/claude-mem-memory-architecture]]"
  - "[[skills/claude-code-settings]]"
  - "[[concepts/claude-code-hooks-lifecycle]]"
  - "[[skills/claude-mem-memory-usage]]"
  - "[[misc/web-zhuanlan-zhihu-com-p-2013213227740325799]]"
created: 2026-08-04T13:30:00Z
updated: 2026-08-04T13:30:00Z
summary: "claude-mem 用 hook 生命周期扩展'记什么',settings 用四级作用域控制'在哪生效';二者共享同一个'装错 scope 就静默失效'的陷阱结构——npm -g 只装 SDK 不注册 hook,与 MCP --global 作用域坑同构。"
provenance:
  extracted: 0.35
  inferred: 0.6
  ambiguous: 0.05
base_confidence: 0.68
lifecycle: draft
lifecycle_changed: "2026-08-04"
relationships:
  - target: "[[concepts/claude-mem-memory-architecture]]"
    type: related_to
  - target: "[[skills/claude-code-settings]]"
    type: related_to
---

# claude-mem-memory-architecture × claude-code-settings

## The Connection

[[concepts/claude-mem-memory-architecture]] 讲 Claude Code 如何被**扩展出记忆**(capture → compress → inject 流水线,挂在 6 个生命周期 hook 上)。[[skills/claude-code-settings]] 讲 Claude Code 的**配置作用域体系**(四级:组织/项目/用户/本地,越具体越优先)。

表面上一个讲"记忆",一个讲"配置",井水不犯河水。但把二者叠起来会发现:**它们是同一台机器上"可扩展性"的两根支柱,并且共享同一个失败模式——扩展装到错误的作用域,就静默失效,没有报错。**

## Where They Co-occur

三个源页把它们拉到一起:[[concepts/claude-code-hooks-lifecycle]](hook 既是 claude-mem 的挂载点,也是 settings.json 里配置的对象)、[[skills/claude-mem-memory-usage]](装 claude-mem 的作用域坑)、[[misc/web-zhuanlan-zhihu-com-p-2013213227740325799]](梳理 CLAUDE.md 四级作用域 + Auto Memory)。三处都在讲"扩展 Claude Code 时,东西装在哪一层决定它是否生效"。

## Cross-cutting Insight

**"记什么"和"在哪生效"是可扩展性的两个正交维度,而二者都栽在同一个作用域陷阱上。**^[inferred]

- **claude-mem 扩展"记什么"**:通过 hook 在生命周期节点(PostToolUse/Stop/SessionStart)插入捕获与注入逻辑。它扩展的是**行为的时间维**——在什么时刻做什么。
- **settings 控制"在哪生效"**:四级作用域决定一条配置(含 hook 注册、MCP server、权限)作用于哪个范围。它扩展的是**行为的空间维**——在哪个项目/用户下启用。
- **共享的陷阱结构**:两者都遵循"装错 scope = 静默失效"。
  - claude-mem:`npm -g` 只装 SDK **不注册 hook**——插件市场或 `npx claude-mem install` 才写 hook 配置。装了却没记忆,不报错。
  - MCP server:`claude mcp add` 默认**项目级**,写进 `~/.claude.json` 的 `projects.<路径>.mcpServers`;只有 `--global`(≡ `-s user`)才落顶层。在 `~/projects/foo` 下 add 只对 foo 生效,不报错。
  - CLAUDE.md:四级作用域"越具体越优先",一条规则放错层就被更具体的层覆盖,不报错。

**这三个坑是同一个 bug 家族**:Claude Code 的扩展点(hook / MCP / 配置规则)全都靠"写到正确的作用域文件"生效,而"作用域"这个概念对用户不可见——你以为装好了,系统却把它记在另一个 scope 下。[[concepts/mcp-server-protocol-quirks]] 里那个"和 `git config` 一样"的类比,是这一整族陷阱的统一心智模型。

## Tensions and Trade-offs

- **不可见的默认作用域是双刃剑。** 默认项目级让配置天然隔离(不同项目互不污染),但也让"我明明装了却不生效"成为高频困惑。可见性 vs 隔离性的取舍。
- **hook 的时间维扩展会撞上 scope 的空间维。** 一个在用户级注册的 claude-mem hook,会在**所有**项目触发捕获;若某项目含敏感数据,时间维的"总是捕获"和空间维的"只在此项目"就冲突——需要 `<private>` 标签或 SKIP 配置兜底。
- **调试成本。** 静默失效意味着排障要先问"它装在哪个 scope",这一步没有工具提示,全靠人肉查 `~/.claude.json` / hooks.json。

## Strongest Objection

**把 claude-mem 的安装坑、MCP 的作用域坑、CLAUDE.md 的覆盖规则归成"同一个 bug 家族",可能是牵强的模式套用。** 它们的底层机制其实不同:claude-mem 的坑是**打包问题**(SDK 与 hook 注册分离),MCP 的坑是**默认值问题**(默认项目级),CLAUDE.md 的坑是**优先级问题**(层级覆盖)。三者都表现为"没按预期生效",但把表象相同当成结构相同,可能掩盖了它们各自需要不同修法的事实。

> test: 检查这三个坑的官方修复路径是否收敛到同一个机制。若 Anthropic 用**统一的作用域可视化/校验**(如一条 `claude doctor` 同时报出 hook 未注册、MCP 装错层、CLAUDE.md 被覆盖)一次性解决,则"同一家族"成立;若三者各自独立修补、互不相关,则本页的归并是表象层面的过度概括。

## Open Questions

- 是否存在一个统一的"扩展作用域检查器",能一次性列出当前生效的 hook / MCP server / CLAUDE.md 规则及其各自的 scope?
- claude-mem 的 hook 若做成 scope-aware(按项目决定是否捕获),能否同时解决"隐私"和"总是捕获"的张力?
- 四级作用域 + hook 生命周期 + MCP 三者,是否应在文档里合并成一节"Claude Code 可扩展性总览",而非分散在三处?

## Related

- [[concepts/claude-mem-memory-architecture]]
- [[skills/claude-code-settings]]
- [[concepts/claude-code-hooks-lifecycle]]
- [[concepts/mcp-server-protocol-quirks]]
- [[skills/claude-mem-memory-usage]]
- [[entities/claude-mem]]
