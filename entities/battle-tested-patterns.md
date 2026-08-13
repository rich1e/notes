---
title: "battle-tested-patterns — 代码级编程模式目录"
category: entities
tags:
  - design-patterns
  - reference
  - open-source
  - github
sources:
  - "https://github.com/Totoro-jam/battle-tested-patterns"
created: 2026-07-08T07:14:00Z
updated: 2026-07-08T07:14:00Z
summary: Totoro-jam 出品的开源文档项目，从 React/Linux/Go/Redis/PostgreSQL 等生产代码库提炼 46 个代码级编程模式，每个模式附精确到行号的源码引用与多语言实现。
tier: core
lifecycle: reviewed
lifecycle_changed: "2026-08-12"
lifecycle_reason: "auto-promoted by wiki-lint --consolidate: age>30d, confidence>0.7"
base_confidence: 0.75
provenance:
  extracted: 0.95
  inferred: 0.05
  ambiguous: 0
visibility: public
relationships:
  - target: "[[references/pattern-catalog-battle-tested-patterns]]"
    type: related_to
  - target: "[[concepts/programming-pattern-categories]]"
    type: related_to
  - target: "[[skills/pattern-study-method]]"
    type: related_to
---

# battle-tested-patterns

**battle-tested-patterns** 是 [Totoro-jam](https://github.com/Totoro-jam) 维护的开源文档项目，定位是从顶级开源项目的源码中提炼**代码级**编程模式（区别于 GoF 那种面向对象设计模式）。

- **GitHub**: <https://github.com/Totoro-jam/battle-tested-patterns>
- **文档站（EN）**: <https://totoro-jam.github.io/battle-tested-patterns/>
- **文档站（中文）**: <https://totoro-jam.github.io/battle-tested-patterns/zh/>
- **许可证**: MIT
- **当前版本**: 1.16.1
- **配套 Agent 技能**: `adopt-pattern`、`audit-pattern`（可通过 Claude Code 插件市场或 `npx skills` 安装）

## 项目定位

项目自述填补的是三块空白 ^[extracted]：

| 现有 | 缺失 |
|---|---|
| GoF 等设计模式书 | 太抽象、太 OOP 中心 |
| 算法仓库 | 与真实工程脱节 |
| 系统设计指南 | 架构级，非代码级 |

**它的承诺**：code-level techniques from React, Linux, Go, Chromium — each with verifiable source links. 每个 "Proven In" 链接都指向源码的**精确行号**，不是目录、不是文件 ^[extracted]。

## 内容规模

| 项目 | 数量 |
|---|---|
| 模式数 | 46 |
| 交互式可视化 | 46（每模式一个 SVG，含时间旅行回放） |
| 练习题 | 93 (TypeScript) + 46 × 3 (Rust/Go/Python) |
| 测试 | 1,073+（4 语言总计） |
| 挑战题 | 184 |
| 系统案例研究 | 9（React / Linux / Go / Git / Node.js / Rust / 游戏引擎 / 分布式系统 / 更多） |
| 指南页 | 11（学习路径、复杂度速查、模式对比、面试题、cheatsheet 等） |
| 支持语言 | 4（TypeScript / Go / Python / Rust） |
| 文档 | 完整英文 + 简体中文双语 |

## 结构组织

```
docs/
├── index.md                 # 首页
├── patterns/                # 46 个模式
│   └── <pattern>/index.md   # 每个模式一页
├── by-project/              # 按项目看模式（React/Linux/Go/...）
├── case-studies/            # 9 个系统案例研究
├── guide/                   # 学习指南、cheatsheet、对比
├── .vitepress/              # 站点配置 + 46 个 Vue 可视化组件
└── zh/                      # 完整中文镜像
exercises/                   # 4 语言实现（answers/ 含答案）
scripts/                     # 校验脚本：source-link 行号、代码块、zh 一致性
```

## 贡献门槛（高）

摘自 README ^[extracted]：

1. ≥ 2 个生产证明 + 精确行号链接
2. TypeScript + ≥ 1 其他语言，且必须 idiomatic（不能直接翻译）
3. 4 语言练习 + 答案
4. 中文翻译代码块与英文完全一致
5. 全部测试通过、无 lint 错误
6. 源码链接由 CI **每周**校验，断链自动开 Issue

## 验证机制

`pnpm check` 串联的执行链 ^[extracted]：

```
lint → typecheck → test → verify-code → verify-mermaid → check:content
```

- `verify-links` — 校验所有源码链接仍可访问
- `verify-lines` — 校验行号范围在源文件中仍有效（应对上游 PR 改文件）
- `verify-code` — 校验 markdown 中的代码块
- `verify-mermaid` — 校验 mermaid 块语法
- `check:structure` / `check:zh-parity` / `check:exercises` / `check:relations` — 内容一致性

## 适合场景

- 准备系统设计 / 后端 / 基础架构岗面试
- 想看 React/Go/PostgreSQL 等真实代码库里某个模式的"教科书实现"
- 教学/写博客时需要带"出处"的代码示例
- 给 AI 编程助手（Claude Code / Codex / Copilot）装上 `adopt-pattern` / `audit-pattern` 技能 ^[extracted]

## 相关页面

- [[references/pattern-catalog-battle-tested-patterns]] — 46 模式目录与"Proven In"源链接
- [[concepts/programming-pattern-categories]] — 五大分类（数据结构/并发/系统/内存/行为）思路
- [[skills/pattern-study-method]] — 怎样用这个项目当系统学习材料
- [[synthesis/battle-tested-patterns × ios-design-patterns]] — 代码级 46 模式与 GoF 23 种对象模式的坐标差异
