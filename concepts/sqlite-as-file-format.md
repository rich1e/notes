---
title: SQLite 作为文件格式
category: concepts
tags:
  - sqlite
  - database
  - file-format
  - architecture
summary: SQLite 不仅是数据库，更是比原始文件系统更好的通用文件格式：≤100KB blob 读写比文件系统快 35%，原子多文件更新，无崩溃时部分写，单文件备份，「数据库即 fopen()」。
sources:
  - "https://joecode.com/2026-08-19-sqlite3/"
  - "https://sqlite.org/whentouse.html"
created: 2026-08-26T00:00:00Z
updated: 2026-08-26T00:00:00Z
tier: supporting
lifecycle: draft
lifecycle_changed: "2026-08-26"
base_confidence: 0.70
provenance:
  extracted: 0.80
  inferred: 0.18
  ambiguous: 0.02
relationships:
  - target: "[[entities/sqlite]]"
    type: derived_from
  - target: "[[concepts/database-as-platform]]"
    type: related_to
---

# SQLite 作为文件格式

> SQLite 的设计者将其描述为"更好的 `fopen()`"——这不是玩笑，而是一个设计目标。

SQLite 官方基准《35% Faster Than The Filesystem》表明：对于 ≤100KB 的小 blob，SQLite 的读写**比操作系统原生文件系统更快**，且磁盘占用少约 **20%**。

## 为什么 SQLite 比文件系统更快（小 blob 场景）

### 文件系统的开销结构

每次文件访问 = `open()` + 读/写 + `close()` + 可能的目录遍历

- **`open()` 不是免费的**：内核要解析路径、检查权限、分配文件描述符
- **目录条目**：4 百万文件的目录（如图床、CDN 缓存）会使 `ls`、`rsync`、备份工具崩溃
- **部分写**：crash 可能留下半截文件，应用需要自己处理

### SQLite 的开销结构

访问 BLOB 列 = 一个已打开的文件句柄 + B-tree 查找

- **文件句柄常驻**：进程持有 db 文件，无重复 open/close
- **B-tree 定位**：O(log n)，索引即目录
- **原子性**：多 blob 更新在同一事务内，崩溃不留部分写

## 文件格式的优势清单

| 问题 | 原始文件系统 | SQLite |
|---|---|---|
| 原子多文件更新 | 需要 WAL/fsync 组合手写 | 内置事务 |
| 崩溃时部分写 | 应用负责处理 | 不可能发生（事务保证）|
| 文件名转义/特殊字符 bug | 常见坑（空格、Unicode、`..`）| 无文件名概念 |
| 目录 entry 数量 vs 性能 | 数百万文件时严重退化 | 行数不影响结构 |
| `rsync` 慢因 inode 数量 | 是 | 一个文件，秒级 |
| 备份 | `rsync`（复杂）或 tar | `cp`/`mv`/Litestream |
| 元数据查询 | `find + stat`（慢）| SQL 查询（快）|

## 适用场景

### 强烈推荐
- **小文件大量堆积**：thumbnail、icon、头像、小附件（<100KB）
- **配置/状态文件**：替代多个 JSON/YAML 文件的"一个配置目录"
- **应用内部数据格式**：浏览器历史（Chrome 用 SQLite）、IDE 索引、手机 App 状态
- **离线/嵌入式应用**：RAG 向量 + 文档 + 元数据打包成一个文件发布

### 不推荐
- **大 blob**（>100KB）：SQLite 不擅长，此时直接文件系统或对象存储更合适
- **流式写入**：视频、大二进制流，SQLite 会把整个 blob 加载进内存

## 存储建议

```sql
CREATE TABLE assets (
  id       INTEGER PRIMARY KEY,
  name     TEXT    NOT NULL,
  mime     TEXT    NOT NULL,
  data     BLOB    NOT NULL,  -- 存 payload，≤100KB 最优
  size     INTEGER NOT NULL,
  created  TEXT    NOT NULL DEFAULT (datetime('now'))
);
```

序列化建议：MessagePack 或 CBOR（比 JSON 紧凑），客户端反序列化。SQLite 团队自己的建议是 Flatbuffers（零拷贝反序列化）。

## 生产中的例子

- **Chrome/Firefox/Safari**：历史记录、书签、Cookie = SQLite 文件
- **macOS/iOS 系统**：联系人、日历、邮件附件元数据 = SQLite
- **Android**：通讯录、短信、设置 = SQLite
- **Obsidian 本身**：本 vault 的 `.obsidian/` 目录内部索引 = SQLite

## 相关

- [[entities/sqlite]]
- [[concepts/database-as-platform]]
- [[references/sqlite-for-everything]]
- [[synthesis/concepts-sqlite-as-file-format × concepts-durable-session-log]] — synthesis: SQLite fopen() 哲学与 session log 可重建性的交汇
