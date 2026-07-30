---
title: "DESIGN.md 的 token 引用与插值"
category: concepts
tags: [design-tokens, design-md, dtcg-spec, ai-coding, concept]
summary: "DESIGN.md 组件定义用 {path.to.token} 形式引用前文 token（如 {colors.primary}、{typography.body-md}），AI agent 读取时实时刻画。该语法借鉴 Design Tokens Community Group 2025.10 规范。"
sources:
  - "https://github.com/google-labs-code/design.md"
  - "https://github.com/VoltAgent/awesome-design-md"
  - "https://www.designtokens.org/tr/2025.10/format/#abstract"
created: "2026-07-28T01:00:00Z"
updated: "2026-07-28T01:00:00Z"
tier: supporting
lifecycle: draft
lifecycle_changed: "2026-07-28"
base_confidence: 0.85
provenance:
  extracted: 0.88
  inferred: 0.10
  ambiguous: 0.02
    type: related_to
relationships:
  - target: "[[concepts/design-md-format-spec]]"
    type: related_to
  - target: "[[entities/awesome-design-md]]"
    type: related_to

---

# DESIGN.md 的 token 引用与插值

> `{colors.primary}` 不是装饰，是组件定义里的实时刻画——agent 读 DESIGN.md 时把 token 引用解析成具体值。

## 引用语法

```yaml
components:
  button-primary:
    backgroundColor: "{colors.tertiary}"
    textColor: "{colors.on-tertiary}"
    rounded: "{rounded.sm}"
    padding: 12px
```

AI agent 读 DESIGN.md 时按 DTCG 路径语法解析：

| 引用 | 解析为 |
|------|--------|
| `{colors.primary}` | YAML frontmatter 里 `colors.primary` 的 hex 值 |
| `{typography.body-md}` | `typography.body-md` 的 typography 对象 |
| `{rounded.md}` | `rounded.md` 的 dimension 值 |
| `{spacing.xl}` | `spacing.xl` 的 dimension 值 |

## 跨字段复用

引用机制允许组件定义中**跨字段复用 token**：

```yaml
colors:
  primary: "#1A1C1E"
  primary-pressed: "#0F1113"

components:
  button-primary:
    backgroundColor: "{colors.primary}"
  button-primary-pressed:
    backgroundColor: "{colors.primary-pressed}"
```

变体（hover / active / pressed）通过**单独的 component entry** 表达：

```yaml
button-primary:        { ... }
button-primary-hover:  { backgroundColor: "{colors.primary-container}" }
button-primary-active: { backgroundColor: "{colors.primary-pressed}" }
button-primary-disabled:
    backgroundColor: "{colors.hairline}"
    textColor: "{colors.muted}"
```

[[entities/awesome-design-md.md|awesome-design-md]] 实测样本（Notion 版本）：

```yaml
button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.button-md}"
    rounded: "{rounded.md}"
    padding: "10px 18px"
button-primary-disabled:
    backgroundColor: "{colors.hairline}"
    textColor: "{colors.muted}"
```

## 与 Design Tokens Community Group 兼容

DESIGN.md 的 token 系统**借鉴** [DTCG 2025.10 规范](https://www.designtokens.org/tr/2025.10/format/#abstract)：

- typed token groups（colors / typography / spacing / rounded）
- `{path.to.token}` 引用语法
- 文档明确说 *"These tokens are easily converted from or to `tokens.json`, Figma variables, and Tailwind theme configs."*

实际意义：一个写好的 DESIGN.md 可以**双向转换**到：

| 目标 | 工具 / 流程 |
|------|-------------|
| `tokens.json` | 自写脚本（YAML → JSON，按 DTCG `$value` 包一层） |
| Figma variables | Figma Tokens 插件或 Tokens Studio |
| Tailwind theme | 自写脚本（colors → `theme.extend.colors`，typography → `theme.extend.fontSize`） |

## 验证机制

`@google/design.md` 的 `lint` 子命令会对引用做闭环检查：

```bash
npx @google/design.md lint DESIGN.md
```

如果某个 component 引用了不存在的 token 路径，lint 会以 `error` 级别报错——避免组件读到空值。

## 与"硬编码值"的对比

DESIGN.md **反对**在 components 里直接写 hex / px：

```yaml
# ❌ 硬编码（lint 接受但不推荐）
button-primary:
    backgroundColor: "#1A1C1E"
    rounded: 8px

# ✅ token 引用（推荐）
button-primary:
    backgroundColor: "{colors.primary}"
    rounded: "{rounded.md}"
```

理由：硬编码值**打断**了"换主题 = 改一处"的链路。改 `colors.primary` 应该自动传播到所有引用它的 component——这是 DESIGN.md 作为"living source of truth"的核心价值。

## 局限

- **路径引用无 namespace**：跨 DESIGN.md 复用 token 不行（每个文件是自包含的）。
- **不支持算术**：不能写 `{spacing.md} * 2`，只能引用已有 token 或写死新值。
- **不支持 condition / dark mode 内嵌**：dark mode 通常通过 `colors.canvas-dark` 等**预定义** token 实现，引用时根据场景选择——不能在引用里写 `{colors.canvas | dark}`。
- **agent 解析依赖 LLM 训练数据**：理论上规范定义了 `{path.to.token}` 解析规则，但**实际**让 agent 正确解析还是靠模型对 DTCG 路径语法的"先验知识"——这是 spec 之外的实现依赖。

## 相关页面

- [[concepts/design-md-format-spec]] — 文件整体结构
- [[concepts/design-system-as-ai-context]] — token 引用为何是 AI agent 的硬约束
- [[sources/google-design-md-spec]] — 官方规范
