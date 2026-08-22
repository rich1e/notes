---
title: rsync 用法详解（阮一峰博客）
category: misc
tags: [rsync, linux, file-sync, backup, ssh]
sources:
  - https://www.ruanyifeng.com/blog/2020/08/rsync.html
source_url: https://www.ruanyifeng.com/blog/2020/08/rsync.html
created: 2026-08-14T08:00:00Z
updated: 2026-08-14T08:00:00Z
summary: 阮一峰 2020 年发布的 rsync 教程汇总：安装、基本参数、排除规则、SSH 远程同步、--link-dest 增量备份脚本模式、常用配置项速查。
affinity: {}
promotion_status: misc
stub: false
provenance:
  extracted: 0.85
  inferred: 0.10
  ambiguous: 0.05
base_confidence: 0.45
lifecycle: draft
lifecycle_changed: 2026-08-14
---

# rsync 用法详解（阮一峰博客）

## Overview

阮一峰 2020-08-26 发布的 [[rsync]] 中文教程，按"简介 → 安装 → 基本用法 → 排除文件 → 远程同步 → 增量备份 → 配置项 → 参考链接"八章铺开。文章本身是参考性速查（reference），不是研究性输出（research）：原文即给 CLI 参数附解释和示例，**没有**给出实测、性能数据或与其他工具（syncthing / unison / Robocopy）的对比。

## Key Points

- `-a`（archive）= `-r` + 元数据（mtime/权限/所有者/软链接），日常同步首选 `-a` 而非 `-r`
- 源路径末尾 `/` 是行为开关：带斜杠 → 同步目录**内容**到目标；不带 → 把目录作为子目录复制到目标
- 默认增量判定只看 size + mtime；加 `-c`/`--checksum` 才按内容校验
- `--delete` 让目标成为源镜像（删除目标独有文件）；这是双向同步错觉的常见来源^[inferred]
- 远程传输默认走 SSH；`-e 'ssh -p 2234'` 用于指定端口或附加 SSH 参数
- 远程可用双冒号语法 `host::module/path` 走 rsync 守护进程（默认 873 端口），前提是远端跑 rsync daemon
- 增量备份核心是 `--link-dest DIR`：与基准目录对比，未变文件生成**硬链接**，空间成本接近增量而非全量
- 配套脚本范式：`backups/${DATETIME}/` 每次新建子目录 + `latest` 软链接始终指向最新一次 + 下次备份以 `latest` 为基准——形成自动滚动的快照链
- `-n`/`--dry-run` + `-v` 是变更前必跑组合；不带 `-n` 直接 `--delete` 是运维事故常见诱因^[inferred]
- `--exclude-from FILE` 把排除规则外置成文件，便于版本管理

## Concepts

- [[rsync]] — Linux 文件同步 CLI；增量传输、`-a` 归档模式、`--link-dest` 增量备份是其三个核心机制
- [[ssh-server-hardening]] — rsync 远程传输默认走 SSH，加固 SSH 等于加固 rsync 远程入口
- [[chezmoi-workflow]] — rsync 与 chezmoi 互斥的 dotfile 同步场景：chezmoi 走模板+加密，rsync 走纯字节镜像^[inferred]

## Entities

- [[ruanyifeng-blog]] — 中文技术博客，本条 URL 来源；产出多篇高质量 CLI/概念教程（rsync、SSH、cron 等）

## 章节速查（按原文顺序）

| 章节 | 主题 | 关键参数/示例 |
|---|---|---|
| 一、简介 | rsync 是 remote sync；增量传输是最大特点 | — |
| 二、安装 | Debian/Red Hat/Arch 三家包管理器 | apt/yum/pacman |
| 三、基本用法 | `-r`/`-a`/`-n`/`--delete`；结尾斜杠规则 | `rsync -av --delete source/ destination` |
| 四、排除文件 | `--exclude`/`--include`/`--exclude-from` | `--exclude='*.txt'`、Bash 大括号扩展 |
| 五、远程同步 | SSH 协议 / rsync 守护进程双冒号 | `-e 'ssh -p 2234'`、`host::module/destination` |
| 六、增量备份 | `--link-dest` 基准目录 + 硬链接 + `latest` 软链脚本 | 完整 Bash 脚本示例（备份 $HOME） |
| 七、配置项 | 30+ 参数速查表 | `-a`/`--delete`/`--bwlimit`/`--append`/`-P` 等 |
| 八、参考链接 | DigitalOcean、HowToForge、linuxconfig 三方英文教程 | — |

## Open Questions

- 阮一峰未涉及 rsync 与 **syncthing** / **unison** 双向实时同步的取舍——双向同步、超大规模目录（百万级 inode）场景下 rsync 是否仍是首选？^[inferred]
- Windows 平台等价物（cwRsync、Robocopy、SyncThing）未提及，但运维场景必然涉及^[ambiguous]
- `--link-dest` 硬链接策略对备份目录所在文件系统的 inodes 配额是否有要求？原文假定 ext4 类无限制^[ambiguous]

## Related

- [[ssh-server-hardening]] — rsync `-e ssh` 复用同一通道
- [[rsync]] — 主概念页
- [[ruanyifeng-blog]] — 来源博客实体页
- 原文参考链接：DigitalOcean [How To Use Rsync](https://www.digitalocean.com/community/tutorials/how-to-use-rsync-to-sync-local-and-remote-directories-on-a-vps)、HowToForge [Mirror Your Web Site With rsync](https://www.howtoforge.com/mirroring_with_rsync)、linuxconfig.org [Incremental Backups](https://linuxconfig.org/how-to-create-incremental-backups-using-rsync-on-linux)