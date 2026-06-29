---
title: 终端中播放本地音乐（macOS）
category: skills
tags:
  - macos
  - cli
  - tools
  - shell
summary: 用 macOS 内置的 afplay + shell 函数实现终端随机播放本地音乐，支持关键字检索、切歌、暂停、自动续播。
sources:
  - http://idle.systems/posts/terminal_music.html
created: 2026-06-29
updated: 2026-06-29
tier: supporting
lifecycle: draft
lifecycle_changed: "2026-06-29"
base_confidence: 0.67
provenance:
  extracted: 0.90
  inferred: 0.08
  ambiguous: 0.02
relationships:
  - target: "[[skills/tmux]]"
    type: related_to
---

# 终端中播放本地音乐（macOS）

macOS 内置 `afplay` 命令行音频播放器，无需安装第三方软件。

## 完整 .zshrc 配置

将以下函数加入 `~/.zshrc`，音乐文件放在 `~/Music/` 目录：

```sh
BYel='\e[0;33m'

# 核心播放函数（随机 + 关键字检索 + 自动续播）
function music_by_keyword() {
    m_path=~/Music/
    keyword="."                          # 默认播放所有歌曲
    if [ -n "$1" ]; then
        keyword="$1"
    fi

    song_num="$(ls $m_path | grep -i -e $keyword | wc -l)"
    while [ 1 ]; do
        dummy1=$((RANDOM))
        timestamp=$(date +%s)
        dummy=$(($dummy1*$timestamp))
        song_index=$(($dummy%$song_num+1))

        song="$(ls $m_path | grep -i -e $keyword | sed -n "$song_index"p)"
        echo -e "${BYel}$song"
        afplay "$m_path$song"            # 不加 & —— 等歌播完再播下一首
        wait
    done
}

# 对外暴露的命令
function m() {   music_by_keyword $1 &; }  # 后台启动，支持关键字
function n() {   # 切歌（下一首）
    pid="$(ps -ef | grep afplay | grep -v grep | head -1 | awk '{print $2}')"
    kill -INT $pid
}
function mm() {  # 完全停止
    pid="$(ps -ef | grep afplay | grep -v grep | head -1 | awk '{print $2}')"
    ppid="$(ps -ef | grep afplay | grep -v grep | head -1 | awk '{print $3}')"
    kill -INT $ppid && kill -INT $pid
}
function ms() {  # 暂停
    pid="$(ps -ef | grep afplay | grep -v grep | head -1 | awk '{print $2}')"
    ppid="$(ps -ef | grep afplay | grep -v grep | head -1 | awk '{print $3}')"
    kill -TSTP $pid && kill -TSTP $ppid
}
function mc() {  # 继续播放
    pid="$(ps -ef | grep afplay | grep -v grep | head -1 | awk '{print $2}')"
    ppid="$(ps -ef | grep afplay | grep -v grep | head -1 | awk '{print $3}')"
    kill -CONT $pid && kill -CONT $ppid
}
```

## 使用方式

| 命令 | 效果 |
|------|------|
| `m` | 随机播放 `~/Music/` 下所有歌曲（后台，自动续播） |
| `m beatles` | 播放文件名包含 "beatles" 的歌曲（支持正则） |
| `n` | 切到下一首 |
| `mm` | 完全停止 |
| `ms` | 暂停 |
| `mc` | 继续播放 |

## 设计要点

- **随机性**：`$((RANDOM * timestamp % song_num))` 避免连续切歌时随机性退化为顺序播放
- **后台运行**：整个 `music_by_keyword` 函数后台运行（`m() { ...$1 &; }`），当前终端仍可继续工作
- **自动续播**：`while [ 1 ]` 循环 + `wait` 实现播完自动播下一首
- **跨终端控制**：通过 `ps` 找到 `afplay` PID，可在任意终端窗口执行 `n`/`mm`/`ms`/`mc`

## 相关页面

- [[skills/tmux]] — 结合 tmux 可以专开一个 pane 显示当前播放状态
