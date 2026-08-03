---
title: Zellij — 终端复用器（tmux 友好替代）
category: skills
tags:
  - zellij
  - tmux
  - cli
  - tools
summary: Rust 写的现代化终端复用器，状态栏+提示键开箱即用，YAML 布局 + WebAssembly 插件系统，默认键反直觉但比 tmux 友好。
sources:
  - https://blog.csdn.net/2301_79518550/article/details/147495379
created: 2026-07-26
updated: 2026-07-26
tier: peripheral
lifecycle: draft
lifecycle_changed: "2026-07-26"
base_confidence: 0.55
provenance:
  extracted: 0.85
  inferred: 0.10
  ambiguous: 0.05
    type: related_to
relationships:
  - target: "[[entities/chezmoi]]"
    type: uses

---

# Zellij — 终端复用器（tmux 友好替代）

> Zellij 最初名为 "Mosaic"，Rust 编写，定位是"现代 tmux 替代"。

## 与 tmux/screen 的差异

| 特性 | Zellij | tmux | screen |
|------|--------|------|--------|
| 默认 UI | 状态栏+键位提示 | 需手动配置 | 无 |
| 插件系统 | WebAssembly（多语言） | 有限 | 无 |
| 布局系统 | YAML，智能优化 | 脚本化 | 无 |
| 学习曲线 | 低 | 中 | 高 |
| 跨平台 | Linux/macOS（Windows WIP） | 广泛 | 广泛 |
| 性能 | 高（Rust） | 高 | 中 |

## 安装

```bash
# macOS
brew install zellij

# Ubuntu/Debian
sudo apt install zellij

# Fedora
sudo dnf install zellij

# Arch
sudo pacman -S zellij

# Cargo
cargo install zellij

# 二进制
wget https://github.com/zellij-org/zellij/releases/latest/download/zellij-x86_64-unknown-linux-musl.tar.gz
tar -xzf zellij-x86_64-unknown-linux-musl.tar.gz
sudo mv zellij /usr/local/bin/
```

## 默认键位（按模式）

> Zellij 是**模式化**的——按前缀进入模式后，再按一次按键执行。比 tmux 的 `Ctrl+b` 单层组合更结构化。

| 模式 | 前缀 | 关键操作 |
|------|------|----------|
| **Pane（窗格）** | `Ctrl+p` | `n` 新建 / `r` 右分 / `d` 下分 / `x` 关闭 / 方向键切换 |
| **Tab（标签）** | `Ctrl+t` | `n` 新建 / `x` 关闭 / 方向键切换 |
| **Resize（调整）** | `Ctrl+n` | 方向键 |
| **Search（搜索）** | `Ctrl+s` | `j`/`k` 滚动 / `e` 打开编辑器 |
| **Session（会话）** | `Ctrl+o` | `d` 分离会话 |
| **Locked（锁定）** | `Ctrl+g` | 暂停所有 Zellij 键位（用来给 Vim 让路）|

**推荐修改**：`Ctrl+p` 与 Vim 冲突，建议改为 `Alt+p`（见配置文件一节）。

## 设为默认 Shell

在 `~/.zshrc` 或 `~/.bashrc` 加入：

```bash
if [[ -z "$ZELLIJ" ]]; then
    zellij
    exit
fi
```

`$ZELLIJ` 环境变量由 Zellij 自身在子 shell 中设置，避免嵌套启动。

## 配置文件 `~/.config/zellij/config.kdl`

```kdl
simplified_ui true        // 无 Nerd Font 时启用
default_layout "compact"
scroll_buffer_size 10000
mouse_mode false
theme "nord"

keybinds {
    normal {
        bind "Ctrl g" { Lock; }
        bind "Alt p" { SwitchToMode "pane"; }  // 推荐改 Ctrl+p → Alt+p
        bind "Ctrl t" { SwitchToMode "tab"; }
    }
}
```

KDL 格式（[kdl.dev](https://kdl.dev)）—— Zellij 自家的配置 DSL，比 tmux.conf 更结构化。

## 布局文件 `~/.config/zellij/layouts/*.yaml`

```yaml
layout:
  panes:
    - direction: Vertical
      panes:
        - command: "htop"
        - command: "bash"
    - direction: Horizontal
      panes:
        - command: "vim"
        - command: "tail -f /var/log/syslog"
```

启动：`zellij -l my_layout`。

为窗格设置环境变量：

```yaml
layout:
  panes:
    - command: "python manage.py runserver"
      env:
        DJANGO_SETTINGS_MODULE: "myproject.settings"
```

## 插件系统（WebAssembly）

**内置插件**：`compact-bar`（紧凑状态栏）、`strider`（类似 Ranger 的文件管理器）。

**安装插件**：

1. 下载 `.wasm` 文件
2. 放到 `~/.config/zellij/plugins/`
3. 在布局文件中引用：

```yaml
layout:
  panes:
    - plugin:
        location: "file:/path/to/plugin.wasm"
```

**开发插件**：用 Rust SDK `zellij-tile` 编写，编译成 `.wasm` 后加载。

## 常用命令

```bash
zellij                                 # 启动默认会话
zellij -s my_project                   # 启动命名会话
zellij ls                              # 列出所有会话
zellij attach <session_name>           # 重新连接
zellij kill-session <name>             # 关闭会话
zellij options --simplified-ui         # 启用简化 UI（无需 Nerd Font）
zellij setup --dump-config > ~/.config/zellij/config.kdl
```

## 浮动窗格与堆叠窗格

- **浮动窗格**：`Alt+p` → `f`（适合临时命令）
- **堆叠窗格**：窗格模式下按 `s`，多个窗格堆叠显示 + 数字键切换激活

## 复制粘贴

```bash
# 启用系统剪贴板（config.kdl）
copy_on_select true
copy_command "pbcopy"                   # macOS
copy_command "xclip -selection clipboard" # Linux
```

## 常见问题

- **状态栏乱码**：终端未启用 Nerd Font → 重装字体或 `simplified_ui true`
- **退格键冲突**：取消 `Ctrl h` 绑定
- **与 Vim/Emacs 冲突**：`Ctrl+g` 锁定 Zellij 键位
- **复制粘贴无效**：检查 `copy_command`

## 何时选 Zellij 而非 tmux

- 想要**开箱即用**的提示层（状态栏+键位提示）
- 团队内**非重度用户**为主，需要低学习曲线
- 想用 **YAML 布局** 一键启动固定窗格拓扑
- 想用**多语言写插件**（Rust/Python/Go via WASM）

仍选 tmux 的场景：

- 需要 **TPM 生态**（resurrect / yank / pain-control 等成熟插件）
- 服务器**最小化部署**（无图形栈）
- 已有大量 `.tmux.conf` 沉淀

## 相关页面

- [[skills/tmux]] — tmux 快捷键速查、配置、插件管理（TPM）
- [[concepts/dotfile-manager]] — 通过 [[entities/chezmoi.md|chezmoi]] 等工具管理 Zellij 配置（`config.kdl` + layouts）
