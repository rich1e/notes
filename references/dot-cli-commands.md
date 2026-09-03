---
title: "dot CLI 命令参考"
category: references
tags: [dotfiles, cli, CLI, tools]
sources:
  - "https://github.com/sebastienrousseau/dotfiles.github.io"
  - "https://dotfiles.io"
created: 2026-07-27T06:20:00Z
updated: 2026-07-27T06:20:00Z
summary: "sebastienrousseau Trusted Shell Platform 的 dot CLI 工具，53 条命令覆盖核心管理、诊断、安全、AI 集成等 8 个类别。"
provenance:
  extracted: 0.92
  inferred: 0.06
  ambiguous: 0.02
base_confidence: 0.72
lifecycle: reviewed
lifecycle_changed: 2026-09-03
lifecycle_reason: "auto-promoted by wiki-lint --consolidate: age>30d, confidence>0.72"
lifecycle_changed: 2026-07-27
tier: peripheral
relationships:
  - target: "[[entities/sebastienrousseau-dotfiles]]"
    type: related_to
  - target: "[[entities/trusted-shell-platform]]"
    type: related_to
---

# dot CLI 命令参考

[[entities/trusted-shell-platform]] 提供的统一管理命令行工具，共 **53 条命令**，覆盖 8 大类别。

## Core（11 条）— 核心生命周期

| 命令 | 用途 |
|------|------|
| `dot apply` | 应用 dotfiles 配置到当前机器 |
| `dot sync` | 同步最新配置 |
| `dot update` | 更新 dotfiles |
| `dot add` | 添加文件到 dotfiles 管理 |
| `dot diff` | 显示当前状态与目标状态差异 |
| `dot status` | 显示管理文件状态 |
| `dot remove` | 从管理中移除文件 |
| `dot cd` | 切换到 dotfiles 源目录 |
| `dot edit` | 编辑指定文件 |
| `dot clean-cache` | 清理缓存 |
| `dot prewarm` | 预热缓存 |

## Diagnostics（14 条）— 诊断与健康检查

| 命令 | 用途 |
|------|------|
| `dot doctor` | 检查环境依赖 |
| `dot heal` | 自动修复已知问题 |
| `dot health` | 系统健康报告 |
| `dot verify` | 验证配置完整性 |
| `dot scorecard` | 生成配置质量评分 |
| `dot snapshot` | 创建环境快照 |
| `dot smoke-test` | 运行冒烟测试 |
| `dot chaos` | 混沌测试 |
| `dot bundle` | 打包配置 |
| `dot rollback` | 回滚到上一状态 |
| `dot drift` | 检测配置漂移 |
| `dot history` | 查看变更历史 |
| `dot benchmark` | 性能基准测试 |
| `dot perf` | 性能分析 |

## Appearance（4 条）— 外观定制

| 命令 | 用途 |
|------|------|
| `dot theme` | 切换主题 |
| `dot wallpaper` | 设置壁纸 |
| `dot fonts` | 管理字体 |
| `dot tune` | 微调外观设置 |

## Security（7 条）— 安全管理

| 命令 | 用途 |
|------|------|
| `dot backup` | 备份配置 |
| `dot encrypt-check` | 检查加密状态 |
| `dot firewall` | 防火墙配置 |
| `dot telemetry` | 遥测数据管理 |
| `dot dns-doh` | 配置 DNS-over-HTTPS |
| `dot lock-screen` | 锁屏配置 |
| `dot usb-safety` | USB 安全策略 |

## Secrets（5 条）— 密钥管理

| 命令 | 用途 |
|------|------|
| `dot secrets-init` | 初始化密钥管理 |
| `dot secrets` | 查看密钥 |
| `dot secrets-create` | 创建新密钥 |
| `dot ssh-key` | 管理 SSH 密钥 |
| `dot ssh-cert` | 管理 SSH 证书 |

## AI（3+ 条）— AI 工具集成

| 命令 | 用途 |
|------|------|
| `dot ai` | 主 AI 入口 |
| `dot ai-setup` | 配置 AI 工具 |
| `dot ai-query` | 执行 AI 查询 |

**AI 包装器**（wrapper 命令）：`cl`（Claude）、`gemini`、`kiro`、`sgpt`、`ollama`、`opencode`、`aider`

## Tools（5 条）— 工具管理

| 命令 | 用途 |
|------|------|
| `dot tools` | 列出可用工具 |
| `dot new` | 创建新项目 |
| `dot sandbox` | 启动沙盒环境 |
| `dot keys` | 快捷键参考 |
| `dot learn` | 学习资源 |

## Meta（3 条）— 元信息

| 命令 | 用途 |
|------|------|
| `dot upgrade` | 升级 dotfiles |
| `dot packages` | 管理包 |
| `dot version` / `dot help` | 版本信息与帮助 |

## 设计特点

- **诊断类命令最多（14 条）**：反映作者对可观测性的重视^[inferred]
- **AI 原生集成**：`dot ai` 系列命令 + 7 个主流 AI 工具包装器
- **安全优先**：独立的 Security 和 Secrets 两个类别，共 12 条命令
- **`dot chaos` / `dot drift`**：罕见的"混沌测试"和"配置漂移检测"命令，工业级运维思路

## 参见

- [[entities/sebastienrousseau-dotfiles]] — 主实体页
- [[concepts/shell-alias-taxonomy]] — 1250+ 别名分类
- [[entities/chezmoi]] — 底层状态管理
