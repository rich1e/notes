---
title: "Capability Seam — Service Definition / Provider / Consumer 三件套"
category: concepts
tags:
  - cordis
  - capability-seam
  - service-definition
  - provider
  - consumer
  - concept
summary: "Capability Seam 设计模式：每个可替换 capability 必备 Service Definition（抽象类 + ctx.<key>）+ Service Provider（实现）+ Consumer（注入方，通常是 model-facing tool）。一换 provider = 整个产品栈跟着换（Bash + PTY + LSP 一起走）。"
sources:
  - "https://github.com/deepseek-ai/deepseek-harness/blob/main/docs/glossary.md"
  - "https://github.com/deepseek-ai/deepseek-harness/blob/main/docs/architecture.md"
created: "2026-08-14T01:28:00Z"
updated: "2026-08-14T01:28:00Z"
provenance:
  extracted: 0.92
  inferred: 0.06
  ambiguous: 0.02
base_confidence: 0.75
lifecycle: draft
lifecycle_changed: "2026-08-14"
tier: supporting
relationships:
  - target: "[[concepts/cordis-plugin-framework]]"
    type: related_to
  - target: "[[entities/deepseek-harness]]"
    type: derived_from
---

# Capability Seam — Service Definition / Provider / Consumer 三件套

> Cordis 应用层概念：每个可替换 capability 必备**三个角色**（Service Definition / Service Provider / Consumer）。一个角色不能算 seam；三个角色齐了，**一换 provider 整个产品栈跟着换**。

## 三件套定义

| 角色 | Cordis 类型 | 命名约定 | 示例（shell capability） |
|---|---|---|---|
| **Service Definition** | `class extends Service` (抽象) | `dsh-<name>` | `dsh-shell` |
| **Service Provider** | Service Definition 的实现 | `dsh-<name>-<impl>` | `dsh-bash-local` / `dsh-bash-sandbox` |
| **Consumer** | 注入服务的代码（通常是 tool） | `dsh-tool-<name>` | `dsh-tool-bash`（模型侧的 bash tool）|

### 为什么 Service Definition 是「abstract class」而不是 `interface`

> "An abstract class such as `ShellExecutor`, or a concrete registry such as `WebRuntime`, never a TypeScript `interface`"

- **抽象类**可以承载**状态 + 类型注册**
- `interface` 只能约束形状，不能注册 `ctx.<key>` 索引
- abstract class 的子类化保证类型 / DI / 服务发现

### 为什么必须三个角色齐全

> "A package may combine roles, but one role alone is not a seam; adding a capability means designing all three."

- **只定义不实现** = 抽象空壳
- **只实现不抽象** = 不可替换
- **只抽象不消费** = 浪费（没人调用）
- **三个齐全** = 抽象 + 可选实现 + 实际可用 = 真 seam

## 经典示例

### Shell capability

```
dsh-shell                  Service Definition: ctx.shell
├── dsh-bash-local         Provider: 本地 bash 进程
├── dsh-bash-sandbox       Provider: 沙箱 bash
└── dsh-tool-bash          Consumer: 模型侧 bash tool
```

### Filesystem capability

```
dsh-fs                    Service Definition: ctx.fs
├── dsh-fs-local           Provider: 本地 fs
├── dsh-fs-sandbox         Provider: 沙箱 fs
└── dsh-tool-*             Consumer: read/write 等工具
```

### LLM capability

```
dsh-llm                   Service Definition + Consumer (同包)
├── dsh-llm-deepseek       Provider: DeepSeek API
└── dsh-llm-openai         Provider: OpenAI API
```

> "Roles normally occupy separate packages when they evolve independently, but a package may own multiple roles when they are one concern (`dsh-llm` owns its Service Definition and Consumer)."

LLM 是「一个 concern」的例外 — Service Definition 和 Consumer 在同一包。

## 核心价值：一换 provider 整个产品栈跟着换

> "Filesystem and subprocess providers share one execution world, so pointing them at a remote sandbox moves Bash, PTY, and LSP with them, with no provider forks."

**示例**：把 `dsh-fs-local` 换成 `dsh-fs-sandbox` (远程 sandbox provider)：
- ✅ bash tool 自动跑在 sandbox
- ✅ PTY 自动跑在 sandbox
- ✅ LSP 自动跑在 sandbox
- ✅ file operations 自动走 sandbox
- ❌ 不需要写新的 `bash-sandbox-tool.py`
- ❌ 不需要维护 `lsp-sandbox.py`

**这是「不 fork 的力量」**：抽象统一 = 整个执行栈可平移。

## 与传统模式对比

| 模式 | 抽象 | 实现 | 调用方 | 整体替换 |
|---|---|---|---|---|
| **传统抽象类 + DI** | ✅ | ✅ | ✅ | ⚠️ 部分 — DI 容器要重新 wire |
| **Strategy 模式** | ✅ Interface | ✅ 实现 | ✅ 客户端代码 | ⚠️ 客户端要知道 strategy 接口 |
| **Microservices** | ✅ API contract | ✅ Service | ✅ 其他 service | ✅ | 
| **Capability Seam** | ✅ abstract class | ✅ 多实现 | ✅ 自动注入 | ✅ 完整栈替换 |

## dsh 当前的 capability 清单

| Capability | Definition | Providers | Consumers |
|---|---|---|---|
| **llm** | `dsh-llm` | `dsh-llm-deepseek`, `dsh-llm-openai` | 同 `dsh-llm` |
| **shell** | `dsh-shell` | `dsh-bash-local`, `dsh-bash-sandbox` | `dsh-tool-bash` |
| **subprocess** | `dsh-subprocess` | `dsh-subprocess-local` | bash, terminal consumers |
| **terminal** | `dsh-terminal` | (local) | `dsh-tool-terminal` |
| **fs** | `dsh-fs` | `dsh-fs-local`, `dsh-fs-sandbox` | file tools |
| **lsp** | `dsh-lsp` | (local) | LSP-aware tools |
| **skill** | `dsh-skill` | `dsh-skill-local` | `dsh-skill-catalog` |
| **web** | `dsh-web` | `dsh-web-search`, `dsh-web-fetch` | `dsh-tool-web` |
| **subagent** | `dsh-subagent` | `dsh-subagent-fork`, `dsh-subagent-delegate` | delegation tools |
| **workflow** | `dsh-workflow` | `dsh-workflow-worker` | workflow tool |
| **compaction** | `dsh-compaction` | `dsh-compaction-basic` | (内部) |
| **credentials** | `dsh-credentials` | `dsh-credentials-env` | (内部) |

→ 完整 package hierarchy 见 [[references/dsh-package-hierarchy]]

## 添加新 capability 的 checklist

> "Adding a capability means designing all three."

1. **Service Definition 包**（`dsh-<name>`）
 - 定义抽象类 `class extends Service`
 - 暴露 `ctx.<key>`（用 `@dshScopeScan` 标记 scope-visible 字段）
 - 定义事件 `<name>/*`（typed events）
2. **Provider 包**（至少一个 `dsh-<name>-<impl>`）
 - 实现 Service Definition
 - 注册时声明依赖（resolver manifest's `dependencies`）
3. **Consumer 包**（通常是 `dsh-tool-<name>`）
 - 用 `@param` / `@returns` JSDoc 文档化
 - tool UI render intent 提前决定（`generic` / `terminal` / `diff` / `locations`）
 - 配合 cookbook：`docs/cookbook/adding-a-tool.md`
4. **测试** — capability seam 都要覆盖 unit + e2e + snapshot 三层

## 反向论证

| 误区 | 实际 |
|---|---|
| 「一个包就够了」 | 三件套要分；同包三件是少数例外 |
| 「interface 也行」 | 接口不能注册 `ctx.<key>` |
| 「Provider 越多越好」 | 1 个 production + N 个 testing 是常态 |
| 「Consumer 不要也是 seam」 | Consumer 缺失 = 没人用 = 不算 seam |

## Open Questions

1. **capability seam 的版本化策略** — Service Definition 改了之后，Provider 必须跟着改？^[ambiguous]
2. **多 Capability 的 transitive 依赖** — shell 依赖 fs、subprocess 等时如何声明 ^[ambiguous]
3. **Provider 的 runtime 可替换性** — 是只能启动时选，还是可以热替换？^[ambiguous]

## 相关页面

- [[concepts/cordis-plugin-framework]] — 三件套的基础
- [[entities/deepseek-harness]] — dsh 实现
- [[references/dsh-package-hierarchy]] — 当前所有 capability 全景
- [[entities/cordis]] — 框架本体