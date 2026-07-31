---
title: >-
  chezmoi Source State Attributes — Reference
category: references
tags: [chezmoi, dotfiles, reference]
sources:
  - "https://www.chezmoi.io/reference/source-state-attributes/"
source_url: "https://www.chezmoi.io/reference/source-state-attributes/"
created: 2026-07-25T02:27:13Z
updated: 2026-07-25T02:27:13Z
summary: >-
  chezmoi 参考手册——源态属性。完整列出 dot_/private_/executable_/encrypted_ 等 17 个前缀及 2 个后缀。
provenance:
  extracted: 0.9
  inferred: 0.07
  ambiguous: 0.03
base_confidence: 0.69
lifecycle: draft
tier: supporting
lifecycle_changed: 2026-07-25
relationships:
  - target: "[[entities/chezmoi]]"
    type: related_to

---

# chezmoi Source State Attributes — Reference

- **URL**: https://www.chezmoi.io/reference/source-state-attributes/
- **角色**: 命名约定的完整参考（按目标类型分组）

## 源态存储

源目录默认 `~/.local/share/chezmoi`，可用 `-S` 或配置项 `sourceDir` 覆盖。文件/符号链接/目录目标对应同类型条目。一些状态直接编码在文件名中，可用 `chattr` 命令修改。

## 全部前缀

| 前缀 | 行为 |
|---|---|
| `after_` | 更新目标之后运行脚本 |
| `before_` | 更新目标之前运行脚本 |
| `create_` | 确保文件存在；缺失时按内容创建 |
| `dot_` | 加上隐藏前缀（`dot_foo` → `.foo`） |
| `empty_` | 即便空文件也保留（chezmoi 默认会删除空文件） |
| `encrypted_` | 在源态加密文件 |
| `external_` | 忽略子条目的属性 |
| `exact_` | 移除一切不在 chezmoi 管理下的内容 |
| `executable_` | 目标文件加可执行位 |
| `literal_` | 停止解析前缀属性 |
| `modify_` | 内容为脚本，用于修改既有文件 |
| `once_` | 仅当此前未成功运行时执行脚本 |
| `onchange_` | 仅当文件名/内容变更时运行脚本 |
| `private_` | 移除组与其他用户权限 |
| `readonly_` | 移除写权限 |
| `remove_` | 若存在则删除文件/链接，若为空则删除目录 |
| `run_` | 内容作为脚本执行 |
| `symlink_` | 创建符号链接而非常规文件 |

## 全部后缀

| 后缀 | 行为 |
|---|---|
| `.literal` | 停止解析后缀属性 |
| `.tmpl` | 内容作为模板处理 |

## 目标类型与允许的属性

属性顺序重要。完整规则：

- **目录 (Directory)**: `remove_`、`external_`、`exact_`、`private_`、`readonly_`、`dot_` —— 无后缀
- **常规文件 (File)**: `encrypted_`、`private_`、`readonly_`、`empty_`、`executable_`、`dot_` —— `.tmpl`
- **创建文件 (File)**: `create_`、`encrypted_`、`private_`、`readonly_`、`empty_`、`executable_`、`dot_` —— `.tmpl`
- **修改文件 (File)**: `modify_`、`encrypted_`、`private_`、`readonly_`、`executable_`、`dot_` —— `.tmpl`
- **移除文件 (File)**: `remove_`、`dot_` —— 无后缀
- **脚本 (File)**: `run_`、`once_` *或* `onchange_`、`before_` *或* `after_` —— `.tmpl`
- **符号链接 (File)**: `symlink_`、`dot_` —— `.tmpl`

## 字面属性（literal）

`literal_` 前缀或 `.literal` 后缀可出现在任意位置，立即停止属性解析，用于突破命名冲突。

## 加密后缀

- `.age` — age 加密（可由 `age.suffix` 覆盖）
- `.asc` — gpg 加密（可由 `gpg.suffix` 覆盖）

## 忽略规则

源目录中以 `.` 开头的文件/目录全部忽略，**`.chezmoi*` 除外**。

## 局限性

- 部分前缀组合未列出（隐含"不允许同时使用"，例如 `remove_` 与 `exact_` 互斥）
- 文档未明示命名长度上限（社区报告存在 255 字符问题）

## 相关链接

- [[concepts/chezmoi-attribute-prefixes]]
- [[concepts/chezmoi-three-state-model]]
- [[concepts/dotfile-manager]]
- [[references/chezmoi-templating-guide]]