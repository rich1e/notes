---
title: Fabric 高频使用场景与工作流集成
category: skills
tags: [ai-tools, prompt-engineering, cli-tools, productivity]
sources:
  - "https://github.com/danielmiessler/Fabric"
created: 2026-07-09T08:00:00Z
updated: 2026-07-09T08:00:00Z
tier: peripheral
summary: >-
  Fabric CLI 的实际使用技巧：YouTube 分析、内容提炼、Obsidian 集成、REST API 服务模式、Shell 别名配置。
lifecycle: reviewed
base_confidence: 0.75
lifecycle_changed: "2026-08-12"
lifecycle_reason: "auto-promoted by wiki-lint --consolidate: age>30d, confidence>0.7"
---

# Fabric 使用场景与工作流集成

## 安装与初始化

```bash
# macOS
brew install fabric-ai
alias fabric='fabric-ai'   # 必须添加此别名

# 初始化（配置 API Key、默认模型等）
fabric --setup
```

## 核心使用模式

### 1. 管道输入（最常用）

```bash
# 从剪贴板读取（macOS）
pbpaste | fabric --pattern summarize

# 流式输出
pbpaste | fabric --stream --pattern analyze_claims

# 指定模型
pbpaste | fabric -m claude-opus-4-7 --pattern extract_wisdom
```

### 2. YouTube 视频分析

```bash
# 提取字幕并分析
fabric -y "https://youtube.com/watch?v=VIDEO_ID" --pattern summarize

# 带时间戳的字幕
fabric -y "URL" --transcript-with-timestamps --pattern extract_wisdom

# 获取评论
fabric -y "URL" --comments --pattern analyze_comments

# 同时开启视觉分析（需 FFmpeg）
fabric -y "URL" --visual --pattern summarize
```

### 3. 网页抓取

```bash
# 通过 Jina AI 抓取网页
fabric -u "https://example.com/article" --pattern summarize

# 问答式搜索
fabric -q "什么是 PTP 协议" --pattern ai
```

### 4. 文件直接输入

```bash
# 输入文件
fabric --pattern summarize < article.txt

# 带附件（图片识别）
fabric --pattern analyze_image -a screenshot.png
```

## Shell 别名配置

将所有 Pattern 注册为 Shell 命令：

```bash
# 添加到 ~/.zshrc
for pattern_file in $HOME/.config/fabric/patterns/*; do
    pattern_name="$(basename "$pattern_file")"
    alias "${pattern_name}"="fabric --pattern ${pattern_name}"
done

# YouTube 快捷函数
yt() {
    local video_link="$1"
    fabric -y "$video_link" --transcript
}
```

之后可直接运行：`summarize`、`extract_wisdom`、`yt URL` 等。

## 保存输出到 Obsidian

```bash
# 基础版：指定输出文件
pbpaste | fabric --pattern extract_wisdom -o ~/obsidian/2026-07-09-notes.md

# 进阶版：动态文件名别名
obsidian_base="$HOME/workspace/code/notes/_raw"
extract_wisdom() {
    local title="$1"
    local output="$obsidian_base/$(date +'%Y-%m-%d')-${title}.md"
    fabric --pattern extract_wisdom -o "$output"
}
# 用法：extract_wisdom "my-article-title"
```

## REST API 服务

```bash
# 启动服务（默认 :8080）
fabric --serve

# 指定地址和 API Key
fabric --serve --address :3000 --api-key my-secret

# Ollama 兼容模式（Pattern 作为模型名）
fabric --serve --serveOllama
```

Swagger UI 文档：`http://localhost:8080/swagger/index.html`

## 按 Pattern 指定模型

```bash
# 环境变量方式（在 ~/.zshrc 中）
export FABRIC_MODEL_PATTERN_EXTRACT_WISDOM="anthropic|claude-opus-4-7"
export FABRIC_MODEL_PATTERN_SUMMARIZE="openai|gpt-4o-mini"
```

## 常用 Pattern 速查

| 场景 | Pattern |
|------|---------|
| 提取核心洞察 | `extract_wisdom` |
| 快速摘要 | `summarize` |
| 分析真实性 | `analyze_claims` |
| 解释代码 | `explain_code` |
| 分析学术论文 | `analyze_paper` |
| 生成 commit 消息 | `create_git_diff_commit` |
| 分析安全威胁 | `analyze_threat_report` |
| 写作评估 | `analyze_prose` |

## 提示策略组合

```bash
# 深度推理（Chain-of-Thought）
echo "分析这段代码的性能" | fabric --strategy cot -p analyze_code

# 快速起草（Chain-of-Draft）
echo "写一篇关于 AI 的文章" | fabric --strategy cod -p write_essay
```

## 扩展（Extensions）

在 Pattern 的 system.md 中调用扩展：

```bash
# 注册扩展
fabric --addextension /path/to/extension.yaml

# 在 Pattern 中使用（仅限 pattern 文件内，不支持直接 stdin）
```

## 相关页面

- [[entities/fabric-ai]] — Fabric 工具整体介绍
- [[concepts/fabric-patterns]] — Pattern 设计理念与分类目录
- [[Research: Fabric AI Framework]] — Research: Fabric AI Framework
