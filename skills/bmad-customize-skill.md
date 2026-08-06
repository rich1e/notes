---
title: "BMad Customize Skill（TOML 覆盖系统）"
category: skills
tags:
  - bmad-method
  - customize
  - toml
  - override
  - skill
summary: "BMad 定制系统：`/bmad-customize <skill-name>` 重写 shipped 行为；两层 override：`_bmad/custom/*.toml` 团队 committed + `.user.toml` 个人 gitignored。4 层 TOML 解析器（stdlib `tomllib`）。"
sources:
  - "https://github.com/bmad-code-org/bmad-method"
created: "2026-08-05T07:00:00Z"
updated: "2026-08-05T07:00:00Z"
provenance:
  extracted: 0.85
  inferred: 0.10
  ambiguous: 0.05
base_confidence: 0.68
lifecycle: draft
lifecycle_changed: "2026-08-05"
tier: supporting
relationships:
  - target: "[[entities/bmad-named-agent]]"
    type: related_to
  - target: "[[concepts/bmad-named-agent-architecture]]"
    type: related_to
  - target: "[[skills/bmad-install-and-setup]]"
    type: related_to
---

# BMad Customize Skill（TOML 覆盖系统）

> BMad 的 customization 是一等公民——`/bmad-customize <skill-name>` 重写 shipped 行为。两层 override：**团队 committed** + **个人 gitignored**。4 层 TOML 解析器（stdlib `tomllib`）。

## 命令入口

```bash
/bmad-customize bmad-party-mode
/bmad-customize bmad-build
/bmad-customize bmad-brainstorming
# 任何 shipped skill
```

## 两层 Override

| 层级 | 路径 | 提交？ | 用途 |
|---|---|---|---|
| **Shipped** | `bmad-method/` repo 内的 `customize.toml` | n/a | 出厂默认 |
| **Team** | `_bmad/custom/{skill-name}.toml` | **是**（committed） | 团队组织约定 |
| **Personal** | `.user.toml` | **否**（gitignored） | 个人偏好 |

**合并顺序**：Shipped ← Team ← Personal（**Personal 覆盖 Team**）。

## 4 层 TOML 解析器

v6.10 修复：`bmad-help` 的 config 数据源从 legacy `config.yaml` / `user-config.yaml` 改为**共享 4 层 TOML 解析器**——之前 `communication_language` 和 `project_knowledge` 没传到 skill。

> "bmad-help reads central config (#2541). Its config data source now goes through the shared four-layer TOML resolver instead of legacy `config.yaml`/`user-config.yaml`, fixing `communication_language` and `project_knowledge` not reaching the skill."

**4 层**（推测）：

1. shipped default
2. team committed
3. personal
4. session runtime override

与 [[skills/claude-code-settings]] 的四级作用域（user / project / local / runtime）**同源设计**。

## 定制维度

| 维度 | 改什么 |
|---|---|
| **Agent role** | 重定义角色（如把 Mary 从 "Analyst" 改为 "Business + Data Analyst"） |
| **Principles** | 加 / 改 / 删 agent 的行动原则 |
| **Communication style** | 改 voice / 措辞 / 语言 |
| **Icon** | 改 emoji |
| **Menu** | 加 / 改 / 删菜单项 |
| **Default party** | pin 自建 group 为默认 party |
| **Default mode** | Party Mode 默认 session / subagent / agent-team |
| **House rules** | 全 session 房间规则 |

## 不能改的

> "They each have a hardcoded identity (name, title, domain) and a customizable layer (role, principles, communication style, icon, menu). You can rewrite Mary's principles or add menu items; **you can't rename her** — that's deliberate."

**不能改名**——品牌识别跨 customization 保留，"hey Mary" 始终激活 analyst。

## 工作流定制示例

### 改 Party Mode 默认

```toml
# _bmad/custom/bmad-party-mode.toml
[party]
default_mode = "subagent"   # 默认从 session 改 subagent
default_party = "code-review-crew"  # 默认 cast

[house_rules]
stay_on_topic = true
require_consensus = false
```

### 改 Agent 行为

```toml
# _bmad/custom/bmad-agent-business-analyst.toml
[role]
description = "Business + Data Analyst"

[principles]
additional = [
  "Always cite the data source for quantitative claims",
  "Default to quantitative analysis when possible"
]
```

## 与 vault 已有 skill / concept 的关系

| vault 已有 | BMad Customize 的同源 |
|---|---|
| [[skills/claude-code-settings]] | 4 层 TOML 解析器 ≈ 4 级 settings 作用域 |
| [[concepts/mcp-server-protocol-quirks]] | "team vs user" 两层切分与 `-s user` 同源 |
| [[concepts/claude-code-hooks-lifecycle]] | "prepend / append steps" = hook 的人格化版本 |
| [[concepts/agent-operating-system]] | Customization = AOS 五层中 "Knowledge Base" + "ADR Memory" 的落地 |

## 迁移路径

v6 → v7 期间 `bmad-sprint-status` 已 deprecated 成 forwarding shim：

> "Now a `v6-shims/` husk that forwards to `bmad-sprint-planning`'s status view with a deprecation notice. Migrate `_bmad/custom/bmad-sprint-status.toml` overrides to `_bmad/custom/bmad-sprint-planning.toml`."

**教训**：v7 升级时检查 deprecated shim，把 override TOML 文件跟着迁移到新 skill。

## 与"party 自建"的区别

| Customize | Party 自建 |
|---|---|
| 改 shipped skill 的**默认行为** | 创建**新 cast** 的 personas |
| 改的是同一 skill | 改的是 cast 组成 |
| 通过 `bmad-customize <skill>` | 通过 `party mode, create a new party` |
| 影响所有用户（team layer）或仅个人（user layer） | 仅该 party |

## Related

- [[entities/bmad-method]] — 框架本体
- [[entities/bmad-named-agent]] — 定制目标
- [[concepts/bmad-named-agent-architecture]] — 三腿凳中的 Customization 腿
- [[skills/bmad-install-and-setup]] — 安装后立即定制
- [[entities/bmad-party-mode]] — 最常被定制的 skill