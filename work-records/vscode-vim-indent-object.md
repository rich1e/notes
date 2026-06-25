#vscode #vim 

`<operator>ii` - 当前缩进块
`<operator>ai` - 当前缩进块和上一行
`<operator>aI` - 当前缩进块和下一行

## 代码缩进

![[assets/work-records/vscode-vim-indent-object/IMG-20260430171340160.gif]]

`>ii` - 缩进当前缩进块
`>ai` - 缩进当前缩进块和上一行
`>aI` - 缩进当前缩进块和下一行

## 配合 `<Opeator>` 操作

![[assets/work-records/vscode-vim-indent-object/IMG-20260430171340284.gif]]

`ci'` - 删除 `''` 中的内容，并切换到 `Insert mode
`ci[` - 删除 `[]` 中的内容，并切换到 `Insert mode
`ci{ - 删除 `{}` 中的内容，并切换到 `Insert mode`

就像 `vim-text-object` 一样，这操作可以与 `operator` （例如 `d` `c` `s` `x` ）以及在 `visual mode` 下一起使用。

在 `visual mode` 下，可以重复命令，这具有迭代的效果，从而增加了所选的缩进范围。指定 `count` 可用于实现相同的效果。

参考

[GitHub - VSCodeVim/Vim: Vim for Visual Studio Code](https://github.com/VSCodeVim/Vim/#vim-indent-object)
[GitHub - michaeljsmith/vim-indent-object](https://github.com/michaeljsmith/vim-indent-object)
[Operate on an Indented Block of Lines with vim-indent-object | seanh.cc](https://www.seanh.cc/2020/08/08/vim-indent-object/)
[My Experience Using Vim Keybindings In VSCode](https://michaelychen.medium.com/my-experience-using-vim-keybindings-in-vscode-ea6d335aa155)
[开发利器：快速删除一个函数 | Just Vim It](https://vim.nauxscript.com/vim/day-16.html)

## 相关笔记

- [[work-records/vscode-vim]] — Vim 基础概念（motion / operator / leader）
- [[work-records/vscode-vim-text-object]] — 文本对象（indent-object 是其扩展）
- [[work-records/vscode-vim-surround]] — Surround 成对符号编辑