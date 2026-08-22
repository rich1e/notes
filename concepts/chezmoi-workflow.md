---
title: chezmoi Workflow — 四个动词 + 一次更新
category: concepts
tags: [chezmoi, dotfiles, workflow, concept]
sources:
  - "https://github.com/twpayne/chezmoi/discussions/2673"
  - "https://chezmoi.io/"
  - "https://axionl.me/p/%E5%BD%92%E6%A1%A3-%E7%94%A8-chezmoi-%E7%AE%A1%E7%90%86%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6/#gnome-keyring"
  -"https://litearch.cn/obsidian/notes/%E6%88%91%E7%9A%84%E7%AC%94%E8%AE%B0/%E7%BC%96%E7%A8%8B/Ops/17%E3%80%81chezmoi%20%E9%83%A8%E7%BD%B2%E7%BB%B4%E6%8A%A4%E6%95%99%E7%A8%8B.html"
  - "https://www.shuzhiduo.com/A/kvJ3V17Xzg/"
  - "https://github.com/twpayne/chezmoi/discussions/2424"
created: 2026-07-25T02:27:13Z
updated: 2026-07-26T10:00:00Z
summary: chezmoi 工作流围绕 add/edit/diff/apply 四个动词；跨机同步可用 update，亦可用 czpush/czpull/czapply 三段式别名明确推送、拉取与部署边界。
provenance:
  extracted: 0.85
  inferred: 0.12
  ambiguous: 0.03
base_confidence: 0.70
lifecycle: draft
lifecycle_changed: 2026-07-25
tier: core
    type: related_to
relationships:
  - target: "[[entities/chezmoi]]"
    type: related_to
---

# chezmoi Workflow — 四个动词 + 一次更新

chezmoi 把 dotfile 管理抽象为 4 个核心动词 + 1 个跨机同步动作。

## 四个核心动词

| 命令 | 输入 | 效果 |
|---|---|---|
| `chezmoi add <path>` | 实际态路径 | 把文件纳入源态，按命名约定重命名 |
| `chezmoi edit <path>` | 实际态路径 | 用 `$EDITOR` 打开源态对应文件 |
| `chezmoi diff` | — | 对比目标态与实际态 |
| `chezmoi apply` | — | 把目标态落到实际态 |

## 跨机同步动作

`chezmoi update` 通常完成 `git pull`、脚本执行、模板渲染和应用。若希望每个边界都可见，可将同步拆成下面的三段式别名。

## 三段式别名：把同步边界显式化

| 别名 | 方向 | 典型实现 | 语义边界 |
|---|---|---|---|
| `czpush` | 实际态 → 源态 → 远端 | 扫描受管文件、`chezmoi add`、提交并 `push` | 只推送，不拉取、不部署 |
| `czpull` | 远端 → 源态 | `chezmoi git -- pull --rebase --autostash` | 只拉取，不自动写入 `~/` |
| `czapply` | 源态 → 实际态 | `chezmoi apply -v` | 只部署，不联网 |

另一台机器同步配置应显式执行 `czpull && czapply`；推送本机修改则执行 `czpush`。这组别名对应 Git 的 `push` / `pull` / `apply`，避免混淆远端、源目录和家目录状态。shell 配置变更后通常还要 `exec bash` 或 `exec zsh` 重新加载。

## 新机引导与恢复检查

可用 `bootstrap.sh` 将 `age`、`chezmoi`、Neovim、Yazi、zoxide 等基础依赖安装、代理配置、AGE 私钥录入和 `chezmoi init/apply` 串成流水线。加密仓库恢复前必须准备 AGE 私钥；建议至少保存在密码管理器、加密 U 盘和纸质冷备三处，且绝不提交 Git。

部署故障排查时，先确认 `~/.config/chezmoi/chezmoi.toml`（其中的 `encryption = "age"` 是解密配置的关键）和 `~/.config/age/key.txt` 均存在。`chezmoi apply` 不一定会创建 `~/.ssh` 目录，应按需 `mkdir -p ~/.ssh && chmod 700 ~/.ssh`，并为 SSH 私钥、config 手动校正 `600` 权限。通过 raw GitHub URL 获取脚本时，使用 commit SHA 替代浮动分支 URL 可绕过 CDN 旧缓存。

## 新机引导动作

```sh
sh -c "$(curl -fsLS https://chezmoi.io/get)" -- init --apply $GITHUB_USERNAME
```

也可以先 `chezmoi init`，检查 `chezmoi diff` 后再 `chezmoi apply`。

## 最佳实践节奏

| 场景 | 推荐命令 |
|---|---|
| 第一次管理某配置 | `chezmoi add ~/.config/some/app` |
| 微调已管理配置 | `chezmoi edit ~/.config/some/app` |
| 提交前必做 | `chezmoi diff` |
| 跨机同步 | `chezmoi update -v` 或 `czpull && czapply` |
| 新机引导 | `chezmoi init --apply $REPO` |
| 看管理清单 | `chezmoi managed` |
| 停管（保留目标） | `chezmoi forget <file>` |

## 编辑器与 diff 工具自定义

`chezmoi edit` 默认跟随 `$VISUAL` / `$EDITOR`，`chezmoi diff` 默认走 `diff` 命令。两者都可在 `~/.config/chezmoi/chezmoi.toml` 中改成更顺手的工具。

最常见的一组是 **VSCode** ([#2424](https://github.com/twpayne/chezmoi/discussions/2424))：

```toml
[edit]
command = "code"
args = ["--wait"]

[diff]
command = "code"
args = ["--wait", "--diff", "{{ .Destination }}", "{{ .Target }}"]
```

`--wait` 必不可少——VSCode 默认非阻塞，chezmoi 需要等待编辑器关闭才能继续 diff/apply。

详见 [[skills/chezmoi-vscode-integration]]。

## 相关链接

- [[concepts/chezmoi-three-state-model]]
- [[concepts/dotfile-manager]]
- [[concepts/chezmoi-attribute-prefixes]]
- [[references/chezmoi-workflow-discussion]]
- [[skills/chezmoi-vscode-integration]]
