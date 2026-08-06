---
title: "studio_create 的 source_ids 与 custom_prompt 语义（含 CLI/MCP 参数名差异）"
category: concepts
tags:
  - notebooklm
  - mcp
  - gemini-notebook-mcp
  - prompt-engineering
  - concept
sources:
  - conversation:2026-08-06
created: "2026-08-06T00:00:00Z"
updated: "2026-08-06T00:00:00Z"
summary: >-
  source_ids 是硬性内容边界（决定读哪些来源），custom_prompt 是软性内容引导（决定怎么解读）；
  两者必须搭配用才能精确控制 slide_deck 内容；nlm CLI 里 custom_prompt 对应的是 --focus，且可能比 MCP 的 custom_prompt 更弱。
provenance:
  extracted: 0.75
  inferred: 0.2
  ambiguous: 0.05
base_confidence: 0.7
lifecycle: draft
lifecycle_changed: "2026-08-06"
tier: supporting
relationships:
  - target: "[[entities/gemini-notebook-mcp-cli]]"
    type: related_to
  - target: "[[skills/gemini-notebook-mcp-cli-setup]]"
    type: related_to
---

# studio_create 的 source_ids 与 custom_prompt 语义

`studio_create`（含 `artifact_type=slide_deck`）用两个不同层次的参数控制产物内容：`source_ids` 决定"读什么"，`custom_prompt` 决定"怎么解读"。二者不可互相替代。

## What It Is

- **`source_ids`**：硬性边界。省略时默认使用 notebook 内**全部**来源；只有显式传入来源 ID 列表才能把生成范围限制到子集。想让一份 slide_deck 只覆盖某个主题（而排除同 notebook 里的竞品资料），唯一可靠做法是传入该主题对应的 `source_ids` 子集，而不是在 prompt 里写"忽略 XX 类来源"。
- **`custom_prompt`**：软性引导。在已确定的来源集合之上，指示模型按特定问题结构（如"1. 核心价值 2. 架构 3. 实践 4. 短板"）组织内容、要求逐条引用来源、要求不要在资料未说明处臆测。它不改变读取哪些来源，只改变呈现和分析角度。

## How It Works

`studio_create` 首次调用返回 `{"status": "pending_confirmation", ...}` 展示拟定设置，需要带 `confirm=True` 重新调用才会真正执行创建。`custom_prompt` 字符串会被当作对模型的指令模板，而非字面文本粘贴进产物——测试确认它能有效引导内容结构（如强制分点、强制引用来源）。

**CLI 与 MCP 参数名不一致** ^[extracted]：`nlm` CLI 的 `slides create` 子命令用 `--focus` 表达等价于 MCP `custom_prompt` 的意图，但命名暗示其语义可能更窄（"聚焦主题"而非"完整指令模板"），实际强度未在本次验证 ^[ambiguous]。若通过 CLI 手动执行发现效果比 MCP 弱，应改用更强的措辞或换回 MCP 路径。

## When to Use

- 需要限定 slide_deck 只覆盖 notebook 子集来源时：用 `source_ids`，不要依赖 prompt 排除指令。
- 需要控制产物的分析角度、结构、引用规范时：用 `custom_prompt`（MCP）或 `--focus`（CLI）。
- 两者组合使用（子集来源 + 结构化 prompt）是精确控制 NotebookLM 生成内容的标准做法，本次会话验证于同一 notebook 生成"纯主题版"与"主题+竞品对比版"两份不同 slide_deck 的场景。

## Related

- [[entities/gemini-notebook-mcp-cli]] — 工具全貌，含 `nlm`/MCP 双产品说明
- [[skills/gemini-notebook-mcp-cli-setup]] — 安装与配置
- [[concepts/nlm-artifact-id-required-for-download]] — 同一调试会话中发现的另一 gotcha
