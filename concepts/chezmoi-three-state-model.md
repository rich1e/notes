---
title: >-
  chezmoi Three-State Model — 源态/目标态/实际态
category: concepts
tags: [chezmoi, dotfiles, state-model, concept]
sources:
  - "https://github.com/twpayne/chezmoi/discussions/2673"
  - "https://www.chezmoi.io/reference/source-state-attributes/"
created: 2026-07-25T02:27:13Z
updated: 2026-07-25T02:27:13Z
summary: >-
  chezmoi 三态模型：源态（声明）在源目录，目标态（期望）经模板渲染，实际态（现状）在 home。`apply` 把目标态同步到实际态。
provenance:
  extracted: 0.8
  inferred: 0.15
  ambiguous: 0.05
base_confidence: 0.65
lifecycle: draft
lifecycle_changed: 2026-07-25
---

# chezmoi Three-State Model — 源态/目标态/实际态

chezmoi 把 dotfile 管理抽象成**三个独立状态**的协调问题。

## 三态定义

| 态 | 位置 | 含义 |
|---|---|---|
| **源态 (source state)** | `~/.local/share/chezmoi`（可覆盖） | 你的"声明"——含模板、属性前缀、加密内容，是 git 仓库 |
| **目标态 (target state)** | 内存中 | 源态经模板渲染/解密/脚本执行后的"应当长成什么" |
| **实际态 (actual state)** | `~/` | 真实文件系统现状 |

## `chezmoi apply` 的执行阶段

1. **脚本阶段**：执行所有 `run_*` 脚本（按 `before_` / `run_` / `after_` 时序）
2. **模板阶段**：渲染 `.tmpl` 与 `.chezmoitemplates/` 引用
3. **同步阶段**：把目标态落到实际态（创建/更新/删除/修改）

## 与"双态"模型（Stow）的关键差异

| 特性 | chezmoi（源态/目标/实际） | Stow（源镜像/目标 symlink） |
|---|---|---|
| 编辑目标 → 自动持久化 | 否 | 是 |
| 跨平台分支 | 模板内 if 分支 | 不同 git 分支 |
| 机密文件 | 加密原语 | 无内置 |
| 真实"diff" | `chezmoi diff` 渲染后 | `diff` 跟踪文件 |
| 状态机复杂度 | 显式三态 | 隐式两态 |

## 为什么是三态而不是两态

直接对照"源态 → 实际态"看似够用，但失去这些能力：

- **模板依赖运行时数据**（hostname、OS、密码管理器查表）——必须有一个"中间渲染层"才能产出目标
- **脚本副作用必须在同步前完成**（安装依赖包、生成 token）——顺序约束需要一个"阶段化"模型
- **加密必须先解密再比对**——目标态是解密后的视图，源态是密文

## 与 [[concepts/dotfile-manager]] 的关系

三态模型是 chezmoi 在 dotfile manager 设计空间里**主动选择复杂度**的体现——选 1（裸 git）的人不会有这个模型；选 4（Nix home-manager）的人会推得更远，把系统包也纳入声明。

## 相关链接

- [[concepts/dotfile-manager]]
- [[concepts/chezmoi-templating]]
- [[concepts/chezmoi-attribute-prefixes]]
- [[concepts/chezmoi-workflow]]
- [[entities/chezmoi]]