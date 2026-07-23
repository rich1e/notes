---
title: Fabric (danielmiessler)
category: entities
tags: [ai-tools, prompt-engineering, llm, cli-tools, open-source]
sources:
  - "https://github.com/danielmiessler/Fabric"
created: 2026-07-09T08:00:00Z
updated: 2026-07-09T08:00:00Z
summary: >-
  danielmiessler 出品的开源 AI 增强框架，通过可复用的 Prompt 模块（Patterns）解决 AI 集成难题，Go 编写，支持 20+ AI 提供商。
lifecycle: draft
base_confidence: 0.8
lifecycle_changed: 2026-07-09
---

# Fabric

**Fabric** 是 Daniel Miessler 创建的开源 AI 增强框架，使命是"通过 AI 促进人类繁荣"。

## 核心定位

> AI 没有能力问题——它有**集成**问题。

Fabric 通过将 AI 功能组织为可复用的 Prompt 模块（称为 **Patterns**），让人们能够方便地将 AI 集成到日常生活和工作流中。

## 关键数字

- **290+ 内置 Patterns**（截至 2026 年中）
- **20+ AI 提供商**支持（OpenAI、Anthropic、Gemini、Ollama、Azure、AWS Bedrock 等）
- **Go 语言**重写（原为 Python，现已迁移至 Go）
- **MIT 协议**开源

## 安装方式

```bash
# macOS (Homebrew)
brew install fabric-ai
alias fabric='fabric-ai'

# 一键安装脚本
curl -fsSL https://raw.githubusercontent.com/danielmiessler/fabric/main/scripts/installer/install.sh | bash

# 从源码
go install github.com/danielmiessler/fabric/cmd/fabric@latest

# 初始化配置
fabric --setup
```

## 典型用法

```bash
# 从剪贴板提取智慧
pbpaste | fabric --pattern extract_wisdom

# YouTube 视频摘要（流式输出）
fabric -y "https://youtube.com/watch?v=..." --pattern summarize --stream

# 分析 Claims
pbpaste | fabric --stream --pattern analyze_claims

# 使用思维链策略
echo "Analyze this code" | fabric --strategy cot -p analyze_code

# 启动 REST API 服务
fabric --serve
```

## REST API 服务模式

```bash
fabric --serve          # 默认 :8080
fabric --serve --serveOllama   # 兼容 Ollama API 格式
```

Ollama 兼容模式下，Patterns 作为模型名出现（如 `summarize:latest`），可无缝接入 Ollama 生态工具。

## 支持的 AI 提供商

**原生集成：** OpenAI、Anthropic、Google Gemini、Ollama、Azure OpenAI、Amazon Bedrock、Vertex AI、LM Studio、Perplexity

**OpenAI 兼容：** Groq、DeepSeek、Mistral、OpenRouter、SiliconCloud、Venice AI、Together 等 20+ 家

## Obsidian 集成

可通过 Shell 别名将 Pattern 输出直接保存到 Obsidian Vault：

```bash
obsidian_base="/path/to/obsidian"
for pattern_file in ~/.config/fabric/patterns/*; do
    pattern_name=$(basename "$pattern_file")
    eval "$pattern_name() { fabric --pattern \"$pattern_name\" -o \"$obsidian_base/\$(date +'%Y-%m-%d')-\$1.md\" }"
done
```

## 相关概念

- [[concepts/fabric-patterns]] — Pattern 设计理念与分类
- 提示工程思想 <!-- broken link: concepts/prompt-engineering-patterns does not exist -->
- [[skills/fabric-usage-patterns]] — 高频使用场景与最佳实践
- [[Research: Fabric AI Framework]] — Research: Fabric AI Framework
