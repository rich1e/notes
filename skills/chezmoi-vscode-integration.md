---
title: chezmoi + VSCode — 把编辑器和 diff 工具换成 VSCode
category: skills
tags:
  - chezmoi
  - dotfiles
  - vscode
  - tools
summary: 在 ~/.config/chezmoi/chezmoi.toml 中配 [edit] 和 [diff] section 用 code --wait 调用 VSCode，让 dotfile 配置体验接近 IDE 工作流。
sources:
  - https://www.shuzhiduo.com/A/kvJ3V17Xzg/
  - https://github.com/twpayne/chezmoi/discussions/2424
created: 2026-07-26
updated: 2026-07-26
tier: peripheral
lifecycle: draft
lifecycle_changed: "2026-07-26"
base_confidence: 0.55
provenance:
  extracted: 0.88
  inferred: 0.10
  ambiguous: 0.02
relationships:
  - target: "[[concepts/chezmoi-workflow]]"
    type: related_to
  - target: "[[entities/chezmoi]]"
    type: related_to
---

# chezmoi + VSCode — 把编辑器和 diff 工具换成 VSCode

> `chezmoi edit` 默认根据 `$VISUAL` / `$EDITOR` 打开文件。把两者都改成 VSCode，再叠加 `--diff` 做对比，dotfile 管理体验接近 IDE 工作流。

## 为什么要换

- **语法高亮**：VSCode 对 `.zshrc` / `.bashrc` / `.toml` / `.yaml` 都有第一方语言支持
- **内置 diff**：VSCode 的 diff viewer 远超 `diff -u` 输出
- **多光标 / 搜索替换**：批量重命名变量、注释开关
- **远程同步**：WSL / SSH 远程目标也可走 VSCode Remote

## 配置文件位置

`~/.config/chezmoi/chezmoi.toml`（TOML 格式，**注意用双引号包裹 `--diff` 后面的 `{{ .Destination }}` 等模板变量**）。

## 把 edit 改成 VSCode

```toml
[edit]
command = "code"
args = ["--wait"]
```

`code --wait` 让 VSCode 阻塞直到文件关闭，chezmoi 才能继续后续 `diff` / `apply` 流程。

依赖：`code` 命令在 PATH 中（VSCode → Cmd+Shift+P → "Shell Command: Install 'code' command in PATH"）。

## 把 diff 改成 VSCode

```toml
[diff]
command = "code"
args = ["--wait", "--diff", "{{ .Destination }}", "{{ .Target }}"]
```

`--diff` 打开左右两栏 diff，`.Destination`（实际态）vs `.Target`（目标态）。

来源：[GitHub Discussion #2424](https://github.com/twpayne/chezmoi/discussions/2424) 里的官方推荐配置。

## 完整示例

```toml
# ~/.config/chezmoi/chezmoi.toml

[edit]
command = "code"
args = ["--wait"]

[diff]
command = "code"
args = ["--wait", "--diff", "{{ .Destination }}", "{{ .Target }}"]

[merge]
command = "code"
args = ["--wait"]
```

## 典型工作流

```bash
# 1. 首次添加某配置
chezmoi add ~/.bashrc

# 2. 编辑（VSCode 打开 dot_bashrc）
chezmoi edit ~/.bashrc

# 3. 对比（VSCode 打开左右两栏 diff）
chezmoi diff ~/.bashrc

# 4. 满意后应用（目标态 → 实际态）
chezmoi apply ~/.bashrc
```

## 替代方案

| 情景 | 替代 |
|------|------|
| 想用纯命令行 diff | `[diff] command = "diff" args = ["-u", "{{ .Destination }}", "{{ .Target }}"]` |
| 想用 Neovim | `[edit] command = "nvim"` |
| 想用 Helix | `[edit] command = "hx"` |
| 想用 terminal UI | `delta` / `difftastic` 包装 `diff` |

## 远程机器方案

如果 chezmoi 跑在远程机器（SSH），VSCode 通过 Remote-SSH 接管：

```toml
[edit]
command = "code"
args = ["--wait", "--remote", "ssh-remote+my-server"]
```

或更简单——本地 SSH 进去后，VSCode Server 自动接管，`code` 命令无需修改。

## 注意事项

- **`--wait` 不可少**：chezmoi 默认假设 editor 阻塞，VSCode 默认非阻塞
- **chezmoi apply 行为**：根据 chezmoi 工作目录的层级覆盖 `HOME` 目录对应文件
- **首次配完要重启 shell**：新的 `chezmoi.toml` 不会立即刷新

## 相关页面

- [[concepts/chezmoi-workflow]] — chezmoi 完整四动词工作流
- [[entities/chezmoi]] — chezmoi 实体页
- [[skills/chezmoi-bitwarden-secrets]] — chezmoi + Bitwarden 密钥管理
