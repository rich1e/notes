---
title: >-
  多 vault 切换机制 — /wiki-switch 与 @name 的双轨路由
category: concepts
tags:
  - obsidian-wiki
  - framework
  - configuration
  - vault
  - routing
sources:
  - conversation:2026-09-05
created: 2026-09-05T01:30:00Z
updated: 2026-09-05T01:30:00Z
summary: >-
  obsidian-wiki 框架用 symlink + 全局 config 目录管理多个 vault profile,/wiki-switch 改持久默认、@name 单次路由、Config Resolution Protocol 是查找入口。理解这两套机制才能在多 vault 工作流里不踩坑。
provenance:
  extracted: 0.85
  inferred: 0.13
  ambiguous: 0.02
base_confidence: 0.9
lifecycle: draft
lifecycle_changed: "2026-09-05"
relationships:
  - target: "[[entities/obsidian-wiki-framework]]"
    type: related_to
  - target: "[[concepts/obsidian-wiki-vault-structure]]"
    type: related_to
  - target: "[[concepts/wiki-framework-self-reference]]"
    type: related_to
---

# 多 vault 切换机制

obsidian-wiki 框架把"管理多个 vault"作为一等公民设计——每个 vault 是一份独立 config 文件,激活状态由一个 symlink 指向决定。两种切换机制并存,**用途完全不同**。

## What It Is

obsidian-wiki 在全局配置目录(`~/.obsidian-wiki/` 或 `~/.config/obsidian-wiki/`)维护:

- `config` — 一个 symlink,指向当前激活的 vault
- `config.<name>` — 每个 vault 的完整环境配置,最关键字段是 `OBSIDIAN_VAULT_PATH`(vault 在文件系统中的根目录)

例:典型多 vault 用户的状态长这样:

```bash
$ ls -la ~/.obsidian-wiki/
config -> config.notes         # ← 当前激活的 vault
config.notes                   # 个人/学习 vault
config.experience              # 工作 vault
config.bak.orig                # 初始备份(可选)
```

每个 `config.<name>` 内容差异主要在 `OBSIDIAN_VAULT_PATH` 和 `OBSIDIAN_WIKI_VERSION`:

```sh
# config.notes
OBSIDIAN_VAULT_PATH="/Users/rich1e/workspace/code/notes"
OBSIDIAN_WIKI_VERSION="2026.8.7"

# config.experience
OBSIDIAN_VAULT_PATH="/Users/.../experience"
OBSIDIAN_WIKI_VERSION="2026.8.6"
```

## How It Works

### 机制 A:`/wiki-switch <name>` — 改持久默认

底层就是一行 `ln -sf`:

```bash
ln -sf "$CONFIG_DIR/config.<name>" "$CONFIG_DIR/config"
```

激活后,框架读取新 config 中的 `OBSIDIAN_VAULT_PATH`,之后所有 wiki-* 技能都在新 vault 上跑。

`/wiki-switch` 的 4 个子动作:

| 触发 | 行为 |
|---|---|
| `/wiki-switch <name>` | 切换到指定 vault(改 symlink) |
| `/wiki-switch list` | 列出所有 vault + 当前激活标记 |
| `/wiki-switch show [name]` | 打印 vault 完整配置(SECRET 自动 redact) |
| `/wiki-switch new <name>` | 从当前 config 复制一份模板,生成新 vault |

### 机制 B:`@<name>` — 单次路由,不污染默认

在**任意一次请求**里用 `@<name>` 路由到指定 vault,只对那次调用生效。框架从请求中**剥掉 `@name`** 后正常处理正文。

```text
wiki-query @experience 关于 X 我知道什么?
@work save this
wiki-update @personal
```

**关键差异**:`@name` 由 Config Resolution Protocol 处理,而不是 `/wiki-switch` skill —— 它**从不重写 symlink**。如果 `config.<name>` 不存在,框架报错并列出可用 vault,**不静默回落到默认**(避免覆盖用户意图)。

### Config Resolution Protocol — 查找入口

vault 是怎么被"找到"的?每次调用按以下优先级(`llm-wiki/SKILL.md`):

1. **inline `@name` override** — 请求含 `@xxx` → 直接读 `config.xxx`
2. **walk up CWD 找 `.env`** — 从当前目录向上找第一个含 `OBSIDIAN_VAULT_PATH` 的 `.env`(让项目级 override 全局)
3. **全局 config symlink** — 默认行为,`~/.obsidian-wiki/config` 跟着 symlink 走
4. **都不存在** — 提示运行 `wiki-setup`

`@name` 和 `/wiki-switch` 都在第 1/3 步起作用,本质都是改变 `OBSIDIAN_VAULT_PATH` 的解析结果。

## When to Use

| 场景 | 推荐 |
|---|---|
| 今天主要在另一个 vault 干活 | `/wiki-switch <name>`(改默认) |
| 偶尔查一眼别的 vault | `@<name>`,避免反复切换 |
| 还不确定要不要长期切 | 先用 `@<name>` 试探 |
| 需要新建第三个 vault | `/wiki-switch new <name>` 从当前复制模板 |
| 在另一个项目目录里期望落到该项目的 vault | 在项目根放含 `OBSIDIAN_VAULT_PATH` 的 `.env`(优先级 2) |

**注意事项**:

- `@name` 不修改 symlink,可在 notes/experience 之间无缝穿梭而不打乱默认
- `/wiki-switch` 改了 symlink 是**持久**的,影响所有未来调用,误操作代价高
- 不同 vault 的 `OBSIDIAN_WIKI_VERSION` 可以不同,但框架代码要兼容(版本不一致时某些 skill 行为可能差异)
- 一个 vault 的 `config.<name>` 文件被改坏时,只要 symlink 没动,其它 vault 不受影响——这就是 `config.bak.orig` 备份的用法

## Related

- [[entities/obsidian-wiki-framework]] — 框架本体(verified, core)
- [[concepts/obsidian-wiki-vault-structure]] — 单 vault 内部的 9 类目 + 4 系统文件结构
- [[concepts/wiki-framework-self-reference]] — 当 vault 本身就是框架运行时,如何避免自我重复 ingest 的拓扑学
- `wiki-switch` skill(SKILL.md) — 多 vault profile 调度的完整实现
- `llm-wiki/SKILL.md` — Config Resolution Protocol 的权威描述
- `CLAUDE.md` — 项目级配置协议入口
