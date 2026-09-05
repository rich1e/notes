---
title: "mmx-cli 图像生成：CLI 用法与提示词硬限制"
category: skills
tags: [mmx-cli, image-generation, minimax, cli, prompt-engineering, skill]
summary: "用 `mmx image generate` 生成图像的 CLI 流程：模型 `image-01`、3:4→1200×1600、`--prompt-optimizer` 提升稳定性，以及官方未文档化的 1500 字符提示词硬限制与 `--yes` 参数陷阱。"
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
  - target: "[[entities/minimax]]"
    type: related_to
  - target: "[[concepts/agentic-design]]"
    type: related_to
  - target: "[[skills/claude-code-mcp-auth-patterns]]"
    type: related_to
---

# mmx-cli 图像生成：CLI 用法与提示词硬限制

> mmx 是 MiniMax AI 平台官方 CLI，`mmx image generate` 是 Claude Code agent 在不接外部图像生成 API 时的最简路径——但有几个**官方 SKILL.md 未提及的硬限制**会在生产里绊人。

## 何时用 mmx image generate

适合：概念图、UI mockup、角色设定卡、风格验证、批量图集——任何"先出一版看看"的任务。
不适合：精确到像素的版式、需要可编辑文本（仍是模型弱项）、需要绝对一致的多张角色图（image-01 的 subject-ref 仍不稳定）。

## 一次跑通的最小命令

```bash
mmx image generate \
  --prompt "..." \
  --aspect-ratio "3:4" \
  --width 1200 --height 1600 \
  --prompt-optimizer \
  --out-dir /path/to/save \
  --out-prefix character-sheet \
  --quiet --non-interactive
```

| Flag | 含义 | 坑 |
|---|---|---|
| `--prompt` | 提示词 | **≤1500 字符硬限制**（见下） |
| `--aspect-ratio` | 比例，如 `3:4` / `16:9` | 同时设 `--width --height` 时被忽略 |
| `--width --height` | 像素（512–2048，8 的倍数） | **必须同时给**才会生效 |
| `--prompt-optimizer` | mmx 平台自动优化 prompt | 强烈推荐开启 |
| `--out-dir / --out-prefix` | 保存路径与文件名前缀 | 加 `--quiet` 时 stdout 只打印路径 |
| `--quiet` | 抑制进度条 | 与 `--non-interactive` 配合使 stdout 为纯数据 |
| `--non-interactive` | 缺参时直接报错 | 与 `--quiet` 配对即可 pipe 给下游 |
| `--yes` | 跳过确认 | **需要传值**（看似 boolean，实际不是） |
| `--n` | 生成张数 | 默认 1 |
| `--seed` | 复现种子 | 可省略 |
| `--subject-ref` | 主体参考（`type=character,image=path`） | 跨图一致性时用 |

## 三个官方 SKILL.md 没写的硬限制

### 1. 提示词 ≤1500 字符

API 实际限制是 **<1500 字符**（不是 "tokens"，是 chars）。超过会立刻报：

```
API error: invalid params, prompt length must be less than 1500 (HTTP 200)
```

注意 HTTP code 是 200，**报错信息藏在 `error.message` 里**，第一眼容易当成成功响应。

**应对**：分两次精简，先去形容词堆叠（"premium / refined / sophisticated / delicate"），再去场景化短句（"soft studio lighting"）。本次角色设定卡的提示词最终压在 1100 字符左右才通过。

### 2. `--yes` 需要传值

虽然其它 boolean flag（`--quiet` / `--non-interactive`）都能裸传，**`--yes` 必须带值**：

```bash
# ❌ 报错：Flag --yes requires a value.
mmx image generate --yes

# ✅ 三种都行
mmx image generate --yes=true
mmx image generate --yes 1
mmx image generate --yes 0   # 注意：0 仍然 "yes"，因为它有值
```

CI/agent 场景**不要用 `--yes`**，直接靠 `--non-interactive` 即可（缺参数立刻 fail，无确认提示）。

### 3. 3:4 比例 + 1200×1600 实际输出

`--aspect-ratio "3:4"` + 不设 width/height 时，平台默认输出 1024×1536 附近的尺寸。**显式加 `--width 1200 --height 1600` 才能拿到 3:4 的高分辨率**（仍是 8 的倍数 + 在 2048 范围内）。

`file` 验证：
```
JPEG image data, ..., 1200x1600, components 3
```

## 推荐流程：SVG 排版稿 + mmx 主体图 + 后期合成

复杂角色档案页的实战范式：

1. **先用 SVG 画版式**（`character-sheet.svg`）—— 文字、网格、栏目位置可控
2. **用 mmx 跑主体图**——三视图、表情头像、服装拆解等"画图难"的内容
3. **必要时再合成**——把 mmx 输出裁切后嵌进 SVG 占位框

mmx 不擅长精确文字，所以**文字部分必须自己控制**（SVG 或后期加）。把"画图"和"排版"分离，能让 mmx 的弱项不变成最终交付的弱点。

## 相关

- [[entities/minimax]] — mmx-cli 平台所属的 MiniMax AI
- [[concepts/agentic-design]] — DESIGN.md / shared memory 模式：mmx 这种"AI 工具"在 agent 工作流中作为外置能力
- [[skills/claude-code-mcp-auth-patterns]] — 同样是"接外部 AI 能力"的 CLI 实战经验，鉴权 + 踩坑模式可对照