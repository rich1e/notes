---
title: CoDesign 项目的七屏源码从 session JSONL 重建
slug: codesign-session-jsonl-recovery
created: 2026-08-23
tags: [codesign, vite, recovery, figma, react]
sources:
  - "figma project session (2026-08-23)"
summary: >-
  当 CoDesign artifact.jsx 被某次 create 操作覆盖成占位时,可从
  ~/Library/Application Support/@open-codesign/desktop/sessions/<designId>.jsonl
  按顺序回放 create + str_replace + insert,完整重建上一版源码。
project: store/project for X/figma
base_confidence: 0.9
provenance:
  extracted: 0.85
  inferred: 0.15
  ambiguous: 0.0
lifecycle_changed: 2026-08-23
---

# CoDesign session JSONL — 项目源码的完整审计线索

## Context

某次 create 操作把 `/Users/rich1e/store/project for X/figma/App.jsx` 从约 2000 行的 7 屏基线覆盖成了 81 行的 recovery placeholder。磁盘本身、Claude 当前会话 JSONL、superpowers 归档都没有源码副本。

## Finding

CoDesign desktop 客户端会在 `~/Library/Application Support/@open-codesign/desktop/sessions/<designId>.jsonl` 维护一个逐行的工具调用审计日志(本项目 designId 为 `482ad7d4-a010-43d3-8517-078c4701af91`,日志 8MB)。每次 `str_replace_based_edit_tool` 的 `create / str_replace / insert` 都被原样记录下来。

### 重建步骤

1. **解析 JSONL**:每条 custom 类型的 tool_call payload 都有 `toolName === "str_replace_based_edit_tool"`,`args` 字段是 dict(包括 `command`、`path`、`file_text` / `old_str` / `new_str`)。
2. **确定起点**:`create` 命令里 file_text 最大的那次是上一版文件的快照。一次性 `create` 通常不是终版 — 本项目的终版是通过 ~30 步 `str_replace` 累加得到的。
3. **按时间顺序回放**:从起点 `create` 开始,依次应用后续的 `str_replace`(用模糊匹配处理行尾空白差异)和 `insert`(append 到末尾)。Screen 08 的探索型编辑需要按时间窗过滤(回退型编辑的副作用要被排除)。
4. **落到 React 模块**:CoDesign artifact 的尾巴 `ReactDOM.createRoot(document.getElementById("root")).render(<App />)` 在 Vite 环境里要改成 `export default App;`,否则会被 main.jsx 重复挂载导致静默失败。

## Implications

- CoDesign 的"create 覆盖失败 → 占位回滚"模式下,完整源码在本地不只有磁盘一份 — session 日志就是 second source。
- 任何最终态的 `create`(即使失败)都不会清空历史,可以从日志按 `command` 字段区分出"想落地的版本"和"占位回滚"。
- 这一恢复路径也意味着:在做大规模 str_replace 之前,**该**清掉早期残留的无效 anchor,否则后续 replace 会因为 old_str 找不到而连锁失败 — 这正是本项目前几轮反复修复失败的根因。

## Related

- [[entities/figwright]] — 双向 Figma MCP,涉及 CoDesign 文件但走的是不同协议
- [[concepts/atomic-state-recovery]] — 类似思路:状态文件被破坏时的二次证据路径