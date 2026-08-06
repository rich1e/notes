---
title: "gemini-notebook-mcp download_artifact 必须显式传 artifact_id"
category: concepts
tags:
  - notebooklm
  - mcp
  - gemini-notebook-mcp
  - bug
  - concept
sources:
  - conversation:2026-08-06
created: "2026-08-06T00:00:00Z"
updated: "2026-08-06T00:00:00Z"
summary: >-
  download_artifact 省略 artifact_id 时不保证下载"最新"产物，会静默取到旧的同类型 artifact，
  导致 v2 下载内容与 v1 完全一致（byte-identical）。
provenance:
  extracted: 0.7
  inferred: 0.25
  ambiguous: 0.05
base_confidence: 0.72
lifecycle: draft
lifecycle_changed: "2026-08-06"
tier: supporting
relationships:
  - target: "[[entities/gemini-notebook-mcp-cli]]"
    type: related_to
  - target: "[[skills/gemini-notebook-mcp-cli-setup]]"
    type: related_to
---

# gemini-notebook-mcp download_artifact 必须显式传 artifact_id

`download_artifact` 的 `artifact_id` 参数是可选的（工具签名允许省略，落到"使用最新一个"）,但实测中省略该参数会取回错误（旧）的产物，即使刚用 `studio_create` 生成了一个带有全新、不同 `artifact_id` 的新 slide_deck。

## What It Is

一次真实调试：为同一 notebook 生成第二版（v2）slide_deck，`studio_create` 返回了一个与 v1 不同的新 `artifact_id`，`studio_status` 也确认了两个独立的 artifact 条目。但 `download_artifact` 不传 `artifact_id` 直接下载后，产物文件与 v1 **byte-identical**（MD5 相同）。

## How It Works

`download_artifact` 在缺省 `artifact_id` 时的"取最新"逻辑不可靠——可能受 artifact 列表排序、缓存或 API 返回顺序影响，实际取到的不是刚创建的那个。显式传入 `studio_create` 返回的 `artifact_id`（或从 `studio_status` 里确认的目标 ID）才能保证下载到期望的版本。

## When to Use

任何时候用 `studio_create` 生成新产物（audio/video/slide_deck/report/...）后紧接着要下载，**永远显式传 `artifact_id`**，不要依赖默认行为。生成后先用 `studio_status(include_details=True)` 核对 artifact_id，再传给 `download_artifact`。这条规则同样应适用于 `download_all_artifacts`（未验证是否受同一问题影响，标记为待观察 ^[inferred]）。

## Related

- [[entities/gemini-notebook-mcp-cli]] — 工具全貌
- [[skills/gemini-notebook-mcp-cli-setup]] — 安装与配置
