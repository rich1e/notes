---
title: "MiniMax"
category: entities
tags: [minimax, ai-platform, mmx-cli, image-generation, llm]
summary: "全球 AI foundation model 公司，2022 年初成立，提供 MiniMax-M3 / MiniMax-Hailuo-2.3 / speech-2.8-hd / image-01 多模态模型，CLI 入口为 `mmx-cli`。"
sources:
  - "session:2026-09-04-mmx-image-character-sheet"
created: "2026-09-04T00:00:00Z"
updated: "2026-09-04T00:00:00Z"
tier: supporting
lifecycle: draft
lifecycle_changed: "2026-09-04"
base_confidence: 0.85
provenance:
  extracted: 0.95
  inferred: 0.05
  ambiguous: 0.0
relationships:
  - target: "[[skills/mmx-cli-image-generation]]"
    type: related_to
---

# MiniMax

> 全球 AI 基础模型公司，多模态能力通过 `mmx-cli` 暴露为 CLI。

## 是什么

- **公司**：MiniMax，2022 年初成立，全球 AI foundation model 公司
- **模型矩阵**：
  - 文本：`MiniMax-M3`（默认）
  - 视频：`MiniMax-Hailuo-2.3` / `MiniMax-Hailuo-2.3-Fast`（带图输入）/ `MiniMax-H3`（独立 skill `mmx-h3-video`）
  - 语音：`speech-2.8-hd`（默认）/ `speech-2.6` / `speech-02`
  - 图像：`image-01`
  - 视觉理解：VLM（`mmx vision describe`）
- **CLI**：`mmx-cli`（PyPI/npm 全局装），支持 OAuth 持久化到 `~/.mmx/credentials.json`、API key 持久化到 `~/.mmx/config.json`
- **Region**：自动检测，可 `--region global` 或 `--region cn` 覆盖

## 相关

- [[skills/mmx-cli-image-generation]] — 图像生成 CLI 实战与提示词硬限制