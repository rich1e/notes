# Shell Scripts

## 目录树

以树形结构列举目录

```sh
tree -L 2 -I 'node_modules|dist|example|patches' --dirsfirst
```

```sh
exa -T --level=6 --ignore-glob="node_modules|mock|views|example|helper|public" --git-ignore --sort=ext
```

[tree 命令，Linux tree 命令详解：树状图列出目录的内容](https://wangchujiang.com/linux-command/c/tree.html)

## node_modules

查询目录下所有的 `node_modules` 目录和所占空间

```sh
find . -name "node_modules" -type d -prune | xargs du -chs
```

```powershell
FOR /d /r . %d in (node_modules) DO @IF EXIST "%d" echo %d"
```

删除目录下所有的 `node_modules` 目录

```sh
find . -name 'node_modules' -type d -exec rm -rf '{}' +
```

```sh
# 命令拆解注释
# . 当前目录
# -name 名字匹配，指定字符串作为寻找文件或目录的范本样式；
# -type 查询文件类型。 -d 就是目录
# -exec 就是匹配后执行一些命令
# rm -rf '{}' 删除匹配到到('{}')
# + 是个骚操作
# 一个-exec只能执行一个命令，而且必须在命令后面加上终结符，终结符有两个："；"和"+"。
# 其中";" 会对每一个find到的文件去执行一次cmd命令。而"+"让find到的文件一次性执行完cmd命令。
```

```sh
find . -name 'node_modules' | xargs rm -rf
```

```powershell
FOR /d /r . %d in (node_modules) DO @IF EXIST "%d" rm -rf "%d"
```

[删除所有本地下载的 node_modules 依赖目录以节省磁盘空间](https://gist.github.com/mehunk/4caa299beaf05905cfe541ea8fd44b22)

[一条命令删除目录下的所有node\_modules | Mulianju](https://www.mulianju.com/delete-all-node_modules/)

[前端不会Shell？Shell 命令只会 cd 的小伙伴，这篇文章你真的得看了 - 掘金](https://juejin.cn/post/7274346507037081640)

## 相关笔记

- [[buckets/work-records/command-tree]] — tree 命令详解
- [[buckets/work-records/command-exa]] — exa 命令（本文用到）
- [[buckets/work-records/node-commands]] — Node/npm/pnpm 包管理命令
