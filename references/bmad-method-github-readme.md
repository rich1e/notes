---
title: "BMad Method GitHub README"
category: references
tags:
  - bmad-method
  - github
  - readme
  - reference
sources:
  - "https://github.com/bmad-code-org/bmad-method"
source_url: "https://github.com/bmad-code-org/bmad-method"
created: "2026-08-05T07:00:00Z"
updated: "2026-08-05T07:00:00Z"
summary: "BMad Method 仓库 README + 完整文件树（407 文件 / 481.6k tokens）：MIT 许可的 AI 驱动敏捷交付框架。包含中/法/英/越南多语言文档 + 6 个生态仓库 + 详细 ecosystem 表。"
provenance:
  extracted: 0.92
  inferred: 0.04
  ambiguous: 0.04
base_confidence: 0.85
lifecycle: reviewed
lifecycle_changed: "2026-08-05"
tier: core
---

# BMad Method GitHub README

> [[entities/bmad-method]] 框架的 GitHub 仓库主入口。gitingest 抓取（commit `05e295f` / 2026-08-05）。

## 仓库元信息

- **URL**: https://github.com/bmad-code-org/bmad-method
- **License**: MIT（商标 "BMad" / "BMAD-METHOD" 属 BMad Code, LLC）
- **Stars / Stats**: README 末有 contrib.rocks image（具体数未抓）
- **npm**: `bmad-method`（latest version badge）
- **当前 commit**: `05e295f48e9176de4e457204325b0444ab185a0f`
- **文件数 / Token**: 407 文件 / 481.6k tokens / 2.03MB（gitingest `--include-pattern "*.md"` 后）

## 完整文件树（精选）

```
bmad-code-org-bmad-method/
├── README.md                    # 主 README
├── AGENTS.md                    # Agent rules（Conventional Commits + quality check）
├── CHANGELOG.md                 # 详细版本变更
├── CONTRIBUTING.md
├── CONTRIBUTORS.md
├── README_CN.md                 # 中文 README
├── README_VN.md                 # 越南语 README
├── SECURITY.md
├── TRADEMARK.md
├── docs/
│   ├── index.md                 # docs 首页
│   ├── _STYLE_GUIDE.md
│   ├── 404.md
│   ├── cs/                      # 捷克语翻译
│   ├── fr/                      # 法语翻译
│   ├── explanation/             # 14 篇解释文档
│   │   ├── advanced-elicitation.md
│   │   ├── analysis-phase.md
│   │   ├── brainstorming.md
│   │   ├── build.md
│   │   ├── checkpoint-preview.md
│   │   ├── deep-recon.md
│   │   ├── established-projects-faq.md
│   │   ├── forge-idea.md        # v6.10 新
│   │   ├── named-agents.md
│   │   ├── party-mode.md
│   │   ├── preventing-agent-conflicts.md
│   │   ├── project-context-theory.md
│   │   ├── project-context.md
│   │   ├── retrospective.md
│   │   ├── sprint-planning.md   # v6.10 重写
│   │   ├── web-bundles.md
│   │   └── why-solutioning-matters.md
│   ├── how-to/                  # 操作指南
│   │   ├── customize-bmad.md
│   │   ├── established-projects.md
│   │   ├── get-answers-about-bmad.md
│   │   ├── install-bmad.md
│   │   ├── project-context.md
│   │   ├── quick-fixes.md
│   │   └── upgrade-to-v6.md
│   └── reference/               # 参考文档
│       ├── agents.md
│       ├── commands.md
│       ├── core-tools.md
│       ├── dev-auto.md          # v6.10 新
│       ├── modules.md
│       ├── testing.md
│       └── workflow-map.md
└── (其他仓库未在此次抓取范围)
```

## 6 个生态仓库

| Module | URL | 用途 |
|---|---|---|
| BMad Method | `bmad-code-org/BMAD-METHOD` | 计划与交付软件（新原型到既有 codebase） |
| BMad Builder | `bmad-code-org/bmad-builder` | Skill / workflow / agent 构造器 |
| BMad Creative Intelligence Suite | `bmad-code-org/bmad-module-creative-intelligence-suite` | 创新 / 设计思维 / 故事讲述 |
| BMad Test Architect | `bmad-code-org/bmad-method-test-architecture-enterprise` | 企业测试 add-on |
| BMad Loop | `bmad-code-org/bmad-loop` | 全自动构建 / 验证 / 复盘整个 epic |
| BMad Game Dev Studio | `bmad-code-org/bmad-module-game-dev-studio` | Unity / Unreal / Godot / Phaser 游戏 |

## README 6 条核心价值

1. **Right-sized process** —— 清晰改动直接实现，复杂 initiative 加 planning
2. **New or existing code** —— 从零或在 inherited codebase 上工作
3. **Durable context** —— 决策向前传递
4. **Specialized perspectives** —— 多视角 agent
5. **Guided collaboration** —— 结构化工作流 + 多 agent 讨论
6. **One delivery path** —— 早期思考到 reviewed implementation 到纠错到学习

## 5 个关键仓库资产

1. **README 横幅**：`banner-bmad-method.png`（视觉品牌）
2. **交付闭环图**：`docs/images/bmad-delivery-loop.svg`——Clarify/Plan/Build/Learn 闭环
3. **Build 流程图**：`docs/diagrams/build-diagram.png`
4. **AGENTS.md** —— Conventional Commits + `npm ci && npm run quality` before push
5. **CHANGELOG** —— 极详细，含 unreleased 段

## 链接资源

- 文档站：[docs.bmad-method.org](https://docs.bmad-method.org)
- Roadmap：[public roadmap](https://docs.bmad-method.org/roadmap/)
- Discord：[discord.gg/gk8jAdXWmj](https://discord.gg/gk8jAdXWmj)
- YouTube：[youtube.com/@BMadCode](https://youtube.com/@BMadCode)
- 主页：[bmadcode.com](https://bmadcode.com)
- Web bundles：[bmadcode.com/web-bundles](https://bmadcode.com/web-bundles/)
- 赞助：[buymeacoffee.com/bmad](https://buymeacoffee.com/bmad) 或 contact@bmadcode.com

## v6.10 主要变更（CHANGELOG）

详见仓库 CHANGELOG.md。核心：

- **bmad-loop** 成为可装模块（替代 deprecated bmad-automator）
- **bmad-dev-auto** 新 unattended workflow skill（spec-frontmatter state machine）
- **sprint-planning** 重写——deterministic script core + JSON-only 输出 + 37 tests
- **party-mode: anti-consensus club**——内置 4 persona（Wildcard / Level / Killjoy / Splinter）
- **新 elicitation 方法**：Subtraction / Map Is Not the Territory
- **Edge Case Hunter** 加 named-set generalization pass（catch rate 50%-100% 提升，token +19%）
- **v7 预告**：所有 Python 脚本标准化 `uv run`

## 安装

```bash
# 前置
node --version   # 20.12+
python3 --version  # 3.10+
uv --version    # v7 起必用

# 一行安装
npx bmad-method install
```

详见 [[skills/bmad-install-and-setup]]。

## Related

- [[entities/bmad-method]] — 框架本体
- [[concepts/bmad-delivery-loop]] — 闭环
- [[concepts/bmad-named-agent-architecture]] — 三腿凳
- [[entities/bmad-named-agent]] — 5 命名 agent
- [[entities/bmad-party-mode]] — 多 agent 房间
- [[skills/bmad-install-and-setup]] — 安装流程
- [[skills/bmad-customize-skill]] — TOML 覆盖系统
- `_raw/github-bmad-code-org-bmad-method.txt` — 完整 gitingest 抓取（407 文件 / 481.6k tokens）