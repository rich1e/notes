---
title: rsync
category: concept
tags: [rsync, linux, file-sync, backup, cli]
sources:
  - https://www.ruanyifeng.com/blog/2020/08/rsync.html
created: 2026-08-14T08:00:00Z
updated: 2026-08-14T08:00:00Z
summary: Linux 增量文件同步 CLI：本地/远程同步、镜像同步、增量备份；核心机制是 size+mtime 增量判定、-a 归档模式、--link-dest 硬链接增量备份。
provenance:
  extracted: 0.70
  inferred: 0.25
  ambiguous: 0.05
base_confidence: 0.45
lifecycle: draft
lifecycle_changed: 2026-08-14
tier: supporting
---

# rsync

**rsync** 是 Linux 平台的增量文件同步 CLI 工具。三大核心机制:

1. **增量传输**:默认按 size + mtime 判定文件是否变动,只传差异部分（加 `-c` 才按 checksum）
2. **`-a` 归档模式**:递归 + 保留元数据（mtime/权限/所有者/软链接），日常首选
3. **`--link-dest DIR`**:增量备份的硬链接机制——未变文件不复制、只硬链接到基准目录

## 三种典型用法

| 场景 | 命令模式 | 关键参数 |
|---|---|---|
| 本地镜像 | `rsync -av --delete src/ dst/` | `--delete` 让目标=源 |
| 远程推送 | `rsync -av src/ user@host:dst/` | 默认 SSH,`-e ssh -p PORT` 改端口 |
| 增量备份 | `rsync -a --delete --link-dest baseline src/ snapshot/` | 配合 `latest` 软链形成滚动快照 |

## 关键陷阱

- **结尾斜杠**: `rsync -a src dst` 与 `rsync -a src/ dst` 行为不同——前者把 src 作为子目录复制到 dst,后者把 src 内容复制到 dst
- **`--delete` 没有 `-n` 预览**:直接跑会删除目标独有文件,先 `rsync -anv` 预览
- **`--link-dest` 假定目标文件系统支持硬链接**:网络文件系统/部分容器文件系统可能拒绝^[inferred]

## 相关

- [[ssh-server-hardening]] — `-e ssh` 复用同一通道;加固 SSH 等于加固 rsync 远程入口
- [[chezmoi-workflow]] — dotfile 场景的另一种思路:模板+加密,不走纯字节镜像

## 源

- 阮一峰博客:[[web-www-ruanyifeng-com-blog-2020-rsync]]