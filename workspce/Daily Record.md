---
banner: "https://images.unsplash.com/photo-1462642109801-4ac2971a3a51?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1073&q=80"
banner_y: 0.504
---

> Just keep doing.

## Routine

```sh
brew update && brew upgrade && brew cleanup
```

```sh
omz update
```

Apps
- iTerm2
- Clash
- Zotero
- Obsidian (update before opening)
- WeChat for Enterprise
- Oulu Dictionary (Eudic)
- Amphetamine

## Quick Links

| 主题 | 笔记 |
|------|------|
| Shell 脚本 / node_modules | [[work-records/shell-scripts]] |
| Git 操作手册 | [[work-records/git-flow]] |
| Node / npm / pnpm | [[work-records/node-commands]] |
| Mac 技巧 | [[work-records/mac-tips]] |
| Windows 环境 / Scoop | [[work-records/windows-settings]] |
| 代理工具 | [[work-records/proxy]] |

## Daily Log

```dataview
table date AS 创建时间, file.mtime AS 修改时间
from ""
where contains(file.path, "daily")
sort date desc
```
