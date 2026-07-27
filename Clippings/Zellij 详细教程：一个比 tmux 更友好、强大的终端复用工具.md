---
title: Zellij 详细教程：一个比 tmux 更友好、强大的终端复用工具
source: https://blog.csdn.net/2301_79518550/article/details/147495379
author:
  - "[[2301_79518550]]"
published: 2025-06-28
created: 2026-07-26
description: 文章浏览阅读5.6k次，点赞26次，收藏32次。Zellij是一款用Rust开发的现代化终端复用器，相比传统工具tmux更加用户友好。它提供会话管理、智能布局系统、WebAssembly插件支持等特性，默认界面直观易用。安装方式多样，可通过包管理器或下载二进制文件快速部署。核心功能包括窗格管理（Ctrl+p）、标签切换（Ctrl+t）等，支持自定义快捷键。Zellij特别适合需要高效管理多终端会话的用户，其简化了tmux的复杂操作，同时保留了强大功能。通过合理配置，可显著提升命令行工作效率。_zellij
tags:
  - clippings
  - Zellij
  - tmux
---
在终端环境中，终端复用器（Terminal Multiplexer）是一种不可或缺的工具。它能够将单一的终端会话分割为多个独立的工作区域，不仅实现“一心多用”，还便于会话管理，确保任务不会因误关闭终端窗口或 SSH 连接中断而丢失。这种特性对于开发者、系统管理员以及命令行爱好者来说尤为重要。

提到终端复用器，许多人首先想到的是经典的 `tmux` ，其名称正是 “terminal multiplexer” 的缩写。凭借庞大的插件生态和高度的可定制性， `tmux` 无疑是一个功能强大、潜力近乎无限的工具。然而，尽管 `tmux` 功能卓越，其复杂的操作逻辑和令人费解的默认键位设置却让不少用户望而却步。网上流传的许多 `tmux` 配置教程，往往以大篇幅修改快捷键开篇，这恰恰反映了默认键位设计的反直觉。（我甚至忍不住怀疑， `tmux` 的作者可能是个拥有二十根手指的外星人，并且使用了一种极为小众的非 QWERTY 键盘布局。）

最近，我发现了一款名为 **Zellij** 的工具。虽然其开发者并未明确宣称它是 `tmux` 的替代品，但 Zellij 在功能上完全可以媲美甚至超越 `tmux` ，同时拥有更加人性化的用户界面、更直观的键位设计。相比传统的终端复用工具如 `tmux` 和 `screen` ，Zellij 提供了更加流畅、直观的操作方式和现代化设计，尤其适合需要高效管理多个终端会话的用户。

本文将为你提供一份全面的 Zellij 使用指南，涵盖安装步骤、基本操作、高级配置、插件使用以及实用技巧，力求帮助你在终端工作环境中如鱼得水。无论你是初次接触终端复用器的新手，还是希望从 `tmux` 迁移而来的资深用户，这篇教程都将助你快速掌握 Zellij 的核心功能，打造高效的命令行工作流。

---

### 一、Zellij 简介

Zellij 是一款用 Rust 语言开发的开源终端工作空间工具，最初名为“Mosaic”。它不仅继承了传统终端复用器的核心功能（如会话管理、窗口分割），还通过内置的布局系统和 WebAssembly 插件系统，提供了高度的自定义能力和现代化用户体验。Zellij 的设计理念是“简单而不失强大”，既适合初学者快速上手，也满足高级用户对深度定制的需求。

#### 主要特性

- **友好的用户界面** ：Zellij 默认提供状态栏和快捷键提示，极大降低学习曲线。
- **智能布局系统** ：支持通过 YAML 文件定义窗格布局，自动优化窗格排列。
- **插件系统** ：基于 WebAssembly，支持用多种语言编写插件，扩展功能。
- **会话管理** ：支持会话分离和重新连接，即使网络中断也能保持进程运行。
- **跨平台支持** ：目前支持 Linux 和 macOS，Windows 支持正在开发中。
- **现代化设计** ：浮动窗格、堆叠窗格等创新功能，提升操作灵活性。

Zellij 的官方教程（ [https://zellij.dev/screencasts/）提供了直观的视频演示，推荐初学者观看以快速了解其界面和操作逻辑。](https://zellij.dev/screencasts/%EF%BC%89%E6%8F%90%E4%BE%9B%E4%BA%86%E7%9B%B4%E8%A7%82%E7%9A%84%E8%A7%86%E9%A2%91%E6%BC%94%E7%A4%BA%EF%BC%8C%E6%8E%A8%E8%8D%90%E5%88%9D%E5%AD%A6%E8%80%85%E8%A7%82%E7%9C%8B%E4%BB%A5%E5%BF%AB%E9%80%9F%E4%BA%86%E8%A7%A3%E5%85%B6%E7%95%8C%E9%9D%A2%E5%92%8C%E6%93%8D%E4%BD%9C%E9%80%BB%E8%BE%91%E3%80%82)

---

### 二、Zellij 安装

Zellij 提供了多种安装方式，适用于不同的操作系统和用户需求。以下是详细的安装步骤，涵盖 Linux 和 macOS 系统。

#### 1\. 前置条件

在安装 Zellij 之前，请确保你的系统满足以下要求：

- **操作系统** ：Linux（支持 Ubuntu、Debian、Arch 等主流发行版）或 macOS。
- **终端环境** ：建议使用支持 Nerd Fonts 的终端模拟器（如 Alacritty、iTerm2、Kitty）以获得最佳显示效果。
- **网络连接** ：部分安装方式需要下载二进制文件或依赖包。

#### 2\. 安装方式

##### 方法一：通过包管理器安装（推荐）

大多数 Linux 发行版和 macOS 的 Homebrew 提供 Zellij 的软件包，安装简单且易于更新。

**Linux（Ubuntu/Debian）**

```bash
sudo apt update
sudo apt install zellij
bash12
```

**Linux（Fedora）**

```bash
sudo dnf install zellij
bash1
```

**Linux（Arch Linux/Manjaro）**

```bash
sudo pacman -S zellij
bash1
```

**macOS（使用 Homebrew）**

```bash
brew install zellij
bash1
```

安装完成后，运行以下命令验证安装是否成功：

```bash
zellij --version
bash1
```

输出类似 `zellij 0.40.0` 表示安装成功。

##### 方法二：通过 Cargo 安装

如果你熟悉 Rust 生态，可以使用 Rust 的包管理器 Cargo 安装 Zellij。这种方式适合需要最新版本或希望参与开发的用户。

1. 确保已安装 Rust 环境：
	```bash
	curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
	source $HOME/.cargo/env
	bash12
	```
2. 使用 Cargo 安装 Zellij：
	```bash
	cargo install zellij
	bash1
	```
3. 验证安装：
	```bash
	zellij --version
	bash1
	```

**注意** ：Cargo 安装的 Zellij 默认位于 `~/.cargo/bin/` ，需确保该路径在你的 `$PATH` 环境变量中。

##### 方法三：使用预编译二进制文件

如果你的系统没有 Zellij 的软件包，或者你需要特定版本，可以直接下载官方提供的二进制文件。

1. 访问 Zellij 官方 GitHub Release 页面（ [https://github.com/zellij-org/zellij/releases）。](https://github.com/zellij-org/zellij/releases%EF%BC%89%E3%80%82)
2. 下载适合你系统的二进制文件（例如 `zellij-x86_64-unknown-linux-musl.tar.gz` ）。
3. 解压并安装：
	```bash
	wget https://github.com/zellij-org/zellij/releases/latest/download/zellij-x86_64-unknown-linux-musl.tar.gz
	tar -xzf zellij-x86_64-unknown-linux-musl.tar.gz
	sudo mv zellij /usr/local/bin/
	bash123
	```
4. 验证安装：
	```bash
	zellij --version
	bash1
	```

##### 方法四：从源代码编译（高级用户）

如果你想体验最新功能或参与开发，可以从源代码编译 Zellij。

1. 克隆 Zellij 仓库：
	```bash
	git clone https://github.com/zellij-org/zellij.git
	cd zellij
	bash12
	```
2. 安装编译依赖（以 Ubuntu 为例）：
	```bash
	sudo apt install build-essential pkg-config libssl-dev
	bash1
	```
3. 编译并运行：
	```bash
	cargo build --release
	./target/release/zellij
	bash12
	```

**注意** ：从源代码编译可能需要较长时间，且主分支可能包含不稳定的功能，建议普通用户优先选择其他安装方式。

#### 3\. 安装 Nerd Fonts（可选）

Zellij 的默认插件（如状态栏）使用 Nerd Fonts 中的字符以增强显示效果。建议安装 Nerd Fonts 以获得最佳体验。

**安装步骤** ：

1. 下载 Nerd Fonts（推荐 JetBrains Mono 或 Fira Code）：
	```bash
	wget https://github.com/ryanoasis/nerd-fonts/releases/download/v3.0.0/JetBrainsMono.zip
	bash1
	```
2. 解压并安装字体（以 Linux 为例）：
	```bash
	unzip JetBrainsMono.zip -d ~/.fonts
	fc-cache -fv
	bash12
	```
3. 在终端模拟器中设置字体为 JetBrains Mono Nerd Font。

如果不想安装 Nerd Fonts，可以启用简化界面：

```bash
zellij options --simplified-ui
bash1
```

---

### 三、Zellij 基本使用

Zellij 的核心功能是管理终端会话、窗格（Pane）和标签（Tab）。以下是从启动到常用操作的详细介绍。

#### 1\. 启动 Zellij

在终端输入以下命令启动 Zellij：

```bash
zellij
bash1
```

启动后，Zellij 会创建一个默认会话，屏幕底部显示状态栏，提示可用快捷键。默认界面包括：

- **窗格** ：终端窗口的子区域，每个窗格运行一个独立的 Shell。
- **标签** ：类似于浏览器标签页，用于组织多个窗格集合。
- **状态栏** ：显示快捷键提示和当前模式。

#### 2\. 基本概念

- **会话（Session）** ：Zellij 的顶级管理单元，一个会话可以包含多个标签和窗格。
- **标签（Tab）** ：类似于 tmux 的窗口，用于组织一组窗格。
- **窗格（Pane）** ：终端的最小单元，运行 Shell 或其他程序。
- **插件** ：扩展功能模块，如状态栏、文件管理器等。

#### 3\. 默认快捷键

Zellij 使用前缀键（Prefix Key）触发操作，默认前缀键为 `Ctrl` + 特定字母。以下是常用快捷键（假设未修改默认配置）：

| 操作模式 | 前缀键 | 功能 | 快捷键 |
| --- | --- | --- | --- |
| 窗格模式（Pane） | `Ctrl + p` | 新建窗格 | `n` |
|  |  | 向右新建窗格 | `r` |
|  |  | 向下新建窗格 | `d` |
|  |  | 切换窗格 | 方向键（ `←↓↑→` ） |
|  |  | 关闭当前窗格 | `x` |
| 标签模式（Tab） | `Ctrl + t` | 新建标签 | `n` |
|  |  | 切换标签 | 方向键（ `←→` ） |
|  |  | 关闭标签 | `x` |
| 调整模式（Resize） | `Ctrl + n` | 调整窗格大小 | 方向键（ `←↓↑→` ） |
| 搜索模式（Search） | `Ctrl + s` | 滚动历史 | `j` （向下）、 `k` （向上） |
| 会话模式（Session） | `Ctrl + o` | 分离会话 | `d` |
| 锁定模式（Locked） | `Ctrl + g` | 锁定/解锁界面 | `Ctrl + g` |

**推荐修改** ：默认的 `Ctrl + p` （窗格模式）可能与其他工具（如 Vim 的查找）冲突，建议改为 `Alt + p` 。修改方法见“高级配置”部分。

**提示** ：状态栏会动态显示当前模式的快捷键提示，初学者无需 记忆 所有快捷键。官方教程（ [https://zellij.dev/screencasts/](https://zellij.dev/screencasts/) ）也提供了直观的快捷键演示。

#### 4\. 基本操作示例

##### 创建和管理窗格

1. 启动 Zellij 后，按 `Ctrl + p` （或自定义的 `Alt + p` ）进入窗格模式。
2. 按 `n` 创建新窗格，Zellij 会自动选择最佳分割方向（水平或垂直）。
3. 使用方向键切换焦点到其他窗格。
4. 按 `x` 关闭当前窗格。

##### 创建和管理标签

1. 按 `Ctrl + t` 进入标签模式。
2. 按 `n` 创建新标签。
3. 使用 `←` 或 `→` 切换标签。
4. 按 `x` 关闭当前标签。

##### 调整窗格大小

1. 按 `Ctrl + n` 进入调整模式。
2. 使用方向键调整当前窗格的尺寸。
3. 按 `Esc` 退出调整模式。

##### 滚动和查看历史

1. 按 `Ctrl + s` 进入搜索模式。
2. 使用 `j` 和 `k` 上下滚动终端历史。
3. 按 `e` 打开默认编辑器查看历史输出。

##### 会话管理

1. 按 `Ctrl + o` 进入会话模式。
2. 按 `d` 分离当前会话（Zellij 继续在后台运行）。
3. 查看现有会话：
	```bash
	zellij ls
	bash1
	```
4. 重新连接会话：
	```bash
	zellij attach <session_name>
	bash1
	```

---

### 四、Zellij 高级配置

Zellij 支持深度定制，用户可以通过配置文件、布局文件和插件扩展功能。

#### 1\. 配置文件

Zellij 默认在 `~/.config/zellij/` 目录下查找 `config.kdl` 文件。如果不存在，可以生成默认配置文件：

```bash
zellij setup --dump-config > ~/.config/zellij/config.kdl
bash1
```

以下是一个示例配置文件，展示了常用选项，包括推荐的 `Alt + p` 键位修改：

```fsharp
// 启用简化界面（不使用 Nerd Fonts）
simplified_ui true

// 设置默认布局
default_layout "compact"

// 控制历史缓冲区大小
scroll_buffer_size 10000

// 禁用鼠标支持
mouse_mode false

// 自定义主题
theme "nord"

// 快捷键绑定
keybinds {
    normal {
        bind "Ctrl g" { Lock; }
        bind "Alt p" { SwitchToMode "pane"; } // 推荐将 Ctrl + p 改为 Alt + p
        bind "Ctrl t" { SwitchToMode "tab"; }
    }
}
kdl1234567891011121314151617181920212223
```

**常用配置项** ：

- `simplified_ui` ：启用简化界面，适合无 Nerd Fonts 的环境。
- `scroll_buffer_size` ：设置历史缓冲区行数，越大占用内存越多。
- `copy_on_select` ：控制鼠标选中内容是否自动复制。
- `theme` ：设置界面主题（如 `nord` 、 `dracula` ）。
- `keybinds` ：自定义shortcut键绑定，推荐将 `Ctrl + p` 改为 `Alt + p` 以避免冲突。

#### 2\. 布局文件

Zellij 支持通过 YAML 文件定义窗格布局，启动时自动加载。布局文件默认存储在 `~/.config/zellij/layouts/` 目录。

**创建布局文件** ：

1. 创建布局文件 `my_layout.yaml` ：
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
	yaml12345678910
	```
2. 使用布局启动 Zellij：
	```bash
	zellij -l my_layout
	bash1
	```

**布局文件示例** ：

- `direction` ：指定分割方向（ `Vertical` 或 `Horizontal` ）。
- `command` ：指定窗格运行的命令。
- `size` ：设置窗格大小（百分比或固定值）。

#### 3\. 插件系统

Zellij 的插件基于 WebAssembly，可以用 Rust 或其他语言开发。默认插件包括：

- **compact-bar** ：简化的状态栏。
- **strider** ：文件管理器（类似 Ranger）。

**安装插件** ：

1. 下载插件的 WebAssembly 文件（`.wasm` ）。
2. 将插件文件放入 `~/.config/zellij/plugins/` 。
3. 在布局文件中引用插件：
	```yaml
	layout:
	  panes:
	    - plugin: 
	        location: "file:/path/to/plugin.wasm"
	yaml1234
	```

**开发插件** ：  
Zellij 提供 Rust SDK（ `zellij-tile` ）用于开发插件。参考官方文档（ [https://zellij.dev/documentation/plugin-development）获取详细指南。](https://zellij.dev/documentation/plugin-development%EF%BC%89%E8%8E%B7%E5%8F%96%E8%AF%A6%E7%BB%86%E6%8C%87%E5%8D%97%E3%80%82)

---

### 五、实用技巧与常见问题

Zellij 的灵活性和强大功能使其在日常使用中可以极大提升效率。以下是一些实用技巧和常见问题的详细解答，帮助你更好地掌握 Zellij 的使用，并解决可能遇到的问题。

#### 1\. 实用技巧

##### 设置 Zellij 为默认 Shell

为了每次打开终端时自动启动 Zellij，你可以在 Shell 的配置文件中添加相应设置。以下是以 Bash 和 Zsh 为例的配置方法：

- **Bash** ：  
	编辑 `~/.bashrc` 文件，添加以下内容：
	```bash
	if [[ -z "$ZELLIJ" ]]; then
	    zellij
	    exit
	fi
	bash1234
	```
	这段代码检查是否已经在 Zellij 会话中（通过 `$ZELLIJ` 环境变量），如果不在，则启动 Zellij 并在退出 Zellij 时关闭终端。
- **Zsh** ：  
	编辑 `~/.zshrc` 文件，添加类似内容：
	```
	if [[ -z "$ZELLIJ" ]]; then
	    zellij
	    exit
	fi
	zsh1234
	```
- **Fish** ：  
	编辑 `~/.config/fish/config.fish` ，添加：
	```
	if not set -q ZELLIJ
	    zellij
	    exit
	end
	fish1234
	```

**注意** ：如果你希望保留原始 Shell 的访问权限，可以省略 `exit` 命令，这样在退出 Zellij 后会返回到普通 Shell。

##### 自动加载特定布局

如果你经常使用特定的窗格布局，可以将其设置为默认布局，无需每次手动指定。编辑 Zellij 配置文件 `~/.config/zellij/config.kdl` ，添加：

```
default_layout "my_layout"
kdl1
```

然后确保 `~/.config/zellij/layouts/my_layout.yaml` 存在。例如：

```yaml
layout:
  panes:
    - command: "htop"
    - command: "bash"
yaml1234
```

每次启动 Zellij 时，将自动加载该布局。

##### 快速启动命名会话

为避免会话名称冲突或便于管理，可以在启动时指定会话名称：

```bash
zellij -s my_project
bash1
```

你还可以创建 Shell 别名以简化操作。编辑 `~/.bashrc` 或 `~/.zshrc` ，添加：

```bash
alias zp='zellij -s my_project'
bash1
```

之后只需运行 `zp` 即可启动名为 `my_project` 的会话。

##### 使用环境变量优化工作流

Zellij 支持在窗格中设置环境变量，适合需要特定环境的项目。例如，在布局文件中为某个窗格设置环境变量：

```yaml
layout:
  panes:
    - command: "python manage.py runserver"
      env:
        DJANGO_SETTINGS_MODULE: "myproject.settings"
yaml12345
```

这确保窗格运行时自动加载指定的环境变量。

##### 高效复制粘贴

Zellij 默认支持鼠标选中复制（需启用 `copy_on_select` ）。若想优化复制体验，可结合系统剪贴板工具：

- **Linux（使用 `xclip` ）** ：  
	安装 `xclip` ：
	```bash
	sudo apt install xclip
	bash1
	```
	在 Zellij 中选中内容后，按 `Ctrl + c` （需自定义快捷键），运行：
	```bash
	echo "selected_text" | xclip -selection clipboard
	bash1
	```
- **macOS** ：  
	使用 `pbcopy` ：
	```bash
	echo "selected_text" | pbcopy
	bash1
	```

你还可以在 `config.kdl` 中启用自动复制：

```
copy_on_select true
copy_command "xclip -selection clipboard" // Linux
// 或
copy_command "pbcopy" // macOS
kdl1234
```

##### 多人协作（实验性功能）

Zellij 正在开发多人协作功能，允许多个用户共享同一会话，适用于教学或远程调试。启动会话时启用实验性功能：

```bash
zellij --enable-experimental-features
bash1
```

具体使用方式请参考官方文档的最新更新。

##### 使用浮动窗格和堆叠窗格

Zellij 支持浮动窗格（Floating Pane）和堆叠窗格（Stacked Pane），适合临时任务或复杂布局：

- **创建浮动窗格** ：按 `Alt + p` （或原 `Ctrl + p` ），然后按 `f` 。
- **切换到堆叠窗格** ：在窗格模式下按 `s` ，将多个窗格堆叠显示，仅激活一个窗格。
- **切换堆叠窗格** ：使用 `Alt + p` 后按 `1` 、 `2` 等切换堆叠中的窗格。

这些功能特别适合在有限屏幕空间内管理多个任务。

##### 定时备份会话状态

Zellij 自动保存会话状态，但你可以通过脚本定期备份会话以防止意外丢失。示例脚本：

```bash
#!/bin/bash
zellij list-sessions > ~/.zellij_session_backup.txt
bash12
```

将此脚本加入 crontab 定时运行：

```bash
crontab -e
* * * * * /path/to/backup_zellij.sh
bash12
```

##### 集成外部工具

Zellij 可以与 `fzf` 等工具结合，提升文件导航效率。例如，在布局文件中运行 `fzf` ：

```yaml
layout:
  panes:
    - command: "fzf"
yaml123
```

或者绑定快捷键运行 `fzf` ：

```
keybinds {
    normal {
        bind "Alt f" { Run "fzf"; }
    }
}
kdl12345
```

#### 2\. 常见问题

- **问题** ：状态栏显示乱码或字符缺失。  
	**解决** ：确保终端模拟器使用 Nerd Fonts（如 JetBrains Mono）。安装字体后，刷新字体缓存：
	```bash
	fc-cache -fv
	bash1
	```
	若不想使用 Nerd Fonts，可在配置文件中启用简化界面：
	```nginx
	simplified_ui true
	kdl1
	```
- **问题** ：按退格键（Backspace）无法删除字符，反而触发其他操作（如进入移动模式）。  
	**解决** ：修改 Zellij 配置文件（默认路径： `~/.config/zellij/config.kdl` ）：
	```fsharp
	keybinds {
	  unbind "Ctrl h" // 解除 Ctrl+H 的默认绑定
	  // 或者直接使用非冲突预设
	  // unlock-first
	  }
	kdl12345
	```
- **问题** ：快捷键与 Vim、Emacs 等工具冲突。  
	**解决** ：
	1. 进入锁定模式（默认 `Ctrl + g` ）暂停 Zellij 快捷键。
		2. 自定义快捷键以避免冲突。例如，将窗格模式改为 `Alt + p` ：
		```
		keybinds {
		    normal {
		        bind "Alt p" { SwitchToMode "pane"; }
		    }
		}
		kdl12345
		```
- **问题** ：复制内容无法粘贴到外部应用。  
	**解决** ：
	1. 确保 `copy_command` 已正确配置（如上文所述）。
		2. 检查系统剪贴板工具是否正常工作。例如，测试 `xclip` ：
		```bash
		echo "test" | xclip -selection clipboard
		bash1
		```
		3. 禁用 `copy_on_select` 以手动控制复制行为：
		```nginx
		copy_on_select false
		kdl1
		```
- **问题** ：Zellij 启动缓慢或占用内存较多。  
	**解决** ：
	1. 减少历史缓冲区大小：
		```
		scroll_buffer_size 5000
		kdl1
		```
		2. 禁用不必要的插件或简化状态栏：
		```
		default_layout "compact"
		kdl1
		```
		3. 检查是否有过多后台会话运行，使用 `zellij kill-session <name>` 清理。
- **问题** ：无法恢复分离的会话。  
	**解决** ：
	1. 列出所有会话：
		```bash
		zellij ls
		bash1
		```
		2. 重新连接：
		```bash
		zellij attach <session_name>
		bash1
		```
		3. 如果会话丢失，检查是否因系统重启或 Zellij 进程被终止。启用定期备份（如上文所述）可降低丢失风险。
- **问题** ：鼠标操作不生效。  
	**解决** ：
	1. 确保 `mouse_mode` 启用：
		```nginx
		mouse_mode true
		kdl1
		```
		2. 检查终端模拟器是否拦截了鼠标事件。例如，在 Alacritty 中确保未禁用鼠标支持。
- **问题** ：特定命令在 Zellij 窗格中运行失败。  
	**解决** ：
	1. 某些交互式命令（如 `htop` ）可能需要终端伪终端支持。尝试在布局文件中指定 `command` ：
		```yaml
		panes:
		  - command: "htop"
		yaml12
		```
		2. 检查环境变量是否正确传递。例如，添加 `TERM=xterm-256color` ：
		```bash
		export TERM=xterm-256color
		bash1
		```

---

### 六、Zellij 与其他工具的比较

| 特性 | Zellij | tmux | screen |
| --- | --- | --- | --- |
| 用户界面 | 友好，带状态栏和提示 | 需手动配置 | 简陋 |
| 插件系统 | WebAssembly，支持多语言 | 有限 | 无 |
| 布局系统 | YAML，智能优化 | 脚本化 | 无 |
| 学习曲线 | 低 | 中 | 高 |
| 跨平台 | Linux/macOS | 广泛 | 广泛 |
| 性能 | 高（Rust 开发） | 高 | 中 |

**选择建议** ：

- 如果你是新手或追求现代化体验，Zellij 是最佳选择。
- 如果需要广泛的社区支持和成熟生态，tmux 更适合。
- 如果在资源受限的环境中，screen 是轻量级选择。

---

### 七、总结

Zellij 凭借其现代化设计、强大的功能和友好的用户体验，正在成为终端复用领域的佼佼者。通过本教程，你已经掌握了 Zellij 的安装、基本操作、高级配置以及实用技巧。无论是开发者、运维人员还是命令行爱好者，Zellij 都能显著提升你的终端工作效率。

**进一步探索** ：

- 访问 Zellij 官网（ [https://zellij.dev）获取最新文档和更新。](https://zellij.xn--dev\)-3c1gt1bn70fmjac353axd48pny1j./)
- 查看官方视频教程（ [https://zellij.dev/screencasts/）以直观了解操作。](https://zellij.dev/screencasts/%EF%BC%89%E4%BB%A5%E7%9B%B4%E8%A7%82%E4%BA%86%E8%A7%A3%E6%93%8D%E4%BD%9C%E3%80%82)
- 加入 Zellij GitHub 社区（ [https://github.com/zellij-org/zellij）参与开发或反馈问题。](https://github.com/zellij-org/zellij%EF%BC%89%E5%8F%82%E4%B8%8E%E5%BC%80%E5%8F%91%E6%88%96%E5%8F%8D%E9%A6%88%E9%97%AE%E9%A2%98%E3%80%82)
- 尝试创建自定义插件或布局，打造专属的终端工作空间。

希望本教程能成为你在 Zellij 学习路上的坚实起点！如果有任何疑问，欢迎在评论区交流。