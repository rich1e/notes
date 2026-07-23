---
title: Fabric Patterns — AI 增强的可复用 Prompt 模块
category: concepts
tags: [prompt-engineering, ai-tools, llm, open-source]
sources:
  - "https://github.com/danielmiessler/Fabric"
  - "https://github.com/danielmiessler/fabric/tree/main/data/patterns"
created: 2026-07-09T08:00:00Z
updated: 2026-07-09T08:00:00Z
summary: >-
  Fabric Patterns 是结构化、可复用的 AI Prompt 单元，用 Markdown 编写，组织在独立目录中，覆盖 290+ 真实任务场景。
lifecycle: draft
base_confidence: 0.75
lifecycle_changed: 2026-07-09
---

# Fabric Patterns

**Patterns** 是 [[entities/fabric-ai|Fabric]] 框架的核心抽象：将 AI 能力封装为**标准化、可复用、可分享的 Prompt 单元**，每个 Pattern 对应一个真实世界的具体任务。

## 设计原则

1. **Markdown 格式** — 最大化可读性和可编辑性，对人和 AI 都友好
2. **System Prompt 优先** — 指令几乎全部放在 System Prompt 中，经验证效果更稳定
3. **极度清晰的指令** — 明确说明要做什么、按什么顺序做
4. **单一职责** — 每个 Pattern 解决一个具体问题

## Pattern 结构

每个 Pattern 存放在独立目录中：

```
~/.config/fabric/patterns/
└── extract_wisdom/
    ├── system.md    # 主要指令（System Prompt）
    └── user.md      # 可选的用户提示模板
```

## Pattern 分类（290+ 个）

### 分析类（analyze_*）
- `analyze_claims` — 分析主张真实性，提供证据与反驳
- `analyze_paper` — 分析研究论文，评估研究质量
- `analyze_threat_report` — 提取网络安全威胁报告的关键发现
- `analyze_malware` — 分析恶意软件指标与检测策略
- `analyze_prose` — 评估写作的新颖性、清晰度和文笔
- `analyze_debate` — 评估辩论表现，提供无偏见分析

### 提取类（extract_*）
- `extract_wisdom` — **核心 Pattern**：从内容中提取有见地的洞察、引用、习惯、事实
- `extract_ideas` — 提取主要观点
- `extract_article_wisdom` — 从文章中提取智慧

### 创建类（create_*）
- `create_summary` — 生成摘要
- `create_coding_project` — 生成项目线框图和启动代码
- `create_git_diff_commit` — 生成 Git commit 消息
- `create_mermaid_visualization` — 生成 Mermaid 图表
- `create_sigma_rules` — 创建 SIGMA 检测规则
- `create_stride_threat_model` — 创建 STRIDE 威胁模型

### 总结类（summarize）
- `summarize` — 通用摘要
- `create_micro_summary` — 极简摘要
- `create_5_sentence_summary` — 5 层深度摘要（5句→1句）

### 安全类（cybersecurity）
- `create_cyber_summary` — 网络安全威胁摘要
- `create_report_finding` — 安全报告发现格式化
- `create_network_threat_landscape` — 网络威胁态势分析

### 内容处理
- `clean_text` — 修复格式错误的文本
- `convert_to_markdown` — 转换为 Markdown
- `rate_content` — 评估内容质量

## extract_wisdom — 旗舰 Pattern

`extract_wisdom` 是 Fabric 中最具代表性的 Pattern，展示了 Pattern 设计的精髓：

```markdown
# IDENTITY and PURPOSE
You extract surprising, insightful, and interesting information from text content...

# STEPS
- Extract a summary in 25 words → SUMMARY
- Extract 20-50 surprising/insightful IDEAS (each exactly 16 words)
- Extract 10-20 refined INSIGHTS (fewer, more abstract)
- Extract 15-30 QUOTES with speaker attribution
- Extract 15-30 practical HABITS
- Extract 15-30 world FACTS
- Extract all REFERENCES mentioned
- ONE-SENTENCE TAKEAWAY (15 words)
- Extract 15-30 RECOMMENDATIONS (each 16 words)
```

关键设计细节：字数限制（每条 16 词）强制精炼，避免冗余输出。

## Prompt Strategies（提示策略）

Patterns 可与策略组合使用，修改 System Prompt 的推理方式：

| 策略 | 说明 |
|------|------|
| `cot` | Chain-of-Thought：逐步推理 |
| `cod` | Chain-of-Draft：迭代起草，每步最多 5 词 |
| `tot` | Tree-of-Thought：多路径推理，取最佳 |
| `aot` | Atom-of-Thought：拆解为最小原子子问题 |
| `ltm` | Least-to-Most：从易到难解决子问题 |
| `self-refine` | 回答→批评→精炼 |
| `reflexion` | 回答→简短批评→精炼回答 |

```bash
echo "解释递归" | fabric --strategy cot -p explain_code
```

## 自定义 Pattern

```bash
# 设置自定义 Pattern 目录（优先级高于内置）
mkdir -p ~/my-patterns/my-analyzer
echo "You are an expert analyzer of ..." > ~/my-patterns/my-analyzer/system.md
fabric --pattern my-analyzer "analyze this text"
```

## Pattern 变量

```bash
# -v 传入变量
fabric --pattern my-pattern -v '#role:expert' -v '#points:30'
```

## 相关链接

- [[entities/fabric-ai]] — Fabric 工具整体介绍
- [[skills/fabric-usage-patterns]] — 高频用法与工作流集成
- [[concepts/prompt-caching]] — LLM 提示缓存机制（相关背景）
- [[Research: Fabric AI Framework]] — Research: Fabric AI Framework
