---
name: youtube-analyze
description: >-
  使用 Fabric 分析 YouTube 视频，提取字幕、视觉帧和洞察，可将结果保存到 Obsidian vault。
  当用户提供 YouTube 链接并想要分析、总结、提取知识时触发。
  触发场景：分析 YouTube 视频、提取视频内容、视频总结、从 YouTube 学习知识、把 YouTube 视频加入 wiki、
  "帮我看这个视频"、"分析这个 YouTube"、"提取这个视频的要点"、"这个视频讲了什么"。
  即使用户只是粘贴了 YouTube URL 并说"分析一下"或"总结一下"，也应使用此 skill。
---

# YouTube 视频分析

使用 [Fabric](https://github.com/danielmiessler/Fabric) 从 YouTube 视频中提取字幕、视觉内容和结构化洞察。

## 前置检查

在开始前确认 fabric 可用：

```bash
which fabric-ai || which fabric
```

如果不可用，提示用户：`brew install fabric-ai`，然后 `fabric --setup` 配置 API Key。

`--visual` 模式还需要 ffmpeg：`which ffmpeg`（不可用则 `brew install ffmpeg`）。

## 输入解析

接受以下格式的 YouTube 链接：
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://youtube.com/watch?v=VIDEO_ID&list=...`（优先取单视频，除非用户指定播放列表）

如果用户没有指定分析模式，询问或使用默认的 `extract_wisdom` pattern。

## 分析模式

### 模式 A — 字幕分析（快速，默认）

适用于有字幕的讲座、播客、演讲类视频：

```bash
fabric-ai -y "URL" --pattern extract_wisdom --stream
```

### 模式 B — 视觉 + 字幕（深度，推荐用于演示/教程类）

同时提取字幕和关键帧画面，适合技术演示、PPT 讲解、操作教程：

```bash
fabric-ai -y "URL" --pattern summarize --visual --stream
```

`--visual` 会用 FFmpeg 做场景检测，提取关键帧并通过 OCR 理解画面内容。

### 模式 C — 带时间戳（适合需要跳转查阅）

```bash
fabric-ai -y "URL" --transcript-with-timestamps --pattern summarize --stream
```

### 模式 D — 全量（字幕 + 评论 + 元数据）

```bash
fabric-ai -y "URL" --comments --metadata --pattern extract_wisdom --stream
```

## 选择合适的 Pattern

| 场景 | 推荐 Pattern |
|------|-------------|
| 通用知识提取（默认） | `extract_wisdom` |
| 快速摘要 | `summarize` |
| 学术讲座 | `summarize_lecture` |
| 视频按章节拆分 | `create_video_chapters` |
| 5 层深度摘要 | `create_5_sentence_summary` |
| 讨论/辩论类 | `summarize_debate` |
| YouTube 专用摘要 | `youtube_summary` |

用户也可以指定任意 fabric pattern：`fabric-ai --listpatterns` 查看全部 290+ 个。

## 执行步骤

1. **解析用户输入** — 提取 URL 和期望的分析类型
2. **选择模式** — 根据视频类型和用户需求选 A/B/C/D
3. **选择 Pattern** — 根据场景推荐，让用户确认或自选
4. **运行 fabric** — 执行命令，`--stream` 实时输出
5. **输出处理** — 决定是输出到终端、保存文件，还是存入 vault

## 保存到 Obsidian Vault（可选）

如果用户想把分析结果存入 wiki，保存到 `_raw/` 暂存区，让 `wiki-ingest` 后续处理：

```bash
fabric-ai -y "URL" --pattern extract_wisdom -o "$OBSIDIAN_VAULT_PATH/_raw/youtube-$(date +%Y%m%d-%H%M%S).md"
```

或直接输出到 vault 的 journal 目录（即时可用，跳过 ingest）：

```bash
fabric-ai -y "URL" --pattern extract_wisdom -o "$OBSIDIAN_VAULT_PATH/journal/youtube-VIDEO_TITLE.md"
```

Vault 路径从 `~/.obsidian-wiki/config` 读取（`OBSIDIAN_VAULT_PATH`）。

## 完整示例

```bash
# 最常用：提取洞察并流式输出
fabric-ai -y "https://youtube.com/watch?v=wPEyyigh10g" --pattern extract_wisdom --stream

# 技术演示（视觉模式）
fabric-ai -y "https://youtube.com/watch?v=VIDEO_ID" --pattern summarize --visual --stream

# 保存到 vault
VAULT=$(grep OBSIDIAN_VAULT_PATH ~/.obsidian-wiki/config | cut -d'"' -f2)
fabric-ai -y "https://youtube.com/watch?v=VIDEO_ID" \
  --pattern extract_wisdom \
  -o "$VAULT/_raw/youtube-$(date +%Y%m%d-%H%M%S).md" \
  --stream
```

## 后续步骤

分析完成后，告诉用户可以：
- 直接在终端阅读输出
- 如已保存到 `_raw/`：运行 `wiki-ingest` 将其蒸馏为正式 wiki 页面
- 如已保存到 `journal/`：直接在 Obsidian 中打开查看

## 错误处理

| 问题 | 解决方案 |
|------|---------|
| `fabric: command not found` | `brew install fabric-ai && alias fabric='fabric-ai'` |
| `ffmpeg not found`（--visual 模式） | `brew install ffmpeg` |
| 视频无字幕 | 切换到 `--visual` 模式，或用 `--transcript` 强制生成（部分视频支持自动字幕） |
| API Key 未配置 | `fabric-ai --setup` 重新配置 |
| 私有视频/地区限制 | 无法处理，提示用户 |
