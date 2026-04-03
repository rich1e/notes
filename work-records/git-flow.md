# Git Flow

## 修改 Commit

```git
# 显示指定提交者信息
git commit -m 'your commit' --author='your-name <your-email>'
# 修改上次提交的 author 信息
git commit --amend --author='your-name <your-email>'
# 修改历史提交
git rebase -i your-branch
# 修改所有的 commit
git rebase -i --root
# 修改 commit 时间为当前时间
git commit --amend --date=now --no-edit
```

空提交

```git
git commit --allow-empty -m 'Release Orca by 202303311015'
```

没有消息

```git
git commit --allow-empty-message -m ''
```

## 查看日志

获取 log 中最近10小时的 commit

```git
git log --author=gongyuqi --oneline --since='10 hours ago' --grep="into 'testDev'" --invert-grep
```

显示最近一次提交的 commit ID 的缩写形式，并复制到剪切板

```git
git log -1 --pretty=format:%h | pbcopy
```

查询 log 中匹配的 keyword

```sh
git log --all -i --grep='keyword'
```

## 分支管理

删除冗余的本地分支

```git
git branch --merged | grep -v 'master\|dev\|testDev' | xargs git branch -D

# PowerShell
git branch -D @(git branch \| select-string -NotMatch "master" \| Foreach {$_.Line.Trim()})|
```

Ref：
[How to delete all merged local branches in Git with PowerShell - Stack Overflow](https://stackoverflow.com/questions/51171479/how-to-delete-all-merged-local-branches-in-git-with-powershell)
[PowerShell command to delete all branches except master](https://gist.github.com/jseed/5d022570ea52ee09a8f43913214496f1)

## 文件操作

显示文件的每一行最后修改的版本和作者

```git
git blame -L start,end <filename>
```

导出文件

```git
git archive --format=zip main > file.zip
```

文件比较

```git
# 显示所有修改的文件的文件名列表
git diff --name-only
# 查看不包含".txt"扩展名的文件
git diff --name-only | grep -v "\.txt$"
# 查看每个修改的类型（例如添加、修改或删除）
git diff --name-status
```

文件暂存

```git
# 暂存所有的文件，包括 untracked 的文件，并命名为 msg
git stash save -u 'msg'
# 拿出某个文件的修改
git checkout <stash@{n}> -- <file-path>
```

## 文件恢复 & 回滚

文件恢复

```git
# 默认就是 --mixed
git reset <commit-id>
git reset --mixed
# 撤销上次commit，保留文件
git reset --soft head^
# 撤销上次commit，删除提交的文件
git reset --hard head^
```

恢复特定 commit 中的某个文件

```git
git checkout <目标 commit> -- <文件>
```

文件回滚

```git
# 仅在工作区修改，还没有提交暂存区和本地仓库
git checkout -- 文件名
# 添加到暂存区，但还未提交 commit
git reset HEAD 文件名
# 已提交commit，但还没有 push 时
git reset <要回滚到的 commit>
# 已 push 到远端时
git revert
```

复制提交中的代码而不想创建新的提交

```git
git cherry-pick --no-commit <commit-id>
```

## 清理

```git
# 删除 untracked 的文件和目录
git clean -df
# 删除被忽略的文件(.gitignore中指定的)
git clean -Xf
# 删除未被版本控制的，包括忽略的和未忽略的
git clean -xf
# 显示哪些文件会被删除
git clean -n
```

## Tag

```git
# 获取远程tag
git fetch origin tag v1.0.1
# 强制刷新tag命令
git fetch --tags -f
# 基于tag签出分支
git switch --detach <tag>
```

> [github - Switch to another Git tag - Stack Overflow](https://stackoverflow.com/questions/4330610/switch-to-another-git-tag)

## Ref

[[buckets/daily/2023-04-18_Tuesday]]
[[buckets/daily/2023-03-31_Friday]]

[Git使用的奇技淫巧 | Escape](https://www.escapelife.site/posts/7a4a6df7.html#toc-heading-3)
[Git 常用指令 - 潘忠显](https://panzhongxian.cn/cn/2021/01/git-common-commands/)

## 相关笔记

- [[work-records/git-blame]] — git blame 逐行追溯作者
- [[work-records/git-open]] — git open 快速打开仓库页面
- [[work-records/Git 分支管理建议]] — GitLab Flow 分支管理规范
- [[work-records/git-remote-host-identification-has-changed]] — SSH 远程主机认证问题
