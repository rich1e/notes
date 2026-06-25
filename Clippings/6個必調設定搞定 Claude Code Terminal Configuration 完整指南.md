---
title: "6個必調設定搞定 Claude Code Terminal Configuration 完整指南"
source: "https://moksaweb.com/claude-code-terminal-configuration/"
author:
  - "[[Moksa]]"
published: 2026-04-03
created: 2026-06-25
description: "Claude Code Terminal Configuration 終端機設定完整指南，詳解 settings.json 4 層作用域、6 個關鍵設定項目（Theme、Nerd Font、環境變數、Proxy）、Permission Mode 權限規則與企業 Managed Settings 管理方案。"
tags:
  - "clippings"
---
## 1\. Claude Code Terminal Configuration 完整指南

> **Moksa 觀點** ：很多人裝完 Claude Code 就直接開始用，其實少了一個關鍵步驟——終端機環境設定。沒設好的 Claude Code Terminal Configuration 意味著你每次都要手動指定模型、重複確認權限、甚至在 Windows 上遇到 shell 路徑錯誤。花 15 分鐘把 Claude Code Terminal Configuration 調好，往後每天都能省下大量時間。這篇文章從支援的終端機、Nerd Font 安裝、shell 整合，到環境變數、Proxy、SSH Remote 以及 tmux/screen 整合，完整涵蓋所有你需要知道的設定細節。

這篇 **Claude Code Terminal Configuration** 完整指南涵蓋從終端機選擇到 shell 整合、環境變數到遠端連線的所有設定細節。不管你是用 macOS、Linux 還是 Windows，正確的 Claude Code Terminal Configuration 是讓 AI 輔助開發流程順暢運作的基礎。本文是 [Moksa Claude Code 完整教學系列](https://moksaweb.com/category/claude-code/) 的一部分。

## 2\. Claude Code Terminal Configuration 有哪些核心功能？：Claude Code Terminal Configuration 涵蓋哪些範圍

Claude Code Terminal Configuration 不只是單一設定檔，而是一套多層次的設定系統，涵蓋從 terminal emulator 選擇到 remote SSH session 管理的完整工作流程。它的核心面向包括：

- **Terminal Emulator 相容性** ：iTerm2、Warp、Windows Terminal、VS Code Terminal、GNOME Terminal、Alacritty 各自的設定方式與已知限制
- **Font Rendering** ：Nerd Font 安裝流程，確保 Claude Code UI 的 icon glyphs、powerline symbols 正確顯示
- **Color Theme** ：dark mode 與 light mode 主題選擇，支援 true color（24-bit）的 ANSI escape code 顯示
- **Shell Integration** ：zsh、bash、fish 三種 shell 的 autocomplete、tab completion 與 command history 整合
- **Environment Variables** ：ANTHROPIC\_API\_KEY、ANTHROPIC\_MODEL、DISABLE\_AUTOUPDATER 等關鍵環境變數的設定位置與優先順序
- **Network Configuration** ：HTTP Proxy、HTTPS Proxy、SSL certificate、NO\_PROXY bypass 設定
- **Remote Development** ：SSH Remote 連線時的 PTY allocation、key forwarding、environment variable propagation
- **Session Persistence** ：tmux 與 screen terminal multiplexer 整合，讓 Claude Code session 在 SSH disconnect 後持續運作

每一個面向都可以透過 settings.json 設定檔或環境變數來調整。理解 Claude Code Terminal Configuration 的完整範圍，才能針對自己的工作環境做最適合的客製化調整，從個人開發者到企業團隊都適用。

Claude Code Terminal Configuration 的設定架構採用 layered precedence model，從最高優先級到最低依序是：command-line flags → environment variables → local project settings → project settings → user settings → managed enterprise settings。這個架構讓你可以在不同 scope 設定不同的 default behavior，而不需要每次啟動時重複指定相同的 options。每一層設定都是獨立的 JSON configuration file，支援 object merging（permission arrays 會合併而非覆蓋）以及 environment variable interpolation。

當你進行 Claude Code Terminal Configuration 時，建議先從 user-level settings（~/.claude/settings.json）開始，設定好個人偏好的 model、permission rules 和 environment variables。再根據每個 project 的需求，在.claude/settings.json 加入 project-specific configuration，例如限制允許執行的 bash commands 或指定 project-level memory。這樣的分層設定方式既靈活又安全，是最佳實踐。

## 3\. 支援的 Terminal：iTerm2、Warp、Windows Terminal、VS Code Terminal 完整設定

進行 Claude Code Terminal Configuration 的第一步是選擇合適的 terminal emulator。不同 terminal 的功能支援和設定方式有明顯差異，這裡逐一說明每款 terminal 的設定重點與最佳實踐：

**iTerm2（macOS 首選 Terminal）**

iTerm2 是 macOS 上進行 Claude Code Terminal Configuration 支援最完整的 terminal。它原生支援 256 color、24-bit true color、Unicode、以及所有 Nerd Font glyphs。iTerm2 的 Shell Integration 功能讓每個指令執行後都能顯示 exit code、執行時間（duration）和 working directory，對 debugging Claude Code 行為非常有用。

在 Claude Code Terminal Configuration 中，iTerm2 對 Claude Code 的 ANSI escape sequences、OSC（Operating System Command）sequences 和 DEC private mode sequences 都有完整支援，這確保了 Claude Code 的 TUI（Terminal User Interface）元件——包括 progress bars、colored diff output、interactive selection menus——都能正確渲染。

iTerm2 獨有的功能對 Claude Code 特別有用：

- **Semantic History** ：Cmd+click 直接開啟 Claude Code 輸出的檔案路徑
- **Triggers** ：自動觸發動作，例如 Claude Code 完成某個任務時發出系統通知
- **Python API** ：可以用 Python script 控制 iTerm2 視窗，搭配 Claude Code 做自動化工作流程
- **Split Panes** ：把 terminal 分割成多個 pane，同時顯示 Claude Code session 和 file editor

設定 iTerm2 給 Claude Code 使用的關鍵步驟：進入 Preferences → Profiles → Text，勾選 “Use a different font for non-ASCII text”，再選擇一款 Nerd Font（建議用 MesloLGS NF 或 Hack Nerd Font Mono）。Color Preset 推薦 Solarized Dark 或 One Dark，對長時間工作的眼睛比較友善。

**Warp（現代化 Rust-based Terminal）**

Warp 是一款用 Rust 語言開發的現代化 terminal，本身整合了 AI command suggestions，跟 Claude Code Terminal Configuration 搭配使用有額外的協同效果。Warp 的 block-based 輸入架構讓每次指令的 stdout/stderr 輸出都被包在獨立的 block 裡，讓你可以輕鬆複製 Claude Code 的輸出結果。

Warp 的主要優勢包括：

- **Command Palette** ：Cmd+P 快速搜尋並執行 shell commands，不需要記全名
- **AI Command Search** ：用自然語言描述要做的事，Warp 會建議對應的 shell command
- **Workflows** ：把常用的 Claude Code 指令序列儲存為 workflow，一鍵執行
- **Team Sharing** ：可以把 configuration 和 workflows 分享給團隊其他成員

注意：Warp 目前對某些自訂 shell prompt（如複雜的 Powerlevel10k 設定）的支援還不完整。如果你的 zsh prompt 使用了大量 custom segments（git status、kubectl context、node version、python venv 等），可能需要在使用 Claude Code 時切換到簡化版的 prompt theme。Warp 有自己的 prompt rendering engine，會跟某些第三方 prompt frameworks 產生衝突。

**Claude Code Terminal Configuration：Windows Terminal（Windows 平台最佳選擇）**

Windows Terminal 是 Windows 上進行 Claude Code Terminal Configuration 的首選。它支援多 tab、split pane、自訂 color scheme，以及透過 WSL2（Windows Subsystem for Linux）執行完整的 Linux shell 環境。在 Windows 上用 Claude Code，強烈建議安裝 WSL2，讓你可以在 Windows Terminal 裡用 bash 或 zsh，避免 Windows 原生 cmd.exe/PowerShell 的相容性問題。

Windows Terminal 的設定檔位於 `%LOCALAPPDATA%\Packages\Microsoft.WindowsTerminal_8wekyb3d8bbwe\LocalState\settings.json` ，可以在這裡設定：

```
// Windows Terminal settings.json 關鍵設定
{
  "defaultProfile": "{your-wsl-profile-guid}",
  "profiles": {
    "defaults": {
      "font": {
        "face": "MesloLGS NF",
        "size": 13
      },
      "colorScheme": "One Half Dark",
      "padding": "8, 8, 8, 8",
      "scrollbarState": "visible"
    },
    "list": [
      {
        "name": "Ubuntu (WSL2) - Claude Dev",
        "source": "Windows.Terminal.Wsl",
        "startingDirectory": "//wsl$/Ubuntu/home/username/projects"
      }
    ]
  },
  "keybindings": [
    {
      "command": "splitPane",
      "keys": "alt+shift+d"
    }
  ]
}
```

**Claude Code Terminal Configuration：VS Code Terminal（整合開發環境內建）**

VS Code Terminal 內建在 VS Code 裡，對開發者最方便，因為可以同時看到 code editor 和 Claude Code 的輸出。進行 Claude Code Terminal Configuration 時，VS Code Terminal 有一個重要設定：你需要在 VS Code 的 settings.json 裡設定 “terminal.integrated.fontFamily” 為一款 Nerd Font，否則 Claude Code 的 UI icon glyphs 會顯示為亂碼方塊（tofu characters）。

```
// VS Code settings.json — Claude Code 相關 terminal 設定
{
  "terminal.integrated.fontFamily": "MesloLGS NF",
  "terminal.integrated.fontSize": 14,
  "terminal.integrated.lineHeight": 1.2,
  "terminal.integrated.cursorStyle": "line",
  "terminal.integrated.scrollback": 10000,
  "terminal.integrated.enableBell": false,
  "terminal.integrated.inheritEnv": true,
  // 確保環境變數從 shell profile 繼承
  "terminal.integrated.env.osx": {
    "ANTHROPIC_API_KEY": "${env:ANTHROPIC_API_KEY}"
  },
  "terminal.integrated.env.linux": {
    "ANTHROPIC_API_KEY": "${env:ANTHROPIC_API_KEY}"
  }
}
```

VS Code Terminal 還支援 “terminal profiles” 功能，可以為 Claude Code 建立一個專用的 launch profile，自動套用特定的 environment variables、working directory 和 shell executable。這個功能類似於 VS Code 的”launch configurations”，讓不同的 development context 可以有不同的 terminal setup。你也可以在 VS Code Keyboard Shortcuts 裡把 “Create New Terminal (With Profile)” 綁到快捷鍵，一鍵開啟 Claude Code 專用 terminal：

```
// VS Code settings.json — Claude Code 專用 terminal profile
{
  "terminal.integrated.profiles.osx": {
    "Claude Code": {
      "path": "/bin/zsh",
      "env": {
        "ANTHROPIC_MODEL": "claude-sonnet-4-6",
        "DISABLE_AUTOUPDATER": "1"
      },
      "icon": "robot"
    }
  },
  "terminal.integrated.defaultProfile.osx": "Claude Code"
}
```

## 4\. Nerd Font 安裝與 Color Theme 設定

Claude Code Terminal Configuration 中，Nerd Font 是一組把 Powerline symbols、Font Awesome icons、Devicons、Weather icons 等超過 3000 個 glyphs 整合進去的程式設計字體。Claude Code 的互動介面使用這些特殊字元來顯示 file type icons、Git branch status、directory separators 等 UI 元素。沒有安裝正確的 Nerd Font，這些 glyphs 會顯示為 replacement character（問號或方塊）。

**macOS 安裝 Nerd Font（使用 Homebrew Cask）**

```
# 加入 Homebrew Cask Fonts tap（一次性設定）
brew tap homebrew/cask-fonts

# 安裝 MesloLGS NF（Powerlevel10k 預設字體，最推薦）
brew install --cask font-meslo-lg-nerd-font

# 安裝 Hack Nerd Font（閱讀性優秀，適合長時間 coding）
brew install --cask font-hack-nerd-font

# 安裝 JetBrains Mono Nerd Font（JetBrains IDE 用戶推薦）
brew install --cask font-jetbrains-mono-nerd-font

# 安裝 Fira Code Nerd Font（支援 ligatures，視覺效果更好）
brew install --cask font-fira-code-nerd-font

# 確認字體安裝成功
fc-list | grep -i "MesloLGS"
```

**Linux 安裝 Nerd Font（手動下載）**

```
# 建立使用者字體目錄（如果不存在）
mkdir -p ~/.local/share/fonts/NerdFonts

# 下載 MesloLGS NF（Powerlevel10k 推薦版本）
cd ~/.local/share/fonts/NerdFonts
for style in Regular Bold Italic "Bold Italic"; do
  wget "https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20${style// /%20}.ttf"
done

# 更新系統字體快取
fc-cache --force --verbose

# 確認字體已載入
fc-list | grep "MesloLGS"

# 或者使用 Nerd Fonts 官方安裝腳本（需要 git）
git clone --depth 1 https://github.com/ryanoasis/nerd-fonts.git /tmp/nerd-fonts
/tmp/nerd-fonts/install.sh Hack JetBrainsMono FiraCode
```

**Windows 安裝 Nerd Font（winget 或手動）**

```
# 使用 winget（Windows Package Manager）安裝
winget install --id DEVCOM.JetBrainsMonoNerdFont

# 或者用 scoop 安裝
scoop bucket add nerd-fonts
scoop install Hack-NF

# 手動安裝步驟：
# 1. 去 https://www.nerdfonts.com/font-downloads 下載 zip
# 2. 解壓縮，選取所有 .ttf 檔案
# 3. 右鍵 → 「為所有使用者安裝」（需要管理員權限）
# 4. 在 Windows Terminal settings.json 設定 "face": "MesloLGS NF"

# 驗證字體可用（PowerShell）
[System.Drawing.Text.InstalledFontCollection]::new().Families | Where-Object { $_.Name -like "*Nerd*" }
```

**Claude Code Terminal Configuration 推薦 Color Theme 對照表**

| Theme 名稱 | Color Mode | 適合場景 | 安裝方式 |
| --- | --- | --- | --- |
| One Dark Pro | Dark | 長時間工作，對比度適中不傷眼 | Terminal 內建或主題包 |
| Dracula Official | Dark | 喜歡高飽和度紫色系 | dracula.github.io |
| Solarized Dark | Dark | 根據人眼 CIELAB 色彩空間設計 | ethanschoonover.com |
| Catppuccin Mocha | Dark | 近年最受歡迎，柔和暖色系 | github.com/catppuccin |
| Tokyo Night Storm | Dark | 深夜工作，極低亮度不刺眼 | VS Code Marketplace |
| Gruvbox Dark | Dark | retro amber 風格，親切感強 | github.com/morhetz/gruvbox |

## 如何設定 Claude Code Terminal Configuration？

### 選擇推薦終端機

macOS 用 iTerm2 或 Ghostty，Windows 用 Windows Terminal，Linux 用 Kitty 或 WezTerm。

### 設定 Option 為 Meta 鍵

iTerm2 在 Settings > Profiles > Keys 設定 Left Option 為 Esc+，VS Code 設定 macOptionIsMeta: true。

### 安裝 Nerd Font

安裝 Meslo Nerd Font 或類似字體，讓終端機正確顯示 Claude Code 的圖示和符號。

### 執行 /terminal-setup

在 Claude Code 中執行 /terminal-setup 自動安裝 Shift+Enter 多行輸入的按鍵綁定。

## 5\. Shell 整合：zsh、bash、fish Autocomplete 完整設定

Shell 整合是 Claude Code Terminal Configuration 裡最能提升日常效率的部分。正確設定之後，在 terminal 裡輸入 `claude` 再按 Tab，就能看到所有 subcommands、flags 和 arguments 的補全列表。這個功能在你忘記某個 flag 名稱時特別省事。

**zsh Autocomplete 完整設定**

```
# === ~/.zshrc 設定 ===

# 方法一：動態載入補全（每次啟動時生成，適合 Claude Code 頻繁更新的情況）
if command -v claude &> /dev/null; then
  eval "$(claude completion zsh)"
fi

# 方法二：靜態補全檔案（載入速度更快，適合穩定版本）
# 只需執行一次，之後 zsh 會自動載入
claude completion zsh > "${fpath[1]}/_claude" 2>/dev/null

# 如果使用 Oh My Zsh，確認以下設定
plugins=(
  git
  zsh-completions       # 額外補全定義
  zsh-autosuggestions   # 根據 history 自動建議
  zsh-syntax-highlighting
)

# 強制重新載入補全系統
autoload -U compinit
compinit -d ~/.zcompdump

# 補全樣式設定（讓補全選單更好看）
zstyle ':completion:*' menu select
zstyle ':completion:*' list-colors "${(s.:.)LS_COLORS}"
zstyle ':completion:*:descriptions' format '%F{yellow}-- %d --%f'
```

**bash Autocomplete 完整設定**

```
# === ~/.bashrc 或 ~/.bash_profile 設定 ===

# 確認 bash-completion 已安裝（macOS 用 Homebrew）
# brew install bash-completion@2
# 在 ~/.bash_profile 加入（brew 會提示這個步驟）：
[[ -r "/usr/local/etc/profile.d/bash_completion.sh" ]] && \
  . "/usr/local/etc/profile.d/bash_completion.sh"

# Claude Code bash 補全
if command -v claude &> /dev/null; then
  eval "$(claude completion bash)"
fi

# 或者靜態安裝到系統補全目錄
# claude completion bash > /usr/local/etc/bash_completion.d/claude

# Linux（系統套件管理安裝 bash-completion）
# sudo apt install bash-completion   # Debian/Ubuntu
# sudo dnf install bash-completion   # Fedora/RHEL
# sudo pacman -S bash-completion     # Arch Linux

# 讓補全在大小寫不區分
bind "set completion-ignore-case on"

# 顯示補全時列出所有選項而不是響鈴
bind "set show-all-if-ambiguous on"
```

**fish Shell Autocomplete 設定**

```
# === ~/.config/fish/config.fish 設定 ===

# Claude Code fish 補全（動態載入）
if command -v claude > /dev/null
    claude completion fish | source
end

# 或者靜態補全檔案（推薦，載入更快）
# 只需執行一次：
# claude completion fish > ~/.config/fish/completions/claude.fish

# fish 的 universal variables（跨 session 持久）
set -Ux ANTHROPIC_MODEL claude-sonnet-4-6
set -Ux DISABLE_AUTOUPDATER 1

# fish 的 abbreviations（比 alias 更強大，會展開顯示）
abbr --add cc "claude"
abbr --add ccc "claude --continue"
abbr --add ccr "claude --resume"

# 設定 fish greeting（可選，關掉預設的 greeting 讓 Claude Code 更乾淨）
set fish_greeting ""
```

**PowerShell Autocomplete（Windows 原生環境）**

```
# === $PROFILE 設定（通常是 ~\Documents\PowerShell\Microsoft.PowerShell_profile.ps1）===

# Claude Code PowerShell 補全
if (Get-Command claude -ErrorAction SilentlyContinue) {
    Invoke-Expression (& claude completion powershell | Out-String)
}

# 設定 PSReadLine 讓補全體驗更好
Set-PSReadLineOption -PredictionSource History
Set-PSReadLineOption -PredictionViewStyle ListView
Set-PSReadLineKeyHandler -Key Tab -Function MenuComplete

# 環境變數設定
$env:DISABLE_AUTOUPDATER = "1"
$env:ANTHROPIC_MODEL = "claude-sonnet-4-6"
```

設定好任意一種 shell 的 autocomplete 後，輸入 `claude` 再按 Tab，就能看到所有可用的 subcommands 清單（chat、run、config、doctor 等）。輸入 `claude --` 再按 Tab 可以列出所有 global flags（如 –model、–no-stream、–output-format 等）。這個功能依賴 shell 的 completion framework：zsh 用 compdef system、bash 用 complete builtin、fish 用 complete 指令。整合完成後，日常使用 Claude Code 的 command-line interface 效率大幅提升。

## 6\. 環境變數、Proxy 設定與 SSH Remote 連線

環境變數是 Claude Code Terminal Configuration 的核心之一。了解每個環境變數的作用和設定位置，能讓你在不同工作環境（本機開發、CI/CD、遠端伺服器）間靈活切換，同時保持安全性。

**6-1 核心 API 環境變數**

| Environment Variable | 說明 | 範例值 | 必填 |
| --- | --- | --- | --- |
| ANTHROPIC\_API\_KEY | Anthropic API 認證金鑰 | sk-ant-api03-xxx… | 是 |
| ANTHROPIC\_MODEL | 覆蓋 settings.json 的 model 設定 | claude-sonnet-4-6 | 否 |
| ANTHROPIC\_BASE\_URL | 覆蓋 API endpoint（用於 Proxy） | https://proxy.example.com | 否 |
| ANTHROPIC\_AUTH\_TOKEN | 替代 API key 的 Bearer token | Bearer eyJ… | 否 |
| CLAUDE\_CODE\_API\_KEY\_HELPER | 動態取得 API key 的 shell 腳本路徑 | /opt/scripts/get-key.sh | 否 |
| ANTHROPIC\_SMALL\_FAST\_MODEL | 指定用於輕量任務的快速模型 | claude-haiku-4 | 否 |

**6-2 行為控制環境變數**

| Environment Variable | 說明 | 推薦值 |
| --- | --- | --- |
| DISABLE\_AUTOUPDATER | 停用 Claude Code 自動更新檢查 | 1（企業環境建議開） |
| CLAUDE\_CODE\_DISABLE\_TELEMETRY | 停用使用統計資料回傳 | 1（隱私敏感環境） |
| USE\_BUILTIN\_RIPGREP | 使用 Claude Code 內建 ripgrep 而非系統版本 | 1（避免版本衝突） |
| CLAUDE\_CODE\_GIT\_BASH\_PATH | Windows Git Bash 可執行檔路徑 | C:\\Program Files\\Git\\bin\\bash.exe |
| CLAUDE\_CODE\_MAX\_OUTPUT\_TOKENS | 每次 API response 的最大 token 數量 | 8192 |
| CLAUDE\_CODE\_TIMEOUT | API request timeout（秒） | 180 |
| CLAUDE\_CODE\_LOG\_LEVEL | logging verbosity（debug/info/warn/error） | info |

**6-3 在 settings.json 的 env 區塊設定環境變數**

比較推薦的方式是把 Claude Code 專用環境變數放在 settings.json 的 “env” 欄位，而不是 shell profile。這樣只影響 Claude Code process，不會污染系統環境，也方便 version control（排除 API key）：

```
// ~/.claude/settings.json — 使用者層設定
{
  "model": "claude-sonnet-4-6",
  "autoUpdatesChannel": "stable",
  "autoMemoryEnabled": true,
  "env": {
    "DISABLE_AUTOUPDATER": "1",
    "USE_BUILTIN_RIPGREP": "1",
    "CLAUDE_CODE_TIMEOUT": "180",
    "CLAUDE_CODE_LOG_LEVEL": "info",
    // Windows 專用：指向 Git Bash 路徑
    "CLAUDE_CODE_GIT_BASH_PATH": "C:\\Program Files\\Git\\bin\\bash.exe"
  },
  "permissions": {
    "allow": [
      "Bash(git *)",
      "Bash(npm *)",
      "Bash(pnpm *)",
      "Read",
      "Write"
    ],
    "deny": [
      "Bash(rm -rf *)",
      "Bash(git push --force *)"
    ]
  }
}
```

注意：永遠不要把 ANTHROPIC\_API\_KEY 放進 settings.json 的 env 區塊，因為 settings.json 可能會被 commit 到 git repository。API key 應該放在 shell profile（~/.zshrc 或 ~/.bashrc）、系統 keychain（macOS Keychain、Windows Credential Manager）、或使用 apiKeyHelper 腳本從 HashiCorp Vault、AWS Secrets Manager、Azure Key Vault 等 secret manager 動態取得，確保 zero secrets in source control 的安全準則。

**6-4 Proxy 設定**

在企業網路或需要透過 forward proxy 連線到 Anthropic API 的環境，Claude Code Terminal Configuration 需要加入 proxy 相關設定。Claude Code 是 Node.js 應用程式，遵循標準的 HTTP\_PROXY 和 HTTPS\_PROXY 環境變數慣例：

```
# shell profile 設定（影響所有工具）
export HTTP_PROXY="http://proxy.company.com:8080"
export HTTPS_PROXY="http://proxy.company.com:8080"
# 或者小寫版本（部分工具只讀小寫）
export http_proxy="http://proxy.company.com:8080"
export https_proxy="http://proxy.company.com:8080"

# NO_PROXY：不走 proxy 的域名清單
export NO_PROXY="localhost,127.0.0.1,*.internal.company.com,10.0.0.0/8"

# 需要認證的 Proxy
export HTTPS_PROXY="http://username:password@proxy.company.com:8080"

# SOCKS5 Proxy（部分網路環境使用）
export ALL_PROXY="socks5://proxy.company.com:1080"
```

如果企業 proxy 進行 SSL inspection（TLS intercept），Anthropic API 的 HTTPS 連線會因為 certificate mismatch 而失敗。需要把公司的 root CA certificate 加入信任鏈：

```
# Node.js extra CA certificates（Claude Code 使用 Node.js runtime）
export NODE_EXTRA_CA_CERTS="/etc/ssl/certs/company-ca-bundle.pem"

# 或在 settings.json 的 env 區塊設定
{
  "env": {
    "NODE_EXTRA_CA_CERTS": "/etc/ssl/certs/company-ca-bundle.pem",
    "HTTPS_PROXY": "http://proxy.company.com:8080",
    "NO_PROXY": "localhost,127.0.0.1"
  }
}

# 測試 proxy 連線是否正常（替換為你的 proxy 位址）
curl -x http://proxy.company.com:8080 \
     --cacert /etc/ssl/certs/company-ca-bundle.pem \
     https://api.anthropic.com/v1/models
```

**6-5 SSH Remote 連線設定**

透過 SSH 連線到遠端伺服器使用 Claude Code 時，有幾個重要的設定需要注意：API key 的傳遞方式、PTY allocation、以及 terminal 環境的正確繼承。

```
# 方法一：使用 SSH config 的 SendEnv（安全、優雅）
# ~/.ssh/config
Host remote-dev-server
    HostName 192.168.1.100
    User developer
    IdentityFile ~/.ssh/id_ed25519
    SendEnv ANTHROPIC_API_KEY ANTHROPIC_MODEL DISABLE_AUTOUPDATER
    # 確認目標伺服器 /etc/ssh/sshd_config 包含：
    # AcceptEnv ANTHROPIC_API_KEY ANTHROPIC_MODEL DISABLE_AUTOUPDATER

# 方法二：SSH 連線時直接在 remote command 裡設定
ssh -t user@remote-server \
    "ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY claude"

# 方法三：使用 SSH -o SendEnv（不修改 ssh config）
ssh -t -o "SendEnv ANTHROPIC_API_KEY" user@remote-server

# 注意：-t flag 強制分配 pseudo-terminal（PTY）
# 沒有 PTY，Claude Code 的 interactive UI 無法正常顯示
# 錯誤症狀：輸出沒有顏色、滾動條失效、Ctrl+C 無法中斷
```

在 remote server 上安裝 Claude Code（如果還沒安裝）：

```
# 在遠端伺服器上安裝 Claude Code（需要 Node.js 18+）
# 確認 Node.js 版本
node --version

# 安裝 Claude Code（需要全局安裝）
npm install -g @anthropic-ai/claude-code

# 確認安裝成功
claude --version

# 設定遠端伺服器的環境變數（~/.bashrc 或 ~/.zshrc）
echo 'export ANTHROPIC_API_KEY="sk-ant-..."' >> ~/.bashrc
echo 'export DISABLE_AUTOUPDATER="1"' >> ~/.bashrc
source ~/.bashrc
```

## 7\. tmux 與 screen 整合：讓 Claude Code Session 持久運作

tmux 和 screen 是 Unix 系統上的 terminal multiplexer，讓你可以把 Claude Code session 在 background 持續執行，不因 SSH disconnect 或 terminal 關閉而中斷。對於長時間的 refactoring、大型 codebase 分析或批次任務，這個功能至關重要。

**tmux 基本整合流程**

```
# 建立命名的 tmux session 專門用於 Claude Code
tmux new-session -s claude-dev -n main

# 在 tmux session 裡啟動 Claude Code（-t 不需要，tmux 自動提供 PTY）
claude

# Detach（離開 tmux 但讓 Claude Code 繼續在背景執行）
# 按 Ctrl+b，然後按 d

# 重新連接到 Claude Code session
tmux attach-session -t claude-dev

# 或者縮寫版
tmux a -t claude-dev

# 查看所有 tmux session
tmux list-sessions

# 在新 window 裡開啟 Claude Code（保持多個 project 並行）
tmux new-window -t claude-dev -n "project-b"
claude

# 在現有 session 裡切換 windows
# Ctrl+b + 0-9（按 window 編號）
# Ctrl+b + n（next window）
# Ctrl+b + p（previous window）
```

**tmux 設定優化（~/.tmux.conf）**

```
# ~/.tmux.conf — Claude Code 最佳化設定

# 設定超大 scrollback buffer（Claude Code 輸出可能很長）
set -g history-limit 100000

# 啟用 256 色和 24-bit true color 支援
set -g default-terminal "tmux-256color"
set -ga terminal-overrides ",xterm-256color:Tc"
set -ga terminal-overrides ",alacritty:Tc"

# 啟用滑鼠支援（方便捲動查看 Claude Code 的長輸出）
set -g mouse on

# 設定 prefix 為 Ctrl+a（比預設的 Ctrl+b 更順手，vim 使用者習慣）
unbind C-b
set-option -g prefix C-a
bind-key C-a send-prefix

# 讓 tmux 使用系統剪貼簿（macOS）
# 需要先 brew install reattach-to-user-namespace
set -g default-command "reattach-to-user-namespace -l $SHELL"
bind-key -T copy-mode-vi y send-keys -X copy-pipe-and-cancel "pbcopy"

# Linux 系統剪貼簿（xclip）
# bind-key -T copy-mode-vi y send-keys -X copy-pipe-and-cancel "xclip -in -selection clipboard"

# 設定 base index 從 1 開始（更直覺的鍵盤操作）
set -g base-index 1
setw -g pane-base-index 1

# 自動重新編號 windows（關掉 window 後）
set -g renumber-windows on

# 縮短 escape time（讓 vim/neovim 在 tmux 裡更流暢）
set -sg escape-time 10

# 顯示 session name 在 status bar
set -g status-left "[#S] "
set -g status-left-length 20
```

**screen 整合（輕量替代方案）**

```
# 建立命名的 screen session
screen -S claude-session

# 在 screen 裡啟動 Claude Code
claude

# Detach（Ctrl+a，然後按 d）

# 重新連接到 session
screen -r claude-session

# 列出所有 screen session（顯示 attached/detached 狀態）
screen -ls

# 強制 detach 並重新連接（當 session 顯示 attached 但實際上已失效）
screen -D -r claude-session

# ~/.screenrc 基本設定
cat >> ~/.screenrc << 'EOF'
# 啟用 256 色
term xterm-256color

# 增大 scrollback buffer
defscrollback 50000

# 顯示 hardstatus（類似 tmux status bar）
hardstatus alwayslastline
hardstatus string '%{= kG}[%{G}%H%{g}][%= %{=kw}%?%-Lw%?%{r}(%{W}%n*%f%t%?(%u)%?%{r})%{w}%?%+Lw%?%?%= %{g}][%{B}%Y-%m-%d %{W}%c%{g}]'

# 不顯示 startup message
startup_message off
EOF
```

使用 tmux 或 screen 時，一個常見問題是 TERM 環境變數設定不正確導致顏色顯示異常或完全沒有顏色。確認方式：

```
# 確認目前 TERM 值
echo $TERM

# 期望值：tmux-256color 或 xterm-256color
# 如果是 screen-256color 或 xterm，顏色可能顯示異常

# 快速測試 true color 支援
awk 'BEGIN{
    s="/\\/\\/\\/\\/\\"; s=s s s s s s s s;
    for (colnum = 0; colnum<77; colnum++) {
        r = 255-(colnum*255/76);
        g = (colnum*510/76);
        b = (colnum*255/76);
        if (g>255) g = 510-g;
        printf "\033[48;2;%d;%d;%dm", r,g,b;
        printf "\033[38;2;%d;%d;%dm", 255-r,255-g,255-b;
        printf "%s\033[0m", substr(s,colnum+1,1);
    }
    printf "\n";
}'
# 看到漂亮的漸層彩虹 = true color 支援正常
# 如果只看到單色或幾種顏色 = TERM 設定有問題，重新檢查 tmux.conf
```

另外，在 tmux 環境使用 Claude Code 時，有個實用技巧是搭配 tmux-resurrect 和 tmux-continuum plugin，讓 tmux sessions（包括正在執行的 Claude Code instance）可以在系統重啟後自動恢復。這對於需要長時間執行的 background tasks（如 large codebase indexing、batch file processing）特別有用，避免因為意外重啟而丟失工作進度。

以上就是完整的 Claude Code Terminal Configuration 實戰指南。從 terminal emulator 選擇、Nerd Font 安裝、shell autocomplete 設定，到環境變數管理、enterprise proxy 設定、SSH remote 連線，再到 tmux session 持久化，每個面向都正確設定之後，你的 **Claude Code Terminal Configuration** 就能在任何工作環境下穩定高效地運作。

以下是一份完整的 Claude Code Terminal Configuration quick reference，把最常用的設定整合在一起，方便直接複製使用：

```
// ~/.claude/settings.json — Claude Code Terminal Configuration 完整範本
// 適用於個人開發者，根據需求調整後使用
{
  // Model configuration
  "model": "claude-sonnet-4-6",
  "autoUpdatesChannel": "stable",
  "autoMemoryEnabled": true,
  "defaultMode": "plan",

  // Environment variables for terminal behavior
  "env": {
    "DISABLE_AUTOUPDATER": "1",
    "USE_BUILTIN_RIPGREP": "1",
    "CLAUDE_CODE_TIMEOUT": "180",
    "CLAUDE_CODE_LOG_LEVEL": "info",
    // Windows only: set path to Git Bash executable
    // "CLAUDE_CODE_GIT_BASH_PATH": "C:\\Program Files\\Git\\bin\\bash.exe"
    // Proxy settings (uncomment if needed):
    // "HTTPS_PROXY": "http://proxy.company.com:8080",
    // "NODE_EXTRA_CA_CERTS": "/path/to/ca-cert.pem"
  },

  // Permission rules — allow safe commands, deny destructive ones
  "permissions": {
    "allow": [
      "Bash(git log *)",
      "Bash(git diff *)",
      "Bash(git status)",
      "Bash(git branch *)",
      "Bash(npm test)",
      "Bash(npm run lint)",
      "Bash(pnpm test)",
      "Bash(pnpm build)",
      "Read",
      "Write"
    ],
    "deny": [
      "Bash(rm -rf *)",
      "Bash(git push --force *)",
      "Bash(git reset --hard *)",
      "Bash(sudo rm *)",
      "Bash(chmod 777 *)"
    ]
  },

  // API key helper (optional, for enterprise key rotation)
  // "apiKeyHelper": "/opt/company/scripts/get-anthropic-key.sh"
}
```

正確完成 Claude Code Terminal Configuration 之後，建議用 `claude doctor` 指令做最後確認。這個 built-in diagnostic command 會檢查 Node.js runtime version（需要 v18+）、ANTHROPIC\_API\_KEY 有效性、shell executable path、settings.json JSON syntax validity，以及所有必要的 runtime dependencies（ripgrep、git 等），確保整個 terminal environment configuration 無誤。如果 doctor 回報任何 warning 或 error，可以對照 error message 找到對應的設定項目修正。

## 8\. 使用 Claude Code Terminal Configuration 要注意什麼？

- **ANTHROPIC\_API\_KEY 永遠不要 commit 進 git** ：把 API key 放進 settings.json 的 env 區塊就是在把 key 放進可能被 commit 的檔案。正確做法是把 key 放在 shell profile（~/.zshrc）、系統 keychain、或 secret manager，再透過環境繼承或 apiKeyHelper 腳本取得。
- **Windows 必須設定 CLAUDE\_CODE\_GIT\_BASH\_PATH** ：在 Windows 原生環境（非 WSL2），Claude Code 需要 Git Bash 執行 shell commands。預設路徑是 C:\\Program Files\\Git\\bin\\bash.exe，如果你安裝在不同位置，必須在 settings.json 的 env 區塊明確指定，否則所有 Bash() 工具呼叫都會失敗。
- **SSH 連線務必加 -t 旗標** ：沒有 pseudo-terminal（PTY），Claude Code 的 interactive TUI 無法正常顯示。症狀包括：輸出沒有顏色、Tab 補全失效、Ctrl+C 無法中斷執行中的指令。使用 ssh -t 或在 SSH config 裡設定 RequestTTY yes 來確保 PTY 分配。
- **tmux 的 TERM 設定是必要步驟** ：tmux 在啟動時會覆蓋 TERM 環境變數。如果 ~/.tmux.conf 裡沒有正確設定 terminal-overrides，Claude Code 的顏色輸出會退回到 16 色或完全無色。在 tmux.conf 加入 set -ga terminal-overrides ",xterm-256color:Tc" 確保 true color 正常傳遞。
- **Nerd Font 需要在終端機層面設定** ：光是在系統層安裝了 Nerd Font 還不夠。你用的那款 terminal emulator（iTerm2、Windows Terminal、VS Code Terminal 等）必須明確設定使用剛安裝的 Nerd Font 字體名稱，圖示才能正確顯示。
- **企業 proxy 的 SSL intercept 要特別處理** ：很多企業防火牆會攔截並重新簽署所有 HTTPS 流量（TLS inspection / SSL deep packet inspection）。Claude Code 使用 Node.js runtime，需要設定 NODE\_EXTRA\_CA\_CERTS 環境變數指向公司的 root CA certificate bundle（PEM format），否則對 api.anthropic.com 的 API 呼叫會因 UNABLE\_TO\_VERIFY\_LEAF\_SIGNATURE 或 CERTIFICATE\_VERIFY\_FAILED 錯誤而失敗。可以用 openssl s\_client -connect api.anthropic.com:443 來診斷 certificate chain 問題。
- **shell 整合設定後要 source 或重開視窗** ：在.zshrc/.bashrc 加入 shell 整合設定後，必須執行 source ~/.zshrc（或開新的 terminal 視窗），設定才會在目前的 shell session 裡生效。不 source 的話，即使設定寫正確，Tab completion 也不會出現。注意：compinit 的 cached dump file（~/.zcompdump）有時需要刪除並重建（rm ~/.zcompdump && exec zsh）才能載入新的 completion definitions。

掌握了以上所有 Claude Code Terminal Configuration 的設定細節之後，你的開發環境就具備了 AI 輔助開發的完整基礎建設。無論是在 macOS 上用 iTerm2 搭配 Powerlevel10k prompt，在 Linux server 上用 tmux 保持 session 持久，還是在 Windows 上用 WSL2 + Windows Terminal 跑完整的 Linux 工具鏈，正確的 Claude Code Terminal Configuration 都能確保每次啟動都有一致的行為表現。

企業環境下的 Claude Code Terminal Configuration 還需要考慮 managed settings 的 fleet deployment 方式。IT 部門可以透過 managed-settings.json（macOS: /Library/Application Support/ClaudeCode/managed-settings.json，Linux: /etc/claude-code/managed-settings.json，Windows: C:\\ProgramData\\ClaudeCode\\managed-settings.json）統一管理全公司設備的 permission policies、allowlist/denylist commands、auto-update channels 和 network proxy settings。可以搭配 MDM（Mobile Device Management）工具如 Jamf、Intune 或 Ansible 來自動部署這份 managed config file 到所有 developer workstations。這些 managed settings 無法被使用者在 user-level 或 project-level 覆蓋，確保 enterprise security compliance 和 IT governance policy 的一致執行，是大型組織 Claude Code Terminal Configuration 的標準做法。

如果你是第一次進行 Claude Code Terminal Configuration，建議按照本文的順序逐步設定：先確認 terminal emulator 支援 256 color 和 Unicode，安裝 Nerd Font 並在 terminal preferences 設定字體，再設定 shell autocomplete（source 後測試 tab completion），接著在 ~/.claude/settings.json 設定 model、permissions 和 env block，最後根據需要設定 proxy（NODE\_EXTRA\_CA\_CERTS）或 SSH remote（SendEnv、PTY）。每完成一個步驟就用 `claude doctor` 驗證，遇到 warning 可以翻查本文對應的 troubleshooting 章節尋找解決方案。完整的 Claude Code Terminal Configuration 是每個 AI-assisted development workflow 的必備前置步驟。

## 9\. 哪裡可以找到更多 Claude Code Terminal Configuration 資源？

以下 3 支官方影片涵蓋 Claude Code Terminal Configuration 的設定流程和使用環境：

![YouTube video](https://i.ytimg.com/vi/6eBSHbLKuN0/hqdefault.jpg)

Mastering Claude Code in 30 minutes — 終端機環境設定完整流程

![YouTube video](https://i.ytimg.com/vi/gv0WHhKelSE/hqdefault.jpg)

Claude Code Best Practices — settings.json 設定與環境變數管理

![YouTube video](https://i.ytimg.com/vi/zrcCS9oHjtI/hqdefault.jpg)

Claude Code on Desktop — 桌面版終端機設定與多平台使用

- [Moksa Claude Code 完整教學系列](https://moksaweb.com/category/claude-code/)
- [Claude Code Settings 官方文件](https://docs.anthropic.com/en/docs/claude-code/settings)
- [Anthropic 官方網站](https://www.anthropic.com/)

## 10\. Claude Code Terminal Configuration 常見問題 FAQ

### Claude Code 支援哪些 terminal emulator？有沒有推薦？

Claude Code 可以在所有主流 terminal 上運作，包括 iTerm2（macOS 推薦）、Warp、Windows Terminal、VS Code Terminal、GNOME Terminal、Alacritty 等。唯一的硬性要求是終端機需要支援 256 色以上（現代 terminal 幾乎都支援），以及 Unicode 字元集。如果你在意 UI 美觀，推薦安裝一款 Nerd Font 並在 terminal 設定裡啟用。

### 為什麼 Claude Code 的圖示顯示為方塊或問號？

這是 Nerd Font 沒有正確安裝或設定的問題。需要兩個步驟：第一，下載並安裝 Nerd Font（推薦 MesloLGS NF 或 Hack Nerd Font）；第二，在你使用的 terminal emulator 設定裡把字體改成剛才安裝的 Nerd Font 名稱。光安裝字體但 terminal 還是用原本的字體，圖示一樣不會正確顯示。

### 在 Windows 上使用 Claude Code 需要特別設定什麼？

Windows 用戶需要注意幾點：第一，強烈建議安裝 WSL2，在 Linux 環境裡使用 Claude Code 可以避免很多相容性問題；第二，如果在 Windows 原生環境使用，需要安裝 Git for Windows 並在 settings.json 的 env 區塊設定 CLAUDE\_CODE\_GIT\_BASH\_PATH；第三，Windows Terminal 是最佳的 terminal 選擇。

### 如何在企業 Proxy 環境下讓 Claude Code 正常連線 Anthropic API？

設定 HTTP\_PROXY 和 HTTPS\_PROXY 環境變數指向你的 proxy 伺服器。如果 proxy 使用自簽 SSL 憑證或進行 TLS inspection，還需要設定 NODE\_EXTRA\_CA\_CERTS 環境變數指向你的 CA 憑證檔案路徑。建議把這些設定放在 settings.json 的 env 區塊。設定完後用 curl -x http://proxy:port https://api.anthropic.com 測試連線。

### SSH 遠端連線時 Claude Code 介面顯示異常或無法互動怎麼處理？

SSH 遠端使用 Claude Code 時，需要確保 SSH 連線有 PTY 分配（加 -t 旗標），否則 interactive UI 無法正常顯示；ANTHROPIC\_API\_KEY 需要傳遞到遠端環境，可以用 SSH config 的 SendEnv 指令；遠端伺服器上需要安裝相同版本的 Claude Code。另外確認遠端的 TERM 環境變數是 xterm-256color 或類似值。

### 在 tmux 或 screen 裡跑 Claude Code 時顏色不對或全是亂碼怎麼辦？

這是 terminal multiplexer 的 TERM 設定問題。在 ~/.tmux.conf 加入 set -g default-terminal "tmux-256color" 和 set -ga terminal-overrides ",xterm-256color:Tc"，然後完全重啟 tmux（kill-server 再重新開）。對於 screen，在 ~/.screenrc 加入 term xterm-256color。另外確認你的 shell profile 裡有 export TERM=xterm-256color。

### Claude Code 的 settings.json 和 shell profile 的環境變數哪個優先？

settings.json 裡 env 區塊設定的環境變數會覆蓋 shell profile 的同名環境變數（Claude Code 啟動時讀取 settings.json，覆蓋目前 process 的環境）。建議把 Claude Code 專用的行為控制環境變數（如 DISABLE\_AUTOUPDATER）放在 settings.json 的 env 區塊，把 ANTHROPIC\_API\_KEY 等敏感金鑰放在 shell profile 或 secret manager，不要放進可能被 commit 的設定檔。

### 如何確認 Claude Code Terminal Configuration 設定有沒有正確載入？

執行 claude doctor 可以診斷 Claude Code 的整體設定狀態，包括 API key 是否有效、設定檔格式是否正確、必要工具是否正確安裝。另外可以在 Claude Code 的互動模式裡輸入 /config 查看目前生效的設定值，確認每個設定都是預期的值。如果設定沒有生效，先確認 JSON 格式正確，再確認修改的是正確層級的設定檔。