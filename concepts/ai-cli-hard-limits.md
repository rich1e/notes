---
title: "AI CLI 调用硬限制"
category: concepts
tags: [ai-cli, prompt-engineering, mmx-cli, api-limits, hidden-flags]
summary: "AI provider 的 CLI 工具几乎都有\"文档未写\"的硬限制（提示词字符上限、flag 取值规则、HTTP code 200 包错）。典型案例：mmx image generate 的 1500 字符上限 + --yes 需传值；共通教训是用 stderr/log 而非 HTTP code 判定成功。"
sources:
  - "session:2026-09-04-mmx-image-character-sheet"
created: "2026-09-04T00:00:00Z"
updated: "2026-09-04T00:00:00Z"
tier: supporting
lifecycle: draft
lifecycle_changed: "2026-09-04"
base_confidence: 0.75
provenance:
  extracted: 0.90
  inferred: 0.10
  ambiguous: 0.0
relationships:
  - target: "[[skills/mmx-cli-image-generation]]"
    type: example_of
---

# AI CLI 调用硬限制

> 凡是 CLI 包装 AI provider 的工具，几乎都有"文档 SKILL.md 没说、报错信息藏在 error.message 里"的硬限制。

## 模式总结

| 维度 | 典型陷阱 | 防御 |
|---|---|---|
| **提示词长度** | mmx image generate **<1500 chars** 硬限制；多数 SDK 按 tokens 算 | 先发小版本确认能跑，再 scale up |
| **Flag 取值** | mmx `--yes` **需要传值**，与同命令的 `--quiet` / `--non-interactive` 直觉不一致 | 不依赖直觉，先 `mmx <cmd> --help` 看 schema |
| **HTTP code** | mmx 报错时 **HTTP 200** + JSON `error.message` 字段承载真实原因 | pipe 时解析 `--output json`，不要用退出码 + grep stdout |
| **Bool vs 取值 flag** | 同命令里两种风格共存（`--quiet` 裸传 vs `--yes=true`） | 写脚本时**统一传值**（`--yes=true` / `--quiet=true`） |
| **宽高同时** | mmx image 必须 `--width` + `--height` 同时给，单独传被忽略 | `--aspect-ratio` 不够时**两个都设** |

## 共通教训

### 1. 永远 pipe `--output json --quiet` + 解析 error.message

不要相信 HTTP code、不要相信 stdout 第一行。AI provider 的 SDK 经常把信息藏在 JSON 嵌套里——`mmx` 用 `--quiet` 时 stdout 是纯数据，`--output json` 时是结构化 JSON。

```bash
mmx image generate ... --output json --quiet --non-interactive
```

agent 场景的最佳实践：**只信任 JSON 的 `error.message` 字段**，不要 grep stdout。

### 2. CLI/agent 友好性 vs 文档完备性的鸿沟

大多数 AI 平台 CLI 都在追赶 agent 用户，但 SKILL.md 仍按"开发者手敲"心智写。两类用户痛点不同：

| 用户类型 | 关注 | 痛点 |
|---|---|---|
| 开发者手敲 | 参数语义、默认值 | 文档不全 |
| agent / CI 调用 | `--non-interactive`、`--quiet`、`--output json` | flag 取值不规整、退出码语义弱、错误信息藏在 JSON 里 |

agent 场景下，**预期 SKILL.md 30% 的内容需要靠实测补全**。

### 3. CLI 包装层的"二次封装"问题

mmx 这种 CLI 包装，等于在 SDK 之上又加了层 flag schema。出错栈：

```
User → mmx CLI flag parsing → mmx SDK → MiniMax HTTP API → mmx SDK 解析 → mmx CLI exit code/JSON
```

任何一层都可能把上游的"中文/英文错误信息"翻译走。**agent 看到的最终消息经常丢失 stack trace**，要把所有中间日志保留（stderr 不丢）。

## 相关

- [[skills/mmx-cli-image-generation]] — mmx image generate 三个硬限制的具体案例
- [[concepts/agentic-design]] — agent 工作流中"接外部 AI 能力"的抽象层