---
title: "Dayfold Stitch 设计系统资产"
category: references
tags: [dayfold, stitch, ux, mobile, ui-design]
sources:
  - "dayfold/.stitch/designs/stitch-use.txt"
summary: "Dayfold 项目的 Google Stitch 设计系统资产索引：DESIGN.md、设计系统 ID、生成屏幕记录及本地文件布局。"
created: "2026-07-28T00:00:00Z"
updated: "2026-07-28T00:00:00Z"
tier: supporting
lifecycle: draft
lifecycle_changed: "2026-07-28"
base_confidence: 0.85
provenance:
  extracted: 0.90
  inferred: 0.10
  ambiguous: 0.00
relationships:
  - target: "[[entities/google-stitch]]"
    type: uses
  - target: "[[projects/dayfold/dayfold]]"
    type: related_to
  - target: [[concepts-design-system-as-ai-context × entities-google-stitch]]
    type: related_to
---

# Dayfold Stitch 设计系统资产

Dayfold 项目通过 Google Stitch MCP 建立的视觉设计系统，用于驱动所有 iOS 屏幕的生成。

## Stitch 项目标识

| 字段 | 值 |
|---|---|
| Project Name | `re-dayfold` |
| Project ID | `projects/13633875149271731736` |
| Design System Asset ID | `assets/4b1bee32e3894e98a837dda03816a473` |
| Design System Name | `dayfold-design-system` |
| DESIGN.md 路径 | `.stitch/DESIGN.md` |

## 设计系统概要

**暖灰深夜皮革阅读室风格**，从 Stitch 上传 `.stitch/DESIGN.md` 后自动创建。

主要 token：

| Token | 值 | 用途 |
|---|---|---|
| `warmPaper` | `#3C3C44` | 主背景色 |
| `warmLight` | `#434350` | Journal Card 表面 |
| `warmDark` | `#E8E8EC` | 主文字色 |
| `warmBrown` | `#9090A0` | 日期/元数据次文字 |
| `warmAccent` | `#E05A3A` | 暖橙强调色（CTA）|
| `cyanAccent` | `#5BC8D8` | 位置/天气点缀 |

字体：
- 标题：中文传统衬线（Songti/宋体）
- 正文：System Serif（日记正文）
- 元数据/标签：System Rounded

圆角：卡片 16pt，按钮 16pt，图片 20pt

## 已生成屏幕

### 1. Dayfold Home Screen（定调页面）

| 字段 | 值 |
|---|---|
| Screen ID | `ce330a7e2e21401aaf0a59d56b99575d` |
| 尺寸 | 780×2048（2× scale） |
| 状态 | COMPLETE |
| 本地 HTML | `.stitch/designs/dayfold-home.html`（13 KB）|
| 本地截图 | `.stitch/designs/dayfold-home.png`（55 KB）|

说明：首个定调页面，3D 笔记本封面 + 暖橙 FAB 双按钮（Browse / Write）。

### 2. Dayfold Timeline Home（首页主版本）

| 字段 | 值 |
|---|---|
| Screen ID | `a388af4f3bcb409c96322277639b94d2` |
| 尺寸 | 780×2134（2× scale）|
| 状态 | COMPLETE |
| 本地 HTML | `.stitch/designs/dayfold-timeline.html`（18 KB）|
| 本地截图 | `.stitch/designs/dayfold-timeline.png`（49 KB）|

已验证元素：
- ✅ Large Title "Dayfold" + 今日日期
- ✅ 内嵌搜索栏（rounded, subtle background）
- ✅ 按日期分组（"MON / 07" section header + 大字日期）
- ✅ Journal Card：时间·天气·位置 / 标题 / 摘要 / 最多 3 张缩略图 / 标签 + 收藏星
- ✅ 暖橙 FAB 圆形浮动按钮（右下 60×60pt）
- ✅ Bottom Tab Bar（首页/列表/笔记本/个人 4 图标）
- ✅ 暖灰夜色 + 暖橙强调配色

### 3. Dayfold Timeline (v2)（备选版本）

| 字段 | 值 |
|---|---|
| Screen ID | `5ca4994fc19248d394b946ea72d2b859` |
| 尺寸 | 780×2488（2× scale，更长） |
| 本地 HTML | `.stitch/designs/dayfold-timeline-v2.html`（16 KB）|
| 本地截图 | `.stitch/designs/dayfold-timeline-v2.png`（64 KB）|

说明：同一 session 重试触发的第二份，布局略有不同。主版本用 v1（2134 高度更紧凑）。

## 本地文件布局

```
dayfold/.stitch/
├── DESIGN.md                   # 设计系统源文件（17 KB，227 行）
├── metadata.json               # Stitch 资产索引（screenId / localAssets）
└── designs/
    ├── dayfold-home.html        # 定调 Home 页面
    ├── dayfold-home.png
    ├── dayfold-timeline.html    # Timeline 主版本 ★
    ├── dayfold-timeline.png
    ├── dayfold-timeline-v2.html # Timeline 备选
    ├── dayfold-timeline-v2.png
    └── stitch-use.txt           # Claude Code 会话记录（工作流备档）
```

## 上传流程回顾

见 [[skills/stitch-upload-design-md]] — 解决了 Claude Code Auto Mode 凭证检测的具体步骤。

关键操作顺序：
1. 向 `~/.claude/settings.json` 添加上传脚本白名单
2. 通过脚本调用 Stitch API 上传 DESIGN.md（返回 sourceScreen ID）
3. 调用 `mcp__stitch__create_design_system_from_design_md`（需 sourceScreen + screenInstance ID）
4. 保存 Design System Asset ID 到 `metadata.json`

## 后续计划

按 Stitch 推荐生成顺序：
- [ ] Entry Detail（日记详情页）
- [ ] Entry Editor（编辑器 / 写作页面）
- [ ] Calendar View（日历视图）
- [ ] Photo Wall（照片墙）
- [ ] Settings（设置页）
- [ ] Empty State（各屏幕空状态变体）

## 相关页面

- [[entities/google-stitch]] — Google Stitch 工具本体
- [[projects/dayfold/dayfold]] — Dayfold 项目概览
- [[skills/stitch-upload-design-md]] — DESIGN.md 上传操作技巧
- [[concepts/design-system-as-ai-context]] — DESIGN.md 作为 AI 硬约束输入的设计哲学
- [[concepts/design-md-format-spec]] — DESIGN.md 文件 schema
