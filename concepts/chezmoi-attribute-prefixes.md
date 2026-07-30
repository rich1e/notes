---
title: >-
  chezmoi Attribute Prefixes — 命名约定作元数据
category: concepts
tags: [chezmoi, dotfiles, naming, concept]
sources:
  - "https://www.chezmoi.io/reference/source-state-attributes/"
  - "https://chezmoi.io/"
created: 2026-07-25T02:27:13Z
updated: 2026-07-25T02:27:13Z
summary: >-
  chezmoi 把 dot_/private_/executable_/encrypted_/modify_ 等 17 个属性嵌入文件名。命名即元数据，源码可读、可审计。
provenance:
  extracted: 0.85
  inferred: 0.12
  ambiguous: 0.03
base_confidence: 0.66
lifecycle: draft
lifecycle_changed: 2026-07-25
relationships:
  - target: "[[entities/chezmoi]]"
    type: related_to

---

# chezmoi Attribute Prefixes — 命名约定作元数据

chezmoi 的核心理念：**不用额外 YAML/JSON 描述文件属性，直接把属性编进文件名**。一个文件名同时承载"路径映射 + 权限 + 类型 + 行为"。

## 完整前缀集合

| 前缀 | 用途 |
|---|---|
| `dot_` | 替换为 `.` 开头（隐藏文件） |
| `private_` | 0o600 权限 |
| `executable_` | 0o755 权限 |
| `readonly_` | 0o444 权限 |
| `empty_` | 即便空也保留 |
| `create_` | 缺失则创建 |
| `remove_` | 若存在则删除 |
| `modify_` | 内容是补丁脚本 |
| `exact_` | 移除目录中其他内容 |
| `external_` | 子条目忽略属性 |
| `symlink_` | 创建符号链接 |
| `run_` | 内容作为脚本执行 |
| `before_` / `after_` | 同步前后 |
| `once_` / `onchange_` | 一次性 / 内容变更时 |
| `encrypted_` | 加密原语 |
| `literal_` | 停止属性解析 |

## 典型例子

| 源文件名 | 目标 | 行为 |
|---|---|---|
| `dot_bashrc` | `~/.bashrc` | 普通文件 |
| `dot_bashrc.tmpl` | `~/.bashrc` | 渲染为模板后写入 |
| `private_dot_ssh/id_ed25519` | `~/.ssh/id_ed25519` | 0o600 权限 |
| `executable_dot_local/bin/script.sh` | `~/.local/bin/script.sh` | 0o755 |
| `encrypted_dot_netrc.age` | `~/.netrc` | age 加密存放 |
| `dot_config/Code/User/settings.json` | `~/.config/Code/User/settings.json` | 多层目录镜像 |

## 顺序很重要

属性前缀必须按官方规定的顺序书写，否则拒绝解析：

- 文件：`encrypted_` → `private_` → `readonly_` → `empty_` → `executable_` → `dot_`
- 脚本：`run_` → `once_`/`onchange_` → `before_`/`after_`

## 设计哲学：命名即元数据（"Convention over Configuration"）

- **可读**：仓库里只看文件名就知道这个文件在目标机器上长什么样
- **可审计**：所有元数据可见，没有 "magic config" 隐藏角落
- **可组合**：前缀可叠加，按顺序解锁不同属性
- **可 git diff**：普通文本差异即可反映属性变化

## 代价

- 文件名变长（如 `private_executable_dot_config/some-app/settings.json.tmpl`）
- 受文件系统 255 字符限制（社区报告深层嵌套会爆栈）
- 团队成员需要学习这套"约定"

## 相关链接

- [[concepts/chezmoi-three-state-model]]
- [[concepts/chezmoi-templating]]
- [[concepts/dotfile-manager]]
- [[references/chezmoi-source-state-attributes]]

## 相关页面

- [[synthesis/concepts-chezmoi-templating × concepts-chezmoi-attribute-prefixes]] — synthesis
