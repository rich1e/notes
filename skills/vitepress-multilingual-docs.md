---
title: "VitePress 多语言文档站构建"
category: skills
tags: [vitepress, docs, tools, f2e]
sources:
  - "https://github.com/sebastienrousseau/dotfiles.github.io"
  - "https://dotfiles.io"
created: 2026-07-27T06:20:00Z
updated: 2026-07-27T06:20:00Z
summary: "使用 VitePress 构建支持 22 种语言的技术文档站，含 SEO、PWA、无障碍、多语言同步策略和质量套件配置。"
provenance:
  extracted: 0.85
  inferred: 0.12
  ambiguous: 0.03
base_confidence: 0.67
lifecycle: draft
lifecycle_changed: 2026-07-27
tier: peripheral
relationships:
  - target: "[[entities/sebastienrousseau-dotfiles]]"
    type: derived_from
---

# VitePress 多语言文档站构建

以 [[entities/sebastienrousseau-dotfiles]] 文档站（dotfiles.io）为参考，总结 VitePress 多语言文档站的关键实践。

## 技术栈

- **框架**: VitePress 1.x（Vite + Vue 3）
- **Node.js**: v18+
- **部署**: GitHub Pages + GitHub Actions（main 分支自动触发）

## 目录结构

```text
docs/
├── .vitepress/
│   ├── config.ts               # 主配置文件
│   ├── config/
│   │   ├── head/               # SEO meta 标签
│   │   ├── nav/                # 导航（每种语言一个配置）
│   │   └── sidebar/            # 侧边栏（每种语言一个配置）
│   ├── public/                 # 静态资源（favicon、manifest）
│   └── theme/                  # 主题覆盖与 CSS
└── en/                         # 英语内容（默认 locale）
└── fr/ zh/ de/ ...             # 其他语言目录
```

## 多语言管理策略

### 语言目录规则
- 每种语言独立目录（`/en/`、`/zh/`、`/fr/` 等）
- 英语（`/en/`）为内容源，其他语言跟随更新
- 技术命令保持英文，描述文字翻译

### Front Matter 必填字段
```yaml
---
title: "SEO Optimized Title"
description: "Compelling summary (max 160 chars)"
lang: en-GB
metaTitle: "Page Title | Dotfiles"
permalink: /category/page-name/
sidebar: true
meta:
  - name: keywords
    content: "keyword1, keyword2"
---
```

### 同步脚本
- `npm run docs:sync:en` — 从 dotfiles 源仓库同步英文文档
- `npm run docs:audit:en` — 审计英文文档准确性
- `npm run content:normalize` — 标准化所有页面的 frontmatter

## 质量套件

```bash
npm run test:quality  # 完整质量套件
```

完整质量套件包含：
1. `npm run build` — 生产构建验证
2. `npm run validate:manifest` — PWA manifest 验证
3. `npm run validate:seo` — 构建产物 SEO 元数据检查
4. `npm run lint:content:a11y` — 无障碍内容 lint

### 可选测试
```bash
npm run test:axe        # axe 无障碍测试
npm run test:lighthouse # Lighthouse CI 审计
```

## SEO 优化策略

- JSON-LD 结构化数据
- OpenGraph + Twitter Cards
- XML sitemap 自动生成（构建时）
- 语义 HTML（H1 → H2 → H3 层次严格）
- 每页独立 `permalink` 和 `metaTitle`

## PWA 支持

通过 `docs/.vitepress/public/manifest.json` 配置，支持：
- 离线访问
- 安装到主屏幕
- Service Worker 缓存策略

## 规模参数

| 指标 | 数值 |
|------|------|
| 支持语言数 | 22 |
| 总页面数 | 1,450+ |
| 别名文档页 | 96（英文）× 22 = 2,112 页 |
| 构建产物 | `docs/.vitepress/dist/` |

## 关键约束

1. **零投机**：文档内容严格镜像源代码，不记录不存在的参数
2. **多语言同步**：更新英文后必须同步更新所有 22 个语言版本
3. **构建必须通过**：`npm run build` 失败则停止，不提交

## 参见

- [[entities/sebastienrousseau-dotfiles]] — 使用此方案的项目
- [[references/dot-cli-commands]] — 文档的核心内容之一
