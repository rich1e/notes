---
title: "trash wrapper 对脚本临时文件的污染"
category: skills
tags:
  - topic/zsh
  - topic/trash
  - topic/cli-safety
summary: "rm 包装为 trash 后,脚本中的临时文件删除会污染 ~/.Trash,需要显式 command rm 绕过"
tier: supporting
related: []
extends: null
contradicts: null
superseded_by: null
capture_source: claude-session
project: zsh-extend
base_confidence: 0.8
lifecycle: draft
lifecycle_changed: 2026-08-23
provenance:
  extracted: 0.85
  inferred: 0.15
sources:
  - "zsh-extend session (2026-08-23)"
---

# trash wrapper 对脚本临时文件的污染

## rm 包装为 trash 的代价

**Behavior:** 把 `rm` 包装成 `trash`（软删除到 `~/.Trash`）后，用户日常删除文件确实更安全（可恢复）。但脚本/函数里 `rm -f` 删除的临时文件（如 lazygit 的 `~/.lazygit/newdir`）也会被移到回收站，每次执行都留下副本。

**Explanation:** zsh 函数优先级高于 alias，包装后的 `rm()` 函数接管所有 `rm` 调用，无差别走 `trash`。trash-cli 不区分"用户手动删"和"脚本清理"。

## 受影响的场景

| 场景 | 现状 |
|------|------|
| `lg` (lazygit wrapper) 退出后 `rm -f ~/.lazygit/newdir` | 每次 lg 退出都在 ~/.Trash 留一个 newdir 副本 |
| npm/yarn 临时文件清理 | 频繁，~/.Trash 迅速膨胀 |
| pip/cache 清理 | 同上 |
| 系统级脚本（如 brew install 触发的 .pkg 删除） | 通常用 `command rm`，不会触发 wrapper |

## 解决模式

**Pattern:** 脚本/函数内部删除临时文件 → 用 `command rm` 显式绕过 wrapper：

```bash
# lg() 中
command rm -f "$LAZYGIT_NEW_DIR_FILE" > /dev/null
```

**通用规则**：
- ✅ 用户手动调用 `rm <file>` → 走 trash（软删除可恢复）
- ❌ 脚本/函数内部清理临时文件 → 用 `command rm`（绕过 wrapper）
- ⚠️ 临时判断：`rm` 是否在函数体 / alias / subshell 内被调用 → 是 → 用 `command`

## 防御性 wrapper 设计

**Workaround:** wrapper 函数可增加"调用上下文检测"，但复杂且不可靠。更简单的方式是**约定**：

```bash
# 在 zsh-extend.sh 头部加注释约定
# 规则：脚本/函数内删除临时文件必须用 'command rm'，
#      'rm' 仅供交互式命令行使用
```

**Confirmed by:** lg() 修改为 `command rm -f` 后，`~/.Trash` 不再出现 `newdir.*` 文件。

## trash CLI 选项速查

```bash
trash <file>...      # 移到 ~/.Trash
trash -l             # 列出回收站内容
trash -e             # 清空回收站（永久删除）
trash -y             # 跳过确认
trash -F             # 强制（删除 root-owned 文件）
```

## Notes

- 第三方 trash（macOS brew 包）路径在 `/opt/homebrew/opt/trash/bin/trash`，对应源码 GNU trash-cli 风格
- 类似 wrapper 设计原则：永不假设 wrapper 接管所有调用方；保留 `command` 前缀逃生通道