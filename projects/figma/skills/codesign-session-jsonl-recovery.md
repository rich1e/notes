---
title: 从 CoDesign session JSONL 恢复 artifact.jsx
category: skills
tags: [codesign, recovery, jsonl, figma, Bugfix]
sources:
  - store/project for X/figma session (2026-08-23)
created: 2026-08-23T16:15:00Z
updated: 2026-08-23T16:15:00Z
base_confidence: 0.9
lifecycle: draft
lifecycle_changed: "2026-08-23"
summary: CoDesign artifact.jsx 被某次 create 覆盖成占位时,可从 ~/Library/Application Support/@open-codesign/desktop/sessions/<designId>.jsonl 按顺序回放 create + str_replace + insert 完整重建上一版源码
---

# 从 CoDesign session JSONL 恢复 artifact.jsx

## 适用场景

CoDesign desktop 客户端的某次 `create` 操作把 artifact.jsx(通常在 `~/store/project for X/<name>/figma/App.jsx`)从完整基线覆盖成了几行的 recovery placeholder,而磁盘本身、Claude 当前会话 JSONL、superpowers 归档都没有源码副本。

## 关键发现

CoDesign desktop 会在 `~/Library/Application Support/@open-codesign/desktop/sessions/<designId>.jsonl` 维护一个**逐行的工具调用审计日志**(本项目 designId 为 `482ad7d4-a010-43d3-8517-078c4701af91`,日志 8MB / ~1500 行)。每次 `str_replace_based_edit_tool` 的 `create / str_replace / insert` 都被原样记录下来 — 这就是源码的 second source。^[extracted:JSONL schema 实际观察]

每条记录的 `custom.data.payload`:

```json
{
  "toolName": "str_replace_based_edit_tool",
  "args": {
    "command": "create | str_replace | insert",
    "path": "App.jsx",
    "file_text": "...",          // 仅 create
    "old_str": "...",            // 仅 str_replace
    "new_str": "..."             // str_replace 和 insert
  }
}
```

## 恢复步骤

### 1. 解析 JSONL

用 Python `json.loads` 逐行读,过滤 `type === "custom"` + `data.kind === "tool_call"` + `payload.toolName === "str_replace_based_edit_tool"` 的记录。

### 2. 确定起点(并非永远是最后一次 create)

- `file_text` 长度最大的那次 `create` 通常是**上一版完整文件**的快照
- 但**一次性 `create` 几乎从不是终版** — 本项目的终版通过 30+ 步 `str_replace` 累加得到,最后一次 `create` 是占位回滚(只需 81 行)
- 鉴别方法:`create` 的 `file_text` 第一行是否包含 "Recovery in progress" / "Recovery placeholder" 这类自描述字样 → 是占位回滚,跳过

### 3. 按时间顺序回放编辑

```python
state = None
for kind, line_no, payload in edits:
    if kind == 'create':
        state = payload  # 整文件
    elif kind == 'str_replace':
        old, new = payload
        if old in state:
            state = state.replace(old, new, 1)
        else:
            # 模糊匹配:处理行尾空白差异
            if old.rstrip() in state:
                state = state.replace(old.rstrip(), new, 1)
    elif kind == 'insert':
        state = state + payload  # 追加到末尾
```

### 4. 过滤"探索型编辑"

如果项目经历过多次失败-回滚(典型如 Screen 08),需要按时间窗截取:
- 本项目方案:只取 L783(create 三屏起点)~ L1192(footer 升级到 "Seven screens")之间,跳过之后的 Screen 08 探索和最终回滚
- 鉴别依据:L1279 之后的 str_replace 都围绕 `// === END SCREEN 08 ===` 反复修补 — 这是探索期的明显信号

### 5. 落地为 React 模块

CoDesign artifact 末尾自带 `ReactDOM.createRoot(document.getElementById("root")).render(<App />)`(依赖全局 React)。要回放到 Vite 调试,必须改两处:
- 删掉末尾 createRoot,替换为 `export default App;`
- 详见 [[projects/figma/skills/codesign-artifact-vite-scaffold]]

## 已知陷阱

- **`str_replace` 的 old_str 找不到**:不要反复试同一个 anchor — 用 `view` 读全文重新对齐;三次失败后 CoDesign harness 会锁住本回合工具调用
- **`insert` 与 `str_replace` 顺序混淆**:`insert` 是追加到末尾(不是光标位置插入),误以为插入到当前行会导致后续 anchor 错位
- **空白差异**:`str_replace` 的 old_str 末尾可能有尾随换行,被替换文件可能有 BOM — 模糊匹配前先 `repr(old[:50])` 确认格式

## 验证恢复成功

恢复后用以下三个信号确认:

1. **函数计数**:`re.findall(r'function (\w+)\(', source)` 应返回 35+ 个组件
2. **React 挂载**:Vite 启动后 `document.getElementById('root').innerHTML.length > 0`
3. **DOM 节点数**:完整七屏应有 3172 个 DOM 元素 + 15893px 页面高度

## Related

- [[projects/figma/figma]] — 项目概览
- [[projects/figma/skills/codesign-artifact-vite-scaffold]] — 恢复后如何本地启动
- [[concepts/atomic-state-recovery]] — 类似思路:状态文件 corrupt 时的二次证据