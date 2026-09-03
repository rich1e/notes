---
title: >-
  Obsidian Wiki daily cron 安装（macOS launchd）
category: skills
tags: [obsidian-wiki, launchd, workflow, Claude]
sources:
  - conversation:2026-08-05
created: 2026-08-05T02:40:00Z
updated: 2026-08-05T02:40:00Z
summary: >-
  用 launchd 给 obsidian-wiki 装每日维护定时任务的完整流程与关键机制：改 LaunchAgents 副本而非 repo 模板、RunAtLoad 补跑语义、bootstrap 取代废弃的 load、幂等 zshrc 提醒、改时间需 bootout+bootstrap 重载。
provenance:
  extracted: 0.8
  inferred: 0.2
  ambiguous: 0.0
base_confidence: 0.9
lifecycle: draft
lifecycle_changed: 2026-08-05
---

# Obsidian Wiki daily cron 安装（macOS launchd）

给 [[concepts/obsidian-wiki-vault-structure|obsidian-wiki]] 装 `/daily-update` 定时任务用的是 **macOS launchd（LaunchAgent）**，不是 crontab。`daily-update` skill 的 Setup Mode 已封装大部分步骤，本页记录实机跑通时的关键机制与易错点。

## 完整流程（Setup Mode）

1. **验证三脚本存在**（在 `$OBSIDIAN_WIKI_REPO/scripts/`）：`daily-update.sh`、`com.obsidian-wiki.daily-update.plist`、`wiki-notify.sh`。repo 由 pipx 装在 `.../site-packages/obsidian_wiki/_data`。
2. **生成 plist 到 `~/Library/LaunchAgents/`**：用 `sed` 把模板里的 `OBSIDIAN_WIKI_REPO` 占位符替换成真实 repo 绝对路径，写到 LaunchAgents。
3. **加载**：`launchctl bootstrap gui/$(id -u) <plist>`。
4. **（可选）终端提醒**：把 `source .../wiki-notify.sh` 追加进 `~/.zshrc`。
5. **手动跑一次** `daily-update.sh` 初始化 state。

## 关键机制与易错点

### 1. 改的是 LaunchAgents 副本，不是 repo 模板 ^[inferred]

plist 模板在 pipx 装的 repo 里（只读心态对待，且升级会被覆盖）。安装时 `sed` 出一份**独立副本**放 `~/Library/LaunchAgents/`。**后续任何修改（改时间、翻 flag）都改这份副本**，不动 repo 模板——launchd 只认 LaunchAgents 里的这份。

### 2. `RunAtLoad` 决定错过的运行是否补跑

模板默认 `RunAtLoad` 为 `<false/>`——严格只在 `StartCalendarInterval` 指定的时刻（笔记本必须醒着）运行。改成 `<true/>` 后，**每次 load/登录时若上次错过就补跑一次**。对笔记本用户更实用（睡眠错过 9AM 不会白等一天）。

代价：`RunAtLoad=true` 时，**每次 `bootstrap`（加载/重载）都会立即触发一次脚本运行**。这不是 bug——脚本内部判断 wiki 新鲜就直接 up-to-date 退出，无副作用。

### 3. 用 `bootstrap` / `bootout`，别用废弃的 `load` / `unload`

现代 launchctl 语法：

```bash
UID_NUM=$(id -u)
# 加载
launchctl bootstrap "gui/$UID_NUM" ~/Library/LaunchAgents/com.obsidian-wiki.daily-update.plist
# 卸载
launchctl bootout "gui/$UID_NUM/com.obsidian-wiki.daily-update"
```

旧的 `launchctl load/unload` 已废弃、在新版 macOS 上时有静默失败。脚本里可以「先 bootstrap，失败再 fallback 到 legacy load」保险。

### 4. 改时间 = 编辑 plist + bootout 后 bootstrap 重载

launchd **不会热重载**磁盘上的 plist；改完必须卸了再装：

```bash
PLIST=~/Library/LaunchAgents/com.obsidian-wiki.daily-update.plist
# 改 StartCalendarInterval 里的 Hour/Minute（例：9:00 → 10:30）
perl -0pi -e 's{(<key>Hour</key>\s*<integer>)9(</integer>\s*<key>Minute</key>\s*<integer>)0(</integer>)}{${1}10${2}30${3}}' "$PLIST"
plutil -lint "$PLIST"                                    # 改完必 lint，plist 语法错会静默不跑
launchctl bootout "gui/$(id -u)/com.obsidian-wiki.daily-update" 2>/dev/null
launchctl bootstrap "gui/$(id -u)" "$PLIST"
```

`Hour`/`Minute` 都是 `<integer>`，`StartCalendarInterval` 只给 Hour+Minute 就是「每天该时刻」。

### 5. zshrc 提醒钩子要幂等、只读、静默

`wiki-notify.sh` 每次开终端都执行，所以设计成：**只读 state**、**>20h（72000s）陈旧才打印**、否则静默 `return`。追加进 `~/.zshrc` 前**先 `grep -qF "wiki-notify.sh"` 判重**，避免重复 source。

### 6. state 按 vault 路径 hash 隔离

state 存 `~/.obsidian-wiki/state/<vault-id>/`，`vault-id` 是 vault 绝对路径的 md5 前 8 位（本 vault = `3fc31535`）。三个文件：`.last_update`（epoch）、`.pending_delta`（stale 源数）、`.vault_path`。多 vault 各自独立，提醒钩子遍历所有 state 目录。

## 验证

- `launchctl list | grep obsidian` → 第二列 `0` = 上次运行成功
- 日志：`/tmp/obsidian-wiki-daily.log`（stdout）+ `.err`（stderr）
- 模拟开终端确认提醒静默：`(source .../wiki-notify.sh)` 在 wiki 新鲜时应无输出

## 卸载

```bash
launchctl bootout "gui/$(id -u)/com.obsidian-wiki.daily-update"
rm ~/Library/LaunchAgents/com.obsidian-wiki.daily-update.plist
# 再从 ~/.zshrc 删掉 wiki-notify.sh 那两行
```

## Related

- [[concepts/obsidian-wiki-vault-structure]] — 被维护的 vault 结构与系统文件
- [[skills/claude-code-settings]] — macOS 下 launchd/托管配置的同类部署思路
- [[skills/wiki-token-threshold-mechanics]] — 另一条 wiki 运维洞察（同属框架运维类 skill）
