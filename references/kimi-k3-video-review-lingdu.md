---
title: "Kimi K3 突然爆火！实测到底有多强？（零度解说）"
category: references
tags: [Deepseek, chinese-ai, video-review]
sources:
  - "https://www.youtube.com/watch?v=8_JZehVSRAI"
source_url: "https://www.youtube.com/watch?v=8_JZehVSRAI"
created: 2026-07-23T09:00:00Z
updated: 2026-07-23T09:00:00Z
summary: >-
  零度解说对 Kimi K3 的中文实测视频（2026-07-20，11.5 万播放）。涵盖基准对比、Agent 虚拟机能力、3D 生成演示、越狱情况和 API 成本对比。
provenance:
  extracted: 0.70
  inferred: 0.25
  ambiguous: 0.05
base_confidence: 0.52
lifecycle: draft
lifecycle_changed: 2026-07-23
---

# Kimi K3 突然爆火！实测到底有多强？（零度解说）

**来源：** https://www.youtube.com/watch?v=8_JZehVSRAI  
**频道：** 零度解说（UCvijahEyGtvMpmMHBu4FS2w）  
**发布：** 2026-07-20  
**时长：** 约 8.7 分钟（520 秒）  
**播放量：** 115,846（截至研究日期）  

> 注：本视频无字幕，内容通过帧分析（每 30 秒一帧，共 17 帧）提取。内容摘要为帧画面与字幕文字的直接描述，置信度适中。

## 视频结构（帧分析）

### 第一部分：基准测试背景
展示 **DeepSWE v1.1 排行榜**（Datacurve 出品）：
| 模型 | 得分 |
|---|---|
| GPT-5.6 Sol | 72% |
| Claude Fable-5 | 68% |
| GPT-5.5 | 61% |
| Claude（另一版本）| 46% |
| Claude（另一版本）| 30% |
| xAI | 13% |

Kimi K3 未出现在该榜单（推测该视频拍摄时 K3 尚未入榜或入榜靠后）^[inferred]

**LiveBench 质量/成本分析**（livebench.ai）：
- Kimi K3 每成功任务成本：**$0.379**
- 成本排名中游（优于 Claude 4.6 Opus Thin $0.404，弱于 GPT-5.6 Sol xHigh Eff $0.355）
- Grok 4.5 最便宜：$0.128/成功任务

### 第二部分：Kimi 平台演示

**Kimi 官网功能入口：**
- 集群 / PPT 生成 / 深度研究 / 网站创建 / 文档处理 / 表格分析

**Kimi Agent 虚拟机能力（核心亮点）：**
- `windows-xp.kimi.site`：浏览器内完整 Windows XP 模拟，红色警戒 2 可正常运行
- `macos27.kimi.page`：浏览器内 macOS 27 模拟，FaceTime 等应用可用（"因为里面功能都可以用"）

### 第三部分：代码生成对比

视频展示 Claude Code（接入 K3）在 `/effort high` 模式下生成 Three.js FPS 射击游戏：
- 5 阶段规划：场景搭建 → 第一人称控制 → AK47 武器系统 → 靶机 + 命中检测 → 游戏逻辑 + HUD
- 产出：13 个文件，约 2,600 行代码
- 包含：后坐力动画、枪口火焰、弹道追踪线、冲击火花粒子系统

**成本对比：**
字幕"而 Claude 花了 0.94 美金"——暗示同等任务 K3 的 API 成本低于或媲美 Claude Fable-5

### 第四部分：K3 3D 内容生成

K3 直接生成交互式 3D 网页（无需编码工具）：
- 骑马探索开放世界（秋季场景，实时光影）
- 四冲程发动机 3D 可视化演示（DOHC 直列四缸，可交互点火顺序）— 字幕"Kimi K3 完全吊打"
- 应县木塔数字展览（10,611 件构件，千年古建筑数字复原）
- 中国古代武侠风格 3D 游戏场景

### 第五部分：安全性（越狱）

标题与描述明确指出"模型已被越狱"：
- 越狱教程链接：https://www.freedidi.com/24857.html（2026-07-20 发布）
- 说明 K3 的安全对齐在发布时存在可利用的弱点

## 关键数据点

| 指标 | 值 | 来源 |
|---|---|---|
| DeepSWE v1.1 最优模型 | GPT-5.6-Sol 72% | Datacurve 榜单截图 |
| LiveBench 成本（K3）| $0.379/成功任务 | livebench.ai 截图 |
| FPS 游戏代码量 | 13 文件 / ~2600 行 | Claude Code 输出截图 |
| Apple 仿制网站（Claude 成本）| $0.94 | 视频字幕 |
| 应县木塔构件数 | 10,611 件 | K3 生成页面截图 |

## 局限性

- **无字幕**：内容通过帧分析推断，可能遗漏口头说明的细节
- **视频为推广性质**：零度解说频道附带 VPN 和会员推广链接，客观性有限
- **越狱内容**：视频链接至越狱教程，相关内容属于安全测试性质

## 关联页面

- [[entities/kimi-k3]] — 模型实体页
- [[entities/moonshot-ai]] — 开发商
- [[synthesis/Research: Kimi K3]] — 综合研究报告
